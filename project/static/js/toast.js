window.addEventListener("DOMContentLoaded", () => {
    const alertElement = document.querySelector("#alert");

    if (alertElement) {
        setTimeout(() => {
            alertElement.classList.add("animate-fade-up");
            setTimeout(() => {
                alertElement.remove();
            }, 1000);
        }, 4000);
    }
});
