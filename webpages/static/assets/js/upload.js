document.addEventListener("DOMContentLoaded", function() {
  const fileInput = document.getElementById("file-input");
  const uploadButton = document.getElementById("upload-button");
  const previewUpload = document.getElementById("preview-upload");
  const uploadFrame = document.getElementById("upload-frame");

  fileInput.addEventListener("change", () => {
    const file = fileInput.files[0];

    if (file) {
      if (file.type === "application/pdf" && file.size <= 750 * 1024) {
        const reader = new FileReader();
        reader.onload = () => {
          uploadFrame.src = reader.result;
        };
        reader.readAsDataURL(file);

        previewUpload.style.display = "block";
      } else {
        alert("Please upload a PDF file with size below 750KB.");
        previewUpload.style.display = "none";
      }
    } else {
      previewUpload.style.display = "none";
    }
  });

  uploadButton.addEventListener("click", () => {
    fileInput.click();
  });
});
