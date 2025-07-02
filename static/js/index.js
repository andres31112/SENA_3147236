 const header = document.querySelector('header');
    const navbar = document.querySelector('.navbar');

    window.addEventListener('scroll', function() {
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