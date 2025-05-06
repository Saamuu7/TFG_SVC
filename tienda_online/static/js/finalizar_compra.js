document.addEventListener('DOMContentLoaded', function() {
    cargarCarrito();  // Cargar carrito al cargar la página

    // Función para cargar el carrito
    function cargarCarrito() {
        let carrito = JSON.parse(localStorage.getItem("carrito")) || [];

        const contenedor = document.querySelector('.productos-lista');
        contenedor.innerHTML = ''; // Limpiar el contenedor antes de añadir nuevos productos

        if (carrito.length === 0) {
            const mensaje = document.createElement('p');
            mensaje.textContent = "No hay productos en el carrito.";
            contenedor.appendChild(mensaje);
        } else {
            carrito.forEach(producto => {
                const item = document.createElement('div');
                item.classList.add('item');
                item.innerHTML = `
                    <div class="item-info">
                        <div class="imagen">
                            <img src="${producto.imagen}" alt="${producto.nombre}" style="width: 100px;">
                        </div>
                        <div class="descripcion">
                            <p><strong>${producto.nombre}</strong></p>
                            <p class="precio-producto">${producto.precio}€</p>
                            <p>Talla: ${producto.talla}</p>
                            <p>Cantidad: ${producto.cantidad}</p>
                        </div>
                    </div>
                `;
                contenedor.appendChild(item);
            });
        }

        actualizarTotal(carrito);  // Actualizar el total del carrito
    }

    // Función para actualizar el total del carrito
    function actualizarTotal(carrito) {
        let total = 0;
        carrito.forEach(producto => {
            total += producto.precio * producto.cantidad;
        });
        document.getElementById('total-carrito').textContent = total.toFixed(2) + "€";
    }
});


