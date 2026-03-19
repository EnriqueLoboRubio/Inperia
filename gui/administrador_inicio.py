from PyQt5.QtCore import QEasingCurve, QPropertyAnimation, QSize, Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtWidgets import (
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from gui.estilos import *
from gui.pantalla_datos_admin import PantallaDatosAdmin
from gui.pantalla_lista_solicitud import PantallaListaSolicitud
from gui.pantalla_lista_modificar_preguntas import PantallaListaModificarPreguntas
from gui.pantalla_lista_modificar_prompt import PantallaListaModificarPrompt
from gui.pantalla_lista_usuarios_administrador import PantallaListaUsuariosAdministrador
from gui.pantalla_perfil import PantallaPerfil
from gui.pantalla_perfil_interno_profesional import PantallaPerfilInternoProfesional
from gui.pantalla_detalle_solicitud_profesional import PantallaDetalleSolicitudProfesional
from gui.pantalla_resumen_profesional import PantallaResumen
from gui.ventana_acerca_inperia import VentanaAcercaInperia


class PantallaBienvenidaAdministrador(QWidget):
    abrir_usuarios = pyqtSignal()
    abrir_modelo = pyqtSignal()
    abrir_preguntas = pyqtSignal()
    abrir_datos = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._iniciar_ui()

    def _iniciar_ui(self):
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(40, 30, 40, 30)
        layout_principal.setSpacing(18)

        layout_principal.addStretch(1)

        self.lbl_titulo = QLabel("Bienvenido")
        self.lbl_titulo.setFont(QFont("Arial", 18))
        self.lbl_titulo.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(self.lbl_titulo)

        self.lbl_subtitulo = QLabel("Panel de administracion de INPERIA")
        self.lbl_subtitulo.setFont(QFont("Arial", 24, QFont.Bold))
        self.lbl_subtitulo.setAlignment(Qt.AlignCenter)
        self.lbl_subtitulo.setStyleSheet("color: #1F1F1F;")
        layout_principal.addWidget(self.lbl_subtitulo)

        self.lbl_descripcion = QLabel(
            "Desde este espacio podra gestionar usuarios, configuracion del sistema,\n"
            "el cuestionario y las operaciones de base de datos."
        )
        self.lbl_descripcion.setFont(QFont("Arial", 12))
        self.lbl_descripcion.setAlignment(Qt.AlignCenter)
        self.lbl_descripcion.setStyleSheet("color: #555555;")
        layout_principal.addWidget(self.lbl_descripcion)

        layout_principal.addStretch(1)

        fila_tarjetas = QHBoxLayout()
        fila_tarjetas.setSpacing(18)
        fila_tarjetas.addWidget(
            self._crear_tarjeta(
                "Usuarios",
                "Gestiona altas y edicion de internos, profesionales y administradores.",
                self.abrir_usuarios.emit,
            )
        )
        fila_tarjetas.addWidget(
            self._crear_tarjeta(
                "Editar modelo",
                "Configura prompts y parametros de analisis.",
                self.abrir_modelo.emit,
            )
        )
        fila_tarjetas.addWidget(
            self._crear_tarjeta(
                "Editar preguntas",
                "Revisa y adapta el cuestionario de entrevista.",
                self.abrir_preguntas.emit,
            )
        )
        fila_tarjetas.addWidget(
            self._crear_tarjeta(
                "Base de datos",
                "Prepara importaciones y exportaciones del sistema.",
                self.abrir_datos.emit,
            )
        )

        layout_principal.addLayout(fila_tarjetas)
        layout_principal.addStretch(2)

    def _crear_tarjeta(self, titulo, descripcion, accion):
        tarjeta = QPushButton()
        tarjeta.setCursor(Qt.PointingHandCursor)
        tarjeta.clicked.connect(accion)
        tarjeta.setStyleSheet(
            """
            QPushButton {
                background-color: #F7F7F7;
                border: 1px solid #D9D9D9;
                border-radius: 20px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #EFEFEF;
                border: 1px solid #CFCFCF;
            }
            QPushButton:pressed {
                background-color: #E7E7E7;
            }
            QLabel {
                background: transparent;
                border: none;
                color: #1F1F1F;
            }
            """
        )
        tarjeta.setMinimumHeight(180)

        layout = QVBoxLayout(tarjeta)
        layout.setContentsMargins(24, 22, 24, 22)
        layout.setSpacing(12)

        lbl_titulo = QLabel(titulo)
        lbl_titulo.setFont(QFont("Arial", 15, QFont.Bold))
        layout.addWidget(lbl_titulo)

        separador = QFrame()
        separador.setFixedHeight(1)
        separador.setStyleSheet("background-color: #D0D0D0; border: none;")
        layout.addWidget(separador)

        lbl_desc = QLabel(descripcion)
        lbl_desc.setWordWrap(True)
        lbl_desc.setFont(QFont("Arial", 11))
        lbl_desc.setStyleSheet("color: #5C5C5C;")
        layout.addWidget(lbl_desc)
        layout.addStretch(1)
        return tarjeta

    def set_usuario(self, usuario):
        nombre = getattr(usuario, "nombre", "") or "Administrador"
        self.lbl_titulo.setText(f"Bienvenido, {nombre}")


class VentanaAdministrador(QMainWindow):
    MENU_ANCHURA_CERRADO = 70
    MENU_ANCHURA_ABIERTO = 250
    COLOR_ABIERTO = "#2B2A2A"
    COLOR_CERRADO = "transparent"

    AJUSTES_ANCHURA_CERRADO = 0
    AJUSTES_ANCHURA_ABIERTO = 200
    AJUSTES_MENU_COLOR = "#3C3C3C"

    def __init__(self):
        super().__init__()
        self.setup_window()
        self.setWindowTitle("INPERIA - Administrador")
        self.menu_abierto = False
        self.ajustes_abierto = False
        self.init_ui()

    def setup_window(self):
        self.setWindowIcon(QIcon("assets/inperia.ico"))
        self.setMinimumSize(1200, 700)
        self.showMaximized()

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.menu_frame = QWidget()
        self.menu_frame.setFixedWidth(self.MENU_ANCHURA_CERRADO)
        self.menu_frame.setStyleSheet(f"background-color: {self.COLOR_CERRADO};")

        menu_layout = QVBoxLayout(self.menu_frame)
        menu_layout.setAlignment(Qt.AlignTop)
        menu_layout.setContentsMargins(5, 5, 5, 5)
        menu_layout.setSpacing(10)

        self.boton_hamburguesa = QPushButton("☰")
        self.boton_hamburguesa.setToolTip("Ver menu")
        self.boton_hamburguesa.setFixedSize(self.MENU_ANCHURA_CERRADO - 10, self.MENU_ANCHURA_CERRADO - 10)
        self.boton_hamburguesa.setFont(QFont("Arial", 20, QFont.Bold))
        self.boton_hamburguesa.setStyleSheet(
            """
            QPushButton {
                background-color: #444444;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover { background-color: #555555; }
            """
        )
        menu_layout.addWidget(self.boton_hamburguesa)
        menu_layout.addSpacing(10)

        self.boton_estilo = """
            QPushButton {
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.4);
                padding: 10px 15px;
                text-align: left;
                background-color: rgba(0, 0, 0, 0.2);
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: rgba(85, 85, 85, 0.5);
            }
        """

        self.boton_usuarios = QPushButton("Usuarios")
        self.boton_usuarios.setToolTip("Gestionar usuarios del sistema")
        self.boton_usuarios.setStyleSheet(self.boton_estilo)
        self.boton_usuarios.setFont(QFont("Arial", 10))
        self.boton_usuarios.hide()

        self.boton_modelo = QPushButton("Editar modelo")
        self.boton_modelo.setToolTip("Editar prompts y ajustes del modelo")
        self.boton_modelo.setStyleSheet(self.boton_estilo)
        self.boton_modelo.setFont(QFont("Arial", 10))
        self.boton_modelo.hide()

        self.boton_preguntas = QPushButton("Editar preguntas")
        self.boton_preguntas.setToolTip("Editar cuestionario")
        self.boton_preguntas.setStyleSheet(self.boton_estilo)
        self.boton_preguntas.setFont(QFont("Arial", 10))
        self.boton_preguntas.hide()

        self.boton_datos = QPushButton("Base de datos")
        self.boton_datos.setToolTip("Importar o exportar datos")
        self.boton_datos.setStyleSheet(self.boton_estilo)
        self.boton_datos.setFont(QFont("Arial", 10))
        self.boton_datos.hide()

        self.main_menu_widgets = [
            self.boton_usuarios,
            self.boton_modelo,
            self.boton_preguntas,
            self.boton_datos,
        ]

        for boton in self.main_menu_widgets:
            menu_layout.addWidget(boton)

        menu_layout.addStretch(1)

        self.pie_menu_widget = QWidget()
        self.pie_menu_layout = QHBoxLayout(self.pie_menu_widget)
        self.pie_menu_layout.setContentsMargins(0, 0, 0, 0)
        self.pie_menu_layout.setAlignment(Qt.AlignRight)
        self.pie_menu_widget.hide()

        self.boton_ajustes = QPushButton()
        self.boton_ajustes.setToolTip("Ver ajustes")
        self.boton_ajustes.setFixedSize(50, 50)
        self.boton_ajustes.setIcon(QIcon("assets/ajustes.png"))
        self.boton_ajustes.setIconSize(QSize(40, 40))
        self.boton_ajustes.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                border-radius: 25px;
            }
            QPushButton:hover { background-color: rgba(85, 85, 85, 0.3); }
            """
        )
        self.pie_menu_layout.addWidget(self.boton_ajustes)
        menu_layout.addWidget(self.pie_menu_widget)

        self.usuario_widget = QWidget()
        self.usuario_layout = QHBoxLayout(self.usuario_widget)
        self.usuario_layout.setContentsMargins(10, 0, 10, 0)

        self.boton_usuario = QPushButton()
        self.boton_usuario.setToolTip("Perfil de usuario")
        self.boton_usuario.setFixedSize(50, 50)
        self.boton_usuario.setIcon(QIcon("assets/admin.png"))
        self.boton_usuario.setIconSize(QSize(40, 40))
        self.boton_usuario.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 25px;
            }
            QPushButton:hover { background-color: rgba(85, 85, 85, 0.3); }
            """
        )

        self.titulo_pantalla = QLabel("Inicio")
        self.titulo_pantalla.setFont(QFont("Arial", 16, QFont.Bold))
        self.titulo_pantalla.setAlignment(Qt.AlignCenter)
        self.titulo_pantalla.setStyleSheet("color: #111111;")

        self.usuario_layout.addStretch(1)
        self.usuario_layout.addWidget(self.titulo_pantalla, alignment=Qt.AlignVCenter)
        self.usuario_layout.addStretch(1)
        self.usuario_layout.addWidget(self.boton_usuario)

        self.stacked_widget = QStackedWidget()
        self.pantalla_bienvenida = PantallaBienvenidaAdministrador()
        self.pantalla_lista_usuarios = PantallaListaUsuariosAdministrador()
        self.pantalla_lista_modificar_preguntas = PantallaListaModificarPreguntas()
        self.pantalla_lista_modificar_prompt = PantallaListaModificarPrompt()
        self.pantalla_datos = PantallaDatosAdmin()
        self.pantalla_lista_solicitudes_profesional = PantallaListaSolicitud()
        self.pantalla_perfil = PantallaPerfil()
        self.pantalla_perfil_interno = PantallaPerfilInternoProfesional()
        self.pantalla_detalle_solicitud = PantallaDetalleSolicitudProfesional()
        self.pantalla_resumen_profesional_lectura = PantallaResumen(solo_lectura=True)

        self.stacked_widget.addWidget(self.pantalla_bienvenida)
        self.stacked_widget.addWidget(self.pantalla_lista_usuarios)
        self.stacked_widget.addWidget(self.pantalla_lista_modificar_preguntas)
        self.stacked_widget.addWidget(self.pantalla_lista_modificar_prompt)
        self.stacked_widget.addWidget(self.pantalla_datos)
        self.stacked_widget.addWidget(self.pantalla_lista_solicitudes_profesional)
        self.stacked_widget.addWidget(self.pantalla_perfil)
        self.stacked_widget.addWidget(self.pantalla_perfil_interno)
        self.stacked_widget.addWidget(self.pantalla_detalle_solicitud)
        self.stacked_widget.addWidget(self.pantalla_resumen_profesional_lectura)
        self.stacked_widget.setCurrentWidget(self.pantalla_bienvenida)

        self._titulos_por_pantalla = {
            self.pantalla_bienvenida: "Inicio",
            self.pantalla_lista_usuarios: "Usuarios",
            self.pantalla_lista_modificar_preguntas: "Modificar preguntas",
            self.pantalla_lista_modificar_prompt: "Ajustes del modelo",
            self.pantalla_datos: "Datos",
            self.pantalla_lista_solicitudes_profesional: "Perfil profesional",
            self.pantalla_perfil: "Perfil",
            self.pantalla_perfil_interno: "Perfil interno",
            self.pantalla_detalle_solicitud: "Solicitud",
            self.pantalla_resumen_profesional_lectura: "Resumen de entrevista",
        }
        self.stacked_widget.currentChanged.connect(self._actualizar_titulo_pantalla)

        self.central_widget = QWidget()
        self.central_layout = QVBoxLayout(self.central_widget)
        self.central_layout.setContentsMargins(0, 0, 0, 0)
        self.central_layout.setSpacing(0)
        self.central_layout.addWidget(self.usuario_widget)
        self.central_layout.addWidget(self.stacked_widget, 1)

        self.ajustes_menu_frame = QWidget()
        self.ajustes_menu_frame.setFixedWidth(self.AJUSTES_ANCHURA_CERRADO)
        self.ajustes_menu_frame.setStyleSheet(
            f"""
            QWidget {{ background-color: {self.AJUSTES_MENU_COLOR}; border-left: 1px solid #1C1C1C; }}
            QAbstractButton {{ color: white; border: none; padding: 10px; text-align: left; }}
            QAbstractButton:hover {{ background-color: rgba(255, 255, 255, 0.2); }}
            """
        )

        self.ajustes_menu_layout = QVBoxLayout(self.ajustes_menu_frame)
        self.ajustes_menu_layout.setContentsMargins(10, 20, 10, 10)
        self.ajustes_menu_layout.setAlignment(Qt.AlignTop)

        self.boton_acerca = QPushButton("Acerca de Inperia")
        self.boton_acerca.setToolTip("Informacion de INPERIA")
        self.boton_acerca.setFont(QFont("Arial", 10))
        self.boton_acerca.setStyleSheet(self.boton_estilo)

        self.boton_perfil = QPushButton("Perfil")
        self.boton_perfil.setToolTip("Ver perfil")
        self.boton_perfil.setFont(QFont("Arial", 10))
        self.boton_perfil.setStyleSheet(self.boton_estilo)

        self.boton_cerrar_sesion = QPushButton("Cerrar Sesion")
        self.boton_cerrar_sesion.setToolTip("Cerrar sesion y volver al inicio")
        self.boton_cerrar_sesion.setFont(QFont("Arial", 10))
        self.boton_cerrar_sesion.setStyleSheet(
            """
            QPushButton {
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.4);
                padding: 10px 15px;
                text-align: left;
                background-color: #AC1F20;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #F3292B;
            }
            """
        )

        self.ajustes_menu_layout.addStretch(1)
        self.ajustes_menu_layout.addWidget(self.boton_acerca)
        self.ajustes_menu_layout.addWidget(self.boton_perfil)
        self.ajustes_menu_layout.addWidget(self.boton_cerrar_sesion)

        main_layout.addWidget(self.menu_frame)
        main_layout.addWidget(self.ajustes_menu_frame)
        main_layout.addWidget(self.central_widget, 1)

        self.boton_hamburguesa.clicked.connect(self.movimiento_menu)
        self.boton_ajustes.clicked.connect(self.movimiento_menu_ajustes)
        self.boton_acerca.clicked.connect(self.mostrar_acerca_inperia)

    def establecer_usuario(self, usuario):
        self.pantalla_bienvenida.set_usuario(usuario)

    def establecer_titulo_pantalla(self, titulo):
        self.titulo_pantalla.setText(str(titulo or ""))

    def mostrar_pantalla_perfil(self):
        self.stacked_widget.setCurrentWidget(self.pantalla_perfil)

    def mostrar_pantalla_perfil_interno(self):
        self.stacked_widget.setCurrentWidget(self.pantalla_perfil_interno)

    def mostrar_pantalla_detalle_solicitud(self):
        self.stacked_widget.setCurrentWidget(self.pantalla_detalle_solicitud)

    def mostrar_pantalla_resumen_entrevista(self):
        self.stacked_widget.setCurrentWidget(self.pantalla_resumen_profesional_lectura)

    def mostrar_acerca_inperia(self):
        VentanaAcercaInperia(self).exec_()

    def _actualizar_titulo_pantalla(self, _index=None):
        actual = self.stacked_widget.currentWidget()
        self.titulo_pantalla.setText(self._titulos_por_pantalla.get(actual, "INPERIA"))

    def movimiento_menu(self):
        if self.ajustes_abierto and self.ajustes_menu_frame.width() > self.AJUSTES_ANCHURA_CERRADO:
            self.movimiento_menu_ajustes()

        if self.menu_abierto:
            anchura_final = self.MENU_ANCHURA_CERRADO
            color_menu = self.COLOR_CERRADO
            for widget in self.main_menu_widgets:
                widget.hide()
            self.pie_menu_widget.hide()
        else:
            anchura_final = self.MENU_ANCHURA_ABIERTO
            color_menu = self.COLOR_ABIERTO
            for widget in self.main_menu_widgets:
                widget.show()
            self.pie_menu_widget.show()

        self.menu_abierto = not self.menu_abierto
        self.menu_frame.setStyleSheet(f"background-color: {color_menu};")

        self.animacion_min = QPropertyAnimation(self.menu_frame, b"minimumWidth")
        self.animacion_min.setDuration(300)
        self.animacion_min.setStartValue(self.menu_frame.width())
        self.animacion_min.setEndValue(anchura_final)
        self.animacion_min.setEasingCurve(QEasingCurve.InOutQuad)
        self.animacion_min.start()

        self.animacion_max = QPropertyAnimation(self.menu_frame, b"maximumWidth")
        self.animacion_max.setDuration(300)
        self.animacion_max.setStartValue(self.menu_frame.width())
        self.animacion_max.setEndValue(anchura_final)
        self.animacion_max.setEasingCurve(QEasingCurve.InOutQuad)
        self.animacion_max.start()

    def movimiento_menu_ajustes(self):
        if self.ajustes_abierto:
            anchura_final = self.AJUSTES_ANCHURA_CERRADO
            self.ajustes_abierto = False
        else:
            anchura_final = self.AJUSTES_ANCHURA_ABIERTO
            self.ajustes_abierto = True

        self.animacion_ajustes_min = QPropertyAnimation(self.ajustes_menu_frame, b"minimumWidth")
        self.animacion_ajustes_min.setDuration(300)
        self.animacion_ajustes_min.setStartValue(self.ajustes_menu_frame.width())
        self.animacion_ajustes_min.setEndValue(anchura_final)
        self.animacion_ajustes_min.setEasingCurve(QEasingCurve.InOutQuad)
        self.animacion_ajustes_min.start()

        self.animacion_ajustes_max = QPropertyAnimation(self.ajustes_menu_frame, b"maximumWidth")
        self.animacion_ajustes_max.setDuration(300)
        self.animacion_ajustes_max.setStartValue(self.ajustes_menu_frame.width())
        self.animacion_ajustes_max.setEndValue(anchura_final)
        self.animacion_ajustes_max.setEasingCurve(QEasingCurve.InOutQuad)
        self.animacion_ajustes_max.start()

    def mostrar_confirmacion_logout(self):
        dialogo = QDialog(self)
        dialogo.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        dialogo.setAttribute(Qt.WA_TranslucentBackground)
        dialogo.setModal(True)

        layout_main = QVBoxLayout(dialogo)
        layout_main.setContentsMargins(0, 0, 0, 0)

        fondo = QFrame()
        fondo.setObjectName("FondoDialogo")
        fondo.setStyleSheet(ESTILO_DIALOGO_ERROR)

        layout_interno = QVBoxLayout(fondo)
        layout_interno.setContentsMargins(20, 20, 20, 20)
        layout_interno.setSpacing(10)

        layout_cabecera = QHBoxLayout()

        lbl_icono = QLabel()
        pixmap = QPixmap("assets/error.png").scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        lbl_icono.setPixmap(pixmap)

        titulo = QLabel("Cerrar sesión")
        titulo.setObjectName("TituloError")

        layout_cabecera.addWidget(lbl_icono)
        layout_cabecera.addWidget(titulo)
        layout_cabecera.addStretch()

        lbl_mensaje = QLabel(
            "¿Está seguro de que quiere cerrar sesión?\n\n"
            "Perderá los datos no guardados."
        )
        lbl_mensaje.setObjectName("TextoError")
        lbl_mensaje.setWordWrap(True)
        lbl_mensaje.setMinimumWidth(320)

        btn_si = QPushButton("Si")
        btn_no = QPushButton("No")

        btn_si.setCursor(Qt.PointingHandCursor)
        btn_no.setCursor(Qt.PointingHandCursor)

        btn_si.setStyleSheet(
            """
            QPushButton {
                background-color: #792A24;
                color: white;
                border-radius: 10px;
                padding: 8px 25px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #C03930; }
            """
        )

        btn_no.setStyleSheet(
            """
            QPushButton {
                background-color: #555;
                color: white;
                border-radius: 10px;
                padding: 8px 25px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #777; }
            """
        )

        btn_si.clicked.connect(dialogo.accept)
        btn_no.clicked.connect(dialogo.reject)

        layout_botones = QHBoxLayout()
        layout_botones.addStretch()
        layout_botones.addWidget(btn_no)
        layout_botones.addWidget(btn_si)

        layout_interno.addLayout(layout_cabecera)
        layout_interno.addSpacing(10)
        layout_interno.addWidget(lbl_mensaje)
        layout_interno.addSpacing(20)
        layout_interno.addLayout(layout_botones)

        layout_main.addWidget(fondo)

        resultado = dialogo.exec_()
        return resultado == QDialog.Accepted
