    const dropArea = document.getElementById('drop-area');
    const fileInput = document.getElementById('fileElem');

    dropArea.addEventListener('dragover', (e) => {
      e.preventDefault();
      dropArea.classList.add('highlight');
    });

    dropArea.addEventListener('dragleave', () => {
      dropArea.classList.remove('highlight');
    });

    dropArea.addEventListener('drop', (e) => {
      e.preventDefault();
      dropArea.classList.remove('highlight');
      const files = e.dataTransfer.files;
      if (files.length > 0) {
        fileInput.files = files;
      }
    });