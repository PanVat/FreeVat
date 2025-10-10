document.addEventListener('DOMContentLoaded', function() {
    const languageToggle = document.querySelector('.language');
    const flagButton = languageToggle.querySelector('.flag-button');
    const flagDropdown = languageToggle.querySelector('.flag-dropdown');

    if (flagButton && flagDropdown) {
        flagButton.addEventListener('click', function(event) {
            /* Zabrání, aby se kliknutí šířilo dál, např. na body (což by to zavřelo) */
            event.stopPropagation();

            /* Přepíná třídu pro zobrazení */
            flagDropdown.classList.toggle('flag-dropdown-visible');
        });

        /* Uzavře dropdown při kliknutí mimo něj */
        document.addEventListener('click', function(event) {
            /* Kontroluje, jestli kliknutí NEBYLO uvnitř kontejneru jazyka */
            if (!languageToggle.contains(event.target)) {
                flagDropdown.classList.remove('flag-dropdown-visible');
            }
        });
    }
});