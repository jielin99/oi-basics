/* 小计算器：整除/取模、int 范围、位运算、字符与 ASCII、printf 格式。
 * 纯计算部分挂在 window.CalcCore，开发期由 tools/test-calc.py 与真实 C++ 输出逐项对照。
 * 所有输入都做范围检查，非法输入给出提示而不是算出怪数。 */
(function () {
  var C = {};
  var INT_MIN = -2147483648n, INT_MAX = 2147483647n;
  var LL_MIN = -9223372036854775808n, LL_MAX = 9223372036854775807n;
  C.INT_MIN = INT_MIN; C.INT_MAX = INT_MAX;

  function esc(s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }

  // ---- 整除 / 取模：C++ 向 0 取整，Python 向下取整 ----
  C.cppDivMod = function (a, b) { return { q: a / b, r: a % b }; };       // BigInt 的 / % 与 C++ 规则一致
  C.pyDivMod = function (a, b) {
    var q = a / b, r = a % b;
    if (r !== 0n && ((r < 0n) !== (b < 0n))) { q -= 1n; r += b; }
    return { q: q, r: r };
  };

  // ---- 表达式按 int 还是 long long 计算，是否超范围 ----
  C.exprCheck = function (x, op, y, tx, ty) {
    var type = (tx === "long long" || ty === "long long") ? "long long" : "int";
    var lo = type === "int" ? INT_MIN : LL_MIN, hi = type === "int" ? INT_MAX : LL_MAX;
    var v = op === "+" ? x + y : op === "-" ? x - y : x * y;
    return { type: type, value: v, ok: v >= lo && v <= hi, lo: lo, hi: hi };
  };

  // ---- 位运算（输入限定 0..255，移位 0..20，保证不溢出）----
  C.bits = function (a, b, k) {
    return { and: a & b, or: a | b, xor: a ^ b, not: ~a, shl: a << k, shr: a >> k };
  };
  C.bin = function (n, pad) { var s = (n >>> 0).toString(2); while (s.length < (pad || 0)) s = "0" + s; return s; };

  // ---- 字符与 ASCII ----
  C.charInfo = function (ch) {
    var code = ch.charCodeAt(0), r = { code: code };
    if (ch >= "0" && ch <= "9") r.digit = code - 48;
    if (ch >= "a" && ch <= "z") r.upper = String.fromCharCode(code - 32);
    if (ch >= "A" && ch <= "Z") r.lower = String.fromCharCode(code + 32);
    return r;
  };

  // ---- printf 格式：%d %5d %-5d %05d %.2f %8.3f ----
  // 小数舍入按 C 的规则（精确二进制值，恰好一半时取偶数位），不用 toFixed 的"取较大"
  C.toFixedC = function (x, p) {
    var neg = x < 0 || (x === 0 && 1 / x < 0), s = Math.abs(x).toFixed(p + 30);
    var dot = s.indexOf("."), ip = s.slice(0, dot), fr = s.slice(dot + 1), keep = fr.slice(0, p), rest = fr.slice(p);
    var up = false, c = rest.charCodeAt(0) - 48;
    if (c > 5) up = true;
    else if (c === 5) {
      var last = (keep.length ? keep : ip).slice(-1).charCodeAt(0) - 48;
      up = /[1-9]/.test(rest.slice(1)) || last % 2 === 1;
    }
    var digits = ip + keep, len = digits.length;
    if (up) { digits = (BigInt(digits) + 1n).toString(); while (digits.length < len) digits = "0" + digits; }
    var ilen = digits.length - p, res = digits.slice(0, ilen) + (p > 0 ? "." + digits.slice(ilen) : "");
    return (neg ? "-" : "") + res;
  };
  C.format = function (spec, text) {
    var m = /^%([-0]?)(\d*)(?:\.(\d+))?([df])$/.exec(spec);
    if (!m) return { err: "不支持的格式" };
    var left = m[1] === "-", zero = m[1] === "0", w = m[2] ? +m[2] : 0, conv = m[4], body;
    if (conv === "d") {
      if (!/^-?\d+$/.test(text)) return { err: "%d 只能配整数（给 %d 传小数是错误用法）" };
      var n = BigInt(text);
      if (n < INT_MIN || n > INT_MAX) return { err: "超出 int 范围，请改用 %lld" };
      body = n.toString();
    } else {
      var x = Number(text);
      if (text.trim() === "" || !isFinite(x) || Math.abs(x) >= 1e15) return { err: "请输入一个不太大的数" };
      body = C.toFixedC(x, m[3] === undefined ? 6 : +m[3]);
    }
    if (body.length < w) {
      if (left) body = body + " ".repeat(w - body.length);
      else if (zero) { var sg = body[0] === "-" ? "-" : ""; body = sg + "0".repeat(w - body.length) + body.slice(sg.length); }
      else body = " ".repeat(w - body.length) + body;
    }
    return { text: body };
  };

  window.CalcCore = C;

  // ================= 界面 =================
  function el(html) { var d = document.createElement("div"); d.innerHTML = html; return d.firstElementChild; }
  function bigOf(s) { return /^-?\d+$/.test(String(s).trim()) ? BigInt(String(s).trim()) : null; }

  var UI = {};

  UI.div = function (root) {
    root.innerHTML = '<div class="card calc"><div class="calc-t">🧮 整除与取模计算器（对比 Python）</div>' +
      '<div class="calc-row"><input id="a" value="-7" inputmode="numeric"> <span>÷ / %</span> <input id="b" value="2" inputmode="numeric"></div>' +
      '<div class="calc-out"></div></div>';
    var a = root.querySelector("#a"), b = root.querySelector("#b"), out = root.querySelector(".calc-out");
    function run() {
      var x = bigOf(a.value), y = bigOf(b.value);
      if (x === null || y === null) { out.innerHTML = '<span class="warn">请输入两个整数</span>'; return; }
      if (y === 0n) { out.innerHTML = '<span class="warn">除数不能是 0（C++ 里除以 0 会出错）</span>'; return; }
      if (x < -1000000000n || x > 1000000000n || y < -1000000000n || y > 1000000000n) { out.innerHTML = '<span class="warn">请输入绝对值不超过 10 亿的整数</span>'; return; }
      var c = C.cppDivMod(x, y), p = C.pyDivMod(x, y);
      out.innerHTML = '<table class="calc-tbl"><tr><th></th><th>商</th><th>余数</th></tr>' +
        '<tr><td>C++ <code>' + x + ' / ' + y + '</code>、<code>' + x + ' % ' + y + '</code></td><td><b>' + c.q + '</b></td><td><b>' + c.r + '</b></td></tr>' +
        '<tr><td>Python <code>' + x + ' // ' + y + '</code>、<code>' + x + ' % ' + y + '</code></td><td>' + p.q + '</td><td>' + p.r + '</td></tr></table>' +
        '<div class="calc-tip">C++：商向 0 取整（直接砍掉小数）；余数的符号和<b>被除数</b>相同。' +
        (c.q !== p.q ? ' <b>这组数据里两边不一样！</b>' : ' 这组数据两边恰好一样。') + '</div>';
    }
    a.addEventListener("input", run); b.addEventListener("input", run); run();
  };

  UI.range = function (root) {
    root.innerHTML = '<div class="card calc"><div class="calc-t">📏 这个运算会不会超范围？</div>' +
      '<div class="calc-row"><select id="tx"><option>int</option><option>long long</option></select> x = <input id="x" value="100000" inputmode="numeric">' +
      ' <select id="op"><option>*</option><option>+</option><option>-</option></select> ' +
      '<select id="ty"><option>int</option><option>long long</option></select> y = <input id="y" value="100000" inputmode="numeric"></div>' +
      '<div class="calc-out"></div></div>';
    var g = function (i) { return root.querySelector(i); }, out = g(".calc-out");
    function run() {
      var x = bigOf(g("#x").value), y = bigOf(g("#y").value), tx = g("#tx").value, ty = g("#ty").value, op = g("#op").value;
      if (x === null || y === null) { out.innerHTML = '<span class="warn">请输入两个整数</span>'; return; }
      var lim = function (t) { return t === "int" ? [INT_MIN, INT_MAX] : [LL_MIN, LL_MAX]; };
      if (x < lim(tx)[0] || x > lim(tx)[1]) { out.innerHTML = '<span class="warn">x 本身就超出了 ' + tx + ' 的范围，请改声明成 long long</span>'; return; }
      if (y < lim(ty)[0] || y > lim(ty)[1]) { out.innerHTML = '<span class="warn">y 本身就超出了 ' + ty + ' 的范围，请改声明成 long long</span>'; return; }
      var r = C.exprCheck(x, op, y, tx, ty);
      out.innerHTML = '<div>这个运算按 <b>' + r.type + '</b> 计算（两边只要有一个是 long long 才会按 long long 算）。</div>' +
        '<div>数学上的真实结果：<b>' + r.value + '</b></div>' +
        (r.ok ? '<div class="calc-ok">✅ 在 ' + r.type + ' 的范围内，安全。</div>'
              : '<div class="calc-bad">⚠️ 超出了 ' + r.type + ' 的范围（' + r.lo + ' ~ ' + r.hi + '）。C++ 里这一步算出来的结果<b>没有保证</b>，不要依赖它。</div>' +
                (r.type === "int" ? '<div class="calc-tip">注意：就算把结果赋给 long long 变量也救不回来——溢出发生在“计算的那一刻”。要先把其中一个转成 long long：<code>(long long)x * y</code>，或者一开始就把 x、y 声明成 long long。</div>' : '')) + '</div>';
    }
    ["#tx", "#ty", "#op", "#x", "#y"].forEach(function (i) { g(i).addEventListener("input", run); g(i).addEventListener("change", run); });
    run();
  };

  UI.bits = function (root) {
    root.innerHTML = '<div class="card calc"><div class="calc-t">🔢 位运算看二进制</div>' +
      '<div class="calc-row">a = <input id="a" value="12" inputmode="numeric"> b = <input id="b" value="10" inputmode="numeric"> 移位 k = <input id="k" value="2" inputmode="numeric" style="width:3em"></div>' +
      '<div class="calc-out"></div></div>';
    var g = function (i) { return root.querySelector(i); }, out = g(".calc-out");
    function run() {
      var a = +g("#a").value, b = +g("#b").value, k = +g("#k").value, ok = function (n, lo, hi) { return Number.isInteger(n) && n >= lo && n <= hi; };
      if (!ok(a, 0, 255) || !ok(b, 0, 255)) { out.innerHTML = '<span class="warn">a、b 请输入 0~255 的整数</span>'; return; }
      if (!ok(k, 0, 20)) { out.innerHTML = '<span class="warn">k 请输入 0~20 的整数</span>'; return; }
      var r = C.bits(a, b, k), row = function (name, code, n, pad) { return '<tr><td>' + name + '</td><td><code>' + code + '</code></td><td>' + n + '</td><td class="bin">' + C.bin(n, pad) + '</td></tr>'; };
      out.innerHTML = '<table class="calc-tbl"><tr><th>运算</th><th>写法</th><th>十进制</th><th>二进制</th></tr>' +
        row("a", "a", a, 8) + row("b", "b", b, 8) +
        row("按位与", "a & b", r.and, 8) + row("按位或", "a | b", r.or, 8) + row("按位异或", "a ^ b", r.xor, 8) +
        row("左移 k 位", "a << k", r.shl, 8) + row("右移 k 位", "a >> k", r.shr, 8) +
        '<tr><td>按位取反</td><td><code>~a</code></td><td>' + r.not + '</td><td class="bin">（int 有 32 位，取反后最高位变 1，是负数：<code>~a = -a - 1</code>）</td></tr></table>';
    }
    ["#a", "#b", "#k"].forEach(function (i) { g(i).addEventListener("input", run); }); run();
  };

  UI.ascii = function (root) {
    root.innerHTML = '<div class="card calc"><div class="calc-t">🔤 字符 ↔ ASCII 码</div>' +
      '<div class="calc-row">输入一个字符：<input id="c" value="a" maxlength="1" style="width:3em"> 或者输入编码（32~126）：<input id="n" value="" inputmode="numeric" style="width:4em"></div>' +
      '<div class="calc-out"></div></div>';
    var g = function (i) { return root.querySelector(i); }, out = g(".calc-out");
    function show(ch) {
      var r = C.charInfo(ch), h = '<div>字符 <code>\'' + esc(ch) + '\'</code> 的编码是 <b>' + r.code + '</b>（<code>(int)\'' + esc(ch) + '\'</code> 就是 ' + r.code + '）</div>';
      if (r.digit !== undefined) h += '<div>数字字符：<code>\'' + ch + '\' - \'0\'</code> = <b>' + r.digit + '</b>，这是把字符变成数字的办法。</div>';
      if (r.upper) h += '<div>小写字母：变大写 <code>\'' + ch + '\' - 32</code> 或 <code>\'' + ch + '\' - \'a\' + \'A\'</code> = <b>\'' + r.upper + '\'</b>（差 32）。</div>';
      if (r.lower) h += '<div>大写字母：变小写 <code>\'' + ch + '\' + 32</code> = <b>\'' + r.lower + '\'</b>。</div>';
      out.innerHTML = h;
    }
    g("#c").addEventListener("input", function () {
      var v = g("#c").value; if (!v) { out.innerHTML = '<span class="warn">请输入一个字符</span>'; return; }
      var code = v.charCodeAt(0); if (code < 32 || code > 126) { out.innerHTML = '<span class="warn">这里只演示 ASCII 可见字符（英文、数字、符号）</span>'; return; }
      g("#n").value = ""; show(v[0]);
    });
    g("#n").addEventListener("input", function () {
      var n = +g("#n").value; if (!Number.isInteger(n) || n < 32 || n > 126) { out.innerHTML = '<span class="warn">请输入 32~126 的整数</span>'; return; }
      g("#c").value = String.fromCharCode(n); show(String.fromCharCode(n));
    });
    show("a");
  };

  UI.fmt = function (root) {
    root.innerHTML = '<div class="card calc"><div class="calc-t">🖨️ printf 格式试一试</div>' +
      '<div class="calc-row"><code>printf("</code><select id="f"><option>%d</option><option>%5d</option><option>%-5d</option><option>%05d</option><option>%.2f</option><option>%8.3f</option><option>%.0f</option><option>%5.1f</option></select><code>", </code>' +
      '<input id="v" value="3.14159" inputmode="decimal" style="width:8em"><code>);</code></div><div class="calc-out"></div></div>';
    var g = function (i) { return root.querySelector(i); }, out = g(".calc-out");
    function run() {
      var r = C.format(g("#f").value, g("#v").value);
      out.innerHTML = r.err ? '<span class="warn">' + esc(r.err) + '</span>' :
        '<div>屏幕上显示（两边的 | 只是帮你看清空格）：</div><div class="stp-out">|' + esc(r.text).replace(/ /g, "␣") + '|</div>' +
        '<div class="calc-tip"><code>%d</code> 是整数；<code>%.2f</code> 保留 2 位小数（四舍五入）；数字是宽度，<code>-</code> 左对齐，<code>0</code> 用 0 补位。' +
        ' 上面的 ␣ 表示一个空格。</div>';
    }
    g("#f").addEventListener("change", run); g("#v").addEventListener("input", run); run();
  };

  window.mountCalcs = function () {
    var nodes = document.querySelectorAll("[data-calc]");
    for (var i = 0; i < nodes.length; i++) { var f = UI[nodes[i].getAttribute("data-calc")]; if (f) f(nodes[i]); }
  };
})();
