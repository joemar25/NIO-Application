const initializeFileUploader = () => {
  const fileInput = document.getElementById("file_script");
  const fileLabel = document.getElementById("file_label");
  const fileInfo = document.getElementById("file_info");
  const fileTitle = document.getElementById("file_title");
  const cancelUpload = document.getElementById("cancel_upload");
  const textArea = document.getElementById("text_script"); // Assuming there's a textarea element with id "text_area"

  const handleFileChange = (fileName) => {
    fileTitle.textContent = fileName;
    fileInfo.classList.remove("hidden");
    textArea.value = ""; // Clear the textarea when a file is uploaded
  };

  const resetFileInput = () => {
    fileInput.value = "";
    fileInfo.classList.add("hidden");
  };

  const handleFileDrop = (e) => {
    e.preventDefault();
    fileInput.files = e.dataTransfer.files;
    handleFileChange(fileInput.files[0].name);
  };

  const handleTextAreaChange = () => {
    if (fileInput.files.length > 0) {
      resetFileInput();
    }
  };

  fileInput.addEventListener("change", (e) => {
    e.preventDefault();
    handleFileChange(e.target.files[0].name);
  });

  cancelUpload.addEventListener("click", (e) => {
    e.preventDefault();
    resetFileInput();
  });

  fileLabel.addEventListener("dragover", (e) => {
    e.preventDefault();
    fileLabel.classList.add("border-blue-500");
  });

  fileLabel.addEventListener("dragleave", () => {
    fileLabel.classList.remove("border-blue-500");
  });

  fileLabel.addEventListener("drop", (e) => {
    e.preventDefault();
    handleFileDrop(e);
  });

  textArea.addEventListener("input", handleTextAreaChange);
};

if (window.location.pathname === "/home") {
  initializeFileUploader();
}
