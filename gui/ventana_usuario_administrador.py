from PyQt5.QtCore import QDate, Qt, QSize
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import (
    QComboBox,
    QDateEdit,
    QDialog,
    QFrame,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from gui.estilos import ESTILO_BOTON_SIG_ATR, ESTILO_COMBOBOX, ESTILO_INPUT, ESTILO_SCROLL, ESTILO_VENTANA_DETALLE


class VentanaUsuarioAdministrador(QDialog):
    def __init__(
        self,
        usuario=None,
        situacion_legal_opciones=None,
        relacion_contacto_opciones=None,
        permitir_eliminacion=True,
        parent=None,
    ):
        super().__init__(parent)
        self._usuario = dict(usuario or {})
        self._modo_edicion = bool(usuario)
        self._accion = "guardar"
        self._permitir_eliminacion = bool(permitir_eliminacion)
        self._situacion_legal_opciones = list(situacion_legal_opciones or [])
        self._relacion_contacto_opciones = list(relacion_contacto_opciones or [])
        self._filas_form = {}
        self._iniciar_ui()
        self._cargar_datos()

    def _iniciar_ui(self):
        self.setWindowTitle("Usuario")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setModal(True)
        self.setFixedSize(720, 760)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        self.frame_fondo = QFrame()
        self.frame_fondo.setObjectName("FondoDetalle")
        self.frame_fondo.setStyleSheet(ESTILO_VENTANA_DETALLE)
        root.addWidget(self.frame_fondo)

        layout = QVBoxLayout(self.frame_fondo)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(18)

        fila_titulo = QHBoxLayout()
        fila_titulo.setContentsMargins(0, 0, 0, 0)
        fila_titulo.setSpacing(12)

        titulo = QLabel("Editar usuario" if self._modo_edicion else "Crear usuario")
        titulo.setFont(QFont("Arial", 16, QFont.Bold))
        titulo.setStyleSheet("color: black; border: none;")
        fila_titulo.addWidget(titulo)
        fila_titulo.addStretch()

        if self._modo_edicion and self._permitir_eliminacion:
            self.boton_borrar = QPushButton("Eliminar")
            self.boton_borrar.setFont(QFont("Arial", 10, QFont.Bold))
            self.boton_borrar.setCursor(Qt.PointingHandCursor)
            self.boton_borrar.setFixedHeight(38)
            self.boton_borrar.setIcon(QIcon("assets/borrar.svg"))
            self.boton_borrar.setIconSize(QSize(16, 16))
            self.boton_borrar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            self.boton_borrar.setStyleSheet(
                """
                QPushButton {
                    color: white;
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    padding: 8px 14px;
                    text-align: center;
                    background-color: #AC1F20;
                    border-radius: 14px;
                    font-family: 'Arial';
                }
                QPushButton:hover {
                    background-color: #F3292B;
                }
                """
            )
            self.boton_borrar.clicked.connect(self._marcar_eliminacion)
            fila_titulo.addWidget(self.boton_borrar, alignment=Qt.AlignRight)

        layout.addLayout(fila_titulo)

        subtitulo = QLabel("Formulario de gestión de cuentas internas del sistema.")
        subtitulo.setFont(QFont("Arial", 10))
        subtitulo.setStyleSheet("color: #6A6A6A; border: none;")
        layout.addWidget(subtitulo)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet(
            ESTILO_SCROLL
            + """
            QScrollArea {
                background: transparent;
                border: none;
            }
            QWidget {
                background: transparent;
            }
            """
        )
        layout.addWidget(scroll, 1)

        contenido = QWidget()
        scroll.setWidget(contenido)

        contenido_layout = QVBoxLayout(contenido)
        contenido_layout.setContentsMargins(0, 0, 4, 0)
        contenido_layout.setSpacing(16)

        form = QFormLayout()
        form.setHorizontalSpacing(18)
        form.setVerticalSpacing(10)
        form.setLabelAlignment(Qt.AlignLeft)

        self.input_nombre = QLineEdit()
        self.input_nombre.setStyleSheet(self._estilo_input_compacto())
        self.input_nombre.setFont(QFont("Arial", 11))
        self._agregar_fila_form(form, "nombre", "Nombre", self.input_nombre)

        self.input_email = QLineEdit()
        self.input_email.setStyleSheet(self._estilo_input_compacto())
        self.input_email.setFont(QFont("Arial", 11))
        self._agregar_fila_form(form, "email", "Email", self.input_email)

        self.combo_rol = QComboBox()
        self.combo_rol.setStyleSheet(self._estilo_combobox_compacto())
        self.combo_rol.setFont(QFont("Arial", 11))
        self.combo_rol.addItem("Administrador", "administrador")
        self.combo_rol.addItem("Profesional", "profesional")
        self.combo_rol.addItem("Interno", "interno")
        self.combo_rol.currentIndexChanged.connect(self._actualizar_campos_rol)
        self._agregar_fila_form(form, "rol", "Rol", self.combo_rol)

        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)
        self.input_password.setStyleSheet(self._estilo_input_compacto())
        self.input_password.setFont(QFont("Arial", 11))
        self._agregar_fila_form(form, "password", "Nueva contraseña", self.input_password)

        self.input_password_2 = QLineEdit()
        self.input_password_2.setEchoMode(QLineEdit.Password)
        self.input_password_2.setStyleSheet(self._estilo_input_compacto())
        self.input_password_2.setFont(QFont("Arial", 11))
        self._agregar_fila_form(form, "password_confirm", "Confirmar nueva", self.input_password_2)

        self.input_num_colegiado = QLineEdit()
        self.input_num_colegiado.setStyleSheet(self._estilo_input_compacto())
        self.input_num_colegiado.setFont(QFont("Arial", 11))
        self._agregar_fila_form(form, "num_colegiado", "N. colegiado", self.input_num_colegiado)

        self.input_num_rc = QLineEdit()
        self.input_num_rc.setStyleSheet(self._estilo_input_compacto())
        self.input_num_rc.setFont(QFont("Arial", 11))
        self._agregar_fila_form(form, "num_rc", "N. recluso", self.input_num_rc)

        self.input_fecha_nac = self._crear_date_edit()
        self._agregar_fila_form(form, "fecha_nac", "Fecha nac.", self.input_fecha_nac)

        self.combo_situacion_legal = QComboBox()
        self.combo_situacion_legal.setStyleSheet(self._estilo_combobox_compacto())
        self.combo_situacion_legal.setFont(QFont("Arial", 11))
        self.combo_situacion_legal.addItem("Seleccionar...", "")
        for opcion in self._situacion_legal_opciones:
            self.combo_situacion_legal.addItem(opcion, opcion)
        self._agregar_fila_form(form, "situacion_legal", "Situación legal", self.combo_situacion_legal)

        self.input_delito = QLineEdit()
        self.input_delito.setStyleSheet(self._estilo_input_compacto())
        self.input_delito.setFont(QFont("Arial", 11))
        self._agregar_fila_form(form, "delito", "Delito", self.input_delito)

        self.input_condena = QLineEdit()
        self.input_condena.setStyleSheet(self._estilo_input_compacto())
        self.input_condena.setFont(QFont("Arial", 11))
        self._agregar_fila_form(form, "condena", "Duración condena", self.input_condena)

        self.input_fecha_ingreso = self._crear_date_edit()
        self._agregar_fila_form(form, "fecha_ingreso", "Fecha ingreso", self.input_fecha_ingreso)

        self.input_modulo = QLineEdit()
        self.input_modulo.setStyleSheet(self._estilo_input_compacto())
        self.input_modulo.setFont(QFont("Arial", 11))
        self._agregar_fila_form(form, "modulo", "Módulo", self.input_modulo)

        self.input_lugar_nacimiento = QLineEdit()
        self.input_lugar_nacimiento.setStyleSheet(self._estilo_input_compacto())
        self.input_lugar_nacimiento.setFont(QFont("Arial", 11))
        self._agregar_fila_form(form, "lugar_nacimiento", "Lugar nacimiento", self.input_lugar_nacimiento)

        self.input_nombre_contacto = QLineEdit()
        self.input_nombre_contacto.setStyleSheet(self._estilo_input_compacto())
        self.input_nombre_contacto.setFont(QFont("Arial", 11))
        self._agregar_fila_form(form, "nombre_contacto_emergencia", "Contacto emergencia", self.input_nombre_contacto)

        self.combo_relacion_contacto = QComboBox()
        self.combo_relacion_contacto.setStyleSheet(self._estilo_combobox_compacto())
        self.combo_relacion_contacto.setFont(QFont("Arial", 11))
        self.combo_relacion_contacto.addItems(self._relacion_contacto_opciones)
        self._agregar_fila_form(form, "relacion_contacto_emergencia", "Relación", self.combo_relacion_contacto)

        self.input_numero_contacto = QLineEdit()
        self.input_numero_contacto.setStyleSheet(self._estilo_input_compacto())
        self.input_numero_contacto.setFont(QFont("Arial", 11))
        self._agregar_fila_form(form, "numero_contacto_emergencia", "Teléfono contacto", self.input_numero_contacto)

        contenido_layout.addLayout(form)

        ayuda = QLabel(
            "El email y el rol permanecen bloqueados al editar. "
            "Los campos específicos solo se muestran cuando el tipo de usuario los necesita."
        )
        ayuda.setWordWrap(True)
        ayuda.setFont(QFont("Arial", 10))
        ayuda.setStyleSheet("color: #666666; border: none;")
        contenido_layout.addWidget(ayuda)
        contenido_layout.addStretch()

        botones = QHBoxLayout()
        botones.setContentsMargins(0, 0, 0, 0)

        boton_cancelar = QPushButton("Cancelar")
        boton_cancelar.setFont(QFont("Arial", 11))
        boton_cancelar.setCursor(Qt.PointingHandCursor)
        boton_cancelar.setFixedSize(120, 40)
        boton_cancelar.setStyleSheet(ESTILO_BOTON_SIG_ATR)
        boton_cancelar.clicked.connect(self.reject)
        botones.addWidget(boton_cancelar)

        botones.addStretch()

        estilo_guardar = ESTILO_BOTON_SIG_ATR.replace("black", "#792A24").replace("rgba(71, 70, 70, 0.7)", "#C03930")
        boton_guardar = QPushButton("Guardar")
        boton_guardar.setFont(QFont("Arial", 11))
        boton_guardar.setCursor(Qt.PointingHandCursor)
        boton_guardar.setFixedSize(120, 40)
        boton_guardar.setStyleSheet(estilo_guardar)
        boton_guardar.clicked.connect(self.accept)
        botones.addWidget(boton_guardar)

        layout.addLayout(botones)

    def _crear_label_form(self, texto):
        label = QLabel(texto)
        label.setFont(QFont("Arial", 11))
        label.setStyleSheet("color: #333333; font-family: 'Arial'; font-size: 11pt; border: none;")
        return label

    def _agregar_fila_form(self, form, clave, texto, widget):
        label = self._crear_label_form(texto)
        form.addRow(label, widget)
        self._filas_form[clave] = (label, widget)

    def _crear_date_edit(self):
        widget = QDateEdit()
        widget.setObjectName("dateEditAdmin")
        widget.setCalendarPopup(True)
        widget.setDisplayFormat("dd/MM/yyyy")
        widget.setDate(QDate.currentDate())
        widget.setStyleSheet(self._estilo_date_edit_compacto())
        widget.setFont(QFont("Arial", 11))
        return widget

    def _mostrar_fila(self, clave, visible):
        label, widget = self._filas_form[clave]
        label.setVisible(visible)
        widget.setVisible(visible)

    @staticmethod
    def _estilo_input_compacto():
        return ESTILO_INPUT + """
            QLineEdit, QTextEdit, QDateEdit, QTimeEdit, QComboBox {
                min-height: 18px;
                padding: 8px 12px;
                font-size: 11pt;
                border: 1px solid #D1D1D1;
            }
            QLineEdit:disabled {
                color: #7A7A7A;
                background-color: #F1F1F1;
            }
        """

    @staticmethod
    def _estilo_combobox_compacto():
        return ESTILO_COMBOBOX + """
            QComboBox {
                background-color: white;
                border: 1px solid #D1D1D1;
                border-radius: 8px;
                padding: 8px 12px;
                min-height: 18px;
                color: #333333;
            }
            QComboBox:disabled {
                color: #7A7A7A;
                background-color: #F1F1F1;
            }
        """

    @staticmethod
    def _estilo_date_edit_compacto():
        return ESTILO_INPUT + """
            QDateEdit#dateEditAdmin {
                background-image: none;
                background: white;
                min-height: 18px;
                font-size: 11pt;
                border: 1px solid #D1D1D1;
                padding-top: 8px;
                padding-bottom: 8px;
                padding-left: 12px;
                padding-right: 32px;
            }
            QDateEdit#dateEditAdmin::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: right center;
                width: 22px;
                border: none;
                background: transparent;
            }
            QDateEdit#dateEditAdmin::down-arrow {
                image: url(assets/flecha_abajo.png);
                width: 12px;
                height: 12px;
            }
            QDateEdit#dateEditAdmin::down-arrow:hover {
                background-color: #F0F0F0;
                border-radius: 4px;
            }
        """

    def _cargar_datos(self):
        if self._modo_edicion:
            self.input_nombre.setText(str(self._usuario.get("nombre", "") or ""))
            self.input_email.setText(str(self._usuario.get("email", "") or ""))
            self.input_email.setEnabled(False)
            rol = str(self._usuario.get("rol", "") or "").strip().lower()
            self.combo_rol.setCurrentIndex(max(0, self.combo_rol.findData(rol)))
            self.combo_rol.setEnabled(False)
            self.input_num_colegiado.setText(str(self._usuario.get("num_colegiado", "") or ""))
            self.input_num_rc.setText(str(self._usuario.get("num_rc", "") or ""))
            self._asignar_fecha(self.input_fecha_nac, self._usuario.get("fecha_nac"))
            self._asignar_fecha(self.input_fecha_ingreso, self._usuario.get("fecha_ingreso"))
            self._seleccionar_combo_por_valor(self.combo_situacion_legal, self._usuario.get("situacion_legal"))
            self.input_delito.setText(str(self._usuario.get("delito", "") or ""))
            self.input_condena.setText(str(self._usuario.get("condena", "") or ""))
            self.input_modulo.setText(str(self._usuario.get("modulo", "") or ""))
            self.input_lugar_nacimiento.setText(str(self._usuario.get("lugar_nacimiento", "") or ""))
            self.input_nombre_contacto.setText(str(self._usuario.get("nombre_contacto_emergencia", "") or ""))
            self._seleccionar_combo_por_texto(self.combo_relacion_contacto, self._usuario.get("relacion_contacto_emergencia"))
            self.input_numero_contacto.setText(str(self._usuario.get("numero_contacto_emergencia", "") or ""))

        self._actualizar_campos_rol()

    def _actualizar_campos_rol(self):
        rol = self.combo_rol.currentData()
        self._mostrar_fila("num_colegiado", rol == "profesional")
        campos_interno = [
            "num_rc",
            "fecha_nac",
            "situacion_legal",
            "delito",
            "condena",
            "fecha_ingreso",
            "modulo",
            "lugar_nacimiento",
            "nombre_contacto_emergencia",
            "relacion_contacto_emergencia",
            "numero_contacto_emergencia",
        ]
        for campo in campos_interno:
            self._mostrar_fila(campo, rol == "interno")

    def _marcar_eliminacion(self):
        self._accion = "eliminar"
        self.accept()

    def accion_solicitada(self):
        return self._accion

    @staticmethod
    def _asignar_fecha(widget, valor):
        texto = str(valor or "").strip()
        if not texto:
            return
        for formato in ("dd/MM/yyyy", "yyyy-MM-dd", "dd-MM-yyyy", "yyyy/MM/dd"):
            fecha = QDate.fromString(texto, formato)
            if fecha.isValid():
                widget.setDate(fecha)
                return

    @staticmethod
    def _seleccionar_combo_por_texto(combo, valor):
        texto = str(valor or "").strip()
        indice = combo.findText(texto, Qt.MatchFixedString)
        if indice >= 0:
            combo.setCurrentIndex(indice)

    @staticmethod
    def _seleccionar_combo_por_valor(combo, valor):
        texto = str(valor or "").strip()
        indice = combo.findData(texto)
        if indice >= 0:
            combo.setCurrentIndex(indice)

    def get_datos(self):
        return {
            "id_usuario": self._usuario.get("id_usuario"),
            "nombre": self.input_nombre.text().strip(),
            "email": self.input_email.text().strip(),
            "rol": self.combo_rol.currentData(),
            "password": self.input_password.text(),
            "password_confirm": self.input_password_2.text(),
            "num_colegiado": self.input_num_colegiado.text().strip(),
            "num_rc": self.input_num_rc.text().strip(),
            "fecha_nac": self.input_fecha_nac.date().toString("dd/MM/yyyy"),
            "situacion_legal": self.combo_situacion_legal.currentData(),
            "delito": self.input_delito.text().strip(),
            "condena": self.input_condena.text().strip(),
            "fecha_ingreso": self.input_fecha_ingreso.date().toString("dd/MM/yyyy"),
            "modulo": self.input_modulo.text().strip(),
            "lugar_nacimiento": self.input_lugar_nacimiento.text().strip(),
            "nombre_contacto_emergencia": self.input_nombre_contacto.text().strip(),
            "relacion_contacto_emergencia": self.combo_relacion_contacto.currentText().strip(),
            "numero_contacto_emergencia": self.input_numero_contacto.text().strip(),
        }
