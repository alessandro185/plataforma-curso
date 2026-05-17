(function () {
  "use strict";

  function getHashTabId() {
    var h = (window.location.hash || "").replace(/^#/, "");
    if (h === "inscricao") {
      return "inscricao";
    }
    return null;
  }

  function activateTab(root, tabId) {
    var tabs = root.querySelectorAll('[role="tab"][data-tab]');
    var panels = root.querySelectorAll('[role="tabpanel"][data-panel]');
    var found = false;

    tabs.forEach(function (btn) {
      var id = btn.getAttribute("data-tab");
      var isSel = id === tabId;
      if (isSel) {
        found = true;
      }
      btn.classList.toggle("is-active", isSel);
      btn.setAttribute("aria-selected", isSel ? "true" : "false");
      btn.tabIndex = isSel ? 0 : -1;
    });

    if (!found && tabs.length) {
      tabId = tabs[0].getAttribute("data-tab");
      return activateTab(root, tabId);
    }

    panels.forEach(function (panel) {
      var id = panel.getAttribute("data-panel");
      var on = id === tabId;
      panel.classList.toggle("is-active", on);
      panel.toggleAttribute("hidden", !on);
    });
  }

  function wireTabs(root) {
    var initial = root.getAttribute("data-initial-tab") || "";
    var hashTab = getHashTabId();
    var start = hashTab || initial || "";

    if (start) {
      activateTab(root, start);
    }

    root.addEventListener("click", function (e) {
      var btn = e.target.closest('[role="tab"][data-tab]');
      if (!btn || !root.contains(btn)) {
        return;
      }
      e.preventDefault();
      var tabId = btn.getAttribute("data-tab");
      activateTab(root, tabId);
      if (root.id === "inscricao" && tabId === "inscricao") {
        history.replaceState(null, "", "#inscricao");
      } else if (root.id === "inscricao") {
        history.replaceState(null, "", window.location.pathname + window.location.search);
      }
    });

    root.addEventListener("keydown", function (e) {
      var tabs = Array.prototype.slice.call(root.querySelectorAll('[role="tab"][data-tab]'));
      if (!tabs.length) {
        return;
      }
      var i = tabs.indexOf(document.activeElement);
      if (i < 0) {
        return;
      }
      var next = null;
      if (e.key === "ArrowRight") {
        next = tabs[(i + 1) % tabs.length];
      } else if (e.key === "ArrowLeft") {
        next = tabs[(i - 1 + tabs.length) % tabs.length];
      } else if (e.key === "Home") {
        next = tabs[0];
      } else if (e.key === "End") {
        next = tabs[tabs.length - 1];
      }
      if (next) {
        e.preventDefault();
        var tid = next.getAttribute("data-tab");
        activateTab(root, tid);
        next.focus();
      }
    });

    window.addEventListener("hashchange", function () {
      if (root.id !== "inscricao") {
        return;
      }
      var ht = getHashTabId();
      if (ht) {
        activateTab(root, ht);
      }
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("[data-tabs]").forEach(wireTabs);
  });
})();
