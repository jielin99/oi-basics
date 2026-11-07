#!/usr/bin/env python3
"""verify-traces：开发期校验轨迹数据（学生端不需要）。

做的事：
  1. 把 web/data/traces/*.js 用 node 载入成 JSON
  2. 结构检查：steps 非空、line 在 source 行数内、最后一步 out == expectOutput
  3. kind=normal：用 harness 真实编译(-std=c++11)运行，输出与 expectOutput 比对
     （统一换行，忽略行尾空白，超时 5s，退出码须为 0）
     kind=illustrative：只检查能编译
不做的事：不验证中间状态——那部分必须人工逐步核对。
"""
import json, os, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRACE_DIR = os.path.join(ROOT, "data", "traces")

LOADER = r"""
const fs = require('fs'), vm = require('vm'), path = require('path');
const dir = process.argv[1];
const ctx = { window: {} }; ctx.window.TRACES = {};
vm.createContext(ctx);
for (const f of fs.readdirSync(dir).filter(f => f.endsWith('.js')).sort())
  vm.runInContext(fs.readFileSync(path.join(dir, f), 'utf8'), ctx, { filename: f });
console.log(JSON.stringify(ctx.window.TRACES));
"""

def norm(s):
    return "\n".join(l.rstrip() for l in s.replace("\r\n", "\n").strip().split("\n"))

def check(tid, t):
    errs = []
    nlines = len(t["source"].rstrip("\n").split("\n"))
    if not t.get("steps"):
        return ["steps 为空"]
    for i, s in enumerate(t["steps"]):
        if not (1 <= s["line"] <= nlines):
            errs.append("step %d: line=%d 超出 1..%d" % (i + 1, s["line"], nlines))
    if t["kind"] == "normal" and norm(t["steps"][-1].get("out", "")) != norm(t["expectOutput"]):
        errs.append("最后一步 out=%r 与 expectOutput=%r 不一致" % (t["steps"][-1].get("out"), t["expectOutput"]))
    if "%SRC%" not in t["harness"]:
        errs.append("harness 缺少 %SRC%")
        return errs
    with tempfile.TemporaryDirectory() as d:
        cpp, exe = os.path.join(d, "a.cpp"), os.path.join(d, "a.out")
        with open(cpp, "w") as f:
            f.write(t["harness"].replace("%SRC%", t["source"]))
        c = subprocess.run(["g++", "-std=c++11", "-Wall", cpp, "-o", exe], capture_output=True, text=True)
        if c.returncode != 0:
            return errs + ["编译失败:\n" + c.stderr]
        if t["kind"] == "illustrative":
            return errs
        try:
            r = subprocess.run([exe], input=t.get("input", ""), capture_output=True, text=True, timeout=5)
        except subprocess.TimeoutExpired:
            return errs + ["运行超时(5s)"]
        if r.returncode != 0:
            errs.append("退出码 %d" % r.returncode)
        if norm(r.stdout) != norm(t["expectOutput"]):
            errs.append("真实输出 %r 与 expectOutput %r 不一致" % (r.stdout, t["expectOutput"]))
    return errs

def main():
    out = subprocess.run(["node", "-e", LOADER, TRACE_DIR], capture_output=True, text=True)
    if out.returncode != 0:
        print(out.stderr); return 2
    traces = json.loads(out.stdout)
    bad = 0
    for tid, t in traces.items():
        errs = check(tid, t)
        print(("FAIL " if errs else "PASS ") + tid + "  (%d 步, kind=%s)" % (len(t["steps"]), t["kind"]))
        for e in errs:
            print("   - " + e)
        bad += bool(errs)
    print("共 %d 个，失败 %d 个" % (len(traces), bad))
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main())
