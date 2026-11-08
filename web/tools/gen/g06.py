import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *

H = INC + "int main() {\n%SRC%\n    return 0;\n}\n"
T = []

# ---- ex-06-01 break / continue ----
t = Trace("ex-06-01", "break 和 continue：跳过、提前结束",
          "for (int i = 1; i <= 10; i++) {\n    if (i % 3 == 0) continue;\n    if (i > 7) break;\n    cout << i << \" \";\n}\n", H)
t.step(1, "i 从 1 开始，一圈一圈往下走。", {"i": 1})
for i in range(1, 11):
    if i % 3 == 0:
        t.step(2, "i = %d，%d %% 3 == 0 成立 → continue：跳过本圈后面的代码，直接去做 i++，进入下一圈。" % (i, i), {"i": i})
    elif i > 7:
        t.step(3, "i = %d，%d > 7 成立 → break：整个循环立刻结束，不再回去判断。" % (i, i), {"i": i})
        break
    else:
        t.say("%d " % i)
        t.step(4, ("i = %d，不是 3 的倍数，也没超过 7，" % i if i > 1 else "i = 1，不是 3 的倍数，也没超过 7，") + "输出 %d。" % i, {"i": i})
T.append(t)

# ---- ex-06-02 拆数位 ----
t = Trace("ex-06-02", "拆数位：用 % 10 和 / 10",
          "int n = 123, digitSum = 0, rev = 0;\nwhile (n > 0) {\n    int d = n % 10;\n    digitSum += d;\n    rev = rev * 10 + d;\n    n /= 10;\n}\ncout << digitSum << \" \" << rev;\n", H)
n, ds, rev = 123, 0, 0
t.step(1, "n = 123 是要拆的数；digitSum 记数位之和，rev 记反转后的数，都先清 0。", {"n": n, "digitSum": 0, "rev": 0})
while n > 0:
    d = cmod(n, 10)
    t.step(3, "while (n > 0) 成立。d = %d %% 10 = %d：取出个位。" % (n, d), {"n": n, "digitSum": ds, "rev": rev, "d": d})
    ds += d
    t.step(4, "digitSum += d，变成 %d。" % ds, {"n": n, "digitSum": ds, "rev": rev, "d": d})
    rev = rev * 10 + d
    t.step(5, "rev = rev * 10 + d：把 rev 左移一位再接上 d，变成 %d。" % rev, {"n": n, "digitSum": ds, "rev": rev, "d": d})
    n = cdiv(n, 10)
    t.step(6, "n /= 10：去掉个位，n 变成 %d。" % n, {"n": n, "digitSum": ds, "rev": rev})
t.step(2, "n = 0，0 > 0 不成立，循环结束。", {"n": n, "digitSum": ds, "rev": rev})
t.say("%d %d" % (ds, rev))
t.step(8, "输出数位之和 %d 和反转数 %d。" % (ds, rev), {"n": n, "digitSum": ds, "rev": rev})
T.append(t)

# ---- ex-06-03a/b 判断质数 ----
for tag, N in (("a", 7), ("b", 15)):
    src = ("int n = %d;\nbool isPrime = true;\nfor (int i = 2; i <= n / i; i++) {\n    if (n %% i == 0) {\n        isPrime = false;\n"
           "        break;\n    }\n}\ncout << (isPrime ? \"prime\" : \"not prime\");\n") % N
    t = Trace("ex-06-03" + tag, "判断质数：只试到 √n（n = %d）" % N, src, H)
    prime = True
    t.step(1, "要判断 n = %d 是不是质数。" % N, {"n": N})
    t.step(2, "先假设它是质数。", {"n": N, "isPrime": "true"})
    i = 2
    while True:
        lim = cdiv(N, i)
        if i <= lim:
            t.step(3, "i = %d，n / i = %d，%d <= %d 成立，进入循环体。（i <= n / i 就是 i×i <= n：只试到 √n）" % (i, lim, i, lim),
                   {"n": N, "isPrime": str(prime).lower(), "i": i})
            if N % i == 0:
                t.step(4, "%d %% %d == 0 成立：%d 能被 %d 整除！" % (N, i, N, i), {"n": N, "isPrime": "true", "i": i})
                prime = False
                t.step(5, "isPrime = false：它不是质数。", {"n": N, "isPrime": "false", "i": i})
                t.step(6, "break：已经找到因数，没必要再试了，直接跳出循环。", {"n": N, "isPrime": "false", "i": i})
                break
            t.step(4, "%d %% %d = %d，不等于 0，不能整除，继续试下一个。" % (N, i, N % i), {"n": N, "isPrime": "true", "i": i})
            i += 1
        else:
            t.step(3, "i = %d，n / i = %d，%d <= %d 不成立，循环结束：√n 以内没有因数。" % (i, lim, i, lim), {"n": N, "isPrime": "true", "i": i})
            break
    t.say("prime" if prime else "not prime")
    t.step(9, "输出 %s。" % ("prime" if prime else "not prime"), {"n": N, "isPrime": str(prime).lower()})
    T.append(t)

