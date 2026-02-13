import sys
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QLineEdit, QTextEdit, QCheckBox, QDateEdit, QTimeEdit, 
    QComboBox, QStackedWidget, QFrame, QScrollArea, QButtonGroup,
    QSizePolicy, QGridLayout, QDialog
)
from PyQt5.QtCore import Qt, QDate, QTime, pyqtSignal
from PyQt5.QtGui import QPixmap

from gui.estilos import *

class IndicadorPaso(QWidget):
    """
    Widget para mostrar el indicador de pasos en parte superior
    """
    def __init__(self, parent=None):
        
        super().__init__(parent)

        self.paso_actual = 1
        self.iniciar_ui()

    def iniciar_ui(self):    
        layout = QHBoxLayout(self)
        layout.setContentsMargins(40, 10, 40, 20)
        layout.setSpacing(0)

        self.pasos = []
        for i in range(4):                    

            circulo = QLabel(str(i + 1))
            circulo.setFixedSize(60,60)
            circulo.setAlignment(Qt.AlignCenter)
            if(i == 0):
                circulo.setStyleSheet(ESTILO_CIRCULO_ACTUAL)
            else:
                circulo.setStyleSheet(ESTILO_CIRCULO_INACTIVO)

            layout.addWidget(circulo)
            self.pasos.append(circulo)

            if i < 3:
                linea = QFrame()
                linea.setFrameShape(QFrame.HLine)
                linea.setStyleSheet("background-color: black")
                linea.setFixedHeight(4)                
                linea.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                
                layout.addWidget(linea)
            

    def actualizar_paso(self, paso):
        """
        Actualiza el estilo visual según el paso actual
        """
        self.paso_actual = paso
        for i, circulo in enumerate(self.pasos):
            if i+1 == paso:
                # Paso actual (negro)
                circulo.setStyleSheet(ESTILO_CIRCULO_ACTUAL)            
            elif i+1 < paso:
                # Paso completado (verde)
                circulo.setStyleSheet(ESTILO_CIRCULO_COMPLETADO)
            else:
                # Paso inactivo (gris)
                circulo.setStyleSheet(ESTILO_CIRCULO_INACTIVO)

class PermisoTarjeta(QWidget):
    """
    Tarjeta seleccionable para tipo de permiso
    """
    clicked = pyqtSignal(object)

    def __init__(self, icono, titulo, subtitulo, parent=None):
        super().__init__(parent)
        self.titulo = titulo
        self.seleccionado = False
        self.iniciar_ui(icono, titulo, subtitulo)

    def iniciar_ui(self, icono, titulo, subtitulo):
        
        layout = QVBoxLayout(self)

        # Icono
        icono_label = QLabel(self)
        icono_label.setPixmap(QPixmap(icono))
        icono_label.setFixedSize(60,60)
        icono_label.setAlignment(Qt.AlignCenter)
        icono_label.setAttribute(Qt.WA_TransparentForMouseEvents)

        # Título
        titulo_label = QLabel(titulo)
        titulo_label.setStyleSheet(ESTILO_TITULO_PERMISO)
        titulo_label.setAttribute(Qt.WA_TransparentForMouseEvents)

        layout_titulo = QHBoxLayout()
        layout_titulo.addWidget(icono_label)
        layout_titulo.addWidget(titulo_label)
        layout_titulo.addStretch() 

        # Subtitulo
        subtitulo_label = QLabel(subtitulo)
        subtitulo_label.setStyleSheet(ESTILO_SUBTITULO_PERMISO)
        subtitulo_label.setWordWrap(True)
        subtitulo_label.setAttribute(Qt.WA_TransparentForMouseEvents)

        layout.addLayout(layout_titulo)
        layout.addWidget(subtitulo_label)

        self.actualizar_estilo()

        self.setStyleSheet(ESTILO_TARJETA_PERMISO_NO)

        self.setFixedHeight(120)
        self.setCursor(Qt.PointingHandCursor)

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setMouseTracking(True)

    def mousePressEvent(self, event):        
        self.clicked.emit(self) 
        super().mousePressEvent(event)

    def set_seleccionado(self, estado):
        """ Método público para cambiar el estado desde fuera """
        self.seleccionado = estado
        self.actualizar_estilo()

    def actualizar_estilo(self):
        if self.seleccionado:
            self.setStyleSheet(ESTILO_TARJETA_PERMISO_SEL)
        else:
            self.setStyleSheet(ESTILO_TARJETA_PERMISO_NO)


