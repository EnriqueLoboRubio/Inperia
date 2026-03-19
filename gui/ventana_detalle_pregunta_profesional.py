import os
from datetime import datetime

from PyQt5.QtCore import QUrl, Qt, QSize, pyqtSignal
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import (
    QComboBox,
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSlider,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from db.pregunta_db import obtener_preguntas_como_diccionario
from gui.estilos import *
from gui.mensajes import Mensajes
from gui.spinner_carga import SpinnerCarga

ESTILO_ANALISIS_IA = f"""
QTextEdit {{
    background-color: {COLOR_IA_MORADO_SUAVE};
    border: 1px solid #DDCCF2;
    border-radius: 14px;
    color: #000000;
    padding: 10px;
    font-size: 20px;
    min-height: 30px;
    font-family: 'Arial';
    selection-background-color: #C9AFE9;
}}
QTextEdit:focus {{
    border: 1px solid {COLOR_AZUL_OSCURO};
}}
"""


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


def cargar_datos_preguntas():
    return obtener_preguntas_como_diccionario()


class VentanaDetallePreguntaProfesional(QDialog):
    nivel_profesional_actualizado = pyqtSignal(int, int)

    def __init__(
        self,
        pregunta,
        numero,
        id_entrevista,
        id_profesional,
        solo_lectura=False,
        analisis_bloqueado=False,
        parent=None,
    ):
        super().__init__(parent)
        self.pregunta = pregunta
        self.numero = int(numero)
        self.id_entrevista = id_entrevista
        self.id_profesional = id_profesional if id_profesional is not None else -1
        self.solo_lectura = solo_lectura
        self._analisis_bloqueado = bool(analisis_bloqueado)
        self.id_respuesta = getattr(pregunta, "id_respuesta", None)
        if getattr(self.pregunta, "comentarios", None) is None:
            self.pregunta.comentarios = []
        self._msg = Mensajes(self)
        self.PREGUNTAS_DATA = cargar_datos_preguntas()
        self.player = QMediaPlayer()
        self._spinner_host_ia = None

        self._construir_ui()
        self._cargar_comentarios()

    def _construir_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setModal(True)
        self.setFixedSize(1000, 950)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        fondo = QFrame()
        fondo.setObjectName("FondoDetalle")
        fondo.setStyleSheet(ESTILO_VENTANA_DETALLE)
        root.addWidget(fondo)

        principal_layout = QVBoxLayout(fondo)
        principal_layout.setSpacing(12)
        principal_layout.setContentsMargins(12, 12, 12, 12)

        principal_layout.addLayout(self._crear_cabecera())
        principal_layout.addWidget(self._crear_bloque_transcripcion())
        principal_layout.addWidget(self._crear_bloque_audio())
        principal_layout.addWidget(self._crear_bloque_analisis())
        principal_layout.addWidget(self._crear_bloque_comentarios(), 1)

    def _crear_cabecera(self):
        layout = QHBoxLayout()
        datos = self.PREGUNTAS_DATA.get(str(self.numero), {})
        titulo_json = datos.get("titulo", f"Pregunta {self.numero}")
        self.lbl_titulo = QLabel(f"Pregunta {self.numero}: {titulo_json}")
        self.lbl_titulo.setFont(QFont("Arial", 16, QFont.Bold))
        self.lbl_titulo.setStyleSheet("border: none; color: #1A1A1A;")
        layout.addWidget(self.lbl_titulo, 1)

        self.boton_analizar = QPushButton("Analizar pregunta")
        self.boton_analizar.setCursor(Qt.PointingHandCursor)
        self.boton_analizar.setStyleSheet(
            ESTILO_BOTON_IA
            + """
            QPushButton:disabled {
                background-color: #EAEAEA;
                color: #9A9A9A;
                border: none;
            }
            """
        )
        self.boton_analizar.setToolTip("Analizar esta pregunta con IA")
        altura_control = self.boton_analizar.sizeHint().height()
        if not self.solo_lectura:
            self._spinner_host_ia = QWidget(self)
            self._spinner_host_ia.setFixedSize(30, 30)
            self._spinner_host_ia.setStyleSheet("background: transparent; border: none;")
            layout.addWidget(self._spinner_host_ia, 0, Qt.AlignBottom)
            self.lbl_spinner_ia = None
            layout.addWidget(self.boton_analizar, 0, Qt.AlignBottom)
        else:
            self.lbl_spinner_ia = None
        self._aplicar_bloqueo_boton_analizar()

        niveles_layout = QHBoxLayout()
        niveles_layout.setSpacing(8)

        bloque_prof = QVBoxLayout()
        bloque_prof.setSpacing(4)
        lbl_titulo_prof = QLabel("Profesional")
        lbl_titulo_prof.setFont(QFont("Arial", 9, QFont.Bold))
        lbl_titulo_prof.setAlignment(Qt.AlignCenter)
        lbl_titulo_prof.setStyleSheet("border: none; color: #666666;")
        self.combo_nivel_prof = QComboBox()
        self.combo_nivel_prof.setStyleSheet(
            ESTILO_COMBOBOX
            + """
            QComboBox { border-radius: 10px; }
            QComboBox::drop-down { border-top-right-radius: 10px; border-bottom-right-radius: 10px; }
            """
        )
        self.combo_nivel_prof.setFixedHeight(altura_control)
        self.combo_nivel_prof.setMinimumWidth(120)
        self.combo_nivel_prof.addItem("Nivel: -", -1)
        cantidad_niveles = int(datos.get("cantidad_niveles", 0) or 0)
        for nivel in range(cantidad_niveles):
            self.combo_nivel_prof.addItem(f"Nivel: {nivel}", nivel)
        nivel_prof_actual = self._nivel_entero(getattr(self.pregunta, "nivel_profesional", None))
        index_prof = self.combo_nivel_prof.findData(nivel_prof_actual)
        self.combo_nivel_prof.setCurrentIndex(index_prof if index_prof >= 0 else 0)
        if self.solo_lectura:
            self.combo_nivel_prof.setEnabled(False)
            self.combo_nivel_prof.setToolTip("Solo lectura: no se puede modificar el nivel profesional.")
        else:
            self.combo_nivel_prof.currentIndexChanged.connect(self._guardar_nivel_profesional)
        bloque_prof.addWidget(lbl_titulo_prof)
        bloque_prof.addWidget(self.combo_nivel_prof)

        bloque_ia = QVBoxLayout()
        bloque_ia.setSpacing(4)
        lbl_titulo_ia = QLabel("IA")
        lbl_titulo_ia.setFont(QFont("Arial", 9, QFont.Bold))
        lbl_titulo_ia.setAlignment(Qt.AlignCenter)
        lbl_titulo_ia.setStyleSheet(f"border: none; color: {COLOR_IA_MORADO};")
        self.lbl_nivel_ia = QLabel(f"Nivel: {self._texto_nivel(getattr(self.pregunta, 'nivel_ia', None))}")
        self.lbl_nivel_ia.setFont(QFont("Arial", 11, QFont.Bold))
        self.lbl_nivel_ia.setAlignment(Qt.AlignCenter)
        self.lbl_nivel_ia.setStyleSheet(ESTILO_NIVEL_IA)
        self.lbl_nivel_ia.setFixedHeight(altura_control)
        bloque_ia.addWidget(lbl_titulo_ia)
        bloque_ia.addWidget(self.lbl_nivel_ia)

        niveles_layout.addLayout(bloque_prof)
        niveles_layout.addLayout(bloque_ia)
        layout.addLayout(niveles_layout)
        self.boton_cerrar = QPushButton("✕")
        self.boton_cerrar.setCursor(Qt.PointingHandCursor)
        self.boton_cerrar.setFixedSize(24, 24)
        self.boton_cerrar.setStyleSheet(
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
        self.boton_cerrar.clicked.connect(self.close)
        layout.addWidget(self.boton_cerrar, 0, Qt.AlignTop)
        return layout

    def _crear_bloque_transcripcion(self):
        frame = QFrame()
        frame.setStyleSheet("QFrame { background: transparent; border: none; }")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        lbl = QLabel("Transcripción")
        lbl.setFont(QFont("Arial", 11, QFont.Bold))
        lbl.setStyleSheet("border: none;")
        layout.addWidget(lbl)

        self.txt_respuesta = QTextEdit()
        self.txt_respuesta.setReadOnly(True)
        self.txt_respuesta.setStyleSheet(ESTILO_INPUT)
        self.txt_respuesta.setText(str(getattr(self.pregunta, "respuesta", "") or ""))
        self.txt_respuesta.setFixedHeight(120)
        layout.addWidget(self.txt_respuesta)
        return frame

    def _crear_bloque_audio(self):
        frame = QFrame()
        frame.setStyleSheet("QFrame { background: transparent; border: none; }")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        lbl = QLabel("Audio")
        lbl.setFont(QFont("Arial", 11, QFont.Bold))
        lbl.setStyleSheet("border: none;")
        layout.addWidget(lbl)

        controles = QHBoxLayout()
        controles.setAlignment(Qt.AlignCenter)
        self.boton_play = QPushButton()
        self.boton_play.setIcon(QIcon("assets/play.png"))
        self.boton_play.setIconSize(QSize(20, 20))
        self.boton_play.setFixedSize(50, 50)
        self.boton_play.setCursor(Qt.PointingHandCursor)
        self.boton_play.setStyleSheet(ESTILO_BOTON_PLAY)
        self.boton_play.clicked.connect(lambda: self.toggle_audio(getattr(self.pregunta, "archivo_audio", None)))
        controles.addWidget(self.boton_play)
        layout.addLayout(controles)

        self.slider_audio = QSlider(Qt.Horizontal)
        self.slider_audio.setRange(0, 0)
        self.slider_audio.setCursor(Qt.PointingHandCursor)
        self.slider_audio.setStyleSheet(ESTILO_SLIDER)
        layout.addWidget(self.slider_audio)

        self.lbl_estado_audio = QLabel("")
        self.lbl_estado_audio.setAlignment(Qt.AlignCenter)
        self.lbl_estado_audio.setStyleSheet("color: #6B7280; font-size: 12px; border: none;")

        tiempo_layout = QHBoxLayout()
        self.lbl_tiempo_actual = QLabel("00:00")
        self.lbl_tiempo_total = QLabel("00:00")
        for lbl_tiempo in (self.lbl_tiempo_actual, self.lbl_tiempo_total):
            lbl_tiempo.setStyleSheet("border: none; color: #374151;")

        tiempo_layout.addWidget(self.lbl_tiempo_actual)
        tiempo_layout.addStretch()
        tiempo_layout.addWidget(self.lbl_estado_audio)
        tiempo_layout.addStretch()
        tiempo_layout.addWidget(self.lbl_tiempo_total)
        layout.addLayout(tiempo_layout)

        self.player.positionChanged.connect(self.actualizar_posicion)
        self.player.durationChanged.connect(self.actualizar_duracion)
        self.player.stateChanged.connect(self.cambio_estado)
        self.slider_audio.sliderMoved.connect(self.player.setPosition)
        return frame

    def _crear_bloque_analisis(self):
        frame = QFrame()
        frame.setStyleSheet("QFrame { background: transparent; border: none; }")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        lbl = QLabel("Comentario IA")
        lbl.setFont(QFont("Arial", 11, QFont.Bold))
        lbl.setStyleSheet(f"border: none; color: {COLOR_IA_MORADO};")
        layout.addWidget(lbl)

        self.txt_analisis = QTextEdit()
        self.txt_analisis.setReadOnly(True)
        self.txt_analisis.setStyleSheet(ESTILO_ANALISIS_IA)
        analisis = str(getattr(self.pregunta, "valoracion_ia", "") or "").strip()
        self.txt_analisis.setText(analisis if analisis else "Sin comentario IA.")
        self.txt_analisis.setFixedHeight(110)
        layout.addWidget(self.txt_analisis)

        self.lbl_estado_ia = QLabel("Estado IA: Analizada" if analisis else "Estado IA: Sin analizar")
        self.lbl_estado_ia.setStyleSheet("border: none; color: #6B7280; font-size: 10pt;")
        layout.addWidget(self.lbl_estado_ia)
        return frame

    def _crear_bloque_comentarios(self):
        frame = QFrame()
        frame.setStyleSheet("QFrame { background: transparent; border: none; }")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        lbl = QLabel("Comentarios")
        lbl.setFont(QFont("Arial", 11, QFont.Bold))
        lbl.setStyleSheet("border: none;")
        layout.addWidget(lbl)

        self.scroll_comentarios = QScrollArea()
        self.scroll_comentarios.setWidgetResizable(True)
        self.scroll_comentarios.setFrameShape(QFrame.NoFrame)
        self.scroll_comentarios.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_comentarios.setStyleSheet(
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

        self.contenedor_comentarios = QWidget()
        self.layout_comentarios = QVBoxLayout(self.contenedor_comentarios)
        self.layout_comentarios.setContentsMargins(4, 4, 4, 4)
        self.layout_comentarios.setSpacing(8)
        self.layout_comentarios.setAlignment(Qt.AlignTop)
        self.scroll_comentarios.setWidget(self.contenedor_comentarios)
        layout.addWidget(self.scroll_comentarios, 1)

        if not self.solo_lectura:
            fila_envio = QHBoxLayout()
            self.txt_nuevo_comentario = QTextEdit()
            self.txt_nuevo_comentario.setStyleSheet(
                ESTILO_INPUT
                + """
                QTextEdit { border-radius: 14px; }
                """
            )
            self.txt_nuevo_comentario.setPlaceholderText("Escribe un comentario...")
            self.txt_nuevo_comentario.setFixedHeight(70)
            fila_envio.addWidget(self.txt_nuevo_comentario, 1)

            self.boton_enviar_comentario = QPushButton("Enviar")
            self.boton_enviar_comentario.setCursor(Qt.PointingHandCursor)
            self.boton_enviar_comentario.setStyleSheet(ESTILO_BOTON_SIG_ATR)
            self.boton_enviar_comentario.setIcon(QIcon("assets/enviar.svg"))
            self.boton_enviar_comentario.setIconSize(QSize(16, 16))
            self.boton_enviar_comentario.setFixedSize(124, 40)
            self.boton_enviar_comentario.clicked.connect(self._enviar_comentario)
            self.boton_enviar_comentario.setEnabled(self.id_profesional is not None and int(self.id_profesional) >= 0)
            if not self.boton_enviar_comentario.isEnabled():
                self.boton_enviar_comentario.setToolTip("Desactivado: profesional no identificado.")
            fila_envio.addWidget(self.boton_enviar_comentario, alignment=Qt.AlignBottom)
            layout.addLayout(fila_envio)
        return frame

    @staticmethod
    def _texto_nivel(valor):
        if valor is None:
            return "-"
        try:
            val = int(valor)
        except (TypeError, ValueError):
            return "-"
        return str(val) if val >= 0 else "-"

    @staticmethod
    def _nivel_entero(valor):
        try:
            nivel = int(valor)
        except (TypeError, ValueError):
            return -1
        return nivel if nivel >= 0 else -1

    def _guardar_nivel_profesional(self, *_args):
        if not self.id_entrevista:
            return
        nivel = self.combo_nivel_prof.currentData()
        if nivel is None:
            nivel = -1
        self.pregunta.nivel_profesional = nivel
        self.nivel_profesional_actualizado.emit(self.numero, int(nivel))

    def _limpiar_layout_comentarios(self):
        while self.layout_comentarios.count():
            item = self.layout_comentarios.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def _cargar_comentarios(self):
        self._limpiar_layout_comentarios()
        if not self.id_respuesta:
            lbl = QLabel("No se encontró la respuesta para comentar.")
            lbl.setStyleSheet("border: none; color: #666666;")
            self.layout_comentarios.addWidget(lbl)
            return

        comentarios = list(getattr(self.pregunta, "comentarios", []) or [])
        if not comentarios:
            lbl = QLabel("Todavía no hay comentarios.")
            lbl.setStyleSheet("border: none; color: #666666;")
            self.layout_comentarios.addWidget(lbl)
            return

        for fila in comentarios:
            self.layout_comentarios.addWidget(self._crear_burbuja_comentario(fila))

        self.layout_comentarios.addStretch()
        self.scroll_comentarios.verticalScrollBar().setValue(
            self.scroll_comentarios.verticalScrollBar().maximum()
        )

    def _crear_burbuja_comentario(self, fila):
        id_comentario = fila.get("id")
        id_profesional = fila.get("id_profesional")
        comentario = fila.get("comentario")
        fecha = fila.get("fecha")
        es_mio = (not self.solo_lectura) and str(id_profesional) == str(self.id_profesional)

        contenedor = QWidget()
        lay = QHBoxLayout(contenedor)
        lay.setContentsMargins(0, 0, 0, 0)

        if es_mio:
            lay.addStretch()

        burbuja = BurbujaComentario(mostrar_boton_borrar=es_mio)
        burbuja.setMaximumWidth(620)
        burbuja.setStyleSheet(
            f"""
            QFrame {{
                background-color: {"#DFF3C8" if es_mio else "#ECECEC"};
                border: 1px solid #D8D8D8;
                border-radius: 12px;
            }}
            """
        )
        lay_b = QVBoxLayout(burbuja)
        lay_b.setContentsMargins(10, 8, 10, 8)
        lay_b.setSpacing(6)

        lbl_txt = QLabel(str(comentario or ""))
        lbl_txt.setWordWrap(True)
        lbl_txt.setStyleSheet("border: none; color: #1A1A1A; font-size: 10.5pt;")
        lay_b.addWidget(lbl_txt)

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
        if not es_mio:
            boton_borrar.setToolTip("Solo puede borrar sus propios comentarios.")
        burbuja.set_boton_borrar(boton_borrar)
        fila_meta.addWidget(boton_borrar)
        lay_b.addLayout(fila_meta)

        lay.addWidget(burbuja)
        if not es_mio:
            lay.addStretch()
        return contenedor

    def _enviar_comentario(self):
        texto = self.txt_nuevo_comentario.toPlainText().strip()
        if not texto:
            self._msg.mostrar_advertencia("Atención", "Debe escribir un comentario.")
            return
        if not self.id_respuesta:
            self._msg.mostrar_advertencia("Atención", "No hay respuesta asociada a la pregunta.")
            return
        ids_existentes = [
            int(c.get("id"))
            for c in getattr(self.pregunta, "comentarios", [])
            if str(c.get("id", "")).lstrip("-").isdigit()
        ]
        siguiente_id_temporal = (min(ids_existentes) - 1) if ids_existentes else -1
        self.pregunta.comentarios.append(
            {
                "id": siguiente_id_temporal,
                "id_respuesta": self.id_respuesta,
                "id_profesional": self.id_profesional,
                "comentario": texto,
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        )
        self.txt_nuevo_comentario.clear()
        self._cargar_comentarios()

    def _borrar_comentario(self, id_comentario):
        comentarios = list(getattr(self.pregunta, "comentarios", []) or [])
        nuevos = [
            c for c in comentarios
            if str(c.get("id")) != str(id_comentario)
        ]
        if len(nuevos) == len(comentarios):
            self._msg.mostrar_advertencia("Error", "No se pudo borrar el comentario.")
            return
        self.pregunta.comentarios = nuevos
        self._cargar_comentarios()

    def toggle_audio(self, ruta):
        if not ruta or not os.path.exists(ruta):
            self.lbl_estado_audio.setText("Archivo de audio no encontrado")
            self.lbl_estado_audio.setStyleSheet("color: red; border: none;")
            return

        try:
            if self.player.mediaStatus() == QMediaPlayer.NoMedia:
                url = QUrl.fromLocalFile(os.path.abspath(ruta))
                self.player.setMedia(QMediaContent(url))

            if self.player.state() == QMediaPlayer.PlayingState:
                self.player.pause()
            else:
                self.player.play()
        except Exception as e:
            self.lbl_estado_audio.setText(f"Error de audio: {e}")
            self.lbl_estado_audio.setStyleSheet("color: red; border: none;")

    def cambio_estado(self, estado):
        if estado == QMediaPlayer.PlayingState:
            self.boton_play.setIcon(QIcon("assets/pausa.png"))
            self.boton_play.setIconSize(QSize(15, 15))
            self.lbl_estado_audio.setText("Reproduciendo...")
            self.lbl_estado_audio.setStyleSheet("color: green; border: none;")
        else:
            self.boton_play.setIcon(QIcon("assets/play.png"))
            self.boton_play.setIconSize(QSize(20, 20))
            self.lbl_estado_audio.setText("")

    def actualizar_posicion(self, posicion):
        self.slider_audio.setValue(posicion)
        self.lbl_tiempo_actual.setText(self.formatear_tiempo(posicion))

    def actualizar_duracion(self, duracion):
        self.slider_audio.setRange(0, duracion)
        self.lbl_tiempo_total.setText(self.formatear_tiempo(duracion))

    @staticmethod
    def formatear_tiempo(ms):
        segundos = ms // 1000
        minutos = segundos // 60
        segundos = segundos % 60
        return f"{minutos:02}:{segundos:02}"

    def closeEvent(self, event):
        try:
            self.player.stop()
            self.player.setMedia(QMediaContent())
        except Exception:
            pass
        super().closeEvent(event)

    def set_estado_analisis(self, texto, en_progreso=False, bloqueado=None):
        self.lbl_estado_ia.setText(f"Estado IA: {str(texto or '').strip()}")
        self._analisis_bloqueado = bool(en_progreso) if bloqueado is None else bool(bloqueado)
        self._aplicar_bloqueo_boton_analizar()
        if self.lbl_spinner_ia is None and self._spinner_host_ia is not None:
            self.lbl_spinner_ia = SpinnerCarga(parent=self._spinner_host_ia, tam=30, color="#111111")
            self.lbl_spinner_ia.move(0, 0)
        if self.lbl_spinner_ia is not None:
            if en_progreso:
                self.lbl_spinner_ia.start()
            else:
                self.lbl_spinner_ia.stop()

    def actualizar_resultado_ia(self, nivel, analisis):
        self.pregunta.nivel_ia = nivel
        self.pregunta.valoracion_ia = str(analisis or "").strip()
        self.lbl_nivel_ia.setText(f"Nivel: {self._texto_nivel(nivel)}")
        self.txt_analisis.setText(self.pregunta.valoracion_ia or "Sin comentario IA.")
        self.set_estado_analisis("Analizada", en_progreso=False)

    def _aplicar_bloqueo_boton_analizar(self):
        if self.solo_lectura:
            return
        self.boton_analizar.setEnabled(not self._analisis_bloqueado)
        if self._analisis_bloqueado:
            self.boton_analizar.setToolTip("Desactivado: esta pregunta ya se está analizando.")
        else:
            self.boton_analizar.setToolTip("Analizar esta pregunta con IA")


# Compatibilidad con imports antiguos.
VentanaDetallePregunta = VentanaDetallePreguntaProfesional
