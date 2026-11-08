#!/usr/bin/env python3
"""内容校验器自测：
  1) 全部 16 个 md 经渲染器转出后，必须通过校验器（转换器无损）
  2) 对页面做 8 种破坏（删段、重复段、<改>、删围栏内 # Python、改标题、删列表项、代码块换位、正文只留在 script 里），校验器必须每次报错"""
import glob, os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "gen"))
import mdpage
from mdpage import split_sections, verify_md, md_inline

def render(text):
    h1, intro, secs = split_sections(text)
    b = '<div data-md><h1>%s</h1></div><div data-md>%s</div>' % (md_inline(h1), "".join(mdpage._blocks(intro)))
    for s in secs:
        b += '<div data-md><h2>%s</h2>%s</div>' % (md_inline(s.title), "".join(mdpage._blocks(s.lines)))
        for k in s.kids: b += '<div data-md><h3>%s</h3>%s</div>' % (md_inline(k.title), "".join(mdpage._blocks(k.lines)))
    return b

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
files = sorted(glob.glob(os.path.join(root, "[0-9]*.md")) + glob.glob(os.path.join(root, "附录*.md")))
bad = 0
for f in files:
    t = open(f, encoding="utf-8").read()
    try: verify_md(t, render(t), os.path.basename(f))
    except AssertionError as e: bad += 1; print("FAIL 无损转换", os.path.basename(f), str(e)[:300])
print("无损转换：%d 个 md，失败 %d" % (len(files), bad))

text = open(os.path.join(root, "06-循环结构.md"), encoding="utf-8").read(); body = render(text)
miss = 0
muts = {
 "删一段落": lambda b: re.sub(r"<p>.*?</p>", "", b, count=1, flags=re.S),
 "重复一段落": lambda b: (lambda m: b[:m.end()] + m.group(0) + b[m.end():])(re.search(r"<p>.*?</p>", b, re.S)),
 "符号 < 改成 >": lambda b: (lambda i: b[:i] + "&gt;" + b[i + 4:])(b.index("&lt;")),
 "删围栏内 # Python": lambda b: b.replace("# Python\n", "", 1),
 "改标题文字": lambda b: re.sub(r"(<h2[^>]*>)", r"\1X", b, count=1),
 "删一个列表项": lambda b: re.sub(r"<li>.*?(?=<li>|</ul>|</ol>)", "", b, count=1, flags=re.S),
 "两个代码块换位": lambda b: (lambda p: b.replace(p[0], "@@", 1).replace(p[1], p[0], 1).replace("@@", p[1], 1))(re.findall(r"<pre.*?</pre>", b, re.S)),
 "正文只留在 script 里": lambda b: (lambda m: b.replace(m.group(0), "", 1) + "<script>" + m.group(1) + "</script>")(re.search(r"<p>(.*?)</p>", b, re.S)),
}
# ---- 针对外审指出的盲区：用小型合成 md，逐项构造"文字拼接相同但语义变了"的页面 ----
def must_fail(name, md, page_fn):
    global miss
    body = render(md)
    try: verify_md(md, page_fn(body), "变异")
    except AssertionError: return
    miss += 1; print("FAIL 没被发现：", name)

def must_raise(name, md):
    global miss
    try: render(md)
    except (ValueError, AssertionError): return
    miss += 1; print("FAIL 没有明确失败：", name)

SYN = """# 标题

> 导语

## 1. 节一

说明 `long long` 与 `x + +y`。

```cpp
int a;
```

| 列一 | 列二 |
|---|---|
| ab | c |

<details>
<summary>展开答案</summary>

答案 `[x](https://e.com)` 正文

</details>

### 1.1 小节

小节说明。
"""
verify_md(SYN, render(SYN), "合成基线")          # 合成 md 本身必须能通过
must_fail("行内代码里的空格被删", SYN, lambda b: b.replace("<code>long long</code>", "<code>longlong</code>"))
must_fail("行内代码 x + +y 变 x++y", SYN, lambda b: b.replace("<code>x + +y</code>", "<code>x++y</code>"))
must_fail("标题/代码/正文顺序被交换", SYN, lambda b: b.replace('<h3', '<pre class="quiz-code"><code>int a;</code></pre><h3', 1).replace('<pre class="quiz-code"><code>int a;</code></pre><table', '<table', 1) if False else
          re.sub(r"(<pre.*?</pre>)(.*?)(<h3)", lambda m: m.group(2) + m.group(1) + m.group(3), b, count=1, flags=re.S))
must_fail("表格列边界移动", SYN, lambda b: b.replace("<td>ab</td><td>c</td>", "<td>a</td><td>bc</td>"))
must_fail("summary 变成普通段落", SYN, lambda b: b.replace("<summary>展开答案</summary>", "<p>展开答案</p>"))
must_fail("details 外壳被去掉", SYN, lambda b: b.replace('<details class="ans">', "").replace("</details>", ""))
must_fail("行内代码里的链接字面量被改成链接", SYN, lambda b: b.replace("<code>[x](https://e.com)</code>", '<code><a href="https://e.com">x</a></code>'))
must_raise("同一行的 <details><summary>…", "# T\n\n## 1. 节\n\n<details><summary>重要</summary>\n\n正文\n\n</details>\n")
must_raise("整行 <details>…</details>", "# T\n\n## 1. 节\n\n<details><summary>a</summary>正文</details>\n")
must_raise("四个反引号围栏", "# T\n\n## 1. 节\n\n````\n```\n## 9. 伪标题\n```\n````\n")
must_raise("~~~ 围栏", "# T\n\n## 1. 节\n\n~~~\ncode\n~~~\n")

for name, fn in muts.items():
    try: verify_md(text, fn(body), "变异"); miss += 1; print("FAIL 没被发现：", name)
    except AssertionError: pass
print("破坏测试：%d 种，漏报 %d" % (len(muts) + 11, miss))
sys.exit(1 if (bad or miss) else 0)
