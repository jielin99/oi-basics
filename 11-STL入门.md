# 第 11 课 STL 入门：比赛工具箱

> 预计用时：1.5~2 周
> 本课目标：会用 `vector`、`pair`、`stack`、`queue`、`priority_queue`、`map`、`set`；知道每种容器适合解决什么问题。

STL（Standard Template Library，标准模板库）是 C++ 自带的一套现成的数据结构和算法。学会它，很多题目能少写一大半代码。

---

## 1. 从 Python 说起

| 需要的功能 | Python | C++ STL |
|---|---|---|
| 可变长度列表 | `list` | `vector` |
| 二元组 | `(a, b)` | `pair<int,int>` |
| 栈 | `list` 的 `append`/`pop` | `stack` |
| 队列 | `collections.deque` | `queue` |
| 优先队列（堆） | `heapq` | `priority_queue` |
| 字典 | `dict` | `map`（**自动按 key 排序**） |
| 集合 | `set` | `set`（**自动排序、去重**） |

> 💡 Python 的 dict / set 是“无序的”，而 C++ 的 `map` / `set` **自动有序**——这是很大的优势。C++ 也有无序版本 `unordered_map` / `unordered_set`，速度更快但不排序。

---

## 2. 知识点

### 2.1 `vector`：可变长数组

```cpp
#include <vector>
vector<int> v;              // 空的 int 数组
vector<int> w(10);          // 10 个元素，全是 0
vector<int> u(10, -1);      // 10 个元素，全是 -1

v.push_back(3);             // 末尾追加，类似 append
v.push_back(5);
v.push_back(1);             // v = {3, 5, 1}
cout << v.size() << "\n";   // 3
cout << v[0] << "\n";       // 3，下标从 0 开始，同样不检查越界！
v.pop_back();               // 删除末尾 → {3, 5}
v.clear();                  // 清空
bool e = v.empty();         // 是否为空

sort(v.begin(), v.end());   // 排序
for (int x : v) cout << x << " ";   // 遍历
```

**二维 vector / 邻接表**（以后学图论必用）：

```cpp
vector<int> g[100010];      // 10 万个 vector，g[u] 存和 u 相连的点
g[1].push_back(2);
g[1].push_back(3);
for (int v : g[1]) ...      // 遍历 1 的所有邻居
```

### 2.2 `pair`：把两个值打包

```cpp
pair<int, int> p = {3, 5};          // 或 make_pair(3, 5)
cout << p.first << " " << p.second << "\n";

vector<pair<int,int>> pts;
pts.push_back({1, 2});
sort(pts.begin(), pts.end());       // 默认先按 first 升序，再按 second 升序
```

只有两个字段时，用 `pair` 比写结构体更省事。

### 2.3 `stack`：栈（后进先出）

像一摞盘子：只能从顶部放、从顶部拿。

```cpp
#include <stack>
stack<int> st;
st.push(1);  st.push(2);  st.push(3);   // 栈底 1 2 3 栈顶
cout << st.top() << "\n";               // 3（看栈顶）
st.pop();                               // 弹出 3（pop 没有返回值！）
cout << st.size() << "\n";              // 2
while (!st.empty()) {
    cout << st.top() << " ";            // 2 1
    st.pop();
}
```

**典型应用：括号匹配**

```cpp
bool check(string s) {
    stack<char> st;
    for (char c : s) {
        if (c == '(') st.push(c);
        else if (c == ')') {
            if (st.empty()) return false;   // 右括号多了
            st.pop();
        }
    }
    return st.empty();                       // 左括号不能剩
}
```

### 2.4 `queue`：队列（先进先出）

像排队：从队尾进，从队头出。

```cpp
#include <queue>
queue<int> q;
q.push(1);  q.push(2);  q.push(3);      // 队头 1 2 3 队尾
cout << q.front() << "\n";              // 1（看队头）
q.pop();                                // 1 出队
cout << q.front() << " " << q.back() << "\n";   // 2 3
```

**典型应用：约瑟夫问题**（n 个人围成圈，报数到 m 的出列）

```cpp
queue<int> q;
for (int i = 1; i <= n; i++) q.push(i);
while (!q.empty()) {
    for (int k = 1; k < m; k++) {       // 前 m-1 个人移到队尾
        q.push(q.front());
        q.pop();
    }
    cout << q.front() << " ";           // 第 m 个人出列
    q.pop();
}
```

队列以后最重要的用途是 **BFS（广度优先搜索）**。

### 2.5 `priority_queue`：优先队列（堆）

每次取出的都是**最大**的元素。

```cpp
priority_queue<int> pq;                               // 大根堆
pq.push(3); pq.push(10); pq.push(5);
cout << pq.top() << "\n";                             // 10
pq.pop();

priority_queue<int, vector<int>, greater<int>> mq;    // 小根堆：每次取最小
```

**典型应用：合并果子**（每次取两个最小的合并，经典贪心）。

### 2.6 `map`：键值对（字典）

```cpp
#include <map>
map<string, int> score;
score["Tom"] = 90;
score["Amy"] = 95;
score["Tom"] += 5;                       // Tom → 95

cout << score["Amy"] << "\n";            // 95
cout << score["Bob"] << "\n";            // 0 ⚠️ 访问不存在的 key 会自动创建它，值为 0
if (score.count("Bob")) ...              // 判断 key 是否存在，不会创建

for (auto it : score) {                  // 按 key 从小到大遍历
    cout << it.first << " " << it.second << "\n";
}
```

