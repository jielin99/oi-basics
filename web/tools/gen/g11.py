import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mdpage import *

PRE = "#include <vector>\n#include <stack>\n#include <queue>\n#include <map>\n#include <set>\n"
H = INC + PRE + "int main() {\n%SRC%\n    return 0;\n}\n"
T = []

# ---- ex-11-01 vector ----
t = Trace("ex-11-01", "vector：会自己变长的数组",
          "vector<int> v;\nv.push_back(3);\nv.push_back(5);\nv.push_back(1);\ncout << v.size() << \" \" << v[0];\nv.pop_back();\ncout << \" \" << v.size();\n", H)
v = []
t.step(1, "v 是一个空的 vector，里面一个元素都没有。和普通数组不同，它不用提前规定大小。", arrays={"v": v})
v.append(3); t.step(2, "push_back(3)：在末尾追加一个元素（像 Python 的 append）。", arrays={"v": v}, hl={"v": 0})
v.append(5); t.step(3, "再追加 5。", arrays={"v": v}, hl={"v": 1})
v.append(1); t.step(4, "再追加 1。现在 v = {3, 5, 1}。", arrays={"v": v}, hl={"v": 2})
t.say("3 3"); t.step(5, "v.size() 是元素个数 3；v[0] 是第一个元素 3。下标从 0 开始，同样不检查越界！", arrays={"v": v}, hl={"v": 0})
v.pop(); t.step(6, "pop_back()：删除末尾的元素，v 变成 {3, 5}。", arrays={"v": v})
t.say(" 2"); t.step(7, "size 变成 2。", arrays={"v": v})
T.append(t)

# ---- ex-11-02 stack ----
t = Trace("ex-11-02", "stack（栈）：后进先出，像一摞盘子",
          "stack<int> st;\nst.push(1);\nst.push(2);\nst.push(3);\ncout << st.top() << \" \";\nst.pop();\nwhile (!st.empty()) {\n    cout << st.top() << \" \";\n    st.pop();\n}\n", H)
st = []
t.step(1, "空栈。图里左边是栈底，右边是栈顶：只能在栈顶放、在栈顶拿。", arrays={"st": st})
for k, line in ((1, 2), (2, 3), (3, 4)):
    st.append(k); t.step(line, "push(%d)：放到栈顶。" % k, arrays={"st": st}, hl={"st": len(st) - 1})
t.say("3 "); t.step(5, "top() 只“看”栈顶，是 3，不会拿走它。", arrays={"st": st}, hl={"st": len(st) - 1})
st.pop(); t.step(6, "pop() 把栈顶的 3 弹出。注意：pop() 没有返回值，要先 top() 看了值，再 pop()。", arrays={"st": st})
while st:
    t.step(7, "栈不空，继续。", arrays={"st": st}, hl={"st": len(st) - 1})
    t.say("%d " % st[-1]); t.step(8, "看栈顶：%d。" % st[-1], arrays={"st": st}, hl={"st": len(st) - 1})
    x = st.pop(); t.step(9, "弹出 %d。" % x, arrays={"st": st})
t.step(7, "栈空了，循环结束。后放进去的先出来：3 2 1，和放进去的顺序正好相反。", arrays={"st": st})
T.append(t)

# ---- ex-11-03 queue ----
t = Trace("ex-11-03", "queue（队列）：先进先出，像排队",
          "queue<int> q;\nq.push(1);\nq.push(2);\nq.push(3);\ncout << q.front() << \" \";\nq.pop();\ncout << q.front() << \" \" << q.back();\n", H)
q = []
t.step(1, "空队列。左边是队头，右边是队尾：从队尾进，从队头出。", arrays={"q": q})
for k, line in ((1, 2), (2, 3), (3, 4)):
    q.append(k); t.step(line, "push(%d)：排到队尾。" % k, arrays={"q": q}, hl={"q": len(q) - 1})
