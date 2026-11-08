#!/usr/bin/env python3
"""重新生成所有课件页与轨迹数据：python3 web/tools/gen/build_all.py（开发期，需 g++）"""
import glob, os, subprocess, sys
d = os.path.dirname(os.path.abspath(__file__))
bad = 0
for f in sorted(glob.glob(os.path.join(d, "g[0-9]*.py"))):
    r = subprocess.run([sys.executable, f], capture_output=True, text=True)
    print(("OK   " if r.returncode == 0 else "FAIL ") + os.path.basename(f), r.stdout.strip().split("\n")[-1] if r.stdout.strip() else "")
    if r.returncode: bad += 1; print(r.stderr[-1500:])
sys.exit(1 if bad else 0)
