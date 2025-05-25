// Función para actualizar el contador del carrito con el total de productos
function actualizarContadorCarrito() {
    const contador = document.getElementById("contador-carrito");
    const carrito = JSON.parse(localStorage.getItem("carrito")) || [];

    // Calcular el total de productos
    let totalProductos = 0;
    carrito.forEach(producto => {
        totalProductos += producto.cantidad; // Sumar las cantidades de cada producto
    });

    if (totalProductos === 0) {
        contador.style.display = "none";
    } else {
        contador.innerText = totalProductos; // Mostrar el total de productos
        contador.style.display = "inline-block";
    }
}

// Llamar al cargar la página para inicializar el contador
document.addEventListener("DOMContentLoaded", actualizarContadorCarrito);

// Modificar la función agregarAlCarrito para actualizar correctamente las cantidades
function agregarAlCarrito(nombre, precio, talla, imagen) {
    let carrito = JSON.parse(localStorage.getItem("carrito")) || [];

    // Verificar si el producto ya está en el carrito
    let productoExistente = carrito.find(producto => producto.nombre === nombre && producto.talla === talla);

    if (productoExistente) {
        // Si el producto ya está en el carrito, incrementar la cantidad
        productoExistente.cantidad += 1;
    } else {
        // Si no está, agregarlo con cantidad 1
        let producto = {
            nombre: nombre,
            precio: parseFloat(precio),
            talla: talla,
            imagen: imagen,
            cantidad: 1
        };
        carrito.push(producto);
    }

    // Guardar el carrito actualizado en localStorage
    localStorage.setItem("carrito", JSON.stringify(carrito));

    alert(`${nombre} añadido al carrito`);

    // Actualizar el contador
    actualizarContadorCarrito(); // 👈 Llamada para actualizar contador
}

document.addEventListener("DOMContentLoaded", () => {
  const botones = document.querySelectorAll(".btn-inscribirse");

  // Función para guardar inscripción con fecha de expiración (1 semana)
  function guardarInscripcion(id) {
    const expiracion = new Date().getTime() + 7 * 24 * 60 * 60 * 1000; // 1 semana en ms
    localStorage.setItem(`inscrito_${id}`, expiracion);
  }

  // Función para verificar si la inscripción sigue vigente
  function estaInscrito(id) {
    const expiracion = localStorage.getItem(`inscrito_${id}`);
    if (!expiracion) return false;
    return new Date().getTime() < parseInt(expiracion);
  }

  botones.forEach((boton, index) => {
    // Usa un id para cada botón. Aquí uso el índice, pero puedes usar otro identificador único
    const botonId = index;

    // Al cargar la página, verifica si el botón está "inscrito"
    if (estaInscrito(botonId)) {
      boton.classList.add("inscrito");
      boton.innerText = "¡Inscrito!";
    }

    boton.addEventListener("click", function(event) {
      event.preventDefault();
      guardarInscripcion(botonId);
      this.classList.add("inscrito");
      this.innerText = "¡Inscrito!";
    });
  });
});

