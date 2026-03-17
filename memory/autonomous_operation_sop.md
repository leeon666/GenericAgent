# 自主行动 SOP

⚠️ **路径警告**：autonomous_reports 在 temp/ 下，用`./autonomous_reports/`访问，**不是**`../memory/autonomous_reports/`或`../autonomous_reports/`！TODO在cwd下。
报告存于 `./autonomous_reports/`，文件名 `RXX_简短描述.md`（XX从 history.txt 推断自增）。

授权你进行自主行动，只要不对环境造成副作用都可进行。

## 任务选择
- 有 `./TODO.txt`（temp根目录）未完成条目 → 取**一条**，直接进入执行，其他条目下次执行
- 无 TODO → 读 `autonomous_operation_sop/task_planning.md` 规划，下次执行
- 不连续两次选相同子任务

价值公式：**「AI训练数据无法覆盖」×「对未来协作有持久收益」**

## 执行

**启动**：
- update_working_checkpoint: `自主行动｜报告→./autonomous_reports/R{XX}_简短描述.md｜≤30回合｜收尾：重读sop，写报告+更新history+标记TODO | 报告严禁放错位置`
- 读 `./autonomous_reports/history.txt` 推断下一编号RXX + 了解历史避免重复

**执行**：
- ≤30回合，小步快跑，边探测边实验
- 用临时脚本验证假设；禁只读即下结论，完整验证再写报告
- 即使失败也记录实验过程和结果，失败报告同样有价值
- 用户不在线，遇到需要决策的问题写入报告待审，不要卡住

**收尾（三件事缺一不可）**：
1. 写报告 `./autonomous_reports/R{XX}_简短描述.md`，格式简洁仅关键发现详述；若有记忆更新建议，附在报告末尾
2. 更新 `./autonomous_reports/history.txt`（prepend一条：`RXX | 日期 | 类型 | 主题 | 结论`，严格单行，先读此文件头几行了解格式）
3. 在 `./TODO.txt`（temp根目录）中将已完成条目标记为 `[x]`

## 权限边界
- 无需批准：只读探测、cwd内写操作/脚本实验
- 需写入报告待审：修改 global_mem / memory下SOP、安装软件、外部API调用、删除非临时文件
- 绝对禁止：读取密钥、修改核心代码库、不可逆危险操作

## 等待用户审查
- 用户归来后审查报告，决定批准、修改或拒绝方案