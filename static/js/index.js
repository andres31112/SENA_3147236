// index.js

const header = document.querySelector('header');
const navbar = document.querySelector('.navbar');

window.addEventListener('scroll', function () {
    // Si el scroll es mayor a 50px...
    if (window.scrollY > 50) {
        // Solo añade la clase 'scrolled' si no la tiene ya.
        if (!navbar.classList.contains('scrolled')) {
            navbar.classList.add('scrolled');
        }
    } else {
        // Si el scroll es menor o igual a 50px y la barra está en modo 'scrolled'...
        if (navbar.classList.contains('scrolled')) {
            // 1. Añadimos una clase al header para DESACTIVAR las transiciones.
            // Esto crea un efecto de "snap" al volver arriba.
            header.classList.add('no-transition-on-return');

            // 2. Quitamos la clase 'scrolled'. El cambio será INSTANTÁNEO.
            navbar.classList.remove('scrolled');

            // 3. Usamos setTimeout para quitar la clase de anulación después
            // de que el navegador haya procesado la eliminación de 'scrolled'.
            // Esto previene un parpadeo y asegura que las animaciones
            // para futuros scrolls funcionen correctamente.
            setTimeout(() => {
                header.classList.remove('no-transition-on-return');
            }, 10);
        }
    }
});


function initCarousel(carouselId) {
    const carouselComponent = document.getElementById(carouselId);
    if (!carouselComponent) {
        console.error(`No se encontró el carrusel con el ID: ${carouselId}`);
        return;
    }

    const slidesContainer = carouselComponent.querySelector('.slides-container');
    const prevButton = carouselComponent.querySelector('.prev-button');
    const nextButton = carouselComponent.querySelector('.next-button');

    const slideItems = Array.from(carouselComponent.querySelectorAll('.carousel-slide'));
    const slidesVisible = window.innerWidth <= 768 ? 1 : 2; // Mostrar 1 en móviles, 2 en pantallas más grandes
    const slideCount = slideItems.length;

    if (slideCount === 0) return;

    // Lógica para el bucle infinito
    // Clona el final y el principio de las diapositivas
    const lastClones = slideItems.slice(-slidesVisible).map(item => item.cloneNode(true));
    const firstClones = slideItems.slice(0, slidesVisible).map(item => item.cloneNode(true));

    lastClones.reverse().forEach(clone => slidesContainer.prepend(clone));
    firstClones.forEach(clone => slidesContainer.appendChild(clone));

    // El índice inicial está en la primera diapositiva "real" (después de los clones)
    let slideIndex = slidesVisible;
    let isTransitioning = false;
    let autoSlideInterval;

    function updateSlidePosition(withTransition = true) {
        slidesContainer.style.transition = withTransition ? 'transform 0.5s ease-in-out' : 'none';
        const offset = -slideIndex * (100 / slidesVisible);
        slidesContainer.style.transform = `translateX(${offset}%)`;
    }

    // Posición inicial sin transición
    updateSlidePosition(false);

    slidesContainer.addEventListener('transitionend', () => {
        isTransitioning = false;

        // Si llegamos a los clones del final, saltamos al primer slide real
        if (slideIndex >= slideCount + slidesVisible) {
            slideIndex = slidesVisible;
            updateSlidePosition(false);
        }

        // Si llegamos a los clones del principio, saltamos al último slide real
        if (slideIndex <= 0) {
            slideIndex = slideCount;
            updateSlidePosition(false);
        }
    });

    function shiftSlide(n) {
        if (isTransitioning) return;
        isTransitioning = true;
        slideIndex += n;
        updateSlidePosition();
    }

    function startAutoSlide() {
        stopAutoSlide();
        autoSlideInterval = setInterval(() => shiftSlide(slidesVisible), 3000);
    }

    function stopAutoSlide() {
        clearInterval(autoSlideInterval);
    }

    nextButton.addEventListener('click', () => {
        stopAutoSlide();
        shiftSlide(slidesVisible);
        startAutoSlide();
    });

    prevButton.addEventListener('click', () => {
        stopAutoSlide();
        shiftSlide(-slidesVisible);
        startAutoSlide();
    });

    carouselComponent.addEventListener('mouseenter', stopAutoSlide);
    carouselComponent.addEventListener('mouseleave', startAutoSlide);

    startAutoSlide();
}

// Inicializar el carrusel cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    initCarousel('mi-carrusel-1');
});