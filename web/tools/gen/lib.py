"""课件生成库（开发期使用，学生端不需要）。

两件事：
1. Trace：用 Python 按 C++ 语义逐步"推演"，每步记录执行该行【之后】的状态；
   finish() 时把 harness 真实编译运行，推演出的输出必须与真实输出一致，否则当场报错。
2. 页面/小测：predict_quiz 的正确答案由真实编译运行得出，不靠手写。
"""
import copy, hashlib, html, json, os, re, subprocess, tempfile

WEB = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# (课次, 主题, 页面文件, md 文件)；上下课导航、md 链接改写、目录页都用它
LESSONS = [("第 0 课", "环境搭建", "00-setup.html", "00-环境搭建.md"),
           ("第 1 课", "第一个程序", "01-first.html", "01-第一个程序.md"),
           ("第 2 课", "变量与数据类型", "02-types.html", "02-变量与数据类型.md"),
           ("第 3 课", "输入输出", "03-io.html", "03-输入输出.md"),
           ("第 4 课", "运算符与表达式", "04-operator.html", "04-运算符与表达式.md"),
           ("第 5 课", "分支结构", "05-branch.html", "05-分支结构.md"),
           ("第 6 课", "循环结构", "06-loop.html", "06-循环结构.md"),
           ("第 7 课", "数组", "07-array.html", "07-数组.md"),
           ("第 8 课", "字符与字符串", "08-string.html", "08-字符与字符串.md"),
           ("第 9 课", "函数与递归", "09-func.html", "09-函数与递归.md"),
           ("第 10 课", "结构体与排序", "10-sort.html", "10-结构体与排序.md"),
           ("第 11 课", "STL 入门", "11-stl.html", "11-STL入门.md"),
           ("第 12 课", "指针、位运算与比赛规范", "12-ptr-bit.html", "12-指针位运算与比赛规范.md"),
           ("附录 A", "Python 与 C++ 对照", "A-python-cpp.html", "附录A-Python与C++对照.md"),
           ("附录 B", "常见错误与调试", "B-errors.html", "附录B-常见错误与调试.md"),
           ("附录 C", "考场模板与规范", "C-template.html", "附录C-考场模板与规范.md")]
MD2PAGE = {m: p for _, _, p, m in LESSONS}
INC = "#include <iostream>\n#include <cstdio>\n#include <cmath>\n#include <string>\n#include <algorithm>\nusing namespace std;\n"


def norm(s):
    return "\n".join(l.rstrip() for l in s.replace("\r\n", "\n").strip().split("\n"))


def run_cpp(src, inp="", std="c++11"):
    with tempfile.TemporaryDirectory() as d:
        cpp, exe = os.path.join(d, "a.cpp"), os.path.join(d, "a.out")
        open(cpp, "w").write(src)
        c = subprocess.run(["g++", "-std=" + std, cpp, "-o", exe], capture_output=True, text=True)
        if c.returncode != 0:
            raise RuntimeError("编译失败:\n" + c.stderr + "\n---\n" + src)
        r = subprocess.run([exe], input=inp, capture_output=True, text=True, timeout=5)
        if r.returncode != 0:
            raise RuntimeError("运行退出码 %d\n%s" % (r.returncode, src))
        return r.stdout


def cdiv(a, b):   # C++ 整除：向 0 取整
    q = abs(a) // abs(b)
    return q if (a >= 0) == (b >= 0) else -q


def cmod(a, b):   # C++ 取模：符号与被除数相同
    return a - cdiv(a, b) * b


