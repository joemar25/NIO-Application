window.addEventListener("DOMContentLoaded", () => {
    const alertElements = document.querySelectorAll("#alert > div");

    if (alertElements) {
        let delay = 5000;
        alertElements.forEach((alertElement) => {
            setTimeout(() => {
                alertElement.classList.add("animate-fade-up");
                setTimeout(() => {
                    alertElement.remove();
                }, 1000);
            }, delay);
            delay += 1000; // increase delay for the next element
        });
    }
});
