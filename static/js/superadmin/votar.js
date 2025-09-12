document.addEventListener("DOMContentLoaded", () => {
  const categorias = ["personero", "contralor", "cabildante"];

  // Validar horario de votación según admin
  const horario = JSON.parse(localStorage.getItem("horarioVotacion")) || {};
  if (horario.inicio && horario.fin) {
    const ahora = new Date();
    const [hi, mi] = horario.inicio.split(":").map(Number);
    const [hf, mf] = horario.fin.split(":").map(Number);
    const inicio = new Date(); inicio.setHours(hi, mi, 0);
    const fin = new Date(); fin.setHours(hf, mf, 0);

    if (ahora < inicio || ahora > fin) {
      alert("La votación no está abierta en este momento.");
      window.location.href = "menu.html";
      return;
    }
  }

  // Verificar si ya votó en cualquier categoría
  const yaVotoGlobal = categorias.some(cat => localStorage.getItem("yaVoto_" + cat) === "true");
  if (yaVotoGlobal) {
    alert("Ya realizaste tu voto. Serás redirigido al menú.");
    window.location.href = "menu.html";
    return;
  }

  categorias.forEach(cat => {
    const contenedor = document.getElementById("opciones-" + cat);
    const candidatos = JSON.parse(localStorage.getItem("candidatos_" + cat)) || [];

    if (candidatos.length === 0) {
      contenedor.innerHTML = "<p>No hay candidatos registrados en esta categoría.</p>";
      return;
    }

    const form = document.createElement("form");

    candidatos.forEach((candidato, index) => {
      const div = document.createElement("div");
      div.className = "col-md-4 mb-3";
      div.innerHTML = `
        <input type="radio" name="voto-${cat}" id="${cat}-${index}" value="${index}">
        <label for="${cat}-${index}">
          <div class="card-opcion">
            <img src="${candidato.foto}" alt="Foto de ${candidato.nombre}">
            <h5>${candidato.nombre}</h5>
            <p><strong>Tarjetón:</strong> ${candidato.tarjeton}</p>
            <p>${candidato.propuesta}</p>
          </div>
        </label>
      `;
      form.appendChild(div);
    });

    // Opción voto en blanco
    const divBlank = document.createElement("div");
    divBlank.className = "col-md-4 mb-3";
    divBlank.innerHTML = `
      <input type="radio" name="voto-${cat}" id="${cat}-blank" value="blanco">
      <label for="${cat}-blank">
        <div class="voto-blanco">Voto en blanco</div>
      </label>
    `;
    form.appendChild(divBlank);

    contenedor.appendChild(form);

    // Resaltar selección visual
    form.addEventListener("change", () => {
      const radios = form.querySelectorAll('input[type="radio"]');
      radios.forEach(r => {
        const card = r.nextElementSibling.querySelector('.card-opcion, .voto-blanco');
        if (r.checked) {
          card.style.backgroundColor = "rgba(0, 120, 173, 0.2)";
          card.style.borderColor = "#00628e";
        } else {
          card.style.backgroundColor = "";
          card.style.borderColor = "transparent";
        }
      });
    });
  });

  // Botón de votar
  const formGeneral = document.getElementById("votacionForm");
  formGeneral.addEventListener("submit", e => {
    e.preventDefault();

    // Validar que todas las categorías tengan selección
    let todasSeleccionadas = true;
    categorias.forEach(cat => {
      const seleccion = document.querySelector(`input[name="voto-${cat}"]:checked`);
      if (!seleccion) todasSeleccionadas = false;
    });

    if (!todasSeleccionadas) {
      alert("Debes seleccionar una opción en todas las categorías antes de votar.");
      return;
    }

    // Registrar votos
    categorias.forEach(cat => {
      const candidatos = JSON.parse(localStorage.getItem("candidatos_" + cat)) || [];
      const seleccion = document.querySelector(`input[name="voto-${cat}"]:checked`);
      if (seleccion.value !== "blanco") {
        const index = seleccion.value;
        candidatos[index].votos = (candidatos[index].votos || 0) + 1;
        localStorage.setItem("candidatos_" + cat, JSON.stringify(candidatos));
      }
      localStorage.setItem("yaVoto_" + cat, "true");
    });

    alert("Tu voto fue registrado correctamente.");
    window.location.href = "menu.html";
  });
});
