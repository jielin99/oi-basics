import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *

H = INC + "int main() {\n%SRC%\n    return 0;\n}\n"
T = []
vis = lambda s: ["␣" if c == " " else c for c in s]       # 空格在格子里显示成 ␣

# ---- ex-08-01 string 基本操作 ----
t = Trace("ex-08-01", "string：像一排字符，下标从 0 开始",
          "string s = \"hello\";\ncout << s.size() << \" \" << s[0];\ns[0] = 'H';\ns = s + \" world\";\ns += '!';\ncout << \" \" << s;\n", H)
s = "hello"
t.step(1, "s 是一个 string，里面是 5 个字符，下标 0~4。", arrays={"s": vis(s)})
t.say("5 h"); t.step(2, "s.size() 是长度 5；s[0] 是第 0 个字符 'h'。", arrays={"s": vis(s)}, hl={"s": 0})
s = "Hello"; t.step(3, "string 的字符可以修改：s[0] = 'H'，变成 Hello。", arrays={"s": vis(s)}, hl={"s": 0})
s = s + " world"; t.step(4, "用 + 可以拼接：s + \" world\"，空格也是一个字符（图里用 ␣ 表示）。", arrays={"s": vis(s)})
s += "!"; t.step(5, "s += '!' 在末尾追加一个字符。", arrays={"s": vis(s)}, hl={"s": len(s) - 1})
t.say(" " + s); t.step(6, "输出整个 string。", arrays={"s": vis(s)})
T.append(t)

# ---- ex-08-02a/b cin 后接 getline ----
for tag, extra in (("a", False), ("b", True)):
    inp = "3\nhello\n"
    src = "int n;\nstring line;\ncin >> n;\n" + ("getline(cin, line);\n" if extra else "") + "getline(cin, line);\ncout << \"[\" << line << \"]\";\n"
    ln_get = 4
    t = Trace("ex-08-02" + tag, "cin >> n 之后读一行：%s" % ("先多读一次 getline（对）" if extra else "直接 getline（经典坑）"), src, H, input=inp)
    tp = lambda pos: {"text": inp, "pos": pos}
    t.step(1, "n 和 line 都先声明。输入是两行：3 和 hello。", tape=tp(0))
    t.step(3, "cin >> n：读到 3。注意：3 后面的换行符还留在输入里没被读走！", vars={"n": 3}, tape=tp(1))
    if extra:
        t.step(4, "先来一句 getline：它从当前位置读到换行为止——读到的是“空”，同时把那个残留的换行吃掉了。", vars={"n": 3, "line": '""'}, tape=tp(2))
        t.step(5, "再 getline：现在才从 hello 这一行开始读，读到 hello，连换行一起吃掉。", vars={"n": 3, "line": "hello"}, tape=tp(8))
        t.say("[hello]"); t.step(6, "输出 [hello]，正确。前提是要读的文字在下一行；如果文字和 n 在同一行，这样写就会把它们一起丢掉。", vars={"n": 3, "line": "hello"}, tape=tp(8))
    else:
        t.step(4, "getline(cin, line)：从当前位置开始读，马上碰到残留的换行——一个字符也没读到，得到空字符串，同时把换行吃掉了。hello 还在后面没被读到！", vars={"n": 3, "line": '""'}, tape=tp(2))
        t.say("[]"); t.step(5, "输出 []：line 是空的。解决办法：中间加一句 getline(cin, line); 把残留的换行吃掉。", vars={"n": 3, "line": '""'}, tape=tp(2))
    T.append(t)

# ---- ex-08-03 字母计数：c - 'a' 当桶下标 ----
H3 = INC + "int cnt[26];\nint main() {\n%SRC%\n    return 0;\n}\n"
src = "string s = \"abca\";\nfor (char c : s) {\n    cnt[c - 'a']++;\n}\nfor (int i = 0; i < 3; i++) {\n    cout << (char)('a' + i) << \":\" << cnt[i] << \" \";\n}\n"
t = Trace("ex-08-03", "统计字母：用 c - 'a' 当桶的下标（cnt 是全局的 26 个桶）", src, H3)
cnt = [0] * 26; s = "abca"
t.step(1, "要统计 abca 里每个字母出现几次。cnt[0] 记 a，cnt[1] 记 b……全局数组一开始全是 0。", arrays={"s": list(s), "cnt": cnt})
for i, c in enumerate(s):
    cnt[ord(c) - 97] += 1
    t.step(3, "c = '%s'：c - 'a' = %d（'a'→0，'b'→1……），所以 cnt[%d]++，变成 %d。字符连续编号，减去 'a' 就得到 0~25 的下标。" % (c, ord(c) - 97, ord(c) - 97, cnt[ord(c) - 97]),
           vars={"c": c}, arrays={"s": list(s), "cnt": cnt}, hl={"s": i, "cnt": ord(c) - 97})
