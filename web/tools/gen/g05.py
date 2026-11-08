import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mdpage import *

H = INC + "int main() {\n%SRC%\n    return 0;\n}\n"
T = []

# ---- ex-05-01 if / else if / else，三种输入 ----
for tag, sc in (("a", 95), ("b", 70), ("c", 30)):
    src = ("int score = %d;\nif (score >= 90) {\n    cout << \"A\";\n} else if (score >= 60) {\n    cout << \"B\";\n} else {\n    cout << \"C\";\n}\n") % sc
    t = Trace("ex-05-01" + tag, "if / else if / else：成绩 %d 走哪条路" % sc, src, H)
    t.step(1, "score = %d。下面三条路，只会走其中一条。" % sc, {"score": sc})
    if sc >= 90:
        t.step(2, "第一个条件：%d >= 90 成立 → 走这条路，后面的 else if、else 全部跳过，不会再判断。" % sc, {"score": sc})
        t.say("A"); t.step(3, "输出 A。", {"score": sc})
    else:
        t.step(2, "第一个条件：%d >= 90 不成立，往下看 else if。" % sc, {"score": sc})
        if sc >= 60:
            t.step(4, "else if：%d >= 60 成立 → 走这条路，else 跳过。" % sc, {"score": sc})
            t.say("B"); t.step(5, "输出 B。", {"score": sc})
        else:
            t.step(4, "else if：%d >= 60 也不成立。" % sc, {"score": sc})
            t.step(6, "前面都不成立，走最后的 else（else 不用写条件）。", {"score": sc})
            t.say("C"); t.step(7, "输出 C。", {"score": sc})
    T.append(t)

# ---- ex-05-02 switch：有 break / 漏写 break ----
src_b = ("int x = 2;\nswitch (x) {\n    case 1:\n        cout << \"one \";\n        break;\n    case 2:\n        cout << \"two \";\n        break;\n"
         "    case 3:\n        cout << \"three \";\n        break;\n}\n")
t = Trace("ex-05-02a", "switch：每个 case 都有 break", src_b, H)
t.step(1, "x = 2。", {"x": 2})
t.step(6, "switch (x)：直接跳到 case 2 这个入口（中间的 case 1 不会判断）。", {"x": 2})
t.say("two "); t.step(7, "输出 two。", {"x": 2})
t.step(8, "遇到 break，立刻跳出整个 switch。", {"x": 2})
T.append(t)
src_n = "int x = 2;\nswitch (x) {\n    case 1:\n        cout << \"one \";\n    case 2:\n        cout << \"two \";\n    case 3:\n        cout << \"three \";\n}\n"
t = Trace("ex-05-02b", "switch：漏写 break 会“穿透”", src_n, H)
t.step(1, "x = 2。这次每个 case 后面都没有 break。", {"x": 2})
t.step(5, "switch (x)：跳到 case 2 这个入口。", {"x": 2})
t.say("two "); t.step(6, "输出 two。", {"x": 2})
t.say("three "); t.step(8, "没有 break，不会停！程序继续往下“掉”进 case 3，不管 x 是不是 3，照样输出 three。这就是穿透。", {"x": 2})
t.step(9, "switch 结束。想只输出 two，要在 case 2 的末尾写 break;", {"x": 2})
T.append(t)

# ---- ex-05-03 悬空 else ----
src = "int a = 1, b = -1;\nif (a > 0)\n    if (b > 0)\n        cout << \"both\";\nelse\n    cout << \"?\";\n"
t = Trace("ex-05-03", "悬空 else：缩进是骗人的", src, H)
t.step(1, "a = 1，b = -1。", {"a": 1, "b": -1})
t.step(2, "外层 if：a > 0 成立，进入下一句。", {"a": 1, "b": -1})
t.step(3, "内层 if：b > 0 不成立（-1 不大于 0），内层 if 的内容跳过。", {"a": 1, "b": -1})
t.step(5, "else 排版上和外层 if 对齐，但规则是：else 总和离它最近的、还没配对的 if 配对——它属于内层的 if (b > 0)！内层条件不成立，所以走这个 else。", {"a": 1, "b": -1})
t.say("?"); t.step(6, "输出 ?。写上花括号就不会有这种误会。", {"a": 1, "b": -1})
T.append(t)

# ---- ex-05-04 三个数排序（分类讨论 + 交换） ----
src = ("int a = 3, b = 1, c = 2, t;\nif (a > b) { t = a; a = b; b = t; }\nif (a > c) { t = a; a = c; c = t; }\n"
       "if (b > c) { t = b; b = c; c = t; }\ncout << a << \" \" << b << \" \" << c;\n")
t = Trace("ex-05-04", "三个数排序：三次“比较并交换”", src, H)
a, b, c = 3, 1, 2
t.step(1, "要把 a、b、c 从小到大排好。t 是用来交换的“中间盒子”。", {"a": a, "b": b, "c": c})
if a > b:
    tt = a; a = b; b = tt
    t.step(2, "a > b：3 > 1 成立，交换 a 和 b（借助 t）。现在 a ≤ b 了。", {"a": a, "b": b, "c": c, "t": tt})
