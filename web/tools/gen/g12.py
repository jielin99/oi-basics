import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *

H = INC + "int main() {\n%SRC%\n    return 0;\n}\n"
T = []

# ---- ex-12-01 指针基础 ----
t = Trace("ex-12-01", "指针：存着“另一个变量的地址”",
          "int a = 5;\nint *p = &a;\ncout << *p << \" \";\n*p = 10;\ncout << a;\n", H)
t.step(1, "a 是一个普通变量，值 5。", {"a": 5})
t.step(2, "&a 是 a 的地址（内存格子的编号）；p 里存的就是这个地址，我们说“p 指向 a”。", {"a": 5, "p": "→ a（a 的地址）"})
t.say("5 "); t.step(3, "*p 是“p 指向的那个变量的值”（解引用），也就是 a 的值 5。", {"a": 5, "p": "→ a"})
t.step(4, "*p = 10：通过指针修改它指向的变量——a 变成了 10！", {"a": 10, "p": "→ a"})
t.say("10"); t.step(5, "输出 a：10。scanf(\"%d\", &n) 里的 &n 就是这个原理：告诉 scanf 把读到的数存到 n 的地址里。", {"a": 10, "p": "→ a"})
T.append(t)

# ---- ex-12-02 指针与数组（练习 12-1） ----
t = Trace("ex-12-02", "指针加减：p + 1 指向下一个元素",
          "int a[4] = {1, 2, 3, 4};\nint *p = a + 1;\n*p += 10;\np++;\ncout << *p << \" \" << a[1];\n", H)
a = [1, 2, 3, 4]
t.step(1, "数组 a 有 4 个元素。", arrays={"a": a})
t.step(2, "a + 1 是 a[1] 的地址（数组名在表达式里会变成指向首元素的指针）。所以 p 指向 a[1]。", vars={"p": "→ a[1]"}, arrays={"a": a}, hl={"a": 1})
a[1] += 10; t.step(3, "*p += 10：p 指向的 a[1] 加 10，变成 12。", vars={"p": "→ a[1]"}, arrays={"a": a}, hl={"a": 1})
t.step(4, "p++：指针移到下一个元素，现在指向 a[2]。", vars={"p": "→ a[2]"}, arrays={"a": a}, hl={"a": 2})
t.say("3 12"); t.step(5, "*p 是 a[2] = 3；a[1] 是 12。输出 3 12。", vars={"p": "→ a[2]"}, arrays={"a": a}, hl={"a": [1, 2]})
T.append(t)

# ---- ex-12-03 数二进制里有几个 1（练习 12-2） ----
t = Trace("ex-12-03", "位运算：n & 1 取最低位，n >>= 1 去掉最低位",
          "int n = 13, cnt = 0;\nwhile (n > 0) {\n    cnt += n & 1;\n    n >>= 1;\n}\ncout << cnt;\n", H)
n, cnt = 13, 0
b = lambda x: "%d = %s₂" % (x, bin(x)[2:])
t.step(1, "13 的二进制是 1101，里面有 3 个 1。我们用程序来数。", {"n": b(n), "cnt": cnt})
while n > 0:
    bit = n & 1; cnt += bit
    t.step(3, "n & 1：只留最低位 = %d（奇数最低位是 1，偶数是 0）。cnt += %d，cnt = %d。" % (bit, bit, cnt), {"n": b(n), "cnt": cnt})
    n >>= 1
    t.step(4, "n >>= 1：所有位右移一位，最低位被丢掉，n 变成 %s。" % (b(n) if n else "0"), {"n": b(n) if n else "0", "cnt": cnt})
t.step(2, "n = 0，循环结束。", {"n": "0", "cnt": cnt})
t.say(str(cnt)); t.step(6, "输出 %d：13 的二进制里有 %d 个 1。" % (cnt, cnt), {"n": "0", "cnt": cnt})
T.append(t)

write_traces("ptr-bit-12.js", T)

# ---------------- 小测 ----------------
q_ptr = predict_quiz("预测输出（练习 12-1）：", "int a[4] = {1, 2, 3, 4};\nint *p = a + 1;\n*p += 10;\np++;\ncout << *p << \" \" << a[1];",
    ["13 2", "2 12", "3 2"], "p 先指向 a[1]，a[1] 变成 12；p++ 后指向 a[2]，值为 3。输出 {real}。")
