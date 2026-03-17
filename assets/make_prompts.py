import sys, os, re
import pyperclip
import json, time
from pathlib import Path
import subprocess
import tempfile
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from llmcore import SiderLLMSession, LLMSession, ToolClient


ask = SiderLLMSession().ask


def generate_tool_schema():
    """
    通过代码内省，将 Handler 的逻辑映射为高语义的工具描述。
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, '../ga.py'), 'r', encoding='utf-8') as f:
        ga_code = f.read()
    # 极简且具备高度概括能力的元 Prompt
    meta_prompt = f"""
# Role
你是一个具备深度推理能力的 AI 系统架构师。你将通过阅读 `GenericAgentHandler` 源码，构建其对应的工具能力矩阵。

# Task
分析下方的源码，并输出 OpenAI Tool Schema。在输出 JSON 之前，你必须进行内部思考（Thinking Process）。

# Thinking Process Requirements
在 `<thinking>` 标签中，请按顺序分析：
1. **核心工具链识别**：识别所有 `do_xxx` 方法，并分析它们依赖的底层 Utility 函数。
2. **内容溯源审计**：重点分析哪些工具是从 `response.content` 提取核心逻辑（如代码块）的。对于这些工具，确认在 Schema 参数中排除掉对应的字段。
3. **调用策略推导**：分析工具间的协作关系（例如 `file_read` 如何为 `file_patch` 提供定位）。
4. **兜底逻辑确认**：明确某些特殊万能工具在系统中的保底角色，快速工具无法执行的操作由保底工具执行，但正常应优先使用方便的工具。
5. **注释审阅**：结合函数注释，理解每个工具的使用限制，其中的重要信息务必反映在工具描述中（如长度限制等）。
注释中的重要信息务必反映在工具描述中。
注释中的重要信息务必反映在工具描述中。

# Tool Schema Formatting Rules
- **参数对齐**：仅包含 `do_xxx` 方法中通过 `args.get()` 显式获取的参数。
- **高引导性描述**：描述应包含“何时调用”以及“如何根据反馈修正”，需要注意函数的注释事项。
- **输出格式**：先输出 `<thinking>` 块，然后输出 ```json 块。

# Source Code
{ga_code}

# Output
请开始思考并生成：
"""
    
    # 假设 ask 是你已经封装好的 LLM 调用接口
    raw_response = ask(meta_prompt, model="gemini-3.0-flash")
    print(raw_response)
    
    # --- 健壮的 JSON 解析逻辑 ---
    try:
        # 1. 清除 Markdown 围栏
        clean_json = raw_response.strip()
        if clean_json.startswith("```"):
            # 兼容 ```json 和 ``` 
            clean_json = re.sub(r'^```(?:json)?\s*', '', clean_json)
            clean_json = re.sub(r'\s*```$', '', clean_json)
        
        # 2. 移除可能的非 JSON 前导/后缀文字（如果有的话）
        start_idx = clean_json.find('[')
        end_idx = clean_json.rfind(']') + 1
        if start_idx != -1 and end_idx != -1:
            clean_json = clean_json[start_idx:end_idx]
            
        final_schema = json.loads(clean_json)
        
        if final_schema:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            with open(os.path.join(script_dir, 'tools_schema.json'), 'w', encoding='utf-8') as f:
                json.dump(final_schema, f, indent=2, ensure_ascii=False)
            print("✅ 成功从代码内省生成 Schema 并持久化。")
        return final_schema

    except Exception as e:
        print(f"❌ 解析 Schema 失败: {e}\n原始响应: {raw_response}")
        return None


def make_system_prompt(ga_code_path=None):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if ga_code_path is None:
        ga_code_path = os.path.join(script_dir, '../ga.py')
    with open(ga_code_path, 'r', encoding='utf-8') as f:
        ga_code = f.read()

    # 这个元 Prompt 的目标是生成“世界观”而非“说明书”
    meta_prompt = f"""
# Role
你是一个 AI 架构师。请阅读下方的工具库源码，为 Agent 生成一份【系统级认知指令 (System Prompt)】。

# Task
基于代码逻辑，定义 Agent 的“能力边界”和“行动协议”。

# Requirements (Crucial)
1. **打破预训练偏见**：针对模型常说的“我只是 AI，不能操作网页/文件”进行修正。明确告诉它：你现在拥有物理操作权限，工具设计保证了所有权限做所有事情。
2. **避开冗余**：不要重复 Tool Schema 里的参数细节。
3. **能力边界定义**：
   - 网页操作：它不是通过“想象”上网，而是通过实时的浏览器读写。
   - 文件操作：它拥有物理文件读写权限，且遵循“先读后写”的稳健性原则。
   - 保底逻辑：当专用工具失效时，使用 `code_run` 编写脚本解决一切。
   - 特殊的update_plan（仅在复杂任务时使用）和ask_user（用户也是有效资源）工具。
4. **行动协议**：
   - 必须在行动前进行<thinking>

我后面还会附上具体的工具描述和Schema，所以不要重复。
主要以世界观为主，不要纠结于具体工具。

# Input Source Code
{ga_code}

# Output
仅输出 System Prompt 的正文，语气要果断、指令化。
"""
    print("🧠 正在重塑 Agent 世界观 (Generating System Prompt)...")
    # 调用你的 llmclient.ask
    system_prompt_content = ask(meta_prompt)
    print("📝 生成的 System Prompt 内容如下：\n")
    print(system_prompt_content)
    clean_content = re.sub(r'<[^>]+>', '', system_prompt_content)
    with open(os.path.join(script_dir, 'sys_prompt.txt'), 'w', encoding='utf-8') as f:
        f.write(clean_content)
    return clean_content

# --- 主逻辑 ---
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python make_prompts.py [schema|prompt]")
        sys.exit(1)
    
    cmd = sys.argv[1].lower()
    if cmd == "schema":
        generate_tool_schema()
    elif cmd == "prompt":
        make_system_prompt()
    else:
        print(f"Unknown command: {cmd}")
        print("Available commands: schema, prompt")