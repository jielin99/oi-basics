#!/usr/bin/env python3
"""calc.js 的纯计算函数与真实 C++ / Python 逐项对照（开发期）。"""
import json, os, subprocess, sys, tempfile
WEB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DIVS = [(-7,2),(7,-2),(-7,-2),(7,2),(17,5),(-17,5),(0,3),(1000000000,-3),(-1000000000,7),(5,7),(-5,7),(1,1)]
FMTS = [("%d","42"),("%d","-7"),("%5d","42"),("%-5d","42"),("%05d","42"),("%05d","-42"),("%.2f","3.14159"),("%.2f","2.675"),
        ("%.2f","0.125"),("%.2f","0.135"),("%.0f","0.5"),("%.0f","1.5"),("%.0f","2.5"),("%.0f","3.5"),("%8.3f","3.14159"),("%5.1f","-0.04"),
        ("%.1f","0.05"),("%.1f","0.25"),("%.1f","0.35"),("%.2f","123456.789"),("%8.3f","-2.0005"),("%.2f","0"),("%.2f","99.995"),("%.2f","9.995"),("%5.1f","99.96")]
BITS = [(12,10,2),(0,255,0),(255,255,20),(5,3,1),(170,85,4),(1,2,7),(200,100,3)]
CHARS = list("09aAzZ5#") + ["m","Q"]

js = r"""
global.window={}; new Function('window',require('fs').readFileSync(process.argv[1],'utf8'))(global.window);
const C=window.CalcCore, d=JSON.parse(process.argv[2]), o={div:[],fmt:[],bits:[],chr:[]};
for(const [a,b] of d.divs){const c=C.cppDivMod(BigInt(a),BigInt(b)),p=C.pyDivMod(BigInt(a),BigInt(b));o.div.push([String(c.q),String(c.r),String(p.q),String(p.r)])}
for(const [f,v] of d.fmts){const r=C.format(f,v);o.fmt.push(r.err?('ERR'):r.text)}
for(const [a,b,k] of d.bits){const r=C.bits(a,b,k);o.bits.push([r.and,r.or,r.xor,r.not,r.shl,r.shr])}
for(const ch of d.chars){const r=C.charInfo(ch);o.chr.push([r.code,r.digit===undefined?null:r.digit,r.upper||null,r.lower||null])}
console.log(JSON.stringify(o));
"""
out = subprocess.run(["node","-e",js,os.path.join(WEB,"js/core/calc.js"),json.dumps(dict(divs=DIVS,fmts=FMTS,bits=BITS,chars=CHARS))],capture_output=True,text=True)
if out.returncode: print(out.stderr); sys.exit(2)
J = json.loads(out.stdout)

cpp = '#include <cstdio>\nint main(){\n'
for a,b in DIVS: cpp += '  printf("%%d %%d\\n", (%d)/(%d), (%d)%%(%d));\n' % (a,b,a,b)
for f,v in FMTS:
    lit = v if (f.endswith("d") or "." in v) else v + ".0"      # %f 必须配 double，不能传整数字面量
    cpp += '  printf("%s\\n", %s);\n' % ('|' + f + '|', lit)
for a,b,k in BITS: cpp += '  printf("%%d %%d %%d %%d %%d %%d\\n", %d&%d, %d|%d, %d^%d, ~%d, %d<<%d, %d>>%d);\n' % (a,b,a,b,a,b,a,a,k,a,k)
cpp += '  return 0;\n}\n'
with tempfile.TemporaryDirectory() as d:
    open(d+"/a.cpp","w").write(cpp)
    c = subprocess.run(["g++","-std=c++11",d+"/a.cpp","-o",d+"/a"],capture_output=True,text=True)
    if c.returncode: print(c.stderr); sys.exit(2)
    lines = subprocess.run([d+"/a"],capture_output=True,text=True).stdout.split("\n")
bad = 0; i = 0
for (a,b),(cq,cr,pq,pr) in zip(DIVS,J["div"]):
    rq,rr = lines[i].split(); i+=1
    py = (a//b, a%b)
    ok = (cq,cr)==(rq,rr) and (pq,pr)==(str(py[0]),str(py[1]))
    if not ok: bad+=1; print("FAIL div",a,b,"js",cq,cr,pq,pr,"c++",rq,rr,"py",py)
for (f,v),got in zip(FMTS,J["fmt"]):
    exp = lines[i]; i+=1; exp = exp[1:-1]
    if exp != got: bad+=1; print("FAIL fmt",f,v,"js=%r"%got,"c=%r"%exp)
for (a,b,k),got in zip(BITS,J["bits"]):
    exp = list(map(int,lines[i].split())); i+=1
    if exp != got: bad+=1; print("FAIL bits",a,b,k,got,exp)
for ch,(code,dg,up,lo) in zip(CHARS,J["chr"]):
    ok = code==ord(ch) and (dg==(ord(ch)-48 if ch.isdigit() else None)) and (up==(ch.upper() if ch.islower() else None)) and (lo==(ch.lower() if ch.isupper() else None))
    if not ok: bad+=1; print("FAIL chr",ch,code,dg,up,lo)
print("div %d + fmt %d + bits %d + chr %d 项对照，失败 %d" % (len(DIVS),len(FMTS),len(BITS),len(CHARS),bad))
sys.exit(1 if bad else 0)
