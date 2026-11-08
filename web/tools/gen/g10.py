import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mdpage import *

# 动画数据 data/traces/sort-10.js 是手工编排后保存的静态文件（由 verify-traces 校验），这里不再生成。
# 下面的小测是从原手写页原样搬来的（题干与基线逐字一致）。
QUIZ = {'q-01a': {'q': '预测：数据是 4 2 3 1。第 1 轮结束后，数组变成什么？',
           'options': ['1 2 3 4', '2 3 1 4', '2 4 3 1'],
           'answer': 1,
           'explain': '第 1 轮从左到右相邻比较：4 和 2 换、4 和 3 换、4 和 1 换，最大的 4 冒到了最后，其余的相对顺序是 2 3 1。'},
 'q-01b': {'q': '变一变：对 n 个数做冒泡排序，外层要进行几轮？',
           'options': ['n 轮', 'n - 1 轮', 'n / 2 轮'],
           'answer': 1,
           'explain': '每一轮都会让一个最大的数归位，n - 1 个归位后，最后一个自然就对了。4 个数就是 3 轮。'},
 'q-02a': {'q': 'cmp 里写成 return a.score >= b.score; 会有什么问题？',
           'options': ['没问题，更保险', '拿 x 和自己比，cmp(x, x) 会返回 true，不符合要求，sort 可能排错甚至崩溃', '只是排得慢一点'],
           'answer': 1,
           'explain': 'cmp(a, b) 表示“a 应该排在 b 前面吗”。x 不应该排在 x 自己前面，所以 cmp(x, x) 必须是 false，比较函数里只能用 > 或 <，不能带等号。'},
 'q-02b': {'q': '要求“先按总分从高到低，总分相同再按学号从小到大”，哪个 cmp 写对了？',
           'options': ['if (a.total != b.total) return a.total > b.total;  return a.id < b.id;',
                       'if (a.id != b.id) return a.id < b.id;  return a.total > b.total;',
                       'return a.total > b.total && a.id < b.id;'],
           'answer': 0,
           'explain': '要一层一层比：前面的关键字不相等就直接决定结果，相等才看下一个。第二个选项先看学号，学号几乎总不同，分数就没用了；第三个选项里“分高但学号大”的人，两边都返回 false，会被当成一样大。'},
 'q-02c': {'q': '题目要求“成绩相同的按输入顺序输出”，但 cmp 只写了 return a.score > b.score;，会怎样？',
           'options': ['sort 一定会保持输入顺序', 'sort 不保证同分的人保持原来的先后', '编译不通过'],
           'answer': 1,
           'explain': 'sort 不保证相等元素的原有顺序（不稳定排序）。所以要把输入编号 id 记下来，作为最后一个关键字。'}}

Z = QUIZ
inserts = {
    "2.3": [("quiz", Z["q-02a"])],
    "2.4": [("trace", "ex-10-02"), ("quiz", Z["q-02b"])],
    "2.5": [("quiz", Z["q-02c"])],
    "2.6": [("trace", "ex-10-01"), ("quiz", Z["q-01a"]), ("quiz", Z["q-01b"])],
}
tasks = (['把冒泡排序敲一遍，把数据改成 <code>5 1 4 2</code>，<b>先猜</b>第 1 轮结束后数组是什么，再在每轮后面加一行输出验证。', '把 cmp 的第二关键字删掉，只留 <code>return a.score &gt; b.score;</code>，看看 Tom 和 Bob 的顺序会不会变（可能变，也可能不变——这正是不能依赖它的原因）。'], "")
path, nq = build_lesson("10-结构体与排序.md", "10-sort.html", "第10课｜结构体与排序", "10", inserts, ["sort-10.js"], tasks)
print("第10课: %d 道小测（正文全文 + 互动）" % nq)
