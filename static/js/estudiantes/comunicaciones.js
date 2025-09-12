const usuarioActualId = 1; // ID del usuario logueado

async function actualizarMensajesRecientes() {
    const res = await fetch(`/mensajes/${usuarioActualId}`);
    const inbox = await res.json();
    const lista = document.getElementById("mensajes-recientes");
    lista.innerHTML = "";

    inbox.slice(0,5).forEach(correo => {
        const li = document.createElement("li");
        li.textContent = `${correo.nombre_rem}: ${correo.Mensaje}`;
        li.onclick = () => verCorreo(correo.Id);
        lista.appendChild(li);
    });
}

async function mostrarInbox() {
    const res = await fetch(`/mensajes/${usuarioActualId}`);
    const inbox = await res.json();

    let html = "<h2>Bandeja de entrada</h2>";
    inbox.forEach(correo => {
        html += `<div class="email-card">
            <div class="email-info" onclick="verCorreo(${correo.Id})">
                <strong>${correo.nombre_rem}</strong>
                <span>${correo.Mensaje}</span>
                <span>${correo.FechaHora}</span>
            </div>
            <div class="email-actions">
                <button onclick="eliminarCorreo(${correo.Id}, event)">Eliminar</button>
            </div>
        </div>`;
    });
    document.getElementById("contenido").innerHTML = html;
    actualizarMensajesRecientes();
}

async function mostrarSent() {
    const res = await fetch(`/enviados/${usuarioActualId}`);
    const enviados = await res.json();

    let html = "<h2>Enviados</h2>";
    enviados.forEach(correo => {
        html += `<div class="email-card">
            <div class="email-info" onclick="verCorreo(${correo.Id})">
                <strong>Para: ${correo.destinatario}</strong>
                <span>${correo.Mensaje}</span>
                <span>${correo.FechaHora}</span>
            </div>
            <div class="email-actions">
                <button onclick="eliminarCorreo(${correo.Id}, event)">Eliminar</button>
            </div>
        </div>`;
    });
    document.getElementById("contenido").innerHTML = html;
    actualizarMensajesRecientes();
}

async function mostrarDeleted() {
    const res = await fetch(`/eliminados/${usuarioActualId}`);
    const deleted = await res.json();

    let html = "<h2>Eliminados</h2>";
    deleted.forEach(correo => {
        html += `<div class="email-card">
            <div class="email-info" onclick="verCorreo(${correo.Id})">
                <strong>${correo.nombre_rem}</strong>
                <span>${correo.Mensaje}</span>
                <span>${correo.FechaHora}</span>
            </div>
            <div class="email-actions">
                <button onclick="recuperarCorreo(${correo.Id}, event)">Recuperar</button>
            </div>
        </div>`;
    });
    document.getElementById("contenido").innerHTML = html;
    actualizarMensajesRecientes();
}

function mostrarCompose() {
    document.getElementById("contenido").innerHTML = `
        <h2>Redactar correo</h2>
        <form onsubmit="enviarCorreo(event)">
            <input type="email" id="destinatario" placeholder="Para: correo@inst.edu" required>
            <textarea id="mensaje" placeholder="Escribe tu mensaje..." required></textarea>
            <button type="submit">Enviar</button>
        </form>
    `;
}

async function enviarCorreo(e) {
    e.preventDefault();
    const destinatario = document.getElementById("destinatario").value;
    const mensaje = document.getElementById("mensaje").value;

    const res = await fetch('/enviar', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({remitente_id: usuarioActualId, destinatario, mensaje})
    });

    const data = await res.json();
    alert(data.mensaje || data.error);
    mostrarSent();
}

async function verCorreo(id) {
    const res = await fetch(`/correo/${id}`);
    const correo = await res.json();
    let html = `<h2>Mensaje</h2>
        <p><strong>De:</strong> ${correo.nombre_rem}</p>
        <p><strong>Para:</strong> ${correo.destinatario}</p>
        <p>${correo.Mensaje}</p>
        <button onclick="mostrarInbox()">Volver</button>
    `;
    document.getElementById("contenido").innerHTML = html;
}

async function eliminarCorreo(id, e) {
    e.stopPropagation();
    await fetch(`/eliminar/${id}`, {method: 'POST'});
    mostrarInbox();
}

async function recuperarCorreo(id, e) {
    e.stopPropagation();
    await fetch(`/recuperar/${id}`, {method: 'POST'});
    mostrarDeleted();
}

// Inicializar
mostrarInbox();
