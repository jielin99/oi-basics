window.TRACES = window.TRACES || {};
/* 由 tools/gen 生成；最终输出由 verify-traces 真实编译比对。 */
window.TRACES["ex-03-01a"] = {
 "title": "cin 读入两个整数（用空格隔开）",
 "source": "int a, b;\ncin >> a >> b;\ncout << a + b;\n",
 "harness": "#include <iostream>\n#include <cstdio>\n#include <cmath>\n#include <string>\n#include <algorithm>\nusing namespace std;\nint main() {\n%SRC%\n    return 0;\n}\n",
 "input": "12 30\n",
 "expectOutput": "42",
 "kind": "normal",
 "steps": [
  {
   "line": 1,
   "vars": {},
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "声明两个整数盒子 a、b，还没有值。下面是键盘输入的内容，cin 从左往右一个字符一个字符地读。",
   "tape": {
    "text": "12 30\n",
    "pos": 0
   }
  },
  {
   "line": 2,
   "vars": {
    "a": 12
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "cin >> a：跳过前面的空白，读一个整数，读到空白（空格或换行）就停。读到 12，放进 a。",
   "tape": {
    "text": "12 30\n",
    "pos": 2
   }
  },
  {
   "line": 2,
   "vars": {
    "a": 12,
    "b": 30
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "cin >> b：先跳过 空格，再读一个整数，读到 30。所以数字用空格隔开、还是分行输入，对 cin 来说都一样。",
   "tape": {
    "text": "12 30\n",
    "pos": 5
   }
  },
  {
   "line": 3,
   "vars": {
    "a": 12,
    "b": 30
   },
   "arrays": {},
   "hl": {},
   "out": "42",
   "note": "输出 a + b = 42。",
   "tape": {
    "text": "12 30\n",
    "pos": 5
   }
  }
 ]
};
window.TRACES["ex-03-01b"] = {
 "title": "cin 读入两个整数（分两行输入）",
 "source": "int a, b;\ncin >> a >> b;\ncout << a + b;\n",
 "harness": "#include <iostream>\n#include <cstdio>\n#include <cmath>\n#include <string>\n#include <algorithm>\nusing namespace std;\nint main() {\n%SRC%\n    return 0;\n}\n",
 "input": "12\n30\n",
 "expectOutput": "42",
 "kind": "normal",
 "steps": [
  {
   "line": 1,
   "vars": {},
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "声明两个整数盒子 a、b，还没有值。下面是键盘输入的内容，cin 从左往右一个字符一个字符地读。",
   "tape": {
    "text": "12\n30\n",
    "pos": 0
   }
  },
  {
   "line": 2,
   "vars": {
    "a": 12
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "cin >> a：跳过前面的空白，读一个整数，读到空白（空格或换行）就停。读到 12，放进 a。",
   "tape": {
    "text": "12\n30\n",
    "pos": 2
   }
  },
  {
   "line": 2,
   "vars": {
    "a": 12,
    "b": 30
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "cin >> b：先跳过 换行，再读一个整数，读到 30。所以数字用空格隔开、还是分行输入，对 cin 来说都一样。",
   "tape": {
    "text": "12\n30\n",
    "pos": 5
   }
  },
  {
   "line": 3,
   "vars": {
    "a": 12,
    "b": 30
   },
   "arrays": {},
   "hl": {},
   "out": "42",
   "note": "输出 a + b = 42。",
   "tape": {
    "text": "12\n30\n",
    "pos": 5
   }
  }
 ]
};
window.TRACES["ex-03-02"] = {
 "title": "while (cin >> x)：读到输入结束为止",
 "source": "int x, sum = 0;\nwhile (cin >> x) {\n    sum += x;\n}\ncout << sum;\n",
 "harness": "#include <iostream>\n#include <cstdio>\n#include <cmath>\n#include <string>\n#include <algorithm>\nusing namespace std;\nint main() {\n%SRC%\n    return 0;\n}\n",
 "input": "3 5 4\n",
 "expectOutput": "12",
 "kind": "normal",
 "steps": [
  {
   "line": 1,
   "vars": {
    "sum": 0
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "sum 先清 0。x 还没有值。",
   "tape": {
    "text": "3 5 4\n",
    "pos": 0
   }
  },
  {
   "line": 2,
   "vars": {
    "sum": 0,
    "x": 3
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "cin >> x 读成功（读到 3），条件为真（cin >> x 本身的值是“读成功没有”），进入循环体。",
   "tape": {
    "text": "3 5 4\n",
    "pos": 1
   }
  },
  {
   "line": 3,
   "vars": {
    "sum": 3,
    "x": 3
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "sum += x，sum 变成 3。",
   "tape": {
    "text": "3 5 4\n",
    "pos": 1
   }
  },
  {
   "line": 2,
   "vars": {
    "sum": 3,
    "x": 5
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "cin >> x 读成功（读到 5），条件为真（cin >> x 本身的值是“读成功没有”），进入循环体。",
   "tape": {
    "text": "3 5 4\n",
    "pos": 3
   }
  },
  {
   "line": 3,
   "vars": {
    "sum": 8,
    "x": 5
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "sum += x，sum 变成 8。",
   "tape": {
    "text": "3 5 4\n",
    "pos": 3
   }
  },
  {
   "line": 2,
   "vars": {
    "sum": 8,
    "x": 4
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "cin >> x 读成功（读到 4），条件为真（cin >> x 本身的值是“读成功没有”），进入循环体。",
   "tape": {
    "text": "3 5 4\n",
    "pos": 5
   }
  },
  {
   "line": 3,
   "vars": {
    "sum": 12,
    "x": 4
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "sum += x，sum 变成 12。",
   "tape": {
    "text": "3 5 4\n",
    "pos": 5
   }
  },
  {
   "line": 2,
   "vars": {
    "sum": 12,
    "x": 4
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "再读：跳过换行后，输入已经到头了（EOF），读失败，条件为假，循环结束。本地测试时输完数据按 Ctrl+Z 再回车就是告诉程序“输入结束”。",
   "tape": {
    "text": "3 5 4\n",
    "pos": 6
   }
  },
  {
   "line": 5,
   "vars": {
    "sum": 12,
    "x": 4
   },
   "arrays": {},
   "hl": {},
   "out": "12",
   "note": "输出 12。",
   "tape": {
    "text": "3 5 4\n",
    "pos": 6
   }
  }
 ]
};
