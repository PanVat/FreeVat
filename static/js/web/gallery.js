window.openModal = function (imageSrc) {
    const modal = document.getElementById('imageModal');
    const modalImg = document.getElementById('modalImage');

    if (modal && modalImg) {
        modal.classList.remove('hidden');
        modalImg.src = imageSrc;
        document.body.classList.add('modal-open');
    }
}

window.closeModal = function () {
    const modal = document.getElementById('imageModal');
    if (modal) {
        modal.classList.add('hidden');
        document.body.classList.remove('modal-open');
    }
}

/* Zavření klávesou 'ESC' nebo kliknutí mimo obrázek */
document.addEventListener('keydown', function (event) {
    if (event.key === "Escape") {
        closeModal();
    }
});