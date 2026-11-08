import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mdpage import *

H = INC + "int main() {\n%SRC%\n    return 0;\n}\n"
T = []

# ---- ex-04-01 复合赋值 ----
t = Trace("ex-04-01", "复合赋值：x += 3 就是 x = x + 3",
          "int x = 10;\nx += 3;\nx -= 2;\nx *= 2;\nx /= 5;\nx %= 3;\ncout << x;\n", H)
x = 10
t.step(1, "x 从 10 开始。", {"x": x})
x += 3;  t.step(2, "x += 3，即 x = x + 3 = 13。", {"x": x})
x -= 2;  t.step(3, "x -= 2，即 x = x - 2 = 11。", {"x": x})
x *= 2;  t.step(4, "x *= 2，即 x = x * 2 = 22。", {"x": x})
x = cdiv(x, 5); t.step(5, "x /= 5：两边都是整数，是整除，22 / 5 = 4（不是 4.4）。", {"x": x})
x = cmod(x, 3); t.step(6, "x %= 3：4 除以 3 余 1。", {"x": x})
t.say(str(x)); t.step(7, "输出 %d。" % x, {"x": x})
T.append(t)

# ---- ex-04-02 a++ 与 ++c ----
t = Trace("ex-04-02", "b = a++ 与 d = ++c 的区别",
          "int a = 5;\nint b = a++;\nint c = 5;\nint d = ++c;\ncout << a << \" \" << b << \" \" << c << \" \" << d;\n", H)
t.step(1, "a = 5。", {"a": 5})
t.step(2, "b = a++：先把 a 现在的值 5 拿去给 b，然后 a 才加 1。所以 b = 5，a = 6。（a++ ：先用后加）", {"a": 6, "b": 5})
t.step(3, "c = 5。", {"a": 6, "b": 5, "c": 5})
t.step(4, "d = ++c：先把 c 加 1 变成 6，再把新值 6 给 d。所以 c = 6，d = 6。（++c ：先加后用）", {"a": 6, "b": 5, "c": 6, "d": 6})
t.say("6 5 6 6"); t.step(5, "输出 6 5 6 6。单独成一句时 i++ 和 ++i 完全一样，区别只在“被用在表达式里”的时候。", {"a": 6, "b": 5, "c": 6, "d": 6})
T.append(t)

# ---- ex-04-03 短路求值 ----
t = Trace("ex-04-03", "短路求值：b 为 0 时，a / b 根本不会被计算",
          "int a = 10, b = 0;\nif (b != 0 && a / b > 2) {\n    cout << \"big\";\n} else {\n    cout << \"safe\";\n}\n", H)
t.step(1, "a = 10，b = 0。注意：如果真去算 a / b，就是除以 0，程序会出错。", {"a": 10, "b": 0})
t.step(2, "A && B：先算左边 b != 0，0 != 0 不成立（假）。&& 只要有一边为假，整体就一定为假，所以右边 a / b > 2 根本不会被计算——这就是短路。", {"a": 10, "b": 0})
t.step(4, "条件为假，走 else。", {"a": 10, "b": 0})
t.say("safe"); t.step(5, "输出 safe。所以要先判断“除数不为 0”，再做除法。", {"a": 10, "b": 0})
T.append(t)

write_traces("op-04.js", T)

# ---------------- 小测 ----------------
assert crashes("int main() { int a = 10, b = 0; if (a / b > 2 && b != 0) cout << \"big\"; else cout << \"safe\"; return 0; }")
q_order = quiz("把条件的顺序调换：if (a / b > 2 && b != 0)，当 b = 0 时会怎样？",
    ["输出 safe，和原来一样", "先算左边的 a / b，除以 0，程序运行出错", "编译不通过"], 1,
    "&& 从左往右算。顺序反了，左边的 a / b 会先被计算，b = 0 就是除以 0。（我们真实运行过这段代码：它会异常退出。）所以“保护条件”要写在前面。")
