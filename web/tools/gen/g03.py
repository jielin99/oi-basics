import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *

H = INC + "int main() {\n%SRC%\n    return 0;\n}\n"
T = []

# ---- ex-03-01 cin >> a >> b（空格分隔 / 分行输入） ----
for tag, inp, how in (("a", "12 30\n", "用空格隔开"), ("b", "12\n30\n", "分两行输入")):
    t = Trace("ex-03-01" + tag, "cin 读入两个整数（%s）" % how, "int a, b;\ncin >> a >> b;\ncout << a + b;\n", H, input=inp)
    tp = lambda pos: {"text": inp, "pos": pos}
    t.step(1, "声明两个整数盒子 a、b，还没有值。下面是键盘输入的内容，cin 从左往右一个字符一个字符地读。", tape=tp(0))
    # 读 a：从 0 开始读到第一个空白前
    i = 0; j = inp.index(inp.split()[0]) + len(inp.split()[0]); a = int(inp.split()[0])
    t.step(2, "cin >> a：先跳过前面的空白，再按 a 的类型（整数）往后读，读到不属于数字的字符（这里是空格或换行）就停。读到 %d，放进 a。" % a, vars={"a": a}, tape=tp(j))
    k = j
    while inp[k] in " \n": k += 1
    b = int(inp.split()[1]); k += len(inp.split()[1])
    t.step(2, "cin >> b：先跳过 %s，再读一个整数，读到 %d。所以数字用空格隔开、还是分行输入，对 cin 来说都一样。" % ("空格" if tag == "a" else "换行", b), vars={"a": a, "b": b}, tape=tp(k))
    t.say(str(a + b)); t.step(3, "输出 a + b = %d。" % (a + b), vars={"a": a, "b": b}, tape=tp(k))
    T.append(t)

# ---- ex-03-02 读到文件结束 ----
inp = "3 5 4\n"
t = Trace("ex-03-02", "while (cin >> x)：读到输入结束为止",
          "int x, sum = 0;\nwhile (cin >> x) {\n    sum += x;\n}\ncout << sum;\n", H, input=inp)
tp = lambda pos: {"text": inp, "pos": pos}
t.step(1, "sum 先清 0。x 还没有值。", vars={"sum": 0}, tape=tp(0))
sum_ = 0
for tok, pos in ((3, 1), (5, 3), (4, 5)):
    t.step(2, "cin >> x 读成功（读到 %d）：while 会检查 cin 的状态，没有出错，条件为真，进入循环体。" % tok, vars={"sum": sum_, "x": tok}, tape=tp(pos))
    sum_ += tok
    t.step(3, "sum += x，sum 变成 %d。" % sum_, vars={"sum": sum_, "x": tok}, tape=tp(pos))
t.step(2, "再读：跳过换行后，输入已经到头了（EOF），读失败，条件为假，循环结束。本地测试时输完数据按 Ctrl+Z 再回车就是告诉程序“输入结束”。", vars={"sum": sum_, "x": 4}, tape=tp(len(inp)))
t.say(str(sum_)); t.step(5, "输出 %d。" % sum_, vars={"sum": sum_, "x": 4}, tape=tp(len(inp)))
T.append(t)

write_traces("io-03.js", T)

# ---------------- 小测 ----------------
q_w = predict_quiz("预测输出：宽度、对齐、补 0（方括号只是帮你看清空格）：",
    "printf(\"[%5d][%-5d][%05d]\", 42, 42, 42);", ["[42][42][42]", "[00042][42   ][   42]"], "%5d 宽度 5、右对齐，前面补空格；%-5d 左对齐，后面补空格；%05d 前面补 0。输出 {real}。")
q_avg = predict_quiz("预测输出：求平均数，3.0 不能写成 3：",
    "double a = 7 / 2;\ndouble b = 7 / 2.0;\nprintf(\"%.2f %.2f\", a, b);", ["3.50 3.50", "3.00 3.00", "3 3.5"], "7 / 2 两边都是整数，是整数除法，得 3，再变成 3.00；7 / 2.0 才是小数除法，得 3.50。%.2f 表示保留 2 位小数。输出 {real}。")
