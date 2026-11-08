import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mdpage import *

APPX = [("附录A-Python与C++对照.md", "A-python-cpp.html", "A", "附录A｜Python与C++对照"),
        ("附录B-常见错误与调试.md", "B-errors.html", "B", "附录B｜常见错误与调试"),
        ("附录C-考场模板与规范.md", "C-template.html", "C", "附录C｜考场模板与规范")]
for md, page, key, label in APPX:
    build_lesson(md, page, label, key, {}, [])
    print("%s: 全文（带目录）" % md)
