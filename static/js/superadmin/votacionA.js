const form = document.getElementById("form-candidato")
const lista = document.getElementById("lista-candidatos")
const resultados = document.getElementById("resultados")

// Control de horario
const horaInicioInput = document.getElementById("hora-inicio")
const horaFinInput = document.getElementById("hora-fin")
const btnGuardarHorario = document.getElementById("guardar-horario")

// Cargar horario guardado
const horarioGuardado = JSON.parse(localStorage.getItem("horarioVotacion")) || {}
if(horarioGuardado.inicio) horaInicioInput.value = horarioGuardado.inicio
if(horarioGuardado.fin) horaFinInput.value = horarioGuardado.fin

btnGuardarHorario.addEventListener("click", () => {
  const inicio = horaInicioInput.value
  const fin = horaFinInput.value
  if(!inicio || !fin){
    alert("Debes seleccionar hora de inicio y fin")
    return
  }
  localStorage.setItem("horarioVotacion", JSON.stringify({inicio, fin}))
  alert(`Horario guardado: ${inicio} a ${fin}`)
})

// Función para cargar candidatos
function cargarCandidatos() {
  lista.innerHTML = ""
  resultados.innerHTML = ""

  const categorias = ["personero", "contralor", "cabildante"]

  categorias.forEach(cat => {
    const candidatos = JSON.parse(localStorage.getItem("candidatos_" + cat)) || []
    if (candidatos.length > 0) {
      const titulo = document.createElement("h3")
      titulo.textContent = "Categoría: " + cat
      lista.appendChild(titulo)

      candidatos.forEach((candidato, index) => {
        const div = document.createElement("div")
        div.className = "candidato"
        div.innerHTML = `
          <img src="${candidato.foto}" alt="${candidato.nombre}">
          <div class="info">
            <h4>${candidato.nombre}</h4>
            <p><strong>Tarjetón:</strong> ${candidato.tarjeton}</p>
            <p>${candidato.propuesta}</p>
            <p><strong>Votos:</strong> ${candidato.votos || 0}</p>
          </div>
          <button class="eliminar" data-categoria="${cat}" data-index="${index}">🗑</button>
        `
        lista.appendChild(div)
      })

      const res = document.createElement("div")
      res.innerHTML = `<h4>Resultados de ${cat}</h4>`
      candidatos.forEach(c => {
        res.innerHTML += `<p>${c.nombre} (${c.tarjeton}): ${c.votos || 0} votos</p>`
      })
      resultados.appendChild(res)
    }
  })
}

// Agregar candidato
form.addEventListener("submit", e => {
  e.preventDefault()
  const nombre = document.getElementById("nombre").value.trim()
  const tarjeton = document.getElementById("tarjeton").value.trim()
  const propuesta = document.getElementById("propuesta").value.trim()
  const categoria = document.getElementById("categoria").value
  const fotoInput = document.getElementById("foto")
  if (!nombre || !tarjeton || !propuesta || !categoria || !fotoInput.files[0]) return
  const candidatos = JSON.parse(localStorage.getItem("candidatos_" + categoria)) || []
  if (candidatos.some(c => c.tarjeton === tarjeton)) {
    alert("El número de tarjetón ya está en uso en esta categoría")
    return
  }
  const reader = new FileReader()
  reader.onload = () => {
    const nuevo = { nombre, tarjeton, propuesta, foto: reader.result, votos: 0 }
    candidatos.push(nuevo)
    localStorage.setItem("candidatos_" + categoria, JSON.stringify(candidatos))
    form.reset()
    cargarCandidatos()
  }
  reader.readAsDataURL(fotoInput.files[0])
})

// Eliminar candidato
lista.addEventListener("click", e => {
  if (e.target.classList.contains("eliminar")) {
    const cat = e.target.dataset.categoria
    const index = e.target.dataset.index
    const candidatos = JSON.parse(localStorage.getItem("candidatos_" + cat)) || []
    candidatos.splice(index, 1)
    localStorage.setItem("candidatos_" + cat, JSON.stringify(candidatos))
    cargarCandidatos()
  }
})

cargarCandidatos()