**典型应用：统计每个单词出现的次数**

```cpp
map<string, int> cnt;
string w;
while (cin >> w) cnt[w]++;
```

当数值范围太大（比如 10⁹）没法开桶数组时，用 `map` 当“桶”。

### 2.7 `set`：集合（自动排序、去重）

```cpp
#include <set>
set<int> s;
s.insert(5); s.insert(1); s.insert(5); s.insert(3);   // s = {1, 3, 5}
cout << s.size() << "\n";            // 3
if (s.count(3)) cout << "has 3\n";
s.erase(3);
for (int x : s) cout << x << " ";    // 1 5（自动从小到大）
```

### 2.8 复杂度速记

| 容器 | 插入 | 删除 | 查找 | 适合 |
|---|---|---|---|---|
| `vector` | 尾部 O(1) | 尾部 O(1) | 按下标 O(1) | 不定长数组 |
| `stack` / `queue` | O(1) | O(1) | 只能看顶/头 | 栈、队列、BFS |
| `priority_queue` | O(log n) | O(log n) | 只能看最大 | 反复取最值 |
| `map` / `set` | O(log n) | O(log n) | O(log n) | 有序、去重、大范围计数 |

### 2.9 其他常用算法函数（`<algorithm>`）

```cpp
reverse(a + 1, a + n + 1);                 // 反转
int mx = *max_element(a + 1, a + n + 1);   // 最大值
int m = unique(a + 1, a + n + 1) - (a + 1);  // 排序后去重，返回去重后的个数
// 二分查找（数组必须已排序）
int pos = lower_bound(a + 1, a + n + 1, x) - a;   // 第一个 >= x 的位置
```

---

## 3. ⚠️ 易错点

1. `st.pop()` / `q.pop()` 没有返回值，要先 `top()` / `front()` 取值再 `pop()`。
2. 对空的栈/队列调用 `top()` / `front()` / `pop()` → RE。先判断 `empty()`。
3. 用 `map[key]` 判断是否存在 → 会自动插入，用 `count`。
4. `vector` 下标越界同样不报错。
5. 在 C++14 下不能写 `for (auto [k, v] : mp)`（这是 C++17 语法），用 `it.first` / `it.second`。

---

## 4. 课堂练习

**练习 11-1**：输入若干个整数（个数未知），存入 vector，排序后输出。

**练习 11-2**：输入一串只含 `()[]` 的括号，判断是否匹配。

**练习 11-3**：输入 n 个整数（范围到 10⁹），输出出现次数最多的数（多个时输出最小的）。

**练习 11-4**：用 set 实现：输入 n 个数，输出去重后的个数和去重后的序列。

<details>
<summary>点击查看参考答案</summary>

```cpp
// 11-2
#include <iostream>
#include <stack>
#include <string>
using namespace std;
int main() {
    string s;
    cin >> s;
    stack<char> st;
    bool ok = true;
    for (char c : s) {
        if (c == '(' || c == '[') st.push(c);
        else {
            char need = (c == ')') ? '(' : '[';
            if (st.empty() || st.top() != need) { ok = false; break; }
            st.pop();
        }
    }
    if (!st.empty()) ok = false;
    cout << (ok ? "OK" : "Wrong") << "\n";
    return 0;
}
```

```cpp
// 11-3
#include <iostream>
#include <map>
using namespace std;
int main() {
    int n;
    cin >> n;
    map<int, int> cnt;
    for (int i = 1; i <= n; i++) {
        int x; cin >> x;
        cnt[x]++;
    }
    int best = 0, bestCnt = 0;
    for (auto it : cnt) {             // map 按 key 从小到大，所以 > 而不是 >=
        if (it.second > bestCnt) {
            bestCnt = it.second;
            best = it.first;
        }
    }
    cout << best << "\n";
    return 0;
}
```

</details>

---

## 5. 课后刷题（洛谷）

| 题号 | 题名 | 要点 | 级别 |
|---|---|---|---|
| P3156 | 【深基15.例1】询问学号 | vector 基本 | 必做 |
| P1739 | 表达式括号匹配 | stack | 必做 |
| P1996 | 约瑟夫问题 | queue | 必做 |
| P1540 | [NOIP 2010 提高组] 机器翻译 | queue + 标记数组 | 必做 |
| P1090 | [NOIP 2004 提高组] 合并果子 | priority_queue | 必做 |
| P5250 | 【深基17.例5】木材仓库 | set | 必做 |
| P5266 | 【深基17.例6】学籍管理 | map | 必做 |
| P1918 | 保龄球 | map | 选做 |
| P4387 | 【深基15.习9】验证栈序列 | stack 模拟 | 挑战 |
| P1449 | 后缀表达式 | stack 应用 | 挑战 |

> 洛谷题单：【数据结构1-1】线性表、【数据结构1-2】二叉树（暂不做）、【数据结构1-3】集合

---

## ✅ 自查清单

- [ ] 我会用 vector 的 push_back、size、下标、sort
- [ ] 我会用 pair，知道它的默认排序规则
- [ ] 我能说出栈和队列的区别，并各举一个应用
- [ ] 我知道 priority_queue 默认取最大，会写小根堆
- [ ] 我知道 map[key] 会自动插入，判断存在用 count
- [ ] 我知道 set 自动排序去重
