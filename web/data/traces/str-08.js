window.TRACES = window.TRACES || {};
/* 由 tools/gen 生成；最终输出由 verify-traces 真实编译比对。 */
window.TRACES["ex-08-01"] = {
 "title": "string：像一排字符，下标从 0 开始",
 "source": "string s = \"hello\";\ncout << s.size() << \" \" << s[0];\ns[0] = 'H';\ns = s + \" world\";\ns += '!';\ncout << \" \" << s;\n",
 "harness": "#include <iostream>\n#include <cstdio>\n#include <cmath>\n#include <string>\n#include <algorithm>\nusing namespace std;\nint main() {\n%SRC%\n    return 0;\n}\n",
 "input": "",
 "expectOutput": "5 h Hello world!",
 "kind": "normal",
 "steps": [
  {
   "line": 1,
   "vars": {},
   "arrays": {
    "s": [
     "h",
     "e",
     "l",
     "l",
     "o"
    ]
   },
   "hl": {},
   "out": "",
   "note": "s 是一个 string，里面是 5 个字符，下标 0~4。"
  },
  {
   "line": 2,
   "vars": {},
   "arrays": {
    "s": [
     "h",
     "e",
     "l",
     "l",
     "o"
    ]
   },
   "hl": {
    "s": 0
   },
   "out": "5 h",
   "note": "s.size() 是长度 5；s[0] 是第 0 个字符 'h'。"
  },
  {
   "line": 3,
   "vars": {},
   "arrays": {
    "s": [
     "H",
     "e",
     "l",
     "l",
     "o"
    ]
   },
   "hl": {
    "s": 0
   },
   "out": "5 h",
   "note": "string 的字符可以修改：s[0] = 'H'，变成 Hello。"
  },
  {
   "line": 4,
   "vars": {},
   "arrays": {
    "s": [
     "H",
     "e",
     "l",
     "l",
     "o",
     "␣",
     "w",
     "o",
     "r",
     "l",
     "d"
    ]
   },
   "hl": {},
   "out": "5 h",
   "note": "用 + 可以拼接：s + \" world\"，空格也是一个字符（图里用 ␣ 表示）。"
  },
  {
   "line": 5,
   "vars": {},
   "arrays": {
    "s": [
     "H",
     "e",
     "l",
     "l",
     "o",
     "␣",
     "w",
     "o",
     "r",
     "l",
     "d",
     "!"
    ]
   },
   "hl": {
    "s": 11
   },
   "out": "5 h",
   "note": "s += '!' 在末尾追加一个字符。"
  },
  {
   "line": 6,
   "vars": {},
   "arrays": {
    "s": [
     "H",
     "e",
     "l",
     "l",
     "o",
     "␣",
     "w",
     "o",
     "r",
     "l",
     "d",
     "!"
    ]
   },
   "hl": {},
   "out": "5 h Hello world!",
   "note": "输出整个 string。"
  }
 ]
};
window.TRACES["ex-08-02a"] = {
 "title": "cin >> n 之后读一行：直接 getline（经典坑）",
 "source": "int n;\nstring line;\ncin >> n;\ngetline(cin, line);\ncout << \"[\" << line << \"]\";\n",
 "harness": "#include <iostream>\n#include <cstdio>\n#include <cmath>\n#include <string>\n#include <algorithm>\nusing namespace std;\nint main() {\n%SRC%\n    return 0;\n}\n",
 "input": "3\nhello\n",
 "expectOutput": "[]",
 "kind": "normal",
 "steps": [
  {
   "line": 1,
   "vars": {},
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "n 和 line 都先声明。输入是两行：3 和 hello。",
   "tape": {
    "text": "3\nhello\n",
    "pos": 0
   }
  },
  {
   "line": 3,
   "vars": {
    "n": 3
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "cin >> n：读到 3。注意：3 后面的换行符还留在输入里没被读走！",
   "tape": {
    "text": "3\nhello\n",
    "pos": 1
   }
  },
  {
   "line": 4,
   "vars": {
    "n": 3,
    "line": "\"\""
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "getline(cin, line)：从当前位置开始读，马上碰到残留的换行——一个字符也没读到，得到空字符串，同时把换行吃掉了。hello 还在后面没被读到！",
   "tape": {
    "text": "3\nhello\n",
    "pos": 2
   }
  },
  {
   "line": 5,
   "vars": {
    "n": 3,
    "line": "\"\""
   },
   "arrays": {},
   "hl": {},
   "out": "[]",
   "note": "输出 []：line 是空的。解决办法：中间加一句 getline(cin, line); 把残留的换行吃掉。",
   "tape": {
    "text": "3\nhello\n",
    "pos": 2
   }
  }
 ]
};
window.TRACES["ex-08-02b"] = {
 "title": "cin >> n 之后读一行：先多读一次 getline（对）",
 "source": "int n;\nstring line;\ncin >> n;\ngetline(cin, line);\ngetline(cin, line);\ncout << \"[\" << line << \"]\";\n",
 "harness": "#include <iostream>\n#include <cstdio>\n#include <cmath>\n#include <string>\n#include <algorithm>\nusing namespace std;\nint main() {\n%SRC%\n    return 0;\n}\n",
 "input": "3\nhello\n",
 "expectOutput": "[hello]",
 "kind": "normal",
 "steps": [
  {
   "line": 1,
   "vars": {},
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "n 和 line 都先声明。输入是两行：3 和 hello。",
   "tape": {
    "text": "3\nhello\n",
    "pos": 0
   }
  },
  {
   "line": 3,
   "vars": {
    "n": 3
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "cin >> n：读到 3。注意：3 后面的换行符还留在输入里没被读走！",
   "tape": {
    "text": "3\nhello\n",
    "pos": 1
   }
  },
  {
   "line": 4,
   "vars": {
    "n": 3,
    "line": "\"\""
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "先来一句 getline：它从当前位置读到换行为止——读到的是“空”，同时把那个残留的换行吃掉了。",
   "tape": {
    "text": "3\nhello\n",
    "pos": 2
   }
  },
  {
   "line": 5,
   "vars": {
    "n": 3,
    "line": "hello"
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "再 getline：现在才从 hello 这一行开始读，读到 hello，连换行一起吃掉。",
   "tape": {
    "text": "3\nhello\n",
    "pos": 8
   }
  },
  {
   "line": 6,
   "vars": {
    "n": 3,
    "line": "hello"
   },
   "arrays": {},
   "hl": {},
   "out": "[hello]",
   "note": "输出 [hello]，正确。前提是要读的文字在下一行；如果文字和 n 在同一行，这样写就会把它们一起丢掉。",
   "tape": {
    "text": "3\nhello\n",
    "pos": 8
   }
  }
 ]
};
window.TRACES["ex-08-03"] = {
 "title": "统计字母：用 c - 'a' 当桶的下标（cnt 是全局的 26 个桶）",
 "source": "string s = \"abca\";\nfor (char c : s) {\n    cnt[c - 'a']++;\n}\nfor (int i = 0; i < 3; i++) {\n    cout << (char)('a' + i) << \":\" << cnt[i] << \" \";\n}\n",
 "harness": "#include <iostream>\n#include <cstdio>\n#include <cmath>\n#include <string>\n#include <algorithm>\nusing namespace std;\nint cnt[26];\nint main() {\n%SRC%\n    return 0;\n}\n",
 "input": "",
 "expectOutput": "a:2 b:1 c:1",
 "kind": "normal",
 "steps": [
  {
   "line": 1,
   "vars": {},
   "arrays": {
    "s": [
     "a",
     "b",
     "c",
     "a"
    ],
    "cnt": [
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0
    ]
   },
   "hl": {},
   "out": "",
   "note": "要统计 abca 里每个字母出现几次。cnt[0] 记 a，cnt[1] 记 b……全局数组一开始全是 0。"
  },
  {
   "line": 3,
   "vars": {
    "c": "a"
   },
   "arrays": {
    "s": [
     "a",
     "b",
     "c",
     "a"
    ],
    "cnt": [
     1,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0
    ]
   },
   "hl": {
    "s": 0,
    "cnt": 0
   },
   "out": "",
   "note": "c = 'a'：c - 'a' = 0（'a'→0，'b'→1……），所以 cnt[0]++，变成 1。字符连续编号，减去 'a' 就得到 0~25 的下标。"
  },
  {
   "line": 3,
   "vars": {
    "c": "b"
   },
   "arrays": {
    "s": [
     "a",
     "b",
     "c",
     "a"
    ],
    "cnt": [
     1,
     1,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0
    ]
   },
   "hl": {
    "s": 1,
    "cnt": 1
   },
   "out": "",
   "note": "c = 'b'：c - 'a' = 1（'a'→0，'b'→1……），所以 cnt[1]++，变成 1。字符连续编号，减去 'a' 就得到 0~25 的下标。"
  },
  {
   "line": 3,
   "vars": {
    "c": "c"
   },
   "arrays": {
    "s": [
     "a",
     "b",
     "c",
     "a"
    ],
    "cnt": [
     1,
     1,
     1,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0
    ]
   },
   "hl": {
    "s": 2,
    "cnt": 2
   },
   "out": "",
   "note": "c = 'c'：c - 'a' = 2（'a'→0，'b'→1……），所以 cnt[2]++，变成 1。字符连续编号，减去 'a' 就得到 0~25 的下标。"
  },
  {
   "line": 3,
   "vars": {
    "c": "a"
   },
   "arrays": {
    "s": [
     "a",
     "b",
     "c",
     "a"
    ],
    "cnt": [
     2,
     1,
     1,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0
    ]
   },
   "hl": {
    "s": 3,
    "cnt": 0
   },
   "out": "",
   "note": "c = 'a'：c - 'a' = 0（'a'→0，'b'→1……），所以 cnt[0]++，变成 2。字符连续编号，减去 'a' 就得到 0~25 的下标。"
  },
  {
   "line": 6,
   "vars": {
    "i": 0
   },
   "arrays": {
    "s": [
     "a",
     "b",
     "c",
     "a"
    ],
    "cnt": [
     2,
     1,
     1,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0
    ]
   },
   "hl": {
    "cnt": 0
   },
   "out": "a:2 ",
   "note": "i = 0：'a' + 0 是 'a'，(char) 把它当字符输出；cnt[0] = 2。"
  },
  {
   "line": 6,
   "vars": {
    "i": 1
   },
   "arrays": {
    "s": [
     "a",
     "b",
     "c",
     "a"
    ],
    "cnt": [
     2,
     1,
     1,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0
    ]
   },
   "hl": {
    "cnt": 1
   },
   "out": "a:2 b:1 ",
   "note": "i = 1：'a' + 1 是 'b'，(char) 把它当字符输出；cnt[1] = 1。"
  },
  {
   "line": 6,
   "vars": {
    "i": 2
   },
   "arrays": {
    "s": [
     "a",
     "b",
     "c",
     "a"
    ],
    "cnt": [
     2,
     1,
     1,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0
    ]
   },
   "hl": {
    "cnt": 2
   },
   "out": "a:2 b:1 c:1 ",
   "note": "i = 2：'a' + 2 是 'c'，(char) 把它当字符输出；cnt[2] = 1。"
  }
 ]
};
