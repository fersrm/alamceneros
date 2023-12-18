function exportTableToExcel(tableID ,filename ) {

  if (!filename) filename = 'excel_data.xls';
  let dataType = 'application/vnd.ms-excel';

  // Origen de los datos
  let tableSelect = document.getElementById(tableID);
  let tableHTML = tableSelect.outerHTML;
   
  // Crea el archivo descargable
  let blob = new Blob(['\ufeff',tableHTML], {type: dataType});
  
  // Crea un enlace de descarga en el navegador
  if (window.navigator && window.navigator.msSaveOrOpenBlob) { // Descargar para IExplorer
    window.navigator.msSaveOrOpenBlob(blob, filename);
  } else { // Descargar para Chrome, Firefox, etc.
    let a = document.createElement("a");
    document.body.appendChild(a);
    a.style = "display: none";
    let csvUrl = URL.createObjectURL(blob);
    a.href = csvUrl;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(a.href)
    a.remove();
  }
}


