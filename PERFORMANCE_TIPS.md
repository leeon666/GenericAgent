# Streamlit Performance Optimization Guide

## 卡顿问题解决方案

### 1. 已自动应用的优化
✅ 创建了 `.streamlit/config.toml` 配置文件
✅ 添加了 `run_streamlit_fast.bat` 优化启动脚本

### 2. 手动优化建议

#### 重启 Streamlit
如果当前页面卡顿,请按以下步骤重启:
1. 关闭当前的浏览器标签页
2. 在命令行窗口按 `Ctrl+C` 停止 Streamlit
3. 双击运行 `run_streamlit_fast.bat`

#### 浏览器优化
- 使用 Chrome 或 Edge 浏览器
- 清除浏览器缓存: `Ctrl+Shift+Delete`
- 关闭其他占用资源的浏览器标签页
- 尝试无痕模式: `Ctrl+Shift+N`

#### 系统资源检查
- 打开任务管理器 (`Ctrl+Shift+Esc`)
- 检查 CPU 和内存使用情况
- 关闭其他占用大量资源的程序

### 3. 配置文件说明

`.streamlit/config.toml` 已启用:
- 禁用 CORS 和 XSRF 保护 (减少安全检查开销)
- 设置服务器为 headless 模式
- 限制日志级别为 error (减少日志输出)
- 优化上传大小限制

### 4. 启动方式对比

| 启动方式 | 性能 | 推荐度 |
|---------|------|--------|
| run_streamlit_fast.bat | ⭐⭐⭐⭐⭐ | 最推荐 |
| run_streamlit.bat | ⭐⭐⭐⭐ | 推荐 |
| run_gui.bat | ⭐⭐⭐⭐ | 桌面应用 |
| run_cli.bat | ⭐⭐⭐⭐⭐ | 最快但无界面 |

### 5. 如果仍然卡顿

1. 检查网络连接 (如果调用在线 LLM API)
2. 检查 mykey.py 中的 API 配置是否正确
3. 查看 Streamlit 日志输出,寻找错误信息
4. 尝试使用 CLI 模式 (`run_cli.bat`) 验证是否是 Streamlit 本身的问题

### 6. 常见问题

**Q: 为什么有时候很快,有时候很慢?**
A: 这取决于调用的 LLM API 响应速度,不是 Streamlit 本身的问题。

**Q: 输入文字有延迟怎么办?**
A: 这是正常的,Streamlit 需要将输入发送到服务器处理。

**Q: 页面加载慢怎么办?**
A: 第一次加载较慢,后续操作会快很多。可以尝试使用缓存。

## 下一步
如果问题持续,可以尝试:
- 使用 `run_cli.bat` 体验原生性能
- 检查 API 配置是否正确
- 联系技术支持提供更多错误信息
