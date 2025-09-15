    document.addEventListener("DOMContentLoaded", function() {
        const sidebar = document.getElementById("sidebar");
        const sidebarToggle = document.getElementById("sidebarToggle");
        const logoutBtn = document.getElementById("logoutBtn");

        // --- Toggle sidebar ---
        if (sidebarToggle && sidebar) {
            sidebarToggle.addEventListener("click", function() {
                sidebar.classList.toggle("active");
            });
        }

        // --- Cierra el sidebar al hacer clic fuera (solo en móviles) ---
        document.addEventListener("click", function(event) {
            if (
                window.innerWidth < 992 &&
                sidebar.classList.contains("active") &&
                !sidebar.contains(event.target) &&
                !sidebarToggle.contains(event.target)
            ) {
                sidebar.classList.remove("active");
            }
        });

        // --- Confirmación de cierre de sesión ---
        if (logoutBtn) {
            logoutBtn.addEventListener("click", function(event) {
                event.preventDefault();
                Swal.fire({
                    title: "¿Cerrar sesión?",
                    text: "Tu sesión actual se cerrará.",
                    icon: "warning",
                    showCancelButton: true,
                    confirmButtonColor: "#3085d6",
                    cancelButtonColor: "#d33",
                    confirmButtonText: "Sí, salir",
                    cancelButtonText: "Cancelar"
                }).then((result) => {
                    if (result.isConfirmed) {
                        window.location.href = "{{ url_for('auth.logout') }}";
                    }
                });
            });
        }
    });

