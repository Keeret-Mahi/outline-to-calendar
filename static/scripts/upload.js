    const dropArea = document.getElementById('drop-area');
    const fileInput = document.getElementById('fileElem');

    ;['dragenter', 'dragover'].forEach(eventName => {
      dropArea.addEventListener(eventName, e => {
        e.preventDefault();
        dropArea.classList.add('highlight');
      }, false);
    });

    ;['dragleave', 'drop'].forEach(eventName => {
      dropArea.addEventListener(eventName, e => {
        e.preventDefault();
        dropArea.classList.remove('highlight');
      }, false);
    });

    dropArea.addEventListener('drop', e => {
      e.preventDefault();
      if (e.dataTransfer.files.length) {
        fileInput.files = e.dataTransfer.files;
      }
    });