class Paso1Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.inicio_ui()

    def inicio_ui(self):
        principal_layout = QVBoxLayout(self)
        principal_layout.setSpacing(20)

        # ---------- TÍTULO ----------
        titulo_paso = QLabel("Información básica")
        titulo_paso.setStyleSheet(ESTILO_TITULO_PASO)

        subtitulo_paso = QLabel(
            "Selecciona el tipo de permiso y especifique el motivo"
        )
        subtitulo_paso.setStyleSheet(ESTILO_SUBTITULO_PASO)

        principal_layout.addWidget(titulo_paso)
        principal_layout.addWidget(subtitulo_paso)

        # ---------- GRID PRINCIPAL ----------
        grid = QGridLayout()
        grid.setHorizontalSpacing(30)
        grid.setVerticalSpacing(12)

        # ================== COLUMNA IZQUIERDA ==================

        # Tipo de permiso
        tipo_label = QLabel("Tipo de permiso *")
        tipo_label.setStyleSheet(ESTILO_TITULO_APARTADO)
        grid.addWidget(tipo_label, 0, 0)

        # Tarjetas (2 columnas internas)
        tarjetas_layout = QHBoxLayout()
        tarjetas_layout.setSpacing(15)

        col1 = QVBoxLayout()
        col1.setSpacing(15)
        col2 = QVBoxLayout()
        col2.setSpacing(15)

        self.tarjeta_familiar = PermisoTarjeta(
            "assets/familia.png",
            "Salida familiar",
            "Visitada a familiares directos por motivos justificados"
        )
        self.tarjeta_educativo = PermisoTarjeta(
            "assets/educacion.png",
            "Permiso educativo",
            "Asistencia a actividades educativas o exámenes"
        )
        self.tarjeta_defuncion = PermisoTarjeta(
            "assets/cruz.png",
            "Permiso por defunción",
            "Asistencia a funeral de familiar directo"
        )

        self.tarjeta_medico = PermisoTarjeta(
            "assets/corazon.png",
            "Permiso médico",
            "Atención médica especializada o acompañamiento"
        )
        self.tarjeta_laboral = PermisoTarjeta(
            "assets/negocio.png",
            "Permiso laboral",
            "Actividades laborales o entrevistas de trabajo"
        )
        self.tarjeta_juridico = PermisoTarjeta(
            "assets/justicia.png",
            "Permiso jurídico",
            "Asistencia a citas legales o judiciales"
        )

        col1.addWidget(self.tarjeta_familiar)
        col1.addWidget(self.tarjeta_educativo)
        col1.addWidget(self.tarjeta_defuncion)

        col2.addWidget(self.tarjeta_medico)
        col2.addWidget(self.tarjeta_laboral)
        col2.addWidget(self.tarjeta_juridico)

        tarjetas_layout.addLayout(col1)
        tarjetas_layout.addLayout(col2)

        grid.addLayout(tarjetas_layout, 1, 0)

        # Motivo específico
        motivo_label = QLabel("Motivo específico *")
        motivo_label.setStyleSheet(ESTILO_TITULO_APARTADO)

        self.motivo_texto = QLineEdit()
        self.motivo_texto.setPlaceholderText("Ingrese el motivo específico...")
        self.motivo_texto.setStyleSheet(ESTILO_INPUT)

        grid.addWidget(motivo_label, 2, 0)
        grid.addWidget(self.motivo_texto, 3, 0)

        # ================== COLUMNA DERECHA ==================

        # Descripción detallada
        desc_label = QLabel("Descripción detallada del motivo *")
        desc_label.setStyleSheet(ESTILO_TITULO_APARTADO)

        self.desc_texto = QTextEdit()
        self.desc_texto.setPlaceholderText(
            "Describa el motivo de su solicitud..."
        )
        self.desc_texto.setFixedHeight(400)
        self.desc_texto.setStyleSheet(ESTILO_INPUT)

        grid.addWidget(desc_label, 0, 1)
        grid.addWidget(self.desc_texto, 1, 1)

        # Nivel de urgencia
        urgencia_label = QLabel("Nivel de urgencia *")
        urgencia_label.setStyleSheet(ESTILO_TITULO_APARTADO)

        urgencia_layout = QHBoxLayout()
        urgencia_layout.setSpacing(15)
        urgencia_layout.setContentsMargins(0, 0, 0, 0)

        self.urgencia_botones = QButtonGroup(self)
        self.urgencia_botones.setExclusive(True)

        self.boton_normal = QCheckBox("Normal")        
        self.boton_importante = QCheckBox("Importante")
        self.boton_urgente = QCheckBox("Urgente")

        for boton in [
            self.boton_normal,
            self.boton_importante,
            self.boton_urgente
        ]:
            boton.setStyleSheet(ESTILO_CHECKBOX)
            boton.setCursor(Qt.PointingHandCursor)
            self.urgencia_botones.addButton(boton)
            urgencia_layout.addWidget(boton)

        grid.addWidget(urgencia_label, 2, 1)
        grid.addLayout(urgencia_layout, 3, 1)

        # ---------- PROPORCIONES ----------
        grid.setColumnStretch(0, 3)
        grid.setColumnStretch(1, 3)

        principal_layout.addLayout(grid)

        # ---------- LÓGICA DE SELECCIÓN ----------
        self.lista_tarjetas = [
            self.tarjeta_familiar,
            self.tarjeta_educativo,
            self.tarjeta_defuncion,
            self.tarjeta_medico,
            self.tarjeta_laboral,
            self.tarjeta_juridico,
        ]

        for tarjeta in self.lista_tarjetas:
            tarjeta.clicked.connect(self.gestionar_seleccion)

    def gestionar_seleccion(self, tarjeta_seleccionada):
        for tarjeta in self.lista_tarjetas:
            tarjeta.set_seleccionado(tarjeta is tarjeta_seleccionada)


