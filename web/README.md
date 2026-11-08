# OI 入门互动课件（Web 版）

**每一课的网页就是完整课件**：课文、代码、表格、练习与参考答案、洛谷题表、自查清单全部在页面里，动画和小测嵌在对应小节后面。
纯静态页面，**双击 `index.html` 即可使用**（不需要网络、不需要安装任何东西），也可以放到任何静态服务器上。

## 内容从哪里来、改哪里（重要）

| 想改什么 | 改哪里 | 然后 |
|---|---|---|
| 课文、代码、表格、练习、答案 | 仓库根目录的 md（如 `07-数组.md`）——**课程正文以 md 为唯一来源** | 运行 `build_all.py` |
| 动画放在哪个小节、小测放在哪个小节 | `web/tools/gen/g*.py` 里的 `inserts = {"2.4": [...]}` | 运行 `build_all.py` |
| 小测的题目、选项、解释 | 对应的 `g*.py`（第 7、10 课的小测也在 `g07.py`/`g10.py`） | 运行 `build_all.py` |
| 动画的逐步过程 | `g*.py` 里的 `Trace(...)`；第 7、10 课的动画是手工保存的 `data/traces/array-07.js`、`sort-10.js` | 运行 `verify-traces.py` |

`lessons/*.html`、`index.html`、`data/traces/*.js`（除第 7、10 课）、`code/` 都是**生成物**，不要直接改。
插入点 key 写法见 `tools/gen/mdpage.py` 文件头；key 在 md 里找不到或重复，构建会直接失败。

## 开发者命令（需要 g++、Python3、Node；浏览器检查需要 Chromium）

```bash
python3 web/tools/gen/build_all.py    # 重新生成所有页面和动画数据（会真实编译运行每个例子；
                                      # 每页还会逐项核对 md 的标题、代码块、正文都完整出现在页面里）
python3 web/tools/verify-traces.py    # 动画数据校验：真实编译运行，输出与动画最终输出一致
python3 web/tools/test-calc.py        # 计算器与真实 C++ / Python 逐项对照
python3 web/tools/inventory.py --check  # 对比“迁移前基线”，确认没有漏掉任何动画/小测/计算器
python3 web/tools/smoke.py            # 无头浏览器冒烟测试所有页面（桌面 + 手机宽度）：脚本错误、动画/小测/计算器挂载数、
                                      # 逐步前进后退、投屏模式字号、不横向滚动等
python3 web/tools/test-mdverify.py    # 内容校验器自测：16 个 md 无损转换，并对页面做 19 种破坏，必须全部被发现
python3 web/tools/linkcheck.py        # 以 web/ 为根起 HTTP 服务，检查 index 与各课页里的全部链接/资源/锚点
                                      # （只检查这些页面直接引用的内容，不继续深入 css/js 内部的引用）
```

- 每个“预测输出”小测的正确答案由真实编译运行得出，不是手写的。
- `web/code/` 是根目录 `code/` 的复制件（局域网/静态服务只发布 `web/`），由构建自动同步，`linkcheck.py` 会比对字节。
