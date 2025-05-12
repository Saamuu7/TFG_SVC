// Función para abrir el modal
function abrirModal(imagen, nombre, precio, talla) {
    console.log("Abriendo modal con datos: ", imagen, nombre, precio, talla); // Verificar si los datos están bien pasados

    // Mostrar el modal
    document.getElementById("miModal").style.display = "block";
    
    // Rellenar el modal con los datos del producto
    document.getElementById("modalImagen").src = imagen;
    document.getElementById("modalNombre").innerText = nombre;
    document.getElementById("modalPrecio").innerText = precio;
    document.getElementById("modalTalla").innerText = talla;
}

// Función para cerrar el modal
function cerrarModal() {
    // Ocultar el modal
    document.getElementById("miModal").style.display = "none";
}

// Cerrar el modal si se hace clic fuera de la ventana
window.onclick = function(event) {
    if (event.target == document.getElementById("miModal")) {
        cerrarModal();
    }
}

//Añadir al carrito
function agregarAlCarrito(nombre, precio, talla, imagen) {
    let carrito = JSON.parse(localStorage.getItem("carrito")) || [];

    let producto = {
        nombre: nombre,
        precio: parseFloat(precio),
        talla: talla,
        imagen: imagen,
        cantidad: 1  // ← Muy importante asegurarse que es número, no undefined/null
    };

    carrito.push(producto);
    localStorage.setItem("carrito", JSON.stringify(carrito));
    alert(`${nombre} añadido al carrito`);
}

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

// Script para búsqueda y ordenación
function filtrarProductos() {
    const input = document.getElementById('busqueda').value.toLowerCase();
    const productos = document.querySelectorAll('.producto');

    productos.forEach(producto => {
        const nombre = producto.dataset.nombre.toLowerCase();
        producto.style.display = nombre.includes(input) ? 'block' : 'none';
    });
}

function ordenarProductos() {
    const orden = document.getElementById('orden').value;
    const contenedor = document.getElementById('productosContainer');
    const productos = Array.from(contenedor.getElementsByClassName('producto'));

    productos.sort((a, b) => {
        const nombreA = a.dataset.nombre.toLowerCase();
        const nombreB = b.dataset.nombre.toLowerCase();
        const precioA = parseFloat(a.dataset.precio);
        const precioB = parseFloat(b.dataset.precio);

        switch (orden) {
            case 'precio_asc': return precioA - precioB;
            case 'precio_desc': return precioB - precioA;
            case 'nombre_az': return nombreA.localeCompare(nombreB);
            case 'nombre_za': return nombreB.localeCompare(nombreA);
            default: return 0;
        }
    });

    productos.forEach(p => contenedor.appendChild(p));
}

