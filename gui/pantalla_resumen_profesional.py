from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QScrollArea, QFrame, QSizePolicy, QButtonGroup, QProgressBar
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, QTimer, QEvent, pyqtSignal

from db.pregunta_db import obtener_preguntas_como_diccionario
from gui.estilos import *
from gui.spinner_carga import SpinnerCarga


def cargar_datos_preguntas():
    return obtener_preguntas_como_diccionario()


BAREMOS_RIESGO = [
    (887.5, "Riesgo muy bajo", "5 %"),
    (910.0, "Riesgo bajo", "10 %"),
    (920.0, "Riesgo bajo", "15 %"),
    (928.0, "Riesgo normal", "20 %"),
    (932.5, "Riesgo normal", "25 %"),
    (940.0, "Riesgo normal", "30 %"),
    (942.5, "Riesgo normal", "35 %"),
    (945.0, "Riesgo elevado", "40 %"),
    (947.5, "Riesgo elevado", "45 %"),
    (955.5, "Riesgo elevado", "50 %"),
    (959.0, "Riesgo elevado", "55 %"),
    (962.5, "Riesgo bastante elevado", "60 %"),
    (966.25, "Riesgo bastante elevado", "65 %"),
    (970.0, "Riesgo bastante elevado", "70 %"),
    (977.0, "Riesgo bastante elevado", "75 %"),
    (985.0, "Riesgo muy elevado", "80 %"),
    (988.75, "Riesgo muy elevado", "85 %"),
    (992.5, "Riesgo muy elevado", "90 %"),
    (996.5, "Riesgo muy elevado", "95 %"),
]

class _MenuAccionesResumen(QWidget):
    def __init__(self, solo_lectura=False, parent=None):
        super().__init__(parent)
        self.solo_lectura = solo_lectura
        self._desplegado = False
        self._altura_expandida = 40 if self.solo_lectura else 84
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self._construir_ui()

    def _construir_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.boton_mas = QPushButton("+")
        self.boton_mas.setFixedSize(36, 36)
        self.boton_mas.setCursor(Qt.PointingHandCursor)
        self.boton_mas.setToolTip("Acciones de entrevista")
        self.boton_mas.setStyleSheet(
            """
            QPushButton {
                background-color: #2B2A2A;
                color: white;
                border: none;
                border-radius: 18px;
                font-size: 15pt;
                font-weight: 400;
                text-align: center;
                padding: 0px;
            }
            QPushButton:hover { background-color: #464545; }
            """
        )
        self.boton_mas.clicked.connect(self._alternar_despliegue)
        self.boton_mas.installEventFilter(self)
        layout.addWidget(self.boton_mas, alignment=Qt.AlignLeft)

        self.panel_botones = QWidget()
        self.panel_botones.setMaximumHeight(0)
        self.panel_botones.setMinimumHeight(0)
        panel_layout = QVBoxLayout(self.panel_botones)
        panel_layout.setContentsMargins(0, 6, 0, 0)
        panel_layout.setSpacing(6)

        self.boton_anadir_comentario = QPushButton("Comentarios")
        self.boton_anadir_comentario.setCursor(Qt.PointingHandCursor)
        self.boton_anadir_comentario.setStyleSheet(ESTILO_BOTON_SOLICITUD)
        self.boton_anadir_comentario.setToolTip("Ver comentarios de la entrevista")
        self.boton_anadir_comentario.setFixedHeight(34)

        self.boton_analizar_entrevista = QPushButton("Analizar entrevista completa")
        self.boton_analizar_entrevista.setCursor(Qt.PointingHandCursor)
        self.boton_analizar_entrevista.setStyleSheet(ESTILO_BOTON_IA)
        self.boton_analizar_entrevista.setToolTip("Analizar toda la entrevista con IA")
        self.boton_analizar_entrevista.setFixedHeight(34)

        panel_layout.addWidget(self.boton_anadir_comentario, alignment=Qt.AlignLeft)
        if not self.solo_lectura:
            panel_layout.addWidget(self.boton_analizar_entrevista, alignment=Qt.AlignLeft)
        layout.addWidget(self.panel_botones, alignment=Qt.AlignLeft)

        self._animacion = QPropertyAnimation(self.panel_botones, b"maximumHeight", self)
        self._animacion.setDuration(180)
        self._animacion.setEasingCurve(QEasingCurve.OutCubic)

    def _alternar_despliegue(self):
        self._set_desplegado(not self._desplegado)

    def _set_desplegado(self, desplegado):
        if self._desplegado == desplegado:
            return

        self._desplegado = desplegado
        self.boton_mas.setText("✕" if desplegado else "+")
        self._animacion.stop()
        self._animacion.setStartValue(self.panel_botones.maximumHeight())
        self._animacion.setEndValue(self._altura_expandida if desplegado else 0)
        self._animacion.start()

    def eventFilter(self, source, event):
        if source is self.boton_mas:
            if event.type() == QEvent.Enter:
                self._set_desplegado(True)
            elif event.type() == QEvent.Leave:
                QTimer.singleShot(120, self._cerrar_si_no_hay_hover)
        return super().eventFilter(source, event)

    def leaveEvent(self, event):
        QTimer.singleShot(120, self._cerrar_si_no_hay_hover)
        super().leaveEvent(event)

    def _cerrar_si_no_hay_hover(self):
        if self.underMouse():
            return
        self._set_desplegado(False)


