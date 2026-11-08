/* PageKit：投屏模式 + "我不懂"问题清单。
 * localStorage 随时可能不可用（file:// 隔离、隐私模式），所有读写都 try/catch，
 * 失败时正文照常使用，只提示"请复制保存"。 */
(function () {
  var qs = [], storageOk = true, KEY = "oi-web:";

  function load(k) { try { return window.localStorage.getItem(KEY + k); } catch (e) { storageOk = false; return null; } }
  function save(k, v) { try { window.localStorage.setItem(KEY + k, v); return true; } catch (e) { storageOk = false; return false; } }

  function lessonKey() { return document.body.getAttribute("data-lesson") || location.pathname; }

  var PageKit = {
    lessonLabel: function () { return document.body.getAttribute("data-lesson-label") || document.title; },

    setPresent: function (on) {
      document.body.classList.toggle("present", !!on);
      save("present", on ? "1" : "0");
      var b = document.getElementById("btn-present");
      if (b) b.textContent = on ? "退出投屏模式" : "投屏模式";
    },

    addQuestion: function (text) {
      if (qs.indexOf(text) < 0) qs.push(text);
      save("q:" + lessonKey(), JSON.stringify(qs));
      this.renderQuestions();
    },

    clearQuestions: function () {
      qs = []; save("q:" + lessonKey(), "[]"); this.renderQuestions();
    },

    renderQuestions: function () {
      var box = document.getElementById("ask-box");
      if (!box) return;
      var ta = box.querySelector("textarea"), warn = box.querySelector(".warn");
      ta.value = qs.join("\n");
      warn.textContent = storageOk ? "" : "⚠️ 这个浏览器没法保存清单，请把上面的文字复制到本子或文件里，再发给老师。";
      box.style.display = qs.length ? "" : "none";
    },

    // 自查清单的勾选状态（读写失败时只是不保存，页面照常使用）
    initChecks: function () {
      var boxes = document.querySelectorAll("input.chk");
      if (!boxes.length) return;
      var saved = [];
      try { saved = JSON.parse(load("chk:" + lessonKey()) || "[]"); } catch (e) { saved = []; }
      for (var i = 0; i < boxes.length; i++) {
        boxes[i].checked = !!saved[i];
        boxes[i].addEventListener("change", function () {
          var st = [];
          for (var j = 0; j < boxes.length; j++) st.push(boxes[j].checked);
          save("chk:" + lessonKey(), JSON.stringify(st));
        });
      }
    },

    init: function () {
      var self = this;
      var raw = load("q:" + lessonKey());
      if (raw) { try { qs = JSON.parse(raw) || []; } catch (e) { qs = []; } }
      if (load("present") === "1") this.setPresent(true);
      var btn = document.getElementById("btn-present");
      if (btn) btn.addEventListener("click", function () { self.setPresent(!document.body.classList.contains("present")); });
      var box = document.getElementById("ask-box");
      if (box) {
        box.querySelector("[data-a=copy]").addEventListener("click", function () {
          var ta = box.querySelector("textarea"); ta.select();
          try { document.execCommand("copy"); } catch (e) {}
        });
        box.querySelector("[data-a=clear]").addEventListener("click", function () { self.clearQuestions(); });
      }
      this.initChecks();
      var allBtn = document.getElementById("btn-all");
      if (allBtn) allBtn.addEventListener("click", function () {
        var ds = document.querySelectorAll("details.sec"), anyClosed = false, i;
        for (i = 0; i < ds.length; i++) if (!ds[i].open) anyClosed = true;
        for (i = 0; i < ds.length; i++) ds[i].open = anyClosed;
        allBtn.textContent = anyClosed ? "全部收起" : "全部展开";
      });
      this.renderQuestions();
      if (!storageOk) this.renderQuestions();
    }
  };
  window.PageKit = PageKit;
})();
