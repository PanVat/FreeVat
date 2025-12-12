document.addEventListener('DOMContentLoaded', function () {
    // Model file handling
    const modelFileInput = document.getElementById('modelFile');
    const modelFileButtonContainer = document.getElementById('modelFileButtonContainer');
    const selectedModelContainer = document.getElementById('selectedModelContainer');
    const modelFileName = document.getElementById('modelFileName');
    const removeModelButton = document.getElementById('removeModelButton');

    if (modelFileInput) {
        modelFileInput.addEventListener('change', function () {
            if (this.files.length > 0) {
                const file = this.files[0];
                modelFileName.textContent = file.name;

                // Skryj tlačítko, ukaž kontejner s názvem
                modelFileButtonContainer.classList.add('hidden');
                selectedModelContainer.classList.remove('hidden');
            }
        });

        // Reset modelu
        removeModelButton.addEventListener('click', function () {
            modelFileInput.value = '';
            modelFileButtonContainer.classList.remove('hidden');
            selectedModelContainer.classList.add('hidden');
        });
    }

    // Preview file handling
    const previewFileInput = document.getElementById('previewFile');
    const previewFileButtonContainer = document.getElementById('previewFileButtonContainer');
    const selectedPreviewContainer = document.getElementById('selectedPreviewContainer');
    const previewFileName = document.getElementById('previewFileName');
    const imagePreview = document.getElementById('imagePreview');
    const removePreviewButton = document.getElementById('removePreviewButton');

    if (previewFileInput) {
        previewFileInput.addEventListener('change', function () {
            if (this.files.length > 0) {
                const file = this.files[0];
                previewFileName.textContent = file.name;

                // Skryj tlačítko, ukaž kontejner s názvem a náhledem
                previewFileButtonContainer.classList.add('hidden');
                selectedPreviewContainer.classList.remove('hidden');

                // Zobraz náhled obrázku
                const reader = new FileReader();
                reader.onload = function (e) {
                    imagePreview.src = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        });

        // Reset preview
        removePreviewButton.addEventListener('click', function () {
            previewFileInput.value = '';
            previewFileButtonContainer.classList.remove('hidden');
            selectedPreviewContainer.classList.add('hidden');
            imagePreview.src = '';
        });
    }

    // Reset celého formuláře
    document.querySelector('button[type="reset"]').addEventListener('click', function () {
        // Reset modelu
        if (modelFileInput) {
            modelFileInput.value = '';
            modelFileButtonContainer.classList.remove('hidden');
            selectedModelContainer.classList.add('hidden');
        }

        // Reset preview
        if (previewFileInput) {
            previewFileInput.value = '';
            previewFileButtonContainer.classList.remove('hidden');
            selectedPreviewContainer.classList.add('hidden');
            imagePreview.src = '';
        }
    });
});