if a > c:
    tt = a; a = c; c = tt
    t.step(3, "a > c 成立，交换。", {"a": a, "b": b, "c": c, "t": tt})
else:
    t.step(3, "a > c：1 > 2 不成立，不用换。现在 a 是三个数里最小的。", {"a": a, "b": b, "c": c, "t": 3})
if b > c:
    tt = b; b = c; c = tt
    t.step(4, "b > c：3 > 2 成立，交换。现在 b ≤ c 了。", {"a": a, "b": b, "c": c, "t": tt})
t.say("%d %d %d" % (a, b, c))
t.step(5, "输出 %d %d %d。Python 里的 a, b = b, a 在 C++ 里不能用，要借助 t，或者直接写 swap(a, b)。" % (a, b, c), {"a": a, "b": b, "c": c, "t": 3})
T.append(t)

write_traces("branch-05.js", T)

# ---------------- 小测 ----------------
q_semi = predict_quiz("预测输出：if 括号后面多了一个分号，会输出什么？",
    "int x = -5;\nif (x > 0);\n{\n    cout << \"positive\";\n}", ["什么也不输出", "编译错误"], "if (x > 0); 里的 ; 让 if 管的是一条空语句，后面的 { } 变成了普通代码块，不管 x 是多少都会执行，所以输出 {real}。")
q_assign = predict_quiz("预测输出：把判断写成了赋值 if (x = 0)，会输出什么？",
    "int x = 5;\nif (x = 0) cout << \"yes\";\nelse cout << \"no\";\ncout << x;", ["yes5", "no5", "yes0"], "x = 0 是赋值：先把 x 改成 0，整个表达式的值是 0（假），走 else；而且 x 已经被改成 0 了。输出 {real}。判断相等要写 ==。")
q_brace = predict_quiz("预测输出：省略花括号后又补了第二条语句，会输出什么？",
    "int x = -1, cnt = 0;\nif (x > 0)\n    cout << \"positive \";\n    cnt++;\ncout << cnt;", ["0", "positive 1", "positive 0"], "不写花括号时，if 只管紧跟着的那一条语句。cnt++ 看着缩进对齐，其实不属于 if，不管 x 是多少都会执行，所以 cnt 变成 1，输出 {real}。初学阶段一律写花括号。")
q_dangle = quiz("悬空 else 的例子里，那个 else 到底属于哪个 if？",
    ["属于外层的 if (a > 0)，因为它们对齐", "属于离它最近的 if (b > 0)", "两个都不属于"], 1,
    "规则：else 总是和离它最近的、还没配对的 if 配对。缩进对编译器没有任何意义，写花括号就不会误会。")
q_switch = predict_quiz("预测输出：x = 1，而且每个 case 后面都漏写了 break，会输出什么？",
    "int x = 1;\nswitch (x) {\n    case 1: cout << \"one \";\n    case 2: cout << \"two \";\n    case 3: cout << \"three \";\n}", ["one", "one two", "three"], "从 case 1 进入后没有 break，就会一路往下“掉”到结尾，把后面所有 case 的语句都执行一遍。输出 {real}。")
q_yes = quiz("题目要求输出 Yes，你写成了 cout << \"YES\"; 评测结果通常是什么？",
    ["通过，大小写无所谓", "WA（答案错误）：输出和标准答案不一致", "编译错误"], 1,
    "评测是逐字比对的，Yes、YES、yes 是三个不同的答案。养成习惯：直接复制题目里的原文。")

inserts = {
    "1.":  [("picker", ["ex-05-01a", "ex-05-01b", "ex-05-01c"], ["score = 95", "score = 70", "score = 30"])],
    "2.1": [("quiz", q_brace)],
    "2.2": [("trace", "ex-05-03"), ("quiz", q_dangle)],
    "2.3": [("picker", ["ex-05-02a", "ex-05-02b"], ["每个 case 都有 break", "漏写 break（穿透）"]), ("quiz", q_switch)],
    "2.5": [("trace", "ex-05-04")],
    "3.":  [("quiz", q_semi), ("quiz", q_assign), ("quiz", q_yes)],
}
tasks = (["把三个数排序的例子敲一遍，把数据改成 <code>5 9 2</code>，<b>先猜</b>每一步后 a、b、c 的值，再用输出验证。",
              "试试把悬空 else 的代码里每个 if 都加上花括号，看看输出会不会变。",
              "做洛谷入门题单里“分支结构”那一组题（题号见 md）。"], "")
path, nq = build_lesson('05-分支结构.md', '05-branch.html', '第5课｜分支', '05', inserts, ['branch-05.js'], tasks)
print("第5课: %d 道小测（正文全文 + 互动）" % nq)
