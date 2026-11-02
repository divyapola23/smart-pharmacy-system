// Small UI helpers. All real validation happens on the server.
document.addEventListener("DOMContentLoaded", function () {
  // Highlight the current sidebar link.
  document.querySelectorAll(".sidebar .nav-link").forEach(function (a) {
    var base = a.getAttribute("href");
    if (base && window.location.pathname.indexOf(base) === 0 && base !== "/") {
      a.classList.add("active");
    }
  });

  // Confirmation dialog + double-submit protection for every form.
  document.querySelectorAll("form").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      var btn = e.submitter || form.querySelector("button");
      var msg = btn && btn.getAttribute("data-confirm");
      if (msg && !window.confirm(msg)) {
        e.preventDefault();
        return;
      }
      if (form.dataset.submitted) {
        e.preventDefault(); // already submitted once
        return;
      }
      form.dataset.submitted = "1";
      if (btn) btn.disabled = true;
    });
  });

  // Purchase form: disable "new batch" fields when an existing batch is chosen.
  var existing = document.getElementById("existing-batch");
  var fields = document.getElementById("new-batch-fields");
  if (existing && fields) {
    var toggle = function () {
      var off = existing.value !== "";
      fields.disabled = off;
      fields.style.opacity = off ? 0.5 : 1;
    };
    existing.addEventListener("change", toggle);
    toggle();
  }

  // Sale form: show the batch selling price as a placeholder.
  var sale = document.getElementById("sale-batch");
  var price = document.getElementById("sale-price");
  if (sale && price) {
    sale.addEventListener("change", function () {
      var opt = sale.options[sale.selectedIndex];
      price.placeholder = opt && opt.dataset.price
        ? "Default: " + opt.dataset.price : "Defaults to batch selling price";
    });
  }
});