# ---- ex-06-04 嵌套循环：直角三角形 ----
t = Trace("ex-06-04", "嵌套循环：打印 3 行直角三角形",
          "for (int i = 1; i <= 3; i++) {\n    for (int j = 1; j <= i; j++) {\n        cout << \"*\";\n    }\n    cout << \"\\n\";\n}\n", H)
for i in range(1, 4):
    t.step(1, "外层 i = %d：开始打印第 %d 行。外层管“第几行”。" % (i, i), {"i": i})
    for j in range(1, i + 1):
        t.say("*")
        t.step(3, ("内层 j 从 1 开始，" if j == 1 else "j++ 变成 %d，" % j) + "j <= %d 成立，输出一个 *。内层管“这一行打印什么”。" % i, {"i": i, "j": j})
    t.say("\n")
    t.step(5, "j 变成 %d，%d <= %d 不成立，这一行打完了，换行。第 %d 行共 %d 个 *，所以内层上限是 i。" % (i + 1, i + 1, i, i, i), {"i": i})
t.step(1, "i 变成 4，4 <= 3 不成立，整个双重循环结束。", {"i": 4})
T.append(t)

p = write_traces("loop-06.js", T)

# ---------------- 小测 ----------------
# 1 分号
q_semi = predict_quiz("预测输出：for 括号后面多写了一个分号，会输出什么？",
    "int s = 0, i;\nfor (i = 1; i <= 3; i++);\ns += i;\ncout << s;",
    ["6", "3", "0"], "多出来的 ; 让循环体变成了空语句：循环空转到 i 变成 4 才结束，然后 s += i 只执行一次，s = 0 + 4 = {real}。")
# 2 累加变量位置
q_init = predict_quiz("想输出累计和 1 3 6，但 sum 的初始化写在了循环里面，实际输出是什么？",
    "for (int i = 1; i <= 3; i++) {\n    int sum = 0;\n    sum += i;\n    cout << sum << \" \";\n}",
    ["1 3 6", "6", "0 0 0"], "每一圈都会重新执行 int sum = 0，上一圈的结果被清掉了，所以只能看到 {real}。累加变量要放在循环外面初始化。")
# 3 逗号
assert compile_fails("int main() { for (int i = 1, i <= 3, i++) { } return 0; }")
q_comma = quiz("for 括号里的三部分用逗号分隔：for (int i = 1, i <= 3, i++)，会怎样？",
    ["正常运行，输出 1 2 3", "编译不通过：三部分必须用分号分隔", "死循环"], 1,
    "for 的三部分是用分号 ; 隔开的，写成逗号编译器会报错。（Python 程序员容易写错的地方。）")
# 4 作用域
assert compile_fails("int main() { for (int i = 1; i <= 3; i++) { } cout << i; return 0; }")
q_scope = quiz("在 for 里声明了 int i，循环结束后还想用 i：cout << i; 会怎样？",
    ["输出 4", "输出 3", "编译不通过：出了循环，i 就不存在了"], 2,
    "在 for 里声明的变量只在这个 for 里面有效。如果循环结束后还要用 i，要把 int i 声明在 for 外面。")
# 5 break 只跳最内层
q_break = predict_quiz("预测输出：break 在内层循环里，跳出的是哪一层？",
    "for (int i = 1; i <= 2; i++) {\n    for (int j = 1; j <= 3; j++) {\n        if (j == 2) break;\n        cout << i << j << \" \";\n    }\n}",
    ["11", "11 12 13 21 22 23", "11 12"], "break 只跳出最内层的那个循环（j 的循环）。i = 1 时 j = 2 就跳出；外层 i 继续，i = 2 时再来一遍，所以是 {real}。")
