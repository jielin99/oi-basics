"""课件生成库（开发期使用，学生端不需要）。

两件事：
1. Trace：用 Python 按 C++ 语义逐步"推演"，每步记录执行该行【之后】的状态；
   finish() 时把 harness 真实编译运行，推演出的输出必须与真实输出一致，否则当场报错。
2. 页面/小测：predict_quiz 的正确答案由真实编译运行得出，不靠手写。
"""
import copy, hashlib, html, json, os, subprocess, tempfile

WEB = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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
  <p>{intro}</p>
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


def build_page(filename, lesson, label, title, h1, intro, md, blocks, tracefile=None, badge="精选演示，非整课"):
    """blocks 元素：
      ("h2", "文字") ("p", "html") ("trace", id) ("picker", [ids], [labels]) ("quiz", dict)
      ("calc", 名字) ("html", 原始html) ("task", [li html, ...], "后记 html")"""
    body, quizzes, n = "", [], 0
    for b in blocks:
        k = b[0]
        if k == "h2": body += "\n  <h2>%s</h2>\n" % b[1]
        elif k == "p": body += "  <p>%s</p>\n" % b[1]
        elif k == "html": body += b[1] + "\n"
        elif k == "trace": body += '  <div data-trace="%s"></div>\n' % b[1]
        elif k == "picker": body += '  <div data-traces="%s" data-labels="%s"></div>\n' % (",".join(b[1]), "|".join(b[2]))
        elif k == "calc": body += '  <div data-calc="%s"></div>\n' % b[1]
        elif k == "quiz":
            n += 1
            body += '  <div id="q%d"></div>\n' % n
            quizzes.append("  Q(\"q%d\", %s);" % (n, json.dumps(b[1], ensure_ascii=False)))
        elif k == "task":
            body += ('\n  <div class="card">\n    <b>✍️ 回到 Dev-C++ 自己试一试</b>\n    <ol>\n%s\n    </ol>\n    <p style="color:var(--muted);font-size:.85rem">%s</p>\n  </div>\n'
                     % ("\n".join("      <li>%s</li>" % x for x in b[1]), b[2]))
        else: raise ValueError(k)
    scripts = ""
    for tf in ([tracefile] if isinstance(tracefile, str) else (tracefile or [])):
        scripts += '<script src="../data/traces/%s"></script>\n' % tf
    for s in ("page.js", "stepper.js", "quiz.js", "calc.js"):
        scripts += '<script src="../js/core/%s"></script>\n' % s
    out = PAGE.format(title=html.escape(title), lesson=lesson, label=html.escape(label), badge=badge, md=md,
                      h1=h1, intro=intro, body=body, scripts=scripts.rstrip("\n"), quizjs="\n".join(quizzes))
    path = os.path.join(WEB, "lessons", filename)
    open(path, "w", encoding="utf-8").write(out)
    return path, n
