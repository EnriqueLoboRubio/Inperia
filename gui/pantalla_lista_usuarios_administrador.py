from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from gui.estilos import *


class TarjetaUsuarioAdministrador(QFrame):
    editar_usuario = pyqtSignal(object)

    def __init__(self, usuario, parent=None):
        super().__init__(parent)
        self.usuario = usuario or {}
        self._iniciar_ui()

    def _iniciar_ui(self):
        self.setStyleSheet(
            """
            QFrame {
                background-color: #F5F5F5;
                border: 1px solid #C9C9C9;
                border-radius: 18px;
            }
            QLabel { border: none; color: black; background: transparent; }
            """
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 14, 20, 14)
        layout.setSpacing(12)

        cabecera = QHBoxLayout()
        cabecera.setSpacing(12)

        avatar = QPushButton(self._iniciales())
        avatar.setCursor(Qt.PointingHandCursor)
        avatar.setFixedSize(52, 52)
        avatar.setStyleSheet(ESTILO_BOTON_PERFIL)
        avatar.setToolTip("Editar usuario")
        avatar.clicked.connect(lambda: self.editar_usuario.emit(self.usuario))
        cabecera.addWidget(avatar, alignment=Qt.AlignTop)

        bloque_info = QVBoxLayout()
        bloque_info.setSpacing(4)

        fila_nombre = QHBoxLayout()
        fila_nombre.setSpacing(10)
        lbl_nombre = QLabel(str(self.usuario.get("nombre", "-")))
        lbl_nombre.setStyleSheet(ESTILO_NOMBRE_INTERNO)
        lbl_nombre.setFixedWidth(300)
        fila_nombre.addWidget(lbl_nombre)

        lbl_rol = QLabel(self._texto_rol(self.usuario.get("rol")))
        lbl_rol.setStyleSheet(
            f"""
            QLabel {{
                background-color: {self._color_rol(self.usuario.get("rol"))};
                color: black;
                border: none;
                border-radius: 10px;
                padding: 3px 10px;
                font-size: 10pt;
                font-weight: 500;
            }}
            """
        )
        fila_nombre.addWidget(lbl_rol, alignment=Qt.AlignVCenter | Qt.AlignLeft)
        fila_nombre.addStretch()
        bloque_info.addLayout(fila_nombre)

        lbl_email = QLabel(str(self.usuario.get("email", "-")))
        lbl_email.setStyleSheet(ESTILO_NUM_RC)
        bloque_info.addWidget(lbl_email)
        cabecera.addLayout(bloque_info, 1)

        boton_editar = QPushButton("Editar")
        boton_editar.setCursor(Qt.PointingHandCursor)
        boton_editar.setFixedHeight(38)
        boton_editar.setStyleSheet(ESTILO_BOTON_SOLICITUD)
        boton_editar.clicked.connect(lambda: self.editar_usuario.emit(self.usuario))
        cabecera.addWidget(boton_editar)

        layout.addLayout(cabecera)

        fila_detalles = QHBoxLayout()
        fila_detalles.setSpacing(40)
        fila_detalles.addLayout(self._crear_bloque_texto("ID usuario", str(self.usuario.get("id_usuario", "-"))))
        fila_detalles.addLayout(self._crear_bloque_texto("Identificador", self._identificador_principal()))
        fila_detalles.addLayout(self._crear_bloque_texto("Dato auxiliar", self._dato_auxiliar()))
        fila_detalles.addStretch()
        layout.addLayout(fila_detalles)

    def _crear_bloque_texto(self, titulo, valor):
        cont = QVBoxLayout()
        cont.setSpacing(2)
        lbl_titulo = QLabel(titulo)
        lbl_titulo.setStyleSheet(ESTILO_TITULO_DETALLE_PERFIL)
        lbl_valor = QLabel(valor)
        lbl_valor.setStyleSheet(ESTILO_DATO_PERFIL)
        cont.addWidget(lbl_titulo)
        cont.addWidget(lbl_valor)
        return cont

    def _iniciales(self):
        nombre = str(self.usuario.get("nombre", "") or "").strip()
        partes = [p for p in nombre.split() if p]
        if not partes:
            return "--"
        if len(partes) == 1:
            return partes[0][:2].upper()
        return (partes[0][0] + partes[1][0]).upper()

    @staticmethod
    def _texto_rol(rol):
        return {
            "administrador": "Administrador",
            "profesional": "Profesional",
            "interno": "Interno",
        }.get(str(rol or "").strip().lower(), "Usuario")

    @staticmethod
    def _color_rol(rol):
        rol_norm = str(rol or "").strip().lower()
        if rol_norm == "administrador":
            return "#D8C7FF"
        if rol_norm == "profesional":
            return "#CBE7D4"
        if rol_norm == "interno":
            return "#F7DEB0"
        return "#D8D8D8"

    def _identificador_principal(self):
        rol = str(self.usuario.get("rol", "")).strip().lower()
        if rol == "profesional":
            return f"COL-{self.usuario.get('num_colegiado', '-')}"
        if rol == "interno":
            return f"RC-{self.usuario.get('num_rc', '-')}"
        return "ADM"

    def _dato_auxiliar(self):
        rol = str(self.usuario.get("rol", "")).strip().lower()
        if rol == "interno":
            return str(self.usuario.get("fecha_nac", "-") or "-")
        if rol == "profesional":
            return "Acceso profesional"
        return "Control del sistema"


