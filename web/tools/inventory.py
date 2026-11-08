#!/usr/bin/env python3
"""互动内容清单：每页有哪些动画(trace/picker)、小测(题干)、计算器。
  python3 tools/inventory.py --save   把当前所有页面的清单存成基线 tools/inventory-baseline.json
  python3 tools/inventory.py --check  对比当前页面与基线：缺了任何一项就失败（防止迁移时整块漏掉）"""
import glob, json, os, re, sys
WEB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(WEB, "tools", "inventory-baseline.json")

def inv(h):
    qs = []
    for m in re.finditer(r'Q\("([^"]+)",\s*\{', h):
        rest = h[m.end():]
        q = re.search(r'"?q"?\s*:\s*"((?:[^"\\]|\\.)*)"', rest)
        qs.append(json.loads('"%s"' % q.group(1)) if q else "?")
    pk = [x.split(",") for x in re.findall(r'data-traces="([^"]*)"', h)]
    return dict(traces=sorted(re.findall(r'data-trace="([^"]+)"', h)),
                pickers=sorted(pk), quizzes=sorted(qs), calcs=sorted(re.findall(r'data-calc="([^"]+)"', h)))

def collect():
    return {os.path.basename(p): inv(open(p, encoding="utf-8").read()) for p in sorted(glob.glob(os.path.join(WEB, "lessons", "*.html")))}

def main():
    cur = collect()
    if "--save" in sys.argv:
        json.dump(cur, open(BASE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("已保存基线：%d 页，动画 %d、切换组 %d、小测 %d、计算器 %d" % (len(cur), sum(len(v["traces"]) for v in cur.values()),
              sum(len(v["pickers"]) for v in cur.values()), sum(len(v["quizzes"]) for v in cur.values()), sum(len(v["calcs"]) for v in cur.values())))
        return 0
    base = json.load(open(BASE, encoding="utf-8")); bad = 0
    for page, b in base.items():
        c = cur.get(page)
        if c is None: print("FAIL 缺页面", page); bad += 1; continue
        for k in ("traces", "pickers", "quizzes", "calcs"):
            miss = [x for x in b[k] if x not in c[k]]
            extra = [x for x in c[k] if x not in b[k]]
            if miss: print("FAIL %s 缺少 %s：%s" % (page, k, miss)); bad += 1
            if extra and "--strict" in sys.argv: print("WARN %s 多出 %s：%s" % (page, k, extra))
    print("基线对比：%d 页，失败 %d" % (len(base), bad))
    return 1 if bad else 0
sys.exit(main())
