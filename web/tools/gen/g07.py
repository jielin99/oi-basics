import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mdpage import *

# 动画数据 data/traces/array-07.js 是手工编排后保存的静态文件（由 verify-traces 校验），这里不再生成。
# 下面的小测是从原手写页原样搬来的（题干与基线逐字一致）。
QUIZ = {'q-01a': {'q': '预测输出：下面的代码会输出什么？',
           'code': 'int b[5] = {1, 2, 3};\ncout << b[3] + b[4];',
           'options': ['5', '0', '编译出错'],
           'answer': 1,
           'explain': '没写的格子自动补 0，所以 b[3] 和 b[4] 都是 0，0 + 0 = 0。'},
 'q-01b': {'q': '变一变：把 a[0] = 10 改成 a[0] = 7，最后 a[4] 是多少？',
           'options': ['7', '14', '20'],
           'answer': 1,
           'explain': 'a[4] = a[0] * 2 = 7 * 2 = 14。'},
 'q-02a': {'q': 'int a[5]; 这个数组能用的下标是哪些？',
           'options': ['0 ~ 4', '1 ~ 5', '0 ~ 5'],
           'answer': 0,
           'explain': '5 个格子，下标从 0 到 4。a[5] 已经越界了，C++ 不会拦你，但结果不可靠。'},
 'q-03a': {'q': '变一变：如果数据变成 3 1 3 2 3 2（多了一个 2），最后 cnt[2] 是多少？',
           'options': ['1', '2', '3'],
           'answer': 1,
           'explain': '数字 2 一共出现了 2 次，所以 2 号桶里是 2。'},
 'q-04a': {'q': '外层 i 从 1 变成 2 以后，内层 j 从几开始？',
           'options': ['接着上一行，从 4 开始', '重新从 1 开始', '保持 3 不变'],
           'answer': 1,
           'explain': '内层循环每次都会重新执行 j = 1，所以每一行都从第 1 列开始。'},
 'q-04b': {'q': 'int g[10000][10000]; 大约要多少内存？（int 占 4 字节）',
           'options': ['约 40 MB', '约 400 MB', '约 4 GB'],
           'answer': 1,
           'explain': '10000 × 10000 = 1 亿个格子，× 4 字节 = 4 亿字节，约 400 MB，一般会超内存。'},
 'q-04c': {'q': 'int a[3] = {1, 2, 3}, b[3]; 然后写 b = a; 会怎样？',
           'options': ['b 变成 {1, 2, 3}', '编译不通过：数组不能整体赋值', '只复制第 1 个数'],
           'answer': 1,
           'explain': '数组不能用 = 整体赋值（编译器报 invalid array assignment），要用循环一个一个复制。'}}

Z = QUIZ
inserts = {
    "2.1": [("trace", "ex-07-01"), ("quiz", Z["q-01a"]), ("quiz", Z["q-01b"])],
    "2.4": [("trace", "ex-07-02"), ("quiz", Z["q-02a"])],
    "2.5": [("trace", "ex-07-03"), ("quiz", Z["q-03a"])],
    "2.6": [("trace", "ex-07-04"), ("quiz", Z["q-04a"])],
    "3.":  [("quiz", Z["q-04b"]), ("quiz", Z["q-04c"])],
}
tasks = (["把 1 号例子敲一遍，把 <code>a[0] = 10</code> 改成 <code>a[0] = 7</code>，<b>先猜</b> <code>a[4]</code> 再运行。",
          "把 4 号例子改成 3 行 4 列，并自己用 <code>cin</code> 读入数据，看输出是不是 3 行。"], "")
path, nq = build_lesson("07-数组.md", "07-array.html", "第7课｜数组", "07", inserts, ["array-07.js"], tasks)
print("第7课: %d 道小测（正文全文 + 互动）" % nq)
