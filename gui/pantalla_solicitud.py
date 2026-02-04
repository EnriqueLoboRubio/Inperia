from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QLineEdit, QTextEdit, QCheckBox, QDateEdit, QTimeEdit, 
    QComboBox, QStackedWidget, QFrame, QScrollArea, QButtonGroup, QMessageBox, 
)
from PyQt5.QtCore import Qt, QDate, QTime
from PyQt5.QtGui import QFont, QPixmap

class IndicadorPaso(QWidget):
    """
    Widget para mostrar el indicador de pasos en parte superior
    """
    def __init__(self, parent=None):
        super.__init__(parent)

        self.paso_actual = 1
        self.iniciar_ui()

    def iniciar_ui(self):    

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 10, 0, 20)

        self.pasos = []
        for i in range(4):

            contenedor_paso = QHBoxLayout()

            circulo = QLabel(str(i + 1))
            circulo.setFixedSize(30,30)
            circulo.setAlignment(Qt.AlignCenter)
            circulo.setStyleSheet("""
                QLabel {
                    background-color: #E0E0E0;
                    color: #666;
                    border-radius: 15px;
                    font-weight: bold;
                }
            """)

            contenedor_paso.addWidget(circulo)

            if i<3:
                linea = QFrame()
                linea.setFrameShape(QFrame.HLine)
                linea.setStyleSheet("background-color: #E0E0E0")
                linea.setFixedHeight(2)
                linea.setFixedWidth(40)

                contenedor_paso.addWidget(linea)
            
            self.pasos.append(circulo)
            for j in range(contenedor_paso.count()):
                layout.addWidget(contenedor_paso.itemAt(j).widget())

        layout.addStretch()

    def actualizar_paso(self, paso):
        """
        Actualiza el estilo visual según el paso actual
        """
        self.paso_actual = paso
        for i, circulo in enumerate(self.pasos):
            if i+1 == paso:
                # Paso actual (negro)
                circulo.setStyleSheet("background-color: #000; color: #FFF; border-radius: 15px; font-weight: bold;")
            elif i+1 < paso:
                # Paso completado (verde)
                circulo.setStyleSheet("background-color: #4CAF50; color: #FFF; border-radius: 15px; font-weight: bold;")
            else:
                # Paso inactivo (gris)
                circulo.setStyleSheet("background-color: #E0E0E0; color: #666; border-radius: 15px; font-weight: bold;")

class PermisoTarjeta(QWidget):
    """
    Tarjeta seleccionable para tipo de permiso
    """
    def __init__(self, icono, titulo, subtitulo, parent=None):
        super().__init__(parent)
        self.titulo = titulo
        self.seleccionado = False
        self.iniciar_ui(icono, titulo, subtitulo)

    def iniciar_ui(self, icono, titulo, subtitulo):
        
        layout = QVBoxLayout(self)

        #Icono
        icono_label = QLabel(self)
        icono_label.setPixmap(QPixmap(icono))
        icono_label.setFixedSize(20,20)
        icono_label.setAlignment(Qt.AlignCenter)

        #Título
        titulo_label = QLabel(titulo)
        titulo_label.setStyleSheet("font-weight: bold; font-size: 14px;")

        layout_titulo = QHBoxLayout(self)

        layout_titulo.addWidget(icono_label)
        layout_titulo.addWidget(titulo_label)

        #Subtitulo
        subtitulo_label = QLabel(subtitulo)
        subtitulo_label.setStyleSheet("color: #666; font-size: 11px;")
        subtitulo_label.setWordWrap(True)

        layout.addWidget(layout_titulo)
        layout.addWidget(subtitulo_label)

        self.setStyleSheet("""
            PermisoTarjeta {
                background-color: white;
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 15px;
            }
            PermisoTarjeta:hover {
                border-color: #999;
            }
        """)

        self.setFixedHeight(120)
        #self.setFixedSize(120, x)
        self.setCursor(Qt.PointingHandCursor)

    def EventoClick(self, evento):
        self.seleccionado = not self.seleccionado
        if self.seleccionado:
            self.setStyleSheet("""
                PermisoTarjeta {
                    background-color: #E3F2FD;
                    border: 2px solid #2196F3;
                    border-radius: 8px;
                    padding: 15px;
                }
            """)
        else:
            self.setStyleSheet("""
                PermisoTarjeta {
                    background-color: white;
                    border: 2px solid #E0E0E0;
                    border-radius: 8px;
                    padding: 15px;
                }
            """)

