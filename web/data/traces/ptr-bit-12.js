window.TRACES = window.TRACES || {};
/* 由 tools/gen 生成；最终输出由 verify-traces 真实编译比对。 */
window.TRACES["ex-12-01"] = {
 "title": "指针：存着“另一个变量的地址”",
 "source": "int a = 5;\nint *p = &a;\ncout << *p << \" \";\n*p = 10;\ncout << a;\n",
 "harness": "#include <iostream>\n#include <cstdio>\n#include <cmath>\n#include <string>\n#include <algorithm>\nusing namespace std;\nint main() {\n%SRC%\n    return 0;\n}\n",
 "input": "",
 "expectOutput": "5 10",
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
   "note": "a 是一个普通变量，值 5。"
  },
  {
   "line": 2,
   "vars": {
    "a": 5,
    "p": "→ a（a 的地址）"
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "&a 是 a 的地址（内存格子的编号）；p 里存的就是这个地址，我们说“p 指向 a”。"
  },
  {
   "line": 3,
   "vars": {
    "a": 5,
    "p": "→ a"
   },
   "arrays": {},
   "hl": {},
   "out": "5 ",
   "note": "*p（解引用）表示“p 指向的那个变量”，也就是 a。这里是读取它的值 5；放在赋值号左边时，则是修改它。"
  },
  {
   "line": 4,
   "vars": {
    "a": 10,
    "p": "→ a"
   },
   "arrays": {},
   "hl": {},
   "out": "5 ",
   "note": "*p = 10：通过指针修改它指向的变量——a 变成了 10！"
  },
  {
   "line": 5,
   "vars": {
    "a": 10,
    "p": "→ a"
   },
   "arrays": {},
   "hl": {},
   "out": "5 10",
   "note": "输出 a：10。scanf(\"%d\", &n) 里的 &n 就是这个原理：告诉 scanf 把读到的数存到 n 的地址里。"
  }
 ]
};
window.TRACES["ex-12-02"] = {
 "title": "指针加减：p + 1 指向下一个元素",
 "source": "int a[4] = {1, 2, 3, 4};\nint *p = a + 1;\n*p += 10;\np++;\ncout << *p << \" \" << a[1];\n",
 "harness": "#include <iostream>\n#include <cstdio>\n#include <cmath>\n#include <string>\n#include <algorithm>\nusing namespace std;\nint main() {\n%SRC%\n    return 0;\n}\n",
 "input": "",
 "expectOutput": "3 12",
 "kind": "normal",
 "steps": [
  {
   "line": 1,
   "vars": {},
   "arrays": {
    "a": [
     1,
     2,
     3,
     4
    ]
   },
   "hl": {},
   "out": "",
   "note": "数组 a 有 4 个元素。"
  },
  {
   "line": 2,
   "vars": {
    "p": "→ a[1]"
   },
   "arrays": {
    "a": [
     1,
     2,
     3,
     4
    ]
   },
   "hl": {
    "a": 1
   },
   "out": "",
   "note": "a + 1 是 a[1] 的地址（数组名在表达式里会变成指向首元素的指针）。所以 p 指向 a[1]。"
  },
  {
   "line": 3,
   "vars": {
    "p": "→ a[1]"
   },
   "arrays": {
    "a": [
     1,
     12,
     3,
     4
    ]
   },
   "hl": {
    "a": 1
   },
   "out": "",
   "note": "*p += 10：p 指向的 a[1] 加 10，变成 12。"
  },
  {
   "line": 4,
   "vars": {
    "p": "→ a[2]"
   },
   "arrays": {
    "a": [
     1,
     12,
     3,
     4
    ]
   },
   "hl": {
    "a": 2
   },
   "out": "",
   "note": "p++：指针移到下一个元素，现在指向 a[2]。"
  },
  {
   "line": 5,
   "vars": {
    "p": "→ a[2]"
   },
   "arrays": {
    "a": [
     1,
     12,
     3,
     4
    ]
   },
   "hl": {
    "a": [
     1,
     2
    ]
   },
   "out": "3 12",
   "note": "*p 是 a[2] = 3；a[1] 是 12。输出 3 12。"
  }
 ]
};
window.TRACES["ex-12-03"] = {
 "title": "位运算：n & 1 取最低位，n >>= 1 去掉最低位",
 "source": "int n = 13, cnt = 0;\nwhile (n > 0) {\n    cnt += n & 1;\n    n >>= 1;\n}\ncout << cnt;\n",
 "harness": "#include <iostream>\n#include <cstdio>\n#include <cmath>\n#include <string>\n#include <algorithm>\nusing namespace std;\nint main() {\n%SRC%\n    return 0;\n}\n",
 "input": "",
 "expectOutput": "3",
 "kind": "normal",
 "steps": [
  {
   "line": 1,
   "vars": {
    "n": "13 = 1101₂",
    "cnt": 0
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "13 的二进制是 1101，里面有 3 个 1。我们用程序来数。"
  },
  {
   "line": 3,
   "vars": {
    "n": "13 = 1101₂",
    "cnt": 1
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "n & 1：只留最低位 = 1（奇数最低位是 1，偶数是 0）。cnt += 1，cnt = 1。"
  },
  {
   "line": 4,
   "vars": {
    "n": "6 = 110₂",
    "cnt": 1
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "n >>= 1：所有位右移一位，最低位被丢掉，n 变成 6 = 110₂。"
  },
  {
   "line": 3,
   "vars": {
    "n": "6 = 110₂",
    "cnt": 1
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "n & 1：只留最低位 = 0（奇数最低位是 1，偶数是 0）。cnt += 0，cnt = 1。"
  },
  {
   "line": 4,
   "vars": {
    "n": "3 = 11₂",
    "cnt": 1
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "n >>= 1：所有位右移一位，最低位被丢掉，n 变成 3 = 11₂。"
  },
  {
   "line": 3,
   "vars": {
    "n": "3 = 11₂",
    "cnt": 2
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "n & 1：只留最低位 = 1（奇数最低位是 1，偶数是 0）。cnt += 1，cnt = 2。"
  },
  {
   "line": 4,
   "vars": {
    "n": "1 = 1₂",
    "cnt": 2
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "n >>= 1：所有位右移一位，最低位被丢掉，n 变成 1 = 1₂。"
  },
  {
   "line": 3,
   "vars": {
    "n": "1 = 1₂",
    "cnt": 3
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "n & 1：只留最低位 = 1（奇数最低位是 1，偶数是 0）。cnt += 1，cnt = 3。"
  },
  {
   "line": 4,
   "vars": {
    "n": "0",
    "cnt": 3
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "n >>= 1：所有位右移一位，最低位被丢掉，n 变成 0。"
  },
  {
   "line": 2,
   "vars": {
    "n": "0",
    "cnt": 3
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "n = 0，循环结束。"
  },
  {
   "line": 6,
   "vars": {
    "n": "0",
    "cnt": 3
   },
   "arrays": {},
   "hl": {},
   "out": "3",
   "note": "输出 3：13 的二进制里有 3 个 1。"
  }
 ]
};
