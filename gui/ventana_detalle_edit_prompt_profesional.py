from datetime import datetime

from PyQt5.QtCore import Qt, QEvent, QSize
from PyQt5.QtGui import QFont, QPixmap, QTextCharFormat, QIcon, QColor
from PyQt5.QtWidgets import (QComboBox, QDialog, QFrame, QHBoxLayout, QLabel, QPushButton, QScrollArea, QSizePolicy, QTextEdit, QVBoxLayout, QWidget)

from db.pregunta_db import obtener_preguntas_como_diccionario
from db.prompt_db import guardar_prompt_version, obtener_versiones_prompt_por_pregunta
from gui.estilos import *


class PlantillaConMarcadoresProtegidos(QTextEdit):
    PROTECTED_PROP = 3001
    PREGUNTA = "pregunta"
    RESPUESTA = "respuesta"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.cursorPositionChanged.connect(self._mover_cursor_fuera_de_protegido)

    def set_desde_template(self, plantilla, texto_pregunta):
        self.clear()
        self._render_template(str(plantilla or ""), str(texto_pregunta or ""))

    def get_template(self):
        texto = self.toPlainText()
        rangos = self._rangos_protegidos()
        if not rangos:
            return texto

        out = []
        cursor = 0
        for inicio, fin, tipo in rangos:
            if inicio > cursor:
                out.append(texto[cursor:inicio])
            out.append("{pregunta}" if tipo == self.PREGUNTA else "{respuesta}")
            cursor = max(cursor, fin)
        if cursor < len(texto):
            out.append(texto[cursor:])
        return "".join(out)

    def _render_template(self, plantilla, texto_pregunta):
        c = self.textCursor()
        i = 0
        while i < len(plantilla):
            p = plantilla.find("{pregunta}", i)
            r = plantilla.find("{respuesta}", i)
            marks = [x for x in (p, r) if x != -1]
            if not marks:
                self._insert_normal(c, plantilla[i:])
                break

            idx = min(marks)
            if idx > i:
                self._insert_normal(c, plantilla[i:idx])

            if idx == p:
                self._insert_protegido(c, "{pregunta}", self.PREGUNTA, oculto=True)
                i = p + len("{pregunta}")
            else:
                self._insert_protegido(c, "{respuesta}", self.RESPUESTA)
                i = r + len("{respuesta}")

    def _insert_protegido(self, cursor, texto, kind, oculto=False):
        fmt = QTextCharFormat()
        fmt.setFontWeight(QFont.Bold)
        fmt.setProperty(self.PROTECTED_PROP, kind)
        if oculto:
            fmt.setForeground(QColor(0, 0, 0, 0))
        cursor.insertText(texto, fmt)

    @staticmethod
    def _insert_normal(cursor, texto):
        fmt = QTextCharFormat()
        fmt.setFontWeight(QFont.Normal)
        fmt.setProperty(PlantillaConMarcadoresProtegidos.PROTECTED_PROP, None)
        cursor.insertText(texto, fmt)

    def _rangos_protegidos(self):
        rangos = []
        block = self.document().firstBlock()
        while block.isValid():
            it = block.begin()
            while not it.atEnd():
                frag = it.fragment()
                if frag.isValid():
                    kind = frag.charFormat().property(self.PROTECTED_PROP)
                    if kind in (self.PREGUNTA, self.RESPUESTA):
                        ini = frag.position()
                        rangos.append((ini, ini + len(frag.text()), str(kind)))
                it += 1
            block = block.next()

        if not rangos:
            return []
        rangos.sort(key=lambda x: (x[0], x[1]))

        merged = [rangos[0]]
        for ini, fin, kind in rangos[1:]:
            m_ini, m_fin, m_kind = merged[-1]
            if kind == m_kind and ini <= m_fin:
                merged[-1] = (m_ini, max(m_fin, fin), m_kind)
            else:
                merged.append((ini, fin, kind))
        return merged

    def _interseca_protegido(self, ini, fin):
        if ini > fin:
            ini, fin = fin, ini
        for p_ini, p_fin, _ in self._rangos_protegidos():
            if not (fin <= p_ini or ini >= p_fin):
                return True
        return False

    def _pos_en_protegido(self, pos):
        for ini, fin, _ in self._rangos_protegidos():
            if ini <= pos < fin:
                return True
        return False

    def _mover_cursor_fuera_de_protegido(self):
        c = self.textCursor()
        pos = c.position()
        for ini, fin, _ in self._rangos_protegidos():
            if ini <= pos < fin:
                c.setPosition(ini if (pos - ini) < (fin - pos) else fin)
                self.setTextCursor(c)
                return

    def keyPressEvent(self, event):
        c = self.textCursor()
        s_ini, s_fin = c.selectionStart(), c.selectionEnd()

        if self._interseca_protegido(s_ini, s_fin):
            return
        if event.key() == Qt.Key_Backspace and s_ini == s_fin and self._pos_en_protegido(c.position() - 1):
            return
        if event.key() == Qt.Key_Delete and s_ini == s_fin and self._pos_en_protegido(c.position()):
            return
        if s_ini == s_fin and self._pos_en_protegido(c.position()):
            return

        super().keyPressEvent(event)

    def insertFromMimeData(self, source):
        c = self.textCursor()
        if self._interseca_protegido(c.selectionStart(), c.selectionEnd()):
            return
        if self._pos_en_protegido(c.position()):
            return
        super().insertFromMimeData(source)

    def posicion_marcador_pregunta(self):
        for inicio, _, tipo in self._rangos_protegidos():
            if tipo == self.PREGUNTA:
                return inicio
        return None

