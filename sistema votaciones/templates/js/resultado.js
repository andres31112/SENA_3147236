document.addEventListener("DOMContentLoaded", () => {
    const votos = JSON.parse(localStorage.getItem("votos")) || [];

    // Función para contar votos por categoría
    function contarVotos(categoria) {
        const conteo = {};

        votos.forEach(voto => {
            const candidato = voto[categoria];
            // Si no votó (blanco), no lo contamos
            if (candidato && candidato !== "blanco") {
                conteo[candidato] = (conteo[candidato] || 0) + 1;
            }
        });

        return conteo;
    }

    // Lista de categorías
    const categorias = ["personero", "contralor", "cabildante"];

    // Contenedor en HTML
    const resultadosDiv = document.getElementById("resultados");

    categorias.forEach(cat => {
        const conteo = contarVotos(cat);

        // Ordenar candidatos de mayor a menor votos
        const ordenados = Object.entries(conteo).sort((a, b) => b[1] - a[1]);

        // Crear sección por categoría
        const section = document.createElement("section");
        section.innerHTML = `<h3>${cat.charAt(0).toUpperCase() + cat.slice(1)}</h3>`;

        const ul = document.createElement("ul");

        if (ordenados.length === 0) {
            ul.innerHTML = "<li>Sin votos registrados</li>";
        } else {
            ordenados.forEach(([candidato, cantidad], index) => {
                const li = document.createElement("li");
                // Resaltar al ganador
                if (index === 0) {
                    li.innerHTML = `<strong> ${candidato} → ${cantidad} voto${cantidad !== 1 ? "s" : ""}</strong>`;
                } else {
                    li.textContent = `${candidato} → ${cantidad} voto${cantidad !== 1 ? "s" : ""}`;
                }
                ul.appendChild(li);
            });
        }

        section.appendChild(ul);
        resultadosDiv.appendChild(section);
    });
});
