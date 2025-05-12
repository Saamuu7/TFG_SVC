document.addEventListener("DOMContentLoaded", function () {
    // Verificamos si el usuario ya aceptó las cookies en esta sesión
    if (!sessionStorage.getItem("cookiesAccepted")) {
        document.getElementById("cookie-popup").style.display = "flex";
    }
});

function acceptCookies() {
    sessionStorage.setItem("cookiesAccepted", "true");
    document.getElementById("cookie-popup").style.display = "none";
}

function closePopup() {
    // Solo cerramos visualmente, no guardamos nada en sessionStorage
    document.getElementById("cookie-popup").style.display = "none";
}
