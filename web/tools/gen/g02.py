import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mdpage import *

H = INC + "int main() {\n%SRC%\n    return 0;\n}\n"
T = []

# ---- ex-02-01 溢出对照（错：x*y 先按 int 算；对：先转 long long） ----
t = Trace("ex-02-01a", "long long z = x * y：看起来对，其实错",
          "int x = 100000, y = 100000;\nlong long z = x * y;\ncout << z;\n", H, kind="illustrative",
          badge="示意：溢出后的结果没有保证，所以不显示具体数字")
t.step(1, "x 和 y 都是 int，各是 10 万。", {"x": 100000, "y": 100000})
t.step(2, "先算右边的 x * y：两个 int 相乘，结果还是 int。数学上等于 10000000000（100 亿），超过 int 的最大值 2147483647（约 21 亿）→ 溢出！溢出发生在“计算的那一刻”，C++ 规定此后结果没有保证。再装进 long long 也救不回来。",
       {"x": 100000, "y": 100000, "z": "？（不可靠）"})
t.say("（一个没有保证的数）"); t.step(3, "所以不能保证得到数学上正确的 10000000000，输出的数也不可依赖。注意：换编译器、换优化选项，看到的数可能不一样，不要去背它。", {"x": 100000, "y": 100000, "z": "？（不可靠）"})
T.append(t)
t = Trace("ex-02-01b", "(long long)x * y：先转类型，再相乘",
          "int x = 100000, y = 100000;\nlong long w = (long long)x * y;\ncout << w;\n", H)
t.step(1, "x 和 y 还是 int。", {"x": 100000, "y": 100000})
t.step(2, "(long long)x 先把 x 的值转换成 long long（x 本身仍然是 int），这样乘法就按 long long 算（小类型自动向大类型看齐）。10万 × 10万 = 100 亿，long long 装得下（最大约 9.2×10¹⁸）。",
       {"x": 100000, "y": 100000, "w": 10000000000})
t.say("10000000000"); t.step(3, "输出 10000000000。最简单的办法：只要可能超过 21 亿，相关变量一开始就声明成 long long。", {"x": 100000, "y": 100000, "w": 10000000000})
T.append(t)

# ---- ex-02-02 类型转换 ----
t = Trace("ex-02-02", "整数除法 vs 小数除法",
          "int a = 7, b = 2;\ndouble r1 = a / b;\ndouble r2 = (double)a / b;\ndouble r3 = a * 1.0 / b;\nint c = 3.99;\ncout << r1 << \" \" << r2 << \" \" << r3 << \" \" << c;\n", H)
t.step(1, "a = 7，b = 2，都是 int。", {"a": 7, "b": 2})
t.step(2, "a / b：两边都是整数，先做整数除法 7 / 2 = 3（砍掉小数部分），然后才把 3 转成 3.0 放进 r1。所以是 3.0，不是 3.5！", {"a": 7, "b": 2, "r1": "3.0"})
t.step(3, "(double)a 先把 a 变成 7.0，再除以 2：小数除法，3.5。", {"a": 7, "b": 2, "r1": "3.0", "r2": "3.5"})
t.step(4, "常用技巧：乘 1.0 也会让整个运算变成小数运算，3.5。", {"a": 7, "b": 2, "r1": "3.0", "r2": "3.5", "r3": "3.5"})
t.step(5, "小数转整数：直接砍掉小数部分，3（不是四舍五入）。", {"a": 7, "b": 2, "r1": "3.0", "r2": "3.5", "r3": "3.5", "c": 3})
t.say("3 3.5 3.5 3"); t.step(6, "输出（cout 默认不显示多余的 .0）：3 3.5 3.5 3。", {"a": 7, "b": 2, "r1": "3.0", "r2": "3.5", "r3": "3.5", "c": 3})
T.append(t)

write_traces("type-02.js", T)

