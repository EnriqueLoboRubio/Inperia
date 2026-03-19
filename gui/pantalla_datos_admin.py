from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QLabel,
    QPushButton,
    QFrame,
    QTextEdit,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
)

from gui.estilos import ESTILO_SCROLL


class PantallaDatosAdmin(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._iniciar_ui()

    def _iniciar_ui(self):
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(40, 24, 60, 20)
        layout_principal.setSpacing(18)

        tarjeta = QFrame()
        tarjeta.setStyleSheet(
            """
            QFrame {
                background-color: #F7F7F7;
                border: 1px solid #D7D7D7;
                border-radius: 20px;
            }
            QLabel {
                background: transparent;
                border: none;
                color: #1F1F1F;
            }
            """
        )

        layout_tarjeta = QVBoxLayout(tarjeta)
        layout_tarjeta.setContentsMargins(26, 24, 26, 24)
        layout_tarjeta.setSpacing(16)

        lbl_titulo = QLabel("Importación y exportación de base de datos")
        lbl_titulo.setFont(QFont("Arial", 16, QFont.Bold))
        layout_tarjeta.addWidget(lbl_titulo)

        lbl_desc = QLabel(
            "Exporta la base de datos actual a una carpeta CSV o importa una copia previa. "
            "La importación reemplaza los datos actuales de las tablas incluidas."
        )
        lbl_desc.setWordWrap(True)
        lbl_desc.setStyleSheet("font-size: 11pt; color: #4A4A4A;")
        layout_tarjeta.addWidget(lbl_desc)

        fila_botones = QHBoxLayout()
        fila_botones.setSpacing(12)

        self.boton_exportar = QPushButton("Exportar CSV")
        self.boton_exportar.setCursor(Qt.PointingHandCursor)
        self.boton_exportar.setFixedHeight(42)
        self.boton_exportar.setStyleSheet(self._estilo_boton("#1F6F5F", "#2C8E79"))
        fila_botones.addWidget(self.boton_exportar)

        self.boton_importar = QPushButton("Importar CSV")
        self.boton_importar.setCursor(Qt.PointingHandCursor)
        self.boton_importar.setFixedHeight(42)
        self.boton_importar.setStyleSheet(self._estilo_boton("#7A4B18", "#9A6223"))
        fila_botones.addWidget(self.boton_importar)

        fila_botones.addStretch()
        layout_tarjeta.addLayout(fila_botones)

        self.lbl_estado = QLabel("Selecciona una acción para comenzar.")
        self.lbl_estado.setWordWrap(True)
        self.lbl_estado.setStyleSheet("font-size: 10.5pt; color: #5B5B5B;")
        layout_tarjeta.addWidget(self.lbl_estado)

        self.txt_registro = QTextEdit()
        self.txt_registro.setReadOnly(True)
        self.txt_registro.setMinimumHeight(260)
        self.txt_registro.setStyleSheet(
            ESTILO_SCROLL
            + """
            QTextEdit {
                background-color: #FFFFFF;
                border: 1px solid #D1D1D1;
                border-radius: 16px;
                padding: 14px;
                font-size: 10.5pt;
                color: #232323;
            }
            """
        )
        layout_tarjeta.addWidget(self.txt_registro, 1)

        layout_principal.addWidget(tarjeta, 1)

    @staticmethod
    def _estilo_boton(color_base, color_hover):
        return f"""
            QPushButton {{
                background-color: {color_base};
                color: white;
                border: none;
                border-radius: 14px;
                padding: 0 18px;
                font-size: 10.5pt;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {color_hover};
            }}
        """

    def establecer_estado(self, texto):
        self.lbl_estado.setText(str(texto or ""))

    def establecer_registro(self, lineas):
        if isinstance(lineas, str):
            texto = lineas
        else:
            texto = "\n".join(str(linea) for linea in (lineas or []))
        self.txt_registro.setPlainText(texto)
