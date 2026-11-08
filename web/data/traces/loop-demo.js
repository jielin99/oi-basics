window.TRACES = window.TRACES || {};
/* T1 框架验证例子：最小循环累加。状态 = 执行该行【之后】；for 拆成 初始化/判断/循环体/更新。
 * 中间状态已人工逐步核对（见 docs 的 T1 记录）。 */
window.TRACES["loop-sum"] = {
  title: "循环累加：1 + 2 + 3",
  source:
    "int s = 0;\n" +
    "for (int i = 1; i <= 3; i++) {\n" +
    "    s += i;\n" +
    "}\n" +
    "cout << s;\n",
  harness: "#include <iostream>\nusing namespace std;\nint main() {\n%SRC%\n    return 0;\n}\n",
  input: "",
  expectOutput: "6",
  kind: "normal",
  steps: [
    { line: 1, vars: { s: 0 }, out: "", note: "先准备一个盒子 s，里面放 0。" },
    { line: 2, vars: { s: 0, i: 1 }, out: "", note: "【初始化】i = 1，这一步整个循环只做一次。" },
    { line: 2, vars: { s: 0, i: 1 }, out: "", note: "【判断】i <= 3 吗？1 <= 3 成立，进入循环体。" },
    { line: 3, vars: { s: 1, i: 1 }, out: "", note: "【循环体】s += i，s 变成 0 + 1 = 1。" },
    { line: 2, vars: { s: 1, i: 2 }, out: "", note: "【更新】i++，i 变成 2。" },
    { line: 2, vars: { s: 1, i: 2 }, out: "", note: "【判断】2 <= 3 成立，再进入循环体。" },
    { line: 3, vars: { s: 3, i: 2 }, out: "", note: "【循环体】s 变成 1 + 2 = 3。" },
    { line: 2, vars: { s: 3, i: 3 }, out: "", note: "【更新】i 变成 3。" },
    { line: 2, vars: { s: 3, i: 3 }, out: "", note: "【判断】3 <= 3 成立，再进一次循环体。" },
    { line: 3, vars: { s: 6, i: 3 }, out: "", note: "【循环体】s 变成 3 + 3 = 6。" },
    { line: 2, vars: { s: 6, i: 4 }, out: "", note: "【更新】i 变成 4。" },
    { line: 2, vars: { s: 6, i: 4 }, out: "", note: "【判断】4 <= 3 不成立！循环结束，跳到 } 后面。注意：最后一次判断失败，循环体不会执行。" },
    { line: 5, vars: { s: 6 }, out: "6", note: "输出 s，屏幕上显示 6。循环结束后 i 就不存在了。" }
  ]
};
