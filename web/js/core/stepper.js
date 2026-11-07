/* CodeStepper：状态完全由 steps[idx] 决定（无累积），所以后退/前进必然一致。
 * idx = -1 表示"尚未执行任何一步"。每步的 state 是【执行 line 之后】的状态。 */
(function () {
  function esc(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function Stepper(root, traceId, opts) {
    var trace = (window.TRACES || {})[traceId];
    if (!trace) { root.textContent = "找不到演示数据：" + traceId; return; }
    this.root = root; this.trace = trace; this.id = traceId;
    root._stepper = this;                       // 便于测试检查定时器
    this.idx = -1; this.timer = null;
    this.opts = opts || {};
    this.build();
    this.render();
  }

  Stepper.prototype.build = function () {
    var t = this.trace, self = this;
    var lines = t.source.replace(/\n$/, "").split("\n");
    var codeHtml = lines.map(function (ln, i) {
      return '<div class="stp-line" data-ln="' + (i + 1) + '"><span class="no">' + (i + 1) +
        '</span><span>' + esc(ln) + '</span></div>';
    }).join("");
    this.root.classList.add("card", "stp");
    this.root.innerHTML =
      '<div class="stp-title">' + esc(t.title) + (t.kind === "illustrative" ? ' <span class="badge">示意：真实 C++ 不会这样拦截</span>' : '') + '</div>' +
      '<div class="stp-main"><div class="stp-code">' + codeHtml + '</div>' +
      '<div class="stp-side"><h3>变量</h3><div class="stp-vars"></div>' +
      '<div class="stp-arrs"></div><h3>输出</h3><div class="stp-out"></div></div></div>' +
      '<div class="stp-note"></div>' +
      '<div class="stp-ctl">' +
      '<button data-a="reset">⟲ 重来</button><button data-a="prev">◀ 上一步</button>' +
      '<button data-a="next" class="primary">下一步 ▶</button><button data-a="play">⏵ 自动播放</button>' +
      '<button data-a="ask">🙋 我不懂这里</button><span class="cnt"></span></div>';
    this.els = {
      lines: this.root.querySelectorAll(".stp-line"),
      vars: this.root.querySelector(".stp-vars"),
      arrs: this.root.querySelector(".stp-arrs"),
      out: this.root.querySelector(".stp-out"),
      note: this.root.querySelector(".stp-note"),
      cnt: this.root.querySelector(".cnt"),
      prev: this.root.querySelector('[data-a="prev"]'),
      next: this.root.querySelector('[data-a="next"]'),
      play: this.root.querySelector('[data-a="play"]')
    };
    this.root.querySelector(".stp-ctl").addEventListener("click", function (e) {
      var a = e.target.getAttribute && e.target.getAttribute("data-a");
      if (!a) return;
      if (a === "next") { self.stop(); self.go(self.idx + 1); }
      else if (a === "prev") { self.stop(); self.go(self.idx - 1); }
      else if (a === "reset") { self.stop(); self.go(-1); }
      else if (a === "play") { self.timer ? self.stop() : self.start(); }
      else if (a === "ask") { self.ask(); }
    });
  };

  Stepper.prototype.go = function (i) {
    var n = this.trace.steps.length;
    this.idx = Math.max(-1, Math.min(n - 1, i));
    this.render();
  };

  Stepper.prototype.start = function () {
    var self = this;
    if (this.timer) return;                      // 重复点击不叠加定时器
    if (this.idx >= this.trace.steps.length - 1) this.idx = -1;
    this.els.play.textContent = "⏸ 暂停";
    this.timer = setInterval(function () {
      if (self.idx >= self.trace.steps.length - 1) { self.stop(); return; }   // 末步自动停止
      self.go(self.idx + 1);
    }, this.opts.interval || 1100);
  };

  Stepper.prototype.stop = function () {
    if (this.timer) { clearInterval(this.timer); this.timer = null; }
    this.els.play.textContent = "⏵ 自动播放";
  };

  Stepper.prototype.ask = function () {
    var label = (this.idx < 0) ? "尚未开始" : "第" + (this.idx + 1) + "步";
    var text = (window.PageKit && PageKit.lessonLabel ? PageKit.lessonLabel() : "") +
      "｜" + this.id + "｜" + label;
    if (window.PageKit) PageKit.addQuestion(text);
  };

  function stateAt(trace, i) {
    return i < 0 ? { vars: {}, arrays: {}, out: "", hl: {}, line: 0, note: "点「下一步」开始。" } : trace.steps[i];
  }

  Stepper.prototype.render = function () {
    var t = this.trace, cur = stateAt(t, this.idx), prev = stateAt(t, this.idx - 1);
    var n = t.steps.length;
    for (var k = 0; k < this.els.lines.length; k++) {
      this.els.lines[k].classList.toggle("on", (k + 1) === cur.line);
    }
    var vh = "", name;
    for (name in (cur.vars || {})) {
      var changed = !prev.vars || !(name in prev.vars) || String(prev.vars[name]) !== String(cur.vars[name]);
      vh += '<span class="var' + (changed && this.idx >= 0 ? " changed" : "") + '"><b>' + esc(name) + '</b> = ' + esc(cur.vars[name]) + '</span>';
    }
    this.els.vars.innerHTML = vh || '<span style="color:#9ca3af">（还没有变量）</span>';
    var ah = "";
    var bases = t.base || {};
    for (name in (cur.arrays || {})) {
      var data = cur.arrays[name], hl = (cur.hl && cur.hl[name]), base = bases[name] || 0;
      if (Array.isArray(data[0])) {
        // 二维：hl 元素为 [行,列]（高亮单格）或 [行]（高亮整行），下标按 base 计；
        // trace.cols[name] 给出列标题（用于"记录表"），否则显示列下标
        var cols = (t.cols || {})[name];
        var pairs = [], rowsOn = [];
        (hl || []).forEach(function (p) { if (p.length === 1) rowsOn.push(p[0]); else pairs.push(p[0] + "," + p[1]); });
        ah += '<div class="arr2"><span class="name">' + esc(name) + '</span><table><tr><td></td>' +
          data[0].map(function (_, c) { return '<td class="i">' + esc(cols ? cols[c] : c + base) + '</td>'; }).join("") + '</tr>' +
          data.map(function (row, r) {
            return '<tr><td class="i">' + (r + base) + '</td>' + row.map(function (v, c) {
              var on = pairs.indexOf((r + base) + "," + (c + base)) >= 0 || rowsOn.indexOf(r + base) >= 0;
              return '<td class="v' + (on ? " hl" : "") + '">' + esc(v) + '</td>';
            }).join("") + '</tr>';
          }).join("") + '</table></div>';
        continue;
      }
      var hls = hl === undefined ? [] : [].concat(hl);
      ah += '<div class="arr"><span class="name">' + esc(name) + '</span>' +
        data.map(function (v, j) {
          var cls = (hls.indexOf(j + base) >= 0 ? " hl" : "") + (v === "?" ? " bad" : "");   // "?" = 越界格，红色警示
          return '<div class="cell' + cls + '"><div class="v">' + esc(v) + '</div><div class="i">' + (j + base) + '</div></div>';
        }).join("") + '</div>';
    }
    this.els.arrs.innerHTML = ah;
    this.els.out.textContent = cur.out || "";
    this.els.note.textContent = cur.note || "";
    this.els.cnt.textContent = (this.idx + 1) + " / " + n;
    this.els.prev.disabled = this.idx < 0;
    this.els.next.disabled = this.idx >= n - 1;
  };

  window.Stepper = Stepper;
  window.mountSteppers = function () {
    var nodes = document.querySelectorAll("[data-trace]");
    for (var i = 0; i < nodes.length; i++) new Stepper(nodes[i], nodes[i].getAttribute("data-trace"));
  };
})();
