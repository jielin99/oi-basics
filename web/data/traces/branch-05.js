window.TRACES = window.TRACES || {};
/* 由 tools/gen 生成；最终输出由 verify-traces 真实编译比对。 */
window.TRACES["ex-05-01a"] = {
 "title": "if / else if / else：成绩 95 走哪条路",
 "source": "int score = 95;\nif (score >= 90) {\n    cout << \"A\";\n} else if (score >= 60) {\n    cout << \"B\";\n} else {\n    cout << \"C\";\n}\n",
 "harness": "#include <iostream>\n#include <cstdio>\n#include <cmath>\n#include <string>\n#include <algorithm>\nusing namespace std;\nint main() {\n%SRC%\n    return 0;\n}\n",
 "input": "",
 "expectOutput": "A",
 "kind": "normal",
 "steps": [
  {
   "line": 1,
   "vars": {
    "score": 95
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "score = 95。下面三条路，只会走其中一条。"
  },
  {
   "line": 2,
   "vars": {
    "score": 95
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "第一个条件：95 >= 90 成立 → 走这条路，后面的 else if、else 全部跳过，不会再判断。"
  },
  {
   "line": 3,
   "vars": {
    "score": 95
   },
   "arrays": {},
   "hl": {},
   "out": "A",
   "note": "输出 A。"
  }
 ]
};
window.TRACES["ex-05-01b"] = {
 "title": "if / else if / else：成绩 70 走哪条路",
 "source": "int score = 70;\nif (score >= 90) {\n    cout << \"A\";\n} else if (score >= 60) {\n    cout << \"B\";\n} else {\n    cout << \"C\";\n}\n",
 "harness": "#include <iostream>\n#include <cstdio>\n#include <cmath>\n#include <string>\n#include <algorithm>\nusing namespace std;\nint main() {\n%SRC%\n    return 0;\n}\n",
 "input": "",
 "expectOutput": "B",
 "kind": "normal",
 "steps": [
  {
   "line": 1,
   "vars": {
    "score": 70
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "score = 70。下面三条路，只会走其中一条。"
  },
  {
   "line": 2,
   "vars": {
    "score": 70
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "第一个条件：70 >= 90 不成立，往下看 else if。"
  },
  {
   "line": 4,
   "vars": {
    "score": 70
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "else if：70 >= 60 成立 → 走这条路，else 跳过。"
  },
  {
   "line": 5,
   "vars": {
    "score": 70
   },
   "arrays": {},
   "hl": {},
   "out": "B",
   "note": "输出 B。"
  }
 ]
};
window.TRACES["ex-05-01c"] = {
 "title": "if / else if / else：成绩 30 走哪条路",
 "source": "int score = 30;\nif (score >= 90) {\n    cout << \"A\";\n} else if (score >= 60) {\n    cout << \"B\";\n} else {\n    cout << \"C\";\n}\n",
 "harness": "#include <iostream>\n#include <cstdio>\n#include <cmath>\n#include <string>\n#include <algorithm>\nusing namespace std;\nint main() {\n%SRC%\n    return 0;\n}\n",
 "input": "",
 "expectOutput": "C",
 "kind": "normal",
 "steps": [
  {
   "line": 1,
   "vars": {
    "score": 30
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "score = 30。下面三条路，只会走其中一条。"
  },
  {
   "line": 2,
   "vars": {
    "score": 30
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "第一个条件：30 >= 90 不成立，往下看 else if。"
  },
  {
   "line": 4,
   "vars": {
    "score": 30
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "else if：30 >= 60 也不成立。"
  },
  {
   "line": 6,
   "vars": {
    "score": 30
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "前面都不成立，走最后的 else（else 不用写条件）。"
  },
  {
   "line": 7,
   "vars": {
    "score": 30
   },
   "arrays": {},
   "hl": {},
   "out": "C",
   "note": "输出 C。"
  }
 ]
};
window.TRACES["ex-05-02a"] = {
 "title": "switch：每个 case 都有 break",
 "source": "int x = 2;\nswitch (x) {\n    case 1:\n        cout << \"one \";\n        break;\n    case 2:\n        cout << \"two \";\n        break;\n    case 3:\n        cout << \"three \";\n        break;\n}\n",
 "harness": "#include <iostream>\n#include <cstdio>\n#include <cmath>\n#include <string>\n#include <algorithm>\nusing namespace std;\nint main() {\n%SRC%\n    return 0;\n}\n",
 "input": "",
 "expectOutput": "two",
 "kind": "normal",
 "steps": [
  {
   "line": 1,
   "vars": {
    "x": 2
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "x = 2。"
  },
  {
   "line": 6,
   "vars": {
    "x": 2
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "switch (x)：直接跳到 case 2 这个入口（中间的 case 1 不会判断）。"
  },
  {
   "line": 7,
   "vars": {
    "x": 2
   },
   "arrays": {},
   "hl": {},
   "out": "two ",
   "note": "输出 two。"
  },
  {
   "line": 8,
   "vars": {
    "x": 2
   },
   "arrays": {},
   "hl": {},
   "out": "two ",
   "note": "遇到 break，立刻跳出整个 switch。"
  }
 ]
};
window.TRACES["ex-05-02b"] = {
 "title": "switch：漏写 break 会“穿透”",
 "source": "int x = 2;\nswitch (x) {\n    case 1:\n        cout << \"one \";\n    case 2:\n        cout << \"two \";\n    case 3:\n        cout << \"three \";\n}\n",
 "harness": "#include <iostream>\n#include <cstdio>\n#include <cmath>\n#include <string>\n#include <algorithm>\nusing namespace std;\nint main() {\n%SRC%\n    return 0;\n}\n",
 "input": "",
 "expectOutput": "two three",
 "kind": "normal",
 "steps": [
  {
   "line": 1,
   "vars": {
    "x": 2
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "x = 2。这次每个 case 后面都没有 break。"
  },
  {
   "line": 5,
   "vars": {
    "x": 2
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "switch (x)：跳到 case 2 这个入口。"
  },
  {
   "line": 6,
   "vars": {
    "x": 2
   },
   "arrays": {},
   "hl": {},
   "out": "two ",
   "note": "输出 two。"
  },
  {
   "line": 8,
   "vars": {
    "x": 2
   },
   "arrays": {},
   "hl": {},
   "out": "two three ",
   "note": "没有 break，不会停！程序继续往下“掉”进 case 3，不管 x 是不是 3，照样输出 three。这就是穿透。"
  },
  {
   "line": 9,
   "vars": {
    "x": 2
   },
   "arrays": {},
   "hl": {},
   "out": "two three ",
   "note": "switch 结束。想只输出 two，要在 case 2 的末尾写 break;"
  }
 ]
};
window.TRACES["ex-05-03"] = {
 "title": "悬空 else：缩进是骗人的",
 "source": "int a = 1, b = -1;\nif (a > 0)\n    if (b > 0)\n        cout << \"both\";\nelse\n    cout << \"?\";\n",
 "harness": "#include <iostream>\n#include <cstdio>\n#include <cmath>\n#include <string>\n#include <algorithm>\nusing namespace std;\nint main() {\n%SRC%\n    return 0;\n}\n",
 "input": "",
 "expectOutput": "?",
 "kind": "normal",
 "steps": [
  {
   "line": 1,
   "vars": {
    "a": 1,
    "b": -1
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "a = 1，b = -1。"
  },
  {
   "line": 2,
   "vars": {
    "a": 1,
    "b": -1
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "外层 if：a > 0 成立，进入下一句。"
  },
  {
   "line": 3,
   "vars": {
    "a": 1,
    "b": -1
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "内层 if：b > 0 不成立（-1 不大于 0），内层 if 的内容跳过。"
  },
  {
   "line": 5,
   "vars": {
    "a": 1,
    "b": -1
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "else 排版上和外层 if 对齐，但规则是：else 总和离它最近的、还没配对的 if 配对——它属于内层的 if (b > 0)！内层条件不成立，所以走这个 else。"
  },
  {
   "line": 6,
   "vars": {
    "a": 1,
    "b": -1
   },
   "arrays": {},
   "hl": {},
   "out": "?",
   "note": "输出 ?。写上花括号就不会有这种误会。"
  }
 ]
};
window.TRACES["ex-05-04"] = {
 "title": "三个数排序：三次“比较并交换”",
 "source": "int a = 3, b = 1, c = 2, t;\nif (a > b) { t = a; a = b; b = t; }\nif (a > c) { t = a; a = c; c = t; }\nif (b > c) { t = b; b = c; c = t; }\ncout << a << \" \" << b << \" \" << c;\n",
 "harness": "#include <iostream>\n#include <cstdio>\n#include <cmath>\n#include <string>\n#include <algorithm>\nusing namespace std;\nint main() {\n%SRC%\n    return 0;\n}\n",
 "input": "",
 "expectOutput": "1 2 3",
 "kind": "normal",
 "steps": [
  {
   "line": 1,
   "vars": {
    "a": 3,
    "b": 1,
    "c": 2
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "要把 a、b、c 从小到大排好。t 是用来交换的“中间盒子”。"
  },
  {
   "line": 2,
   "vars": {
    "a": 1,
    "b": 3,
    "c": 2,
    "t": 3
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "a > b：3 > 1 成立，交换 a 和 b（借助 t）。现在 a ≤ b 了。"
  },
  {
   "line": 3,
   "vars": {
    "a": 1,
    "b": 3,
    "c": 2,
    "t": 3
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "a > c：1 > 2 不成立，不用换。现在 a 是三个数里最小的。"
  },
  {
   "line": 4,
   "vars": {
    "a": 1,
    "b": 2,
    "c": 3,
    "t": 3
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "b > c：3 > 2 成立，交换。现在 b ≤ c 了。"
  },
  {
   "line": 5,
   "vars": {
    "a": 1,
    "b": 2,
    "c": 3,
    "t": 3
   },
   "arrays": {},
   "hl": {},
   "out": "1 2 3",
   "note": "输出 1 2 3。Python 里的 a, b = b, a 在 C++ 里不能用，要借助 t，或者直接写 swap(a, b)。"
  }
 ]
};