class VentanaDetallePromptEditProfesional(QDialog):
    def __init__(self, numero_pregunta=None, numero_prompt=None, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(1080, 700)

        self.numero_pregunta = int(numero_pregunta if numero_pregunta is not None else numero_prompt)
        self._cierre_confirmado = False
        self._cargando_combo = False
        self._index_version_actual = 0
        self._altura_inicial_aplicada = False

        preguntas = obtener_preguntas_como_diccionario()
        self._texto_pregunta = str(preguntas.get(str(self.numero_pregunta), {}).get("texto", "")).rstrip()
        self._versiones = obtener_versiones_prompt_por_pregunta(self.numero_pregunta) or [self._version_vacia()]

        self._build_ui()
        self._cargar_combo_versiones()
        self._estado_inicial = self._serializar_estado()

    def _version_vacia(self):
        return {
            "id": None,
            "id_pregunta": self.numero_pregunta,
            "titulo": f"Prompt {self.numero_pregunta}",
            "plantilla": "",
            "descripcion": "",
            "version": 1,
            "activo": 1,
            "fecha_modificacion": None,
        }

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        self.frame_fondo = QFrame()
        self.frame_fondo.setObjectName("FondoDetalle")
        self.frame_fondo.setStyleSheet(ESTILO_VENTANA_DETALLE)
        root.addWidget(self.frame_fondo)

        layout = QVBoxLayout(self.frame_fondo)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        layout.addLayout(self._build_header())
        layout.addWidget(self._build_scroll(), 1)
        layout.addLayout(self._build_actions())

    def _build_header(self):
        l = QHBoxLayout()
        l.addWidget(self._label_titulo())
        l.addStretch()

        ancho = 200
        self.combo_version = QComboBox()
        self.combo_version.setStyleSheet(
            ESTILO_COMBOBOX
            + """
            QComboBox { border-radius: 10px; }
            QComboBox::drop-down { border-top-right-radius: 10px; border-bottom-right-radius: 10px; }
            """
        )
        self.combo_version.setCursor(Qt.PointingHandCursor)
        self.combo_version.setFixedSize(ancho, 32)
        self.combo_version.currentIndexChanged.connect(self._cambiar_version)

        self.boton_nueva_version = QPushButton("Nueva versión")
        self.boton_nueva_version.setStyleSheet(ESTILO_BOTON_SOLICITUD)
        self.boton_nueva_version.setCursor(Qt.PointingHandCursor)
        self.boton_nueva_version.setFixedSize(ancho, 32)
        self.boton_nueva_version.clicked.connect(self._crear_nueva_version_borrador)

        self.lbl_ultima_edicion = QLabel("Última vez editado:\n-")
        self.lbl_ultima_edicion.setFont(QFont("Arial", 10))
        self.lbl_ultima_edicion.setStyleSheet("border: none; color: #333;")
        self.lbl_ultima_edicion.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.lbl_ultima_edicion.setMinimumWidth(170)

        l.addWidget(self.combo_version)
        l.addWidget(self.boton_nueva_version)
        l.addWidget(self.lbl_ultima_edicion)
        return l

    def _label_titulo(self):
        lbl = QLabel(f"Prompt {self.numero_pregunta}")
        lbl.setFont(QFont("Arial", 16, QFont.Bold))
        lbl.setStyleSheet("border: none; color: black;")
        lbl.setAlignment(Qt.AlignLeft)
        return lbl

    def _build_scroll(self):
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setStyleSheet(ESTILO_SCROLL)

        self.scroll_widget = QWidget()
        self.scroll_widget.setStyleSheet("background-color: transparent;")
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setContentsMargins(4, 4, 4, 4)
        self.scroll_layout.setSpacing(12)

        self.txt_titulo = self._crear_textedit(min_height=58)
        self.txt_plantilla = self._crear_textedit(min_height=260, plantilla=True)
        self.txt_descripcion = self._crear_textedit(min_height=95)
        self._crear_boton_info_inline_en_plantilla()

        self.scroll_layout.addWidget(self._label_campo("<b>Título (Editable):</b>"))
        self.scroll_layout.addWidget(self.txt_titulo)
        self.scroll_layout.addWidget(self._label_campo("<b>Plantilla (bloqueando {pregunta} y {respuesta}):</b>"))
        self.scroll_layout.addWidget(self.txt_plantilla)
        self.scroll_layout.addWidget(self._label_campo("<b>Descripción (Editable):</b>"))
        self.scroll_layout.addWidget(self.txt_descripcion)
        self.scroll_layout.addStretch(1)

        self.scroll_area.setWidget(self.scroll_widget)
        return self.scroll_area

    def _crear_boton_info_inline_en_plantilla(self):
        self.boton_info_pregunta = QPushButton(self.txt_plantilla.viewport())
        self.boton_info_pregunta.setFixedSize(32, 32)
        self.boton_info_pregunta.setIcon(QIcon("assets/info.png"))
        self.boton_info_pregunta.setIconSize(QSize(24, 24))
        self.boton_info_pregunta.setStyleSheet(
            """
            QPushButton { background: rgba(200, 200, 200, 0.6); border-radius: 15px; padding: 10px; }
            QPushButton:hover { background-color: rgba(128, 128, 128, 0.6); border-radius: 15px; }
            """
        )
        self.boton_info_pregunta.setCursor(Qt.PointingHandCursor)
        self.boton_info_pregunta.installEventFilter(self)

        self.popup_ayuda = QLabel(self)
        self.popup_ayuda.setStyleSheet(
            """
            QLabel {
                background-color: #FFFFFF;
                color: #333333;
                border: 2px solid #333333;
                border-radius: 15px;
                padding: 20px;
                font-family: 'Arial';
                font-size: 20px;
                font-weight: normal;
            }
            """
        )
        self.popup_ayuda.setWordWrap(True)
        self.popup_ayuda.setFixedWidth(400)
        self.popup_ayuda.setText(self._texto_pregunta or "Sin informacion adicional.")
        self.popup_ayuda.adjustSize()
        self.popup_ayuda.hide()

        self.txt_plantilla.textChanged.connect(self._reposicionar_boton_info_pregunta)
        self.txt_plantilla.verticalScrollBar().valueChanged.connect(self._reposicionar_boton_info_pregunta)
        self.txt_plantilla.horizontalScrollBar().valueChanged.connect(self._reposicionar_boton_info_pregunta)

    def _reposicionar_boton_info_pregunta(self):
        pos = self.txt_plantilla.posicion_marcador_pregunta()
        if pos is None:
            self.boton_info_pregunta.hide()
            return
        cursor = self.txt_plantilla.textCursor()
        cursor.setPosition(pos)
        rect = self.txt_plantilla.cursorRect(cursor)
        self.boton_info_pregunta.move(rect.x(), rect.y() - 2)
        self.boton_info_pregunta.show()

    def _build_actions(self):
        l = QHBoxLayout()
        l.setContentsMargins(0, 0, 0, 0)

        self.boton_cerrar = self._crear_boton("Cerrar", ESTILO_BOTON_SIG_ATR, self.cerrar_ventana)
        self.boton_guardar = self._crear_boton(
            "Guardar",
            ESTILO_BOTON_SIG_ATR.replace("black", "#792A24").replace("rgba(71, 70, 70, 0.7)", "#C03930"),
            self.guardar_datos,
        )
        self.boton_guardar.setToolTip("Guardar prompt")

        l.addWidget(self.boton_cerrar)
        l.addStretch()
        l.addWidget(self.boton_guardar)
        return l

    @staticmethod
    def _label_campo(texto):
        lbl = QLabel(texto)
        lbl.setFont(QFont("Arial", 11))
        return lbl

    def _crear_textedit(self, min_height, plantilla=False):
        w = PlantillaConMarcadoresProtegidos() if plantilla else QTextEdit()
        w.setStyleSheet(ESTILO_INPUT)
        w.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        w.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        w.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        w.setFixedHeight(min_height)
        w.setProperty("base_height", int(min_height))
        return w

    @staticmethod
    def _crear_boton(texto, estilo, slot):
        b = QPushButton(texto)
        b.setFont(QFont("Arial", 11))
        b.setFixedSize(110, 40)
        b.setCursor(Qt.PointingHandCursor)
        b.setStyleSheet(estilo)
        b.clicked.connect(slot)
        return b

    @staticmethod
    def _ajustar_altura(widget, min_height):
        widget.setFixedHeight(max(min_height, int(widget.document().size().height()) + 16))

    def _cargar_combo_versiones(self):
        self._cargando_combo = True
        self.combo_version.clear()
        activa = 0
        for i, v in enumerate(self._versiones):
            sufijo = " (activa)" if int(v.get("activo", 0)) == 1 else ""
            self.combo_version.addItem(f"Versión {int(v.get('version', 1))}{sufijo}")
            if int(v.get("activo", 0)) == 1:
                activa = i
        self.combo_version.setCurrentIndex(activa)
        self._index_version_actual = activa
        self._cargando_combo = False
        self._cargar_version_en_form(activa)

    def _cargar_version_en_form(self, index):
        if not (0 <= index < len(self._versiones)):
            return
        v = self._versiones[index]
        v["plantilla"] = self._canonizar_plantilla(v.get("plantilla", ""))
        self.txt_titulo.setText(str(v.get("titulo", "")))
        self.txt_plantilla.set_desde_template(str(v.get("plantilla", "")), self._texto_pregunta)
        self.txt_descripcion.setText(str(v.get("descripcion", "")))
        self.lbl_ultima_edicion.setText("Última vez editado:\n" + self._formatear_fecha(v.get("fecha_modificacion")))
        self._reposicionar_boton_info_pregunta()
        if not self._altura_inicial_aplicada:
            self._ajustar_altura_inicial(self.txt_titulo)
            self._ajustar_altura_inicial(self.txt_plantilla)
            self._ajustar_altura_inicial(self.txt_descripcion)
            self._altura_inicial_aplicada = True
            self._reposicionar_boton_info_pregunta()

    def _ajustar_altura_inicial(self, widget):
        base = int(widget.property("base_height") or 0)
        self._ajustar_altura(widget, base)

    def _volcar_form_en_version(self, index):
        if not (0 <= index < len(self._versiones)):
            return
        self._versiones[index]["titulo"] = self.txt_titulo.toPlainText().strip()
        plantilla = self.txt_plantilla.get_template().strip()
        self._versiones[index]["plantilla"] = self._canonizar_plantilla(plantilla)
        self._versiones[index]["descripcion"] = self.txt_descripcion.toPlainText().strip()

    def _normalizar_placeholders(self, plantilla):
        texto = str(plantilla or "")
        pregunta = str(self._texto_pregunta or "").strip()
        if pregunta:
            texto = texto.replace(pregunta, "{pregunta}")
        return texto

    def _dejar_un_placeholder(self, texto, token):
        primero = texto.find(token)
        if primero == -1:
            return texto
        cabeza = texto[:primero + len(token)]
        cola = texto[primero + len(token):].replace(token, "")
        return cabeza + cola

    def _canonizar_plantilla(self, plantilla):
        texto = self._normalizar_placeholders(plantilla)
        texto = self._dejar_un_placeholder(texto, "{pregunta}")
        texto = self._dejar_un_placeholder(texto, "{respuesta}")
        return texto

    def _cambiar_version(self, index):
        if self._cargando_combo:
            return
        self._volcar_form_en_version(self._index_version_actual)
        self._index_version_actual = int(index)
        self._cargar_version_en_form(self._index_version_actual)

    def _crear_nueva_version_borrador(self):
        self._volcar_form_en_version(self._index_version_actual)
        siguiente = max(int(v.get("version", 1)) for v in self._versiones) + 1
        base = dict(self._versiones[self._index_version_actual])
        base.update({"id": None, "version": siguiente, "activo": 0, "fecha_modificacion": None})
        self._versiones.insert(0, base)

        self._cargando_combo = True
        self.combo_version.insertItem(0, f"Versión {siguiente} (nueva)")
        self.combo_version.setCurrentIndex(0)
        self._cargando_combo = False
        self._index_version_actual = 0
        self._cargar_version_en_form(0)

    def _serializar_estado(self):
        self._volcar_form_en_version(self._index_version_actual)
        return tuple(
            (
                v.get("id"),
                int(v.get("version", 1)),
                str(v.get("titulo", "")),
                str(v.get("plantilla", "")),
                str(v.get("descripcion", "")),
                int(v.get("activo", 0)),
            )
            for v in self._versiones
        )

    @staticmethod
    def _formatear_fecha(fecha_raw):
        if not fecha_raw:
            return "-"
        txt = str(fecha_raw).strip()
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
            try:
                return datetime.strptime(txt, fmt).strftime("%d/%m/%Y %H:%M")
            except ValueError:
                pass
        return txt

    def hay_cambios(self):
        return self._serializar_estado() != self._estado_inicial

    def guardar_datos(self):
        self._volcar_form_en_version(self._index_version_actual)
        v = self._versiones[self._index_version_actual]
        prompt_id = guardar_prompt_version(
            id_pregunta=self.numero_pregunta,
            titulo=v.get("titulo", ""),
            plantilla=v.get("plantilla", ""),
            descripcion=v.get("descripcion", ""),
            version=v.get("version"),
            id_prompt=v.get("id"),
            activar=True,
        )
        if prompt_id is not None:
            self.accept()

    def mostrar_confirmacion_cerrar(self):
        d = QDialog(self)
        d.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        d.setAttribute(Qt.WA_TranslucentBackground)
        d.setModal(True)

        main = QVBoxLayout(d)
        main.setContentsMargins(0, 0, 0, 0)

        fondo = QFrame()
        fondo.setObjectName("FondoDialogo")
        fondo.setStyleSheet(ESTILO_DIALOGO_ERROR)
        main.addWidget(fondo)

        lay = QVBoxLayout(fondo)
        lay.setContentsMargins(20, 20, 20, 20)
        lay.setSpacing(10)

        head = QHBoxLayout()
        icono = QLabel()
        icono.setPixmap(QPixmap("assets/error.png").scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        head.addWidget(icono)
        titulo = QLabel("Cerrar edición")
        titulo.setObjectName("TituloError")
        head.addWidget(titulo)
        head.addStretch()
        lay.addLayout(head)

        msg = QLabel("¿Está seguro de cerrar?\nPerderá los datos no guardados")
        msg.setObjectName("TextoError")
        msg.setWordWrap(True)
        msg.setMinimumWidth(320)
        lay.addWidget(msg)

        b_no = QPushButton("No")
        b_si = QPushButton("Si")
        for b in (b_no, b_si):
            b.setCursor(Qt.PointingHandCursor)
        b_si.setStyleSheet(
            "QPushButton { background-color: #792A24; color: white; border-radius: 10px; padding: 8px 25px; font-weight: bold; }"
            "QPushButton:hover { background-color: #C03930; }"
        )
        b_no.setStyleSheet(
            "QPushButton { background-color: #555; color: white; border-radius: 10px; padding: 8px 25px; font-weight: bold; }"
            "QPushButton:hover { background-color: #777; }"
        )
        b_si.clicked.connect(d.accept)
        b_no.clicked.connect(d.reject)

        actions = QHBoxLayout()
        actions.addStretch()
        actions.addWidget(b_no)
        actions.addWidget(b_si)
        lay.addLayout(actions)

        return d.exec_() == QDialog.Accepted

    def eventFilter(self, obj, event):
        if obj is getattr(self, "boton_info_pregunta", None):
            if event.type() == QEvent.Enter:
                self.popup_ayuda.setText(self._texto_pregunta or "Sin informacion adicional.")
                self.popup_ayuda.adjustSize()
                pos = self.boton_info_pregunta.mapTo(self, self.boton_info_pregunta.rect().bottomRight())
                self.popup_ayuda.move(pos.x(), pos.y())
                self.popup_ayuda.raise_()
                self.popup_ayuda.show()
            elif event.type() == QEvent.Leave:
                self.popup_ayuda.hide()
        return super().eventFilter(obj, event)

    def cerrar_ventana(self):
        if not self.hay_cambios() or self.mostrar_confirmacion_cerrar():
            self._cierre_confirmado = True
            self.reject()

    def closeEvent(self, event):
        if self.result() == QDialog.Accepted or self._cierre_confirmado or not self.hay_cambios():
            event.accept()
            return
        event.accept() if self.mostrar_confirmacion_cerrar() else event.ignore()
