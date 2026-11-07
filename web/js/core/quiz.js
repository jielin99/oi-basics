/* Quiz：单选题。答错给解释，不扣分，可重选。
 * Quiz.mount(el, { q, code, options: [...], answer: 下标, explain }) */
(function () {
  function esc(s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }

  window.Quiz = {
    mount: function (el, d) {
      el.classList.add("card");
      el.innerHTML =
        '<div class="quiz-q">🤔 ' + esc(d.q) + '</div>' +
        (d.code ? '<div class="quiz-code">' + esc(d.code) + '</div>' : '') +
        '<div class="quiz-opts">' + d.options.map(function (o, i) {
          return '<button data-i="' + i + '">' + esc(o) + '</button>';
        }).join("") + '</div><div class="quiz-fb"></div>';
      var fb = el.querySelector(".quiz-fb"), btns = el.querySelectorAll(".quiz-opts button");
      el.querySelector(".quiz-opts").addEventListener("click", function (e) {
        var b = e.target.closest ? e.target.closest("button") : null;
        if (!b) return;
        var i = +b.getAttribute("data-i"), ok = i === d.answer;
        for (var k = 0; k < btns.length; k++) btns[k].classList.remove("right", "wrong");
        b.classList.add(ok ? "right" : "wrong");
        fb.className = "quiz-fb show " + (ok ? "ok" : "no");
        fb.textContent = (ok ? "✅ 答对了！" : "❌ 再想想，可以换一个选项再试。") + " " + (d.explain || "");
      });
    }
  };
})();
