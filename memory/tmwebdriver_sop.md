# TMWebDriver SOP

- 禁止import，直接用web_scan/web_execute_js工具。本文件只记录特性和坑。
- 底层：`../TMWebDriver.py`通过Tampermonkey脚本接管用户浏览器（保留登录态/Cookie）
- 非Selenium/Playwright，不需调试浏览器或新数据目录
- 支撑 `web_scan`(只读DOM) / `web_execute_js`(执行JS) 等高层工具

## 限制(isTrusted)
- JS dispatch的事件`isTrusted=false`，敏感操作(文件上传/部分按钮)会被浏览器拦截
- ⭐**首选绕过：CDP桥**——CDP派发的Input事件是浏览器原生级别(isTrusted=true)，且无需前台，见下方CDP章节
- 文件上传：JS无法填充`<input type=file>`
  - ⭐首选CDP batch：getDocument→querySelector→DOM.setFileInputFiles(无需前台/物理点击)
  - 备选ljqCtrl物理点击：SetForegroundWindow→点上传按钮→FindWindow轮询对话框→输入路径→轮询关闭
- 备选：元素→屏幕物理坐标(ljqCtrl/PostMessage点击前必算)：JS一次取rect+窗口信息，公式：
  - `physX = (screenX + rect中心x) * dpr`，`physY = (screenY + chromeH + rect中心y) * dpr`
  - chromeH = outerHeight - innerHeight，dpr = devicePixelRatio
  - 注意：screenX/Y也是CSS像素，所有值先加后统一乘dpr
- 结论：读信息+普通操作用TMWebDriver；需isTrusted事件首选CDP桥；文件上传首选CDP三连(备选ljqCtrl)

## 导航
- `web_scan` 仅读当前页不导航，切换网站用 `web_execute_js` + `location.href='url'`

## Google图搜
- class名混淆禁硬编码，点击结果用 `[role=button]` div
- web_scan过滤边栏，弹出后用JS：文本`document.body.innerText`，大图遍历img按`naturalWidth`最大取src
- "访问"链接：遍历a找`textContent.includes('访问')`的href
- 缩略图：`img[src^="data:image"]`直接提取；大图src可能截断用`return img.src`

## Chrome下载PDF
场景：PDF链接在浏览器内预览而非下载
```js
fetch('PDF_URL').then(r=>r.blob()).then(b=>{
  const a=document.createElement('a');
  a.href=URL.createObjectURL(b);
  a.download='filename.pdf';
  a.click();
});
```
注意：需同源或CORS允许，跨域先导航到目标域再执行

## Chrome后台标签节流
- 后台标签中`setTimeout`被Chrome intensive throttling延迟到≥1min/次
- TM脚本中detect_newtab的轮询(`setTimeout 150ms × 10`)会超时
- 已修复：移除TM脚本内轮询，改由Python侧`get_session_dict()`前后对比检测新标签
- 同理：TM脚本中任何后台逻辑都应避免依赖setTimeout轮询

## CDP桥(tmwd_cdp_bridge扩展) ⭐首选
扩展路径：`assets/tmwd_cdp_bridge/`(需安装，含debugger权限)
⚠TID密钥：首次运行自动生成到`assets/tmwd_cdp_bridge/config.js`(已gitignore)，扩展通过manifest引用
调用：MutationObserver监听addedNodes(id=TID)，⚠每次必须remove旧→createElement新→设textContent JSON→appendChild
```js
// TID从assets/tmwd_cdp_bridge/config.js读取，示例用'__ljq_ctrl'占位
const old = document.getElementById(TID);
if (old) old.remove();
const el = document.createElement('div');
el.id = TID; el.style.display = 'none';
el.textContent = JSON.stringify({cmd:'...', ...});
document.body.appendChild(el);  // 响应写回el.textContent
```
单命令：`{cmd:'tabs'}` | `{cmd:'cookies'}` | `{cmd:'cdp', tabId:N, method:'...', params:{...}}`
- ⭐batch混合：`{cmd:'batch', commands:[{cmd:'cookies'},{cmd:'tabs'},{cmd:'cdp',...},...]}`
  - 返回`{ok:true, results:[...]}`，一次请求多命令，CDP懒attach复用session
  - `$N.path`引用第N个结果字段(0-indexed)，如`"nodeId":"$2.root.nodeId"`
  - 典型：文件上传三连 getDocument→querySelector(input[type=file])→setFileInputFiles
  - ⚠tabId：CDP默认sender.tab.id(当前注入页)，跨tab需显式tabId或先batch内tabs查
