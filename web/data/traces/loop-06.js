window.TRACES = window.TRACES || {};
/* 由 tools/gen 生成；最终输出由 verify-traces 真实编译比对。 */
window.TRACES["ex-06-01"] = {
 "title": "break 和 continue：跳过、提前结束",
 "source": "for (int i = 1; i <= 10; i++) {\n    if (i % 3 == 0) continue;\n    if (i > 7) break;\n    cout << i << \" \";\n}\n",
 "harness": "#include <iostream>\n#include <cstdio>\n#include <cmath>\n#include <string>\n#include <algorithm>\nusing namespace std;\nint main() {\n%SRC%\n    return 0;\n}\n",
 "input": "",
 "expectOutput": "1 2 4 5 7",
 "kind": "normal",
 "steps": [
  {
   "line": 1,
   "vars": {
    "i": 1
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "i 从 1 开始，一圈一圈往下走。"
  },
  {
   "line": 4,
   "vars": {
    "i": 1
   },
   "arrays": {},
   "hl": {},
   "out": "1 ",
   "note": "i = 1，不是 3 的倍数，也没超过 7，输出 1。"
  },
  {
   "line": 4,
   "vars": {
    "i": 2
   },
   "arrays": {},
   "hl": {},
   "out": "1 2 ",
   "note": "i = 2，不是 3 的倍数，也没超过 7，输出 2。"
  },
  {
   "line": 2,
   "vars": {
    "i": 3
   },
   "arrays": {},
   "hl": {},
   "out": "1 2 ",
   "note": "i = 3，3 % 3 == 0 成立 → continue：跳过本圈后面的代码，直接去做 i++，进入下一圈。"
  },
  {
   "line": 4,
   "vars": {
    "i": 4
   },
   "arrays": {},
   "hl": {},
   "out": "1 2 4 ",
   "note": "i = 4，不是 3 的倍数，也没超过 7，输出 4。"
  },
  {
   "line": 4,
   "vars": {
    "i": 5
   },
   "arrays": {},
   "hl": {},
   "out": "1 2 4 5 ",
   "note": "i = 5，不是 3 的倍数，也没超过 7，输出 5。"
  },
  {
   "line": 2,
   "vars": {
    "i": 6
   },
   "arrays": {},
   "hl": {},
   "out": "1 2 4 5 ",
   "note": "i = 6，6 % 3 == 0 成立 → continue：跳过本圈后面的代码，直接去做 i++，进入下一圈。"
  },
  {
   "line": 4,
   "vars": {
    "i": 7
   },
   "arrays": {},
   "hl": {},
   "out": "1 2 4 5 7 ",
   "note": "i = 7，不是 3 的倍数，也没超过 7，输出 7。"
  },
  {
   "line": 3,
   "vars": {
    "i": 8
   },
   "arrays": {},
   "hl": {},
   "out": "1 2 4 5 7 ",
   "note": "i = 8，8 > 7 成立 → break：整个循环立刻结束，不再回去判断。"
  }
 ]
};
window.TRACES["ex-06-02"] = {
 "title": "拆数位：用 % 10 和 / 10",
 "source": "int n = 123, digitSum = 0, rev = 0;\nwhile (n > 0) {\n    int d = n % 10;\n    digitSum += d;\n    rev = rev * 10 + d;\n    n /= 10;\n}\ncout << digitSum << \" \" << rev;\n",
 "harness": "#include <iostream>\n#include <cstdio>\n#include <cmath>\n#include <string>\n#include <algorithm>\nusing namespace std;\nint main() {\n%SRC%\n    return 0;\n}\n",
 "input": "",
 "expectOutput": "6 321",
 "kind": "normal",
 "steps": [
  {
   "line": 1,
   "vars": {
    "n": 123,
    "digitSum": 0,
    "rev": 0
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "n = 123 是要拆的数；digitSum 记数位之和，rev 记反转后的数，都先清 0。"
  },
  {
   "line": 3,
   "vars": {
    "n": 123,
    "digitSum": 0,
    "rev": 0,
    "d": 3
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "while (n > 0) 成立。d = 123 % 10 = 3：取出个位。"
  },
  {
   "line": 4,
   "vars": {
    "n": 123,
    "digitSum": 3,
    "rev": 0,
    "d": 3
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "digitSum += d，变成 3。"
  },
  {
   "line": 5,
   "vars": {
    "n": 123,
    "digitSum": 3,
    "rev": 3,
    "d": 3
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "rev = rev * 10 + d：把 rev 左移一位再接上 d，变成 3。"
  },
  {
   "line": 6,
   "vars": {
    "n": 12,
    "digitSum": 3,
    "rev": 3
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "n /= 10：去掉个位，n 变成 12。"
  },
  {
   "line": 3,
   "vars": {
    "n": 12,
    "digitSum": 3,
    "rev": 3,
    "d": 2
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "while (n > 0) 成立。d = 12 % 10 = 2：取出个位。"
  },
  {
   "line": 4,
   "vars": {
    "n": 12,
    "digitSum": 5,
    "rev": 3,
    "d": 2
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "digitSum += d，变成 5。"
  },
  {
   "line": 5,
   "vars": {
    "n": 12,
    "digitSum": 5,
    "rev": 32,
    "d": 2
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "rev = rev * 10 + d：把 rev 左移一位再接上 d，变成 32。"
  },
  {
   "line": 6,
   "vars": {
    "n": 1,
    "digitSum": 5,
    "rev": 32
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "n /= 10：去掉个位，n 变成 1。"
  },
  {
   "line": 3,
   "vars": {
    "n": 1,
    "digitSum": 5,
    "rev": 32,
    "d": 1
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "while (n > 0) 成立。d = 1 % 10 = 1：取出个位。"
  },
  {
   "line": 4,
   "vars": {
    "n": 1,
    "digitSum": 6,
    "rev": 32,
    "d": 1
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "digitSum += d，变成 6。"
  },
  {
   "line": 5,
   "vars": {
    "n": 1,
    "digitSum": 6,
    "rev": 321,
    "d": 1
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "rev = rev * 10 + d：把 rev 左移一位再接上 d，变成 321。"
  },
  {
   "line": 6,
   "vars": {
    "n": 0,
    "digitSum": 6,
    "rev": 321
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "n /= 10：去掉个位，n 变成 0。"
  },
  {
   "line": 2,
   "vars": {
    "n": 0,
    "digitSum": 6,
    "rev": 321
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "n = 0，0 > 0 不成立，循环结束。"
  },
  {
   "line": 8,
   "vars": {
    "n": 0,
    "digitSum": 6,
    "rev": 321
   },
   "arrays": {},
   "hl": {},
   "out": "6 321",
   "note": "输出数位之和 6 和反转数 321。"
  }
 ]
};
window.TRACES["ex-06-03a"] = {
 "title": "判断质数：只试到 √n（n = 7）",
 "source": "int n = 7;\nbool isPrime = true;\nfor (int i = 2; i <= n / i; i++) {\n    if (n % i == 0) {\n        isPrime = false;\n        break;\n    }\n}\ncout << (isPrime ? \"prime\" : \"not prime\");\n",
 "harness": "#include <iostream>\n#include <cstdio>\n#include <cmath>\n#include <string>\n#include <algorithm>\nusing namespace std;\nint main() {\n%SRC%\n    return 0;\n}\n",
 "input": "",
 "expectOutput": "prime",
 "kind": "normal",
 "steps": [
  {
   "line": 1,
   "vars": {
    "n": 7
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "要判断 n = 7 是不是质数。"
  },
  {
   "line": 2,
   "vars": {
    "n": 7,
    "isPrime": "true"
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "先假设它是质数。"
  },
  {
   "line": 3,
   "vars": {
    "n": 7,
    "isPrime": "true",
    "i": 2
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "i = 2，n / i = 3，2 <= 3 成立，进入循环体。（i <= n / i 就是 i×i <= n：只试到 √n）"
  },
  {
   "line": 4,
   "vars": {
    "n": 7,
    "isPrime": "true",
    "i": 2
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "7 % 2 = 1，不等于 0，不能整除，继续试下一个。"
  },
  {
   "line": 3,
   "vars": {
    "n": 7,
    "isPrime": "true",
    "i": 3
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "i = 3，n / i = 2，3 <= 2 不成立，循环结束：√n 以内没有因数。"
  },
  {
   "line": 9,
   "vars": {
    "n": 7,
    "isPrime": "true"
   },
   "arrays": {},
   "hl": {},
   "out": "prime",
   "note": "输出 prime。"
  }
 ]
};
window.TRACES["ex-06-03b"] = {
 "title": "判断质数：只试到 √n（n = 15）",
 "source": "int n = 15;\nbool isPrime = true;\nfor (int i = 2; i <= n / i; i++) {\n    if (n % i == 0) {\n        isPrime = false;\n        break;\n    }\n}\ncout << (isPrime ? \"prime\" : \"not prime\");\n",
 "harness": "#include <iostream>\n#include <cstdio>\n#include <cmath>\n#include <string>\n#include <algorithm>\nusing namespace std;\nint main() {\n%SRC%\n    return 0;\n}\n",
 "input": "",
 "expectOutput": "not prime",
 "kind": "normal",
 "steps": [
  {
   "line": 1,
   "vars": {
    "n": 15
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "要判断 n = 15 是不是质数。"
  },
  {
   "line": 2,
   "vars": {
    "n": 15,
    "isPrime": "true"
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "先假设它是质数。"
  },
  {
   "line": 3,
   "vars": {
    "n": 15,
    "isPrime": "true",
    "i": 2
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "i = 2，n / i = 7，2 <= 7 成立，进入循环体。（i <= n / i 就是 i×i <= n：只试到 √n）"
  },
  {
   "line": 4,
   "vars": {
    "n": 15,
    "isPrime": "true",
    "i": 2
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "15 % 2 = 1，不等于 0，不能整除，继续试下一个。"
  },
  {
   "line": 3,
   "vars": {
    "n": 15,
    "isPrime": "true",
    "i": 3
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "i = 3，n / i = 5，3 <= 5 成立，进入循环体。（i <= n / i 就是 i×i <= n：只试到 √n）"
  },
  {
   "line": 4,
   "vars": {
    "n": 15,
    "isPrime": "true",
    "i": 3
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "15 % 3 == 0 成立：15 能被 3 整除！"
  },
  {
   "line": 5,
   "vars": {
    "n": 15,
    "isPrime": "false",
    "i": 3
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "isPrime = false：它不是质数。"
  },
  {
   "line": 6,
   "vars": {
    "n": 15,
    "isPrime": "false",
    "i": 3
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "break：已经找到因数，没必要再试了，直接跳出循环。"
  },
  {
   "line": 9,
   "vars": {
    "n": 15,
    "isPrime": "false"
   },
   "arrays": {},
   "hl": {},
   "out": "not prime",
   "note": "输出 not prime。"
  }
 ]
};
window.TRACES["ex-06-04"] = {
 "title": "嵌套循环：打印 3 行直角三角形",
 "source": "for (int i = 1; i <= 3; i++) {\n    for (int j = 1; j <= i; j++) {\n        cout << \"*\";\n    }\n    cout << \"\\n\";\n}\n",
 "harness": "#include <iostream>\n#include <cstdio>\n#include <cmath>\n#include <string>\n#include <algorithm>\nusing namespace std;\nint main() {\n%SRC%\n    return 0;\n}\n",
 "input": "",
 "expectOutput": "*\n**\n***",
 "kind": "normal",
 "steps": [
  {
   "line": 1,
   "vars": {
    "i": 1
   },
   "arrays": {},
   "hl": {},
   "out": "",
   "note": "外层 i = 1：开始打印第 1 行。外层管“第几行”。"
  },
  {
   "line": 3,
   "vars": {
    "i": 1,
    "j": 1
   },
   "arrays": {},
   "hl": {},
   "out": "*",
   "note": "内层 j 从 1 开始，j <= 1 成立，输出一个 *。内层管“这一行打印什么”。"
  },
  {
   "line": 5,
   "vars": {
    "i": 1
   },
   "arrays": {},
   "hl": {},
   "out": "*\n",
   "note": "j 变成 2，2 <= 1 不成立，这一行打完了，换行。第 1 行共 1 个 *，所以内层上限是 i。"
  },
  {
   "line": 1,
   "vars": {
    "i": 2
   },
   "arrays": {},
   "hl": {},
   "out": "*\n",
   "note": "外层 i = 2：开始打印第 2 行。外层管“第几行”。"
  },
  {
   "line": 3,
   "vars": {
    "i": 2,
    "j": 1
   },
   "arrays": {},
   "hl": {},
   "out": "*\n*",
   "note": "内层 j 从 1 开始，j <= 2 成立，输出一个 *。内层管“这一行打印什么”。"
  },
  {
   "line": 3,
   "vars": {
    "i": 2,
    "j": 2
   },
   "arrays": {},
   "hl": {},
   "out": "*\n**",
   "note": "j++ 变成 2，j <= 2 成立，输出一个 *。内层管“这一行打印什么”。"
  },
  {
   "line": 5,
   "vars": {
    "i": 2
   },
   "arrays": {},
   "hl": {},
   "out": "*\n**\n",
   "note": "j 变成 3，3 <= 2 不成立，这一行打完了，换行。第 2 行共 2 个 *，所以内层上限是 i。"
  },
  {
   "line": 1,
   "vars": {
    "i": 3
   },
   "arrays": {},
   "hl": {},
   "out": "*\n**\n",
   "note": "外层 i = 3：开始打印第 3 行。外层管“第几行”。"
  },
  {
   "line": 3,
   "vars": {
    "i": 3,
    "j": 1
   },
   "arrays": {},
   "hl": {},
   "out": "*\n**\n*",
   "note": "内层 j 从 1 开始，j <= 3 成立，输出一个 *。内层管“这一行打印什么”。"
  },
  {
   "line": 3,
   "vars": {
    "i": 3,
    "j": 2
   },
   "arrays": {},
   "hl": {},
   "out": "*\n**\n**",
   "note": "j++ 变成 2，j <= 3 成立，输出一个 *。内层管“这一行打印什么”。"
  },
  {
   "line": 3,
   "vars": {
    "i": 3,
    "j": 3
   },
   "arrays": {},
   "hl": {},
   "out": "*\n**\n***",
   "note": "j++ 变成 3，j <= 3 成立，输出一个 *。内层管“这一行打印什么”。"
  },
  {
   "line": 5,
   "vars": {
    "i": 3
   },
   "arrays": {},
   "hl": {},
   "out": "*\n**\n***\n",
   "note": "j 变成 4，4 <= 3 不成立，这一行打完了，换行。第 3 行共 3 个 *，所以内层上限是 i。"
  },
  {
   "line": 1,
   "vars": {
    "i": 4
   },
   "arrays": {},
   "hl": {},
   "out": "*\n**\n***\n",
   "note": "i 变成 4，4 <= 3 不成立，整个双重循环结束。"
  }
 ]
};
