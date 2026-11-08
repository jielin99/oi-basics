window.TRACES = window.TRACES || {};
/* 第 10 课排序小样。由 gen10.py 按语义推演生成；最终输出由 verify-traces 真实编译比对，
 * 中间状态已人工核对（见 docs/web-courseware-design.md 的 T3 记录）。
 * 注意：ex-10-02 只演示“cmp 被问到什么、怎么回答”，不冒充 std::sort 内部的搬动顺序。 */
window.TRACES["ex-10-01"] = {
 "title": "冒泡排序：4 个数，一共 3 轮",
 "source": "int a[5] = {0, 4, 2, 3, 1};   // a[0] 不用\nint n = 4;\nfor (int i = 1; i < n; i++) {\n    for (int j = 1; j <= n - i; j++) {\n        if (a[j] > a[j + 1]) swap(a[j], a[j + 1]);\n    }\n}\nfor (int i = 1; i <= n; i++) cout << a[i] << \" \";\n",
 "harness": "#include <iostream>\n#include <algorithm>\nusing namespace std;\nint main() {\n%SRC%\n    return 0;\n}\n",
 "input": "",
 "expectOutput": "1 2 3 4",
 "kind": "normal",
 "base": {
  "a": 1
 },
 "steps": [
  {
   "line": 1,
   "vars": {},
   "arrays": {
    "a": [
     4,
     2,
     3,
     1
    ]
   },
   "hl": {},
   "out": "",
   "note": "4 个数放在 a[1]~a[4]：4 2 3 1。冒泡排序的想法：每一轮从左到右，相邻两个比一比，前面大就交换，大的数会像气泡一样“冒”到最后。"
  },
  {
   "line": 2,
   "vars": {
    "n": 4
   },
   "arrays": {
    "a": [
     4,
     2,
     3,
     1
    ]
   },
   "hl": {},
   "out": "",
   "note": "n = 4 个数。"
  },
  {
   "line": 3,
   "vars": {
    "n": 4,
    "i": 1
   },
   "arrays": {
    "a": [
     4,
     2,
     3,
     1
    ]
   },
   "hl": {},
   "out": "",
   "note": "第 1 轮开始（i = 1）。一共要进行 n - 1 = 3 轮。"
  },
  {
   "line": 5,
   "vars": {
    "n": 4,
    "i": 1,
    "j": 1
   },
   "arrays": {
    "a": [
     2,
     4,
     3,
     1
    ]
   },
   "hl": {
    "a": [
     1,
     2
    ]
   },
   "out": "",
   "note": "内层 j 从 1 开始。比较 a[1] = 4 和 a[2] = 2：4 > 2，前面大，交换！"
  },
  {
   "line": 5,
   "vars": {
    "n": 4,
    "i": 1,
    "j": 2
   },
   "arrays": {
    "a": [
     2,
     3,
     4,
     1
    ]
   },
   "hl": {
    "a": [
     2,
     3
    ]
   },
   "out": "",
   "note": "j++ 变成 2。比较 a[2] = 4 和 a[3] = 3：4 > 3，前面大，交换！"
  },
  {
   "line": 5,
   "vars": {
    "n": 4,
    "i": 1,
    "j": 3
   },
   "arrays": {
    "a": [
     2,
     3,
     1,
     4
    ]
   },
   "hl": {
    "a": [
     3,
     4
    ]
   },
   "out": "",
   "note": "j++ 变成 3。比较 a[3] = 4 和 a[4] = 1：4 > 1，前面大，交换！ 这一轮结束：数组是 [2, 3, 1, 4]，最大的 4 已经“冒”到了位置 4。"
  },
  {
   "line": 3,
   "vars": {
    "n": 4,
    "i": 2
   },
   "arrays": {
    "a": [
     2,
     3,
     1,
     4
    ]
   },
   "hl": {},
   "out": "",
   "note": "第 2 轮开始（i = 2）。这一轮只需要比较前 3 个位置，因为后面 1 个已经排好了。"
  },
  {
   "line": 5,
   "vars": {
    "n": 4,
    "i": 2,
    "j": 1
   },
   "arrays": {
    "a": [
     2,
     3,
     1,
     4
    ]
   },
   "hl": {
    "a": [
     1,
     2
    ]
   },
   "out": "",
   "note": "内层 j 从 1 开始。比较 a[1] = 2 和 a[2] = 3：2 > 3 不成立，不用交换。"
  },
  {
   "line": 5,
   "vars": {
    "n": 4,
    "i": 2,
    "j": 2
   },
   "arrays": {
    "a": [
     2,
     1,
     3,
     4
    ]
   },
   "hl": {
    "a": [
     2,
     3
    ]
   },
   "out": "",
   "note": "j++ 变成 2。比较 a[2] = 3 和 a[3] = 1：3 > 1，前面大，交换！ 这一轮结束：数组是 [2, 1, 3, 4]，最大的 3 已经“冒”到了位置 3。"
  },
  {
   "line": 3,
   "vars": {
    "n": 4,
    "i": 3
   },
   "arrays": {
    "a": [
     2,
     1,
     3,
     4
    ]
   },
   "hl": {},
   "out": "",
   "note": "第 3 轮开始（i = 3）。这一轮只需要比较前 2 个位置，因为后面 2 个已经排好了。"
  },
  {
   "line": 5,
   "vars": {
    "n": 4,
    "i": 3,
    "j": 1
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
    "a": [
     1,
     2
    ]
   },
   "out": "",
   "note": "内层 j 从 1 开始。比较 a[1] = 2 和 a[2] = 1：2 > 1，前面大，交换！ 这一轮结束：数组是 [1, 2, 3, 4]，最大的 2 已经“冒”到了位置 2。"
  },
  {
   "line": 3,
   "vars": {
    "n": 4,
    "i": 4
   },
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
   "note": "i 变成 4，4 < 4 不成立，三轮结束，排序完成。"
  },
  {
   "line": 8,
   "vars": {
    "n": 4
   },
   "arrays": {
    "a": [
     1,
     2,
     3,
     4
    ]
   },
   "hl": {},
   "out": "1 2 3 4 ",
   "note": "从 a[1] 到 a[4] 输出：1 2 3 4。注意：冒泡 O(n²)，n 大了很慢，比赛里写 sort；这里只需要会读、会分析。"
  }
 ]
};
window.TRACES["ex-10-02"] = {
 "title": "结构体排序：分数高在前，同分看编号",
 "source": "struct Student { string name; int score, id; };\nbool cmp(Student a, Student b) {\n    if (a.score != b.score)\n        return a.score > b.score;   // 分数高的在前\n    return a.id < b.id;             // 同分：id 小的在前\n}\n",
 "harness": "#include <iostream>\n#include <string>\n#include <algorithm>\nusing namespace std;\n%SRC%\nStudent stu[10];\nint main() {\n    string nm[4] = {\"Tom\", \"Amy\", \"Bob\", \"Lily\"};\n    int sc[4] = {90, 95, 90, 80};\n    for (int i = 1; i <= 4; i++) { stu[i].name = nm[i - 1]; stu[i].score = sc[i - 1]; stu[i].id = i; }\n    sort(stu + 1, stu + 5, cmp);\n    for (int i = 1; i <= 4; i++) cout << stu[i].name << \" \" << stu[i].score << \"\\n\";\n    return 0;\n}\n",
 "input": "",
 "expectOutput": "Amy 95\nTom 90\nBob 90\nLily 80",
 "kind": "normal",
 "base": {
  "stu": 1
 },
 "cols": {
  "stu": [
   "name",
   "score",
   "id"
  ]
 },
 "steps": [
  {
   "line": 1,
   "vars": {},
   "arrays": {
    "stu": [
     [
      "Tom",
      90,
      1
     ],
     [
      "Amy",
      95,
      2
     ],
     [
      "Bob",
      90,
      3
     ],
     [
      "Lily",
      80,
      4
     ]
    ]
   },
   "hl": {
    "stu": []
   },
   "out": "",
   "note": "每个学生是一条“记录”：名字、分数、编号 id（输入顺序）。结构体把它们捆在一起，排序时整条一起移动，不会拆散。"
  },
  {
   "line": 2,
   "vars": {},
   "arrays": {
    "stu": [
     [
      "Tom",
      90,
      1
     ],
     [
      "Amy",
      95,
      2
     ],
     [
      "Bob",
      90,
      3
     ],
     [
      "Lily",
      80,
      4
     ]
    ]
   },
   "hl": {
    "stu": []
   },
   "out": "",
   "note": "sort 会反复拿两个学生 a 和 b 来问：cmp(a, b)——“a 应该排在 b 前面吗？”返回 true 就是“应该”。sort 内部具体怎么搬动由库决定，我们只管把这个问题回答对。"
  },
  {
   "line": 4,
   "vars": {},
   "arrays": {
    "stu": [
     [
      "Tom",
      90,
      1
     ],
     [
      "Amy",
      95,
      2
     ],
     [
      "Bob",
      90,
      3
     ],
     [
      "Lily",
      80,
      4
     ]
    ]
   },
   "hl": {
    "stu": [
     [
      2
     ],
     [
      1
     ]
    ]
   },
   "out": "",
   "note": "问：cmp(Amy, Tom)？两人分数 95 和 90 不同，由第一关键字决定：95 > 90 成立，返回 true——Amy 排在 Tom 前面。"
  },
  {
   "line": 3,
   "vars": {},
   "arrays": {
    "stu": [
     [
      "Tom",
      90,
      1
     ],
     [
      "Amy",
      95,
      2
     ],
     [
      "Bob",
      90,
      3
     ],
     [
      "Lily",
      80,
      4
     ]
    ]
   },
   "hl": {
    "stu": [
     [
      1
     ],
     [
      3
     ]
    ]
   },
   "out": "",
   "note": "再问：cmp(Tom, Bob)？两人分数都是 90，相等，第一关键字分不出胜负，不 return，继续往下走。"
  },
  {
   "line": 5,
   "vars": {},
   "arrays": {
    "stu": [
     [
      "Tom",
      90,
      1
     ],
     [
      "Amy",
      95,
      2
     ],
     [
      "Bob",
      90,
      3
     ],
     [
      "Lily",
      80,
      4
     ]
    ]
   },
   "hl": {
    "stu": [
     [
      1
     ],
     [
      3
     ]
    ]
   },
   "out": "",
   "note": "第二关键字：return a.id < b.id，即 1 < 3 成立，返回 true——Tom 的编号小，排在 Bob 前面。分数相同时，按输入顺序。"
  },
  {
   "line": 0,
   "vars": {},
   "arrays": {
    "stu": [
     [
      "Amy",
      95,
      2
     ],
     [
      "Tom",
      90,
      1
     ],
     [
      "Bob",
      90,
      3
     ],
     [
      "Lily",
      80,
      4
     ]
    ]
   },
   "hl": {
    "stu": []
   },
   "out": "Amy 95\nTom 90\nBob 90\nLily 80\n",
   "note": "排好了：分数从高到低；Tom 和 Bob 同分，按 id 小的在前。如果没有第二关键字，sort 不保证同分的人保持原来的先后。"
  }
 ]
};