class Paso2Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.iniciar_ui()
    
    def iniciar_ui(self):
        principal_layout = QVBoxLayout(self)
        principal_layout.setSpacing(20)
        
        principal_titulo_layout = QVBoxLayout()
        
        titulo_paso = QLabel("Fecha y Destino")
        titulo_paso.setStyleSheet(ESTILO_TITULO_PASO)

        subtitulo_paso = QLabel("Especifique las fechas, horarios y lugar del permiso")
        subtitulo_paso.setStyleSheet(ESTILO_SUBTITULO_PASO)

        principal_titulo_layout.addWidget(titulo_paso)
        principal_titulo_layout.addWidget(subtitulo_paso)
        principal_layout.addLayout(principal_titulo_layout)

        # --- FECHAS ---
        fechas_layout = QHBoxLayout() 
        fechas_layout.setSpacing(20) 

        inicio_layout = QVBoxLayout()
        inicio_label = QLabel("Fecha de Inicio *")
        inicio_label.setStyleSheet(ESTILO_TITULO_APARTADO)
        self.fecha_inicio = QDateEdit()
        self.fecha_inicio.setCalendarPopup(True)
        self.fecha_inicio.setDate(QDate.currentDate())
        self.fecha_inicio.setStyleSheet(ESTILO_INPUT)

        inicio_layout.addWidget(inicio_label)
        inicio_layout.addWidget(self.fecha_inicio)

        fin_layout = QVBoxLayout()
        fin_label = QLabel("Fecha de Fin *")
        fin_label.setStyleSheet(ESTILO_TITULO_APARTADO)
        self.fecha_fin = QDateEdit()
        self.fecha_fin.setCalendarPopup(True)
        self.fecha_fin.setDate(QDate.currentDate())
        self.fecha_fin.setStyleSheet(ESTILO_INPUT)
        fin_layout.addWidget(fin_label)
        fin_layout.addWidget(self.fecha_fin)

        fechas_layout.addLayout(inicio_layout, 1)
        fechas_layout.addLayout(fin_layout, 1)

        principal_layout.addLayout(fechas_layout)

        # --- HORARIOS ---
        horarios_layout = QHBoxLayout()
        horarios_layout.setSpacing(20)

        salida_layout = QVBoxLayout()
        salida_label = QLabel("Hora de Salida *")
        salida_label.setStyleSheet(ESTILO_TITULO_APARTADO)
        self.hora_salida = QTimeEdit()
        self.hora_salida.setTime(QTime.currentTime())
        self.hora_salida.setStyleSheet(ESTILO_INPUT)
        salida_layout.addWidget(salida_label)
        salida_layout.addWidget(self.hora_salida)

        llegada_layout = QVBoxLayout() 
        llegada_label = QLabel("Hora de Llegada *")
        llegada_label.setStyleSheet(ESTILO_TITULO_APARTADO)
        self.hora_llegada = QTimeEdit()
        self.hora_llegada.setTime(QTime.currentTime())
        self.hora_llegada.setStyleSheet(ESTILO_INPUT)
        llegada_layout.addWidget(llegada_label)
        llegada_layout.addWidget(self.hora_llegada)

        horarios_layout.addLayout(salida_layout)
        horarios_layout.addLayout(llegada_layout)
        principal_layout.addLayout(horarios_layout) 

        # --- DESTINO ---
        destino_layout = QHBoxLayout() # Sin self
        destino_layout.setSpacing(20)

        destino_principal_layout = QVBoxLayout() # Sin self
        destino_label = QLabel("Destino Principal *")
        destino_label.setStyleSheet(ESTILO_TITULO_APARTADO)
        self.destino_texto = QLineEdit()
        self.destino_texto.setPlaceholderText("Ingrese el destino principal...")
        self.destino_texto.setStyleSheet(ESTILO_INPUT)
        destino_principal_layout.addWidget(destino_label)
        destino_principal_layout.addWidget(self.destino_texto)

        ciudad_layout = QVBoxLayout() # Sin self
        ciudad_label = QLabel("Ciudad *")
        ciudad_label.setStyleSheet(ESTILO_TITULO_APARTADO)
        self.ciudad_texto = QLineEdit()
        self.ciudad_texto.setPlaceholderText("Ciudad...")
        self.ciudad_texto.setStyleSheet(ESTILO_INPUT)
        ciudad_layout.addWidget(ciudad_label)
        ciudad_layout.addWidget(self.ciudad_texto)

        destino_layout.addLayout(destino_principal_layout, 2)
        destino_layout.addLayout(ciudad_layout, 1)

        principal_layout.addLayout(destino_layout)

        # --- Direccion y código postal ---
        direccion_layout = QHBoxLayout() # Sin self
        direccion_layout.setSpacing(20)

        direccion_completa_layout = QVBoxLayout() # Sin self
        direccion_label = QLabel("Dirección Completa *")
        direccion_label.setStyleSheet(ESTILO_TITULO_APARTADO)
        self.direccion_texto = QLineEdit()
        self.direccion_texto.setPlaceholderText("Calle, número, referencias...")
        self.direccion_texto.setStyleSheet(ESTILO_INPUT)
        direccion_completa_layout.addWidget(direccion_label)
        direccion_completa_layout.addWidget(self.direccion_texto)

        codigo_layout = QVBoxLayout() # Sin self
        codigo_label = QLabel("Código postal")
        codigo_label.setStyleSheet(ESTILO_TITULO_APARTADO)
        self.codigo_texto  = QLineEdit()
        self.codigo_texto.setPlaceholderText("C.P.")
        self.codigo_texto.setStyleSheet(ESTILO_INPUT)
        codigo_layout.addWidget(codigo_label)
        codigo_layout.addWidget(self.codigo_texto)
        
        direccion_layout.addLayout(direccion_completa_layout, 2)
        direccion_layout.addLayout(codigo_layout, 1)

        principal_layout.addLayout(direccion_layout)
        principal_layout.addStretch()    


