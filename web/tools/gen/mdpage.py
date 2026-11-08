"""整课页面构建：md 正文全文 + 嵌在所属小节里的互动块（动画/小测/小工具）。

正文以 md 为唯一来源；互动块由各课脚本的 inserts 指定位置：
  inserts = {"intro": [...], "2.4": [...], "3.": [...], "第二部分/3.": [...]}
key 规则（缺失或重复即构建失败，不做模糊匹配）：
  intro            第一个 ## 之前的导语
  "N."             二级标题（## N. …），插在整节（含全部三级小节）之后
  "N.M"            三级标题（### N.M …），要求全页唯一，插在该小节正文之后
  "父/子"           父为二级标题的第一个词（第一部分、4. …），子为三级标题的第一个词（1.），用于编号重复的页面
"""
import html as H
import os, re
from html.parser import HTMLParser
from lib import *
from lib import _blocks, _fix_href


# ---------------- 围栏感知的切分 ----------------
class Sec:
    def __init__(self, level, title):
        self.level, self.title, self.lines, self.kids = level, title, [], []
        self.tok = re.split(r"[：:\s]", title.strip(), 1)[0]


def split_sections(text):
    """只在代码围栏之外识别标题（围栏里的 `# Python` 是代码注释，不是标题）。"""
    h1, intro, secs, cur, cur3, inf = None, [], [], None, None, False
    for ln in text.split("\n"):
        if ln.startswith("````") or ln.startswith("~~~"): raise ValueError("不支持的代码围栏（只支持 3 个反引号）：%r" % ln)
        if ln.startswith("```"): inf = not inf
        if not inf and not ln.startswith("```"):
            m = re.match(r"^(#{1,6})\s+(.*)$", ln)
            if m:
                lv, title = len(m.group(1)), m.group(2).strip()
                if lv == 1:
                    assert h1 is None, "出现第二个一级标题"; h1 = title
                elif lv == 2:
                    cur = Sec(2, title); secs.append(cur); cur3 = None
                elif lv == 3:
                    assert cur is not None, "### 出现在任何 ## 之前：" + title
                    cur3 = Sec(3, title); cur.kids.append(cur3)
                else:
                    raise ValueError("本页转换器不支持 %d 级标题：%s" % (lv, title))
                continue
        (cur3 or cur).lines.append(ln) if (cur3 or cur) else intro.append(ln)
    assert h1, "缺少一级标题"
    return h1, intro, secs


def resolve(key, secs):
    """返回要在其后插入的 Sec 对象（二级则表示整节），或 'intro'。"""
    if key == "intro": return "intro"
    if "/" in key:
        p, c = [x.strip() for x in key.split("/", 1)]
        hits = [k for s in secs if s.tok == p for k in s.kids if k.tok == c]
    elif re.fullmatch(r"\d+\.\d+", key):
        hits = [k for s in secs for k in s.kids if k.tok == key]
    else:
        hits = [s for s in secs if s.tok == key]
    assert len(hits) == 1, "插入点 %r 在 md 里匹配到 %d 处（必须恰好 1 处）" % (key, len(hits))
    return hits[0]


# ---------------- 渲染 ----------------
def _plain(s):
    return re.sub(r"<[^>]+>", "", md_inline(s))


def build_lesson(md_name, filename, label, lesson_key, inserts, tracefiles, tasks=None):
    """生成课页；返回 (路径, 小测数)。tasks=("li…", "后记")：放在“课堂练习”之后。"""
    md_path = os.path.join(WEB, "..", md_name)
    text = open(md_path, encoding="utf-8").read()
    h1, intro, secs = split_sections(text)
    # 解析全部插入点（先解析，失败得早）
    targets = {}
    for key, blocks in inserts.items():
        t = resolve(key, secs)
        assert id(t) not in targets, "两个 key 指向同一小节：%s" % key
        targets[id(t) if t != "intro" else "intro"] = (key, blocks)
    counter, quizjs, ids, toc = [0], [], [0], []

    def lab(key_obj):
        item = targets.get(key_obj if key_obj == "intro" else id(key_obj))
        if not item: return ""
        body, qj, _ = render_blocks(item[1], counter)
        quizjs.extend(qj)
        return '<div class="lab"><div class="lab-t">🎮 动手看看</div>%s</div>\n' % body

    def heading(sec):
        ids[0] += 1; hid = "sec-%d" % ids[0]
        toc.append((sec.level, hid, _plain(sec.title)))
        return '<h%d id="%s">%s</h%d>' % (sec.level, hid, md_inline(sec.title), sec.level)

    out = ['<div data-md><h1>%s</h1></div>' % md_inline(h1),
           '<div data-md>%s</div>' % "".join(_blocks(intro)), lab("intro")]
    for s in secs:
        out.append('<div data-md>%s%s</div>' % (heading(s), "".join(_blocks(s.lines))))
        for k in s.kids:
            out.append('<div data-md>%s%s</div>' % (heading(k), "".join(_blocks(k.lines))))
            out.append(lab(k))
        out.append(lab(s))
        if tasks and s.tok == "4.":                    # 课堂练习（含参考答案折叠块）之后
            b, _, _ = render_blocks([("task", tasks[0], tasks[1])]); out.append(b)
    body = "\n".join(x for x in out if x)

    # 目录
    toc_html = '<details class="toc"><summary>目录</summary><ol>'
    for lv, hid, t in toc:
        toc_html += '<li class="l%d"><a href="#%s">%s</a></li>' % (lv, hid, H.escape(t))
    toc_html += "</ol></details>"
    # 上下课
    order = [x[2] for x in LESSONS]; i = order.index(filename)
    prev_ = '<a href="%s">← %s %s</a>' % (LESSONS[i - 1][2], LESSONS[i - 1][0], LESSONS[i - 1][1]) if i > 0 else "<span></span>"
    next_ = '<a href="%s">%s %s →</a>' % (LESSONS[i + 1][2], LESSONS[i + 1][0], LESSONS[i + 1][1]) if i + 1 < len(LESSONS) else "<span></span>"

    scripts = ""
    for tf in tracefiles: scripts += '<script src="../data/traces/%s"></script>\n' % tf
    for sname in ("page.js", "stepper.js", "quiz.js", "calc.js"): scripts += '<script src="../js/core/%s"></script>\n' % sname
    page = LESSON_TPL.format(title=H.escape(_plain(h1)), lesson=lesson_key, label=H.escape(label), toc=toc_html, body=body,
                             prev=prev_, next=next_, scripts=scripts.rstrip("\n"), quizjs="\n".join(quizjs))
    verify_md(text, page, md_name)                      # 内容完整性：不通过就不落盘
    path = os.path.join(WEB, "lessons", filename)
    open(path, "w", encoding="utf-8").write(page)
    return path, counter[0]