t.say("1 "); t.step(5, "front() 看队头，是最先来的 1。", arrays={"q": q}, hl={"q": 0})
q.pop(0); t.step(6, "pop()：队头的 1 出队。", arrays={"q": q})
t.say("2 3"); t.step(7, "现在队头是 2，队尾是 3。队列以后最重要的用途是 BFS（广度优先搜索）。", arrays={"q": q}, hl={"q": [0, 1]})
T.append(t)

# ---- ex-11-04 map：访问不存在的 key 会自动创建 ----
t = Trace("ex-11-04", "map：score[\"Bob\"] 会悄悄创建一个 Bob",
          "map<string, int> score;\nscore[\"Tom\"] = 90;\nscore[\"Amy\"] = 95;\ncout << score[\"Bob\"] << \" \";\ncout << score.size() << \" \";\nif (score.count(\"Eve\")) cout << \"has Eve \";\ncout << score.size();\n",
          H, base={"score": 1}, cols={"score": ["key", "value"]})
m = {}
tbl = lambda: [[k, m[k]] for k in sorted(m)]
t.step(1, "map 是“键值对”：每行是 key → value，自动按 key 从小到大排好。现在是空的。", arrays={"score": [["", ""]]} if False else {})
m["Tom"] = 90; t.step(2, "score[\"Tom\"] = 90：Tom 不存在，创建一行。", arrays={"score": tbl()}, hl={"score": [[1]]})
m["Amy"] = 95; t.step(3, "score[\"Amy\"] = 95：按 key 排序，Amy 排在 Tom 前面。", arrays={"score": tbl()}, hl={"score": [[1]]})
m["Bob"] = 0; t.say("0 "); t.step(4, "读 score[\"Bob\"]：Bob 不存在，C++ 会自动创建它，值为 0，然后才把 0 读出来！这是个坑。", arrays={"score": tbl()}, hl={"score": [[2]]})
t.say("3 "); t.step(5, "所以现在 size 是 3，而不是 2。", arrays={"score": tbl()})
t.step(6, "score.count(\"Eve\") 只检查在不在，不会创建，返回 0（假）。判断 key 是否存在，要用 count，不要用 [ ]。", arrays={"score": tbl()})
t.say("3"); t.step(7, "size 仍然是 3。", arrays={"score": tbl()})
T.append(t)

# ---- ex-11-05 set：自动排序、去重 ----
t = Trace("ex-11-05", "set：自动排序、自动去重",
          "set<int> s;\ns.insert(5);\ns.insert(1);\ns.insert(5);\ns.insert(3);\ncout << s.size() << \": \";\nfor (int x : s) cout << x << \" \";\n", H)
s = set()
t.step(1, "空集合。", arrays={"s": []})
for v_, line in ((5, 2), (1, 3), (5, 4), (3, 5)):
    had = v_ in s; s.add(v_)
    t.step(line, ("insert(%d)：已经有 %d 了，集合里不会出现重复，什么都没变。" % (v_, v_)) if had else ("insert(%d)：放进集合，并且自动按从小到大排好。" % v_),
           arrays={"s": sorted(s)}, hl={"s": sorted(s).index(v_)})
t.say("3: "); t.step(6, "size 是 3：5 只算一个。", arrays={"s": sorted(s)})
for x in sorted(s): t.say("%d " % x)
t.step(7, "遍历 set，按从小到大输出：1 3 5。", arrays={"s": sorted(s)})
T.append(t)

write_traces("stl-11.js", T)

# ---------------- 小测 ----------------
assert compile_fails("int main() { stack<int> st; st.push(1); int x = st.pop(); return 0; }", pre=PRE)
q_pop = quiz("想取出栈顶的值并弹出，st.pop() 会返回那个值吗？int x = st.pop(); 对吗？",
    ["对，pop 返回被弹出的值", "不对：pop 没有返回值，要先 int x = st.top(); 再 st.pop();", "对，但只对 int 栈有效"], 1,
    "pop() 只负责弹出，不返回值（我们真实编译过 int x = st.pop();，会报错）。顺序是先 top() 取值，再 pop()。")
