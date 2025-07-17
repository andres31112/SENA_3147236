document.querySelectorAll('.ver-btn').forEach(btn => {
btn.addEventListener('click', () => {
    document.getElementById('modal-id').textContent = btn.getAttribute('data-id');
    document.getElementById('modal-nombre').textContent = btn.getAttribute('data-nombre');
    document.getElementById('modal-sala').textContent = btn.getAttribute('data-sala');
    document.getElementById('modal-usuario').textContent = btn.getAttribute('data-usuario');
    document.getElementById('modal-estado').textContent = btn.getAttribute('data-estado');
    document.getElementById('modal-so').textContent = btn.getAttribute('data-so');
    document.getElementById('modal-ram').textContent = btn.getAttribute('data-ram');
    document.getElementById('modal-disco').textContent = btn.getAttribute('data-disco');
    document.getElementById('modal-mantenimiento').textContent = btn.getAttribute('data-mantenimiento');
});
});