#!/usr/bin/env python3
"""链接检查：以 web/ 为根起一个本地 HTTP 服务（和局域网服务的发布范围一致），
从 index.html 出发遍历所有本地链接与资源：
  - 每个链接/资源都必须返回 200（指向 web/ 之外的文件在这里会 404）
  - #锚点 必须在目标页里真实存在；同一页内 id 不得重复
  - web/code/ 下的文件必须与仓库根目录 code/ 里的源文件字节一致
用法：python3 web/tools/linkcheck.py [起始页面...]（默认 index.html 和 lessons/*.html）"""
import functools, glob, http.server, os, re, sys, threading, urllib.error, urllib.parse, urllib.request
WEB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass

def main():
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=WEB))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = "http://127.0.0.1:%d/" % srv.server_address[1]
    starts = sys.argv[1:] or (["index.html"] + sorted("lessons/" + os.path.basename(p) for p in glob.glob(os.path.join(WEB, "lessons", "*.html"))))
    cache, ids, bad, checked = {}, {}, [], 0
    def get(url):
        url = urllib.parse.quote(url, safe=":/%?=&")
        if url not in cache:
            try:
                with urllib.request.urlopen(url, timeout=10) as r: cache[url] = (r.status, r.read())
            except urllib.error.HTTPError as e: cache[url] = (e.code, b"")
        return cache[url]
    def page_ids(url, body):
        if url not in ids:
            found = re.findall(r'\bid="([^"]+)"', body.decode("utf-8", "replace"))
            dup = sorted({i for i in found if found.count(i) > 1})
            if dup: bad.append("%s 里重复的 id：%s" % (url.replace(base, ""), dup))
            ids[url] = set(found)
        return ids[url]
    for st in starts:
        url = base + st
        code, body = get(url)
        if code != 200: bad.append("起始页打不开 %s (%d)" % (st, code)); continue
        page_ids(url, body)
        for link in re.findall(r'(?:href|src)="([^"]+)"', body.decode("utf-8", "replace")):
            if re.match(r"^(https?:|mailto:|javascript:)", link): continue
            full = urllib.parse.urljoin(url, link); target, _, frag = full.partition("#")
            checked += 1
            c, b = get(target)
            if c != 200: bad.append("%s → %s 返回 %d" % (st, link, c)); continue
            if frag:
                if not target.endswith(".html"): bad.append("%s → %s 锚点指向非页面" % (st, link)); continue
                if frag not in page_ids(target, b): bad.append("%s → %s 锚点不存在" % (st, link))
    cdir = os.path.join(WEB, "code")
    if os.path.isdir(cdir):
        for f in os.listdir(cdir):
            src = os.path.join(WEB, "..", "code", f)
            if not os.path.exists(src) or open(src, "rb").read() != open(os.path.join(cdir, f), "rb").read():
                bad.append("web/code/%s 与根目录 code/%s 不一致" % (f, f))
    for b_ in bad: print("FAIL", b_)
    print("链接检查：起始 %d 页，检查 %d 个链接/资源，失败 %d" % (len(starts), checked, len(bad)))
    return 1 if bad else 0
sys.exit(main())
