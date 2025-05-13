// Comprobar si hay una imagen guardada en localStorage al cargar la página
window.onload = function() {
    const storedImage = localStorage.getItem("profileImage");
    if (storedImage) {
        document.getElementById("profile-pic").src = storedImage;
    }
};

// Cambiar la imagen y guardarla en localStorage
document.getElementById("profile-upload").addEventListener("change", function(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const imageDataUrl = e.target.result;
            // Guardar la imagen en localStorage
            localStorage.setItem("profileImage", imageDataUrl);
            document.getElementById("profile-pic").src = imageDataUrl;
        }
        reader.readAsDataURL(file);
    }
});

// Mostrar/ocultar secciones de configuración
document.addEventListener('DOMContentLoaded', function() {
    const options = document.querySelectorAll('.config-option');
    const contentSections = document.querySelectorAll('.config-content');
    
    // Ocultar todas las secciones inicialmente
    contentSections.forEach(section => {
        section.style.display = 'none';
    });

    // Función para mostrar la sección correspondiente
    function showSection(targetId) {
        contentSections.forEach(section => {
            section.style.display = 'none';
        });

        const targetSection = document.getElementById(targetId);
        if (targetSection) {
            targetSection.style.display = 'block';
        }
    }

    // Añadir event listener a cada opción de la lista
    options.forEach(option => {
        option.addEventListener('click', function() {
            const targetId = option.getAttribute('data-target');
            showSection(targetId);
        });
    });

    // Mostrar la primera sección por defecto
    if (options.length > 0) {
        showSection(options[0].getAttribute('data-target'));
    }
});

// Manejo de metodos de pago
document.addEventListener('DOMContentLoaded', function() {
    const paymentList = document.getElementById('payment-list');
    const addPaymentBtn = document.getElementById('add-payment-btn');
    const paymentForm = document.getElementById('payment-form');
    const savePaymentBtn = document.getElementById('save-payment-btn');
    
    let payments = JSON.parse(localStorage.getItem('payments')) || [];

    // Función para actualizar la lista de pagos
    function updatePaymentList() {
        paymentList.innerHTML = ''; // Limpiar lista
        payments.forEach((payment, index) => {
            const li = document.createElement('li');
            li.classList.add('payment-item');
            
            // Mostrar los últimos 4 dígitos de la tarjeta y la fecha de caducidad
            li.innerHTML = `
                <span>**** **** **** ${payment.cardNumber.slice(-4)} - ${payment.expiryDate}</span>
                <button class="delete-payment-btn" data-index="${index}">
                    Eliminar
                </button>
            `;
            
            paymentList.appendChild(li);
        });
        addPaymentBtn.disabled = payments.length >= 2;
    }

    // Mostrar formulario para agregar tarjeta
    addPaymentBtn.addEventListener('click', function() {
        paymentForm.style.display = 'block';
    });

// Guardar un nuevo método de pago
savePaymentBtn.addEventListener('click', function() {
    const cardNumber = document.getElementById('card-number').value;
    const expiryDate = document.getElementById('expiry-date').value;
    const cvv = document.getElementById('cvv').value;

    if (cardNumber.length === 16 && cvv.length === 3) {
        // Obtener el id del usuario (puedes modificar esta línea según tu lógica de usuario)
        const userId = 1; // Este valor debe ser dinámico, dependiendo del usuario logueado

        // Hacer una solicitud POST para guardar la tarjeta en la base de datos
        fetch('/agregar_tarjeta', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                numero: cardNumber,
                fecha_caducidad: expiryDate,
                cvv: cvv,
                id_usuario: userId
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                payments.push({ cardNumber, expiryDate });
                localStorage.setItem('payments', JSON.stringify(payments));
                updatePaymentList();
                paymentForm.reset();
                paymentForm.style.display = 'none';
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Hubo un error al guardar la tarjeta.');
        });
    } else {
        alert('Datos inválidos. Verifica la información ingresada.');
    }
});


    // Eliminar un método de pago
    paymentList.addEventListener('click', function(event) {
        if (event.target && event.target.classList.contains('delete-payment-btn')) {
            const index = event.target.getAttribute('data-index');
            payments.splice(index, 1); // Eliminar la tarjeta de la lista
            localStorage.setItem('payments', JSON.stringify(payments)); // Actualizar almacenamiento
            updatePaymentList(); // Actualizar la lista de pagos mostrada
        }
    });

    updatePaymentList(); // Inicializar la lista de pagos
});

// Manejo de la privacidad
document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("privacy-settings");
    const checkboxes = document.querySelectorAll("input[type='checkbox']");
    
    // Verifica que el formulario existe antes de trabajar con él
    if (!form) {
        console.error("Formulario no encontrado. Asegúrate de que el ID es 'privacy-settings'");
        return;
    }

    // Cargar configuración guardada
    checkboxes.forEach(checkbox => {
        const savedValue = localStorage.getItem(checkbox.name);
        if (savedValue === "true") {  // Si el valor guardado es "true", marca el checkbox
            checkbox.checked = true;
        } else if (savedValue === "false") {  // Si es "false", desmarca el checkbox
            checkbox.checked = false;
        }
    });

    // Guardar configuración al hacer submit
    form.addEventListener("submit", function(event) {
        event.preventDefault();
        checkboxes.forEach(checkbox => {
            localStorage.setItem(checkbox.name, checkbox.checked);  // Guardar el estado (checked) de cada checkbox
        });
        alert("Configuración guardada correctamente.");
    });
});


// Manejo de la visibilidad
document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("visibility-settings");
    const radios = document.querySelectorAll("input[type='radio']");
    const button = document.querySelector("button");

    // Cargar configuración guardada
    radios.forEach(radio => {
        const savedValue = localStorage.getItem(radio.name);
        if (savedValue && radio.value === savedValue) {
            radio.checked = true;
        }
    });

    // Guardar configuración al hacer submit
    form.addEventListener("submit", function(event) {
        event.preventDefault();
        radios.forEach(radio => {
            if (radio.checked) {
                localStorage.setItem(radio.name, radio.value);
            }
        });
        alert("Configuración guardada correctamente.");
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


