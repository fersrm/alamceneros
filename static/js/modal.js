const $ = jQuery.noConflict();

// para productos
function abrir_modal_add(url) {
  $("#addModal").load(url, function () {
    $(this).modal("show");
    inicializarModal("myFormAdd");
  });
}

function abrir_modal_edit(url) {
  $("#editModal").load(url, function () {
    $(this).modal("show");
    inicializarModal("myFormEdit");
  });
}

function abrir_modal_plus(url) {
  $("#addProducModal").load(url, function () {
    $(this).modal("show");
    inicializarModal("myFormPlus");
  });
}

// para usuarios
function abrir_modal_add_user(url) {
  $("#addModalUser").load(url, function () {
    $(this).modal("show");
  });
}

function abrir_modal_edit_user(url) {
  $("#editModalUser").load(url, function () {
    $(this).modal("show");
  });
}

// tabla de stock
function tabla_poco_stock(url) {
  $("#tablaStock").load(url, function () {
    $(this).modal("show");
  });
}

// para clientes
function abrir_modal_add_client(url) {
  $("#addModalClient").load(url, function () {
    $(this).modal("show");
  });
}

function abrir_modal_edit_client(url) {
  $("#editModalClient").load(url, function () {
    $(this).modal("show");
  });
}

//--------------------Variables de margenes---------------------

function inicializarModal(formId) {
  const precioBruto = document.querySelector(
    `#${formId} [name='precio_bruto_producto']`
  );
  const precioVenta = document.querySelector(
    `#${formId} [name='precio_venta']`
  );
  const margenGanancia = document.querySelector(
    `#${formId} [name='margen_ganancia']`
  );

  function calcularYActualizarMargen() {
    const precioBrutoValor = parseFloat(precioBruto.value.trim());
    const precioVentaValor = parseFloat(precioVenta.value.trim());

    if (!isNaN(precioBrutoValor) && !isNaN(precioVentaValor)) {
      const margen =
        ((precioVentaValor - precioBrutoValor) / precioBrutoValor) * 100;
      margenGanancia.value = margen.toFixed(2);
    } else {
      margenGanancia.value = 0;
    }
  }

  precioBruto.addEventListener("input", calcularYActualizarMargen);
  precioVenta.addEventListener("input", calcularYActualizarMargen);

  // Calcular el margen al inicializar el formulario
  calcularYActualizarMargen();
}
