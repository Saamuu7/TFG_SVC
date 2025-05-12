import os, sys, platform
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtWebEngineWidgets import QWebEngineView

class Advertencia(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.setWindowTitle("Advertencia")
        botones = QDialogButtonBox.Close| QDialogButtonBox.Open

        self.caja_botones = QDialogButtonBox(botones)
        self.caja_botones.accepted.connect(self.accept)
        self.caja_botones.rejected.connect(self.reject)

        self.layout_advertencia = QVBoxLayout()
        self.layout_advertencia.addWidget(QLabel("¿Estás seguro de usar ese usuario? Si es así pulsa abrir..."))
        self.layout_advertencia.addWidget(self.caja_botones)
        self.setLayout(self.layout_advertencia)

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Inicio de sesión")
        #crea los campos de usuario y contraseña
        self.usuario_edit = QLineEdit()
        self.contraseña_edit = QLineEdit()
        self.contraseña_edit.setEchoMode(QLineEdit.Password)

        #crea los botones de inicio de sesión y cancelar
        self.inicio_boton = QPushButton("Iniciar Sesión")
        self.cancelar_boton = QPushButton("Cancelar")
        self.cancelar_boton.clicked.connect(self.close)

        #crea el diseño vertical para la ventana
        layout = QVBoxLayout()

        #crea el diseño horizontal para los campos de usuario y contraseña
        formulario_plantilla = QHBoxLayout()
        formulario_plantilla.addWidget(QLabel("Usuario: "))
        formulario_plantilla.addWidget(self.usuario_edit)
        formulario_plantilla.addWidget(QLabel("Contraseña: "))
        formulario_plantilla.addWidget(self.contraseña_edit)
        layout.addLayout(formulario_plantilla)

        #agrega los botones de inicio de sesión y cancelar
        boton_formulario = QHBoxLayout()
        boton_formulario.addWidget(self.inicio_boton)
        boton_formulario.addWidget(self.cancelar_boton)
        layout.addLayout(boton_formulario)

        self.setLayout(layout)

class RegisterWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registro")

        #campos de registro de usuario y contraseña
        self.usuario_redit = QLineEdit()
        self.contraseña_redit = QLineEdit()
        self.contraseña_redit.setEchoMode(QLineEdit.Password)

        #crear botones de registro y cancelar
        self.registro_boton = QPushButton("Registrarse")
        self.cancelar2_boton = QPushButton("Cancelar")
        self.cancelar2_boton.clicked.connect(self.close)

        #diseño del formulario
        plantilla = QVBoxLayout()
        formulario_plantilla2 = QHBoxLayout()
        formulario_plantilla2.addWidget(QLabel("Usuario: "))
        formulario_plantilla2.addWidget(self.usuario_redit)
        formulario_plantilla2.addWidget(QLabel("Contraseña: "))
        formulario_plantilla2.addWidget(self.contraseña_redit)
        plantilla.addLayout(formulario_plantilla2)

        #agregar botones
        boton_formulario2 = QHBoxLayout()
        boton_formulario2.addWidget(self.registro_boton)
        boton_formulario2.addWidget(self.cancelar2_boton)
        plantilla.addLayout(boton_formulario2)

        self.setLayout(plantilla)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reserva")
        
        plantilla_horizontal = QHBoxLayout()
        principal = QWidget()
        principal.setStyleSheet(f"Background-color: #44cccc")
        principal.setLayout(plantilla_horizontal)
        self.setCentralWidget(principal)
        fuente = QFont()
        fuente.setBold(True)

        #menubar
        self.barra = self.menuBar()
        menu = self.barra.addMenu("&Sitios Web")
        
        ##hoteles
        menu2 = menu.addMenu("&Hoteles")
        h1 = QAction("Ir a Four Seasons Hotel", self)
        h1.triggered.connect(self.h_fourseasons_web)
        h2 = QAction("Ir a Hotel Ritz", self)
        h2.triggered.connect(self.h_rits_web)
        h3 = QAction("Ir a Hotel Villa Magna", self)
        h3.triggered.connect(self.h_villamagna_web)
        menu2.addAction(h1)
        menu2.addAction(h2)
        menu2.addAction(h3)

        ##restaurantes
        menu3 = menu.addMenu("&Restaurantes")
        r1 = QAction("Ir a Restaurante Botín", self)
        r1.triggered.connect(self.r_botin_web)
        r2 = QAction("Ir a Restaurante Casa Mono", self)
        r2.triggered.connect(self.r_casamono_web)
        r3 = QAction("Ir a Restaurante La Vaca y la Huerta", self)
        r3.triggered.connect(self.r_vacahuerta_web)
        r4 = QAction("Ir a Restaurante StreetXO", self)
        r4.triggered.connect(self.r_streetxo_web)
        menu3.addAction(r1)
        menu3.addAction(r2)
        menu3.addAction(r3)
        menu3.addAction(r4)

        ##museos
        menu4 = menu.addMenu("&Museos")
        m1 = QAction("Ir a Museo del Prado", self)
        m1.triggered.connect(self.m_prado_web)
        m2 = QAction("Ir a Museo Nacional Centro de Arte Reina Sofía", self)
        m2.triggered.connect(self.m_nacionalsofia_web)
        m3 = QAction("Ir a Museo Thyssen-Bornemisza", self)
        m3.triggered.connect(self.m_thyssen_web)
        menu4.addAction(m1)
        menu4.addAction(m2)
        menu4.addAction(m3)

        ##atracciones
        menu5 = menu.addMenu("&Atracciones")
        a1 = QAction("Ir a Parque de Atracciones de Madrid", self)
        a1.triggered.connect(self.a_parqueatracciones_web)
        a2 = QAction("Ir a Parque Warner", self)
        a2.triggered.connect(self.a_warner_Web)
        menu5.addAction(a1)
        menu5.addAction(a2)

        ##ir a menú
        menu6 = self.barra.addMenu("&Ir a Menú")
        im = QAction("Ir a Menú", self)
        im.triggered.connect(self.menu)
        menu6.addAction(im)

        ##cerrar sesión
        menu7 = self.barra.addMenu("&Cerrar Sesión")
        cs = QAction("Cerrar Sesión", self)
        cs.triggered.connect(self.cerrar_sesion)
        menu7.addAction(cs)

        self.barra.setHidden(True)

        
        #inicio
        plantilla_inicio = QFormLayout()
        inicio = QWidget()
        inicio.setLayout(plantilla_inicio)
        registro_boton = QPushButton("Registrarse")
        registro_boton.setStyleSheet("color: white; background-color: black;")
        registro_boton.setFont(fuente)
        registro_boton.clicked.connect(self.mostrar_dialogo_de_registro)
        plantilla_inicio.addRow(registro_boton)
        inicio_boton = QPushButton("Iniciar Sesión")
        inicio_boton.setStyleSheet("color: white; background-color: black;")
        inicio_boton.setFont(fuente)
        inicio_boton.clicked.connect(self.mostrar_dialogo_de_inicio)
        plantilla_inicio.addRow(inicio_boton)
        salir = QPushButton("Salir")
        salir.setStyleSheet("color: white; background-color: black;")
        salir.setFont(fuente)
        salir.clicked.connect(self.cerrar)
        plantilla_inicio.addRow(salir)

        #menu
        formulario_eleccionr = QFormLayout()
        menu = QWidget()
        menu.setLayout(formulario_eleccionr)
        etiqueta1 = QLabel("MENÚ")
        etiqueta1.setStyleSheet("color: white;")
        etiqueta1.setFont(fuente)
        formulario_eleccionr.addRow(etiqueta1)
        plan_boton = QPushButton("Elige tu plan")
        plan_boton.setStyleSheet("color: white; background-color: black;")
        plan_boton.setFont(fuente)
        plan_boton.clicked.connect(self.eleccion)
        formulario_eleccionr.addRow(plan_boton)
        reserva_boton = QPushButton("Reservas")
        reserva_boton.setStyleSheet("color: white; background-color: black;")
        reserva_boton.setFont(fuente)
        reserva_boton.clicked.connect(self.reservas)
        formulario_eleccionr.addRow(reserva_boton)
        cerrar_sesion_boton = QPushButton("Cerrar Sesión")
        cerrar_sesion_boton.setStyleSheet("color: white; background-color: black;")
        cerrar_sesion_boton.setFont(fuente)
        cerrar_sesion_boton.clicked.connect(self.cerrar_sesion)
        formulario_eleccionr.addRow(cerrar_sesion_boton)

        
        #eleccion
        plantilla_eleccion = QFormLayout()
        eleccion = QWidget()
        eleccion.setLayout(plantilla_eleccion)

        eleccion_etiqueta = QLabel("Elige tu plan ideal: \n")
        eleccion_etiqueta.setStyleSheet("color: white;")
        eleccion_etiqueta.setFont(fuente)
        plantilla_eleccion.addRow(eleccion_etiqueta)

        hotel_eleccion = QLabel("Hoteles: ")
        hotel_eleccion.setStyleSheet("color: white;")
        hotel_eleccion.setFont(fuente)
        self.hotel_box = QComboBox()
        self.hotel_box.setStyleSheet("color: black; background-color: white;")
        self.hotel_box.setFont(fuente)
        self.hotel_box.setFixedSize(200, 40)
        plantilla_eleccion.addRow(hotel_eleccion, self.hotel_box)
        self.hotel_box.insertItem(0, "")
        self.hotel_box.addItems(["Hotel Four Seasons: 500€", "Hotel Ritz: 400€", "Hotel Villa Magna: 300€"])

        restaurante_eleccion = QLabel("Restaurantes: ")
        restaurante_eleccion.setStyleSheet("color: white;")
        restaurante_eleccion.setFont(fuente)
        self.restaurante_box = QComboBox()
        self.restaurante_box.setStyleSheet("color: black; background-color: white;")
        self.restaurante_box.setFont(fuente)
        self.restaurante_box.setFixedSize(200, 40)
        plantilla_eleccion.addRow(restaurante_eleccion, self.restaurante_box)
        self.restaurante_box.insertItem(0, "")
        self.restaurante_box.addItems(["Restaurante Botín: 60€", "Restaurante StreetXO: 50€", "Restaurante Casa Mono: 40€", "Restaurante La Vaca y La Huerta: 35€"])

        museo_eleccion = QLabel("Museos: ")
        museo_eleccion.setStyleSheet("color: white; ")
        museo_eleccion.setFont(fuente)
        self.museo_box = QComboBox()
        self.museo_box.setStyleSheet("color: black; background-color: white;")
        self.museo_box.setFont(fuente)
        self.museo_box.setFixedSize(200, 40)
        plantilla_eleccion.addRow(museo_eleccion, self.museo_box)
        self.museo_box.insertItem(0, "")
        self.museo_box.addItems(["Museo del Prado: 15€", "Museo Thyssen-Bornemisza: 13€", "Museo Nacional Centro de Arte Reina Sofia: 10€"])

        atraccion_eleccion = QLabel("Atracciones: ")
        atraccion_eleccion.setStyleSheet("color: white;")
        atraccion_eleccion.setFont(fuente)
        self.atracciones_box = QComboBox()
        self.atracciones_box.setStyleSheet("color: black; background-color: white;")
        self.atracciones_box.setFont(fuente)
        self.atracciones_box.setFixedSize(200, 40)
        plantilla_eleccion.addRow(atraccion_eleccion, self.atracciones_box)
        self.atracciones_box.insertItem(0, "")
        self.atracciones_box.addItems(["Parque Warner: 50€", "Parque de Atracciones: 30€" ])
        
        reserva_etiqueta = QLabel("Calcula tu plan ideal -->")
        reserva_etiqueta.setStyleSheet("color: white;")
        reserva_etiqueta.setFont(fuente)
        reserva_boton = QPushButton("RESERVAR")
        reserva_boton.setStyleSheet("color: white; background-color: black;")
        reserva_boton.setFont(fuente)
        reserva_boton.clicked.connect(self.reservar)
        plantilla_eleccion.addRow(reserva_etiqueta, reserva_boton)




        #reserva
        plantilla_reserva = QFormLayout()
        reserva = QWidget()
        reserva.setLayout(plantilla_reserva)
        datos_reserva_etiqueta = QLabel("Los Datos de la reserva son los siguientes: \n")
        datos_reserva_etiqueta.setStyleSheet("color: white;")
        datos_reserva_etiqueta.setFont(fuente)
        plantilla_reserva.addRow(datos_reserva_etiqueta)

        self.hotel_etiqueta1 = QLabel("Hotel elegido: ")
        self.hotel_etiqueta1.setStyleSheet("color: white;")
        self.hotel_etiqueta1.setFont(fuente)
        self.hotel_etiqueta2 = QLabel("Ninguno")
        self.hotel_etiqueta2.setStyleSheet("color: white;")
        self.hotel_etiqueta2.setFont(fuente)
        plantilla_reserva.addRow(self.hotel_etiqueta1, self.hotel_etiqueta2)

        self.restaurante_etiqueta1 = QLabel("Restaurante elegido: ")
        self.restaurante_etiqueta1.setStyleSheet("color: white;")
        self.restaurante_etiqueta1.setFont(fuente)
        self.restaurante_etiqueta2 = QLabel("Ninguno")
        self.restaurante_etiqueta2.setStyleSheet("color: white;")
        self.restaurante_etiqueta2.setFont(fuente)
        plantilla_reserva.addRow(self.restaurante_etiqueta1, self.restaurante_etiqueta2)

        self.museo_etiqueta1 = QLabel("Museo elegido: ")
        self.museo_etiqueta1.setStyleSheet("color: white;")
        self.museo_etiqueta1.setFont(fuente)
        self.museo_etiqueta2 = QLabel("Ninguno")
        self.museo_etiqueta2.setStyleSheet("color: white;")
        self.museo_etiqueta2.setFont(fuente)
        plantilla_reserva.addRow(self.museo_etiqueta1, self.museo_etiqueta2)

        self.atraccion_etiqueta1 = QLabel("Atracción elegida: ")
        self.atraccion_etiqueta1.setStyleSheet("color: white;")
        self.atraccion_etiqueta1.setFont(fuente)
        self.atraccion_etiqueta2 = QLabel("Ninguna")
        self.atraccion_etiqueta2.setStyleSheet("color: white;")
        self.atraccion_etiqueta2.setFont(fuente)
        plantilla_reserva.addRow(self.atraccion_etiqueta1, self.atraccion_etiqueta2)

        self.total_etiqueta1 = QLabel("Total del plan: ")
        self.total_etiqueta1.setStyleSheet("color: white;")
        self.total_etiqueta1.setFont(fuente)
        self.total_etiqueta2 = QLabel("0€")
        self.total_etiqueta2.setStyleSheet("color: white;")
        self.total_etiqueta2.setFont(fuente)
        plantilla_reserva.addRow(self.total_etiqueta1, self.total_etiqueta2)

        self.usuario_etiqueta1 = QLabel("Usuario en uso: ")
        self.usuario_etiqueta1.setStyleSheet("color: white;")
        self.usuario_etiqueta1.setFont(fuente)
        self.usuario_etiqueta2 = QLabel("")
        self.usuario_etiqueta2.setStyleSheet("color: white;")
        self.usuario_etiqueta2.setFont(fuente)
        plantilla_reserva.addRow(self.usuario_etiqueta1, self.usuario_etiqueta2)

        
        #WEBS
        ##hotel cuatro estaciones
        plantilla_web1 = QVBoxLayout()
        fourseasons_web = QWidget()
        fourseasons_web.setLayout(plantilla_web1)
        fourseasons_web.setFixedSize(1000, 700)

        self.vistaweb1 = QWebEngineView()
        self.vistaweb1.load(QUrl("https://www.fourseasons.com/es-es/madrid/"))

        self.plantilla_web1h = QHBoxLayout()

        plantilla_web1.addLayout(self.plantilla_web1h)
        plantilla_web1.addWidget(self.vistaweb1)

        ##hotel ritz
        plantilla_web2 = QVBoxLayout()
        ritz_web = QWidget()
        ritz_web.setLayout(plantilla_web2)
        ritz_web.setFixedSize(1000, 700)

        self.vistaweb2 = QWebEngineView()
        self.vistaweb2.load(QUrl("https://www.mandarinoriental.com/es-es/madrid/hotel-ritz"))

        self.plantilla_web2h = QHBoxLayout()

        plantilla_web2.addLayout(self.plantilla_web2h)
        plantilla_web2.addWidget(self.vistaweb2)

        ##hotel Villa Magna
        plantilla_web3 = QVBoxLayout()
        villamagna_web = QWidget()
        villamagna_web.setLayout(plantilla_web3)
        villamagna_web.setFixedSize(1000, 700)

        self.vistaweb3 = QWebEngineView()
        self.vistaweb3.load(QUrl("https://www.rosewoodhotels.com/es/villa-magna"))

        self.plantilla_web3h = QHBoxLayout()

        plantilla_web3.addLayout(self.plantilla_web3h)
        plantilla_web3.addWidget(self.vistaweb3)

        ##restaurante botin
        plantilla_web4 = QVBoxLayout()
        botin_web = QWidget()
        botin_web.setLayout(plantilla_web4)
        botin_web.setFixedSize(1000, 700)

        self.vistaweb4 = QWebEngineView()
        self.vistaweb4.load(QUrl("https://botin.es"))

        self.plantilla_web1r = QHBoxLayout()

        plantilla_web4.addLayout(self.plantilla_web1r)
        plantilla_web4.addWidget(self.vistaweb4)

        ##restaurante streexo
        plantilla_web5 = QVBoxLayout()
        streexo_web = QWidget()
        streexo_web.setLayout(plantilla_web5)
        streexo_web.setFixedSize(1000, 700)

        self.vistaweb5 = QWebEngineView()
        self.vistaweb5.load(QUrl("https://streetxo.com/madrid/"))

        self.plantilla_web2r = QHBoxLayout()

        plantilla_web5.addLayout(self.plantilla_web2r)
        plantilla_web5.addWidget(self.vistaweb5)

        ##restaurante casa mono
        plantilla_web6 = QVBoxLayout()
        casamono_web = QWidget()
        casamono_web.setLayout(plantilla_web6)
        casamono_web.setFixedSize(1000, 700)

        self.vistaweb6 = QWebEngineView()
        self.vistaweb6.load(QUrl("https://www.casamonomadrid.com"))

        self.plantilla_web3r = QHBoxLayout()

        plantilla_web6.addLayout(self.plantilla_web3r)
        plantilla_web6.addWidget(self.vistaweb6)

        ##restaurante vaca huerta
        plantilla_web7 = QVBoxLayout()
        vacahuerta_web = QWidget()
        vacahuerta_web.setLayout(plantilla_web7)
        vacahuerta_web.setFixedSize(1000, 700)

        self.vistaweb7 = QWebEngineView()
        self.vistaweb7.load(QUrl("https://lavacaylahuerta.com"))

        self.plantilla_web4r = QHBoxLayout()

        plantilla_web7.addLayout(self.plantilla_web4r)
        plantilla_web7.addWidget(self.vistaweb7)

        ##museo prado
        plantilla_web8 = QVBoxLayout()
        prado_web = QWidget()
        prado_web.setLayout(plantilla_web8)
        prado_web.setFixedSize(1000, 700)

        self.vistaweb8 = QWebEngineView()
        self.vistaweb8.load(QUrl("https://www.museodelprado.es"))

        self.plantilla_web1m = QHBoxLayout()

        plantilla_web8.addLayout(self.plantilla_web1m)
        plantilla_web8.addWidget(self.vistaweb8)

        ##museo sofia
        plantilla_web9 = QVBoxLayout()
        sofia_web = QWidget()
        sofia_web.setLayout(plantilla_web9)
        sofia_web.setFixedSize(1000, 700)

        self.vistaweb9 = QWebEngineView()
        self.vistaweb9.load(QUrl("https://www.museoreinasofia.es"))

        self.plantilla_web2m = QHBoxLayout()

        plantilla_web9.addLayout(self.plantilla_web2m)
        plantilla_web9.addWidget(self.vistaweb9)

        ##museo thyssen
        plantilla_web10 = QVBoxLayout()
        thyssen_web = QWidget()
        thyssen_web.setLayout(plantilla_web10)
        thyssen_web.setFixedSize(1000, 700)

        self.vistaweb10 = QWebEngineView()
        self.vistaweb10.load(QUrl("https://www.museothyssen.org"))

        self.plantilla_web3m = QHBoxLayout()

        plantilla_web10.addLayout(self.plantilla_web3m)
        plantilla_web10.addWidget(self.vistaweb10)

        ##atraccion warner
        plantilla_web11 = QVBoxLayout()
        warner_web = QWidget()
        warner_web.setLayout(plantilla_web11)
        warner_web.setFixedSize(1000, 700)

        self.vistaweb11 = QWebEngineView()
        self.vistaweb11.load(QUrl("https://www.parquewarner.com"))

        self.plantilla_web1a = QHBoxLayout()

        plantilla_web11.addLayout(self.plantilla_web1a)
        plantilla_web11.addWidget(self.vistaweb11)

        ##atraccion parque
        plantilla_web12 = QVBoxLayout()
        parque_web = QWidget()
        parque_web.setLayout(plantilla_web12)
        parque_web.setFixedSize(1000, 700)

        self.vistaweb12 = QWebEngineView()
        self.vistaweb12.load(QUrl("https://www.parquedeatracciones.es"))

        self.plantilla_web2a = QHBoxLayout()

        plantilla_web12.addLayout(self.plantilla_web2a)
        plantilla_web12.addWidget(self.vistaweb12)

        #ventanas
        self.capa = QStackedLayout()
        self.capa.addWidget(inicio)
        self.capa.addWidget(menu)
        self.capa.addWidget(eleccion)
        self.capa.addWidget(reserva)
        self.capa.addWidget(fourseasons_web)
        self.capa.addWidget(ritz_web)
        self.capa.addWidget(villamagna_web)
        self.capa.addWidget(botin_web)
        self.capa.addWidget(streexo_web)
        self.capa.addWidget(casamono_web)
        self.capa.addWidget(vacahuerta_web)
        self.capa.addWidget(prado_web)
        self.capa.addWidget(thyssen_web)
        self.capa.addWidget(sofia_web)
        self.capa.addWidget(warner_web)
        self.capa.addWidget(parque_web)
        plantilla_horizontal.addLayout(self.capa)



    def mostrar_dialogo_de_registro(self):
        #crear una instancia de la ventana de registro de sesión
        self.dialogo_registro = RegisterWindow()

        #conecta el botón de registro de sesion a la escritura
        self.dialogo_registro.registro_boton.clicked.connect(self.escribir)

        #muestra la ventana de inicio de sesion
        self.dialogo_registro.exec()


    def mostrar_dialogo_de_inicio(self):
        #crea una instancia de la ventana de inicio de sesion
        self.dialogo_inicio = LoginWindow()

        #conecta el botón de inicio de sesion a la funcion de verificacion de credenciales
        self.dialogo_inicio.inicio_boton.clicked.connect(self.comprobar_credenciales)

        #muestra la ventana de inicio de sesion
        self.dialogo_inicio.exec()

        
    def escribir(self):
        usuario = self.dialogo_registro.usuario_redit.text()
        contraseña = self.dialogo_registro.contraseña_redit.text()

        try:
            try:
                with open('datos.txt', 'r') as archivo:
                    for linea in archivo:
                        if linea.startswith(usuario + ';'):
                            raise Exception("El usuario ya existe")
            except FileNotFoundError:
                pass
            
            with open('datos.txt', 'a') as archivo:
                registro_texto = usuario + ';' + contraseña + '\n'
                archivo.write(registro_texto)
            
            self.dialogo_registro.accept()
        
        except Exception as e:
            QMessageBox.critical(self, "Error de creación de usuario", "El usuario ya existe", buttons=QMessageBox.Ok, defaultButton=QMessageBox.Ok)



    def comprobar_credenciales(self):
        try:
            comprobar = 0
            registro = open ('datos.txt', "r+")
            registro.seek(0)

            for linea in registro:
                user, passwd = linea.split(';')
                if self.dialogo_inicio.usuario_edit.text() == user and self.dialogo_inicio.contraseña_edit.text() + "\n" == passwd: 
                    comprobar = 1

            if comprobar == 1:
                translator = QTranslator(app)
                translations = QLibraryInfo.location(QLibraryInfo.TranslationsPath)
                translator.load("qt_es", translations)
                app.installTranslator(translator)
                ventana = Advertencia(self)
                resultado = ventana.exec()
                if resultado:
                    self.capa.setCurrentIndex(1)
                    print("Usuario de inicio correcto")
                    self.capa.setCurrentIndex(1)
                    self.dialogo_inicio.accept()
                    self.barra.setHidden(False)
                else:
                    print("")

            else:
                translator = QTranslator(app)
                translations = QLibraryInfo.location(QLibraryInfo.TranslationsPath)
                translator.load("qt_es", translations)
                app.installTranslator(translator)
                QMessageBox.critical(self, "Error de inicio de sesión", "El usuario y/o la contraseña no son válidos", buttons = QMessageBox.Discard, defaultButton = QMessageBox.Discard)

            registro.close()
        except FileNotFoundError:
            translator = QTranslator(app)
            translations = QLibraryInfo.location(QLibraryInfo.TranslationsPath)
            translator.load("qt_es", translations)
            app.installTranslator(translator)
            QMessageBox.critical(self, "Error", "El archivo 'datos.txt' no existe", buttons=QMessageBox.Discard, defaultButton=QMessageBox.Discard)

    def cerrar(self):
        QApplication.instance().quit()

    def cerrar_sesion(self):
        self.capa.setCurrentIndex(0)
        self.barra.setHidden(True)

    def menu(self):
        self.capa.setCurrentIndex(1)

    def eleccion(self):
        self.capa.setCurrentIndex(2)
    
    def reservas(self):
        self.capa.setCurrentIndex(3)
        self.usuario_etiqueta2.setText(self.dialogo_inicio.usuario_edit.text())

    

    def h_fourseasons_web(self):
        self.capa.setCurrentIndex(4)
        
    def h_rits_web(self):
        self.capa.setCurrentIndex(5)

    def h_villamagna_web(self):
        self.capa.setCurrentIndex(6)

    def r_botin_web(self):
        self.capa.setCurrentIndex(7)

    def r_streetxo_web(self):
        self.capa.setCurrentIndex(8)

    def r_casamono_web(self):
        self.capa.setCurrentIndex(9)
    
    def r_vacahuerta_web(self):
        self.capa.setCurrentIndex(10)

    def m_prado_web(self):
        self.capa.setCurrentIndex(11)

    def m_thyssen_web(self):
        self.capa.setCurrentIndex(12)

    def m_nacionalsofia_web(self):
        self.capa.setCurrentIndex(13)

    def a_warner_Web(self):
        self.capa.setCurrentIndex(14)

    def a_parqueatracciones_web(self):
        self.capa.setCurrentIndex(15)

    

    def reservar(self):
        hotel = 0
        restaurante = 0
        museo = 0
        atraccion = 0

        if self.hotel_box.currentText() == "Hotel Four Seasons: 500€":
            self.hotel_etiqueta2.setText("Four Seasons")
            hotel = 500

        elif self.hotel_box.currentText() == "Hotel Ritz: 400€":
            self.hotel_etiqueta2.setText("Ritz")
            hotel = 400
        elif self.hotel_box.currentText() == "Hotel Villa Magna: 300€":
            self.hotel_etiqueta2.setText("Villa Magna")
            hotel = 300

        if self.restaurante_box.currentText() == "Restaurante Botín: 60€":
            self.restaurante_etiqueta2.setText("Botín")
            restaurante = 60

        elif self.restaurante_box.currentText() == "Restaurante StreetXO: 50€":
            self.restaurante_etiqueta2.setText("StreetXO")
            restaurante = 50

        elif self.restaurante_box.currentText() == "Restaurante Casa Mono: 40€":
            self.restaurante_etiqueta2.setText("Casa Mono")
            restaurante = 40

        elif self.restaurante_box.currentText() == "Restaurante La Vaca y La Huerta: 35€":
            self.restaurante_etiqueta2.setText("La Vaca y La Huerta")
            restaurante = 35

        if self.museo_box.currentText() == "Museo del Prado: 15€":
            self.museo_etiqueta2.setText("Del Prado")
            museo = 15

        elif self.museo_box.currentText() == "Museo Thyssen-Bornemisza: 13€":
            self.museo_etiqueta2.setText("Thyssen-Bornemisza")
            museo = 13

        elif self.museo_box.currentText() == "Museo Nacional Centro de Arte Reina Sofia: 10€":
            self.museo_etiqueta2.setText("Nacional Centro de Arte Reina Sofia")
            museo = 10

        if self.atracciones_box.currentText() == "Parque Warner: 50€":
            self.atraccion_etiqueta2.setText("Parque Warner")
            atraccion = 50
    
        elif self.atracciones_box.currentText() == "Parque de Atracciones: 30€":
            self.atraccion_etiqueta2.setText("Parque de Atracciones")
            atraccion = 30

        total = hotel + restaurante + museo + atraccion
        self.total_etiqueta2.setText(str(total))
        self.usuario_etiqueta2.setText(self.dialogo_inicio.usuario_edit.text())
        self.capa.setCurrentIndex(3)

    
    


if __name__ == "__main__":
    app = QApplication([])
    ventana_principal = MainWindow()
    ventana_principal.show()
    sys.exit(app.exec())

