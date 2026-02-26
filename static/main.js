document.addEventListener("DOMContentLoaded", function () {
    var returnForms = document.querySelectorAll(".return-form");
    returnForms.forEach(function (form) {
        form.addEventListener("submit", function (event) {
            var ok = window.confirm("Mark this item as returned?");
            if (!ok) {
                event.preventDefault();
            }
        });
    });
});
