document.addEventListener("DOMContentLoaded", function () {
    // Solo ejecuta la animación si existe el elemento con id "typed-text"
    const typedElement = document.getElementById("typed-text");
    if (typedElement) {
        startTypingAnimation(typedElement, "It's the only place you have to live.");
    }

    // Aquí puedes agregar más funciones para diferentes páginas
});

function startTypingAnimation(element, text, speed = 100) {
    const cursorElement = element.querySelector(".typed-cursor");
    let index = 0;

    function typeText() {
        if (index < text.length) {
            element.firstChild.textContent = text.substring(0, index + 1);
            index++;
            setTimeout(typeText, speed);
        } else if (cursorElement) {
            cursorElement.style.display = "inline-block";
        }
    }

    typeText();
}
