from datetime import datetime

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import (
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from gui.estilos import (
    COLOR_IA_MORADO,
    COLOR_IA_MORADO_SUAVE,
    ESTILO_BOTON_SIG_ATR,
    ESTILO_INPUT,
    ESTILO_SCROLL,
    ESTILO_VENTANA_DETALLE,
)
from gui.mensajes import Mensajes


class BurbujaComentario(QFrame):
    def __init__(self, mostrar_boton_borrar, parent=None):
        super().__init__(parent)
        self._mostrar_boton_borrar = mostrar_boton_borrar
        self.boton_borrar = None
        self.setMouseTracking(True)

    def set_boton_borrar(self, boton):
        self.boton_borrar = boton
        self._actualizar_visibilidad_boton(False)

    def enterEvent(self, event):
        self._actualizar_visibilidad_boton(True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._actualizar_visibilidad_boton(False)
        super().leaveEvent(event)

    def _actualizar_visibilidad_boton(self, visible):
        if self.boton_borrar is None or not self._mostrar_boton_borrar:
            return
        self.boton_borrar.setVisible(visible)


class VentanaComentariosEntrevistaProfesional(QDialog):
    def __init__(self, entrevista, id_profesional, solo_lectura=False, parent=None):
        super().__init__(parent)
        self.entrevista = entrevista
        self.id_entrevista = getattr(entrevista, "id_entrevista", None)
        self.id_profesional = id_profesional
        self.solo_lectura = solo_lectura
        if getattr(self.entrevista, "comentarios", None) is None:
            self.entrevista.comentarios = []
        self._msg = Mensajes(self)
        self._construir_ui()
        self._recargar_comentarios()

    def _construir_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setModal(True)
        self.setFixedSize(760, 620)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        fondo = QFrame()
        fondo.setObjectName("FondoDetalle")
        fondo.setStyleSheet(ESTILO_VENTANA_DETALLE)
        root.addWidget(fondo)

        layout = QVBoxLayout(fondo)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)

        cabecera = QHBoxLayout()
        titulo = QLabel("Comentarios de entrevista")
        titulo.setFont(QFont("Arial", 14, QFont.Bold))
        titulo.setStyleSheet("border: none; color: #222222;")
        cabecera.addWidget(titulo)
        cabecera.addStretch()

        boton_cerrar = QPushButton("✕")
        boton_cerrar.setCursor(Qt.PointingHandCursor)
        boton_cerrar.setFixedSize(24, 24)
        boton_cerrar.setStyleSheet(
            """
            QPushButton {
                background: transparent;
                border: none;
                color: #666666;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #F1F1F1;
                border: 1px solid #E0E0E0;
                border-radius: 12px;
                color: #111111;
            }
            """
        )
        boton_cerrar.clicked.connect(self.accept)
        cabecera.addWidget(boton_cerrar)
        layout.addLayout(cabecera)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setStyleSheet(
            ESTILO_SCROLL
            + """
            QScrollArea {
                background-color: #F8F8F8;
                border: 1px solid #D8D8D8;
                border-radius: 14px;
            }
            QWidget {
                background: transparent;
            }
            """
        )

        self.contenido = QWidget()
        self.layout_comentarios = QVBoxLayout(self.contenido)
        self.layout_comentarios.setContentsMargins(8, 8, 8, 8)
        self.layout_comentarios.setSpacing(10)
        self.layout_comentarios.setAlignment(Qt.AlignTop)

        self.scroll.setWidget(self.contenido)
        layout.addWidget(self.scroll, 1)

        if not self.solo_lectura:
            fila_envio = QHBoxLayout()
            fila_envio.setSpacing(8)
            self.txt_nuevo = QTextEdit()
            self.txt_nuevo.setPlaceholderText("Escribe un comentario...")
            self.txt_nuevo.setStyleSheet(
                ESTILO_INPUT
                + """
                QTextEdit { border-radius: 14px; }
                """
            )
            self.txt_nuevo.setFixedHeight(78)
            fila_envio.addWidget(self.txt_nuevo, 1)

            self.boton_enviar = QPushButton("")
            self.boton_enviar.setCursor(Qt.PointingHandCursor)
            self.boton_enviar.setStyleSheet(ESTILO_BOTON_SIG_ATR)
            self.boton_enviar.setIcon(QIcon("assets/enviar.svg"))
            self.boton_enviar.setIconSize(QSize(18, 18))
            self.boton_enviar.setFixedSize(42, 42)
            self.boton_enviar.clicked.connect(self._enviar_comentario)
            fila_envio.addWidget(self.boton_enviar, alignment=Qt.AlignBottom)

            layout.addLayout(fila_envio)

    def _limpiar_layout_comentarios(self):
        while self.layout_comentarios.count():
            item = self.layout_comentarios.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def _comentarios_visibles(self):
        filas = []
        comentario_ia = getattr(self.entrevista, "comentario_ia_general", None)
        if comentario_ia:
            filas.append(comentario_ia)
        filas.extend(list(getattr(self.entrevista, "comentarios", []) or []))
        return filas

    def _recargar_comentarios(self):
        self._limpiar_layout_comentarios()
        filas = self._comentarios_visibles()
        if not filas:
            lbl = QLabel("Todavia no hay comentarios.")
            lbl.setStyleSheet("color: #666666; font-size: 10pt; border: none;")
            lbl.setAlignment(Qt.AlignCenter)
            self.layout_comentarios.addWidget(lbl)
            return

        for fila in filas:
            widget = self._crear_burbuja_comentario(fila)
            self.layout_comentarios.addWidget(widget)

        self.layout_comentarios.addStretch()
        self.scroll.verticalScrollBar().setValue(self.scroll.verticalScrollBar().maximum())

    def _crear_burbuja_comentario(self, fila):
        id_comentario = fila.get("id")
        id_profesional = fila.get("id_profesional")
        comentario = fila.get("comentario")
        fecha = fila.get("fecha")
        es_ia = bool(fila.get("es_ia"))

        contenedor = QWidget()
        layout = QHBoxLayout(contenedor)
        layout.setContentsMargins(0, 0, 0, 0)

        es_mio = (
            (not self.solo_lectura)
            and not es_ia
            and id_profesional is not None
            and int(id_profesional) == int(self.id_profesional)
        )
        if es_mio:
            layout.addStretch()

        bubble = BurbujaComentario(mostrar_boton_borrar=es_mio)
        bubble.setStyleSheet(
            f"""
            QFrame {{
                background-color: {COLOR_IA_MORADO_SUAVE if es_ia else ("#DFF3C8" if es_mio else "#ECECEC")};
                border: 1px solid {COLOR_IA_MORADO if es_ia else "#D8D8D8"};
                border-radius: 12px;
            }}
            """
        )
        lay_bubble = QVBoxLayout(bubble)
        lay_bubble.setContentsMargins(10, 8, 10, 8)
        lay_bubble.setSpacing(6)

        if es_ia:
            lbl_origen = QLabel("IA")
            lbl_origen.setStyleSheet(
                f"border: none; color: {COLOR_IA_MORADO}; font-size: 8.5pt; font-weight: 700;"
            )
            lay_bubble.addWidget(lbl_origen)

        lbl_texto = QLabel(str(comentario or "").strip())
        lbl_texto.setWordWrap(True)
        lbl_texto.setStyleSheet("border: none; color: #1A1A1A; font-size: 10.5pt;")
        lay_bubble.addWidget(lbl_texto)

        fila_meta = QHBoxLayout()
        lbl_fecha = QLabel(str(fecha or ""))
        lbl_fecha.setStyleSheet("border: none; color: #666666; font-size: 8.5pt;")
        fila_meta.addWidget(lbl_fecha)
        fila_meta.addStretch()

        boton_borrar = QPushButton("Borrar")
        boton_borrar.setCursor(Qt.PointingHandCursor)
        boton_borrar.setIcon(QIcon("assets/borrar.svg"))
        boton_borrar.setIconSize(QSize(14, 14))
        boton_borrar.setFixedHeight(26)
        boton_borrar.setStyleSheet(
            """
            QPushButton {
                background-color: #C03930;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 3px 10px;
                font-size: 8.5pt;
            }
            QPushButton:hover { background-color: #A93226; }
            """
        )
        boton_borrar.clicked.connect(lambda: self._borrar_comentario(id_comentario))
        boton_borrar.setEnabled(es_mio)
        boton_borrar.setVisible(False)
        bubble.set_boton_borrar(boton_borrar)
        fila_meta.addWidget(boton_borrar)

        lay_bubble.addLayout(fila_meta)
        bubble.setMaximumWidth(500)
        layout.addWidget(bubble)

        if not es_mio:
            layout.addStretch()

        return contenedor

    def _enviar_comentario(self):
        texto = self.txt_nuevo.toPlainText().strip()
        if not texto:
            self._msg.mostrar_advertencia("Atencion", "Debe escribir un comentario.")
            return
        ids_existentes = [
            int(c.get("id"))
            for c in getattr(self.entrevista, "comentarios", [])
            if str(c.get("id", "")).lstrip("-").isdigit()
        ]
        siguiente_id_temporal = (min(ids_existentes) - 1) if ids_existentes else -1
        self.entrevista.comentarios.append(
            {
                "id": siguiente_id_temporal,
                "id_entrevista": self.id_entrevista,
                "id_profesional": self.id_profesional,
                "comentario": texto,
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        )
        self.txt_nuevo.clear()
        self._recargar_comentarios()

    def _borrar_comentario(self, id_comentario):
        comentarios = list(getattr(self.entrevista, "comentarios", []) or [])
        nuevos = [c for c in comentarios if str(c.get("id")) != str(id_comentario)]
        if len(nuevos) == len(comentarios):
            self._msg.mostrar_advertencia("Error", "No se pudo borrar el comentario.")
            return
        self.entrevista.comentarios = nuevos
        self._recargar_comentarios()
