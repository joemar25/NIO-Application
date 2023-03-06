/* 
wrap JavaScript code inside a DOMContentLoaded event listener,
which ensures that the code is executed only after the HTML document
has been completely loaded and parsed.
*/

const initializeFileUploader = () => {
    const fileInput = document.getElementById('file_script');
    const fileLabel = document.getElementById('file_label');
    const fileTitle = document.getElementById('file_title');
    const cancelUpload = document.getElementById('cancel_upload');
    const isTouchDevice = () => {
        return 'ontouchstart' in window || navigator.maxTouchPoints > 0 || navigator.msMaxTouchPoints > 0;
    };
    const handleFileChange = (fileName) => {
        fileTitle.textContent = fileName;
        fileTitle.classList.remove('hidden');
        cancelUpload.classList.remove('hidden');
    };
    const resetFileInput = () => {
        fileInput.value = '';
        fileTitle.classList.add('hidden');
        cancelUpload.classList.add('hidden');
    };
    const handleFileDrop = (e) => {
        e.preventDefault();
        fileInput.files = e.dataTransfer.files;
        handleFileChange(fileInput.files[0].name);
    };
    fileInput.addEventListener('change', (e) => {
        handleFileChange(e.target.files[0].name);
    });
    cancelUpload.addEventListener('click', () => {
        resetFileInput();
    });
    if (!isTouchDevice()) {
        fileLabel.addEventListener('dragover', (e) => {
            e.preventDefault();
            fileLabel.classList.add('border-blue-500');
        });
        fileLabel.addEventListener('dragleave', () => {
            fileLabel.classList.remove('border-blue-500');
        });
        fileLabel.addEventListener('drop', handleFileDrop);
    }
};

const hideSubmitHomeBtn = () => {
    const submitButton = document.getElementById('home_submit_btn');
    submitButton.addEventListener('click', () => {
        setTimeout(() => {
            submitButton.disabled = true;
        }, 10);
    });
};

const checkUsernameInput = () => {
    const usernameInput = document.querySelector('#username-input');
    const usernameCounter = document.querySelector('#username-counter');
    const minChars = 3;
    const maxChars = 10;
    const updateUsernameCounter = () => {
        const characterCount = usernameInput.value.length;
        if (characterCount >= minChars && characterCount !== maxChars) {
            usernameCounter.textContent = `${characterCount}/${maxChars} characters`;
        } else if (characterCount === maxChars) {
            usernameCounter.textContent = `Maximum ${maxChars} characters reached`;
        } else {
            usernameCounter.textContent = '';
        }
    };
    usernameInput.addEventListener('input', updateUsernameCounter);
};

if (window.location.pathname === '/home') {
    initializeFileUploader();
    hideSubmitHomeBtn();
    checkUsernameInput();
}
