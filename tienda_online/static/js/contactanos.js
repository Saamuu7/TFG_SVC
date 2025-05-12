document.addEventListener("DOMContentLoaded", function () {
    const formulario = document.getElementById("form-contacto");

    formulario.addEventListener("submit", function (e) {
        e.preventDefault(); // Evita que se recargue la página

        // Aquí podrías hacer una petición AJAX si quisieras
        // Por ahora simplemente mostramos el mensaje
        alert("✅ ¡Tu formulario ha sido enviado correctamente!");

        formulario.reset(); // Limpia los campos del formulario (opcional)
    });
});

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