class Paso1Widget(QWidget):
    """
    Paso 1: Información básica del permiso
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.inicio_ui()

    def inicio_ui(self):
        principal_layout = QVBoxLayout(self)    
        principal_layout.setSpacing(20)  

        # Titulo y Subtitulo
        principal_titulo_layout = QVBoxLayout(self)

        # Layout para columnas
        principal_contenido_layout = QHBoxLayout(self)

        # Columna para tipos de permiso y motivo      
        principal_col1_layout = QVBoxLayout(self) 
        #Columna para detalles y urgencia
        principal_col2_layout = QVBoxLayout(self)

        #Titulo y subtitulo del paso
        titulo_paso = QLabel("Información básica")
        titulo_paso.setStyleSheet("font-size: 18px; font-weight: bold;")

        subtitulo_paso = QLabel("Selecciona el tipo de permiso y especifique el motivo")
        subtitulo_paso.setStyleSheet("color: #999; font-size: 13px;")

        principal_titulo_layout.addWidget(titulo_paso)
        principal_titulo_layout.addWidget(subtitulo_paso)

        principal_layout.addLayout(principal_titulo_layout)

        # --- COLUMNA 1 --- 
        #Tipo de permiso
        tipo_label = QLabel("Tipo de permiso *")
        tipo_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        principal_col1_layout.addWidget(tipo_label)

        #Grid de tarjetas de permiso
        tarjetas_layout = QHBoxLayout()
        tarjetas_layout.setSpacing(15)

        #Columna 1
        col1 = QVBoxLayout()
        col1.setSpacing(15)
        self.tarjeta_familiar = PermisoTarjeta("assets/familia.png", "Salida familiar",
                                               "Visitada a familiares directos por motivos justificados")
        self.tarjeta_educativo = PermisoTarjeta("assets/educacion.png", "Permiso educativo",
                                               "Asistencia a actividades educativas o exámenes")
        self.tarjeta_defuncion = PermisoTarjeta("assets/cruz.png", "Permiso por defunción",
                                               "Asistencia a funeral de familiar directo")
        col1.addWidget(self.tarjeta_familiar)
        col1.addWidget(self.tarjeta_educativo)
        col1.addWidget(self.tarjeta_defuncion)

        #Columna 2
        col2 = QVBoxLayout()
        col2.setSpacing(15)
        self.tarjeta_medico = PermisoTarjeta("assets/corazon.png", "Permiso médico",
                                               "Atención médica especialiszada o acompañamiento")
        self.tarjeta_laboral = PermisoTarjeta("assets/negocio.png", "Permiso laboral",
                                               "Actividades laborales o entrevistas de trabajo")
        self.tarjeta_juridico = PermisoTarjeta("assets/justicia.png", "Permiso jurídico",
                                               "Asistencia a citas legales o judiciales")
        col2.addWidget(self.tarjeta_medico)
        col2.addWidget(self.tarjeta_laboral)
        col2.addWidget(self.tarjeta_juridico)        

        tarjetas_layout.addLayout(col1)
        tarjetas_layout.addLayout(col2)
        tarjetas_layout.addStretch()

        principal_col1_layout.addLayout(tarjetas_layout)

        #Motivo específico
        motivo_label = QLabel("Motivo específico *")
        motivo_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        principal_col1_layout.addWidget(motivo_label)
        
        self.motivo_texto = QLineEdit()
        self.motivo_texto.setPlaceholderText("Ingrese el motivo específico...")
        self.motivo_texto.setStyleSheet("""
            QLineEdit {
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 10px;
                font-size: 13px;
                min-height: 20px;
            }
            QLineEdit:focus {
                border-color: #2196F3;
            }
        """)

        principal_col1_layout.addWidget(self.motivo_texto)
        principal_contenido_layout.addLayout(principal_col1_layout)

        # --- COLUMNA 2 ---
        #Descripcion del motivo
        desc_label = QLabel("Descripción detallada del motivo *")
        desc_label.setStyleSheet("font-weight: bold; margin-top: 10px;")

        principal_col2_layout.addWidget(desc_label)

        self.desc_texto = QTextEdit()
        self.desc_texto.setPlaceholderText("Describa el motivo de su solicitud...")
        self.desc_texto.setFixedHeight(100)
        self.desc_texto.setStyleSheet("""
            QTextEdit {
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 10px;
                font-size: 13px;
            }
            QTextEdit:focus {
                border-color: #2196F3;
            }
        """)

        principal_col2_layout.addWidget(self.desc_texto)

        #Nivel urgencia
        urgencia_label = QLabel("Nivel de urgencia *")
        urgencia_label.setStyleSheet("font-weight: bold; margin-top: 10px;")

        principal_col2_layout.addWidget(urgencia_label)

        urgencia_layout = QHBoxLayout()
        self.urgencia_botones = QButtonGroup(self)               

        self.boton_normal = QCheckBox("Normal")
        self.boton_importante = QCheckBox("Importante")
        self.boton_urgente = QCheckBox("Urgente")
        
        for boton in [self.boton_normal, self.boton_importante, self.boton_urgente]:
            boton.setStyleSheet("""
                QCheckBox {
                    spacing: 8px;
                    font-size: 13px;
                }
                QCheckBox::indicator {
                    width: 20px;
                    height: 20px;
                }
            """)

        urgencia_layout.addWidget(self.boton_normal)
        urgencia_layout.addWidget(self.boton_importante)
        urgencia_layout.addWidget(self.boton_urgente)

        principal_col2_layout.addLayout(urgencia_layout)
        principal_contenido_layout.addLayout(principal_col2_layout)
        principal_layout.addLayout(principal_contenido_layout)


class Paso2Widget(QWidget):
    """
    Paso 2: Detalles del destino y fechas
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.iniciar_ui()
    
    def iniciar_ui(self):
        principal_layout = QVBoxLayout(self)
        principal_layout.setSpacing(20)

        # Titulo y Subtitulo
        principal_titulo_layout = QVBoxLayout(self)
        
        titulo_paso = QLabel("Fecha y Destino")
        titulo_paso.setStyleSheet("font-size: 18px; font-weight: bold;")

        subtitulo_paso = QLabel("Especifique las fechas, horarios y lugar del permiso")
        subtitulo_paso.setStyleSheet("color: #999; font-size: 13px;")

        principal_titulo_layout.addWidget(titulo_paso)
        principal_titulo_layout.addWidget(subtitulo_paso)

        principal_layout.addLayout(principal_titulo_layout)

        # --- FECHAS ---

        fechas_layout = QHBoxLayout()
        fechas_layout.setSpacing(20) 

        #Fecha inicio
        inicio_layout = QVBoxLayout()
        inicio_label = QLabel("Fecha de Inicio *")
        inicio_label.setStyleSheet("font-weight: bold;")
        self.fecha_inicio = QDateEdit()
        self.fecha_inicio.setCalendarPopup(True)
        self.fecha_inicio.setDate(QDate.currentDate())
        self.fecha_inicio.setStyleSheet("""
            QDateEdit {
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 10px;
                font-size: 13px;
                min-height: 20px;
            }
        """)

        inicio_layout.addWidget(inicio_label)
        inicio_layout.addWidget(self.fecha_inicio)

        # Fecha de fin
        fin_layout = QVBoxLayout()
        fin_label = QLabel("Fecha de Fin *")
        fin_label.setStyleSheet("font-weight: bold;")
        self.fecha_fin = QDateEdit()
        self.fecha_fin.setCalendarPopup(True)
        self.fecha_fin.setDate(QDate.currentDate())
        self.fecha_fin.setStyleSheet("""
            QDateEdit {
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 10px;
                font-size: 13px;
                min-height: 20px;
            }
        """)
        fin_layout.addWidget(fin_label)
        fin_layout.addWidget(self.fecha_fin)

        fechas_layout.addLayout(inicio_layout)
        fechas_layout.addLayout(fin_layout)
        fechas_layout.addStretch()

        principal_layout.addLayout(fechas_layout)

        # --- HORARIOS ---
        horarios_layout = QHBoxLayout()
        horarios_layout.setSpacing(20)

        # Hora de salida
        salida_layout = QVBoxLayout()
        salida_label = QLabel("Hora de Salida *")
        salida_label.setStyleSheet("font-weight: bold;")
        self.hora_salida = QTimeEdit()
        self.hora_salida.setTime(QTime.currentTime())
        self.hora_salida.setStyleSheet("""
            QTimeEdit {
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 10px;
                font-size: 13px;
                min-height: 20px;
            }
        """)
        salida_layout.addWidget(salida_label)
        salida_layout.addWidget(self.hora_salida)

        # Hora de llegada
        llegada_layout = QVBoxLayout()
        llegada_label = QLabel("Hora de Llegada *")
        llegada_label.setStyleSheet("font-weight: bold;")
        self.hora_llegada = QTimeEdit()
        self.hora_llegada.setTime(QTime.currentTime())
        self.hora_llegada.setStyleSheet("""
            QTimeEdit {
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 10px;
                font-size: 13px;
                min-height: 20px;
            }
        """)
        llegada_layout.addWidget(llegada_label)
        llegada_layout.addWidget(self.hora_llegada)

        horarios_layout.addWidget(salida_layout)
        horarios_layout.addWidget(llegada_layout)

        # --- DESTINO ---
        destino_layout = QHBoxLayout()
        destino_layout.setSpacing(20)

        #Destino Principal
        destino_principal_layout = QVBoxLayout()
        destino_label = QLabel("Destino Principal *")
        destino_label.setStyleSheet("font-weight: bold;")
        self.destino_texto = QLineEdit()
        self.destino_texto.setPlaceholderText("Ingrese el destino principal...")
        self.destino_texto.setStyleSheet("""
            QLineEdit {
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 10px;
                font-size: 13px;
                min-height: 20px;
            }
        """)
        destino_principal_layout.addWidget(destino_label)
        destino_principal_layout.addWidget(self.destino_texto)

        # Ciudad
        ciudad_layout = QVBoxLayout()
        ciudad_label = QLabel("Ciudad *")
        ciudad_label.setStyleSheet("font-weight: bold;")
        self.ciudad_texto = QLineEdit()
        self.ciudad_texto.setPlaceholderText("Ciudad...")
        self.ciudad_texto.setStyleSheet("""
            QLineEdit {
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 10px;
                font-size: 13px;
                min-height: 20px;
            }
        """)
        ciudad_layout.addWidget(ciudad_label)
        ciudad_layout.addWidget(self.ciudad_texto)

        destino_layout.addLayout(destino_principal_layout, 2)
        destino_layout.addLayout(ciudad_layout, 1)

        principal_layout.addLayout(destino_layout)

        # --- Direccion y código postal ---
        direccion_layout = QHBoxLayout()
        direccion_layout.setSpacing(20)

        # Dirección completa
        direccion_completa_layout = QVBoxLayout()
        direccion_label = QLabel("Dirección Completa *")
        direccion_label.setStyleSheet("font-weight: bold;")
        self.direccion_texto = QLineEdit()
        self.direccion_texto.setPlaceholderText("Calle, número, referencias...")
        self.direccion_texto.setStyleSheet("""
            QLineEdit {
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 10px;
                font-size: 13px;
                min-height: 20px;
            }
        """)
        direccion_completa_layout.addWidget(direccion_label)
        direccion_completa_layout.addWidget(self.direccion_texto)

        # Código postal
        codigo_layout = QVBoxLayout()
        codigo_label = QLabel("Código postal")
        codigo_label.setStyleSheet("font-weight: bold;")
        self.codigo_input = QLineEdit()
        self.codigo_input.setPlaceholderText("C.P.")
        self.codigo_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 10px;
                font-size: 13px;
                min-height: 20px;
            }
        """)
        codigo_layout.addWidget(codigo_label)
        codigo_layout.addWidget(self.codigo_input)
        
        direccion_layout.addLayout(direccion_completa_layout, 2)
        direccion_layout.addLayout(codigo_layout, 1)

        principal_layout.addLayout(direccion_layout)
        principal_layout.addStretch()

class Paso3Widget(QWidget):
    """
    Paso 3: Contactos e información adicional
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.inicio_ui()

    def inicio_ui(self):
        principal_layout = QVBoxLayout(self)    
        principal_layout.setSpacing(20)

        # Titulo y Subtitulo
        principal_titulo_layout = QVBoxLayout(self)
        
        titulo_paso = QLabel("Contactos e información adicional")
        titulo_paso.setStyleSheet("font-size: 18px; font-weight: bold;")

        subtitulo_paso = QLabel("Proporcione información de contacto y detalles adicionales")
        subtitulo_paso.setStyleSheet("color: #999; font-size: 13px;")

        principal_titulo_layout.addWidget(titulo_paso)
        principal_titulo_layout.addWidget(subtitulo_paso)

        principal_layout.addLayout(principal_titulo_layout)

        # Contacto principal de emergencia
        cont_prin_label = QLabel("Contacto Principal")
        cont_prin_label.setStyleSheet("font-weight: bold; font-size: 14px; margin-top: 10px;")
        principal_layout.addWidget(cont_prin_label)

        # --- FILA 1 --- (nombre, telf, relacion)
        fila1_layout = QHBoxLayout()
        fila1_layout.setSpacing(15)

        #Nombre
        nombre_prin_layout = QVBoxLayout()
        nombre_prin_label = QLabel("Nombre Completo")        
        nombre_prin_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        self.nombre_prin_texto = QLineEdit()
        self.nombre_prin_texto.setPlaceholderText("Nombre y apellidos...")
        self.nombre_prin_texto.setStyleSheet(self.estilo())
        nombre_prin_layout.addWidget(nombre_prin_label)
        nombre_prin_layout.addWidget(self.nombre_prin_texto)

        #Telefono
        telefono_prin_layout = QVBoxLayout()
        telefono_prin_label = QLabel("Teléfono *")
        telefono_prin_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        self.telefono_prin_texto = QLineEdit()
        self.telefono_prin_texto.setPlaceholderText("Número de teléfono...")
        self.telefono_prin_texto.setStyleSheet(self.estilo())
        telefono_prin_layout.addWidget(telefono_prin_label)
        telefono_prin_layout.addWidget(self.telefono_prin_texto)

        #Relacion
        relacion_prin_layout = QVBoxLayout()
        relacion_prin_label = QLabel("Relación *")
        relacion_prin_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        self.relacion_prin_combo = QComboBox()
        self.relacion_prin_combo.addItems(["Seleccionar...", "Padre/Madre", "Hermano/a", 
                                       "Esposo/a", "Hijo/a", "Otro"])
        self.relacion_prin_combo.setStyleSheet(self.estilo())
        relacion_prin_layout.addWidget(relacion_prin_label)
        relacion_prin_layout.addWidget(self.relacion_prin_combo)

        fila1_layout.addLayout(nombre_prin_layout, 2)
        fila1_layout.addLayout(telefono_prin_layout, 1)
        fila1_layout.addLayout(relacion_prin_layout, 1)

        principal_layout.addLayout(fila1_layout)

        # Dirección completa
        direccion_prin_layout = QVBoxLayout()
        direccion_prin_label = QLabel("Dirección Completa *")
        direccion_prin_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        self.direccion_prin_input = QLineEdit()
        self.direccion_prin_input.setPlaceholderText("Dirección completa del contacto...")
        self.direccion_prin_input.setStyleSheet(self.estilo())
        direccion_prin_layout.addWidget(direccion_prin_label)
        direccion_prin_layout.addWidget(self.direccion_prin_input)

        # Contacto Secundario
        cont_secun_label = QLabel("Contacto Secundario")
        cont_secun_label.setStyleSheet("font-weight: bold; font-size: 14px; margin-top: 15px;")    

        principal_layout.addWidget(cont_secun_label)

        # -- FILA 2 --- (Nombre, telefono , relacion)

        fila2_layout = QHBoxLayout()
        fila2_layout.setSpacing(15)

        #Nombre
        nombre_secun_layout = QVBoxLayout()
        nombre_secun_label = QLabel("Nombre Completo")
        nombre_secun_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        self.nombre_secun_input = QLineEdit()
        self.nombre_secun_input.setPlaceholderText("Nombre y apellidos...")
        self.nombre_secun_input.setStyleSheet(self.estilo())
        nombre_secun_layout.addWidget(nombre_secun_label)
        nombre_secun_layout.addWidget(self.nombre_secun_input)

        #Telefono
        telefono_secun_layout = QVBoxLayout()
        telefono_secun_label = QLabel("Teléfono")
        telefono_secun_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        self.telefono_secun_texto = QLineEdit()
        self.telefono_secun_texto.setPlaceholderText("Número de teléfono...")
        self.telefono_secun_texto.setStyleSheet(self.estilo())
        telefono_secun_layout.addWidget(telefono_secun_label)
        telefono_secun_layout.addWidget(self.telefono_secun_texto)
        
        #Relacion
        relacion_secun_layout = QVBoxLayout()
        relacion_secun_label = QLabel("Relación")
        relacion_secun_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        self.relacion_secun_combo = QComboBox()
        self.relacion_secun_combo.addItems(["Seleccionar...", "Padre/Madre", "Hermano/a", 
                                       "Esposo/a", "Hijo/a", "Otro"])
        self.relacion_secun_combo.setStyleSheet(self.estilo())
        relacion_secun_layout.addWidget(relacion_secun_label)
        relacion_secun_layout.addWidget(self.relacion_secun_combo)

        fila2_layout.addLayout(nombre_secun_layout, 2)
        fila2_layout.addLayout(telefono_secun_layout, 1)
        fila2_layout.addLayout(relacion_secun_layout, 1)

        principal_layout.addLayout(fila2_layout)

        principal_layout.addStretch()

    def estilo(self):
        return """
            QLineEdit, QComboBox {
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 10px;
                font-size: 13px;
                min-height: 20px;
            }
            QLineEdit:focus, QComboBox:focus {
                border-color: #2196F3;
            }
        """
    
