window.TRACES = window.TRACES || {};
/* 由 tools/gen 生成；最终输出由 verify-traces 真实编译比对。 */
window.TRACES["ex-01-01"] = {
 "title": "cout：想输出什么，就自己写什么",
 "source": "cout << \"I love OI\";\ncout << endl;\ncout << \"Line 2\\n\";\ncout << 10 << \" \" << 20 << endl;\ncout << 7 * 6 << endl;\ncout << \"7 * 6\" << endl;\n",
 "harness": "#include <iostream>\n#include <cstdio>\n#include <cmath>\n#include <string>\n#include <algorithm>\nusing namespace std;\nint main() {\n%SRC%\n    return 0;\n}\n",
 "input": "",
 "expectOutput": "I love OI\nLine 2\n10 20\n42\n7 * 6",
 "kind": "normal",
 "steps": [
  {
   "line": 1,
   "vars": {},
   "arrays": {},
   "hl": {},
   "out": "I love OI",
   "note": "双引号里的文字原样输出。cout 不会自动换行。"
  },
  {
   "line": 2,
   "vars": {},
   "arrays": {},
   "hl": {},
   "out": "I love OI\n",
   "note": "endl 表示换行。"
  },
  {
   "line": 3,
   "vars": {},
   "arrays": {},
   "hl": {},
   "out": "I love OI\nLine 2\n",
   "note": "\\n 写在字符串里面，也是换行。数据量大时 \"\\n\" 比 endl 快，建议养成用 \"\\n\" 的习惯。"
  },
  {
   "line": 4,
   "vars": {},
   "arrays": {},
   "hl": {},
   "out": "I love OI\nLine 2\n10 20\n",
   "note": "<< 可以连着接很多个东西。两个数之间的空格要自己写（Python 的 print 会自动加空格，cout 不会）。"
  },
  {
   "line": 5,
   "vars": {},
   "arrays": {},
   "hl": {},
   "out": "I love OI\nLine 2\n10 20\n42\n",
   "note": "没有引号：这是算式，先算出 7 * 6 = 42 再输出。"
  },
  {
   "line": 6,
   "vars": {},
   "arrays": {},
   "hl": {},
   "out": "I love OI\nLine 2\n10 20\n42\n7 * 6\n",
   "note": "加了引号：这是文字，原样输出 7 * 6。"
  }
 ]
};
window.TRACES["ex-01-02"] = {
 "title": "打印字符画：一行一行输出",
 "source": "cout << \"  *  \\n\";\ncout << \" *** \\n\";\ncout << \"*****\\n\";\ncout << \" *** \\n\";\ncout << \"  *  \\n\";\n",
 "harness": "#include <iostream>\n#include <cstdio>\n#include <cmath>\n#include <string>\n#include <algorithm>\nusing namespace std;\nint main() {\n%SRC%\n    return 0;\n}\n",
 "input": "",
 "expectOutput": "*\n ***\n*****\n ***\n  *",
 "kind": "normal",
 "steps": [
  {
   "line": 1,
   "vars": {},
   "arrays": {},
   "hl": {},
   "out": "  *  \n",
   "note": "第 1 行：“␣␣*␣␣”（␣ 表示空格）。空格也是要输出的内容，也要写进引号里。"
  },
  {
   "line": 2,
   "vars": {},
   "arrays": {},
   "hl": {},
   "out": "  *  \n *** \n",
   "note": "第 2 行：“␣***␣”（␣ 表示空格）。空格也是要输出的内容，也要写进引号里。"
  },
  {
   "line": 3,
   "vars": {},
   "arrays": {},
   "hl": {},
   "out": "  *  \n *** \n*****\n",
   "note": "第 3 行：“*****”（␣ 表示空格）。空格也是要输出的内容，也要写进引号里。"
  },
  {
   "line": 4,
   "vars": {},
   "arrays": {},
   "hl": {},
   "out": "  *  \n *** \n*****\n *** \n",
   "note": "第 4 行：“␣***␣”（␣ 表示空格）。空格也是要输出的内容，也要写进引号里。"
  },
  {
   "line": 5,
   "vars": {},
   "arrays": {},
   "hl": {},
   "out": "  *  \n *** \n*****\n *** \n  *  \n",
   "note": "第 5 行：“␣␣*␣␣”（␣ 表示空格）。空格也是要输出的内容，也要写进引号里。"
  }
 ]
};