class Trace:
    def __init__(self, id, title, source, harness, input="", kind="normal", base=None, cols=None, badge=None):
        self.id, self.title, self.source, self.harness = id, title, source, harness
        self.input, self.kind, self.base, self.cols, self.badge = input, kind, base, cols, badge
        self.steps, self.out = [], ""
        self.nlines = len(source.rstrip("\n").split("\n"))

    def say(self, s):          # 模拟 cout / printf 输出
        self.out += s

    def step(self, line, note, vars=None, arrays=None, hl=None, stack=None, tape=None, ret=None):
        assert 0 <= line <= self.nlines, "%s: line %d 超出 0..%d" % (self.id, line, self.nlines)
        s = dict(line=line, vars=copy.deepcopy(vars or {}), arrays=copy.deepcopy(arrays or {}),
                 hl=copy.deepcopy(hl or {}), out=self.out, note=note)
        if stack is not None: s["stack"] = copy.deepcopy(stack)
        if tape is not None: s["tape"] = dict(tape)
        if ret is not None: s["ret"] = ret
        self.steps.append(s)

    def finish(self):
        src = self.harness.replace("%SRC%", self.source)
        if self.kind == "normal":
            real = run_cpp(src, self.input)
            assert norm(real) == norm(self.out), "%s: 推演输出 %r 与真实输出 %r 不一致" % (self.id, self.out, real)
            expect = norm(real)
        else:
            run_cpp(src, self.input)     # illustrative：只要求能编译、能运行
            expect = ""
        d = dict(title=self.title, source=self.source, harness=self.harness, input=self.input,
                 expectOutput=expect, kind=self.kind, steps=self.steps)
        if self.base: d["base"] = self.base
        if self.cols: d["cols"] = self.cols
        if self.badge: d["badge"] = self.badge
        return d


def write_traces(filename, traces, note=""):
    out = "window.TRACES = window.TRACES || {};\n/* 由 tools/gen 生成；最终输出由 verify-traces 真实编译比对。%s */\n" % note
    for t in traces:
        d = t.finish()
        out += "window.TRACES[%s] = %s;\n" % (json.dumps(t.id), json.dumps(d, ensure_ascii=False, indent=1))
    path = os.path.join(WEB, "data", "traces", filename)
    open(path, "w", encoding="utf-8").write(out)
    return path


# ---------------- 小测 ----------------
def quiz(q, options, answer, explain, code=None):
    d = dict(q=q, options=options, answer=answer, explain=explain)
    if code: d["code"] = code
    return d


def predict_quiz(q, code, wrong, explain, main=True, inp="", pre="", extra_q=""):
    """预测输出题：正确答案 = 真实编译运行的输出。wrong 为干扰项（不得与真实输出相同）。"""
    body = code if not main else "int main() {\n" + code + "\n    return 0;\n}\n"
    real = norm(run_cpp(INC + pre + "\n" + body, inp))
    show = lambda x: x.replace("\n", " ⏎ ")
    assert all(norm(w) != real for w in wrong), "干扰项与真实输出相同：%r" % real
    opts = [real] + list(wrong)
    h = int(hashlib.md5((q + real).encode()).hexdigest(), 16)
    order = sorted(range(len(opts)), key=lambda i: (h >> (i * 5)) % 997 + i * 0.001)
    shown = [show(opts[i]) for i in order]
    return dict(q=q, code=code.strip("\n"), options=shown, answer=order.index(0), explain=explain.replace("{real}", show(real)))


def compile_fails(code, pre=""):
    with tempfile.TemporaryDirectory() as d:
        cpp = os.path.join(d, "a.cpp")
        open(cpp, "w").write(INC + pre + "\n" + code)
        return subprocess.run(["g++", "-std=c++11", cpp, "-o", os.path.join(d, "a")], capture_output=True, text=True).returncode != 0


def crashes(code, pre=""):
    """能编译、但运行时非正常退出（如除以 0）。用来核实“这样写会出错”的断言。"""
    with tempfile.TemporaryDirectory() as d:
        cpp, exe = os.path.join(d, "a.cpp"), os.path.join(d, "a")
        open(cpp, "w").write(INC + pre + "\n" + code)
        c = subprocess.run(["g++", "-std=c++11", cpp, "-o", exe], capture_output=True, text=True)
        assert c.returncode == 0, c.stderr
        return subprocess.run([exe], capture_output=True, text=True, timeout=5).returncode != 0



# ---------------- md → HTML（附录与第 0 课正文由 md 直接转出，保证内容一致） ----------------
def _fix_href(u):
    """页面都在 lessons/ 下，只发布 web/ 目录：md 链接改成课页，code/ 下的文件用 web/code/ 里的复制件。"""
    if re.match(r"^(https?:|#|mailto:)", u): return u
    base = os.path.basename(u)
    if base in MD2PAGE: return MD2PAGE[base]
    if u.startswith("code/"):
        import shutil                                   # 局域网/静态服务只发布 web/，把源文件复制过来
        os.makedirs(os.path.join(WEB, "code"), exist_ok=True)
        shutil.copyfile(os.path.join(WEB, "..", u), os.path.join(WEB, u))
        return "../" + u
    raise ValueError("无法改写的相对链接：%s" % u)