class Paso4Widget(QWidget):
    """
    Paso 4: Revisión y confirmación
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.iniciar_ui()
    
    def iniciar_ui(self):
        principal_layout = QHBoxLayout(self)
        principal_layout.setSpacing(20)

        # Columna izquierda (Documentos y Compromisos)
        columna_izq = QVBoxLayout()
        columna_izq.setSpacing(15)

        #Documentos requeridos
        docs_frame = QFrame()
        docs_frame.setStyleSheet("""
            QFrame {
                background-color: #FAFAFA;
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        docs_layout = QVBoxLayout(docs_frame)

        docs_titulo = QLabel("Documentos Requeridos")
        docs_titulo.setStyleSheet("font-weight: bold; font-size: 14px;")
        docs_layout.addWidget(docs_titulo)

        docs_subtitulo = QLabel("Sekeccione los documentos que adjuntará con su solicitud")
        docs_subtitulo.setStyleSheet("color: #666; font-size: 11px;")
        docs_layout.addWidget(docs_subtitulo)

        self.doc_identidad = QCheckBox("Documento de identidad del familiar")
        self.doc_relacion = QCheckBox("Comprobante de relación familiar")
        self.doc_invitacion = QCheckBox("Carta de invitación")

        for checkbox in [self.doc_identidad, self.doc_relacion, self.doc_invitacion]:
            checkbox.setStyleSheet("QCheckBox { spacing: 8px; font-size: 13px; }")
            docs_layout.addWidget(checkbox)

        columna_izq.addWidget(docs_frame)

        #Compromisos
        compromisos_frame = QFrame()
        compromisos_frame.setStyleSheet("""
            QFrame {
                background-color: #FAFAFA;
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        compromisos_layout = QVBoxLayout(compromisos_frame)
        
        compromisos_titulo = QLabel("Compromisos")
        compromisos_titulo.setStyleSheet("font-weight: bold; font-size: 14px;")
        compromisos_layout.addWidget(compromisos_titulo)

        compromisos_subtitulo = QLabel("Seleccione los compromisos que acepta cumplir durante el permiso")
        compromisos_subtitulo.setStyleSheet("color: #666; font-size: 11px;")
        compromisos_layout.addWidget(compromisos_subtitulo)


class PantallaSolicitudInterno(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)    
            
        principal_layout = QVBoxLayout(self)             

        principal_layout.addStretch(1)

                   

        self.titulo = QLabel("PANTALLA SOLICITUD")
        self.titulo.setFont(QFont("Arial", 18))
        self.titulo.setAlignment(Qt.AlignCenter)
        principal_layout.addWidget(self.titulo)

        principal_layout.addSpacing(50)        