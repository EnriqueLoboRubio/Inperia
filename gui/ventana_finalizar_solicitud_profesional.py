from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QComboBox,
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
)

from gui.estilos import ESTILO_BOTON_SIG_ATR, ESTILO_COMBOBOX, ESTILO_INPUT, ESTILO_VENTANA_DETALLE
from gui.mensajes import Mensajes
from utils.enums import Tipo_estado_solicitud


class VentanaFinalizarSolicitudProfesional(QDialog):
    ESTADOS_DISPONIBLES = [
        (Tipo_estado_solicitud.ACEPTADA.value, "Aceptada"),
        (Tipo_estado_solicitud.RECHAZADA.value, "Rechazada"),
        (Tipo_estado_solicitud.CANCELADA.value, "Cancelada"),
    ]

    def __init__(self, solicitud=None, parent=None):
        super().__init__(parent)
        self._solicitud = solicitud
        self._datos = None
        self._msg = Mensajes(self)
        self._build_ui()
        self._cargar_datos_iniciales()

    def _build_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setModal(True)
        self.setFixedSize(760, 520)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        self.frame_fondo = QFrame()
        self.frame_fondo.setObjectName("FondoDetalle")
        self.frame_fondo.setStyleSheet(ESTILO_VENTANA_DETALLE)
        root.addWidget(self.frame_fondo)

        layout = QVBoxLayout(self.frame_fondo)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)

        layout.addLayout(self._build_header())
        layout.addLayout(self._build_form())
        layout.addStretch()
        layout.addLayout(self._build_actions())

    def _build_header(self):
        l = QHBoxLayout()
        lbl = QLabel("Finalizar solicitud")
        lbl.setFont(QFont("Arial", 16, QFont.Bold))
        lbl.setStyleSheet("border: none; color: black;")
        l.addWidget(lbl)
        l.addStretch()
        return l

    def _build_form(self):
        l = QVBoxLayout()
        l.setSpacing(10)

        lbl_estado = QLabel("Estado final *")
        lbl_estado.setFont(QFont("Arial", 11))

        self.combo_estado = QComboBox()
        self.combo_estado.setStyleSheet(ESTILO_COMBOBOX)
        self.combo_estado.setCursor(Qt.PointingHandCursor)
        self.combo_estado.setFixedHeight(36)
        for estado_valor, estado_texto in self.ESTADOS_DISPONIBLES:
            self.combo_estado.addItem(estado_texto, estado_valor)

        lbl_conclusiones = QLabel("Conclusiones del profesional *")
        lbl_conclusiones.setFont(QFont("Arial", 11))

        self.txt_conclusiones = QTextEdit()
        self.txt_conclusiones.setStyleSheet(ESTILO_INPUT)
        self.txt_conclusiones.setPlaceholderText("Escribe aquí las conclusiones finales...")
        self.txt_conclusiones.setFixedHeight(250)

        l.addWidget(lbl_estado)
        l.addWidget(self.combo_estado)
        l.addWidget(lbl_conclusiones)
        l.addWidget(self.txt_conclusiones)
        return l

    def _build_actions(self):
        l = QHBoxLayout()
        l.setContentsMargins(0, 0, 0, 0)

        boton_cancelar = QPushButton("Cancelar")
        boton_cancelar.setFont(QFont("Arial", 11))
        boton_cancelar.setFixedSize(120, 40)
        boton_cancelar.setCursor(Qt.PointingHandCursor)
        boton_cancelar.setStyleSheet(ESTILO_BOTON_SIG_ATR)
        boton_cancelar.clicked.connect(self.reject)

        estilo_guardar = ESTILO_BOTON_SIG_ATR.replace("black", "#792A24").replace(
            "rgba(71, 70, 70, 0.7)", "#C03930"
        )
        boton_guardar = QPushButton("Guardar")
        boton_guardar.setFont(QFont("Arial", 11))
        boton_guardar.setFixedSize(120, 40)
        boton_guardar.setCursor(Qt.PointingHandCursor)
        boton_guardar.setStyleSheet(estilo_guardar)
        boton_guardar.clicked.connect(self._guardar)

        l.addWidget(boton_cancelar)
        l.addStretch()
        l.addWidget(boton_guardar)
        return l

    def _cargar_datos_iniciales(self):
        estado_actual = str(getattr(self._solicitud, "estado", "") or "").lower()
        idx = 0
        for i in range(self.combo_estado.count()):
            if self.combo_estado.itemData(i) == estado_actual:
                idx = i
                break
        self.combo_estado.setCurrentIndex(idx)
        self.txt_conclusiones.setPlainText(str(getattr(self._solicitud, "conclusiones_profesional", "") or "").strip())

    def _guardar(self):
        conclusiones = self.txt_conclusiones.toPlainText().strip()
        if not conclusiones:
            self._msg.mostrar_advertencia(
                "Atención",
                "Debe escribir una conclusión para finalizar la solicitud.",
            )
            return

        self._datos = {
            "estado": self.combo_estado.currentData(),
            "conclusiones_profesional": conclusiones,
        }
        self.accept()

    def get_datos(self):
        return self._datos
