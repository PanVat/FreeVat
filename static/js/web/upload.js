/* Stará se o nahrání dat do databáze a logiku */
document.addEventListener('DOMContentLoaded', function () {

    /* Načtení prvků dropdownu z DOM */
    const trigger = document.getElementById('dropdownTrigger');
    const list = document.getElementById('dropdownList');
    const chevron = document.getElementById('dropdownChevron');
    const hiddenInput = document.querySelector('input[name="category"]');
    const selectedText = document.getElementById('selectedCategoryText');

    /* Inicializace textu: pokud už je v hidden inputu hodnota (např. při editaci), nastavíme text v UI */
    if (hiddenInput && hiddenInput.value) {
        const defaultLi = list.querySelector(`li[data-value="${hiddenInput.value}"]`);
        if (defaultLi) selectedText.innerText = defaultLi.querySelector('span').innerText;
    }

    /* Otevírání/zavírání seznamu kategorií a otáčení šipky po kliknutí na trigger */
    if (trigger) {
        trigger.addEventListener('click', () => {
            list.classList.toggle('hidden');
            chevron.classList.toggle('rotate-180');
        });
    }

    /* Výběr kategorie: uložení ID do hidden inputu, aktualizace textu a zavření seznamu */
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

    /* Zavření dropdownu kliknutím kamkoliv mimo něj */
    document.addEventListener('click', (e) => {
        if (trigger && list && !trigger.contains(e.target) && !list.contains(e.target)) {
            list.classList.add('hidden');
            chevron.classList.remove('rotate-180');
        }
    });

    /* Skryje nahrávací texty/tlačítka a zobrazí jméno souboru s křížkem (nebo naopak) */
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

    /* Logika pro 3D model soubor (.obj, .glb, atd.) */
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

    /* Logika pro hlavní náhledový obrázek (Thumbnail) */
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

    const galleryArea = document.getElementById('galleryFileUploadArea');
    const galleryInput = document.getElementById('galleryFiles');
    const galleryList = document.getElementById('galleryFilesList');
    const galleryContainer = document.getElementById('selectedGalleryContainer');
    const clearAllBtn = document.getElementById('clearAllGallery');
    let galleryFilesArray = []; /* Pole, kde držíme reálné objekty souborů z JS */

    /* Funkce, která vykreslí seznam souborů v galerii na základě galleryFilesArray */
    function renderGallery() {
        if (!galleryList || !galleryArea) return;

        galleryList.innerHTML = '';
        galleryFilesArray.forEach((file, index) => {
            const item = document.createElement('div');
            item.className = "selected-file-container mb-2";
            item.innerHTML = `
            <span class="truncate pr-4">${file.name}</span>
            <button type="button" class="remove-single-file remove-file-button" data-index="${index}">
                <img src="${crossIconUrl}" alt="Remove"/>
            </button>
        `;
            galleryList.appendChild(item);
        });

        /* Přepínání viditelnosti textů podle toho, zda je galerie prázdná */
        const texts = galleryArea.querySelectorAll('.file-upload-title, .file-upload-description');
        if (galleryFilesArray.length > 0) {
            galleryContainer.classList.remove('hidden');
            texts.forEach(el => el.classList.add('hidden'));
        } else {
            galleryContainer.classList.add('hidden');
            texts.forEach(el => el.classList.remove('hidden'));
        }
    }

    /* Přidání vybraných souborů do našeho pole a promazání inputu pro další výběr */
    if (galleryInput) {
        galleryInput.addEventListener('change', function () {
            if (this.files.length > 0) {
                galleryFilesArray = [...galleryFilesArray, ...Array.from(this.files)];
                renderGallery();
                this.value = '';
            }
        });
    }

    /* Odstraňování souborů z galerie (delegování událostí na galleryList) */
    if (galleryList) {
        galleryList.addEventListener('click', function (e) {
            const btn = e.target.closest('.remove-single-file');
            if (!btn) return;

            const index = btn.getAttribute('data-index');

            if (index !== null) {
                /* Smazání nově přidaného souboru z pole */
                galleryFilesArray.splice(parseInt(index), 1);
                renderGallery();
            } else {
                /* Smazání existujícího souboru (pouze vizuální z UI) */
                const container = btn.closest('.selected-file-container');
                if (container) {
                    container.remove();
                }

                /* Kontrola prázdného stavu pro zobrazení původních textů */
                if (galleryList.children.length === 0 && galleryFilesArray.length === 0) {
                    galleryContainer.classList.add('hidden');
                    const texts = galleryArea.querySelectorAll('.file-upload-title, .file-upload-description');
                    texts.forEach(el => el.classList.remove('hidden'));
                }
            }
        });
    }

    /* Tlačítko pro kompletní vymazání galerie */
    if (clearAllBtn) {
        clearAllBtn.addEventListener('click', () => {
            galleryFilesArray = [];
            renderGallery();
        });
    }

    /* Protože soubory držíme v JS poli, musíme je před odesláním vložit do skutečného inputu */
    const uploadForm = document.getElementById('uploadForm');
    if (uploadForm) {
        uploadForm.addEventListener('submit', function (e) {
            const dataTransfer = new DataTransfer();

            /* Přeneseme všechny soubory z galleryFilesArray do objektu DataTransfer */
            galleryFilesArray.forEach(file => {
                dataTransfer.items.add(file);
            });

            /* Přiřadíme výsledné soubory do inputu, který odchází na server */
            if (galleryInput) {
                galleryInput.files = dataTransfer.files;
            }
        });
    }


    /* Vyčistí kompletně celé uživatelské rozhraní formuláře do původního stavu */
    function clearUI() {
        toggleUploadState('model', false);
        toggleUploadState('preview', false);

        galleryFilesArray = [];
        renderGallery();

        if (selectedText) selectedText.innerText = "Select a category";
        if (hiddenInput) hiddenInput.value = "";
        if (trigger) trigger.classList.remove('border-blue-500');
    }

    /* Tlačítko Reset: Vymaže formulář a po krátké prodlevě vyčistí i UI prvky */
    const resetBtn = document.getElementById('resetButton');
    if (resetBtn) {
        resetBtn.addEventListener('click', function () {
            setTimeout(() => {
                clearUI();
            }, 10);
        });
    }

    /* Tlačítko Discard: Vymaže formulář, vyčistí UI a přesměruje uživatele pryč */
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