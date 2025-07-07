const header = document.querySelector('header');
const navbar = document.querySelector('.navbar');

window.addEventListener('scroll', function () {
    // Si el scroll es mayor a 50px...
    if (window.scrollY > 50) {
        // Solo añade la clase 'scrolled' si no la tiene ya.
        // Esto activa la animación hacia abajo gracias al CSS.
        if (!navbar.classList.contains('scrolled')) {
            navbar.classList.add('scrolled');
        }
    } else {
        // Si el scroll es menor o igual a 50px y la barra está en modo 'scrolled'...
        if (navbar.classList.contains('scrolled')) {
            // 1. Añadimos una clase al header para DESACTIVAR las transiciones en el CSS.
            header.classList.add('no-transition-on-return');

            // 2. Quitamos la clase 'scrolled'. El cambio será INSTANTÁNEO.
            navbar.classList.remove('scrolled');

            // 3. Usamos requestAnimationFrame para quitar la clase de anulación en el siguiente
            //    "frame" del navegador. Esto asegura que el cambio de estilo se complete
            //    antes de reactivar las transiciones para futuros scrolls hacia abajo.
            requestAnimationFrame(() => {
                header.classList.remove('no-transition-on-return');
            });
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
    const slidesVisible = 2;
    const slideCount = slideItems.length;
    let isTransitioning = false;
    let autoSlideInterval;

    if (slideCount === 0) return;

    // --- LÓGICA MEJORADA PARA BUCLE INFINITO ---

    // Clonar el final al principio y el principio al final
    const lastClones = slideItems.slice(-slidesVisible).map(item => item.cloneNode(true));
    const firstClones = slideItems.slice(0, slidesVisible).map(item => item.cloneNode(true));

    lastClones.reverse().forEach(clone => slidesContainer.prepend(clone));
    firstClones.forEach(clone => slidesContainer.appendChild(clone));

    // Empezar en el primer slide real
    let slideIndex = slidesVisible;

    function updateSlidePosition(withTransition = true) {
        if (withTransition) {
            slidesContainer.style.transition = 'transform 0.5s ease-in-out';
        } else {
            slidesContainer.style.transition = 'none';
        }
        const offset = -slideIndex * (100 / slidesVisible);
        slidesContainer.style.transform = `translateX(${offset}%)`;
    }

    // Posición inicial sin transición
    updateSlidePosition(false);

    slidesContainer.addEventListener('transitionend', () => {
        isTransitioning = false;

        // Si llegamos a los clones del final, saltamos al principio
        if (slideIndex >= slideCount + slidesVisible) {
            slideIndex = slidesVisible;
            updateSlidePosition(false);
        }

        // Si llegamos a los clones del principio, saltamos al final
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

document.addEventListener('DOMContentLoaded', () => {
    initCarousel('mi-carrusel-1');
});
