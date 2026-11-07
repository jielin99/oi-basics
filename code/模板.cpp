// 题目：Pxxxx 题目名
// 思路：（写一两句话，以后复习看得懂）
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;          // 以后写 ll 就代表 long long
const int N = 100000 + 10;     // 数组大小：按题目数据范围多开一点

int a[N];                      // 大数组开在 main 外面（全局）

int main() {
    // 比赛要求文件读写时，去掉下面两行开头的 // （文件名按题目要求改）
    // freopen("xxx.in", "r", stdin);
    // freopen("xxx.out", "w", stdout);

    ios::sync_with_stdio(false);   // 加速 cin/cout（之后不要再混用 scanf/printf）
    cin.tie(nullptr);

    int n;
    cin >> n;
    for (int i = 1; i <= n; i++) {
        cin >> a[i];
    }

    // TODO: 在这里写解题逻辑

    cout << n << "\n";
    return 0;
}