q_bits = predict_quiz("预测输出：六种位运算（12 = 1100，10 = 1010）：",
    "cout << (12 & 10) << \" \" << (12 | 10) << \" \" << (12 ^ 10) << \" \" << (3 << 2) << \" \" << (12 >> 2);",
    ["14 8 6 12 3", "8 14 6 3 12", "8 14 2 12 3"], "与：都是 1 才是 1 → 1000 = 8；或：有一个 1 就是 1 → 1110 = 14；异或：不同为 1 → 0110 = 6；3 << 2 相当于 ×4 = 12；12 >> 2 相当于 ÷4 = 3。输出 {real}。")
q_prec = predict_quiz("预测输出：位运算优先级很低，一定要加括号。判断 x = 4 是不是偶数：",
    "int x = 4;\nif (x & 1 == 0) cout << \"even\";\nelse cout << \"odd\";", ["even", "编译错误"], "1 == 0 的优先级比 & 高，实际算的是 x & (1 == 0) = 4 & 0 = 0（假），走 else。正确写法 (x & 1) == 0。输出 {real}。")
q_xor = predict_quiz("预测输出：异或两次相同的数等于没异或：", "int a = 7, b = 9;\ncout << (a ^ b ^ b);", ["9", "0", "14"], "a ^ b ^ b = a ^ (b ^ b) = a ^ 0 = a。输出 {real}。")
q_scanf = quiz("scanf(\"%d\", &n) 里，为什么要写 &n？",
    ["规定而已，没有道理", "scanf 需要知道把读到的数存到哪里，所以要传 n 的地址", "& 表示“并且”"], 1,
    "& 是取地址。scanf 拿到 n 的地址，才能把读到的数放进 n 里。")
cnt = 0
n = 100000
for i in range(1, n + 1):
    for j in range(i, n + 1, i): cnt += 1
q_harm = predict_quiz("估算（练习 12-3）：n = 100000 时，下面的循环里 cnt++ 一共执行多少次？",
    "int n = 100000;\nlong long cnt = 0;\nfor (int i = 1; i <= n; i++)\n    for (int j = i; j <= n; j += i)\n        cnt++;\ncout << cnt;",
    ["100000", "10000000000", "5000050000"], "内层次数是 n/1 + n/2 + n/3 + …，叫“调和级数”，大约 n × ln n，也就是 O(n log n)。这里约 1.2×10⁶，远小于 10⁸，不会超时。真实输出 {real}。")
assert cnt == int(run_cpp(INC + "int main(){int n=100000;long long cnt=0;for(int i=1;i<=n;i++)for(int j=i;j<=n;j+=i)cnt++;cout<<cnt;return 0;}"))
q_tle = quiz("题目 n ≤ 100000。你写了双重循环（O(n²)），会怎样？",
    ["10⁵ × 10⁵ = 10¹⁰ 次，远超 1 秒能做的 10⁸，肯定超时", "10⁵ 不大，肯定能过", "只要不死循环就能过"], 0,
    "先看 n 的范围，倒推需要什么复杂度。想不出满分做法时，先写暴力拿小数据的部分分——比赛按测试点给分。")
q_mem = quiz("int a[5000][5000]; 大约占多少内存？（int 占 4 字节）", ["约 25 MB", "约 100 MB", "约 400 MB"], 1,
    "5000 × 5000 = 2.5×10⁷ 个元素，× 4 字节 = 1 亿字节，约 100 MB。比赛内存限制通常 256 MB 或 512 MB，要小心。")
q_file = quiz("比赛要求文件读写，freopen 里文件名写错了（比如题目是 sum.in，你写成 Sum.in），会怎样？",
    ["没关系，大小写无所谓", "程序读不到数据，输出不对，通常是 0 分：题做对了也白做", "评测机会自动改"], 1,
    "“题做对了，文件名写错了，0 分”是考场上最惨的事。所以本地做题时就养成加 freopen 的习惯。")

