document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("cookie-popup").style.display = "flex";
});

function acceptCookies() {
    document.getElementById("cookie-popup").style.display = "none";
}

function closePopup() {
    document.getElementById("cookie-popup").style.display = "none";
}
