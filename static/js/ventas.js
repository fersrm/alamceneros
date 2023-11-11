document.addEventListener("DOMContentLoaded", function () {
  function actualizarTabla() {
    const productCarrito = JSON.parse(localStorage.getItem("carrito")) || [];
    const btnContainer = document.getElementById("containerBtnVentas");
    const tableBody = document.querySelector("#table-venta tbody");
    // Limpia la tabla
    tableBody.innerHTML = "";

    if (productCarrito.length !== 0 && productCarrito) {
      const productCarritoTabla = productCarrito.filter(
        (producto) => producto.cantidad > 0
      );
      // Obtener la referencia a la tabla donde se mostrarán los productos

      // Inicializar el precio total del carrito
      let precioTotal = 0;

      // Recorre los productos en el carrito y agrega filas actualizadas a la tabla
      productCarritoTabla.forEach((producto) => {
        let fila = document.createElement("tr");

        let codigo = document.createElement("td");
        codigo.textContent = producto.codigo;

        let nombreProducto = document.createElement("td");
        nombreProducto.textContent = producto.nombre;

        let cantidad = document.createElement("td");
        cantidad.textContent = producto.cantidad;

        let precioUnitario = document.createElement("td");
        precioUnitario.textContent = producto.precio;

        let subtotal = document.createElement("td");
        // Calcular el subtotal para este producto
        let subtotalProducto = producto.cantidad * producto.precio;
        subtotal.textContent = subtotalProducto;

        // Actualizar el precio total del carrito
        precioTotal += subtotalProducto;

        let acciones = document.createElement("td");

        // Contenedor de botones
        let containerBtn = document.createElement("div");
        containerBtn.classList.add("d-flex", "gap-2", "btn-carrito");

        // Botón para eliminar producto
        let botonEliminar = document.createElement("button");
        botonEliminar.innerHTML = '<i class="bi bi-trash3"></i>';
        botonEliminar.classList.add("btn", "btn-outline-danger", "btn-sm");
        botonEliminar.addEventListener("click", () =>
          eliminarProductoVentas(producto.id, productCarritoTabla, tableBody)
        );

        if (producto.medida === 1) {
          // Botón para aumentar cantidad
          let botonAumentar = document.createElement("button");
          botonAumentar.innerHTML = '<i class="bi bi-plus-circle"></i>';
          botonAumentar.classList.add("btn", "btn-outline-success", "btn-sm");
          botonAumentar.addEventListener("click", () =>
            aumentarCantidadVentas(producto.id, productCarritoTabla, tableBody)
          );

          // Botón para disminuir cantidad
          let botonDisminuir = document.createElement("button");
          botonDisminuir.innerHTML = '<i class="bi bi-dash-circle"></i>';
          botonDisminuir.classList.add("btn", "btn-outline-warning", "btn-sm");
          botonDisminuir.addEventListener("click", () =>
            disminuirCantidadVentas(producto.id, productCarritoTabla, tableBody)
          );

          containerBtn.appendChild(botonAumentar);
          containerBtn.appendChild(botonDisminuir);
        }

        containerBtn.appendChild(botonEliminar);

        acciones.appendChild(containerBtn);

        fila.appendChild(codigo);
        fila.appendChild(nombreProducto);
        fila.appendChild(cantidad);
        fila.appendChild(precioUnitario);
        fila.appendChild(subtotal);
        fila.appendChild(acciones);

        tableBody.appendChild(fila);
      });

      if (btnContainer.classList.contains("none")) {
        btnContainer.classList.remove("none");
      }
    } else {
      btnContainer.classList.add("none");

      let filaVacio = `<tr><td colspan="6">NO HAY PRODUCTOS INGRESADOS</td></tr>`;

      tableBody.innerHTML = filaVacio;
    }
  }

  function eliminarProductoVentas(id, productos, tabla) {
    eliminarDelCarrito(id);
    actualizarTabla(productos, tabla);
    updateCalculoCarrito();
  }

  function aumentarCantidadVentas(id, productos, tabla) {
    aumentarCantidad(id);
    actualizarTabla(productos, tabla);
    updateCalculoCarrito();
  }

  function disminuirCantidadVentas(id, productos, tabla) {
    disminuirCantidad(id);
    actualizarTabla(productos, tabla);
    updateCalculoCarrito();
  }

  actualizarTabla();

  ////////////////////////////////////////////////////////////////////
  ///////////// CALCULA SUBTOTAL Y TOTAL DE LO QUE TIENE LA TABLA ////
  ////////////////////////////////////////////////////////////////////

  // Función para actualizar los cálculos
  function updateCalculoCarrito() {
    const productCarrito = JSON.parse(localStorage.getItem("carrito"));

    let total = 0;
    let totalImpuesto = 0;
    let subtotal = 0;

    if (productCarrito && productCarrito.length > 0) {
      const productCarritoTabla = productCarrito.filter(
        (producto) => producto.cantidad > 0
      );

      productCarritoTabla.forEach(function (product) {
        const precio = parseFloat(product.precio);
        const cantidad = parseInt(product.cantidad);
        const impuesto = parseInt(product.impuesto);

        // Total por prodcuto
        const totalProducto = precio * cantidad;

        // Suma de los productos
        total += totalProducto;

        if (impuesto === 1) {
          const totalImpuestoProducto = totalProducto * 0.19;
          totalImpuesto += totalImpuestoProducto;
          totalImpuesto = Math.round(totalImpuesto);
        }
      });

      subtotal = total - totalImpuesto;
    }

    // Actualiza los valores

    document.querySelector("[name='subtotal']").value = subtotal.toFixed(2);
    document.querySelector("[name='impuestos']").value =
      totalImpuesto.toFixed(2);
    document.querySelector("[name='total']").value = total.toFixed(2);
  }

  updateCalculoCarrito();

  // LIMPIAR VENTA
  const btnBorrarVenta = document.getElementById("btnLimpiarVenta");

  btnBorrarVenta.addEventListener("click", function () {
    Swal.fire({
      titleText: `¿Estás seguro Borrar la Compra?`,
      icon: "question",
      showCancelButton: true,
      cancelButtonText: "No, Cancelar",
      confirmButtonText: "Si, Eliminar",
      confirmButtonColor: "#dc3545",
    }).then(function (result) {
      if (result.isConfirmed) {
        localStorage.removeItem("carrito");
        location.reload();
      }
    });
  });

  /////////////////////////////////////
  ///// GENERAR VENTA ////////////////
  ////////////////////////////////////

  const btnPdfVenta = document.getElementById("btnSumitVenta");

  function crearTablaBoleta() {
    let carrito = JSON.parse(localStorage.getItem("carrito")) || [];

    if (carrito.length !== 0) {
      let tablaCarrito = document.createElement("table");

      let encabezados =
        "<thead><tr><th>Codigo</th><th>Nombre</th><th>Cantidad</th><th>Precio</th><th>Subtotal</th></tr></thead>";
      tablaCarrito.innerHTML = encabezados;

      // Crear cuerpo de tabla
      let cuerpoTabla = document.createElement("tbody");

      // Recorrer los productos en el carrito y agregarlos a la tabla
      carrito.forEach((producto) => {
        let fila = document.createElement("tr");

        let codigo = document.createElement("td");
        codigo.textContent = producto.codigo;

        let nombreProducto = document.createElement("td");
        nombreProducto.textContent = producto.nombre;

        let cantidad = document.createElement("td");
        cantidad.textContent = producto.cantidad;

        let precioUnitario = document.createElement("td");
        precioUnitario.textContent = producto.precio;

        let subtotal = document.createElement("td");
        // Calcular el subtotal para este producto
        let subtotalProducto = producto.cantidad * producto.precio;
        subtotal.textContent = subtotalProducto;

        fila.appendChild(codigo);
        fila.appendChild(nombreProducto);
        fila.appendChild(cantidad);
        fila.appendChild(precioUnitario);
        fila.appendChild(subtotal);

        cuerpoTabla.appendChild(fila);
      });

      tablaCarrito.appendChild(cuerpoTabla);

      // Crear fila para mostrar el precio total del carrito
      let filaSubtotal = document.createElement("tr");
      let filaIVA = document.createElement("tr");
      let filaTotal = document.createElement("tr");

      let total = document.querySelector("[name='total']").value;
      let subtotal = document.querySelector("[name='subtotal']").value;
      let iva = document.querySelector("[name='impuestos']").value;

      filaSubtotal.innerHTML = `<td colspan="3">&nbsp;</td><td><strong>Sub Total:</strong></td><td>${subtotal}</td>`;
      filaIVA.innerHTML = `<td colspan="3">&nbsp;</td><td><strong>IVA:</strong></td><td>${iva}</td>`;
      filaTotal.innerHTML = `<td colspan="3">&nbsp;</td><td><strong>Total:</strong></td><td>${total}</td>`;

      cuerpoTabla.appendChild(filaSubtotal);
      cuerpoTabla.appendChild(filaIVA);
      cuerpoTabla.appendChild(filaTotal);

      return tablaCarrito;
    }
  }

  btnPdfVenta.addEventListener("click", (e) => {
    const carrito = obtenerCarritoDesdeLocalStorage();

    document.getElementById("carrito-input").value = JSON.stringify(carrito);

    const tabla = crearTablaBoleta();

    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    const tableTitle = "Boleta";

    doc.text(tableTitle, 95, 20);

    let startY = 30;
    doc.autoTable({ html: tabla, startY });

    doc.output("dataurlnewwindow");

    document.getElementById("formDatosVenta").submit();
  });

  function obtenerCarritoDesdeLocalStorage() {
    const carritoString = localStorage.getItem("carrito");
    const carrito = JSON.parse(carritoString) || [];
    return carrito;
  }
});