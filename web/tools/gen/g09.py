import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *

H = INC + "%SRC%\n"          # 本课例子都是完整程序（含函数和 main）
T = []

# ---- ex-09-01a/b 值传递 vs 引用传递 ----
for tag, amp in (("a", ""), ("b", "&")):
    src = "void change(int %sx) {\n    x = 100;\n}\nint main() {\n    int a = 5;\n    change(a);\n    cout << a;\n}\n" % amp
    t = Trace("ex-09-01" + tag, "值传递：函数拿到“复印件”" if not amp else "引用传递：函数拿到“原件”", src, H)
    main = lambda a, at="": {"fn": "main", "vars": {"a": a}, "at": at}
    t.step(5, "main 里有一个变量 a，值是 5。", stack=[main(5)])
    if not amp:
        t.step(6, "调用 change(a)：函数的参数 x 是 a 的一份“复印件”，里面也是 5，但它是另一个格子。",
               stack=[main(5, "等待 change 结束"), {"fn": "change", "vars": {"x": 5}, "at": "x 是复印件"}])
        t.step(2, "x = 100：改的是复印件。原件 a 纹丝不动，还是 5。",
               stack=[main(5, "等待 change 结束"), {"fn": "change", "vars": {"x": 100}, "at": "只改了复印件"}])
        t.step(3, "change 结束，复印件 x 随着函数一起消失。", stack=[main(5)])
        t.say("5"); t.step(7, "输出 a：还是 5。", stack=[main(5)])
    else:
        t.step(6, "调用 change(a)：参数写成 int &x，x 就是 a 的“别名”——不是复印件，和 a 是同一个格子。",
               stack=[main(5, "等待 change 结束"), {"fn": "change", "vars": {"x": "（就是 a）5"}, "at": "x 是 a 的别名"}])
        t.step(2, "x = 100：改 x 就是改 a！",
               stack=[main(100, "等待 change 结束"), {"fn": "change", "vars": {"x": "（就是 a）100"}, "at": "改的是原件"}])
        t.step(3, "change 结束。", stack=[main(100)])
        t.say("100"); t.step(7, "输出 a：变成了 100。想让函数改动调用者传进来的 int 变量，可以把参数写成引用 int &x。", stack=[main(100)])
    T.append(t)

# ---- ex-09-02 fact(3) 的调用栈 ----
src = ("long long fact(int n) {\n    if (n == 0) return 1;\n    return n * fact(n - 1);\n}\nint main() {\n    cout << fact(3);\n}\n")
t = Trace("ex-09-02", "递归：fact(3) 一层一层进去，再一层一层出来", src, H)
def fr(n, at=""): return {"fn": "fact(%d)" % n, "vars": {"n": n}, "at": at}
M = lambda at: {"fn": "main", "vars": {}, "at": at}
t.step(6, "main 调用 fact(3)。每调用一次函数，就会多出一个“栈帧”，每个栈帧里有自己的 n。", stack=[M("等待 fact(3) 的结果"), fr(3, "正在执行")])
t.step(2, "fact(3)：n == 0 吗？3 不等于 0，不是出口，继续。", stack=[M("等待"), fr(3, "正在执行")])
t.step(3, "return 3 * fact(2)：要先算出 fact(2) 才能算乘法。于是 fact(3) 暂停，调用 fact(2)。注意：新的栈帧里 n 是 2，和下面那个 n = 3 互不相干。",
       stack=[M("等待"), fr(3, "暂停，等 fact(2)"), fr(2, "正在执行")])
t.step(2, "fact(2)：n == 0 吗？不是，继续。", stack=[M("等待"), fr(3, "暂停，等 fact(2)"), fr(2, "正在执行")])
t.step(3, "return 2 * fact(1)：fact(2) 也暂停，调用 fact(1)。",
       stack=[M("等待"), fr(3, "暂停，等 fact(2)"), fr(2, "暂停，等 fact(1)"), fr(1, "正在执行")])
t.step(2, "fact(1)：n == 0 吗？不是，继续。", stack=[M("等待"), fr(3, "暂停"), fr(2, "暂停"), fr(1, "正在执行")])
t.step(3, "return 1 * fact(0)：fact(1) 暂停，调用 fact(0)。",
       stack=[M("等待"), fr(3, "暂停"), fr(2, "暂停"), fr(1, "暂停，等 fact(0)"), fr(0, "正在执行")])
t.step(2, "fact(0)：n == 0 成立！这就是出口，直接 return 1，不再往下调用了。——到底了，接下来开始一层一层返回。",
       stack=[M("等待"), fr(3, "暂停"), fr(2, "暂停"), fr(1, "暂停"), fr(0, "出口：返回 1")])
t.step(3, "fact(0) 返回 1，它的栈帧消失。fact(1) 拿到 1，算 1 * 1 = 1。",
       stack=[M("等待"), fr(3, "暂停"), fr(2, "暂停"), fr(1, "拿到 1，算 1 * 1 = 1，返回")], ret=1)
t.step(3, "fact(1) 返回 1。fact(2) 拿到 1，算 2 * 1 = 2。",
       stack=[M("等待"), fr(3, "暂停"), fr(2, "拿到 1，算 2 * 1 = 2，返回")], ret=1)
t.step(3, "fact(2) 返回 2。fact(3) 拿到 2，算 3 * 2 = 6。",
       stack=[M("等待"), fr(3, "拿到 2，算 3 * 2 = 6，返回")], ret=2)
t.step(6, "fact(3) 返回 6，栈里只剩 main。", stack=[M("拿到 6，准备输出")], ret=6)
t.say("6"); t.step(6, "输出 6。写递归的两要素：① 出口（什么时候不再递归）；② 递推关系（怎样把大问题变成更小的同类问题）。", stack=[M("结束")])
T.append(t)

