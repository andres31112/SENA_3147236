  document.addEventListener('DOMContentLoaded', () => {
            // --- Funcionalidad del Dropdown "Mas Opciones" ---
            const dropdownBtn = document.getElementById('dropdownBtn');
            const dropdownMenu = document.getElementById('dropdownMenu');

            if (dropdownBtn) {
                dropdownBtn.addEventListener('click', (event) => {
                    // Evita que el evento de clic en el botón se propague al 'window'
                    event.stopPropagation();
                    // Alterna la clase 'show' para mostrar u ocultar el menú
                    dropdownMenu.classList.toggle('show');
                });
            }

            // Cierra el dropdown si se hace clic fuera de él
            window.addEventListener('click', () => {
                if (dropdownMenu.classList.contains('show')) {
                    dropdownMenu.classList.remove('show');
                }
            });

            // --- Funcionalidad de los Checkboxes de la tabla ---
            const selectAllCheckbox = document.getElementById('selectAllCheckbox');
            const rowCheckboxes = document.querySelectorAll('.row-checkbox');

            if (selectAllCheckbox) {
                selectAllCheckbox.addEventListener('change', function() {
                    // Marcar o desmarcar todos los checkboxes de las filas
                    rowCheckboxes.forEach(checkbox => {
                        checkbox.checked = this.checked;
                    });
                });
            }

            // Desmarcar "seleccionar todo" si un checkbox individual es desmarcado
            rowCheckboxes.forEach(checkbox => {
                checkbox.addEventListener('change', () => {
                    if (!checkbox.checked) {
                        selectAllCheckbox.checked = false;
                    }
                    // Verifica si todos están marcados para marcar el principal
                    const allChecked = Array.from(rowCheckboxes).every(cb => cb.checked);
                    selectAllCheckbox.checked = allChecked;
                });
            });
        });