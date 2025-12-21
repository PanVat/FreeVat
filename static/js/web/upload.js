document.addEventListener('DOMContentLoaded', function () {
    /* Dropdown pro výběr kategorie */
    const trigger = document.getElementById('dropdownTrigger');
    const list = document.getElementById('dropdownList');
    const chevron = document.getElementById('dropdownChevron');
    const hiddenInput = document.querySelector('input[name="category"]');
    const selectedText = document.getElementById('selectedCategoryText');

    if (hiddenInput && hiddenInput.value) {
        const defaultLi = list.querySelector(`li[data-value="${hiddenInput.value}"]`);
        if (defaultLi) selectedText.innerText = defaultLi.querySelector('span').innerText;
    }

    if (trigger) {
        trigger.addEventListener('click', () => {
            list.classList.toggle('hidden');
            chevron.classList.toggle('rotate-180');
        });
    }

    if (list) {
        list.querySelectorAll('li').forEach(item => {
            item.addEventListener('click', function () {
                hiddenInput.value = this.getAttribute('data-value');
                selectedText.innerText = this.querySelector('span').innerText;
                list.classList.add('hidden');
                chevron.classList.remove('rotate-180');
            });
        });
    }

    document.addEventListener('click', (e) => {
        if (trigger && list && !trigger.contains(e.target) && !list.contains(e.target)) {
            list.classList.add('hidden');
            chevron.classList.remove('rotate-180');
        }
    });


    /* Funkce pro přepínání stavu nahrávání souborů */
    function toggleUploadState(type, isFileSelected) {
        const area = document.getElementById(`${type}FileUploadArea`);
        if (!area) return;

        const texts = area.querySelectorAll('h3, p:not(.text-red-400)');
        const buttonContainer = document.getElementById(`${type}FileButtonContainer`);
        const selectedContainer = document.getElementById(`selected${type.charAt(0).toUpperCase() + type.slice(1)}Container`);

        if (isFileSelected) {
            texts.forEach(el => el.classList.add('hidden'));
            if (buttonContainer) buttonContainer.classList.add('hidden');
            if (selectedContainer) selectedContainer.classList.remove('hidden');
        } else {
            texts.forEach(el => el.classList.remove('hidden'));
            if (buttonContainer) buttonContainer.classList.remove('hidden');
            if (selectedContainer) selectedContainer.classList.add('hidden');
        }
    }

    /* Obsluha nahrávání jednotlivých souborů */
    const modelFileInput = document.getElementById('modelFile');
    const modelFileName = document.getElementById('modelFileName');
    const removeModelButton = document.getElementById('removeModelButton');

    if (modelFileInput && removeModelButton) {
        modelFileInput.addEventListener('change', function () {
            if (this.files.length > 0) {
                modelFileName.textContent = this.files[0].name;
                toggleUploadState('model', true);
            }
        });

        removeModelButton.addEventListener('click', function () {
            modelFileInput.value = '';
            toggleUploadState('model', false);
        });
    }

    /* Obsluha nahrávání náhledového souboru */
    const previewFileInput = document.getElementById('previewFile');
    const previewFileName = document.getElementById('previewFileName');
    const removePreviewButton = document.getElementById('removePreviewButton');

    if (previewFileInput && removePreviewButton) {
        previewFileInput.addEventListener('change', function () {
            if (this.files.length > 0) {
                previewFileName.textContent = this.files[0].name;
                toggleUploadState('preview', true);
            }
        });

        removePreviewButton.addEventListener('click', function () {
            previewFileInput.value = '';
            toggleUploadState('preview', false);
        });
    }

    /* Pokročilá obsluha nahrávání více souborů (do galerie) */
    const galleryArea = document.getElementById('galleryFileUploadArea');
    const galleryInput = document.getElementById('galleryFiles');
    const galleryButtonContainer = document.getElementById('galleryFileButtonContainer');
    const galleryContainer = document.getElementById('selectedGalleryContainer');
    const galleryList = document.getElementById('galleryFilesList');
    const clearAllBtn = document.getElementById('clearAllGallery');
    let galleryFilesArray = [];

    function renderGallery() {
        if (!galleryList || !galleryArea) return;

        galleryList.innerHTML = '';
        galleryFilesArray.forEach((file, index) => {
            const item = document.createElement('div');
            // Stejná třída jako u jednotlivých souborů pro konzistenci stylů
            item.className = "selected-file-container mb-2";
            item.innerHTML = `
            <span class="truncate pr-4">${file.name}</span>
            <button type="button" class="remove-single-file remove-file-button" data-index="${index}">
                <img src="/static/img/icons/cross.svg" alt="Remove"/>
            </button>
        `;
            galleryList.appendChild(item);
        });

        const texts = galleryArea.querySelectorAll('.file-upload-title, .file-upload-description');

        if (galleryFilesArray.length > 0) {
            galleryContainer.classList.remove('hidden');
            texts.forEach(el => el.classList.add('hidden'));
        } else {
            galleryContainer.classList.add('hidden');
            texts.forEach(el => el.classList.remove('hidden'));
        }
    }

    /* Přidávání souborů do galerie */
    if (galleryInput) {
        galleryInput.addEventListener('change', function () {
            if (this.files.length > 0) {
                galleryFilesArray = [...galleryFilesArray, ...Array.from(this.files)];
                renderGallery();
                this.value = ''; // Reset inputu, aby šlo vybrat stejný soubor znovu
            }
        });
    }

    /* Mazání nahraných souborů */
    if (galleryList) {
        galleryList.addEventListener('click', function (e) {
            const btn = e.target.closest('.remove-single-file');
            if (btn) {
                const index = parseInt(btn.getAttribute('data-index'));
                galleryFilesArray.splice(index, 1);
                renderGallery();
            }
        });
    }

    // Mazání všeho
    if (clearAllBtn) {
        clearAllBtn.addEventListener('click', () => {
            galleryFilesArray = [];
            renderGallery();
        });
    }

    // KLÍČOVÁ ČÁST: Synchronizace před odesláním
    const uploadForm = document.getElementById('uploadForm');
    if (uploadForm) {
        uploadForm.addEventListener('submit', function (e) {
            // Vytvoříme virtuální kontejner pro soubory
            const dataTransfer = new DataTransfer();

            // Přidáme všechny soubory z našeho JS pole do tohoto kontejneru
            galleryFilesArray.forEach(file => {
                dataTransfer.items.add(file);
            });

            // Přepíšeme obsah skutečného inputu těmito soubory
            if (galleryInput) {
                galleryInput.files = dataTransfer.files;
            }

            // Pokud pole prázdné a pole je povinné, zde můžete přidat e.preventDefault()
        });
    }


    // ==========================================
    // 5. RESET A DISCARD LOGIKA
    // ==========================================

    function clearUI() {
        toggleUploadState('model', false);
        toggleUploadState('preview', false);

        galleryFilesArray = [];
        renderGallery(); // Toto zajistí, že se tlačítko vrátí nahoru a texty se zobrazí

        if (selectedText) selectedText.innerText = "Select a category";
        if (hiddenInput) hiddenInput.value = "";
        if (trigger) trigger.classList.remove('border-blue-500');
    }

    const resetBtn = document.getElementById('resetButton');
    if (resetBtn) {
        resetBtn.addEventListener('click', function () {
            setTimeout(() => {
                clearUI();
            }, 10);
        });
    }

    const discardBtn = document.getElementById('discardButton');
    if (discardBtn && uploadForm) {
        discardBtn.addEventListener('click', function (e) {
            e.preventDefault();
            uploadForm.reset();
            setTimeout(() => {
                clearUI();
                window.location.href = '/';
            }, 10);
        });
    }
});