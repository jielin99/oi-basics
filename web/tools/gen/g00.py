import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *

MD = "00-环境搭建.md"
text = open(os.path.join(WEB, "..", MD), encoding="utf-8").read()
title, intro, secs = md_sections(text)
assert_covers(text, intro + sections_html(secs))

q_old = quiz("你改了代码，但直接点“运行”，没有重新编译，运行的是什么？",
    ["新代码，因为文件已经保存了", "旧的 a.exe：没重新编译，可执行文件还是改动前生成的", "什么都不会运行"], 1,
    "C++ 是先编译再运行：改了代码一定要重新编译，否则运行的还是旧程序。这是新手最常见的“我明明改了怎么没变”。")
q_err = quiz("语法错误（比如漏了分号）在 C++ 里什么时候会被发现？",
    ["运行到那一行才报错，和 Python 一样", "编译的时候就会报出来，一个错都不能有，否则生成不了程序", "永远不会被发现"], 1,
    "C++ 大部分语法错误在编译时就报出来。有语法错误，根本生成不了可执行文件。")
q_env = quiz("在考场里用 Dev-C++ 写好代码，最后评测是在哪里进行的？",
    ["就在写代码的那个 Windows 里", "统一放到 Linux 上用 g++ 评测，所以代码要按标准 C++ 写，不能用 Windows 专有的东西", "由选手自己决定"], 1,
    "课程 md 里的原话：无论考场里用哪个编辑器写代码，最后都放到 Linux 上用 g++ 评测。具体环境以每年 CCF 和本省的通知为准。")
q_path = quiz("hello.cpp 编译总是出怪错，文件放在“桌面\\我的 C++ 作业\\”里，可能的原因和办法是？",
    ["没有问题，是电脑坏了", "路径里有中文或空格会让老版编译器异常，换个纯英文路径，如 D:\\oi\\", "必须放在 C 盘根目录"], 1,
    "还要检查：输入法有没有打出中文标点；文件扩展名是不是 .cpp（不是 .txt 或 .c）。")
q_re = quiz("洛谷提交后显示 RE（运行时错误），最可能是什么原因？",
    ["数组越界、除以 0、递归太深", "算法太慢", "语法写错了"], 0,
    "RE 是程序运行起来以后出的错。语法错是 CE（编译错误）；算法太慢是 TLE（超时）；输出不对是 WA（答案错误）。")
q_tle = quiz("洛谷显示 TLE，说明什么？",
    ["答案错误", "超时：算法太慢、死循环、或者输入太多却用了慢速读入", "超内存"], 1,
    "超内存是 MLE（数组开得太大）。AC 才是通过。")

def sec(k): return ("html", sections_html([secs[k]], open_all=True))
blocks = [
    ("html", '  <div class="md-tools"><button id="btn-all">全部收起</button></div>\n  ' + intro),
    sec(0), ("quiz", q_old), ("quiz", q_err),
    sec(1), ("quiz", q_env),
    sec(2), ("quiz", q_path),
    sec(3), ("quiz", q_re), ("quiz", q_tle),
    sec(4),
    sec(5),
]
path, nq = build_page("00-setup.html", "00", "第0课｜环境搭建", "第0课 环境搭建（完整内容）", title.replace("第 0 课 ", ""), "", MD, blocks, badge="内容与 md 相同，加了几道小测")
print("第0课: %d 节, %d 道小测, 自查清单可勾选" % (len(secs), nq))
