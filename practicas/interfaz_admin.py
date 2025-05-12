import sys
import numpy as np
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QLineEdit, QComboBox, QSlider, QSpinBox, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import ctypes

# Clase para el lienzo gráfico donde se dibujará la señal
class LienzoGrafico(FigureCanvas):
    def __init__(self, padre=None):
        self.fig, self.ax = plt.subplots()
        super().__init__(self.fig)
        self.graficar(8000, 'cuadrada')  # Valor inicial de frecuencia y tipo de señal

    def graficar(self, frecuencia, tipo_de_senal):
        self.ax.clear()
        t = np.linspace(0, 2, 500)

        if tipo_de_senal == 'Cuadrada':
            senal = np.sign(np.sin(2 * np.pi * frecuencia * t))
        elif tipo_de_senal == 'Triangular':
            senal = 2 * np.abs(2 * (t * frecuencia - np.floor(t * frecuencia + 0.5))) - 1
        else:  # Señal sinusoidal
            senal = np.sin(2 * np.pi * frecuencia * t)

        self.ax.plot(t, senal, color='#ee4f70')
        self.ax.set_title("Estimulación Magnética Transcraneal")
        self.ax.set_xlabel("Tiempo (s)")
        self.ax.set_ylabel("Amplitud")
        self.draw()