class PantallaResumen(QWidget):
    guardar_evaluacion_profesional = pyqtSignal()

    def __init__(self, solo_lectura=False, parent=None):
        super().__init__(parent)

        self.solo_lectura = solo_lectura
        self.PREGUNTAS_DATA = cargar_datos_preguntas()
        self.grupo_botones_entrar = QButtonGroup(self)
        self.grupo_botones_ia = QButtonGroup(self)
        self._tarjetas_pregunta = {}
        self._analisis_global_bloqueado = False
        self._preguntas_ia_bloqueadas = set()
        self._evaluacion_profesional_pendiente = False

        principal_layout = QVBoxLayout(self)
        principal_layout.setContentsMargins(10, 0, 60, 30)
        principal_layout.setSpacing(30)

        fila_acciones_superior = QHBoxLayout()
        fila_acciones_superior.setContentsMargins(10, 0, 10, 0)
        fila_acciones_superior.setSpacing(12)
        self.menu_acciones = _MenuAccionesResumen(solo_lectura=self.solo_lectura)
        self.boton_anadir_comentario = self.menu_acciones.boton_anadir_comentario
        self.boton_analizar_entrevista = self.menu_acciones.boton_analizar_entrevista
        fila_acciones_superior.addWidget(self.menu_acciones, alignment=Qt.AlignLeft | Qt.AlignTop)
        self._crear_panel_progreso_analisis()
        fila_acciones_superior.addWidget(self.panel_progreso_analisis, alignment=Qt.AlignLeft | Qt.AlignVCenter)
        fila_acciones_superior.addStretch()

        self._panel_global = QWidget()
        panel_layout = QVBoxLayout(self._panel_global)
        panel_layout.setContentsMargins(0, 0, 0, 0)
        panel_layout.setSpacing(8)

        self._panel_global_ia = self._crear_bloque_puntuacion_global("IA", COLOR_IA_MORADO)
        self._contenedor_global_ia = self._panel_global_ia["contenedor"]
        self.lbl_riesgo_global = self._panel_global_ia["lbl_riesgo"]
        self.lbl_puntuacion_global = self._panel_global_ia["lbl_puntuacion"]
        panel_layout.addWidget(self._contenedor_global_ia, alignment=Qt.AlignRight)

        self._panel_global_profesional = self._crear_bloque_puntuacion_global("Profesional", "#666666")
        self._contenedor_global_profesional = self._panel_global_profesional["contenedor"]
        self.lbl_riesgo_global_profesional = self._panel_global_profesional["lbl_riesgo"]
        self.lbl_puntuacion_global_profesional = self._panel_global_profesional["lbl_puntuacion"]
        self.boton_guardar_evaluacion_profesional = self._panel_global_profesional["boton_guardar"]
        panel_layout.addWidget(self._contenedor_global_profesional, alignment=Qt.AlignRight)


        self._panel_global.setVisible(False)
        fila_acciones_superior.addWidget(self._panel_global, alignment=Qt.AlignRight | Qt.AlignVCenter)
        principal_layout.addLayout(fila_acciones_superior)

        self.lbl_estado_entrevista_ia = QLabel()
        self.lbl_estado_entrevista_ia.setAlignment(Qt.AlignCenter)
        self._aplicar_estilo_estado_ia(self.lbl_estado_entrevista_ia, "sin evaluación", prefijo=True)
        principal_layout.addWidget(self.lbl_estado_entrevista_ia, 0, Qt.AlignLeft)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setStyleSheet(ESTILO_SCROLL)

        self.scroll_content_widget = QWidget()
        self.scroll_content_layout = QVBoxLayout(self.scroll_content_widget)
        self.scroll_content_layout.setAlignment(Qt.AlignTop)
        self.scroll_content_layout.setSpacing(30)
        self.scroll_content_layout.setContentsMargins(10, 0, 10, 30)
        self.scroll_area.setWidget(self.scroll_content_widget)
        principal_layout.addWidget(self.scroll_area, 1)

        boton_layout = QHBoxLayout()
        self.boton_atras = QPushButton("Volver")
        self.boton_atras.setCursor(Qt.PointingHandCursor)
        self.boton_atras.setStyleSheet(ESTILO_BOTON_SIG_ATR)
        self.boton_atras.setToolTip("Volver")
        boton_layout.addWidget(self.boton_atras)
        boton_layout.addStretch()
        principal_layout.addLayout(boton_layout)

    def _crear_panel_progreso_analisis(self):
        self._progreso_total_analisis = 0
        self._progreso_actual_analisis = 0

        self.panel_progreso_analisis = QFrame()
        self.panel_progreso_analisis.setVisible(False)
        self.panel_progreso_analisis.setStyleSheet(
            """
            QFrame {
                background-color: transparent;
                border: none;
            }
            """
        )
        layout = QVBoxLayout(self.panel_progreso_analisis)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        self.lbl_progreso_analisis = QLabel("0/0 preguntas analizadas")
        self.lbl_progreso_analisis.setStyleSheet(
            "border: none; background: transparent; color: #111111; font-size: 9.5pt; font-weight: 600;"
        )
        layout.addWidget(self.lbl_progreso_analisis)

        self.barra_progreso_analisis = QProgressBar()
        self.barra_progreso_analisis.setTextVisible(False)
        self.barra_progreso_analisis.setFixedSize(220, 10)
        self.barra_progreso_analisis.setRange(0, 100)
        self.barra_progreso_analisis.setValue(0)
        self.barra_progreso_analisis.setStyleSheet(
            """
            QProgressBar {
                background-color: #E3E3E3;
                border: none;
                border-radius: 5px;
            }
            QProgressBar::chunk {
                background-color: #111111;
                border-radius: 5px;
            }
            """
        )
        layout.addWidget(self.barra_progreso_analisis, alignment=Qt.AlignLeft)

    def _crear_bloque_puntuacion_global(self, titulo, color_texto):
        contenedor = QWidget()
        layout = QVBoxLayout(contenedor)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        lbl_titulo = QLabel(str(titulo))
        lbl_titulo.setStyleSheet(f"font-size: 9pt; font-weight: 700; color: {color_texto}; border: none;")
        layout.addWidget(lbl_titulo, alignment=Qt.AlignLeft)

        fila = QHBoxLayout()
        fila.setContentsMargins(0, 0, 0, 0)
        fila.setSpacing(8)

        boton_guardar = None
        es_profesional = str(titulo).strip().lower() == "profesional"
        if es_profesional and not self.solo_lectura:
            boton_guardar = QPushButton("Guardar")
            boton_guardar.setCursor(Qt.PointingHandCursor)
            boton_guardar.setFixedHeight(28)
            boton_guardar.setStyleSheet(
                """
                QPushButton {
                    background-color: #222222;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 4px 12px;
                    font-size: 9.5pt;
                    font-weight: 600;
                }
                QPushButton:hover { background-color: #3A3A3A; }
                QPushButton:disabled {
                    background-color: #CFCFCF;
                    color: #777777;
                }
                """
            )
            boton_guardar.setToolTip("Guardar evaluacion profesional en base de datos")
            boton_guardar.setVisible(False)
            boton_guardar.clicked.connect(self.guardar_evaluacion_profesional.emit)
            fila.addWidget(boton_guardar, alignment=Qt.AlignVCenter)

        lbl_riesgo = QLabel("")
        lbl_riesgo.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        lbl_riesgo.setVisible(False)
        fila.addWidget(lbl_riesgo, alignment=Qt.AlignVCenter)

        lbl_puntuacion = QLabel("Puntuación global: -")
        lbl_puntuacion.setStyleSheet(f"font-size: 11pt; font-weight: 600; color: {color_texto}; border: none;")
        fila.addWidget(lbl_puntuacion, alignment=Qt.AlignVCenter)

        layout.addLayout(fila)
        return {
            "contenedor": contenedor,
            "lbl_riesgo": lbl_riesgo,
            "lbl_puntuacion": lbl_puntuacion,
            "boton_guardar": boton_guardar,
        }

    def cargar_datos_respuestas(self, entrevista, nombre_interno=""):
        self._evaluacion_profesional_pendiente = False
        self._tarjetas_pregunta = {}
        for boton in list(self.grupo_botones_entrar.buttons()):
            self.grupo_botones_entrar.removeButton(boton)
        for boton in list(self.grupo_botones_ia.buttons()):
            self.grupo_botones_ia.removeButton(boton)
        while self.scroll_content_layout.count():
            item = self.scroll_content_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        _ = nombre_interno

        respuestas = list(getattr(entrevista, "respuestas", []) or [])
        self._actualizar_panel_global(entrevista, respuestas)
        self.set_estado_global_entrevista(getattr(entrevista, "estado_evaluacion_ia", "sin evaluación"))
        respuestas_por_pregunta = {
            int(getattr(r, "id_pregunta", 0)): r
            for r in respuestas
            if getattr(r, "id_pregunta", None) is not None
        }

        for i in range(1, 11):
            datos = self.PREGUNTAS_DATA.get(str(i), {})
            titulo = datos.get("titulo", f"Pregunta {i}")
            respuesta = respuestas_por_pregunta.get(i)
            tarjeta = self.crear_tarjeta_pregunta(i, titulo, respuesta)
            self.scroll_content_layout.addWidget(tarjeta)
        self._reaplicar_bloqueos_ia()

    def refrescar_desde_modelo(self, entrevista):
        respuestas = list(getattr(entrevista, "respuestas", []) or [])
        respuestas_por_pregunta = {
            int(getattr(r, "id_pregunta", 0)): r
            for r in respuestas
            if getattr(r, "id_pregunta", None) is not None
        }
        for numero in list(self._tarjetas_pregunta.keys()):
            pregunta = respuestas_por_pregunta.get(int(numero))
            if pregunta is None:
                continue
            self.actualizar_nivel_profesional_pregunta(numero, getattr(pregunta, "nivel_profesional", None))
            nivel_ia = getattr(pregunta, "nivel_ia", None)
            analisis_ia = getattr(pregunta, "valoracion_ia", "")
            if self._nivel_entero(nivel_ia) >= 0 or str(analisis_ia or "").strip():
                self.actualizar_resultado_analisis_pregunta(numero, nivel_ia, analisis_ia)
            else:
                refs = self._tarjetas_pregunta.get(int(numero), {})
                if refs.get("lbl_nivel_ia") is not None:
                    refs["lbl_nivel_ia"].setText(f"Nivel: {self._texto_nivel(nivel_ia)}")
                if refs.get("lbl_analisis") is not None:
                    refs["lbl_analisis"].setText("")
                if refs.get("lbl_titulo_analisis") is not None:
                    refs["lbl_titulo_analisis"].setVisible(False)
                if refs.get("caja_analisis") is not None:
                    refs["caja_analisis"].setVisible(False)
                self.set_estado_analisis_pregunta(numero, "Sin analizar", en_progreso=False)
        self._actualizar_panel_global(entrevista, respuestas)
        self._actualizar_estado_guardado_profesional(respuestas)
        self.set_estado_global_entrevista(getattr(entrevista, "estado_evaluacion_ia", "sin evaluacion"))
        self._reaplicar_bloqueos_ia()

    def crear_tarjeta_pregunta(self, numero, titulo, pregunta):
        tarjeta_frame = QFrame()
        tarjeta_frame.setStyleSheet(ESTILO_TARJETA_RESUMEN)

        tarjeta_layout = QVBoxLayout(tarjeta_frame)
        tarjeta_layout.setContentsMargins(25, 20, 25, 10)
        tarjeta_layout.setSpacing(10)

        top_tarjeta_layout = QHBoxLayout()
        top_tarjeta_layout.setSpacing(8)
        top_tarjeta_layout.setAlignment(Qt.AlignVCenter)

        lbl_titulo = QLabel(f"Pregunta {numero}: {titulo}", tarjeta_frame)
        lbl_titulo.setFont(QFont("Arial", 16, QFont.Bold))
        lbl_titulo.setStyleSheet("border: none; color: black;")
        lbl_titulo.setAlignment(Qt.AlignLeft)
        top_tarjeta_layout.addWidget(lbl_titulo, 0, Qt.AlignVCenter)

        estado_ia = QLabel(tarjeta_frame)
        estado_ia.setAlignment(Qt.AlignCenter)
        self._aplicar_estilo_estado_ia(
            estado_ia,
            "Analizada" if self._nivel_entero(getattr(pregunta, "nivel_ia", None)) >= 0 else "Sin analizar",
        )
        top_tarjeta_layout.addWidget(estado_ia, 0, Qt.AlignVCenter)
        top_tarjeta_layout.addStretch()

        niveles_layout = QHBoxLayout()
        niveles_layout.setSpacing(8)

        bloque_prof = QVBoxLayout()
        lbl_titulo_prof = QLabel("Profesional", tarjeta_frame)
        lbl_titulo_prof.setFont(QFont("Arial", 9, QFont.Bold))
        lbl_titulo_prof.setAlignment(Qt.AlignCenter)
        lbl_titulo_prof.setStyleSheet("border: none; color: #666666;")
        lbl_nivel_prof = QLabel(
            f"Nivel: {self._texto_nivel(getattr(pregunta, 'nivel_profesional', None))}",
            tarjeta_frame,
        )
        lbl_nivel_prof.setFont(QFont("Arial", 11, QFont.Bold))
        lbl_nivel_prof.setAlignment(Qt.AlignCenter)
        lbl_nivel_prof.setStyleSheet(ESTILO_NIVEL)
        bloque_prof.addWidget(lbl_titulo_prof)
        bloque_prof.addWidget(lbl_nivel_prof)

        bloque_ia = QVBoxLayout()
        lbl_titulo_ia = QLabel("IA", tarjeta_frame)
        lbl_titulo_ia.setFont(QFont("Arial", 9, QFont.Bold))
        lbl_titulo_ia.setAlignment(Qt.AlignCenter)
        lbl_titulo_ia.setStyleSheet(f"border: none; color: {COLOR_IA_MORADO};")
        lbl_nivel_ia = QLabel(f"Nivel: {self._texto_nivel(getattr(pregunta, 'nivel_ia', None))}", tarjeta_frame)
        lbl_nivel_ia.setFont(QFont("Arial", 11, QFont.Bold))
        lbl_nivel_ia.setAlignment(Qt.AlignCenter)
        lbl_nivel_ia.setStyleSheet(ESTILO_NIVEL_IA)
        bloque_ia.addWidget(lbl_titulo_ia)
        bloque_ia.addWidget(lbl_nivel_ia)

        niveles_layout.addLayout(bloque_prof)
        niveles_layout.addLayout(bloque_ia)
        top_tarjeta_layout.addLayout(niveles_layout)
        tarjeta_layout.addLayout(top_tarjeta_layout)

        lbl_respuesta_titulo = QLabel("Respuesta:", tarjeta_frame)
        lbl_respuesta_titulo.setFont(QFont("Arial", 11, QFont.Bold))
        lbl_respuesta_titulo.setStyleSheet("border: none; color: black;")
        lbl_respuesta_titulo.setAlignment(Qt.AlignLeft)
        tarjeta_layout.addWidget(lbl_respuesta_titulo)

        texto_respuesta = str(getattr(pregunta, "respuesta", "") or "").strip()
        if not texto_respuesta:
            texto_respuesta = "-"

        lbl_respuesta = QLabel(tarjeta_frame)
        lbl_respuesta.setFont(QFont("Arial", 11))
        lbl_respuesta.setWordWrap(True)
        lbl_respuesta.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        lbl_respuesta.setAlignment(Qt.AlignLeft)
        lbl_respuesta.setText(self._recortar_texto_dos_lineas_aprox(texto_respuesta))
        altura_linea = lbl_respuesta.fontMetrics().lineSpacing()
        lbl_respuesta.setMaximumHeight((altura_linea * 2) + 4)
        tarjeta_layout.addWidget(lbl_respuesta)

        analisis_ia = str(getattr(pregunta, "valoracion_ia", "") or "").strip()
        lbl_titulo_analisis = QLabel("Comentario IA:", tarjeta_frame)
        lbl_titulo_analisis.setStyleSheet(
            f"font-size: 12pt; font-weight: bold; color: {COLOR_IA_MORADO}; border: none;"
        )
        lbl_titulo_analisis.setVisible(bool(analisis_ia))
        tarjeta_layout.addWidget(lbl_titulo_analisis)

        caja_analisis = QFrame(tarjeta_frame)
        caja_analisis.setStyleSheet(
            f"""
            QFrame {{
                background-color: {COLOR_IA_MORADO_SUAVE};
                border: none;
                border-radius: 14px;
            }}
            """
        )
        caja_analisis.setVisible(bool(analisis_ia))
        analisis_layout = QVBoxLayout(caja_analisis)
        analisis_layout.setContentsMargins(16, 12, 16, 12)
        analisis_layout.setSpacing(8)

        lbl_analisis = QLabel(analisis_ia, caja_analisis)
        lbl_analisis.setFont(QFont("Arial", 11))
        lbl_analisis.setWordWrap(True)
        lbl_analisis.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        lbl_analisis.setAlignment(Qt.AlignJustify)
        lbl_analisis.setStyleSheet("font-size: 11pt; color: #222222; background: transparent;")
        analisis_layout.addWidget(lbl_analisis)
        tarjeta_layout.addWidget(caja_analisis)

        boton_layout = QHBoxLayout()
        boton_layout.setSpacing(8)
        boton_layout.addStretch()

        icono_ia = QIcon("assets/ia.png")
        spinner_ia = None
        spinner_host = None
        boton_ia = None
        if not self.solo_lectura:
            spinner_host = QWidget(tarjeta_frame)
            spinner_host.setFixedSize(30, 30)
            spinner_host.setStyleSheet("background: transparent; border: none;")
            boton_layout.addWidget(spinner_host)

            boton_ia = QPushButton()
            boton_ia.setFixedSize(45, 45)
            boton_ia.setIcon(icono_ia)
            boton_ia.setIconSize(QSize(25, 25))
            boton_ia.setCursor(Qt.PointingHandCursor)
            boton_ia.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: {COLOR_IA_MORADO_2};
                    border: none;
                    border-radius: 22px;
                    font-family: 'Arial';
                }}
                QPushButton:hover {{
                    background-color: {COLOR_IA_MORADO};
                }}
                """
            )
            boton_ia.setToolTip("Analizar con IA esta pregunta")
            self.grupo_botones_ia.addButton(boton_ia, numero)
            boton_layout.addWidget(boton_ia)

        icono_entrar = QIcon("assets/entrar.png")
        boton_entrar = QPushButton()
        boton_entrar.setFixedSize(45, 45)
        boton_entrar.setIcon(icono_entrar)
        boton_entrar.setIconSize(QSize(25, 25))
        boton_entrar.setCursor(Qt.PointingHandCursor)
        boton_entrar.setStyleSheet(ESTILO_BOTON_TARJETA)
        boton_entrar.setToolTip(f"Ver detalles de la respuesta {numero}")
        self.grupo_botones_entrar.addButton(boton_entrar, numero)
        boton_layout.addWidget(boton_entrar)

        tarjeta_layout.addLayout(boton_layout)
        self._tarjetas_pregunta[numero] = {
            "pregunta": pregunta,
            "lbl_nivel_prof": lbl_nivel_prof,
            "lbl_nivel_ia": lbl_nivel_ia,
            "lbl_analisis": lbl_analisis,
            "lbl_titulo_analisis": lbl_titulo_analisis,
            "caja_analisis": caja_analisis,
            "lbl_estado": estado_ia,
            "spinner_host": spinner_host,
            "spinner_ia": spinner_ia,
            "boton_ia": boton_ia,
        }
        return tarjeta_frame

    @staticmethod
    def _texto_nivel(valor):
        if valor is None:
            return "-"
        try:
            valor_int = int(valor)
        except (TypeError, ValueError):
            return "-"
        if valor_int < 0:
            return "-"
        return str(valor_int)

    @staticmethod
    def _nivel_entero(valor):
        try:
            nivel = int(valor)
        except (TypeError, ValueError):
            return -1
        return nivel if nivel >= 0 else -1

    @staticmethod
    def _recortar_texto_dos_lineas_aprox(texto):
        texto_limpio = " ".join(str(texto or "").split())
        if not texto_limpio:
            return "-"
        max_chars = 190
        if len(texto_limpio) <= max_chars:
            return texto_limpio
        recortado = texto_limpio[:max_chars].rstrip()
        ultimo_espacio = recortado.rfind(" ")
        if ultimo_espacio > int(max_chars * 0.6):
            recortado = recortado[:ultimo_espacio]
        return recortado + "..."

    def _actualizar_panel_global(self, entrevista, respuestas):
        mostrar_ia = self._todas_preguntas_analizadas(respuestas)
        mostrar_profesional = self._todas_preguntas_con_nivel_profesional(respuestas)

        self._actualizar_bloque_puntuacion_global(
            self.lbl_puntuacion_global_profesional,
            self.lbl_riesgo_global_profesional,
            getattr(entrevista, "puntuacion_profesional", None) if mostrar_profesional else None,
        )
        self._contenedor_global_profesional.setVisible(mostrar_profesional)

        self._actualizar_bloque_puntuacion_global(
            self.lbl_puntuacion_global,
            self.lbl_riesgo_global,
            getattr(entrevista, "puntuacion_ia", None) if mostrar_ia else None,
        )
        self._contenedor_global_ia.setVisible(mostrar_ia)

        self._panel_global.setVisible(mostrar_ia or mostrar_profesional)
        self._actualizar_estado_guardado_profesional(respuestas)
        self._ajustar_chip_riesgo_global()

    def _actualizar_estado_guardado_profesional(self, respuestas):
        if self.boton_guardar_evaluacion_profesional is None:
            return
        completo = self._todas_preguntas_con_nivel_profesional(respuestas)
        visible = bool(completo and self._evaluacion_profesional_pendiente and not self.solo_lectura)
        self.boton_guardar_evaluacion_profesional.setVisible(visible)
        self.boton_guardar_evaluacion_profesional.setEnabled(visible)

    def _actualizar_bloque_puntuacion_global(self, lbl_puntuacion, lbl_riesgo, puntuacion):
        texto_puntuacion = self._texto_puntuacion_global(puntuacion)
        lbl_puntuacion.setText(f"Puntuacion global: {texto_puntuacion}")

        if texto_puntuacion == "-":
            lbl_riesgo.setVisible(False)
            return

        riesgo_txt, pct_txt, color_bg, color_txt = self._clasificar_riesgo(puntuacion)
        lbl_riesgo.setText(f"{riesgo_txt} ({pct_txt})")
        lbl_riesgo.setStyleSheet(
            f"""
            QLabel {{
                background-color: {color_bg};
                color: {color_txt};
                border-radius: 10px;
                padding: 3px 10px;
                font-size: 10pt;
                font-weight: 500;
                border: none;
            }}
            """
        )
        lbl_riesgo.setVisible(True)

    def _ajustar_chip_riesgo_global(self):
        for label in (self.lbl_riesgo_global_profesional, self.lbl_riesgo_global):
            if not label.isVisible():
                continue
            label.ensurePolished()
            label.setFixedSize(label.sizeHint())
            label.updateGeometry()
        QTimer.singleShot(0, self._reajustar_chip_riesgo_global)

    def _reajustar_chip_riesgo_global(self):
        for label in (self.lbl_riesgo_global_profesional, self.lbl_riesgo_global):
            if not label.isVisible():
                continue
            label.ensurePolished()
            label.setFixedSize(label.sizeHint())
            label.updateGeometry()

    def set_estado_global_entrevista(self, estado):
        self._aplicar_estilo_estado_ia(self.lbl_estado_entrevista_ia, estado, prefijo=True)

    def iniciar_progreso_analisis_completo(self, total_preguntas):
        self._progreso_total_analisis = max(0, int(total_preguntas or 0))
        self._progreso_actual_analisis = 0
        self.panel_progreso_analisis.setVisible(self._progreso_total_analisis > 0)
        self._refrescar_progreso_analisis()

    def actualizar_progreso_analisis_completo(self, preguntas_analizadas):
        self._progreso_actual_analisis = max(0, int(preguntas_analizadas or 0))
        self._refrescar_progreso_analisis()

    def finalizar_progreso_analisis_completo(self, ocultar=False):
        if self._progreso_total_analisis > 0:
            self._progreso_actual_analisis = self._progreso_total_analisis
            self._refrescar_progreso_analisis()
        if ocultar:
            self.panel_progreso_analisis.setVisible(False)
            self._progreso_total_analisis = 0
            self._progreso_actual_analisis = 0
            self.barra_progreso_analisis.setValue(0)

    def ocultar_progreso_analisis_completo(self):
        self.panel_progreso_analisis.setVisible(False)
        self._progreso_total_analisis = 0
        self._progreso_actual_analisis = 0
        self.lbl_progreso_analisis.setText("0/0 preguntas analizadas")
        self.barra_progreso_analisis.setValue(0)

    def set_estado_analisis_pregunta(self, numero, estado, en_progreso=False):
        refs = self._tarjetas_pregunta.get(int(numero), {})
        lbl_estado = refs.get("lbl_estado")
        if lbl_estado is not None:
            self._aplicar_estilo_estado_ia(lbl_estado, estado)

        spinner = refs.get("spinner_ia")
        spinner_host = refs.get("spinner_host")
        if spinner is None and spinner_host is not None:
            spinner = SpinnerCarga(parent=spinner_host, tam=30, color="#111111")
            spinner.move(0, 0)
            refs["spinner_ia"] = spinner
        if spinner is not None:
            if en_progreso:
                spinner.start()
            else:
                spinner.stop()

    def actualizar_resultado_analisis_pregunta(self, numero, nivel, analisis):
        refs = self._tarjetas_pregunta.get(int(numero), {})
        lbl_nivel_ia = refs.get("lbl_nivel_ia")
        if lbl_nivel_ia is not None:
            lbl_nivel_ia.setText(f"Nivel: {self._texto_nivel(nivel)}")

        lbl_analisis = refs.get("lbl_analisis")
        if lbl_analisis is not None:
            lbl_analisis.setText(str(analisis or "").strip())

        lbl_titulo_analisis = refs.get("lbl_titulo_analisis")
        if lbl_titulo_analisis is not None:
            lbl_titulo_analisis.setVisible(bool(str(analisis or "").strip()))

        caja_analisis = refs.get("caja_analisis")
        if caja_analisis is not None:
            caja_analisis.setVisible(bool(str(analisis or "").strip()))

        self.set_estado_analisis_pregunta(numero, "Analizada", en_progreso=False)

    def actualizar_nivel_profesional_pregunta(self, numero, nivel):
        refs = self._tarjetas_pregunta.get(int(numero), {})
        lbl_nivel_prof = refs.get("lbl_nivel_prof")
        if lbl_nivel_prof is not None:
            lbl_nivel_prof.setText(f"Nivel: {self._texto_nivel(nivel)}")

    def marcar_evaluacion_profesional_pendiente(self, pendiente=True):
        self._evaluacion_profesional_pendiente = bool(pendiente)
        respuestas = []
        for numero in sorted(self._tarjetas_pregunta.keys()):
            refs = self._tarjetas_pregunta.get(int(numero), {})
            pregunta = refs.get("pregunta")
            if pregunta is not None:
                respuestas.append(pregunta)
        self._actualizar_estado_guardado_profesional(respuestas)

    def bloquear_controles_ia(self, bloquear):
        self._analisis_global_bloqueado = bool(bloquear)
        self._reaplicar_bloqueos_ia()

    def bloquear_ia_pregunta(self, numero, bloquear=True):
        numero = int(numero)
        if bloquear:
            self._preguntas_ia_bloqueadas.add(numero)
        else:
            self._preguntas_ia_bloqueadas.discard(numero)
        self._reaplicar_bloqueos_ia()

    def limpiar_bloqueos_ia_preguntas(self):
        self._preguntas_ia_bloqueadas.clear()
        self._reaplicar_bloqueos_ia()

    def _reaplicar_bloqueos_ia(self):
        if not self.solo_lectura:
            self.boton_analizar_entrevista.setEnabled(not self._analisis_global_bloqueado)
            if self._analisis_global_bloqueado:
                self.boton_analizar_entrevista.setToolTip("Desactivado: se está analizando la entrevista completa.")
            else:
                self.boton_analizar_entrevista.setToolTip("Analizar toda la entrevista con IA")

        for numero, refs in self._tarjetas_pregunta.items():
            boton = refs.get("boton_ia")
            if boton is None:
                continue
            bloqueado = self._analisis_global_bloqueado or int(numero) in self._preguntas_ia_bloqueadas
            boton.setEnabled(not bloqueado)
            if self._analisis_global_bloqueado:
                boton.setToolTip("Desactivado: se está analizando la entrevista completa.")
            elif int(numero) in self._preguntas_ia_bloqueadas:
                boton.setToolTip("Desactivado: esta pregunta ya se está analizando.")
            else:
                boton.setToolTip("Analizar con IA esta pregunta")

    def _refrescar_progreso_analisis(self):
        total = max(0, self._progreso_total_analisis)
        actual = min(max(0, self._progreso_actual_analisis), total if total > 0 else 0)
        self.lbl_progreso_analisis.setText(f"{actual}/{total} preguntas analizadas")
        porcentaje = int((actual / total) * 100) if total > 0 else 0
        self.barra_progreso_analisis.setValue(porcentaje)

    def _aplicar_estilo_estado_ia(self, label, estado, prefijo=False):
        texto, color = obtener_estado_ia_visual(estado)
        label.setText(f"Estado IA: {texto}" if prefijo else texto)
        label.setStyleSheet(f"QLabel {{ {estilo_chip_estado(color)} }}")
        label.ensurePolished()
        label.setFixedSize(label.sizeHint())
        label.updateGeometry()

    @staticmethod
    def _todas_preguntas_analizadas(respuestas):
        if len(respuestas) < 10:
            return False
        preguntas_validas = {}
        for r in respuestas:
            try:
                id_preg = int(getattr(r, "id_pregunta", 0))
            except (TypeError, ValueError):
                continue
            preguntas_validas[id_preg] = r
        if any(i not in preguntas_validas for i in range(1, 11)):
            return False
        for i in range(1, 11):
            nivel = getattr(preguntas_validas[i], "nivel_ia", None)
            try:
                nivel_int = int(nivel)
            except (TypeError, ValueError):
                return False
            if nivel_int < 0:
                return False
        return True

    @staticmethod
    def _todas_preguntas_con_nivel_profesional(respuestas):
        if len(respuestas) < 10:
            return False
        preguntas_validas = {}
        for r in respuestas:
            try:
                id_preg = int(getattr(r, "id_pregunta", 0))
            except (TypeError, ValueError):
                continue
            preguntas_validas[id_preg] = r
        if any(i not in preguntas_validas for i in range(1, 11)):
            return False
        for i in range(1, 11):
            nivel = getattr(preguntas_validas[i], "nivel_profesional", None)
            try:
                nivel_int = int(nivel)
            except (TypeError, ValueError):
                return False
            if nivel_int < 0:
                return False
        return True

    @staticmethod
    def _texto_puntuacion_global(puntuacion):
        if puntuacion is None:
            return "-"
        try:
            valor = float(puntuacion)
        except (TypeError, ValueError):
            return "-"
        if valor < 0:
            return "-"
        return f"{valor:.2f}"

    @staticmethod
    def _clasificar_riesgo(puntuacion):
        try:
            valor = float(puntuacion)
        except Exception:
            color_bg = "#D8D8D8"
            return "Sin entrevista", "-", color_bg, color_texto_contraste(color_bg)

        for limite, texto, pct in BAREMOS_RIESGO:
            if valor <= limite:
                color_bg = COLOR_RIESGO.get(texto, "#D8D8D8")
                return texto, pct, color_bg, color_texto_contraste(color_bg)

        color_bg = COLOR_RIESGO["Riesgo maximo"]
        return "Riesgo maximo", "100 %", color_bg, color_texto_contraste(color_bg)
