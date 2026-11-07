# 附录 A：Python ↔ C++ 速查对照表

> 建议打印出来贴在桌边。前几周写 C++ 时“手比脑快”写出 Python 语法是正常的，对照这张表改过来。

## 程序结构

| Python | C++ |
|---|---|
| 直接从第一行开始写 | `#include <bits/stdc++.h>` + `using namespace std;` + `int main() { ... return 0; }` |
| 缩进表示代码块 | `{ }` 表示代码块 |
| 换行结束语句 | `;` 结束语句 |
| `# 注释` | `// 注释` 或 `/* 注释 */` |

## 变量与类型

| Python | C++ |
|---|---|
| `x = 5` | `int x = 5;` |
| `x = 10**12` | `long long x = 1000000000000LL;` |
| `x = 3.14` | `double x = 3.14;` |
| `c = 'a'` | `char c = 'a';`（单引号） |
| `s = "abc"` | `string s = "abc";`（双引号） |
| `ok = True` | `bool ok = true;` |
| `None` | 无对应 |
| 整数无限大 | `int` 约 ±21 亿，`long long` 约 ±9.2×10¹⁸，超了就**溢出**，运行时不会提醒，结果不可靠 |

## 运算

| Python | C++ | 注意 |
|---|---|---|
| `7 / 2` → 3.5 | `7 / 2` → **3** | 整数相除得整数 |
| `7 // 2` → 3 | `7 / 2` → 3 | |
| `-7 // 2` → -4 | `-7 / 2` → **-3** | C++ 向 0 取整 |
| `-7 % 2` → 1 | `-7 % 2` → **-1** | 余数符号随被除数 |
| `2 ** 10` | 循环相乘，或 `pow(2,10)`（返回 double） | `^` 是异或！ |
| `and` `or` `not` | `&&` `\|\|` `!` | |
| `1 < x < 10` | `1 < x && x < 10` | C++ 连写能编译但结果错 |
| `x += 1` | `x += 1;` 或 `x++;` | |
| `a, b = b, a` | `swap(a, b);` | |
| `abs(x)` | `abs(x)`（整数）/ `fabs(x)`（小数） | |
| `max(a, b, c)` | `max(max(a, b), c)` 或 `max({a, b, c})` | 参数类型必须相同 |
| `int(3.9)` → 3 | `(int)3.9` → 3 | |
| `float(7)` | `(double)7` 或 `7 * 1.0` | |

## 输入输出

| Python | C++ |
|---|---|
| `n = int(input())` | `int n; cin >> n;` |
| `a, b = map(int, input().split())` | `int a, b; cin >> a >> b;` |
| `s = input()`（整行） | `string s; getline(cin, s);` |
| `print(x)` | `cout << x << "\n";` |
| `print(a, b)` | `cout << a << " " << b << "\n";` |
| `print(x, end="")` | `cout << x;` |
| `print(f"{x:.2f}")` | `printf("%.2f\n", x);` |
| `print(f"{x:05d}")` | `printf("%05d\n", x);` |

## 分支与循环

| Python | C++ |
|---|---|
| `if x > 0:` | `if (x > 0) {` |
| `elif x == 0:` | `} else if (x == 0) {` |
| `else:` | `} else {` |
| `a if cond else b` | `cond ? a : b` |
| `for i in range(n):` | `for (int i = 0; i < n; i++) {` |
| `for i in range(1, n+1):` | `for (int i = 1; i <= n; i++) {` |
| `for i in range(n, 0, -1):` | `for (int i = n; i >= 1; i--) {` |
| `for c in s:` | `for (char c : s) {` |
| `while cond:` | `while (cond) {` |
| `pass` | `;` 或空的 `{ }` |

## 容器

| Python | C++ |
|---|---|
| `a = [0] * 100` | `int a[100] = {0};` 或全局 `int a[100];` 或 `vector<int> a(100);` |
| `a.append(x)` | `v.push_back(x);` |
| `a.pop()` | `v.pop_back();` |
| `len(a)` | `v.size()`；数组自己记 n |
| `a[-1]` | `v.back()`（v 不能为空）；数组：存在 `a[0]~a[n-1]` 时是 `a[n-1]`，存在 `a[1]~a[n]`（本课程习惯）时是 `a[n]` |
| `a.sort()` | `sort(a + 1, a + n + 1);` / `sort(v.begin(), v.end());` |
| `a.sort(reverse=True)` | `sort(..., greater<int>());` |
| `a.reverse()` | `reverse(a + 1, a + n + 1);` |
| `x in a` | `find(...)` 或用 `set`/`map` 的 `count` |
| `d = {}` | `map<string, int> d;` |
| `d[k] = v` | `d[k] = v;` |
| `k in d` | `d.count(k)` |
| `s = set()` | `set<int> s;` |
| `s.add(x)` | `s.insert(x);` |
| `(a, b)` | `pair<int,int> p = {a, b};` → `p.first`, `p.second` |

## 字符串

| Python | C++ |
|---|---|
| `len(s)` | `s.size()` |
| `s[1:4]` | `s.substr(1, 3)`（起点，长度） |
| `s.find("ab")` → 找不到 -1 | `s.find("ab")` → 找不到 `string::npos` |
| `s.upper()` | 逐个字符 `toupper(c)` |
| `s[::-1]` | `reverse(s.begin(), s.end());` |
| `str(123)` | `to_string(123)` |
| `int("123")` | `stoi("123")` |
| `ord('a')` | `(int)'a'` 或直接 `'a'` 参与运算 |
| `chr(97)` | `(char)97` |
| 字符串不可修改 | `s[0] = 'X';` 可以 |

## 函数

| Python | C++ |
|---|---|
| `def f(a, b):` | `int f(int a, int b) {` |
| 无返回值 | `void f(...) {` |
| `return a, b` | 用引用参数 `void f(int &a, int &b)` 或返回 `pair` / 结构体 |
| 改列表参数会影响外面 | 默认都是复制；要改外面的用 `&` 引用；数组除外 |
| `global x` | 变量直接定义在函数外面即可 |
