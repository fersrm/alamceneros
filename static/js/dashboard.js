(() => {
  "use strict";

  // Obtén el elemento canvas del gráfico
  const ctx = document.getElementById("myChart");

  // Obtiene las fechas y los valores de ventas del diccionario ventas_diarias
  const fechas = Object.keys(ventas_diarias);
  const valoresVentas = Object.values(ventas_diarias);

  // Configura el gráfico
  const myChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: fechas, // Usa las fechas como etiquetas en el eje x
      datasets: [
        {
          data: valoresVentas, // Usa los valores de ventas como datos en el eje y
          lineTension: 0,
          backgroundColor: "transparent",
          borderColor: "#007bff",
          borderWidth: 4,
          pointBackgroundColor: "#007bff",
        },
      ],
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
        },
      },
      plugins: {
        legend: {
          display: false,
        },
        tooltip: {
          boxPadding: 3,
        },
      },
    },
  });
})();