blocks = [
    ("h2", "第一部分：指针（要求：能读懂初赛阅读程序题）"),
    ("trace", "ex-12-01"),
    ("quiz", q_scanf),
    ("trace", "ex-12-02"),
    ("quiz", q_ptr),
    ("h2", "第二部分：位运算"),
    ("p", "对两个数的<b>每一个二进制位</b>分别运算。在下面试试，看二进制是怎么对应的（输入范围 0~255，移位 0~20）："),
    ("calc", "bits"),
    ("quiz", q_bits),
    ("trace", "ex-12-03"),
    ("quiz", q_prec),
    ("quiz", q_xor),
    ("h2", "第三部分：比赛规范与复杂度"),
    ("html", """  <div class="card"><b>📂 freopen：从文件读入、输出到文件</b>
    <pre class="quiz-code">freopen("sum.in", "r", stdin);
freopen("sum.out", "w", stdout);</pre>
    <p style="margin:6px 0 0">练习方法：在代码所在文件夹新建 <code>sum.in</code>，写入 <code>3 5</code>，运行程序后打开 <code>sum.out</code> 应该看到 <code>8</code>。<b>从现在开始，所有在本地做的题，都尝试加上 freopen 来测试。</b></p></div>"""),
    ("quiz", q_file),
    ("html", """  <div class="card"><b>⏱ 时间复杂度：拿到题先看 n 的范围</b>
    <p style="margin:6px 0">粗略估计：评测机 1 秒大约执行 10⁸ 次简单运算（只是数量级估算，接近上限时要留余量）。</p>
    <table class="calc-tbl">
      <tr><th>n 的最大值</th><th>可以接受</th><th>估算</th></tr>
      <tr><td>20</td><td>O(2ⁿ)</td><td>2²⁰ ≈ 10⁶ ✅</td></tr>
      <tr><td>500</td><td>O(n³)</td><td>1.25×10⁸ 勉强</td></tr>
      <tr><td>5000</td><td>O(n²)</td><td>2.5×10⁷ ✅</td></tr>
      <tr><td>10⁵</td><td>O(n log n)</td><td>≈ 1.7×10⁶ ✅；O(n²) = 10¹⁰ ❌</td></tr>
      <tr><td>10⁶</td><td>O(n) 或 O(n log n)</td><td></td></tr>
      <tr><td>10⁹ 以上</td><td>O(√n)、O(log n)、O(1)</td><td></td></tr>
    </table></div>"""),
    ("quiz", q_tle),
    ("quiz", q_harm),
    ("quiz", q_mem),
    ("html", """  <div class="card"><b>🎯 部分分意识</b><ul style="margin:6px 0 0">
    <li>比赛<b>按测试点给分</b>，不是全对才有分。</li>
    <li>想不出满分做法时，<b>先写暴力</b>拿小数据的分。</li>
    <li>题目里“对于 30% 的数据，n ≤ 100”这种说明，就是在提示你部分分。</li></ul></div>"""),
    ("html", """  <div class="card"><b>🏁 结业测评</b>
    <p style="margin:6px 0 0">结业分两部分：<b>A. 考场熟练度模拟</b>（计时 3.5 小时，全程用 freopen，不看资料）；<b>B. 新题迁移测评</b>（没见过的题，由老师/家长另选）。题目和要求请看第 12 课 md 的“结业：模拟测试”一节。</p></div>"""),
    ("task", ["把指针的例子敲一遍，再试 <code>cout &lt;&lt; p;</code>，看看输出的地址长什么样（每台电脑都不同）。",
              "用 <code>n &amp; 1</code> 和 <code>n &gt;&gt;= 1</code> 写一个“数二进制里有几个 1”的程序，用 freopen 从 <code>count.in</code> 读入。"],
     "本页是精选演示，其余内容（指针与数组的关系、补码、进制转换、空间估算等）请读第 12 课 md。"),
]
path, nq = build_page("12-ptr-bit.html", "12", "第12课｜指针位运算与比赛规范", "第12课 指针、位运算与比赛规范（精选演示）", "指针、位运算和比赛规范", INTRO, "12-指针位运算与比赛规范.md", blocks, tracefile="ptr-bit-12.js")
print("第12课: %d 个演示, %d 道小测, 1 个计算器" % (len(T), nq))
