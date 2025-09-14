// Script para el carrusel de galería "coverflow" - VERSIÓN FINAL Y OPTIMIZADA
document.addEventListener('DOMContentLoaded', (event) => {
    const wrap = document.getElementById('galleryWrap');
    if (!wrap) return; // Salir si el contenedor principal no existe

    const track = document.getElementById('galleryTrack');
    const prevBtn = document.getElementById('galleryPrev');
    const nextBtn = document.getElementById('galleryNext');

    let originals = Array.from(track.children);
    const N = originals.length;
    if (N === 0) return;

    // Clonar los elementos para el bucle infinito
    for (let i = 0; i < N; i++) track.appendChild(originals[i].cloneNode(true));
    for (let i = N - 1; i >= 0; i--) track.insertBefore(originals[i].cloneNode(true), track.firstChild);

    let items = Array.from(track.children);
    let currentIndex = N + Math.floor(N / 2); // Iniciar en la mitad de la sección original
    const AUTO_MS = 4000;
    const TRANSITION_DURATION = 700;
    const TRANSITION = `transform ${TRANSITION_DURATION}ms cubic-bezier(.2,.9,.3,1)`;
    let isTransitioning = false;
    let autoTimer = null;
    let resizeTimer = null;

    function applyClasses() {
        items.forEach((it, i) => {
            const dist = Math.abs(i - currentIndex);
            it.classList.remove('large', 'medium', 'small');
            if (dist === 0) it.classList.add('large');
            else if (dist === 1) it.classList.add('medium');
            else it.classList.add('small');
        });
    }

    function setTransform(animate = true) {
        track.style.transition = animate ? TRANSITION : 'none';
        
        const centralItem = items[currentIndex];
        const centralItemWidth = centralItem ? centralItem.offsetWidth : 0;
        
        const offset = (currentIndex - N) * (items[0].offsetWidth + 24);
        const delta = (wrap.offsetWidth / 2) - offset - (centralItemWidth / 2);
        
        track.style.transform = `translateX(${delta}px)`;
    }

    function moveBy(dir) {
        if (isTransitioning) return;
        isTransitioning = true;
        currentIndex += dir;

        applyClasses();
        setTransform();

        setTimeout(() => {
            isTransitioning = false;
            if (currentIndex >= 2 * N) {
                track.style.transition = 'none';
                currentIndex -= N;
                setTransform(false);
            } else if (currentIndex < N) {
                track.style.transition = 'none';
                currentIndex += N;
                setTransform(false);
            }
        }, TRANSITION_DURATION);
        restartAuto();
    }

    // Agregar validación para evitar errores si los botones no existen
    if (prevBtn) {
        prevBtn.addEventListener('click', () => moveBy(-1));
    }
    if (nextBtn) {
        nextBtn.addEventListener('click', () => moveBy(1));
    }
    
    function startAuto() {
        stopAuto();
        autoTimer = setInterval(() => moveBy(1), AUTO_MS);
    }
    function stopAuto() {
        if (autoTimer) clearInterval(autoTimer);
        autoTimer = null;
    }
    function restartAuto() {
        stopAuto();
        startAuto();
    }

    wrap.addEventListener('mouseenter', stopAuto);
    wrap.addEventListener('mouseleave', startAuto);

    window.addEventListener('resize', () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
            setTransform(false);
            applyClasses();
        }, 140);
    });

    function init() {
        setTransform(false);
        applyClasses();
        setTimeout(startAuto, 500);
    }

    const imgElements = track.querySelectorAll('img');
    let loadedCount = 0;
    if (imgElements.length > 0) {
        imgElements.forEach(img => {
            if (img.complete) {
                loadedCount++;
            } else {
                img.addEventListener('load', () => {
                    loadedCount++;
                    if (loadedCount === imgElements.length) init();
                });
            }
        });
        if (loadedCount === imgElements.length) init();
    } else {
        init();
    }
});