q_char = predict_quiz("预测输出：cin 读 char 会跳过空白。输入是“A B”：",
    "char c1, c2;\ncin >> c1 >> c2;\ncout << c1 << c2;", ["A B", "A", "BA"], "cin 读 char 时会先跳过空格和换行，读一个非空白字符。第二个读到的是 B，不是空格。输出 {real}。", inp="A B\n")
q_amp = quiz("scanf 读普通 int 变量，写成 scanf(\"%d\", n); 忘了 & 会怎样？",
    ["没问题，一样能读", "行为没有保证：常见是程序崩溃，也可能读出错误的值", "编译一定不通过"], 1,
    "scanf 要知道把读到的数放在哪，所以普通变量前要加 &（传地址，第 12 课解释原因）。忘了 & 编译常常能通过，但运行结果没有保证。")
q_lf = quiz("用 scanf 读 double 变量应该用哪个格式符？", ["%f", "%lf", "%d"], 1,
    "scanf 读 double 要用 %lf（printf 输出 double 用 %f 就行）。用 %f 读会读出错误的值。读 long long 要用 %lld，不能用 %d。")
q_prompt = quiz("比赛的程序里写了 cout << \"请输入 n：\"; 会怎样？",
    ["没关系，只是提示", "输出多了文字，评测会判 WA（答案错误）", "评测会自动忽略"], 1,
    "评测是把你的输出和标准答案逐字比对的。比赛程序只输出题目要求的内容，不要有任何提示文字。")
q_mix = quiz("加了 ios::sync_with_stdio(false); 加速以后，可以混用 cin 和 scanf 吗？",
    ["可以，没有影响", "不可以，会导致输入输出顺序乱掉；要么全用 C++ 风格，要么全用 C 风格", "只有 cout 和 printf 不能混用"], 1,
    "加速以后，不能再混用 cin 和 scanf（或 cout 和 printf）。初学时一个程序里只选一种风格。")

blocks = [
    ("h2", "1. cin 是怎么读数据的"),
    ("p", "输入的内容像一条“传送带”，<b>cin 从左往右一个一个读</b>：先跳过空白，再按变量的类型读取（读整数就读数字，读 char 就读一个非空白字符）。灰色划掉的是已经读走的，黄色是下一个要读的位置。"),
    ("picker", ["ex-03-01a", "ex-03-01b"], ["数字用空格隔开", "数字分两行输入"]),
    ("quiz", q_char),
    ("h2", "2. 读到输入结束"),
    ("trace", "ex-03-02"),
    ("h2", "3. 控制输出格式：printf"),
    ("p", "下面的小工具可以试各种格式（和真实 C++ 的 printf 逐项对照过）。<b>%.2f</b> 保留两位小数，数字是宽度，<b>-</b> 左对齐，<b>0</b> 补零。"),
    ("calc", "fmt"),
    ("quiz", q_w),
    ("quiz", q_avg),
    ("h2", "4. 几个容易错的地方"),
    ("quiz", q_amp),
    ("quiz", q_lf),
    ("quiz", q_prompt),
    ("quiz", q_mix),
    ("task", ["把 cin 的例子敲一遍，输入 <code>12 30</code> 和分两行输入各试一次，看看结果是不是一样。",
              "把总分、平均分的例子用 scanf/printf 敲一遍：输入 <code>90 85 77</code>，看看保留两位小数的平均分。"],
     "本页是精选演示，其余内容（scanf 完整用法、cout 保留小数、加速等）请读第 3 课 md。"),
]
path, nq = build_page("03-io.html", "03", "第3课｜输入输出", "第3课 输入输出（精选演示）", "输入输出：cin 怎么读数据，printf 怎么排版", INTRO, "03-输入输出.md", blocks, tracefile="io-03.js")
print("第3课: %d 个演示, %d 道小测" % (len(T), nq))
