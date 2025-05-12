document.addEventListener('DOMContentLoaded', function () {

    // Inicializar variables
    const inputCodigo = document.getElementById('codigo-descuento');
    const btnCanjear = document.getElementById('btn-canjear');
    const btnFinalizarCompra = document.getElementById("btn-finalizar-compra");

    // Asegúrate de que el descuento se restablezca cada vez que entras en el carrito
    restablecerDescuento();

    // // Evento para aplicar código de descuento
    // btnCanjear.addEventListener('click', function () {
    //     const codigo = inputCodigo.value.trim();

    //     if (codigo === 'SS2025') {
    //         aplicarDescuento(15);
    //         inputCodigo.style.backgroundColor = '#d4edda'; // Verde claro
    //         inputCodigo.disabled = true;
    //         btnCanjear.disabled = true;
    //         // Guardar el estado del descuento en localStorage para que persista
    //         localStorage.setItem('descuento_aplicado', 'true');
    //     } else {
    //         alert('Código no válido');
    //     }
    // });

    // Aplicar descuento al total
    function aplicarDescuento(porcentaje) {
        let precioActual = parseFloat(document.getElementById('precio-carrito').textContent.replace('€', '').trim());
        let descuento = precioActual * (porcentaje / 100);
        let precioFinal = precioActual - descuento;

        document.getElementById('descuento').textContent = '-' + descuento.toFixed(2) + '€';
        document.getElementById('precio-total').textContent = precioFinal.toFixed(2) + '€';
    }

    // Restablecer el descuento al cargar la página o cuando se sale del carrito
    function restablecerDescuento() {
        // Verificar si hay un descuento aplicado guardado en localStorage
        const descuentoAplicado = localStorage.getItem('descuento_aplicado');

        // Si el descuento ha sido aplicado, lo restablecemos al entrar en el carrito
        if (descuentoAplicado === 'true') {
            inputCodigo.value = ''; // Limpiar el código de descuento
            inputCodigo.disabled = false; // Habilitar el campo para nuevos códigos
            btnCanjear.disabled = false; // Habilitar el botón
            document.getElementById('descuento').textContent = '0€'; // Restablecer el descuento
            document.getElementById('precio-total').textContent = document.getElementById('precio-carrito').textContent; // Restablecer precio
            // Eliminar el valor guardado de descuento en localStorage
            localStorage.removeItem('descuento_aplicado');
        }
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

    // Cargar productos del carrito en la vista
    function cargarCarrito() {
        const contenedor = document.querySelector('.productos-lista');
        let carrito = JSON.parse(localStorage.getItem("carrito")) || [];

        if (carrito.length === 0) {
            contenedor.innerHTML = '<p>Tu carrito está vacío.</p>';
            return;
        }

        contenedor.innerHTML = '';  // Limpiar la lista antes de agregar los nuevos productos

        carrito.forEach((producto, index) => {
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

            contenedor.appendChild(item);
        });

        inicializarEventos();
        actualizarTotal();
    }

    // Inicializar eventos de botones
    function inicializarEventos() {
        // Eliminar producto
        document.querySelectorAll('.eliminar').forEach(boton => {
            boton.addEventListener('click', function (e) {
                e.preventDefault();
                const index = Array.from(document.querySelectorAll('.eliminar')).indexOf(this);
                let carrito = JSON.parse(localStorage.getItem("carrito")) || [];
                carrito.splice(index, 1);
                localStorage.setItem("carrito", JSON.stringify(carrito));
                cargarCarrito();
            });
        });

        // Cambiar cantidad
        document.querySelectorAll('.btn-cantidad').forEach(boton => {
            boton.addEventListener('click', function () {
                const esSuma = this.textContent === '+';
                const item = this.closest('.item');
                const index = Array.from(document.querySelectorAll('.item')).indexOf(item);
                let carrito = JSON.parse(localStorage.getItem("carrito")) || [];

                if (esSuma) {
                    carrito[index].cantidad++;
                } else if (carrito[index].cantidad > 1) {
                    carrito[index].cantidad--;
                }

                localStorage.setItem("carrito", JSON.stringify(carrito));
                item.querySelector('span').textContent = carrito[index].cantidad;
                actualizarTotal();
            });
        });
    }

    // Cargar productos al iniciar
    cargarCarrito();

    // Vaciar carrito al finalizar compra
    btnFinalizarCompra.addEventListener("click", function (e) {
        e.preventDefault();

        const confirmar = confirm("¿Estás seguro de que quieres finalizar la compra?");

        if (confirmar) {
            localStorage.removeItem("carrito");  // Vacía el carrito
            window.location.href = "{{ url_for('finalizar_compra') }}";  // Redirige
        }
    });
});