q_incr = predict_quiz("预测输出：a++ 和 ++b 用在表达式里，会输出什么？",
    "int a = 3, b = 3;\nint x = a++ * 2;\nint y = ++b * 2;\ncout << x << \" \" << y << \" \" << a << \" \" << b;",
    ["8 8 4 4", "6 6 4 4", "6 8 3 4"], "a++ 先用旧值 3：x = 3 * 2 = 6，之后 a 才变成 4；++b 先加到 4 再用：y = 4 * 2 = 8。输出 {real}。")
q_short = predict_quiz("预测输出：短路求值会“吞掉”右边的副作用。输出什么？",
    "int a = 0, b = 5;\nif (a != 0 && ++b > 0) { }\ncout << b;", ["6", "0", "1"], "a != 0 为假，右边的 ++b > 0 根本不执行，所以 b 没被加 1，仍然是 {real}。")
q_assign = predict_quiz("预测输出：if (x = 5) 把判断写成了赋值，会输出什么？",
    "int x = 3;\nif (x = 5) cout << \"five\";\ncout << x;", ["five3", "3", "five"], "x = 5 是赋值：x 变成 5，整个表达式的值是 5（非 0，当作真），所以会输出 five；而且 x 也被改成了 5。输出 {real}。判断相等要写 ==。")
q_chain = predict_quiz("预测输出：想判断 x 在 1 到 10 之间，写成了 1 < x < 10，x = 20 时输出什么？",
    "int x = 20;\nif (1 < x < 10) cout << \"yes\";\nelse cout << \"no\";", ["no", "编译错误"], "1 < x < 10 会被拆成 (1 < x) < 10：先算 1 < 20 得到 true（也就是 1），再算 1 < 10，成立，所以输出 {real}。要写成 1 < x && x < 10。")
q_and = predict_quiz("预测输出：把 && 写成 &，结果会一样吗？",
    "int a = 1, b = 2;\nif (a & b) cout << \"yes\"; else cout << \"no\";\nif (a && b) cout << \"yes\"; else cout << \"no\";", ["yesyes", "yesno", "nono"], "& 是按位与：1 & 2 的二进制 01 & 10 = 00 = 0（假）；&& 是逻辑与：两边都非零，为真。所以输出 {real}。有时碰巧对，有时错，别混用。")
q_float = predict_quiz("预测输出：用 == 比较小数，会输出什么？",
    "double a = 0.1 + 0.2;\nif (a == 0.3) cout << \"equal\";\nelse cout << \"not equal\";", ["equal"], "小数在计算机里有微小的误差，0.1 + 0.2 并不恰好等于 0.3。要写 fabs(a - 0.3) < 1e-9。这里输出 {real}。")
q_pow = quiz("要算整数的乘方（比如 3 的 5 次方）再放进 int，更稳妥的写法是？",
    ["(int)pow(3, 5)，库函数肯定没问题", "用循环自己一个一个乘", "3 ^ 5"], 1,
    "pow 返回 double，用来算整数乘方可能有微小误差（偶尔会少 1）；^ 在 C++ 里是异或，不是乘方。整数乘方请用循环自己乘。")

inserts = {
    "2.1": [("trace", "ex-04-01")],
    "2.2": [("trace", "ex-04-02"), ("quiz", q_incr)],
    "2.3": [("trace", "ex-04-03"), ("quiz", q_order), ("quiz", q_short)],
    "3.":  [("quiz", q_assign), ("quiz", q_chain), ("quiz", q_and), ("quiz", q_float), ("quiz", q_pow)],
}
tasks = (["把自增的例子敲一遍，再加一行 <code>int e = a-- + --c;</code>，<b>先猜</b> a、c、e 的值，再运行。",
              "把 ex-04-03 里的 <code>b</code> 改成 2，再看输出；再把两个条件顺序对调、b 改回 0，亲眼看看会发生什么。"], "")
path, nq = build_lesson('04-运算符与表达式.md', '04-operator.html', '第4课｜运算符', '04', inserts, ['op-04.js'], tasks)
print("第4课: %d 道小测（正文全文 + 互动）" % nq)
