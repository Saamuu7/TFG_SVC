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
        let subtotal = 0;
        carrito.forEach(producto => {
            subtotal += producto.precio * producto.cantidad;
        });
    
        // Obtener descuento desde localStorage o poner 0 si no existe
        let descuentoPorcentaje = parseFloat(localStorage.getItem("descuentoAplicado")) || 0;
        let descuento = subtotal * (descuentoPorcentaje / 100);
        let totalFinal = subtotal - descuento;
    
        document.getElementById('total-carrito').textContent = totalFinal.toFixed(2) + "€";
    }

    document.getElementById('pagar').addEventListener('click', function () {
        localStorage.removeItem('descuentoAplicado');
        // Aquí puedes redirigir o mostrar un mensaje de éxito
    });
    
    
    
});

document.addEventListener('DOMContentLoaded', () => {
    const radioTarjeta = document.getElementById('payment-method-card');
    const radioPaypal = document.getElementById('payment-method-paypal');
    const paypalFields = document.querySelector('.paypal-fields');
    const tarjetaFields = document.querySelector('.tarjeta-fields');

    function toggleCamposPago() {
        if (radioTarjeta.checked) {
            tarjetaFields.style.display = 'block';
            paypalFields.style.display = 'none';
        } else if (radioPaypal.checked) {
            tarjetaFields.style.display = 'none';
            paypalFields.style.display = 'block';
        }
    }

    radioTarjeta.addEventListener('change', toggleCamposPago);
    radioPaypal.addEventListener('change', toggleCamposPago);

    // Inicializar al cargar la página
    toggleCamposPago();
});

    //Para que aparezca el paypal
document.addEventListener('DOMContentLoaded', () => {
    const radioTarjeta = document.getElementById('payment-method-card');
    const radioPaypal = document.getElementById('payment-method-paypal');
    const paypalFields = document.querySelector('#paypal-fields');  // Corregido
    const tarjetaFields = document.querySelector('#tarjeta-fields');  // Corregido

    function toggleCamposPago() {
        if (radioTarjeta.checked) {
            tarjetaFields.style.display = 'block';
            paypalFields.style.display = 'none';
        } else if (radioPaypal.checked) {
            tarjetaFields.style.display = 'none';
            paypalFields.style.display = 'block';
        }
    }

    radioTarjeta.addEventListener('change', toggleCamposPago);
    radioPaypal.addEventListener('change', toggleCamposPago);

    toggleCamposPago(); // Ejecutar al inicio
});

    