class Paso3Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.inicio_ui()

    def inicio_ui(self):
        principal_layout = QVBoxLayout(self)    
        principal_layout.setSpacing(20)

        # CORRECCIÓN: Sin self
        principal_titulo_layout = QVBoxLayout()
        
        titulo_paso = QLabel("Contactos e información adicional")
        titulo_paso.setStyleSheet(ESTILO_TITULO_PASO)

        subtitulo_paso = QLabel("Proporcione información de contacto y detalles adicionales")
        subtitulo_paso.setStyleSheet(ESTILO_SUBTITULO_PASO)

        principal_titulo_layout.addWidget(titulo_paso)
        principal_titulo_layout.addWidget(subtitulo_paso)

        principal_layout.addLayout(principal_titulo_layout)

        cont_prin_label = QLabel("Contacto Principal")
        cont_prin_label.setStyleSheet(ESTILO_TITULO_APARTADO)
        principal_layout.addWidget(cont_prin_label)

        # --- FILA 1 ---
        fila1_layout = QHBoxLayout() # Sin self
        fila1_layout.setSpacing(15)

        nombre_prin_layout = QVBoxLayout() # Sin self
        nombre_prin_label = QLabel("Nombre Completo *")        
        nombre_prin_label.setStyleSheet(ESTILO_TITULO_APARTADO)
        self.nombre_prin_texto = QLineEdit()
        self.nombre_prin_texto.setPlaceholderText("Nombre y apellidos...")
        self.nombre_prin_texto.setStyleSheet(ESTILO_INPUT)
        nombre_prin_layout.addWidget(nombre_prin_label)
        nombre_prin_layout.addWidget(self.nombre_prin_texto)

        telefono_prin_layout = QVBoxLayout() # Sin self
        telefono_prin_label = QLabel("Teléfono *")
        telefono_prin_label.setStyleSheet(ESTILO_TITULO_APARTADO)
        self.telefono_prin_texto = QLineEdit()
        self.telefono_prin_texto.setPlaceholderText("Número de teléfono...")
        self.telefono_prin_texto.setStyleSheet(ESTILO_INPUT)
        telefono_prin_layout.addWidget(telefono_prin_label)
        telefono_prin_layout.addWidget(self.telefono_prin_texto)

        relacion_prin_layout = QVBoxLayout() # Sin self
        relacion_prin_label = QLabel("Relación *")
        relacion_prin_label.setStyleSheet(ESTILO_TITULO_APARTADO)
        self.relacion_prin_combo = QComboBox()
        self.relacion_prin_combo.addItems(["Seleccionar...", "Padre/Madre", "Hermano/a", 
                                       "Esposo/a", "Hijo/a", "Otro"])
        self.relacion_prin_combo.setStyleSheet(ESTILO_INPUT)
        relacion_prin_layout.addWidget(relacion_prin_label)
        relacion_prin_layout.addWidget(self.relacion_prin_combo)

        fila1_layout.addLayout(nombre_prin_layout, 2)
        fila1_layout.addLayout(telefono_prin_layout, 1)
        fila1_layout.addLayout(relacion_prin_layout, 1)

        principal_layout.addLayout(fila1_layout)

        # Dirección completa
        direccion_prin_layout = QVBoxLayout() # Sin self
        direccion_prin_label = QLabel("Dirección Completa *")
        direccion_prin_label.setStyleSheet(ESTILO_TITULO_APARTADO)
        self.direccion_prin_texto = QLineEdit()
        self.direccion_prin_texto.setPlaceholderText("Dirección completa del contacto...")
        self.direccion_prin_texto.setStyleSheet(ESTILO_INPUT)
        direccion_prin_layout.addWidget(direccion_prin_label)
        direccion_prin_layout.addWidget(self.direccion_prin_texto)
        # Falta añadirlo al layout principal
        principal_layout.addLayout(direccion_prin_layout)

        # Contacto Secundario
        cont_secun_label = QLabel("Contacto Secundario")
        cont_secun_label.setStyleSheet(ESTILO_TITULO_APARTADO)    

        principal_layout.addWidget(cont_secun_label)

        # -- FILA 2 ---
        fila2_layout = QHBoxLayout() 
        fila2_layout.setSpacing(15)

        nombre_secun_layout = QVBoxLayout()
        nombre_secun_label = QLabel("Nombre Completo")
        nombre_secun_label.setStyleSheet(ESTILO_TITULO_APARTADO)
        self.nombre_secun_texto = QLineEdit()
        self.nombre_secun_texto.setPlaceholderText("Nombre y apellidos...")
        self.nombre_secun_texto.setStyleSheet(ESTILO_INPUT)
        nombre_secun_layout.addWidget(nombre_secun_label)
        nombre_secun_layout.addWidget(self.nombre_secun_texto)

        telefono_secun_layout = QVBoxLayout() 
        telefono_secun_label = QLabel("Teléfono")
        telefono_secun_label.setStyleSheet(ESTILO_TITULO_APARTADO)
        self.telefono_secun_texto = QLineEdit()
        self.telefono_secun_texto.setPlaceholderText("Número de teléfono...")
        self.telefono_secun_texto.setStyleSheet(ESTILO_INPUT)
        telefono_secun_layout.addWidget(telefono_secun_label)
        telefono_secun_layout.addWidget(self.telefono_secun_texto)
        
        relacion_secun_layout = QVBoxLayout()
        relacion_secun_label = QLabel("Relación")
        relacion_secun_label.setStyleSheet(ESTILO_TITULO_APARTADO)
        self.relacion_secun_combo = QComboBox()
        self.relacion_secun_combo.addItems(["Seleccionar...", "Padre/Madre", "Hermano/a", 
                                       "Esposo/a", "Hijo/a", "Otro"])
        self.relacion_secun_combo.setStyleSheet(ESTILO_INPUT)
        relacion_secun_layout.addWidget(relacion_secun_label)
        relacion_secun_layout.addWidget(self.relacion_secun_combo)

        fila2_layout.addLayout(nombre_secun_layout, 2)
        fila2_layout.addLayout(telefono_secun_layout, 1)
        fila2_layout.addLayout(relacion_secun_layout, 1)

        principal_layout.addLayout(fila2_layout)

        principal_layout.addStretch()
    