def md_inline(s):
    codes = []
    s = re.sub(r"`[^`]+`", lambda m: (codes.append(m.group(0)) or "\x01%d\x01" % (len(codes) - 1)), s)   # 先保护行内代码
    links = []
    def grab(m):
        label = re.sub(r"\x01(\d+)\x01", lambda k: codes[int(k.group(1))], m.group(1))
        links.append('<a href="%s">%s</a>' % (html.escape(_fix_href(m.group(2)), quote=True), md_inline(label)))
        return "\x00%d\x00" % (len(links) - 1)
    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", grab, s)
    parts = re.split(r"(\x01\d+\x01)", s)
    is_code = lambda p: len(p) > 2 and p.startswith("\x01") and p.endswith("\x01")
    # 粗体可以跨过行内代码（**数据量大时用 `"\n"`**），所以按整句配对，而不是在每段里单独找
    balanced = sum(p.count("**") for p in parts if not is_code(p)) % 2 == 0
    bold, out = False, []
    for part in parts:
        if is_code(part):
            out.append("<code>%s</code>" % html.escape(codes[int(part[1:-1])][1:-1]))
        else:
            q = html.escape(part, quote=False)
            if balanced:
                pieces = q.split("**"); q = pieces[0]
                for piece in pieces[1:]:
                    bold = not bold; q += ("<b>" if bold else "</b>") + piece
            out.append(q)
    r = "".join(out)
    return re.sub(r"\x00(\d+)\x00", lambda m: links[int(m.group(1))], r)


def _split_row(line):
    cells = re.split(r"(?<!\\)\|", line.strip())
    if cells and cells[0].strip() == "": cells = cells[1:]
    if cells and cells[-1].strip() == "": cells = cells[:-1]
    return [c.strip().replace("\\|", "|") for c in cells]


_LI = re.compile(r"^(\s*)([-*]|\d+\.)\s+(.*)$")


def _render_list(items):
    """items: [(indent, ordered, text, 序号)] → 嵌套 ul/ol；有序列表按第一项的序号起算（被代码块打断后从 4 继续）"""
    out, stack = [], []          # stack: [(indent, tag)]
    for ind, ordered, text, num in items:
        tag = "ol" if ordered else "ul"
        while stack and ind < stack[-1][0]:
            out.append("</li></%s>" % stack.pop()[1])
        if stack and ind == stack[-1][0]:
            out.append("</li>")
        elif not stack or ind > stack[-1][0]:
            out.append(('<ol start="%d">' % num) if (ordered and num != 1) else "<%s>" % tag); stack.append((ind, tag))
        m = re.match(r"^\[( |x)\]\s+(.*)$", text)
        if m:
            out.append('<li class="task"><label><input type="checkbox" class="chk"> %s</label>' % md_inline(m.group(2)))
        else:
            out.append("<li>%s" % md_inline(text))
    while stack:
        out.append("</li></%s>" % stack.pop()[1])
    return "".join(out)