# ---------------- 小测 ----------------
q_avg = predict_quiz("预测输出：求平均数写成 sum / n（sum 和 n 都是 int），和 sum * 1.0 / n 的结果一样吗？",
    "int sum = 7, n = 2;\ncout << sum / n << \" \" << sum * 1.0 / n;", ["3.5 3.5", "3 3", "3.5 3"], "sum / n 两边都是整数，是整数除法，结果被砍成 3；乘 1.0 后变成小数除法才是 3.5。输出 {real}。")
q_div = predict_quiz("预测输出：负数的整除和取模（和 Python 不一样）：",
    "cout << 17 / 5 << \" \" << 17 % 5 << \" \" << -17 / 5 << \" \" << -17 % 5 << \" \" << (int)2.9;",
    ["3 2 -4 3 2", "3 2 -3 -2 3"], "C++ 的整除向 0 取整：-17 / 5 = -3（Python 是 -4）；余数符号和被除数相同：-17 % 5 = -2（Python 是 3）；(int)2.9 砍掉小数得 2。输出 {real}。")
q_max = predict_quiz("int 能存的最大值是多少？", "cout << INT_MAX;", ["2147483648", "2147483646", "2147483000"], "int 的最大值是 2³¹ − 1 = {real}，初赛常考，要记住。", pre="#include <climits>")
q_xor = predict_quiz("预测输出：想算 2 的 10 次方，写成 2 ^ 10，会得到多少？", "cout << (2 ^ 10);", ["1024", "20", "100"], "^ 在 C++ 里是按位异或，不是乘方！2 ^ 10 的结果是 {real}。整数乘方请用循环自己乘。")
q_ll = quiz("x、y 都是 int 且都等于 100000。写 long long z = x * y;，z 的值对吗？",
    ["对，因为 z 是 long long，装得下", "不对：x * y 先按 int 算，已经溢出了，再装进 long long 也晚了", "不对：long long 只能存 10 万以内的数"], 1,
    "溢出发生在“计算的那一刻”，而不是“存储的那一刻”。要先把其中一个转成 long long：(long long)x * y。上面的计算器里选一选就能看到。")
q_init = quiz("在 main 里写 int sum; 然后直接 sum += i; 累加，为什么不可靠？",
    ["没有问题，int 默认是 0", "局部变量不赋初值，它的值是不确定的", "sum 必须是 long long"], 1,
    "main 里声明的变量如果不赋初值，值是不确定的（这次看着正常，换台电脑就可能变）。养成习惯：声明时就赋初值，比如 sum = 0。")
assert compile_fails("int main() { char c = \"A\"; return 0; }")
q_char = quiz("char grade = \"A\"; 这样写对吗？",
    ["对，字符用双引号", "编译不通过：字符用单引号 'A'，双引号是字符串", "能编译，但 grade 的值是 0"], 1,
    "单引号是一个字符 'A'；双引号是字符串 \"A\"。char 变量只能装一个字符，要用单引号。")

inserts = {
    "2.2": [("quiz", q_max)],
    "2.3": [("picker", ["ex-02-01a", "ex-02-01b"], ["long long z = x * y（错）", "(long long)x * y（对）"]), ("calc", "range"), ("quiz", q_ll)],
    "2.4": [("calc", "div"), ("quiz", q_div)],
    "2.5": [("trace", "ex-02-02"), ("quiz", q_avg)],
    "3.":  [("quiz", q_init), ("quiz", q_char), ("quiz", q_xor)],
}
tasks = (["把类型转换的例子敲一遍，把 a、b 改成 <code>9</code> 和 <code>4</code>，<b>先猜</b>四个结果，再运行。",
              "在 Dev-C++ 里亲自试一下 <code>cout &lt;&lt; 2147483647 + 1;</code>，看看你的电脑上显示什么——然后记住：<b>这不是规律，不要依赖它</b>。"], "")
path, nq = build_lesson('02-变量与数据类型.md', '02-types.html', '第2课｜变量与类型', '02', inserts, ['type-02.js'], tasks)
print("第2课: %d 道小测（正文全文 + 互动）" % nq)