class Paso4Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.iniciar_ui()
    
    def iniciar_ui(self):
        principal_layout = QHBoxLayout(self)
        principal_layout.setSpacing(20)

        # --- Columna izquierda ---
        columna_izq = QVBoxLayout()
        columna_izq.setSpacing(15)

        estilo_frame_interno = """
                            #frame_interno {
                                background-color: #FAFAFA;
                                border: 2px solid #E0E0E0;
                                border-radius: 8px;
                            }
                            /* Forzamos a que los Labels dentro sean transparentes y sin borde */
                            QLabel {
                                background-color: transparent;
                                border: none;
                            }
                            /* Aseguramos que los CheckBox sean transparentes */
                            QCheckBox {
                                background-color: transparent;
                            }
                        """                

        # Documentos requeridos
        docs_frame = QFrame()
        docs_frame.setObjectName("frame_interno")
        docs_frame.setStyleSheet(estilo_frame_interno)
        
        docs_layout = QVBoxLayout(docs_frame)

        docs_titulo = QLabel("Documentos Requeridos")
        docs_titulo.setStyleSheet(ESTILO_TITULO_PASO)
        docs_layout.addWidget(docs_titulo)

        docs_subtitulo = QLabel("Seleccione los documentos que adjuntará con su solicitud")
        docs_subtitulo.setStyleSheet(ESTILO_SUBTITULO_PASO)
        docs_layout.addWidget(docs_subtitulo)

        self.doc_identidad = QCheckBox("Documento de identidad del familiar")
        self.doc_relacion = QCheckBox("Comprobante de relación familiar")
        self.doc_invitacion = QCheckBox("Carta de invitación")

        for checkbox in [self.doc_identidad, self.doc_relacion, self.doc_invitacion]:
            checkbox.setStyleSheet(ESTILO_CHECKBOX)
            checkbox.setCursor(Qt.PointingHandCursor)
            docs_layout.addWidget(checkbox)

        docs_layout.addStretch()
        columna_izq.addWidget(docs_frame)    

        # Compromisos
        compromisos_frame = QFrame()
        compromisos_frame.setObjectName("frame_interno")
        compromisos_layout = QVBoxLayout(compromisos_frame)
        compromisos_frame.setStyleSheet(estilo_frame_interno)
        
        
        compromisos_titulo = QLabel("Compromisos")
        compromisos_titulo.setStyleSheet(ESTILO_TITULO_PASO)
        compromisos_layout.addWidget(compromisos_titulo)

        compromisos_subtitulo = QLabel("Seleccione los compromisos que acepta cumplir")
        compromisos_subtitulo.setStyleSheet(ESTILO_SUBTITULO_PASO)
        compromisos_layout.addWidget(compromisos_subtitulo)

        self.comp1 = QCheckBox("Cumplir estrictamente con los horarios establecidos")
        self.comp2 = QCheckBox("Mantener contacto permanente con la institución")
        self.comp3 = QCheckBox("No consumir alcohol ni sustancias prohibidas")
        self.comp4 = QCheckBox("Presentar comprobantes de las actividades realizadas")
        self.comp5 = QCheckBox("Informar cualquier cambio en la programación")
        self.comp6 = QCheckBox("No alejarse del lugar autorizado sin permiso")

        for checkbox in [self.comp1, self.comp2, self.comp3, 
                         self.comp4, self.comp5, self.comp6]:
            checkbox.setStyleSheet(ESTILO_CHECKBOX)
            checkbox.setCursor(Qt.PointingHandCursor)
            compromisos_layout.addWidget(checkbox)
        
        columna_izq.addWidget(compromisos_frame)

        # --- Columna derecha ---
        columna_der = QVBoxLayout() 

        observaciones_frame = QFrame()
        observaciones_frame.setObjectName("frame_interno")
        observaciones_frame.setStyleSheet(estilo_frame_interno)
        observaciones_layout = QVBoxLayout(observaciones_frame)
        

        observaciones_titulo = QLabel("Observaciones Adicionales")
        observaciones_titulo.setStyleSheet(ESTILO_TITULO_PASO)
        observaciones_layout.addWidget(observaciones_titulo)

        observaciones_subtitulos = QLabel("Comparta información adicional relevante")
        observaciones_subtitulos.setStyleSheet(ESTILO_SUBTITULO_PASO)
        observaciones_layout.addWidget(observaciones_subtitulos)

        self.observaciones_texto = QTextEdit()
        self.observaciones_texto.setPlaceholderText("Comentario adicional...")
        self.observaciones_texto.setMinimumHeight(400)
        self.observaciones_texto.setStyleSheet(ESTILO_INPUT)
        observaciones_layout.addWidget(self.observaciones_texto)

        columna_der.addWidget(observaciones_frame)

        # Añadir columnas al layout principal
        principal_layout.addLayout(columna_izq, 1)
        principal_layout.addLayout(columna_der, 1)


