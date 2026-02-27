document.addEventListener("DOMContentLoaded", () => {
  const uploadZone = document.getElementById("upload-zone");
  const fileInput = document.getElementById("file-input");
  const browseBtn = document.getElementById("browse-btn");

  // States
  const loadingState = document.getElementById("loading-state");
  const successState = document.getElementById("success-state");
  const errorState = document.getElementById("error-state");

  // Actions
  const downloadWordsBtn = document.getElementById("download-words");
  const downloadQuizBtn = document.getElementById("download-quiz");
  const resetBtn = document.getElementById("reset-btn");
  const retryBtn = document.getElementById("retry-btn");
  const errorMessage = document.getElementById("error-message");

  // Click to browse
  browseBtn.addEventListener("click", () => fileInput.click());
  uploadZone.addEventListener("click", (e) => {
    if (e.target !== browseBtn) fileInput.click();
  });

  // Drag and Drop
  ["dragenter", "dragover", "dragleave", "drop"].forEach((eventName) => {
    uploadZone.addEventListener(eventName, preventDefaults, false);
  });

  function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
  }

  ["dragenter", "dragover"].forEach((eventName) => {
    uploadZone.addEventListener(
      eventName,
      () => {
        uploadZone.classList.add("dragover");
      },
      false,
    );
  });

  ["dragleave", "drop"].forEach((eventName) => {
    uploadZone.addEventListener(
      eventName,
      () => {
        uploadZone.classList.remove("dragover");
      },
      false,
    );
  });

  uploadZone.addEventListener("drop", (e) => {
    let dt = e.dataTransfer;
    let files = dt.files;
    handleFiles(files);
  });

  fileInput.addEventListener("change", function () {
    handleFiles(this.files);
  });

  function handleFiles(files) {
    if (files.length === 0) return;

    const file = files[0];
    if (!file.name.endsWith(".txt")) {
      showError("Please upload a valid .txt file");
      return;
    }

    uploadFile(file);
  }

  function showState(stateElement) {
    uploadZone.classList.add("hidden");
    loadingState.classList.add("hidden");
    successState.classList.add("hidden");
    errorState.classList.add("hidden");

    stateElement.classList.remove("hidden");
  }

  function showError(msg) {
    errorMessage.textContent = msg;
    showState(errorState);
  }

  async function uploadFile(file) {
    showState(loadingState);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("/api/process", {
        method: "POST",
        body: formData,
      });

      const result = await response.json();

      if (response.ok) {
        // Success
        downloadWordsBtn.href = result.word_list_url;
        downloadQuizBtn.href = result.quiz_url;
        showState(successState);
      } else {
        // Server error
        showError(
          result.detail || "An error occurred while processing the file.",
        );
      }
    } catch (error) {
      // Network error
      showError("Network error. Make sure the server is running.");
      console.error(error);
    }
  }

  function resetUI() {
    fileInput.value = "";
    showState(uploadZone);
  }

  resetBtn.addEventListener("click", resetUI);
  retryBtn.addEventListener("click", resetUI);
});