# Clase principal que contiene la interfaz de la aplicación
class AplicacionEstimulador(QWidget):
    def __init__(self):
        super().__init__()
        self.iniciarUI()
        self.showMaximized()

    def iniciarUI(self):
        self.setWindowIcon(QIcon("icono.png"))
        self.setWindowTitle("Estimulación Magnética Transcraneal")

        self.lienzo_grafico = LienzoGrafico(self)

        self.etiqueta_senal = QLabel("Tipo de Señal:")
        self.selector_senal = QComboBox()
        self.selector_senal.addItems(["Cuadrada", "Triangular", "Sinusoidal"])

        self.etiqueta_offset = QLabel("Offset:")
        self.selector_offset = QComboBox()
        self.selector_offset.addItems(["Centrada", "Positiva", "Negativa"])

        self.slider_amplitud = self.crear_slider()
        self.slider_offset = self.crear_slider()
        self.slider_duty = self.crear_slider()

        self.caja_parametros = self.crear_caja_parametros()
        self.caja_valores = self.crear_caja_valores()

        self.etiqueta_numero_serie = QLabel("Número de Serie:")
        self.entrada_numero_serie = QLineEdit()
        self.entrada_numero_serie.setFixedWidth(150)

        self.etiqueta_sesiones_restantes = QLabel("Sesiones Restantes:")
        self.entrada_sesiones_restantes = QLineEdit()
        self.entrada_sesiones_restantes.setFixedWidth(150)

        self.boton_cargar_sesiones = QPushButton("Cargar Sesiones")
        self.boton_cargar_sesiones.setFixedWidth(155)

        layout_principal = QVBoxLayout()

        fila_1_layout = QHBoxLayout()
        fila_1_layout.addWidget(self.lienzo_grafico, 7)

        widget_controles = QWidget()
        layout_controles = self.crear_controles()
        widget_controles.setLayout(layout_controles)
        fila_1_layout.addWidget(widget_controles, 3)

        layout_principal.addLayout(fila_1_layout)

        fila_2_layout = QHBoxLayout()
        fila_2_layout.addWidget(self.caja_parametros, 1)
        fila_2_layout.addWidget(self.caja_valores, 1)
        layout_principal.addLayout(fila_2_layout)

        fila_3_layout = QVBoxLayout()
        fila_3_layout.addWidget(self.etiqueta_numero_serie)
        fila_3_layout.addWidget(self.entrada_numero_serie)
        fila_3_layout.addWidget(self.etiqueta_sesiones_restantes)
        fila_3_layout.addWidget(self.entrada_sesiones_restantes)
        fila_3_layout.setAlignment(Qt.AlignCenter)
        layout_principal.addLayout(fila_3_layout)

        fila_4_layout = QHBoxLayout()
        fila_4_layout.addWidget(self.boton_cargar_sesiones, 1)
        fila_4_layout.setAlignment(Qt.AlignCenter)
        layout_principal.addLayout(fila_4_layout)

        self.setLayout(layout_principal)

    def crear_slider(self):
        slider = QSlider(Qt.Vertical)
        slider.setRange(0, 100)
        slider.setValue(50)
        slider.setTickInterval(10)
        slider.setTickPosition(QSlider.TicksBelow)

        slider.setStyleSheet("""
            QSlider::handle:vertical {
                background: #ee4f70;
                width: 20px;
                height: 20px;
                border-radius: 10px;
            }
            QSlider::groove:vertical {
                background: #D3D3D3;
                width: 20px;
                border-radius: 10px;
            }
        """)

        return slider

    def crear_caja_parametros(self):
        layout_parametros = QVBoxLayout()

        self.etiqueta_frecuencia = QLabel("Frecuencia (Hz):")
        self.entrada_frecuencia = QSpinBox()
        self.entrada_frecuencia.setRange(1, 10000)
        self.entrada_frecuencia.setValue(8000)

        self.etiqueta_minutos = QLabel("Minutos:")
        self.entrada_minutos = QSpinBox()
        self.entrada_minutos.setRange(1, 60)
        self.entrada_minutos.setValue(30)

        self.etiqueta_muestras = QLabel("Muestras:")
        self.entrada_muestras = QSpinBox()
        self.entrada_muestras.setRange(1, 100)
        self.entrada_muestras.setValue(50)

        self.boton_aplicar = QPushButton("Aplicar")
        self.boton_aplicar.clicked.connect(self.aplicar_configuraciones)

        layout_parametros.addWidget(self.etiqueta_frecuencia)
        layout_parametros.addWidget(self.entrada_frecuencia)
        layout_parametros.addWidget(self.etiqueta_minutos)
        layout_parametros.addWidget(self.entrada_minutos)
        layout_parametros.addWidget(self.etiqueta_muestras)
        layout_parametros.addWidget(self.entrada_muestras)
        layout_parametros.addWidget(self.boton_aplicar)

        caja_parametros = QGroupBox("Parámetros")
        caja_parametros.setLayout(layout_parametros)
        caja_parametros.setStyleSheet("QGroupBox { border: 1px solid black; padding: 10px; margin-top: 15px; margin-bottom: 15px; }")
        return caja_parametros

    def crear_caja_valores(self):
        layout_valores = QGridLayout()

        etiquetas = ["1 pp", "1 max", "1 min", "Duty", "1 rms", "1 med"]
        unidades = ["uA", "uA", "uA", "%", "uA", "uA"]

        for i in range(6):
            etiqueta_valor = QLabel(f"{etiquetas[i]}:")
            entrada_valor = QLineEdit()
            etiqueta_unidad = QLabel(f"({unidades[i]})")
            entrada_valor.setReadOnly(False)  # Editable ahora

            row = i // 2
            if i % 2 == 0:  # Primera columna (izquierda)
                col = 0
            else:  # Segunda columna (derecha), saltando columna 1 para separación
                col = 3

            layout_valores.addWidget(etiqueta_valor, row, col)
            layout_valores.addWidget(entrada_valor, row, col + 1)
            layout_valores.addWidget(etiqueta_unidad, row, col + 2)

        caja_valores = QGroupBox("Valores")
        caja_valores.setLayout(layout_valores)
        caja_valores.setStyleSheet("QGroupBox { border: 1px solid black; padding: 10px; margin-top: 15px; margin-bottom: 15px; }")
        return caja_valores


    def crear_controles(self):
        layout_controles = QVBoxLayout()

        # Agregar los widgets de la señal y el offset
        layout_controles.addWidget(self.etiqueta_senal)
        layout_controles.addWidget(self.selector_senal)
        layout_controles.addWidget(self.etiqueta_offset)
        layout_controles.addWidget(self.selector_offset)

        # Crear un layout horizontal para los sliders
        slider_layout = QHBoxLayout()

        # Agregar los sliders con sus etiquetas encima
        slider_layout.addLayout(self.crear_slider_con_etiqueta("Amplitud", self.slider_amplitud))
        slider_layout.addLayout(self.crear_slider_con_etiqueta("Offset", self.slider_offset))
        slider_layout.addLayout(self.crear_slider_con_etiqueta("Duty", self.slider_duty))

        layout_controles.addLayout(slider_layout)

        return layout_controles

    def crear_slider_con_etiqueta(self, texto, slider):
        layout_slider = QVBoxLayout()
        etiqueta = QLabel(texto)
        layout_slider.addWidget(etiqueta)
        layout_slider.addWidget(slider)
        return layout_slider

    def aplicar_configuraciones(self):
        frecuencia = self.entrada_frecuencia.value()
        tipo_de_senal = self.selector_senal.currentText()
        self.lienzo_grafico.graficar(frecuencia, tipo_de_senal)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = AplicacionEstimulador()
    ventana.show()
    sys.exit(app.exec_())
