window.TRACES = window.TRACES || {};
/* 由 tools/gen 生成；最终输出由 verify-traces 真实编译比对。 */
window.TRACES["ex-11-01"] = {
 "title": "vector：会自己变长的数组",
 "source": "vector<int> v;\nv.push_back(3);\nv.push_back(5);\nv.push_back(1);\ncout << v.size() << \" \" << v[0];\nv.pop_back();\ncout << \" \" << v.size();\n",
 "harness": "#include <iostream>\n#include <cstdio>\n#include <cmath>\n#include <string>\n#include <algorithm>\nusing namespace std;\n#include <vector>\n#include <stack>\n#include <queue>\n#include <map>\n#include <set>\nint main() {\n%SRC%\n    return 0;\n}\n",
 "input": "",
 "expectOutput": "3 3 2",
 "kind": "normal",
 "steps": [
  {
   "line": 1,
   "vars": {},
   "arrays": {
    "v": []
   },
   "hl": {},
   "out": "",
   "note": "v 是一个空的 vector，里面一个元素都没有。和普通数组不同，它不用提前规定大小。"
  },
  {
   "line": 2,
   "vars": {},
   "arrays": {
    "v": [
     3
    ]
   },
   "hl": {
    "v": 0
   },
   "out": "",
   "note": "push_back(3)：在末尾追加一个元素（像 Python 的 append）。"
  },
  {
   "line": 3,
   "vars": {},
   "arrays": {
    "v": [
     3,
     5
    ]
   },
   "hl": {
    "v": 1
   },
   "out": "",
   "note": "再追加 5。"
  },
  {
   "line": 4,
   "vars": {},
   "arrays": {
    "v": [
     3,
     5,
     1
    ]
   },
   "hl": {
    "v": 2
   },
   "out": "",
   "note": "再追加 1。现在 v = {3, 5, 1}。"
  },
  {
   "line": 5,
   "vars": {},
   "arrays": {
    "v": [
     3,
     5,
     1
    ]
   },
   "hl": {
    "v": 0
   },
   "out": "3 3",
   "note": "v.size() 是元素个数 3；v[0] 是第一个元素 3。下标从 0 开始，同样不检查越界！"
  },
  {
   "line": 6,
   "vars": {},
   "arrays": {
    "v": [
     3,
     5
    ]
   },
   "hl": {},
   "out": "3 3",
   "note": "pop_back()：删除末尾的元素，v 变成 {3, 5}。"
  },
  {
   "line": 7,
   "vars": {},
   "arrays": {
    "v": [
     3,
     5
    ]
   },
   "hl": {},
   "out": "3 3 2",
   "note": "size 变成 2。"
  }
 ]
};
window.TRACES["ex-11-02"] = {
 "title": "stack（栈）：后进先出，像一摞盘子",
 "source": "stack<int> st;\nst.push(1);\nst.push(2);\nst.push(3);\ncout << st.top() << \" \";\nst.pop();\nwhile (!st.empty()) {\n    cout << st.top() << \" \";\n    st.pop();\n}\n",
 "harness": "#include <iostream>\n#include <cstdio>\n#include <cmath>\n#include <string>\n#include <algorithm>\nusing namespace std;\n#include <vector>\n#include <stack>\n#include <queue>\n#include <map>\n#include <set>\nint main() {\n%SRC%\n    return 0;\n}\n",
 "input": "",
 "expectOutput": "3 2 1",
 "kind": "normal",
 "steps": [
  {
   "line": 1,
   "vars": {},
   "arrays": {
    "st": []
   },
   "hl": {},
   "out": "",
   "note": "空栈。图里左边是栈底，右边是栈顶：只能在栈顶放、在栈顶拿。"
  },
  {
   "line": 2,
   "vars": {},
   "arrays": {
    "st": [
     1
    ]
   },
   "hl": {
    "st": 0
   },
   "out": "",
   "note": "push(1)：放到栈顶。"
  },
  {
   "line": 3,
   "vars": {},
   "arrays": {
    "st": [
     1,
     2
    ]
   },
   "hl": {
    "st": 1
   },
   "out": "",
   "note": "push(2)：放到栈顶。"
  },
  {
   "line": 4,
   "vars": {},
   "arrays": {
    "st": [
     1,
     2,
     3
    ]
   },
   "hl": {
    "st": 2
   },
   "out": "",
   "note": "push(3)：放到栈顶。"
  },
  {
   "line": 5,
   "vars": {},
   "arrays": {
    "st": [
     1,
     2,
     3
    ]
   },
   "hl": {
    "st": 2
   },
   "out": "3 ",
   "note": "top() 只“看”栈顶，是 3，不会拿走它。"
  },
  {
   "line": 6,
   "vars": {},
   "arrays": {
    "st": [
     1,
     2
    ]
   },
   "hl": {},
   "out": "3 ",
   "note": "pop() 把栈顶的 3 弹出。注意：pop() 没有返回值，要先 top() 看了值，再 pop()。"
  },
  {
   "line": 7,
   "vars": {},
   "arrays": {
    "st": [
     1,
     2
    ]
   },
   "hl": {
    "st": 1
   },
   "out": "3 ",
   "note": "栈不空，继续。"
  },
  {
   "line": 8,
   "vars": {},
   "arrays": {
    "st": [
     1,
     2
    ]
   },
   "hl": {
    "st": 1
   },
   "out": "3 2 ",
   "note": "看栈顶：2。"
  },
  {
   "line": 9,
   "vars": {},
   "arrays": {
    "st": [
     1
    ]
   },
   "hl": {},
   "out": "3 2 ",
   "note": "弹出 2。"
  },
  {
   "line": 7,
   "vars": {},
   "arrays": {
    "st": [
     1
    ]
   },
   "hl": {
    "st": 0
   },
   "out": "3 2 ",
   "note": "栈不空，继续。"
  },
  {
   "line": 8,
   "vars": {},
   "arrays": {
    "st": [
     1
    ]
   },
   "hl": {
    "st": 0
   },
   "out": "3 2 1 ",
   "note": "看栈顶：1。"
  },
  {
   "line": 9,
   "vars": {},
   "arrays": {
    "st": []
   },
   "hl": {},
   "out": "3 2 1 ",
   "note": "弹出 1。"
  },
  {
   "line": 7,
   "vars": {},
   "arrays": {
    "st": []
   },
   "hl": {},
   "out": "3 2 1 ",
   "note": "栈空了，循环结束。后放进去的先出来：3 2 1，和放进去的顺序正好相反。"
  }
 ]
};
window.TRACES["ex-11-03"] = {
 "title": "queue（队列）：先进先出，像排队",
 "source": "queue<int> q;\nq.push(1);\nq.push(2);\nq.push(3);\ncout << q.front() << \" \";\nq.pop();\ncout << q.front() << \" \" << q.back();\n",
 "harness": "#include <iostream>\n#include <cstdio>\n#include <cmath>\n#include <string>\n#include <algorithm>\nusing namespace std;\n#include <vector>\n#include <stack>\n#include <queue>\n#include <map>\n#include <set>\nint main() {\n%SRC%\n    return 0;\n}\n",
 "input": "",
 "expectOutput": "1 2 3",
 "kind": "normal",
 "steps": [
  {
   "line": 1,
   "vars": {},
   "arrays": {
    "q": []
   },
   "hl": {},
   "out": "",
   "note": "空队列。左边是队头，右边是队尾：从队尾进，从队头出。"
  },
  {
   "line": 2,
   "vars": {},
   "arrays": {
    "q": [
     1
    ]
   },
   "hl": {
    "q": 0
   },
   "out": "",
   "note": "push(1)：排到队尾。"
  },
  {
   "line": 3,
   "vars": {},
   "arrays": {
    "q": [
     1,
     2
    ]
   },
   "hl": {
    "q": 1
   },
   "out": "",
   "note": "push(2)：排到队尾。"
  },
  {
   "line": 4,
   "vars": {},
   "arrays": {
    "q": [
     1,
     2,
     3
    ]
   },
   "hl": {
    "q": 2
   },
   "out": "",
   "note": "push(3)：排到队尾。"
  },
  {
   "line": 5,
   "vars": {},
   "arrays": {
    "q": [
     1,
     2,
     3
    ]
   },
   "hl": {
    "q": 0
   },
   "out": "1 ",
   "note": "front() 看队头，是最先来的 1。"
  },
  {
   "line": 6,
   "vars": {},
   "arrays": {
    "q": [
     2,
     3
    ]
   },
   "hl": {},
   "out": "1 ",
   "note": "pop()：队头的 1 出队。"
  },
  {
   "line": 7,
   "vars": {},
   "arrays": {
    "q": [
     2,
     3
    ]
   },
   "hl": {
    "q": [
     0,
     1
    ]
   },
   "out": "1 2 3",
   "note": "现在队头是 2，队尾是 3。队列以后最重要的用途是 BFS（广度优先搜索）。"
  }
 ]
};
window.TRACES["ex-11-04"] = {
 "title": "map：score[\"Bob\"] 会悄悄创建一个 Bob",
 "source": "map<string, int> score;\nscore[\"Tom\"] = 90;\nscore[\"Amy\"] = 95;\ncout << score[\"Bob\"] << \" \";\ncout << score.size() << \" \";\nif (score.count(\"Eve\")) cout << \"has Eve \";\ncout << score.size();\n",
 "harness": "#include <iostream>\n#include <cstdio>\n#include <cmath>\n#include <string>\n#include <algorithm>\nusing namespace std;\n#include <vector>\n#include <stack>\n#include <queue>\n#include <map>\n#include <set>\nint main() {\n%SRC%\n    return 0;\n}\n",
 "input": "",
 "expectOutput": "0 3 3",
 "kind": "normal",
 "steps": [
  {
   "line": 1,
   "vars": {},
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "map 是“键值对”：每行是 key → value，自动按 key 从小到大排好。现在是空的。"
  },
  {
   "line": 2,
   "vars": {},
   "arrays": {
    "score": [
     [
      "Tom",
      90
     ]
    ]
   },
   "hl": {
    "score": [
     [
      1
     ]
    ]
   },
   "out": "",
   "note": "score[\"Tom\"] = 90：Tom 不存在，创建一行。"
  },
  {
   "line": 3,
   "vars": {},
   "arrays": {
    "score": [
     [
      "Amy",
      95
     ],
     [
      "Tom",
      90
     ]
    ]
   },
   "hl": {
    "score": [
     [
      1
     ]
    ]
   },
   "out": "",
   "note": "score[\"Amy\"] = 95：按 key 排序，Amy 排在 Tom 前面。"
  },
  {
   "line": 4,
   "vars": {},
   "arrays": {
    "score": [
     [
      "Amy",
      95
     ],
     [
      "Bob",
      0
     ],
     [
      "Tom",
      90
     ]
    ]
   },
   "hl": {
    "score": [
     [
      2
     ]
    ]
   },
   "out": "0 ",
   "note": "读 score[\"Bob\"]：Bob 不存在，C++ 会自动创建它，值为 0，然后才把 0 读出来！这是个坑。"
  },
  {
   "line": 5,
   "vars": {},
   "arrays": {
    "score": [
     [
      "Amy",
      95
     ],
     [
      "Bob",
      0
     ],
     [
      "Tom",
      90
     ]
    ]
   },
   "hl": {},
   "out": "0 3 ",
   "note": "所以现在 size 是 3，而不是 2。"
  },
  {
   "line": 6,
   "vars": {},
   "arrays": {
    "score": [
     [
      "Amy",
      95
     ],
     [
      "Bob",
      0
     ],
     [
      "Tom",
      90
     ]
    ]
   },
   "hl": {},
   "out": "0 3 ",
   "note": "score.count(\"Eve\") 只检查在不在，不会创建，返回 0（假）。判断 key 是否存在，要用 count，不要用 [ ]。"
  },
  {
   "line": 7,
   "vars": {},
   "arrays": {
    "score": [
     [
      "Amy",
      95
     ],
     [
      "Bob",
      0
     ],
     [
      "Tom",
      90
     ]
    ]
   },
   "hl": {},
   "out": "0 3 3",
   "note": "size 仍然是 3。"
  }
 ],
 "base": {
  "score": 1
 },
 "cols": {
  "score": [
   "key",
   "value"
  ]
 }
};
window.TRACES["ex-11-05"] = {
 "title": "set：自动排序、自动去重",
 "source": "set<int> s;\ns.insert(5);\ns.insert(1);\ns.insert(5);\ns.insert(3);\ncout << s.size() << \": \";\nfor (int x : s) cout << x << \" \";\n",
 "harness": "#include <iostream>\n#include <cstdio>\n#include <cmath>\n#include <string>\n#include <algorithm>\nusing namespace std;\n#include <vector>\n#include <stack>\n#include <queue>\n#include <map>\n#include <set>\nint main() {\n%SRC%\n    return 0;\n}\n",
 "input": "",
 "expectOutput": "3: 1 3 5",
 "kind": "normal",
 "steps": [
  {
   "line": 1,
   "vars": {},
   "arrays": {
    "s": []
   },
   "hl": {},
   "out": "",
   "note": "空集合。"
  },
  {
   "line": 2,
   "vars": {},
   "arrays": {
    "s": [
     5
    ]
   },
   "hl": {
    "s": 0
   },
   "out": "",
   "note": "insert(5)：放进集合，并且自动按从小到大排好。"
  },
  {
   "line": 3,
   "vars": {},
   "arrays": {
    "s": [
     1,
     5
    ]
   },
   "hl": {
    "s": 0
   },
   "out": "",
   "note": "insert(1)：放进集合，并且自动按从小到大排好。"
  },
  {
   "line": 4,
   "vars": {},
   "arrays": {
    "s": [
     1,
     5
    ]
   },
   "hl": {
    "s": 1
   },
   "out": "",
   "note": "insert(5)：已经有 5 了，集合里不会出现重复，什么都没变。"
  },
  {
   "line": 5,
   "vars": {},
   "arrays": {
    "s": [
     1,
     3,
     5
    ]
   },
   "hl": {
    "s": 1
   },
   "out": "",
   "note": "insert(3)：放进集合，并且自动按从小到大排好。"
  },
  {
   "line": 6,
   "vars": {},
   "arrays": {
    "s": [
     1,
     3,
     5
    ]
   },
   "hl": {},
   "out": "3: ",
   "note": "size 是 3：5 只算一个。"
  },
  {
   "line": 7,
   "vars": {},
   "arrays": {
    "s": [
     1,
     3,
     5
    ]
   },
   "hl": {},
   "out": "3: 1 3 5 ",
   "note": "遍历 set，按从小到大输出：1 3 5。"
  }
 ]
};
