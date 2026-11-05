/* AI Code Study — 全站共享脚本（零依赖） */
(function(){
  "use strict";

  /* ---------- 终端逐行显示 ---------- */
  var termBody = document.getElementById("termBody");
  if (termBody) {
    var lines = termBody.querySelectorAll(".term-line");
    var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduced) {
      lines.forEach(function(l){ l.classList.add("on"); });
    } else {
      var ti = 0;
      var nextLine = function(){
        if (ti >= lines.length) return;
        lines[ti].classList.add("on");
        ti++;
        setTimeout(nextLine, ti === 1 ? 900 : 420);
      };
      setTimeout(nextLine, 260);
    }
  }

  /* ---------- toast + 复制 ---------- */
  var toast = document.getElementById("toast");
  var toastTimer = null;
  function showToast(msg){
    if (!toast) return;
    toast.textContent = msg;
    toast.classList.add("on");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function(){ toast.classList.remove("on"); }, 1600);
  }
  function copyText(text){
    if (navigator.clipboard && navigator.clipboard.writeText) {
      return navigator.clipboard.writeText(text);
    }
    return new Promise(function(resolve, reject){
      var ta = document.createElement("textarea");
      ta.value = text;
      ta.style.position = "fixed";
      ta.style.opacity = "0";
      document.body.appendChild(ta);
      ta.select();
      try { document.execCommand("copy"); resolve(); } catch(e){ reject(e); }
      document.body.removeChild(ta);
    });
  }
  document.querySelectorAll(".code").forEach(function(block){
    var btn = block.querySelector(".copy");
    var pre = block.querySelector("pre");
    if (!btn || !pre) return;
    btn.addEventListener("click", function(){
      copyText(pre.innerText.replace(/\u00a0/g, " ")).then(function(){
        btn.classList.add("done");
        btn.textContent = "已复制";
        showToast("已复制到剪贴板");
        setTimeout(function(){
          btn.classList.remove("done");
          btn.textContent = "复制";
        }, 1500);
      }).catch(function(){
        showToast("复制失败，请手动选中");
      });
    });
  });

  /* ---------- tabs ---------- */
  document.querySelectorAll(".tabs").forEach(function(group){
    var tabs = Array.prototype.slice.call(group.querySelectorAll("[role=tab]"));
    tabs.forEach(function(tab){
      tab.addEventListener("click", function(){
        tabs.forEach(function(t){
          t.setAttribute("aria-selected", "false");
          var p = document.getElementById(t.getAttribute("aria-controls"));
          if (p) p.hidden = true;
        });
        tab.setAttribute("aria-selected", "true");
        var panel = document.getElementById(tab.getAttribute("aria-controls"));
        if (panel) panel.hidden = false;
        var box = group.closest(".searchable");
        if (box) applyBoxFilter(box);
      });
    });
  });

  /* ---------- 可搜索表格（.searchable 容器内：.search-input + tabs + panels） ---------- */
  function applyBoxFilter(box){
    var input = box.querySelector(".search-input");
    if (!input) return;
    var countEl = box.querySelector(".search-count");
    var noResult = box.querySelector(".no-result");
    var q = input.value.trim().toLowerCase();
    var activeTab = box.querySelector('.tabs [aria-selected="true"]');
    var panel = activeTab ? document.getElementById(activeTab.getAttribute("aria-controls")) : null;
    if (!panel) return;
    var rows = panel.querySelectorAll("tbody tr");
    var hit = 0;
    rows.forEach(function(tr){
      var ok = !q || tr.innerText.toLowerCase().indexOf(q) !== -1;
      tr.classList.toggle("gone", !ok);
      if (ok) hit++;
    });
    if (countEl) countEl.textContent = q ? (hit + " 条匹配") : "";
    if (noResult) noResult.hidden = !(q && hit === 0);
  }
  document.querySelectorAll(".searchable").forEach(function(box){
    var input = box.querySelector(".search-input");
    if (!input) return;
    input.addEventListener("input", function(){ applyBoxFilter(box); });
    input.addEventListener("search", function(){ applyBoxFilter(box); });
  });

  /* ---------- 目录高亮 ---------- */
  var navLinks = Array.prototype.slice.call(document.querySelectorAll("#toc a"));
  if (navLinks.length) {
    var sections = navLinks.map(function(a){
      return document.querySelector(a.getAttribute("href"));
    }).filter(Boolean);

    if ("IntersectionObserver" in window) {
      var io = new IntersectionObserver(function(entries){
        entries.forEach(function(en){
          if (!en.isIntersecting) return;
          var idx = sections.indexOf(en.target);
          if (idx === -1) return;
          navLinks.forEach(function(a){ a.classList.remove("active"); });
          navLinks[idx].classList.add("active");
        });
      }, { rootMargin: "-20% 0px -65% 0px", threshold: 0 });
      sections.forEach(function(s){ io.observe(s); });
    }

    navLinks.forEach(function(a){
      a.addEventListener("click", function(){
        navLinks.forEach(function(x){ x.classList.remove("active"); });
        a.classList.add("active");
      });
    });
  }

  /* ---------- 自检勾选（按页面独立存储） ---------- */
  var storeKey = "acs-" + (document.body.getAttribute("data-page") || "page") + "-checklist";
  var boxes = Array.prototype.slice.call(document.querySelectorAll("#checklist input"));
  if (boxes.length) {
    var countBox = document.getElementById("checkCount");
    var saved = {};
    try { saved = JSON.parse(localStorage.getItem(storeKey) || "{}"); } catch(e){ saved = {}; }

    var refreshCount = function(){
      if (!countBox) return;
      var n = boxes.filter(function(b){ return b.checked; }).length;
      countBox.textContent = n + " / " + boxes.length;
    };
    boxes.forEach(function(b){
      if (saved[b.dataset.key]) b.checked = true;
      b.addEventListener("change", function(){
        saved[b.dataset.key] = b.checked;
        try { localStorage.setItem(storeKey, JSON.stringify(saved)); } catch(e){}
        refreshCount();
      });
    });
    refreshCount();
  }

  /* ---------- 首页教程搜索 ---------- */
  var siteSearch = document.getElementById("siteSearch");
  if (siteSearch) {
    var siteCount = document.getElementById("siteCount");
    var cats = Array.prototype.slice.call(document.querySelectorAll(".cat"));
    siteSearch.addEventListener("input", function(){
      var q = siteSearch.value.trim().toLowerCase();
      var shown = 0;
      cats.forEach(function(cat){
        var visible = 0;
        cat.querySelectorAll(".card").forEach(function(card){
          var ok = !q || card.innerText.toLowerCase().indexOf(q) !== -1;
          card.classList.toggle("gone", !ok);
          if (ok) visible++;
        });
        cat.classList.toggle("gone", visible === 0);
        shown += visible;
      });
      if (siteCount) siteCount.textContent = q ? (shown + " 门教程匹配") : "";
    });
  }



  /* ---------- 主题切换 ---------- */
  (function(){
    var html = document.documentElement;
    var cfg = window.ACS_CONFIG || {};
    var saved = null;
    try { saved = localStorage.getItem("acs-theme"); } catch(e){}
    var systemDark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;

    function applyTheme(theme){
      if(theme === "dark" || theme === "light"){
        html.setAttribute("data-theme", theme);
        try { localStorage.setItem("acs-theme", theme); } catch(e){}
      } else {
        html.removeAttribute("data-theme");
        try { localStorage.removeItem("acs-theme"); } catch(e){}
      }
    }

    applyTheme(saved || (systemDark ? "dark" : "light"));

    if(cfg.enableDarkMode !== false){
      var nav = document.querySelector('.site-nav .inner > nav[aria-label="全站导航"]');
      if(nav){
        var btn = document.createElement("button");
        btn.className = "theme-toggle";
        btn.type = "button";
        btn.setAttribute("aria-label", "切换主题");
        function updateLabel(){
          btn.textContent = html.getAttribute("data-theme") === "dark" ? "浅色" : "深色";
        }
        updateLabel();
        btn.addEventListener("click", function(){
          var next = html.getAttribute("data-theme") === "dark" ? "light" : "dark";
          applyTheme(next);
          updateLabel();
        });
        nav.appendChild(btn);
      }
    }
  })();

  /* ---------- 阅读进度条 ---------- */
  (function(){
    var bar = document.createElement("div");
    bar.id = "readProgress";
    bar.setAttribute("aria-hidden", "true");
    document.body.appendChild(bar);

    function update(){
      var scrollTop = window.scrollY || document.documentElement.scrollTop || document.body.scrollTop || 0;
      var docHeight = document.documentElement.scrollHeight - window.innerHeight;
      var pct = docHeight > 0 ? (scrollTop / docHeight * 100) : 0;
      bar.style.width = pct + "%";
    }

    window.addEventListener("scroll", update, {passive:true});
    window.addEventListener("resize", update);
    update();
  })();

  /* ---------- 返回顶部 ---------- */
  (function(){
    var btn = document.createElement("button");
    btn.className = "back-to-top";
    btn.type = "button";
    btn.setAttribute("aria-label", "返回顶部");
    btn.textContent = "↑";
    btn.hidden = true;
    document.body.appendChild(btn);

    function toggle(){
      var y = window.scrollY || document.documentElement.scrollTop || 0;
      btn.hidden = y < 400;
    }

    window.addEventListener("scroll", toggle, {passive:true});
    btn.addEventListener("click", function(){
      window.scrollTo({top:0, behavior:"smooth"});
    });
    toggle();
  })();

  /* ---------- 面包屑 Schema.org ---------- */
  (function(){
    var crumbsNav = document.querySelector('nav[aria-label="面包屑"]');
    if(!crumbsNav) return;

    var links = Array.prototype.slice.call(crumbsNav.querySelectorAll("a"));
    var items = links.map(function(a, i){
      return {
        "@type": "ListItem",
        "position": i + 1,
        "name": a.textContent.trim(),
        "item": a.href
      };
    });

    var current = crumbsNav.querySelector("b");
    if(current && current.textContent.trim()){
      items.push({
        "@type": "ListItem",
        "position": items.length + 1,
        "name": current.textContent.trim()
      });
    }

    if(items.length === 0) return;

    var schema = {
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": items
    };

    var script = document.createElement("script");
    script.type = "application/ld+json";
    script.textContent = JSON.stringify(schema);
    document.head.appendChild(script);
  })();

})();