write_traces("func-09.js", T)

# ---------------- 小测 ----------------
q_swap = predict_quiz("预测输出：mySwap 的参数忘了写 &，交换成功吗？",
    "void mySwap(int a, int b) {\n    int t = a; a = b; b = t;\n}\nint main() {\n    int x = 1, y = 2;\n    mySwap(x, y);\n    cout << x << \" \" << y;\n}",
    ["2 1", "2 2"], "没有 & 的参数是复印件，交换的只是函数里的两份复印件，main 里的 x、y 纹丝不动，输出 {real}。写成 int &a, int &b 才能真正交换。", main=False)
q_div = predict_quiz("预测输出：用引用“返回”多个结果：",
    "void divide(int a, int b, int &q, int &r) {\n    q = a / b;\n    r = a % b;\n}\nint main() {\n    int q, r;\n    divide(17, 5, q, r);\n    cout << q << \" \" << r;\n}",
    ["17 5", "2 3", "0 0"], "q 和 r 是引用，函数里给它们赋值，就是在改 main 里的 q 和 r。17 / 5 = 3 余 2，输出 {real}。", main=False)
q_arr = predict_quiz("预测输出：数组传进函数不是复印件。输出什么？",
    "void fill(int a[], int n) {\n    for (int i = 1; i <= n; i++) a[i] = i * i;\n}\nint b[5];\nint main() {\n    fill(b, 3);\n    cout << b[1] << \" \" << b[2] << \" \" << b[3];\n}",
    ["0 0 0", "1 2 3"], "数组传进函数时，函数里改的就是原数组（不是复印件），所以 main 里能看到修改。输出 {real}。", main=False)
q_glob = predict_quiz("预测输出：局部变量和全局变量同名，会“遮住”全局的。输出什么？",
    "int n = 10;\nvoid show() { cout << n; }\nint main() {\n    int n = 5;\n    show();\n    cout << \" \" << n;\n}",
    ["5 5", "10 10", "5 10"], "show() 里用的是全局的 n（10）；main 里又声明了一个局部的 n（5），把全局的遮住了。main 里的 n 和全局的 n 是两个不同的变量。输出 {real}。", main=False)
assert crashes("long long f(int n) { return n * f(n - 1); }\nint main() { cout << f(3); return 0; }")
q_exit = quiz("fact 函数没有写出口（去掉 if (n == 0) return 1;），调用 fact(3) 会怎样？",
    ["正常算出 6", "无限递归，栈溢出，程序崩溃（RE）", "输出 0"], 1,
    "没有出口，函数会一直调用自己，栈帧越叠越多，直到栈用完程序崩溃。我们真实运行过这种写法，它确实会异常退出。出口写错也一样。")
q_ret = quiz("一个返回 int 的普通函数（不是 main），某次调用走到了函数末尾，却没有执行 return，会怎样？",
    ["自动返回 0，没问题", "这是程序错误，结果不可靠，甚至可能崩溃", "编译一定不通过"], 1,
    "不是“自动返回 0”或“返回一个随机数”那么简单：这是程序错误，后果不可预料。（main 是特例：走到末尾等于 return 0。）加 -Wall 编译，编译器会警告 control reaches end of non-void function。")
q_fib = predict_quiz("递归为什么慢？数一数：求 fib(5) 一共调用了几次 fib 函数？",
    "int cnt = 0;\nint fib(int n) {\n    cnt++;\n    if (n <= 2) return 1;\n    return fib(n - 1) + fib(n - 2);\n}\nint main() {\n    fib(5);\n    cout << cnt;\n}",
    ["5", "6", "15"], "fib(5) 要调用 fib(4) 和 fib(3)，它们又各自往下调用……同一个值被反复计算（fib(3) 就算了 2 次）。一共 {real} 次，n 一大次数暴增，所以要用“记忆化”。", main=False)

blocks = [
    ("h2", "1. 值传递和引用传递"),
    ("p", "C++ 里函数的参数<b>默认都是“复印件”</b>。想让函数改动调用者传进来的变量，可以在参数类型后面加 <code>&amp;</code>（引用）。点上面的按钮对比两种写法："),
    ("picker", ["ex-09-01a", "ex-09-01b"], ["值传递（复印件）", "引用传递（int &x）"]),
    ("quiz", q_swap),
    ("quiz", q_div),
    ("quiz", q_arr),
    ("h2", "2. 局部变量和全局变量"),
    ("quiz", q_glob),
    ("h2", "3. 递归：函数调用自己"),
    ("p", "先拿很小的 n 把过程一层一层展开：<b>谁在暂停等待、每一层的 n 是多少、结果按什么顺序返回</b>。右边的调用栈，最上面是当前正在执行的函数。"),
    ("trace", "ex-09-02"),
    ("quiz", q_exit),
    ("quiz", q_ret),
    ("quiz", q_fib),
    ("task", ["把 fact 敲一遍，在函数开头加一行 <code>cout &lt;&lt; \"进入 \" &lt;&lt; n &lt;&lt; \"\\n\";</code>，看看输出顺序是不是和上面的调用栈一样。",
              "把 mySwap 的参数加上 <code>&amp;</code>，再运行，看看输出怎么变。"],
     "本页是精选演示，其余内容（记忆化、汉诺塔、全局变量等）请读第 9 课 md。"),
]
path, nq = build_page("09-func.html", "09", "第9课｜函数与递归", "第9课 函数与递归（精选演示）", "函数与递归：复印件、原件和调用栈",
                      INTRO, "09-函数与递归.md", blocks, tracefile="func-09.js")
print("第9课: %d 个演示, %d 道小测" % (len(T), nq))
