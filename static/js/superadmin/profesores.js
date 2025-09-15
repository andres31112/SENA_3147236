// static/js/superadmin/profesores.js
document.addEventListener('DOMContentLoaded', () => {
    const tableBody = document.getElementById('profesores-table-body');

    // Función para renderizar los datos en la tabla
    function renderTable(profesores) {
        tableBody.innerHTML = ''; // Limpiar cualquier contenido previo

        profesores.forEach(profesor => {
            const row = document.createElement('tr');
            
            const userId = profesor.id_usuario; 

            // Determinar la clase del badge según el estado de la cuenta
            const estadoClase = profesor.estado_cuenta === 'activa' ? 'badge-success' : 'badge-danger';
            const estadoTexto = profesor.estado_cuenta === 'activa' ? 'Activo' : 'Inactivo';

            row.innerHTML = `
                <td><input type="checkbox" class="row-checkbox"></td>
                <td>${profesor.no_identidad}</td>
                <td><span class="avatar"><i class="fa-solid fa-user"></i></span></td>
                <td><a href="#">${profesor.nombre_completo}</a></td>
                <td>${profesor.correo}</td>
                <td><span class="tag tag-profesor">${profesor.rol}</span></td>
                <td><span class="badge ${estadoClase}">${estadoTexto}</span></td>
                <td>${profesor.curso_asignado}</td>
                <td>${profesor.materia_area}</td>
                <td>${profesor.sede_asignada}</td>
                <td class="actions-cell">
                    <a href="/admin/editar_usuario/${userId}" class="btn-action edit" title="Editar"><i class="fas fa-edit"></i></a>
                    <form action="/admin/eliminar_usuario/${userId}" method="POST" style="display:inline;" onsubmit="return confirm('¿Estás seguro de que quieres eliminar este usuario?');">
                        <button type="submit" class="btn-action delete" title="Eliminar"><i class="fas fa-trash-alt"></i></button>
                    </form>
                </td>
            `;
            tableBody.appendChild(row);
        });
    }
    // Función para obtener los datos de la API
    async function fetchProfesores() {
        try {
            const response = await fetch('/admin/api/profesores');
            const data = await response.json();

            if (response.ok) {
                renderTable(data.data);
            } else {
                console.error('Error al obtener datos de la API:', data.error);
                tableBody.innerHTML = `<tr><td colspan="9">Error al cargar los datos. Intente de nuevo más tarde.</td></tr>`;
            }
        } catch (error) {
            console.error('Error de red o del servidor:', error);
            tableBody.innerHTML = `<tr><td colspan="9">No se pudo conectar con el servidor.</td></tr>`;
        }
    }

    // Llamar a la función para cargar los datos al iniciar la página
    fetchProfesores();

    // Configurar la recarga automática cada 3 segundos (3000 milisegundos)
    // Nota: El intervalo de 3 segundos es muy corto para un ambiente de producción.
    setInterval(fetchProfesores, 3000);
});