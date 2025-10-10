document.addEventListener('DOMContentLoaded', function() {
    const overlay = document.querySelector('.overlay');

    /* Volá se při najetí kurzorem na odkaz */
    function activateOverlay() {
        overlay.classList.add('opacity-[0.1]'); // Příklad ztlumení na 40%
        overlay.classList.remove('opacity-0');
    }

    /* Volá se při opuštění odkazu */
    function deactivateOverlay() {
        overlay.classList.remove('opacity-[0.1]');
        overlay.classList.add('opacity-0');
    }

    /* Všechny prvky, které mají aktivovat overlay při najetí myší */
    const menuItems = document.querySelectorAll('.menu-item');

    menuItems.forEach(item => {
        item.addEventListener('mouseenter', activateOverlay);
        item.addEventListener('mouseleave', deactivateOverlay);
    });
});