window.TRACES = window.TRACES || {};
/* 由 tools/gen 生成；最终输出由 verify-traces 真实编译比对。 */
window.TRACES["ex-04-01"] = {
 "title": "复合赋值：x += 3 就是 x = x + 3",
 "source": "int x = 10;\nx += 3;\nx -= 2;\nx *= 2;\nx /= 5;\nx %= 3;\ncout << x;\n",
 "harness": "#include <iostream>\n#include <cstdio>\n#include <cmath>\n#include <string>\n#include <algorithm>\nusing namespace std;\nint main() {\n%SRC%\n    return 0;\n}\n",
 "input": "",
 "expectOutput": "1",
 "kind": "normal",
 "steps": [
  {
   "line": 1,
   "vars": {
    "x": 10
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "x 从 10 开始。"
  },
  {
   "line": 2,
   "vars": {
    "x": 13
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "x += 3，即 x = x + 3 = 13。"
  },
  {
   "line": 3,
   "vars": {
    "x": 11
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "x -= 2，即 x = x - 2 = 11。"
  },
  {
   "line": 4,
   "vars": {
    "x": 22
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "x *= 2，即 x = x * 2 = 22。"
  },
  {
   "line": 5,
   "vars": {
    "x": 4
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "x /= 5：两边都是整数，是整除，22 / 5 = 4（不是 4.4）。"
  },
  {
   "line": 6,
   "vars": {
    "x": 1
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "x %= 3：4 除以 3 余 1。"
  },
  {
   "line": 7,
   "vars": {
    "x": 1
   },
   "arrays": {},
   "hl": {},
   "out": "1",
   "note": "输出 1。"
  }
 ]
};
window.TRACES["ex-04-02"] = {
 "title": "b = a++ 与 d = ++c 的区别",
 "source": "int a = 5;\nint b = a++;\nint c = 5;\nint d = ++c;\ncout << a << \" \" << b << \" \" << c << \" \" << d;\n",
 "harness": "#include <iostream>\n#include <cstdio>\n#include <cmath>\n#include <string>\n#include <algorithm>\nusing namespace std;\nint main() {\n%SRC%\n    return 0;\n}\n",
 "input": "",
 "expectOutput": "6 5 6 6",
 "kind": "normal",
 "steps": [
  {
   "line": 1,
   "vars": {
    "a": 5
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "a = 5。"
  },
  {
   "line": 2,
   "vars": {
    "a": 6,
    "b": 5
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "b = a++：先把 a 现在的值 5 拿去给 b，然后 a 才加 1。所以 b = 5，a = 6。（a++ ：先用后加）"
  },
  {
   "line": 3,
   "vars": {
    "a": 6,
    "b": 5,
    "c": 5
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "c = 5。"
  },
  {
   "line": 4,
   "vars": {
    "a": 6,
    "b": 5,
    "c": 6,
    "d": 6
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "d = ++c：先把 c 加 1 变成 6，再把新值 6 给 d。所以 c = 6，d = 6。（++c ：先加后用）"
  },
  {
   "line": 5,
   "vars": {
    "a": 6,
    "b": 5,
    "c": 6,
    "d": 6
   },
   "arrays": {},
   "hl": {},
   "out": "6 5 6 6",
   "note": "输出 6 5 6 6。单独成一句时 i++ 和 ++i 完全一样，区别只在“被用在表达式里”的时候。"
  }
 ]
};
window.TRACES["ex-04-03"] = {
 "title": "短路求值：b 为 0 时，a / b 根本不会被计算",
 "source": "int a = 10, b = 0;\nif (b != 0 && a / b > 2) {\n    cout << \"big\";\n} else {\n    cout << \"safe\";\n}\n",
 "harness": "#include <iostream>\n#include <cstdio>\n#include <cmath>\n#include <string>\n#include <algorithm>\nusing namespace std;\nint main() {\n%SRC%\n    return 0;\n}\n",
 "input": "",
 "expectOutput": "safe",
 "kind": "normal",
 "steps": [
  {
   "line": 1,
   "vars": {
    "a": 10,
    "b": 0
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "a = 10，b = 0。注意：如果真去算 a / b，就是除以 0，程序会出错。"
  },
  {
   "line": 2,
   "vars": {
    "a": 10,
    "b": 0
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "A && B：先算左边 b != 0，0 != 0 不成立（假）。&& 只要有一边为假，整体就一定为假，所以右边 a / b > 2 根本不会被计算——这就是短路。"
  },
  {
   "line": 4,
   "vars": {
    "a": 10,
    "b": 0
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "条件为假，走 else。"
  },
  {
   "line": 5,
   "vars": {
    "a": 10,
    "b": 0
   },
   "arrays": {},
   "hl": {},
   "out": "safe",
   "note": "输出 safe。所以要先判断“除数不为 0”，再做除法。"
  }
 ]
};
