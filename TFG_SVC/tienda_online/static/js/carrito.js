document.addEventListener('DOMContentLoaded', function () {

    const contenedor = document.querySelector('.carrito-productos');
    let carrito = JSON.parse(localStorage.getItem("carrito")) || [];

    function guardarCarrito() {
        localStorage.setItem("carrito", JSON.stringify(carrito));
    }

    function actualizarTotal() {
        let subtotal = 0;
        carrito.forEach(producto => {
            subtotal += producto.precio * producto.cantidad;
        });

        let descuentoAplicado = localStorage.getItem("descuentoAplicado");
        let descuento = descuentoAplicado ? subtotal * (parseFloat(descuentoAplicado) / 100) : 0;
        let total = subtotal - descuento;

        document.getElementById('precio-carrito').textContent = subtotal.toFixed(2) + '€';
        document.getElementById('descuento').textContent = descuento ? '-' + descuento.toFixed(2) + '€' : '0€';
        document.getElementById('precio-total').textContent = total.toFixed(2) + '€';
    }

    function cargarCarrito() {
        const productosContenedor = document.createElement('div');
        productosContenedor.classList.add('productos-lista');
        productosContenedor.innerHTML = '';

        carrito.forEach((producto, index) => {
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
                    <button class="btn-cantidad" data-accion="sumar" data-index="${index}">+</button>
                    <span>${producto.cantidad}</span>
                    <button class="btn-cantidad" data-accion="restar" data-index="${index}">-</button>
                </div>
            `;
            productosContenedor.appendChild(item);
        });

        const existente = contenedor.querySelector('.productos-lista');
        if (existente) {
            contenedor.replaceChild(productosContenedor, existente);
        } else {
            contenedor.appendChild(productosContenedor);
        }

        activarBotones();
        actualizarTotal();
    }

    function activarBotones() {
        // Eliminar
        const botonesEliminar = document.querySelectorAll('.eliminar');
        botonesEliminar.forEach((btn, index) => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                carrito.splice(index, 1);
                guardarCarrito();
                cargarCarrito();
            });
        });

        // Botones de cantidad
        const botonesCantidad = document.querySelectorAll('.btn-cantidad');
        botonesCantidad.forEach(btn => {
            btn.addEventListener('click', () => {
                const index = parseInt(btn.getAttribute('data-index'));
                const accion = btn.getAttribute('data-accion');
                if (accion === 'sumar') {
                    carrito[index].cantidad++;
                } else if (accion === 'restar' && carrito[index].cantidad > 1) {
                    carrito[index].cantidad--;
                }
                guardarCarrito();
                cargarCarrito();
            });
        });
    }

    // Aplicar código de descuento
    document.getElementById('btn-canjear').addEventListener('click', function () {
        const codigo = document.getElementById('codigo-descuento').value.trim();
        const inputCodigo = document.getElementById('codigo-descuento');

        if (codigo === 'SS2025') {
            localStorage.setItem("descuentoAplicado", 15);
            inputCodigo.style.backgroundColor = '#d4edda';
            inputCodigo.disabled = true;
            this.disabled = true;
            actualizarTotal();
        } else {
            alert('Código no válido');
        }
    });

    // Comprobación descuento ya aplicado
    if (localStorage.getItem("descuentoAplicado")) {
        const input = document.getElementById('codigo-descuento');
        input.value = 'SS2025';
        input.style.backgroundColor = '#d4edda';
        input.disabled = true;
        document.getElementById('btn-canjear').disabled = true;
    }

    cargarCarrito();
});

// Vaciar carrito si el usuario abandona la página, salvo que vaya a finalizar compra
window.addEventListener('beforeunload', function (e) {
    // Verificamos si el enlace que hizo salir al usuario fue "Finalizar Compra"
    const linkFinalizar = document.activeElement;
    
    if (
        linkFinalizar &&
        linkFinalizar.id === 'btn-finalizar-compra'
    ) {
        // No vaciamos el carrito si se va a finalizar compra
        return;
    }

    // Si no va a finalizar compra, vaciamos el carrito
    localStorage.removeItem("carrito");
    localStorage.removeItem("descuentoAplicado");
});