# 6 long long
assert 100000 * 100001 // 2 > 2147483647 and 100000 * 100001 // 2 < 9223372036854775807
q_ll = quiz("求 1 + 2 + … + 100000 的和（约 50 亿），累加变量 sum 应该用什么类型？",
    ["int", "long long", "char"], 1,
    "1 到 100000 的和是 5000050000，超过 int 的最大值 2147483647（约 21 亿），要用 long long。")
# 7 for 步长
q_step = predict_quiz("变一变：把步长改成 i += 2，会输出什么？",
    "for (int i = 1; i <= 7; i += 2) {\n    cout << i << \" \";\n}", ["1 2 3 4 5 6 7", "1 3 5", "3 5 7"], "i 从 1 开始，每圈加 2：1、3、5、7，7 <= 7 还成立，所以是 {real}。")
# 8 拆数位变式
q_digit = predict_quiz("变一变：如果 n 是 405，这段代码会输出什么？",
    "int n = 405, digitSum = 0, rev = 0;\nwhile (n > 0) {\n    int d = n % 10;\n    digitSum += d;\n    rev = rev * 10 + d;\n    n /= 10;\n}\ncout << digitSum << \" \" << rev;",
    ["9 54", "5 504", "9 405"], "5、0、4 依次取出：数位和 9；rev 依次是 5、50、504，所以反转数是 504（前导的 0 在末尾）。输出 {real}。")

blocks = [
    ("h2", "1. for 循环：初始化 → 判断 → 循环体 → 更新"),
    ("p", "<code>for (int i = 1; i &lt;= 3; i++)</code> 的执行顺序：<b>先初始化一次</b>，然后反复“判断 → 循环体 → 更新”，直到判断不成立。注意最后一次判断失败时，循环体不会执行。"),
    ("trace", "loop-sum"),
    ("quiz", quiz("上面的循环里，条件 i <= 3 一共被判断了几次？", ["3 次", "4 次", "5 次"], 1,
                  "i 为 1、2、3 时成立（3 次），i 变成 4 时还要判断一次才发现不成立，所以是 4 次。")),
    ("quiz", q_step),
    ("quiz", q_semi),
    ("quiz", q_init),
    ("quiz", q_ll),
    ("h2", "2. break 和 continue"),
    ("p", "<code>continue</code>：跳过这一圈剩下的代码，去做更新、进入下一圈。<code>break</code>：整个循环马上结束。"),
    ("trace", "ex-06-01"),
    ("quiz", q_break),
    ("h2", "3. 拆数位：while + % 10 + / 10"),
    ("p", "<code>n % 10</code> 取出个位，<code>n / 10</code> 去掉个位。重复到 n 变成 0，就把每一位都处理了。"),
    ("trace", "ex-06-02"),
    ("quiz", q_digit),
    ("h2", "4. 判断质数：只试到 √n"),
    ("p", "如果 n = a × b 且 a ≤ b，那么 a ≤ √n，所以只需要试到 √n。写成 <code>i &lt;= n / i</code>，既避免浮点误差，也避免 <code>i * i</code> 溢出。点上面的按钮可以换一个 n 再看一遍。"),
    ("picker", ["ex-06-03a", "ex-06-03b"], ["n = 7（质数）", "n = 15（不是质数）"]),
    ("h2", "5. 嵌套循环：打印图形"),
    ("p", "<b>外层管“第几行”，内层管“这一行打印什么”</b>。先在纸上写出每一行的行号和星号数，找到它们的关系，再写代码。"),
    ("trace", "ex-06-04"),
    ("quiz", q_comma),
    ("quiz", q_scope),
    ("task", ["把拆数位的例子敲一遍，把 <code>n</code> 改成你的生日（如 20120315），<b>先猜</b>数位和与反转数，再运行。",
              "把直角三角形改成 5 行；再试试改成“每行 <code>2*i-1</code> 个星”，看看图形怎么变。",
              "做洛谷入门题单里“循环结构”那一组题（题号见 md）。"],
     "本页是精选演示，其余内容（do-while、求最值、九九乘法表、死循环调试等）请读第 6 课 md。"),
]
path, nq = build_page("06-loop.html", "06", "第6课｜循环", "第6课 循环结构（精选演示）", "循环：一圈一圈重复做事",
                      INTRO, "06-循环结构.md", blocks, tracefile=["loop-demo.js", "loop-06.js"])
print("第6课: %d 个演示, %d 道小测" % (len(T) + 1, nq))