def _blocks(lines):
    """把一段 md 行转成 html（不含 ## 分节）"""
    out, i, n = [], 0, len(lines)
    while i < n:
        ln = lines[i]
        if not ln.strip() or re.match(r"^---+\s*$", ln):
            i += 1; continue
        if ln.startswith("````") or ln.startswith("~~~"):
            raise ValueError("不支持的代码围栏（只支持 3 个反引号）：%r" % ln)
        if ln.startswith("```"):
            lang = ln[3:].strip(); i += 1; buf = []
            while i < n and not lines[i].startswith("```"): buf.append(lines[i]); i += 1
            i += 1
            out.append('<pre class="quiz-code"><code>%s</code></pre>' % html.escape("\n".join(buf)))
        elif ln.startswith(">"):
            buf = []
            while i < n and lines[i].startswith(">"): buf.append(re.sub(r"^>\s?", "", lines[i])); i += 1
            out.append("<blockquote>%s</blockquote>" % "".join(_blocks(buf)))
        elif ln.startswith("|") and i + 1 < n and re.match(r"^\|[\s:\-|]+\|\s*$", lines[i + 1]):
            head = _split_row(ln); i += 2; rows = []
            while i < n and lines[i].startswith("|"): rows.append(_split_row(lines[i])); i += 1
            t = '<table class="calc-tbl"><tr>%s</tr>' % "".join("<th>%s</th>" % md_inline(c) for c in head)
            for r in rows: t += "<tr>%s</tr>" % "".join("<td>%s</td>" % md_inline(c) for c in r)
            out.append(t + "</table>")
        elif ln.startswith("<details"):
            if ln.strip() != "<details>": raise ValueError("不支持的 <details> 写法（必须独占一行）：%r" % ln)
            out.append('<details class="ans">'); i += 1
        elif ln.startswith("</details"):
            if ln.strip() != "</details>": raise ValueError("不支持的 </details> 写法：%r" % ln)
            out.append("</details>"); i += 1
        elif ln.startswith("<summary"):
            m = re.fullmatch(r"<summary>(.*)</summary>", ln.strip())
            if not m: raise ValueError("不支持的 <summary> 写法（必须是独占一行的 <summary>文字</summary>）：%r" % ln)
            out.append("<summary>%s</summary>" % md_inline(m.group(1).strip())); i += 1
        elif ln.startswith("### "):
            out.append("<h3>%s</h3>" % md_inline(ln[4:].strip())); i += 1
        elif _LI.match(ln):
            items = []
            while i < n:
                m = _LI.match(lines[i])
                if m:
                    items.append([len(m.group(1)), m.group(2)[0].isdigit(), m.group(3), int(m.group(2)[:-1]) if m.group(2)[0].isdigit() else 0]); i += 1
                elif lines[i].startswith((" ", "\t")) and lines[i].strip() and items:
                    items[-1][2] += " " + lines[i].strip(); i += 1
                elif not lines[i].strip() and i + 1 < n and _LI.match(lines[i + 1]) and items and _LI.match(lines[i + 1]).group(1):
                    i += 1
                else:
                    break
            out.append(_render_list(items))
        else:
            buf = []
            while i < n and lines[i].strip() and not lines[i].startswith(("```", ">", "|", "### ", "<details", "</details>", "<summary>")) and not _LI.match(lines[i]) and not re.match(r"^---+\s*$", lines[i]):
                buf.append(lines[i].strip()); i += 1
            if not buf: buf.append(lines[i].strip()); i += 1
            out.append("<p>%s</p>" % md_inline(" ".join(buf)))
    return out


def md_sections(text):
    """返回 (标题, 导语html, [(小节标题, 小节html)])。## 起分节，# 为页面标题。"""
    lines = text.split("\n")
    title = next((l[2:].strip() for l in lines if l.startswith("# ")), "")
    body = [l for l in lines if not l.startswith("# ")]
    intro, secs, cur = [], [], None
    for l in body:
        if l.startswith("## "):
            cur = [l[3:].strip(), []]; secs.append(cur)
        else:
            (cur[1] if cur else intro).append(l)
    return title, "".join(_blocks(intro)), [(h, "".join(_blocks(b))) for h, b in secs]


def _norm_text(s):
    return re.sub(r"[^\w\u4e00-\u9fff]", "", s)


def assert_covers(md_text, html_text):
    """md 的每一行文字都必须出现在转出的 HTML 里（去标签、去标点后比较），防止转换时丢内容。"""
    plain = html.unescape(re.sub(r"<[^>]+>", "", html_text))
    hn = _norm_text(plain)
    miss = []
    for ln in md_text.split("\n"):
        if ln.startswith("# "): continue                     # 页面标题由模板单独放置
        t = re.sub(r"\]\([^)]*\)", "]", ln)                  # 链接去掉 url
        t = re.sub(r"^(\s*[-*]\s+\[[ x]\]|\s*[-*]|\s*\d+\.|>|#+)\s*", "", t)
        t = t.replace("\\|", "|")
        if t.strip().startswith("---") or t.strip().startswith("```") or re.match(r"^\|[\s:\-|]+\|\s*$", t.strip()): continue
        if t.startswith("# "): continue
        n = _norm_text(t)
        if n and n not in hn: miss.append(ln)
    assert not miss, "转换丢失了内容：\n" + "\n".join(miss[:8])


def sections_html(secs, open_first=False, open_all=False):
    h = ""
    for k, (title, body) in enumerate(secs):
        op = " open" if (open_all or (open_first and k == 0)) else ""
        h += '<details class="sec"%s><summary>%s</summary>%s</details>\n' % (op, md_inline(title), body)
    return h