LESSON_TPL = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="../css/base.css">
</head>
<body data-lesson="{lesson}" data-lesson-label="{label}">
<div class="wrap lesson">
  <div class="topbar"><a href="../index.html">← 目录</a><button id="btn-present">投屏模式</button></div>
  <div class="layout">
    <nav class="toc-box">{toc}</nav>
    <main>
{body}
      <div id="ask-box" class="card ask-box" style="display:none">
        <b>🙋 我的问题清单</b>（复制后发给老师）
        <textarea readonly></textarea>
        <div class="warn"></div>
        <button data-a="copy">复制</button> <button data-a="clear">清空</button>
      </div>
      <nav class="lnav">{prev}{next}</nav>
    </main>
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


# ---------------- 独立的内容校验（不依赖渲染器的实现） ----------------
# 把 md 和页面都化成同一种"有序序列"，逐项相等才算通过：
#   ("h", 层级, 文字) ("c", 代码块原文) ("tbl", [[单元格文字…]…]) ("sum", 文字) ("details",) ("/details",) ("t", 一段正文)
# 行内代码另外按出现顺序逐字比较（空白也不能动）。标题/代码块/表格/折叠块/正文的先后顺序因此也被检查。
def _ws(s):
    return re.sub(r"\s+", "", s)


def _md_inline_text(s):
    """md 行内文字 → 页面上应显示的文字：代码里的内容原样保留，链接只留文字，粗体记号去掉。"""
    codes = []
    s = re.sub(r"`[^`]+`", lambda m: (codes.append(m.group(0)[1:-1]) or "\x01%d\x01" % (len(codes) - 1)), s)   # 先保护代码
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    s = s.replace("**", "")
    return re.sub(r"\x01(\d+)\x01", lambda m: codes[int(m.group(1))], s)


def _md_line_text(l):
    t = l.strip()
    if not t or re.fullmatch(r"-{3,}", t): return ""
    t = re.sub(r"^(>\s?)+", "", t).strip()
    t = re.sub(r"^([-*]|\d+\.)\s+", "", t)
    t = re.sub(r"^\[[ xX]\]\s+", "", t)
    return _ws(_md_inline_text(t))


def _code_spans(line):
    return re.findall(r"`([^`]+)`", line)


class _Seq:
    """顺序序列构造器：相邻正文合并成一段，遇到结构元素先把正文收尾。"""
    def __init__(self): self.items, self.buf = [], []
    def text(self, t):
        if t: self.buf.append(t)
    def flush(self):
        t = "".join(self.buf); self.buf = []
        if t: self.items.append(("t", t))
    def add(self, item): self.flush(); self.items.append(item)


