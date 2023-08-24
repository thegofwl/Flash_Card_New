document.addEventListener("DOMContentLoaded", function () {
    var prevContent = document.querySelector(".content");

    document.querySelectorAll(".btn-slide").forEach(function (btn) {
        btn.addEventListener("click", function (event) {
            event.preventDefault();
            var targetUrl = this.getAttribute("data-url");
            var newContent = document.createElement("div");
            newContent.classList.add("content");

            fetch(targetUrl)
                .then(response => response.text())
                .then(data => {
                    newContent.innerHTML = data;
                    prevContent.classList.add("slide-left");
                    newContent.classList.add("active", "slide-right");
                    prevContent.parentElement.appendChild(newContent);

                    newContent.addEventListener("animationend", function () {
                        prevContent.parentElement.removeChild(prevContent);
                        prevContent = newContent;
                    });
                })
                .catch(error => console.error("Error fetching content:", error));
        });
    });
});