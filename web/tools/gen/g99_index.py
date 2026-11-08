import glob, html, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *

rows = ""
for no, name, page, md in LESSONS:
    kind = "速查页" if no.startswith("附录") else "完整课件"
    h = open(os.path.join(WEB, "lessons", page), encoding="utf-8").read()
    demos = len(re.findall(r'data-trace="', h)) + sum(len(x.split(",")) for x in re.findall(r'data-traces="([^"]*)"', h))
    quizzes = len(re.findall(r'^\s*Q\("q\d+"', h, re.M))
    calcs = len(re.findall(r'data-calc="', h))
    parts = []
    if demos: parts.append("%d 个动画演示" % demos)
    if quizzes: parts.append("%d 道小测" % quizzes)
    if calcs: parts.append("%d 个小工具" % calcs)
    rows += '      <tr><td>%s</td><td><a href="lessons/%s"><b>%s</b></a></td><td>%s</td><td>%s</td></tr>\n' % (
        no, page, html.escape(name), kind, "、".join(parts) or "—")

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
  <p>每一课就是完整的课件：<b>课文、代码、练习和参考答案都在页面里，不用再翻别的文件</b>。动画和小测放在对应小节后面——点「下一步」逐行看程序怎么跑；做小测会马上告诉你对不对；看不懂就点「🙋 我不懂这里」，把生成的那行文字发给老师。学完一段，一定要回到 Dev-C++ 自己敲一遍。</p>
  <div class="card">
    <table class="calc-tbl">
      <tr><th>课次</th><th>主题</th><th>形态</th><th>互动内容</th></tr>
%s    </table>
    <p style="color:var(--muted);font-size:.85rem;margin:8px 0 0">页面左侧（手机上是顶部）有本课目录，底部有“上一课 / 下一课”。右上角“投屏模式”会放大字号并隐藏目录。</p>
  </div>
</div>
<script src="js/core/page.js"></script>
<script>PageKit.init();</script>
</body>
</html>
""" % rows
open(os.path.join(WEB, "index.html"), "w", encoding="utf-8").write(page)
print("目录: %d 行" % len(LESSONS))
