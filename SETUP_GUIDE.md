# GenericAgent 配置说明

## ✅ 配置完成状态

### 1. API 配置
已创建 `mykey.py` 配置文件,包含:

**主 API (iflow):**
- 端点: `https://apis.iflow.cn/v1`
- API Key: `sk-b2823ce670237eb624a445dcd284db91`
- 模型: `qwen3-coder-plus`

**备用 API (iflow 第二个 Key):**
- API Key: `sk-487ec26566d58183533b9ed93119f266`

**备用 API (newx):**
- 端点: `https://newx.icqq.asia/v1`
- API Key: `sk-VAeoDMxucIwZxbWdnz9njLmTQIIVFX50sCJWeCvJA8Xr4KrR`
- 模型: `deepseek-chat`

### 2. 依赖安装
已安装必要依赖:
- ✅ streamlit
- ✅ pywebview
- ✅ requests

### 3. 启动脚本
已创建 `start.bat` 启动脚本

---

## 🚀 启动方式

### 方式 1: 使用启动脚本 (推荐)
双击运行 `start.bat`,选择启动模式:
- **CLI 模式**: 命令行交互界面
- **GUI 模式**: 桌面悬浮窗界面

### 方式 2: 命令行启动
打开命令提示符,切换到项目目录:

```cmd
cd C:\Users\40868\Downloads\Compressed\GenericAgent-main
```

**CLI 模式:**
```cmd
python agentmain.py
```

**GUI 模式:**
```cmd
python launch.pyw
```

---

## 📋 可用模型列表

### iflow API
- ✅ `qwen3-coder-plus` (当前使用)
- `qwen3-vl-plus`
- `kimi-k2-0905`
- `deepseek-r1`
- `deepseek-v3.2`
- `deepseek-v3`
- `iflow-rome-30ba3b`

### newx API
- `deepseek-chat`
- `deepseek-chat-search`
- `deepseek-reasoner`
- `deepseek-reasoner-rearch`

---

## 🔄 切换模型

编辑 `mykey.py` 文件,修改 `model` 参数:

```python
# 切换到 deepseek-v3.2
oai_config = {
    'apikey': 'sk-b2823ce670237eb624a445dcd284db91',
    'apibase': 'https://apis.iflow.cn/v1',
    'model': 'deepseek-v3.2',  # 修改这里
    ...
}

# 或切换到 deepseek-chat (newx API)
oai_config_newx = {
    'apikey': 'sk-VAeoDMxucIwZxbWdnz9njLmTQIIVFX50sCJWeCvJA8Xr4KrR',
    'apibase': 'https://newx.icqq.asia/v1',
    'model': 'deepseek-chat',
    ...
}
```

---

## 💡 使用建议

### 第一次启动后

1. **解锁 PowerShell 执行权限**
   ```
   请帮我当前用户解锁 powershell 的 ps1 执行权限
   ```

2. **配置 Everything 文件搜索**
   ```
   安装并配置 everything 命令行工具进PATH
   ```

3. **解锁 Web 工具**
   ```
   执行 web setup sop 解锁 web 工具
   ```

4. **安装常用工具**
   ```
   安装常用 Python 自动化包
   ```

5. **配置视觉能力**
   ```
   配置截图与 OCR 工具，解锁你的屏幕视觉
   ```

---

## 🎯 GenericAgent 特点

- **极简架构**: 仅 ~3,300 行核心代码
- **自我进化**: 自动沉淀 Skills,形成专属技能树
- **系统级控制**: 浏览器、终端、文件系统、键鼠、屏幕
- **多平台支持**: Windows / macOS / Linux / Android
- **多 Bot 接口**: QQ / 飞书 / 企业微信 / 钉钉 / Telegram

---

## 📚 文档

- 快速开始: `README.md`
- 新手引导: `WELCOME_NEW_USER.md`
- 快速入门 PDF: `QUICK_START.pdf`

---

## ⚠️ 注意事项

1. **首次启动**: 可能需要几秒钟初始化
2. **代理设置**: 如需代理,编辑 `mykey.py` 中的 `proxy` 参数
3. **模型选择**: `qwen3-coder-plus` 适合代码任务,`deepseek-reasoner` 适合推理任务
4. **API 配额**: 注意各 API 的调用限制

---

## 🔧 故障排除

**问题: 找不到模块**
```cmd
pip install streamlit pywebview requests
```

**问题: API 调用失败**
- 检查 `mykey.py` 中的 API Key 是否正确
- 检查网络连接
- 尝试切换到备用 API

**问题: GUI 无法启动**
- 使用 CLI 模式: `python agentmain.py`
- 或安装额外依赖: `pip install pywebview

---

## 📞 支持

- GitHub: https://github.com/lsdefine/GenericAgent
- 微信交流群: 见 `assets/images/wechat_group.jpg`

---

**配置完成时间**: 2026-03-17
**配置文件位置**: `C:\Users\40868\Downloads\Compressed\GenericAgent-main\mykey.py`
