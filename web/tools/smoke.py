#!/usr/bin/env python3
"""冒烟测试：用无头 Chromium 打开 lessons/*.html（file://），对每页检查：
  - 无脚本错误；所有演示数据都找得到
  - 每个演示走完全部步骤；每步代码行高亮（line=0 除外）；逐步后退与前进时的画面一致
  - 每道小测：点错误项出"再想想"、点正确项出"答对了"，答案下标合法
  - 计算器能挂载且有输出
  - 手机宽度(390)下页面本身不横向滚动（代码区内部滚动允许）
用法：python3 web/tools/smoke.py [页面名子串...]    环境变量 CHROME 可指定浏览器路径"""
import glob, os, re, subprocess, sys, tempfile

WEB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME = os.environ.get("CHROME") or glob.glob(os.path.expanduser("~/.cache/ms-playwright/chromium-*/chrome-linux64/chrome"))[0]

TEST = r"""
(function () {
  var R = [], errs = [];
  function ok(n, c, x) { R.push((c ? "PASS " : "FAIL ") + n + (c ? "" : "  <= " + x)); }
  window.addEventListener("error", function (e) { errs.push(e.message); });
  function snap(el) {
    var q = function (s) { var n = el.querySelector(s); return n ? n.innerHTML : ""; };
    var on = el.querySelector(".stp-line.on");
    return [on ? on.getAttribute("data-ln") : "-", q(".stp-vars"), q(".stp-arrs"), q(".stp-tape-box"), q(".stp-stack-box"), q(".stp-out"), q(".stp-note")].join("§");
  }
  function walk(el, label) {
    var st = el._stepper, t = st.trace, n = t.steps.length, fwd = [snap(el)], i, good = true, bad = "";
    for (i = 0; i < n; i++) {
      el.querySelector("[data-a=next]").click();
      fwd.push(snap(el));
      var on = el.querySelectorAll(".stp-line.on").length, want = t.steps[i].line === 0 ? 0 : 1;
      if (on !== want) { good = false; bad = "step " + (i + 1) + " 高亮行数 " + on; }
    }
    ok(label + " 走完 " + n + " 步且每步高亮正确", good && el.querySelector(".cnt").textContent === n + " / " + n, bad);
    var back = true;
    for (i = n - 1; i >= 0; i--) { el.querySelector("[data-a=prev]").click(); if (snap(el) !== fwd[i]) { back = false; bad = "后退到 " + i; } }
    ok(label + " 后退画面与前进一致", back, bad);
    el.querySelector("[data-a=reset]").click();
  }
  document.querySelectorAll("[data-trace],[data-traces]").forEach(function (el) {
    if (el.hasAttribute("data-traces")) {
      var bs = el.querySelectorAll(".pick button");
      for (var k = 0; k < bs.length; k++) { bs[k].click(); walk(el, el._stepper.id); }
    } else {
      ok("演示数据存在 " + el.getAttribute("data-trace"), !!el._stepper, el.textContent);
      if (el._stepper) walk(el, el._stepper.id);
    }
  });
  document.querySelectorAll(".card").forEach(function (c) {
    if (!c._quiz) return;
    var d = c._quiz, bs = c.querySelectorAll(".quiz-opts button"), fb = c.querySelector(".quiz-fb");
    var q = d.q.slice(0, 18);
    ok("小测答案下标合法 「" + q + "」", d.answer >= 0 && d.answer < bs.length && bs.length >= 2, d.answer);
    var w = d.answer === 0 ? 1 : 0; bs[w].click();
    var a = fb.classList.contains("no") && bs[w].classList.contains("wrong");
    bs[d.answer].click();
    ok("小测对错反馈 「" + q + "」", a && fb.classList.contains("ok") && bs[d.answer].classList.contains("right"), fb.className);
  });
  document.querySelectorAll("[data-calc]").forEach(function (c) {
    var o = c.querySelector(".calc-out"); ok("计算器有输出 " + c.getAttribute("data-calc"), !!o && o.textContent.length > 5, "empty");
  });
  ok("页面本身不横向滚动 (scrollWidth " + document.documentElement.scrollWidth + " / innerWidth " + window.innerWidth + ")", document.documentElement.scrollWidth <= window.innerWidth + 1, "overflow");
  ok("无脚本错误", errs.length === 0, errs.join(" ; "));
  var pre = document.createElement("pre"); pre.id = "smoke"; pre.textContent = R.join("\n"); document.body.appendChild(pre);
})();
"""

def run(page, width):
    html = open(page, encoding="utf-8").read()
    html = html.replace('"../', '"file://%s/' % WEB)
    html = html.replace("<head>", "<head>", 1).replace("</body>", "<script>" + TEST + "</script></body>")
    with tempfile.TemporaryDirectory() as d:
        f = os.path.join(d, "t.html"); open(f, "w", encoding="utf-8").write(html)
        out = subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--allow-file-access-from-files",
                              "--window-size=%d,1000" % width, "--virtual-time-budget=8000", "--dump-dom", "file://" + f],
                             capture_output=True, text=True, timeout=90).stdout
    m = re.search(r'<pre id="smoke">(.*?)</pre>', out, re.S)
    if not m: return ["FAIL 页面没有产出测试结果（脚本可能整体出错）"]
    import html as H
    return H.unescape(m.group(1)).split("\n")

def main():
    pats = sys.argv[1:]
    pages = sorted(glob.glob(os.path.join(WEB, "lessons", "*.html")))
    pages = [p for p in pages if not pats or any(s in os.path.basename(p) for s in pats)]
    total = fail = 0
    for p in pages:
        for w in (1280, 390):
            res = run(p, w)
            f = [l for l in res if l.startswith("FAIL")]
            total += len(res); fail += len(f)
            print("%s %-22s 宽%-4d %3d 项 失败 %d" % ("FAIL" if f else "PASS", os.path.basename(p), w, len(res), len(f)))
            for l in f: print("     " + l)
    print("合计 %d 项，失败 %d" % (total, fail))
    return 1 if fail else 0

if __name__ == "__main__":
    sys.exit(main())
