/* Umožňuje posouvat položky v carouselu pomocí šipek a drag & drop. */
document.addEventListener('DOMContentLoaded', function () {
    const carousel = document.querySelector('.categories-carousel');
    const leftArrow = document.querySelector('.carousel-arrow-left');
    const rightArrow = document.querySelector('.carousel-arrow-right');

    /* Jak moc se posune obsah */
    const scrollAmount = 1000;

    /* Funkce pro aktualizaci viditelnosti šipek */
    function updateArrowVisibility() {
        leftArrow.classList.remove('arrow-hidden');
        leftArrow.style.pointerEvents = 'auto';

        rightArrow.classList.remove('arrow-hidden');
        rightArrow.style.pointerEvents = 'auto';
    }

    /* Inicializace při načtení */
    updateArrowVisibility();

    /* Přidání event listeneru na šipky */
    leftArrow.addEventListener('click', () => {
        carousel.scrollBy({left: -scrollAmount, behavior: 'smooth'});
    });

    rightArrow.addEventListener('click', () => {
        carousel.scrollBy({left: scrollAmount, behavior: 'smooth'});
    });

    /* Kontrola pozice při scrollování */
    carousel.addEventListener('scroll', updateArrowVisibility);

    /* Drag & drop */
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

    window.addEventListener('resize', updateArrowVisibility);
});