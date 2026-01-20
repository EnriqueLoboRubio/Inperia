from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QScrollArea
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QSize, pyqtSignal

# --- Widget individual para cada tarjeta de pregunta ---
# Esto representa una de las tarjetas blancas de tu imagen
class PantallaResumen(QWidget):
    # Señal que se emite cuando se pulsa el botón de editar
    editar_pregunta = pyqtSignal()

    def __init__(self, numero, titulo, respuesta, parent=None):
        super().__init__(parent)
        self.numero = numero
        self.init_ui(numero, titulo, respuesta)

    def init_ui(self, numero, titulo, respuesta):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # --- Fila superior: Título y Botón de Editar ---
        top_layout = QHBoxLayout()
        
        self.titulo_label = QLabel(f"Pregunta {numero}: {titulo}")
        self.titulo_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.titulo_label.setStyleSheet("color: #333;")

        self.edit_button = QPushButton("✎") # Icono de lápiz
        self.edit_button.setFixedSize(30, 30)
        self.edit_button.setToolTip("Editar esta respuesta")
        self.edit_button.setStyleSheet("""
            QPushButton {
                font-size: 18px;
                color: #555;
                background-color: #eee;
                border: 1px solid #ccc;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #ddd;
            }
        """)
        
        top_layout.addWidget(self.titulo_label)
        top_layout.addStretch()
        top_layout.addWidget(self.edit_button)

        # --- Fila inferior: La Respuesta ---
        # Si la respuesta está vacía, mostramos un texto alternativo
        if not respuesta:
            respuesta = "No se ha introducido respuesta."
            
        self.respuesta_label = QLabel(respuesta)
        self.respuesta_label.setFont(QFont("Arial", 11))
        self.respuesta_label.setStyleSheet("color: #444; padding-top: 5px;")
        self.respuesta_label.setWordWrap(True) # Para que el texto se ajuste

        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.respuesta_label)

        # --- Estilo de la tarjeta ---
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
            }
        """)

        # --- Conexión ---
        self.edit_button.clicked.connect(self.editar_pregunta.emit)


# --- Pantalla principal de Resumen ---
class PantallaResumen(QWidget):
    # Señal que emite el NÚMERO de la pregunta a editar
    editar_pregunta_signal = pyqtSignal(int) 
    # Señal para el botón "Atrás"
    atras_signal = pyqtSignal()
    # Señal para el botón "Enviar"
    enviar_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Almacenará los widgets de las tarjetas (por número) para actualizarlos
        self.preguntas_widgets = {} 
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # --- Título ---
        titulo_resumen = QLabel("Resumen de la Entrevista")
        titulo_resumen.setFont(QFont("Arial", 20, QFont.Bold))
        titulo_resumen.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(titulo_resumen)
        main_layout.addSpacing(20)

        # --- Área de Scroll para las preguntas ---
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; }") # Quitar borde

        scroll_widget = QWidget()
        scroll_widget.setStyleSheet("QWidget { background-color: transparent; }")
        
        # Este layout contendrá las tarjetas
        self.scroll_layout = QVBoxLayout(scroll_widget)
        self.scroll_layout.setContentsMargins(10, 10, 10, 10)
        self.scroll_layout.setSpacing(15)

        scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(scroll_area) # Añade el área de scroll al layout principal

        # --- Botones inferiores: Atrás y Enviar ---
        botones_layout = QHBoxLayout()
        botones_layout.setContentsMargins(10, 20, 10, 0)
        
        estilo_boton_negro = """
            QPushButton { 
                color: white; background-color: black; border: none;
                padding: 10px 15px; border-radius: 15px; font-size: 14px;
            }
            QPushButton:hover { background-color: #333; }
        """
        
        estilo_boton_rojo = estilo_boton_negro.replace("black", "#AC1F20").replace("#333", "#F3292B")

        self.boton_atras = QPushButton("Atrás")
        self.boton_atras.setStyleSheet(estilo_boton_negro)
        self.boton_atras.setFixedSize(150, 50)
        
        self.boton_enviar = QPushButton("Enviar")
        self.boton_enviar.setStyleSheet(estilo_boton_rojo)
        self.boton_enviar.setFixedSize(150, 50)

        botones_layout.addWidget(self.boton_atras)
        botones_layout.addStretch()
        botones_layout.addWidget(self.boton_enviar)
        
        main_layout.addLayout(botones_layout)

        # --- Conexiones de señales ---
        self.boton_atras.clicked.connect(self.atras_signal.emit)
        self.boton_enviar.clicked.connect(self.enviar_signal.emit)

    def cargar_resumen(self, datos_preguntas, respuestas):
        """Limpia y vuelve a cargar todas las tarjetas de respuesta."""
        
        # Limpiar widgets antiguos
        while self.scroll_layout.count():
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        self.preguntas_widgets = {}

        # Crear y añadir nuevas tarjetas
        for i in range(len(respuestas)):
            numero = i + 1
            respuesta = respuestas[i]
            
            # Obtener título del JSON (clave es string)
            datos = datos_preguntas.get(str(numero), {"titulo": "Desconocido"})
            
            card = PantallaResumen(numero, datos['titulo'], respuesta)
            
            # Conectar la señal de la tarjeta a la señal principal (pasando el número)
            card.editar_pregunta.connect(
                lambda n=numero: self.editar_pregunta_signal.emit(n)
            )
            
            self.scroll_layout.addWidget(card)
            self.preguntas_widgets[numero] = card # Guardar referencia
        
        self.scroll_layout.addStretch() # Empuja todo hacia arriba