# OI 入门互动课件（Web 版）

纯静态页面，**双击 `index.html` 即可使用**（不需要网络、不需要安装任何东西），也可以放到任何静态服务器上。
内容以上一级目录的 md 为准；这里是它的“可视化讲解层”。

## 开发者命令（需要 g++、Python3、Node）

```bash
python3 web/tools/gen/build_all.py   # 重新生成所有课件页和动画数据（会真实编译运行每个例子）
python3 web/tools/verify-traces.py   # 校验动画数据：真实编译运行，输出与动画最终输出一致
python3 web/tools/test-calc.py       # 计算器与真实 C++ / Python 逐项对照
python3 web/tools/smoke.py           # 无头浏览器冒烟测试所有页面（桌面 + 手机宽度）
```

- `lessons/*.html`、`data/traces/*.js`、`index.html` 由 `tools/gen/` 生成：要改内容请改 `tools/gen/g*.py`，不要直接改生成物（第 7、10 课是手写页，直接改页面）。
- 每个“预测输出”小测的正确答案由真实编译运行得出，不是手写的。