def md_expect(text):
    seq, spans, inf, buf = _Seq(), [], False, []
    lines = text.split("\n"); k = 0
    while k < len(lines):
        ln = re.sub(r"^(>\s?)+", "", lines[k]); raw = lines[k]; k += 1          # 引用（含嵌套）里也可以有代码围栏
        if ln.startswith("```"):
            if inf: seq.add(("c", "\n".join(buf))); buf = []
            inf = not inf; continue
        if inf: buf.append(ln); continue
        m = re.match(r"^(#{1,6})\s+(.*)$", ln)
        if m:
            seq.add(("h", len(m.group(1)), _ws(_md_inline_text(m.group(2))))); spans += _code_spans(m.group(2)); continue
        if ln.strip() == "<details>": seq.add(("details",)); continue
        if ln.strip() == "</details>": seq.add(("/details",)); continue
        ms = re.fullmatch(r"<summary>(.*)</summary>", ln.strip())
        if ms: seq.add(("sum", _ws(_md_inline_text(ms.group(1))))); spans += _code_spans(ms.group(1)); continue
        if raw.startswith("|") and k < len(lines) and re.fullmatch(r"\|[\s:\-|]+\|\s*", lines[k]):
            rows = []; j = k - 1
            while j < len(lines) and lines[j].startswith("|"):
                if not re.fullmatch(r"\|[\s:\-|]+\|\s*", lines[j]):
                    cells = re.split(r"(?<!\\)\|", lines[j].strip())
                    cells = cells[1:] if cells and cells[0].strip() == "" else cells
                    cells = cells[:-1] if cells and cells[-1].strip() == "" else cells
                    cells = [c.strip().replace("\\|", "|") for c in cells]
                    rows.append([_ws(_md_inline_text(c)) for c in cells])
                    for c in cells: spans += _code_spans(c)
                j += 1
            seq.add(("tbl", rows)); k = j; continue
        seq.text(_md_line_text(ln)); spans += _code_spans(ln)
    seq.flush()
    return seq.items, spans


class _Collect(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth, self.seq, self.spans = 0, _Seq(), []
        self.pre = self.head = self.summ = self.cell = None
        self.buf = []; self.skip = 0; self.rows = None; self.row = None; self.incode = 0

    def handle_starttag(self, tag, attrs):
        if tag == "div":
            if self.depth: self.depth += 1
            elif "data-md" in dict(attrs): self.depth = 1
            return
        if not self.depth: return
        if tag == "pre": self.pre = True; self.buf = []
        elif re.fullmatch(r"h[1-6]", tag): self.head = int(tag[1]); self.buf = []
        elif tag == "summary": self.summ = True; self.buf = []
        elif tag == "details": self.seq.add(("details",))
        elif tag == "table": self.seq.flush(); self.rows = []
        elif tag == "tr" and self.rows is not None: self.row = []
        elif tag in ("td", "th") and self.row is not None: self.cell = []
        elif tag == "code" and not self.pre: self.incode += 1; self.cbuf = []
        elif tag in ("script", "style"): self.skip += 1

    def handle_endtag(self, tag):
        if tag == "div" and self.depth: self.depth -= 1; return
        if not self.depth: return
        if tag == "pre" and self.pre: self.seq.add(("c", "".join(self.buf))); self.pre = None
        elif re.fullmatch(r"h[1-6]", tag) and self.head: self.seq.add(("h", self.head, _ws("".join(self.buf)))); self.head = None
        elif tag == "summary" and self.summ: self.seq.add(("sum", _ws("".join(self.buf)))); self.summ = None
        elif tag == "details": self.seq.add(("/details",))
        elif tag in ("td", "th") and self.cell is not None: self.row.append(_ws("".join(self.cell))); self.cell = None
        elif tag == "tr" and self.row is not None: self.rows.append(self.row); self.row = None
        elif tag == "table" and self.rows is not None: self.seq.add(("tbl", self.rows)); self.rows = None
        elif tag == "code" and self.incode: self.incode -= 1; self.spans.append("".join(self.cbuf))
        elif tag in ("script", "style"): self.skip -= 1

    def handle_data(self, d):
        if not self.depth or self.skip: return
        if self.incode: self.cbuf.append(d)
        if self.pre or self.head or self.summ: self.buf.append(d)
        elif self.cell is not None: self.cell.append(d)
        elif self.rows is None: self.seq.text(_ws(d))


def verify_md(md_text, page_html, name=""):
    """md 正文必须在页面的 data-md 区域里完整、按序、逐字出现。比较统一的有序序列
    （标题层级+文字、代码块逐字、表格行列与单元格、折叠块与 summary、正文），外加行内代码逐字比较。"""
    ex, ex_spans = md_expect(md_text)
    c = _Collect(); c.feed(page_html); c.seq.flush()
    got, got_spans = c.seq.items, c.spans
    errs = []
    if ex != got:
        i = next((k for k in range(min(len(ex), len(got))) if ex[k] != got[k]), min(len(ex), len(got)))
        show = lambda x: repr(x)[:160]
        errs.append("内容/顺序不一致（md %d 项 / 页面 %d 项），第 %d 项：\n    md  ：%s\n    页面：%s" % (len(ex), len(got), i + 1, show(ex[i:i + 1]), show(got[i:i + 1])))
    if ex_spans != got_spans:
        i = next((k for k in range(min(len(ex_spans), len(got_spans))) if ex_spans[k] != got_spans[k]), min(len(ex_spans), len(got_spans)))
        errs.append("行内代码不一致（md %d 处 / 页面 %d 处），第 %d 处：md=%r 页面=%r" % (len(ex_spans), len(got_spans), i + 1, ex_spans[i:i + 1], got_spans[i:i + 1]))
    if re.search(r'href="[^"]*\.md[#"]', page_html): errs.append("页面里残留指向 .md 的链接")
    assert not errs, "%s 内容校验失败：\n  " % name + "\n  ".join(errs)
