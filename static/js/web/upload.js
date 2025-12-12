document.addEventListener('DOMContentLoaded', function () {

    // Nyní již nepoužíváme imagePreview, ale pro reset formuláře jej můžeme definovat
    // a nechat prohlížeč ignorovat, pokud neexistuje.
    const imagePreview = document.getElementById('imagePreview');

    /**
     * Pomocná funkce pro přepínání viditelnosti prvků v upload zóně.
     * Skrývá nadpisy (H3, P) a tlačítko 'Select' a zobrazuje kontejner s vybraným souborem.
     * @param {string} type - 'model' nebo 'preview'
     * @param {boolean} isFileSelected - zda byl vybrán soubor
     */
    function toggleUploadState(type, isFileSelected) {
        const area = document.getElementById(`${type}FileUploadArea`);
        if (!area) return;

        // Najdeme textové elementy (H3 a P), které chceme skrýt
        // Vyloučíme chybové hlášky, které mají často třídu text-red-400
        const texts = area.querySelectorAll('h3, p:not(.text-red-400)');
        const buttonContainer = document.getElementById(`${type}FileButtonContainer`);
        const selectedContainer = document.getElementById(`selected${type.charAt(0).toUpperCase() + type.slice(1)}Container`);

        if (isFileSelected) {
            // Skryj nadpisy a tlačítko Select
            texts.forEach(el => el.classList.add('hidden'));
            buttonContainer.classList.add('hidden');
            // Zobraz kontejner s vybraným souborem
            selectedContainer.classList.remove('hidden');
        } else {
            // Zobraz nadpisy a tlačítko Select
            texts.forEach(el => el.classList.remove('hidden'));
            buttonContainer.classList.remove('hidden');
            // Skryj kontejner s vybraným souborem
            selectedContainer.classList.add('hidden');
        }
    }

    // --- Model file handling ---
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

    // --- Preview file handling ---
    const previewFileInput = document.getElementById('previewFile');
    const previewFileName = document.getElementById('previewFileName');
    const removePreviewButton = document.getElementById('removePreviewButton');

    if (previewFileInput && removePreviewButton) {
        previewFileInput.addEventListener('change', function () {
            if (this.files.length > 0) {
                // Přímé nastavení názvu souboru
                previewFileName.textContent = this.files[0].name;
                toggleUploadState('preview', true);
            }
            // ZÁMĚRNĚ ODSTRANĚNA MANIPULACE S imagePreview, aby se neobjevovala chyba
        });

        removePreviewButton.addEventListener('click', function () {
            previewFileInput.value = '';
            toggleUploadState('preview', false);
        });
    }

    // --- Reset celého formuláře ---
    const resetBtn = document.querySelector('button[type="reset"]');
    if (resetBtn) {
        resetBtn.addEventListener('click', function () {
            // Používáme setTimeout pro zajištění správného resetu UI po vyčištění polí prohlížečem
            setTimeout(() => {
                toggleUploadState('model', false);
                toggleUploadState('preview', false);
                // Vzhledem k tomu, že imagePreview je null, tato podmínka se neprovede,
                // ale je zde ponechána pro případ, že by se náhled v budoucnu vrátil.
                if (imagePreview) imagePreview.src = '';
            }, 10);
        });
    }
});