/* Vezme tyto HTML prvky a uloží je do konstant */
document.addEventListener('DOMContentLoaded', function () {
    const languageToggle = document.querySelector('.language');
    const flagButton = languageToggle.querySelector('.flag-button');
    const flagDropdown = languageToggle.querySelector('.flag-dropdown');

    if (flagButton && flagDropdown) {
        flagButton.addEventListener('click', function (event) {
            /* Zabrání, aby se kliknutí šířilo dál, např. na body (což by to zavřelo) */
            event.stopPropagation();

            /* Přepíná třídu pro zobrazení */
            flagDropdown.classList.toggle('flag-dropdown-visible');
        });

        /* Uzavře dropdown při kliknutí mimo něj */
        document.addEventListener('click', function (event) {
            /* Kontroluje, jestli kliknutí NEBYLO uvnitř kontejneru jazyka */
            if (!languageToggle.contains(event.target)) {
                flagDropdown.classList.remove('flag-dropdown-visible');
            }
        });
    }
});

/* Posouvání carouselu pomocí šipek */
document.addEventListener('DOMContentLoaded', function () {
    const carousel = document.querySelector('.categories-carousel');
    const leftArrow = document.querySelector('.carousel-arrow-left');
    const rightArrow = document.querySelector('.carousel-arrow-right');

    const scrollAmount = 1000;

    // Funkce pro kontrolu pozice a skrytí/zobrazení šipek
    function updateArrowVisibility() {
        // Tolerance 5px pro zaokrouhlení
        const tolerance = 5;

        // Kontrola zda jsme na začátku
        const isAtStart = carousel.scrollLeft <= tolerance;

        // Kontrola zda jsme na konci
        const isAtEnd = carousel.scrollLeft + carousel.clientWidth >= carousel.scrollWidth - tolerance;

        // Upravíme šipku vlevo
        if (isAtStart) {
            leftArrow.classList.add('arrow-hidden');
            leftArrow.style.pointerEvents = 'none';
        } else {
            leftArrow.classList.remove('arrow-hidden');
            leftArrow.style.pointerEvents = 'auto';
        }

        // Upravíme šipku vpravo
        if (isAtEnd) {
            rightArrow.classList.add('arrow-hidden');
            rightArrow.style.pointerEvents = 'none';
        } else {
            rightArrow.classList.remove('arrow-hidden');
            rightArrow.style.pointerEvents = 'auto';
        }
    }

    // Inicializace při načtení
    updateArrowVisibility();

    // Přidání event listenerů na šipky
    leftArrow.addEventListener('click', () => {
        carousel.scrollBy({left: -scrollAmount, behavior: 'smooth'});
    });

    rightArrow.addEventListener('click', () => {
        carousel.scrollBy({left: scrollAmount, behavior: 'smooth'});
    });

    // Kontrola pozice při scrollování
    carousel.addEventListener('scroll', updateArrowVisibility);

    // Drag & drop
    let isDragging = false;
    let startX, scrollLeft;

    carousel.addEventListener('mousedown', (e) => {
        isDragging = true;
        startX = e.pageX - carousel.offsetLeft;
        scrollLeft = carousel.scrollLeft;
        carousel.style.cursor = 'grabbing';
    });

    ['mouseleave', 'mouseup'].forEach(event => {
        carousel.addEventListener(event, () => {
            isDragging = false;
            carousel.style.cursor = 'grab';
        });
    });

    carousel.addEventListener('mousemove', (e) => {
        if (!isDragging) return;
        e.preventDefault();
        const x = e.pageX - carousel.offsetLeft;
        const walk = (x - startX) * 2;
        carousel.scrollLeft = scrollLeft - walk;
    });

    // Resize listener pro případ změny velikosti okna
    window.addEventListener('resize', updateArrowVisibility);
});