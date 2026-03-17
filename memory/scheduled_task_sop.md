# 定时任务 SOP

目录：`../sche_tasks/` 放任务定义JSON，`../sche_tasks/done/` 放执行报告

## 任务JSON格式（*.json）
```json
{"schedule":"08:00", "repeat":"daily", "enabled":true, "prompt":"..."}
```
repeat可选：daily | weekly | monthly | once | every_Nh（每N小时）| every_Nd（每N天）

## 触发流程
1. scheduler.py（reflect/）每60秒轮询 sche_tasks/*.json
2. 条件全满足才触发：enabled=true + 当前时间≥schedule + 冷却时间已过（基于done/最新报告时间戳）
3. 触发时拼prompt，含报告路径 `../sche_tasks/done/YYYY-MM-DD_任务名.md`
4. **收到任务后第一件事**：用 update_working_checkpoint 记录报告目标文件路径，防止长任务执行中遗忘
5. 执行完毕后将报告写入上述路径（scheduler靠此文件判断今天已执行）

## 注意
- once类型：执行一次后冷却100年（实际效果为永久跳过）
- 任务文件只管"干什么"，报告路径由scheduler自动生成注入prompt
- sche_tasks目录在../，即code root下