# ---------------- 页面 ----------------
PAGE = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="../css/base.css">
</head>
<body data-lesson="{lesson}" data-lesson-label="{label}">
<div class="wrap">
  <div class="topbar">
    <a href="../index.html">← 目录</a>
    <span class="badge">{badge} · 完整内容见 <a href="../../{md}">{md}</a></span>
    <button id="btn-present">投屏模式</button>
  </div>

  <h1>{h1}</h1>
  {intro}
{body}
  <div id="ask-box" class="card ask-box" style="display:none">
    <b>🙋 我的问题清单</b>（复制后发给老师）
    <textarea readonly></textarea>
    <div class="warn"></div>
    <button data-a="copy">复制</button> <button data-a="clear">清空</button>
  </div>
</div>

{scripts}
<script>
  var Q = function (id, d) {{ Quiz.mount(document.getElementById(id), d); }};
{quizjs}
  mountSteppers();
  mountCalcs();
  PageKit.init();
</script>
</body>
</html>
"""


INTRO = "先看动画，再做小测，最后一定要在 Dev-C++ 里自己敲一遍。黄色高亮是「这一步刚变的地方」。看不懂就点「🙋 我不懂这里」，页面底部会生成一行文字，发给老师就行。"


def render_blocks(blocks, counter=None):
    """blocks 元素：("h2", 文字) ("p", html) ("trace", id) ("picker", [ids], [labels]) ("quiz", dict)
      ("calc", 名字) ("html", 原始html) ("task", [li html, ...], "后记 html")
    返回 (html, [小测挂载js], 小测数)。counter 是小测编号计数器（整页共用，保证 id 不重复）。"""
    counter = counter if counter is not None else [0]
    body, quizzes = "", []
    for b in blocks:
        k = b[0]
        if k == "h2": body += "\n  <h2>%s</h2>\n" % b[1]
        elif k == "p": body += "  <p>%s</p>\n" % b[1]
        elif k == "html": body += b[1] + "\n"
        elif k == "trace": body += '  <div data-trace="%s"></div>\n' % b[1]
        elif k == "picker": body += '  <div data-traces="%s" data-labels="%s"></div>\n' % (",".join(b[1]), "|".join(b[2]))
        elif k == "calc": body += '  <div data-calc="%s"></div>\n' % b[1]
        elif k == "quiz":
            counter[0] += 1
            body += '  <div id="q%d"></div>\n' % counter[0]
            quizzes.append("  Q(\"q%d\", %s);" % (counter[0], json.dumps(b[1], ensure_ascii=False)))
        elif k == "task":
            body += ('\n  <div class="card">\n    <b>✍️ 回到 Dev-C++ 自己试一试</b>\n    <ol>\n%s\n    </ol>\n%s  </div>\n'
                     % ("\n".join("      <li>%s</li>" % x for x in b[1]),
                        ('    <p style="color:var(--muted);font-size:.85rem">%s</p>\n' % b[2]) if b[2] else ""))
        else: raise ValueError(k)
    return body, quizzes, len(quizzes)


def build_page(filename, lesson, label, title, h1, intro, md, blocks, tracefile=None, badge="精选演示，非整课"):
    """blocks 元素：
      ("h2", "文字") ("p", "html") ("trace", id) ("picker", [ids], [labels]) ("quiz", dict)
      ("calc", 名字) ("html", 原始html) ("task", [li html, ...], "后记 html")"""
    body, quizzes, n = render_blocks(blocks)
    scripts = ""
    for tf in ([tracefile] if isinstance(tracefile, str) else (tracefile or [])):
        scripts += '<script src="../data/traces/%s"></script>\n' % tf
    for s in ("page.js", "stepper.js", "quiz.js", "calc.js"):
        scripts += '<script src="../js/core/%s"></script>\n' % s
    out = PAGE.format(title=html.escape(title), lesson=lesson, label=html.escape(label), badge=badge, md=md,
                      h1=h1, intro=("<p>%s</p>" % intro) if intro else "", body=body, scripts=scripts.rstrip("\n"), quizjs="\n".join(quizzes))
    path = os.path.join(WEB, "lessons", filename)
    open(path, "w", encoding="utf-8").write(out)
    return path, n