class PantallaSolicitudInterno(QWidget):
    """
    Vista principal de la pantalla solicitud
    """
    def __init__(self, parent=None):
        super().__init__(parent)            
        self.iniciar_ui()

    def iniciar_ui(self):
        principal_layout = QVBoxLayout(self)
        principal_layout.setContentsMargins(20, 20, 20, 20)
        principal_layout.setSpacing(0)

        # --- ENCABEZADO --- 
        encabezado_frame = QFrame()
        encabezado_frame.setObjectName("encabezado")
        encabezado_frame.setStyleSheet("""
            #encabezado {
                border: 2px solid #E0E0E0;   
                border-radius: 15px;         
                background-color: #f0f0f0;     
            }
        """)

        encabezado_layout = QVBoxLayout(encabezado_frame)
        encabezado_layout.setContentsMargins(20, 20, 5, 20)
        encabezado_layout.setSpacing(5)       


        # Titulo
        titulo = QLabel("Nueva Solicitud Permiso")
        titulo.setStyleSheet(ESTILO_TITULO_PASO_ENCA)

        self.descripcion_paso = QLabel("Paso 1 de 4 - Complete toda la información requerida")
        self.descripcion_paso.setStyleSheet(ESTILO_DES_PASO_ENCA)

        self.subtitulo_paso = QLabel("Información básica del permiso")
        self.subtitulo_paso.setStyleSheet(ESTILO_SUBTITULO_PASO_ENCA)

        # Indicador pasos
        self.indicador_pasos = IndicadorPaso()

        encabezado_layout.addWidget(titulo)
        encabezado_layout.addWidget(self.descripcion_paso)
        encabezado_layout.addWidget(self.indicador_pasos)
        encabezado_layout.addWidget(self.subtitulo_paso)
    
        principal_layout.addWidget(encabezado_frame)    

        principal_layout.addSpacing(20)

        # Frame para el contenido con borde
        self.contenido_frame = QFrame()
        self.contenido_frame.setObjectName("apartado")
        self.contenido_frame.setStyleSheet(ESTILO_APARTADO_FRAME)

        frame_layout = QVBoxLayout(self.contenido_frame)
        frame_layout.setContentsMargins(0, 5, 0, 5)

        # --- SCROLL AREA ---
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame) 
        scroll.setStyleSheet("background-color: transparent;")    
        scroll.setStyleSheet(ESTILO_SCROLL)

        scroll_widget = QWidget()
        scroll_widget.setStyleSheet("background-color: transparent;")   

        scroll_layout = QVBoxLayout(scroll_widget)        

        # Stacked para pasos
        self.stacked_widget = QStackedWidget()

        self.paso1 = Paso1Widget()
        self.paso2 = Paso2Widget()
        self.paso3 = Paso3Widget()
        self.paso4 = Paso4Widget()

        self.stacked_widget.addWidget(self.paso1)
        self.stacked_widget.addWidget(self.paso2)
        self.stacked_widget.addWidget(self.paso3)
        self.stacked_widget.addWidget(self.paso4)

        scroll_layout.addWidget(self.stacked_widget) 
        scroll.setWidget(scroll_widget)              
        frame_layout.addWidget(scroll)
        
        principal_layout.addWidget(self.contenido_frame, 1)

        # --- BOTONES NAVEGACION ---
        botones_layout = QHBoxLayout()
        botones_layout.setContentsMargins(0, 20, 0, 0)

        self.boton_anterior = QPushButton("Anterior")
        self.boton_anterior.setFixedSize(120, 45)       
        self.boton_anterior.setVisible(False)
        self.boton_anterior.setStyleSheet(ESTILO_BOTON_SIG_ATR)

        self.boton_siguiente = QPushButton("Siguiente")
        self.boton_siguiente.setFixedSize(120, 45)
        self.boton_siguiente.setStyleSheet(ESTILO_BOTON_SIG_ATR)

        botones_layout.addWidget(self.boton_anterior)
        botones_layout.addStretch()
        botones_layout.addWidget(self.boton_siguiente)

        principal_layout.addLayout(botones_layout)

        self.setStyleSheet("QWidget { background-color: #f0f0f0; }")

    def ir_siguiente(self):
        actual = self.stacked_widget.currentIndex()
        if actual < 3:
            self.actualizar_ui(actual + 2)

    def ir_anterior(self):
        actual = self.stacked_widget.currentIndex()
        if actual > 0:
            self.actualizar_ui(actual)

    def actualizar_ui(self, paso):
        """
        Actualiza la intefaz cambia el paso
        """
        self.stacked_widget.setCurrentIndex(paso - 1)
        self.indicador_pasos.actualizar_paso(paso)

        # Actualizar botones      
        self.boton_anterior.setVisible(paso > 1)
        if paso == 4:
            self.boton_siguiente.setText("Enviar")
        else:
            self.boton_siguiente.setText("Siguiente")

        # Actualizar descripción
        descripciones = [
            "Paso 1 de 4 - Complete toda la información requerida",
            "Paso 2 de 4 - Complete toda la información requerida",
            "Paso 3 de 4 - Complete toda la información requerida",
            "Paso 4 de 4 - Revise y mande la solicitud"
        ]

        subtitulos = [
            "Información básica del permiso",
            "Detalles del destino y fechas",
            "Contactos e información adicional",
            "Revisión y confirmación"
        ]

        self.descripcion_paso.setText(descripciones[paso-1])
        self.subtitulo_paso.setText(subtitulos[paso-1])


    def mostrar_validacion_error(self, mensaje):
        """
        Crea un diálogo personalizado para tener control total del espaciado
        """
        dialogo = QDialog(self)
        dialogo.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog) 
        dialogo.setAttribute(Qt.WA_TranslucentBackground)
        
        # Layout principal del diálogo
        layout_main = QVBoxLayout(dialogo)
        layout_main.setContentsMargins(0, 0, 0, 0)
        
        # --- MARCO DE FONDO ---
        fondo = QFrame()
        fondo.setObjectName("FondoDialogo") 
        fondo.setStyleSheet(ESTILO_DIALOGO_ERROR)
            
        layout_interno = QVBoxLayout(fondo)
        layout_interno.setContentsMargins(20, 20, 20, 20)
        layout_interno.setSpacing(5)
        
        # --- ICONO Y TÍTULO  ---
        layout_cabecera = QHBoxLayout()
        layout_cabecera.setSpacing(10)
        
        lbl_icono = QLabel()
        pixmap = QPixmap("assets/error.png").scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)     
        lbl_icono.setPixmap(pixmap) 
        lbl_icono.setFixedSize(30, 30)
        lbl_icono.setStyleSheet("background: transparent; border: none;")


        titulo = QLabel("Atención")
        titulo.setObjectName("TituloError")
        
        layout_cabecera.addWidget(lbl_icono)
        layout_cabecera.addWidget(titulo)
        layout_cabecera.addStretch()
        
        # --- TEXTO DEL MENSAJE ---
        lbl_mensaje = QLabel(mensaje)
        lbl_mensaje.setObjectName("TextoError")
        lbl_mensaje.setWordWrap(True)
        lbl_mensaje.setMinimumWidth(300) 
        
        # --- BOTÓN ---
        boton = QPushButton("Entendido")
        boton.setCursor(Qt.PointingHandCursor)
        boton.setStyleSheet("""
            QPushButton { 
                background-color: black; 
                color: white; 
                border-radius: 10px; 
                padding: 8px 20px;
                font-family: 'Arial';
                font-weight: bold;
                font-size: 9pt;
            }
            QPushButton:hover { background-color: #333; }
        """)
        boton.clicked.connect(dialogo.accept)
     
        layout_boton = QHBoxLayout()
        layout_boton.addStretch()
        layout_boton.addWidget(boton)
                
        layout_interno.addLayout(layout_cabecera)
        layout_interno.addSpacing(5)
        layout_interno.addWidget(lbl_mensaje)
        layout_interno.addSpacing(15)
        layout_interno.addLayout(layout_boton)
        
        layout_main.addWidget(fondo)
        
        dialogo.exec_()      