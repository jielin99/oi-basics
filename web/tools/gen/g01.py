import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mdpage import *

H = INC + "int main() {\n%SRC%\n    return 0;\n}\n"
T = []

t = Trace("ex-01-01", "cout：想输出什么，就自己写什么",
          "cout << \"I love OI\";\ncout << endl;\ncout << \"Line 2\\n\";\ncout << 10 << \" \" << 20 << endl;\ncout << 7 * 6 << endl;\ncout << \"7 * 6\" << endl;\n", H)
t.say("I love OI"); t.step(1, "双引号里的文字原样输出。cout 不会自动换行。")
t.say("\n"); t.step(2, "endl 表示换行。")
t.say("Line 2\n"); t.step(3, "\\n 写在字符串里面，也是换行。数据量大时 \"\\n\" 比 endl 快，建议养成用 \"\\n\" 的习惯。")
t.say("10 20\n"); t.step(4, "<< 可以连着接很多个东西。两个数之间的空格要自己写（Python 的 print 会自动加空格，cout 不会）。")
t.say("42\n"); t.step(5, "没有引号：这是算式，先算出 7 * 6 = 42 再输出。")
t.say("7 * 6\n"); t.step(6, "加了引号：这是文字，原样输出 7 * 6。")
T.append(t)

t = Trace("ex-01-02", "打印字符画：一行一行输出",
          "cout << \"  *  \\n\";\ncout << \" *** \\n\";\ncout << \"*****\\n\";\ncout << \" *** \\n\";\ncout << \"  *  \\n\";\n", H)
for k, ln in enumerate(["  *  ", " *** ", "*****", " *** ", "  *  "], 1):
    t.say(ln + "\n"); t.step(k, "第 %d 行：%s。空格也是要输出的内容，也要写进引号里。" % (k, "“" + ln.replace(" ", "␣") + "”（␣ 表示空格）"))
T.append(t)
write_traces("first-01.js", T)

q_nospace = predict_quiz("预测输出：cout 会不会在两个值之间自动加空格？", "cout << 10 << 20;", ["10 20", "30", "10\n20"], "cout 什么都不会自动加：不加空格，也不换行。10 和 20 直接连在一起，输出 {real}。")
q_quote = predict_quiz("预测输出：加不加引号的区别：", "cout << 7 * 6 << \"\\n\";\ncout << \"7 * 6\" << \"\\n\";", ["42\n42", "7 * 6\n7 * 6", "7 * 6\n42"], "没有引号是算式，会算出结果；有引号是文字，原样输出。输出 {real}。")
q_esc = predict_quiz("预测输出：想输出带双引号的文字，要用转义：", "cout << \"He said \\\"Hi\\\"\" << \"\\n\";", ["He said Hi", "He said \\\"Hi\\\"", "编译错误"], "字符串里想要一个双引号，要写成 \\\"；想要换行写 \\n；想要一个反斜杠写 \\\\。输出 {real}。")
assert compile_fails("int main() { cout << \"hi\"； return 0; }")
q_cn = quiz("代码里写了中文标点：cout << \"hi\"；（分号是中文的），会怎样？",
    ["能正常运行，看着一样", "编译不通过：必须是英文半角标点", "只是警告"], 1, "；（）“”全是错的，必须用英文半角。报错信息里会看到 stray '\\357' in program 这样的怪字符，就是中文标点。")
assert compile_fails("int main() { Cout << 1; return 0; }")
q_case = quiz("C++ 区分大小写。把 cout 写成 Cout，会怎样？", ["没关系，一样", "编译不通过：Cout 没有定义", "输出会变成大写"], 1, "Cout、Main、Return 全是错的。")
assert compile_fails("void main() { }")
q_main = quiz("把 main 写成 void main()，会怎样？", ["没关系，很多书上都这样写", "g++ 直接报错：本课程统一写 int main()", "只是警告"], 1, "main 函数必须返回 int。统一写 int main() { ... return 0; }。")
q_semi = quiz("编译器提示“缺少分号”，报错指着第 6 行，真正漏写分号的地方最可能在哪里？",
    ["第 6 行或者它的上一行：要连同上一行一起检查", "一定是第 6 行", "第 6 行之后很远的地方"], 0,
    "编译器要读到下一行才发现上一行没结束，所以有的编译器（比如 Dev-C++ 自带的老版本）会把报错位置标在下一行。看到这类报错，先检查报错行和它的上一行。")

FLOW = """  <div class="card"><div class="flow">
    <div class="box">📝 源代码<small>a.cpp，你写的</small></div><div class="arrow">→</div>
    <div class="box err">🔧 编译<small>g++ 检查语法<br><b>语法错误在这里报</b></small></div><div class="arrow">→</div>
    <div class="box">⚙️ 可执行文件<small>a.exe</small></div><div class="arrow">→</div>
    <div class="box err">▶️ 运行<small><b>运行出错、答案不对在这里</b></small></div>
  </div><p style="margin:10px 0 0">和 Python 不同：C++ 要<b>先编译、再运行</b>。编译没通过就不会有可执行文件；编译通过了，答案也不一定对。</p></div>"""

inserts = {
    "1.":  [("html", FLOW)],
    "2.1": [("trace", "ex-01-01"), ("quiz", q_nospace), ("quiz", q_quote)],
    "2.4": [("quiz", q_esc)],
    "2.5": [("trace", "ex-01-02")],
    "3.":  [("quiz", q_semi), ("quiz", q_cn), ("quiz", q_case), ("quiz", q_main)],
}
tasks = (["把 ex-01-01 敲一遍，编译运行，看输出是不是 5 行。再故意删掉一个分号，读一读编译器的报错，找到它指的是第几行。",
              "输出你的名字（拼音）、年级、最喜欢的数字，每项一行。不用计算器，让程序算出 <code>123 * 456 + 789</code> 并输出。"], "")
path, nq = build_lesson('01-第一个程序.md', '01-first.html', '第1课｜第一个程序', '01', inserts, ['first-01.js'], tasks)
print("第1课: %d 道小测（正文全文 + 互动）" % nq)
