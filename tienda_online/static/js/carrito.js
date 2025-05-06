document.addEventListener('DOMContentLoaded', function() {

    // Función para eliminar productos
    const botonesEliminar = document.querySelectorAll('.eliminar');
    botonesEliminar.forEach(boton => {
        boton.addEventListener('click', function(e) {
            e.preventDefault();
            const item = this.closest('.item');
            const index = Array.from(document.querySelectorAll('.eliminar')).indexOf(this);

            let carrito = JSON.parse(localStorage.getItem("carrito")) || [];
            carrito.splice(index, 1); // Eliminar el producto del carrito
            localStorage.setItem("carrito", JSON.stringify(carrito)); // Guardar cambios en el localStorage

            cargarCarrito(); // Recargar el carrito actualizado
        });
    });

    // Función para aplicar código de descuento
    const btnCanjear = document.getElementById('btn-canjear');
    btnCanjear.addEventListener('click', function() {
        const codigo = document.getElementById('codigo-descuento').value.trim();
        const inputCodigo = document.getElementById('codigo-descuento');

        if (codigo === 'SS2025') {
            aplicarDescuento(15);
            inputCodigo.style.backgroundColor = '#d4edda'; // Fondo verde claro
            inputCodigo.disabled = true; // Deshabilitar el campo de texto
            btnCanjear.disabled = true; // Deshabilitar el botón de canjear
        } else {
            alert('Código no válido');
        }
    });

    function aplicarDescuento(porcentaje) {
        let precioActual = parseFloat(document.getElementById('precio-carrito').textContent.replace('€', '').trim());
        let descuento = precioActual * (porcentaje / 100);
        let precioFinal = precioActual - descuento;

        document.getElementById('descuento').textContent = '-' + descuento.toFixed(2) + '€';
        document.getElementById('precio-total').textContent = precioFinal.toFixed(2) + '€';
    }

    // Actualizar el total del carrito
    function actualizarTotal() {
        let carrito = JSON.parse(localStorage.getItem("carrito")) || [];
        let subtotal = 0;

        carrito.forEach(producto => {
            subtotal += producto.precio * producto.cantidad;
        });

        document.getElementById('precio-carrito').textContent = subtotal.toFixed(2) + '€';
        document.getElementById('precio-total').textContent = subtotal.toFixed(2) + '€';
        document.getElementById('descuento').textContent = '0€';
    }

    // Cargar carrito
    function cargarCarrito() {
        const contenedor = document.querySelector('.carrito-productos');
        let carrito = JSON.parse(localStorage.getItem("carrito")) || [];
    
        // Mantener el título, solo actualizar los productos
        const productosContenedor = contenedor.querySelector('.productos-lista') || document.createElement('div');
        productosContenedor.classList.add('productos-lista');
        productosContenedor.innerHTML = '';  // Limpiar solo la lista de productos
    
        carrito.forEach((producto, index) => {
            // Asegurarse de que la cantidad está bien definida
            if (!producto.cantidad || isNaN(producto.cantidad)) {
                producto.cantidad = 1;
            }
    
            const item = document.createElement('div');
            item.className = 'item';
    
            item.innerHTML = `
                <div class="item-info">
                    <div class="imagen">
                        <img src="${producto.imagen}" alt="${producto.nombre}" style="width: 100px;">
                    </div>
                    <div class="descripcion">
                        <p><strong>${producto.nombre}</strong></p>
                        <p class="precio-producto">${producto.precio.toFixed(2)}€</p>
                        <p>${producto.talla} | #${index + 1}</p>
                        <a href="#" class="eliminar">Eliminar</a>
                    </div>
                </div>
                <div class="item-cantidad">
                    <button class="btn-cantidad">+</button>
                    <span>${producto.cantidad}</span>
                    <button class="btn-cantidad">-</button>
                </div>
            `;
    
            productosContenedor.appendChild(item);
        });
    
        contenedor.appendChild(productosContenedor);  // Añadir los productos al contenedor
        inicializarEventos(); // Inicializar los eventos para los botones de eliminar y cantidad
        actualizarTotal(); // Actualizar el total después de cargar el carrito
    }
    

    function inicializarEventos() {
        // Botón eliminar
        document.querySelectorAll('.eliminar').forEach(boton => {
            boton.addEventListener('click', function(e) {
                e.preventDefault();
                const index = Array.from(document.querySelectorAll('.eliminar')).indexOf(this);
                let carrito = JSON.parse(localStorage.getItem("carrito")) || [];
                carrito.splice(index, 1); // Eliminar el producto del carrito
                localStorage.setItem("carrito", JSON.stringify(carrito)); // Guardar cambios en el localStorage
                cargarCarrito(); // Recargar el carrito actualizado
            });
        });

        // Botón cantidad (+ y -)
        document.querySelectorAll('.btn-cantidad').forEach(boton => {
            boton.addEventListener('click', function() {
                const esSuma = this.textContent === '+'; // Determinar si es "+" o "-"
                const item = this.closest('.item');
                const index = Array.from(document.querySelectorAll('.item')).indexOf(item);

                let carrito = JSON.parse(localStorage.getItem("carrito")) || [];

                // Aumentar o disminuir la cantidad
                if (esSuma) {
                    carrito[index].cantidad++;
                } else if (carrito[index].cantidad > 1) {
                    carrito[index].cantidad--;
                }

                // Actualizar carrito en localStorage
                localStorage.setItem("carrito", JSON.stringify(carrito));

                // Actualizar la cantidad en el DOM sin recargar el carrito
                item.querySelector('span').textContent = carrito[index].cantidad;

                // Actualizar el total dinámicamente
                actualizarTotal();
            });
        });
    }

    cargarCarrito(); // Cargar el carrito al cargar la página
});

document.getElementById("btn-finalizar-compra").addEventListener("click", function() {
    window.location.href = "{{ url_for('finalizar_compra') }}";
});

