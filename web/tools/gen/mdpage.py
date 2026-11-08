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
def _ws(s):
    return re.sub(r"\s+", "", s)


def _md_inline_text(s):
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    out = []
    for part in re.split(r"(`[^`]+`)", s):          # 粗体记号只在代码之外去掉：`10**12` 里的 ** 是代码本身
        out.append(part[1:-1] if (len(part) > 1 and part.startswith("`") and part.endswith("`")) else part.replace("**", ""))
    return "".join(out)


def _md_line_text(l):
    t = l.strip()
    if not t or re.fullmatch(r"-{3,}", t): return ""
    if re.fullmatch(r"\|[\s:\-|]+\|", t): return ""
    t = re.sub(r"^(>\s?)+", "", t).strip()
    if t.startswith("|"):
        cells = re.split(r"(?<!\\)\|", t)
        t = "".join(c.strip().replace("\\|", "|") for c in cells)
    t = re.sub(r"^([-*]|\d+\.)\s+", "", t)
    t = re.sub(r"^\[[ xX]\]\s+", "", t)
    if t.startswith("<details") or t.startswith("</details"): return ""
    t = re.sub(r"</?summary>", "", t)
    return _ws(_md_inline_text(t))


def md_expect(text):
    heads, codes, texts, inf, buf = [], [], [], False, []
    for ln in text.split("\n"):
        if ln.startswith(">"): ln = re.sub(r"^>\s?", "", ln)      # 引用块里也可以有代码围栏
        if ln.startswith("```"):
            if inf: codes.append("\n".join(buf)); buf = []
            inf = not inf; continue
        if inf: buf.append(ln); continue
        m = re.match(r"^(#{1,6})\s+(.*)$", ln)
        if m: heads.append((len(m.group(1)), _ws(_md_inline_text(m.group(2))))); continue
        texts.append(_md_line_text(ln))
    return heads, codes, "".join(texts)


class _Collect(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth, self.heads, self.codes, self.text = 0, [], [], []
        self.pre = self.head = None; self.buf = []; self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag == "div":
            if self.depth: self.depth += 1
            elif "data-md" in dict(attrs): self.depth = 1
            return
        if not self.depth: return
        if tag == "pre": self.pre = True; self.buf = []
        elif re.fullmatch(r"h[1-6]", tag): self.head = int(tag[1]); self.buf = []
        elif tag in ("script", "style"): self.skip += 1

    def handle_endtag(self, tag):
        if tag == "div" and self.depth: self.depth -= 1; return
        if not self.depth: return
        if tag == "pre" and self.pre: self.codes.append("".join(self.buf)); self.pre = None
        elif re.fullmatch(r"h[1-6]", tag) and self.head: self.heads.append((self.head, _ws("".join(self.buf)))); self.head = None
        elif tag in ("script", "style"): self.skip -= 1

    def handle_data(self, d):
        if not self.depth or self.skip: return
        if self.pre or self.head: self.buf.append(d)
        else: self.text.append(d)


def verify_md(md_text, page_html, name=""):
    """md 正文必须在页面的 data-md 区域里完整、按序、逐字出现：标题(层级+文字)、代码块(逐字)、其余文字(规整后按序相等)。"""
    eh, ec, et = md_expect(md_text)
    c = _Collect(); c.feed(page_html)
    ht = _ws("".join(c.text))
    errs = []
    if eh != c.heads:
        i = next((k for k in range(min(len(eh), len(c.heads))) if eh[k] != c.heads[k]), min(len(eh), len(c.heads)))
        errs.append("标题不一致（md %d 个 / 页面 %d 个），第 %d 处：md=%r 页面=%r" % (len(eh), len(c.heads), i + 1, eh[i:i + 1], c.heads[i:i + 1]))
    if ec != c.codes:
        i = next((k for k in range(min(len(ec), len(c.codes))) if ec[k] != c.codes[k]), min(len(ec), len(c.codes)))
        errs.append("代码块不一致（md %d 个 / 页面 %d 个），第 %d 个：md=%r 页面=%r" % (len(ec), len(c.codes), i + 1, (ec[i:i + 1] or [""])[0][:80], (c.codes[i:i + 1] or [""])[0][:80]))
    if et != ht:
        i = next((k for k in range(min(len(et), len(ht))) if et[k] != ht[k]), min(len(et), len(ht)))
        errs.append("正文不一致（md %d 字 / 页面 %d 字），首个差异位置 %d：md「…%s」页面「…%s」" % (len(et), len(ht), i, et[max(0, i - 15):i + 25], ht[max(0, i - 15):i + 25]))
    if re.search(r'href="[^"]*\.md[#"]', page_html): errs.append("页面里残留指向 .md 的链接")
    assert not errs, "%s 内容校验失败：\n  " % name + "\n  ".join(errs)
