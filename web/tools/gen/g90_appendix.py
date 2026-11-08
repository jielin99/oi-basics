import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *

APPX = [("附录A-Python与C++对照.md", "A-python-cpp.html", "A"),
        ("附录B-常见错误与调试.md", "B-errors.html", "B"),
        ("附录C-考场模板与规范.md", "C-template.html", "C")]
for md, out, key in APPX:
    text = open(os.path.join(WEB, "..", md), encoding="utf-8").read()
    title, intro, secs = md_sections(text)
    body = sections_html(secs, open_first=True)
    assert_covers(text, intro + body)
    blocks = [("html", '  <div class="md-tools"><button id="btn-all">全部展开</button></div>\n  ' + intro + "\n" + body)]
    build_page(out, key, "附录" + key, title, title, "", md, blocks, badge="速查页，内容与 md 相同")
    print("%s: %d 节" % (md, len(secs)))