q_empty = quiz("对空的栈调用 st.top() 会怎样？",
    ["返回 0", "行为没有保证：常见是程序崩溃（RE），也可能读到错的值继续算下去", "编译不通过"], 1,
    "不要赌它会怎样：用 top()、front()、pop() 之前先判断 empty()。")
q_map = predict_quiz("预测输出：用 m[key] 判断“是否存在”，会有什么副作用？",
    "map<int, int> m;\nif (m[5] == 0) cout << \"no \";\ncout << m.size();", ["no 0", "0", "no"], "m[5] 访问不存在的 key 时会自动创建它（值为 0），所以 size 变成 1。要判断是否存在，用 m.count(5)。输出 {real}。", pre=PRE)
q_vec = quiz("vector 用 [] 访问，下标越界会被自动检查吗？",
    ["会，越界会报错", "不会，和普通数组一样不检查，后果也一样危险", "只有 push_back 之后才检查"], 1, "v[i] 不检查越界，和数组一样。size() 是多少，合法下标就是 0 到 size() - 1。")
q_auto = quiz("遍历 map 时，想写 for (auto [k, v] : mp)，在本课程约定的 C++ 标准下行吗？",
    ["行，这是最简洁的写法", "不行：这是 C++17 的语法，本课程只用 C++11 就有的写法，要写 it.first / it.second", "只在 Dev-C++ 里不行"], 1,
    "考场环境不一定支持新标准。写 for (auto it : mp) 然后用 it.first、it.second。")
q_pq = predict_quiz("预测输出：priority_queue 每次取出的是最大的：",
    "priority_queue<int> pq;\npq.push(3); pq.push(10); pq.push(5);\ncout << pq.top() << \" \";\npq.pop();\ncout << pq.top();", ["3 5", "10 3", "5 10"], "优先队列每次取最大的，和放进去的顺序无关：先是 10，弹出后剩下 3 和 5，最大的是 5。输出 {real}。（想每次取最小的：priority_queue<int, vector<int>, greater<int>>。）", pre=PRE)
q_pair = predict_quiz("预测输出：pair 排序，默认先比 first，再比 second：",
    "vector<pair<int,int>> p;\np.push_back({2, 1});\np.push_back({1, 5});\np.push_back({1, 2});\nsort(p.begin(), p.end());\nfor (int i = 0; i < 3; i++) cout << p[i].first << \"-\" << p[i].second << \" \";", ["2-1 1-2 1-5", "1-5 1-2 2-1", "1-5 2-1 1-2"], "先按 first 从小到大，first 相同再按 second 从小到大。输出 {real}。", pre=PRE)

inserts = {
    "2.1": [("trace", "ex-11-01"), ("quiz", q_vec)],
    "2.2": [("quiz", q_pair)],
    "2.3": [("trace", "ex-11-02"), ("quiz", q_pop), ("quiz", q_empty)],
    "2.4": [("trace", "ex-11-03")],
    "2.5": [("quiz", q_pq)],
    "2.6": [("trace", "ex-11-04"), ("quiz", q_map), ("quiz", q_auto)],
    "2.7": [("trace", "ex-11-05")],
}
tasks = (["把 map 的例子敲一遍，把 <code>score[\"Bob\"]</code> 那一行换成 <code>score.count(\"Bob\")</code>，看最后 size 是几。",
              "用 stack 实现括号匹配（md 里有完整代码）：输入 <code>(()())</code> 和 <code>(()</code>，看看输出。"], "")
path, nq = build_lesson('11-STL入门.md', '11-stl.html', '第11课｜STL', '11', inserts, ['stl-11.js'], tasks)
print("第11课: %d 道小测（正文全文 + 互动）" % nq)
