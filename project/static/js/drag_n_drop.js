// this initialize the file upload widget

/* 
wrap your JavaScript code inside a DOMContentLoaded event listener,
which ensures that the code is executed only after the HTML document
has been completely loaded and parsed.
*/

const initializeFileUploader = () => {
    const fileInput = document.getElementById("file_script");
    const fileLabel = document.getElementById("file_label");
    const fileTitle = document.getElementById("file_title");
    const cancelUpload = document.getElementById("cancel_upload");

    fileInput.addEventListener("change", (e) => {
        const fileName = e.target.files[0].name;
        fileTitle.textContent = fileName;
        fileTitle.classList.remove("hidden");
        cancelUpload.classList.remove("hidden");
    });

    cancelUpload.addEventListener("click", () => {
        fileInput.value = "";
        fileTitle.classList.add("hidden");
        cancelUpload.classList.add("hidden");
    });

    const isTouchDevice = () => {
        return (
            "ontouchstart" in window ||
            navigator.maxTouchPoints > 0 ||
            navigator.msMaxTouchPoints > 0
        );
    };

    if (!isTouchDevice()) {
        fileLabel.addEventListener("dragover", (e) => {
            e.preventDefault();
            fileLabel.classList.add("border-blue-500");
        });

        fileLabel.addEventListener("dragleave", () => {
            fileLabel.classList.remove("border-blue-500");
        });

        fileLabel.addEventListener("drop", (e) => {
            e.preventDefault();
            fileInput.files = e.dataTransfer.files;
            const fileName = fileInput.files[0].name;
            fileTitle.textContent = fileName;
            fileTitle.classList.remove("hidden");
            cancelUpload.classList.remove("hidden");
        });
    }
};

// if on home page then execute the function
if (window.location.pathname === "/home") {
    initializeFileUploader();
}


