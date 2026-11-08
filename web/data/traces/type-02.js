window.TRACES = window.TRACES || {};
/* 由 tools/gen 生成；最终输出由 verify-traces 真实编译比对。 */
window.TRACES["ex-02-01a"] = {
 "title": "long long z = x * y：看起来对，其实错",
 "source": "int x = 100000, y = 100000;\nlong long z = x * y;\ncout << z;\n",
 "harness": "#include <iostream>\n#include <cstdio>\n#include <cmath>\n#include <string>\n#include <algorithm>\nusing namespace std;\nint main() {\n%SRC%\n    return 0;\n}\n",
 "input": "",
 "expectOutput": "",
 "kind": "illustrative",
 "steps": [
  {
   "line": 1,
   "vars": {
    "x": 100000,
    "y": 100000
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "x 和 y 都是 int，各是 10 万。"
  },
  {
   "line": 2,
   "vars": {
    "x": 100000,
    "y": 100000,
    "z": "？（不可靠）"
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "先算右边的 x * y：两个 int 相乘，结果还是 int。数学上等于 10000000000（100 亿），超过 int 的最大值 2147483647（约 21 亿）→ 溢出！溢出发生在“计算的那一刻”，C++ 规定此后结果没有保证。再装进 long long 也救不回来。"
  },
  {
   "line": 3,
   "vars": {
    "x": 100000,
    "y": 100000,
    "z": "？（不可靠）"
   },
   "arrays": {},
   "hl": {},
   "out": "（一个没有保证的数）",
   "note": "所以不能保证得到数学上正确的 10000000000，输出的数也不可依赖。注意：换编译器、换优化选项，看到的数可能不一样，不要去背它。"
  }
 ],
 "badge": "示意：溢出后的结果没有保证，所以不显示具体数字"
};
window.TRACES["ex-02-01b"] = {
 "title": "(long long)x * y：先转类型，再相乘",
 "source": "int x = 100000, y = 100000;\nlong long w = (long long)x * y;\ncout << w;\n",
 "harness": "#include <iostream>\n#include <cstdio>\n#include <cmath>\n#include <string>\n#include <algorithm>\nusing namespace std;\nint main() {\n%SRC%\n    return 0;\n}\n",
 "input": "",
 "expectOutput": "10000000000",
 "kind": "normal",
 "steps": [
  {
   "line": 1,
   "vars": {
    "x": 100000,
    "y": 100000
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "x 和 y 还是 int。"
  },
  {
   "line": 2,
   "vars": {
    "x": 100000,
    "y": 100000,
    "w": 10000000000
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "(long long)x 先把 x 的值转换成 long long（x 本身仍然是 int），这样乘法就按 long long 算（小类型自动向大类型看齐）。10万 × 10万 = 100 亿，long long 装得下（最大约 9.2×10¹⁸）。"
  },
  {
   "line": 3,
   "vars": {
    "x": 100000,
    "y": 100000,
    "w": 10000000000
   },
   "arrays": {},
   "hl": {},
   "out": "10000000000",
   "note": "输出 10000000000。最简单的办法：只要可能超过 21 亿，相关变量一开始就声明成 long long。"
  }
 ]
};
window.TRACES["ex-02-02"] = {
 "title": "整数除法 vs 小数除法",
 "source": "int a = 7, b = 2;\ndouble r1 = a / b;\ndouble r2 = (double)a / b;\ndouble r3 = a * 1.0 / b;\nint c = 3.99;\ncout << r1 << \" \" << r2 << \" \" << r3 << \" \" << c;\n",
 "harness": "#include <iostream>\n#include <cstdio>\n#include <cmath>\n#include <string>\n#include <algorithm>\nusing namespace std;\nint main() {\n%SRC%\n    return 0;\n}\n",
 "input": "",
 "expectOutput": "3 3.5 3.5 3",
 "kind": "normal",
 "steps": [
  {
   "line": 1,
   "vars": {
    "a": 7,
    "b": 2
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "a = 7，b = 2，都是 int。"
  },
  {
   "line": 2,
   "vars": {
    "a": 7,
    "b": 2,
    "r1": "3.0"
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "a / b：两边都是整数，先做整数除法 7 / 2 = 3（砍掉小数部分），然后才把 3 转成 3.0 放进 r1。所以是 3.0，不是 3.5！"
  },
  {
   "line": 3,
   "vars": {
    "a": 7,
    "b": 2,
    "r1": "3.0",
    "r2": "3.5"
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "(double)a 先把 a 变成 7.0，再除以 2：小数除法，3.5。"
  },
  {
   "line": 4,
   "vars": {
    "a": 7,
    "b": 2,
    "r1": "3.0",
    "r2": "3.5",
    "r3": "3.5"
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "常用技巧：乘 1.0 也会让整个运算变成小数运算，3.5。"
  },
  {
   "line": 5,
   "vars": {
    "a": 7,
    "b": 2,
    "r1": "3.0",
    "r2": "3.5",
    "r3": "3.5",
    "c": 3
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "小数转整数：直接砍掉小数部分，3（不是四舍五入）。"
  },
  {
   "line": 6,
   "vars": {
    "a": 7,
    "b": 2,
    "r1": "3.0",
    "r2": "3.5",
    "r3": "3.5",
    "c": 3
   },
   "arrays": {},
   "hl": {},
   "out": "3 3.5 3.5 3",
   "note": "输出（cout 默认不显示多余的 .0）：3 3.5 3.5 3。"
  }
 ]
};
