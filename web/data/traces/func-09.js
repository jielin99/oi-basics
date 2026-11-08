window.TRACES = window.TRACES || {};
/* 由 tools/gen 生成；最终输出由 verify-traces 真实编译比对。 */
window.TRACES["ex-09-01a"] = {
 "title": "值传递：函数拿到“复印件”",
 "source": "void change(int x) {\n    x = 100;\n}\nint main() {\n    int a = 5;\n    change(a);\n    cout << a;\n}\n",
 "harness": "#include <iostream>\n#include <cstdio>\n#include <cmath>\n#include <string>\n#include <algorithm>\nusing namespace std;\n%SRC%\n",
 "input": "",
 "expectOutput": "5",
 "kind": "normal",
 "steps": [
  {
   "line": 5,
   "vars": {},
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "main 里有一个变量 a，值是 5。",
   "stack": [
    {
     "fn": "main",
     "vars": {
      "a": 5
     },
     "at": ""
    }
   ]
  },
  {
   "line": 6,
   "vars": {},
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "调用 change(a)：函数的参数 x 是 a 的一份“复印件”，里面也是 5，但它是另一个格子。",
   "stack": [
    {
     "fn": "main",
     "vars": {
      "a": 5
     },
     "at": "等待 change 结束"
    },
    {
     "fn": "change",
     "vars": {
      "x": 5
     },
     "at": "x 是复印件"
    }
   ]
  },
  {
   "line": 2,
   "vars": {},
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "x = 100：改的是复印件。原件 a 纹丝不动，还是 5。",
   "stack": [
    {
     "fn": "main",
     "vars": {
      "a": 5
     },
     "at": "等待 change 结束"
    },
    {
     "fn": "change",
     "vars": {
      "x": 100
     },
     "at": "只改了复印件"
    }
   ]
  },
  {
   "line": 3,
   "vars": {},
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "change 结束，复印件 x 随着函数一起消失。",
   "stack": [
    {
     "fn": "main",
     "vars": {
      "a": 5
     },
     "at": ""
    }
   ]
  },
  {
   "line": 7,
   "vars": {},
   "arrays": {},
   "hl": {},
   "out": "5",
   "note": "输出 a：还是 5。",
   "stack": [
    {
     "fn": "main",
     "vars": {
      "a": 5
     },
     "at": ""
    }
   ]
  }
 ]
};
window.TRACES["ex-09-01b"] = {
 "title": "引用传递：函数拿到“原件”",
 "source": "void change(int &x) {\n    x = 100;\n}\nint main() {\n    int a = 5;\n    change(a);\n    cout << a;\n}\n",
 "harness": "#include <iostream>\n#include <cstdio>\n#include <cmath>\n#include <string>\n#include <algorithm>\nusing namespace std;\n%SRC%\n",
 "input": "",
 "expectOutput": "100",
 "kind": "normal",
 "steps": [
  {
   "line": 5,
   "vars": {},
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "main 里有一个变量 a，值是 5。",
   "stack": [
    {
     "fn": "main",
     "vars": {
      "a": 5
     },
     "at": ""
    }
   ]
  },
  {
   "line": 6,
   "vars": {},
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "调用 change(a)：参数写成 int &x，x 就是 a 的“别名”——不是复印件，和 a 是同一个格子。",
   "stack": [
    {
     "fn": "main",
     "vars": {
      "a": 5
     },
     "at": "等待 change 结束"
    },
    {
     "fn": "change",
     "vars": {
      "x": "（就是 a）5"
     },
     "at": "x 是 a 的别名"
    }
   ]
  },
  {
   "line": 2,
   "vars": {},
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "x = 100：改 x 就是改 a！",
   "stack": [
    {
     "fn": "main",
     "vars": {
      "a": 100
     },
     "at": "等待 change 结束"
    },
    {
     "fn": "change",
     "vars": {
      "x": "（就是 a）100"
     },
     "at": "改的是原件"
    }
   ]
  },
  {
   "line": 3,
   "vars": {},
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "change 结束。",
   "stack": [
    {
     "fn": "main",
     "vars": {
      "a": 100
     },
     "at": ""
    }
   ]
  },
  {
   "line": 7,
   "vars": {},
   "arrays": {},
   "hl": {},
   "out": "100",
   "note": "输出 a：变成了 100。想在函数里改外面的变量，参数类型后面要加 &。",
   "stack": [
    {
     "fn": "main",
     "vars": {
      "a": 100
     },
     "at": ""
    }
   ]
  }
 ]
};
window.TRACES["ex-09-02"] = {
 "title": "递归：fact(3) 一层一层进去，再一层一层出来",
 "source": "long long fact(int n) {\n    if (n == 0) return 1;\n    return n * fact(n - 1);\n}\nint main() {\n    cout << fact(3);\n}\n",
 "harness": "#include <iostream>\n#include <cstdio>\n#include <cmath>\n#include <string>\n#include <algorithm>\nusing namespace std;\n%SRC%\n",
 "input": "",
 "expectOutput": "6",
 "kind": "normal",
 "steps": [
  {
   "line": 6,
   "vars": {},
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "main 调用 fact(3)。每调用一次函数，就会多出一个“栈帧”，每个栈帧里有自己的 n。",
   "stack": [
    {
     "fn": "main",
     "vars": {},
     "at": "等待 fact(3) 的结果"
    },
    {
     "fn": "fact(3)",
     "vars": {
      "n": 3
     },
     "at": "正在执行"
    }
   ]
  },
  {
   "line": 2,
   "vars": {},
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "fact(3)：n == 0 吗？3 不等于 0，不是出口，继续。",
   "stack": [
    {
     "fn": "main",
     "vars": {},
     "at": "等待"
    },
    {
     "fn": "fact(3)",
     "vars": {
      "n": 3
     },
     "at": "正在执行"
    }
   ]
  },
  {
   "line": 3,
   "vars": {},
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "return 3 * fact(2)：要先算出 fact(2) 才能算乘法。于是 fact(3) 暂停，调用 fact(2)。注意：新的栈帧里 n 是 2，和下面那个 n = 3 互不相干。",
   "stack": [
    {
     "fn": "main",
     "vars": {},
     "at": "等待"
    },
    {
     "fn": "fact(3)",
     "vars": {
      "n": 3
     },
     "at": "暂停，等 fact(2)"
    },
    {
     "fn": "fact(2)",
     "vars": {
      "n": 2
     },
     "at": "正在执行"
    }
   ]
  },
  {
   "line": 2,
   "vars": {},
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "fact(2)：n == 0 吗？不是，继续。",
   "stack": [
    {
     "fn": "main",
     "vars": {},
     "at": "等待"
    },
    {
     "fn": "fact(3)",
     "vars": {
      "n": 3
     },
     "at": "暂停，等 fact(2)"
    },
    {
     "fn": "fact(2)",
     "vars": {
      "n": 2
     },
     "at": "正在执行"
    }
   ]
  },
  {
   "line": 3,
   "vars": {},
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "return 2 * fact(1)：fact(2) 也暂停，调用 fact(1)。",
   "stack": [
    {
     "fn": "main",
     "vars": {},
     "at": "等待"
    },
    {
     "fn": "fact(3)",
     "vars": {
      "n": 3
     },
     "at": "暂停，等 fact(2)"
    },
    {
     "fn": "fact(2)",
     "vars": {
      "n": 2
     },
     "at": "暂停，等 fact(1)"
    },
    {
     "fn": "fact(1)",
     "vars": {
      "n": 1
     },
     "at": "正在执行"
    }
   ]
  },
  {
   "line": 2,
   "vars": {},
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "fact(1)：n == 0 吗？不是，继续。",
   "stack": [
    {
     "fn": "main",
     "vars": {},
     "at": "等待"
    },
    {
     "fn": "fact(3)",
     "vars": {
      "n": 3
     },
     "at": "暂停"
    },
    {
     "fn": "fact(2)",
     "vars": {
      "n": 2
     },
     "at": "暂停"
    },
    {
     "fn": "fact(1)",
     "vars": {
      "n": 1
     },
     "at": "正在执行"
    }
   ]
  },
  {
   "line": 3,
   "vars": {},
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "return 1 * fact(0)：fact(1) 暂停，调用 fact(0)。",
   "stack": [
    {
     "fn": "main",
     "vars": {},
     "at": "等待"
    },
    {
     "fn": "fact(3)",
     "vars": {
      "n": 3
     },
     "at": "暂停"
    },
    {
     "fn": "fact(2)",
     "vars": {
      "n": 2
     },
     "at": "暂停"
    },
    {
     "fn": "fact(1)",
     "vars": {
      "n": 1
     },
     "at": "暂停，等 fact(0)"
    },
    {
     "fn": "fact(0)",
     "vars": {
      "n": 0
     },
     "at": "正在执行"
    }
   ]
  },
  {
   "line": 2,
   "vars": {},
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "fact(0)：n == 0 成立！这就是出口，直接 return 1，不再往下调用了。——到底了，接下来开始一层一层返回。",
   "stack": [
    {
     "fn": "main",
     "vars": {},
     "at": "等待"
    },
    {
     "fn": "fact(3)",
     "vars": {
      "n": 3
     },
     "at": "暂停"
    },
    {
     "fn": "fact(2)",
     "vars": {
      "n": 2
     },
     "at": "暂停"
    },
    {
     "fn": "fact(1)",
     "vars": {
      "n": 1
     },
     "at": "暂停"
    },
    {
     "fn": "fact(0)",
     "vars": {
      "n": 0
     },
     "at": "出口：返回 1"
    }
   ]
  },
  {
   "line": 3,
   "vars": {},
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "fact(0) 返回 1，它的栈帧消失。fact(1) 拿到 1，算 1 * 1 = 1。",
   "stack": [
    {
     "fn": "main",
     "vars": {},
     "at": "等待"
    },
    {
     "fn": "fact(3)",
     "vars": {
      "n": 3
     },
     "at": "暂停"
    },
    {
     "fn": "fact(2)",
     "vars": {
      "n": 2
     },
     "at": "暂停"
    },
    {
     "fn": "fact(1)",
     "vars": {
      "n": 1
     },
     "at": "拿到 1，算 1 * 1 = 1，返回"
    }
   ],
   "ret": 1
  },
  {
   "line": 3,
   "vars": {},
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "fact(1) 返回 1。fact(2) 拿到 1，算 2 * 1 = 2。",
   "stack": [
    {
     "fn": "main",
     "vars": {},
     "at": "等待"
    },
    {
     "fn": "fact(3)",
     "vars": {
      "n": 3
     },
     "at": "暂停"
    },
    {
     "fn": "fact(2)",
     "vars": {
      "n": 2
     },
     "at": "拿到 1，算 2 * 1 = 2，返回"
    }
   ],
   "ret": 1
  },
  {
   "line": 3,
   "vars": {},
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "fact(2) 返回 2。fact(3) 拿到 2，算 3 * 2 = 6。",
   "stack": [
    {
     "fn": "main",
     "vars": {},
     "at": "等待"
    },
    {
     "fn": "fact(3)",
     "vars": {
      "n": 3
     },
     "at": "拿到 2，算 3 * 2 = 6，返回"
    }
   ],
   "ret": 2
  },
  {
   "line": 6,
   "vars": {},
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "fact(3) 返回 6，栈里只剩 main。",
   "stack": [
    {
     "fn": "main",
     "vars": {},
     "at": "拿到 6，准备输出"
    }
   ],
   "ret": 6
  },
  {
   "line": 6,
   "vars": {},
   "arrays": {},
   "hl": {},
   "out": "6",
   "note": "输出 6。写递归的两要素：① 出口（什么时候不再递归）；② 递推关系（怎样把大问题变成更小的同类问题）。",
   "stack": [
    {
     "fn": "main",
     "vars": {},
     "at": "结束"
    }
   ]
  }
 ]
};