- CDP可用任意方法(Input/Network/DOM/Page/Runtime/Emulation等)，单条每次attach→send→detach
- ⭐跨tab无需前台：指定tabId即可操作后台标签页
- ⭐绕过isTrusted：CDP派发的Input事件是浏览器原生级别

## autofill获取
检测：web_scan输出input带`data-autofilled="true"`，value显示为受保护提示(非真实值，Chrome安全保护需点击释放)
- ⭐首选CDP单次点击：JS取任一autofill输入框坐标→CDP `Input.dispatchMouseEvent` mousePressed一次即可释放→JS读`.value`
  - ⚠点击一个autofill字段会释放页面上**所有**autofill字段的值，无需逐个点击
  - ⚠只需mousePressed，不需要mouseReleased配对
  - ⚠tabId：当前注入页无需指定(默认sender.tab.id)，跨tab才需显式tabId(整数)
  - 示例(当前页)：`{cmd:'cdp',method:'Input.dispatchMouseEvent',params:{type:'mousePressed',x:X,y:Y,button:'left',clickCount:1}}`
  - 示例(跨tab)：先`{cmd:'tabs'}`获取tabId(整数)，再`{cmd:'cdp',tabId:N,method:'Input.dispatchMouseEvent',params:{...}}`
  - ⚠batch的`$N.path`引用会将整数tabId转为字符串导致类型错误，跨tab时建议分两次命令而非batch
- 备选PostMessage物理点击(仅Windows/需前台)：枚举Chrome窗口标题匹配→rect*dpr→WM_LBUTTONDOWN/UP到Chrome_RenderWidgetHostHWND子窗口
  - 坑：多RenderWidgetHostHWND共存，必须按父窗口标题匹配再取子窗口

## 验证码/页面视觉截图
- ⭐首选CDP截图：`Page.captureScreenshot`(format:'png')→返回base64，无需前台/后台tab也行，全页高清
- 验证码canvas/img：JS `canvas.toDataURL()` 直接拿base64最干净
- 备选：`window.open(location.href,'_blank')` 前台开新标签→win32截图→完后close
  - GM_openInTab在web_execute_js不可用（非油猴上下文）

## 直接import(仅作调试使用)
- `sys.path.insert(0, GenericAgent根目录)`, `from TMWebDriver import TMWebDriver`
- `d=TMWebDriver()`, `d.set_session('url_pattern')`, `d.execute_js('code')` → 返回`{'data': value}`(非裸值)
- 配合simphtml：`str(simphtml.optimize_html_for_tokens(html))` → 注意返回BS4 Tag需str()

## 跨域iframe操控(postMessage中继)
- 跨域iframe的contentDocument不可访问，web_execute_js只在顶层执行
- TM脚本已改造：iframe内不return，改为监听postMessage并eval执行+回传结果
- 顶层发送：`iframe.contentWindow.postMessage({type:'ljq_exec', id, code}, '*')`
- iframe回传：`{type:'ljq_result', id, result}` 通过window.addEventListener('message')接收
- ⚠只能eval表达式，不支持return/函数体包装，构造代码时注意
- 流程：发postMessage→等→读window._ljqResults[id]获取结果
- 已验证：读取iframe内DOM(document.title)、填写input均成功

## 连不上排查
web_scan失败时按序排查：
①TM没装？→遍历本机所有Chromium浏览器(Chrome/Edge/Brave…)用户数据目录下Extensions/，各子目录manifest.json搜"tampermonkey"
  没找到→走web_setup_sop；找到→记住装在哪个浏览器
②浏览器没开？→检查①对应的浏览器进程是否在跑(tasklist/ps)，没有则启动并打开正常URL（⚠about:blank等内部页不加载扩展）
③WS后台挂了？→socket.connect_ex(('127.0.0.1',18766))非0即dead→手动`from TMWebDriver import TMWebDriver; TMWebDriver()`起master

## 性能
- ⚠ URL必须用`127.0.0.1`不用`localhost`。Windows下localhost先尝试IPv6(::1)超时2s再回退IPv4，每次HTTP请求多2s