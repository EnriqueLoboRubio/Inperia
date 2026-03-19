from PyQt5.QtWidgets import (
    QComboBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from gui.estilos import ESTILO_BOTON_SIG_ATR, ESTILO_COMBOBOX, ESTILO_INPUT, ESTILO_VENTANA_DETALLE


class VentanaUsuarioAdministrador(QDialog):
    def __init__(self, usuario=None, parent=None):
        super().__init__(parent)
        self._usuario = dict(usuario or {})
        self._modo_edicion = bool(usuario)
        self._iniciar_ui()
        self._cargar_datos()

    def _iniciar_ui(self):
        self.setWindowTitle("Usuario")
        self.setModal(True)
        self.setMinimumWidth(560)
        self.setStyleSheet(ESTILO_VENTANA_DETALLE)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 22, 22, 22)
        layout.setSpacing(16)

        titulo = QLabel("Editar usuario" if self._modo_edicion else "Crear usuario")
        layout.addWidget(titulo)

        form = QFormLayout()
        form.setHorizontalSpacing(18)
        form.setVerticalSpacing(12)

        self.input_nombre = QLineEdit()
        self.input_nombre.setStyleSheet(ESTILO_INPUT)
        form.addRow("Nombre", self.input_nombre)

        self.input_email = QLineEdit()
        self.input_email.setStyleSheet(ESTILO_INPUT)
        form.addRow("Email", self.input_email)

        self.combo_rol = QComboBox()
        self.combo_rol.setStyleSheet(ESTILO_COMBOBOX)
        self.combo_rol.addItem("Administrador", "administrador")
        self.combo_rol.addItem("Profesional", "profesional")
        self.combo_rol.addItem("Interno", "interno")
        self.combo_rol.currentIndexChanged.connect(self._actualizar_campos_rol)
        form.addRow("Rol", self.combo_rol)

        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)
        self.input_password.setStyleSheet(ESTILO_INPUT)
        form.addRow("Contraseña", self.input_password)

        self.input_password_2 = QLineEdit()
        self.input_password_2.setEchoMode(QLineEdit.Password)
        self.input_password_2.setStyleSheet(ESTILO_INPUT)
        form.addRow("Confirmar", self.input_password_2)

        self.input_num_colegiado = QLineEdit()
        self.input_num_colegiado.setStyleSheet(ESTILO_INPUT)
        form.addRow("Nº colegiado", self.input_num_colegiado)

        self.input_num_rc = QLineEdit()
        self.input_num_rc.setStyleSheet(ESTILO_INPUT)
        form.addRow("Nº recluso", self.input_num_rc)

        self.input_fecha_nac = QLineEdit()
        self.input_fecha_nac.setPlaceholderText("dd/mm/yyyy")
        self.input_fecha_nac.setStyleSheet(ESTILO_INPUT)
        form.addRow("Fecha nac.", self.input_fecha_nac)

        layout.addLayout(form)

        ayuda = QLabel(
            "En edición, deja la contraseña vacía si no quieres cambiarla. "
            "El rol no se puede modificar una vez creado el usuario."
        )
        ayuda.setWordWrap(True)
        layout.addWidget(ayuda)

        botones = QHBoxLayout()
        botones.addStretch()

        boton_cancelar = QPushButton("Cancelar")
        boton_cancelar.setStyleSheet(ESTILO_BOTON_SIG_ATR)
        boton_cancelar.clicked.connect(self.reject)
        botones.addWidget(boton_cancelar)

        boton_guardar = QPushButton("Guardar")
        boton_guardar.setStyleSheet(ESTILO_BOTON_SIG_ATR)
        boton_guardar.clicked.connect(self.accept)
        botones.addWidget(boton_guardar)

        layout.addLayout(botones)

    def _cargar_datos(self):
        if self._modo_edicion:
            self.input_nombre.setText(str(self._usuario.get("nombre", "") or ""))
            self.input_email.setText(str(self._usuario.get("email", "") or ""))
            rol = str(self._usuario.get("rol", "") or "").strip().lower()
            self.combo_rol.setCurrentIndex(max(0, self.combo_rol.findData(rol)))
            self.combo_rol.setEnabled(False)
            self.input_num_colegiado.setText(str(self._usuario.get("num_colegiado", "") or ""))
            self.input_num_rc.setText(str(self._usuario.get("num_rc", "") or ""))
            self.input_fecha_nac.setText(str(self._usuario.get("fecha_nac", "") or ""))

        self._actualizar_campos_rol()

    def _actualizar_campos_rol(self):
        rol = self.combo_rol.currentData()
        self.input_num_colegiado.setVisible(rol == "profesional")
        self.input_num_rc.setVisible(rol == "interno")
        self.input_fecha_nac.setVisible(rol == "interno")

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
            "fecha_nac": self.input_fecha_nac.text().strip(),
        }
