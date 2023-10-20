const $ = jQuery.noConflict();

// para productos
function abrir_modal_add(url) {
  $("#addModal").load(url, function () {
    $(this).modal("show");
  });
}

function abrir_modal_edit(url) {
  $("#editModal").load(url, function () {
    $(this).modal("show");
  });
}

function abrir_modal_add_produc(url) {
  $("#addProducModal").load(url, function () {
    $(this).modal("show");
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