class PantallaListaUsuariosAdministrador(QWidget):
    crear_usuario = pyqtSignal()
    editar_usuario = pyqtSignal(object)
    filtros_cambiados = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._usuarios_filtrados = []
        self._tam_lote = 12
        self._num_visibles = 0
        self._iniciar_ui()

    def _iniciar_ui(self):
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(35, 20, 60, 15)
        layout_principal.setSpacing(14)

        fila_superior = QHBoxLayout()
        fila_superior.setSpacing(8)

        self.input_busqueda = QLineEdit()
        self.input_busqueda.setPlaceholderText("Buscar por nombre, email o identificador ...")
        self.input_busqueda.setFixedHeight(40)
        self.input_busqueda.setStyleSheet(
            """
            QLineEdit {
                background-color: #ECECEC;
                border: 1px solid #BEBEBE;
                border-radius: 20px;
                padding: 0 16px;
                font-size: 11pt;
            }
            """
        )
        tam_icono = self.input_busqueda.fontMetrics().height() + 3
        icono_busqueda_svg = QIcon("assets/buscar.svg")
        icono_busqueda = QIcon(icono_busqueda_svg.pixmap(tam_icono, tam_icono))
        self.input_busqueda.addAction(icono_busqueda, QLineEdit.LeadingPosition)
        self.input_busqueda.textChanged.connect(self.filtros_cambiados.emit)
        fila_superior.addWidget(self.input_busqueda, 1)

        self.combo_rol = QComboBox()
        self.combo_rol.setFixedSize(190, 40)
        self.combo_rol.setStyleSheet(ESTILO_COMBOBOX)
        self.combo_rol.addItem("Todos", "todos")
        self.combo_rol.addItem("Internos", "interno")
        self.combo_rol.addItem("Profesionales", "profesional")
        self.combo_rol.addItem("Administradores", "administrador")
        self.combo_rol.currentIndexChanged.connect(self.filtros_cambiados.emit)
        fila_superior.addWidget(self.combo_rol)

        self.boton_crear = QPushButton("Crear usuario")
        self.boton_crear.setFixedSize(180, 40)
        self.boton_crear.setCursor(Qt.PointingHandCursor)
        self.boton_crear.setStyleSheet(ESTILO_BOTON_NEGRO)
        self.boton_crear.clicked.connect(self.crear_usuario.emit)
        fila_superior.addWidget(self.boton_crear)

        layout_principal.addLayout(fila_superior)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setStyleSheet(ESTILO_SCROLL)

        self.contenedor = QWidget()
        self.layout_lista = QVBoxLayout(self.contenedor)
        self.layout_lista.setContentsMargins(0, 0, 0, 0)
        self.layout_lista.setSpacing(10)
        self.layout_lista.setAlignment(Qt.AlignTop)

        self.scroll.setWidget(self.contenedor)
        self.scroll.verticalScrollBar().valueChanged.connect(self._al_scroll_lista)
        layout_principal.addWidget(self.scroll, 1)

    def obtener_filtros(self):
        return {
            "texto": self.input_busqueda.text().strip(),
            "rol": self.combo_rol.currentData(),
        }

    def cargar_datos(self, usuarios):
        self._usuarios_filtrados = list(usuarios or [])
        self._num_visibles = min(self._tam_lote, len(self._usuarios_filtrados))
        self._render_lista()

    def _al_scroll_lista(self, valor):
        barra = self.scroll.verticalScrollBar()
        if valor < (barra.maximum() - 80):
            return
        self._cargar_siguiente_lote()

    def _cargar_siguiente_lote(self):
        if self._num_visibles >= len(self._usuarios_filtrados):
            return
        self._num_visibles = min(self._num_visibles + self._tam_lote, len(self._usuarios_filtrados))
        self._render_lista()

    def _limpiar_lista(self):
        while self.layout_lista.count():
            item = self.layout_lista.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def _render_lista(self):
        self._limpiar_lista()

        if not self._usuarios_filtrados:
            lbl_vacio = QLabel("No hay usuarios para los filtros actuales.")
            lbl_vacio.setAlignment(Qt.AlignCenter)
            lbl_vacio.setStyleSheet("font-size: 12pt; color: #7A7A7A;")
            self.layout_lista.addWidget(lbl_vacio)
            self.layout_lista.addStretch()
            return

        for usuario in self._usuarios_filtrados[: self._num_visibles]:
            tarjeta = TarjetaUsuarioAdministrador(usuario)
            tarjeta.editar_usuario.connect(self.editar_usuario.emit)
            self.layout_lista.addWidget(tarjeta)

        if self._num_visibles < len(self._usuarios_filtrados):
            lbl_mas = QLabel(
                f"Mostrando {self._num_visibles} de {len(self._usuarios_filtrados)} usuarios. Desplaza para cargar más."
            )
            lbl_mas.setAlignment(Qt.AlignCenter)
            lbl_mas.setStyleSheet("font-size: 10pt; color: #7A7A7A;")
            self.layout_lista.addWidget(lbl_mas)

        self.layout_lista.addStretch()
