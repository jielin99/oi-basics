import glob, html, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *

# 课次 → (页面文件, md 文件, 形态)
ROWS = [("第 0 课", "环境搭建", "00-setup.html", "00-环境搭建.md", "完整内容"),
        ("第 1 课", "第一个程序", "01-first.html", "01-第一个程序.md", "精选演示"),
        ("第 2 课", "变量与数据类型", "02-types.html", "02-变量与数据类型.md", "精选演示"),
        ("第 3 课", "输入输出", "03-io.html", "03-输入输出.md", "精选演示"),
        ("第 4 课", "运算符与表达式", "04-operator.html", "04-运算符与表达式.md", "精选演示"),
        ("第 5 课", "分支结构", "05-branch.html", "05-分支结构.md", "精选演示"),
        ("第 6 课", "循环结构", "06-loop.html", "06-循环结构.md", "精选演示"),
        ("第 7 课", "数组", "07-array.html", "07-数组.md", "精选演示"),
        ("第 8 课", "字符与字符串", "08-string.html", "08-字符与字符串.md", "精选演示"),
        ("第 9 课", "函数与递归", "09-func.html", "09-函数与递归.md", "精选演示"),
        ("第 10 课", "结构体与排序", "10-sort.html", "10-结构体与排序.md", "精选演示"),
        ("第 11 课", "STL 入门", "11-stl.html", "11-STL入门.md", "精选演示"),
        ("第 12 课", "指针、位运算与比赛规范", "12-ptr-bit.html", "12-指针位运算与比赛规范.md", "精选演示"),
        ("附录 A", "Python 与 C++ 对照", "A-python-cpp.html", "附录A-Python与C++对照.md", "速查页"),
        ("附录 B", "常见错误与调试", "B-errors.html", "附录B-常见错误与调试.md", "速查页"),
        ("附录 C", "考场模板与规范", "C-template.html", "附录C-考场模板与规范.md", "速查页")]
rows = ""
for no, name, page, md, kind in ROWS:
    h = open(os.path.join(WEB, "lessons", page), encoding="utf-8").read()
    demos = len(re.findall(r'data-trace="', h)) + sum(len(x.split(",")) for x in re.findall(r'data-traces="([^"]*)"', h))
    quizzes = len(re.findall(r'^\s*Q\("q\d+"', h, re.M))
    calcs = len(re.findall(r'data-calc="', h))
    parts = []
    if demos: parts.append("%d 个动画演示" % demos)
    if quizzes: parts.append("%d 道小测" % quizzes)
    if calcs: parts.append("%d 个小工具" % calcs)
    rows += '      <tr><td>%s</td><td><a href="lessons/%s"><b>%s</b></a></td><td>%s</td><td>%s</td><td><a href="../%s">md</a></td></tr>\n' % (
        no, page, html.escape(name), kind, "、".join(parts) or "—", md)

page = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>OI 入门互动课件</title>
<link rel="stylesheet" href="css/base.css">
</head>
<body data-lesson="index" data-lesson-label="目录">
<div class="wrap">
  <div class="topbar"><span></span><button id="btn-present">投屏模式</button></div>
  <h1>OI 入门互动课件</h1>
  <p>配合 md 课程使用：<b>先看动画建立直觉，再回到 Dev-C++ 自己敲一遍</b>。点「下一步」逐行看程序怎么跑；做小测会马上告诉你对不对；看不懂就点「🙋 我不懂这里」，把生成的那行文字发给老师。</p>
  <div class="card">
    <table class="calc-tbl">
      <tr><th>课次</th><th>主题</th><th>形态</th><th>互动内容</th><th>原文</th></tr>
%s    </table>
    <p style="color:var(--muted);font-size:.85rem;margin:8px 0 0">“精选演示”是挑出最需要动画才能懂的部分，不是整课讲义；其余内容请读对应的 md。</p>
  </div>
</div>
<script src="js/core/page.js"></script>
<script>PageKit.init();</script>
</body>
</html>
""" % rows
open(os.path.join(WEB, "index.html"), "w", encoding="utf-8").write(page)
print("目录: %d 行" % len(ROWS))