o = ""
for i in range(3):
    o_ = "%s:%d " % (chr(97 + i), cnt[i]); t.say(o_)
    t.step(6, "i = %d：'a' + %d 是 '%s'，(char) 把它当字符输出；cnt[%d] = %d。" % (i, i, chr(97 + i), i, cnt[i]), vars={"i": i}, arrays={"s": list(s), "cnt": cnt}, hl={"cnt": i})
T.append(t)

write_traces("str-08.js", T)

# ---------------- 小测 ----------------
q_plus = predict_quiz("预测输出：char 参与运算会变成 int。输出什么？", "char c = 'A';\ncout << c + 1 << \" \" << (char)(c + 1);", ["B B", "66 66", "A 66"], "c + 1 里 char 先变成 int（65 + 1 = 66），所以输出数字；想要字符 B，要写 (char)(c + 1)。输出 {real}。")
q_digit = predict_quiz("预测输出：数字字符怎么变成数字？", "char c = '7';\nint d = c - '0';\ncout << d + 1;", ["56", "7", "55"], "'7' 的编码是 55，'0' 是 48，相减得到数字 7，再加 1 就是 8。直接把 '7' 当数字用会得到 55。输出 {real}。")
q_up = predict_quiz("预测输出：小写变大写：", "char c = 'q';\ncout << (char)(c - 'a' + 'A');", ["q", "113", "81"], "c - 'a' 是它在字母表里的位置，加上 'A' 就是对应的大写字母。（小写 = 大写 + 32）输出 {real}。")
q_word = predict_quiz("预测输出：cin >> s 读 string，遇到空格会怎样？输入是“hello world”：", "string s;\ncin >> s;\ncout << s;", ["hello world", "world", "hello w"], "cin >> s 读“一个词”，遇到空格或换行就停，world 还在输入里没被读。要读整行用 getline(cin, s)。输出 {real}。", inp="hello world\n")
q_gl = predict_quiz("预测输出：先 cin >> n，再直接 getline，输入是“3 换行 abc”：", "int n;\nstring line;\ncin >> n;\ngetline(cin, line);\ncout << \"[\" << line << \"]\";", ["[abc]", "[3]", "[3abc]"], "getline 读到的是 n 后面残留的换行，得到空字符串。要在中间多加一句 getline 把它吃掉。输出 {real}。", inp="3\nabc\n")
assert compile_fails("int main() { string s = 'a'; return 0; }")
q_quote = quiz("string s = 'a'; 这样写对吗？", ["对，单引号双引号都行", "编译不通过：'a' 是一个字符，字符串要用双引号 \"a\"", "能编译，s 是空串"], 1, "单引号是一个字符（char），双引号是字符串。string s = \"a\"; 才得到一个 string。")
out = run_cpp(INC + "int main() { string s; cout << s.size() - 1; return 0; }")
assert len(out) >= 10 and out.isdigit()
q_size = quiz("s 是空串，cout << s.size() - 1; 会输出什么？", ["-1", "0", "一个巨大的正数"], 2,
    "size() 返回的是“无符号整数”，空串时 0 - 1 不会得到 -1，而是回绕成一个巨大的数。所以写 (int)s.size() - 1 更安全。（我们真实运行过：确实输出了一个十位以上的大数。）")

blocks = [
    ("h2", "1. char 和 ASCII 码"),
    ("p", "每个字符在计算机里都对应一个整数。<b>必须记住三段</b>：<code>'0'~'9'</code> 是 48~57，<code>'A'~'Z'</code> 是 65~90，<code>'a'~'z'</code> 是 97~122；同类字符连续编号，小写 = 大写 + 32。"),
    ("calc", "ascii"),
    ("quiz", q_plus),
    ("quiz", q_digit),
    ("quiz", q_up),
    ("h2", "2. string：一排字符"),
    ("trace", "ex-08-01"),
    ("quiz", q_word),
    ("quiz", q_quote),
    ("quiz", q_size),
    ("h2", "3. 读一整行：cin 后面接 getline 的经典坑"),
    ("p", "<code>cin &gt;&gt; n</code> 读完数字，<b>换行符还留在输入里</b>。对比一下两种写法："),
    ("picker", ["ex-08-02a", "ex-08-02b"], ["直接 getline（读到空行）", "先多读一次（正确）"]),
    ("quiz", q_gl),
    ("h2", "4. 统计字母：c - 'a' 当桶的下标"),
    ("trace", "ex-08-03"),
    ("task", ["把统计字母的例子敲一遍，输入你的英文名，看每个字母出现几次。",
              "把“先 cin >> n 再 getline”的两种写法都敲一遍，输入 <code>3</code> 换行 <code>abc</code>，亲眼看看区别。"],
     "本页是精选演示，其余内容（string 常用函数、char 数组等）请读第 8 课 md。"),
]
path, nq = build_page("08-string.html", "08", "第8课｜字符与字符串", "第8课 字符与字符串（精选演示）", "字符与字符串：ASCII、string 和 getline", INTRO, "08-字符与字符串.md", blocks, tracefile="str-08.js")
print("第8课: %d 个演示, %d 道小测" % (len(T), nq))
