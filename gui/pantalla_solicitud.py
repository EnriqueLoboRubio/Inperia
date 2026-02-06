import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QLineEdit, QTextEdit, QCheckBox, QDateEdit, QTimeEdit, 
    QComboBox, QStackedWidget, QFrame, QScrollArea, QButtonGroup, QMessageBox
)
from PyQt5.QtCore import Qt, QDate, QTime
from PyQt5.QtGui import QFont, QPixmap

class IndicadorPaso(QWidget):
    """
    Widget para mostrar el indicador de pasos en parte superior
    """
    def __init__(self, parent=None):
        # CORRECCIÓN: Se añadieron paréntesis a super()
        super().__init__(parent)

        self.paso_actual = 1
        self.iniciar_ui()

    def iniciar_ui(self):    
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 10, 0, 20)

        self.pasos = []
        for i in range(4):
            # CORRECCIÓN: Layout hijo sin self
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

            if i < 3:
                linea = QFrame()
                linea.setFrameShape(QFrame.HLine)
                linea.setStyleSheet("background-color: #E0E0E0")
                linea.setFixedHeight(2)
                linea.setFixedWidth(40)
                contenedor_paso.addWidget(linea)
            
            self.pasos.append(circulo)
            
            # Añadir los elementos del contenedor temporal al layout principal
            for j in range(contenedor_paso.count()):
                item = contenedor_paso.itemAt(j)
                if item.widget():
                    layout.addWidget(item.widget())

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

        # Icono
        icono_label = QLabel(self)
        # Nota: Si la imagen no existe, no crashea, solo no se muestra.
        icono_label.setPixmap(QPixmap(icono))
        icono_label.setFixedSize(20,20)
        icono_label.setAlignment(Qt.AlignCenter)

        # Título
        titulo_label = QLabel(titulo)
        titulo_label.setStyleSheet("font-weight: bold; font-size: 14px;")

        # CORRECCIÓN: Layout hijo sin self
        layout_titulo = QHBoxLayout()
        layout_titulo.addWidget(icono_label)
        layout_titulo.addWidget(titulo_label)
        layout_titulo.addStretch() # Para que el texto no se centre raro

        # Subtitulo
        subtitulo_label = QLabel(subtitulo)
        subtitulo_label.setStyleSheet("color: #666; font-size: 11px;")
        subtitulo_label.setWordWrap(True)

        # CORRECCIÓN: Usar addLayout para añadir un layout dentro de otro
        layout.addLayout(layout_titulo)
        layout.addWidget(subtitulo_label)

        self.setStyleSheet("""
            PermisoTarjeta {
                background-color: white;
                border: 2px solid #E0E0E0;
                border-radius: 8px;
            }
        """)

        self.setFixedHeight(120)
        self.setCursor(Qt.PointingHandCursor)

    # CORRECCIÓN: Capturar el evento de click del ratón
    def mousePressEvent(self, event):
        self.EventoClick(event)
        super().mousePressEvent(event)

    def EventoClick(self, evento):
        self.seleccionado = not self.seleccionado
        if self.seleccionado:
            self.setStyleSheet("""
                PermisoTarjeta {
                    background-color: #E3F2FD;
                    border: 2px solid #2196F3;
                    border-radius: 8px;
                }
            """)
        else:
            self.setStyleSheet("""
                PermisoTarjeta {
                    background-color: white;
                    border: 2px solid #E0E0E0;
                    border-radius: 8px;
                }
            """)

class Paso1Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.inicio_ui()

    def inicio_ui(self):
        principal_layout = QVBoxLayout(self)    
        principal_layout.setSpacing(20)  

        # CORRECCIÓN: Todos los sub-layouts se inicializan sin self
        principal_titulo_layout = QVBoxLayout()
        principal_contenido_layout = QHBoxLayout()
        principal_col1_layout = QVBoxLayout() 
        principal_col2_layout = QVBoxLayout()

        # Titulo y subtitulo del paso
        titulo_paso = QLabel("Información básica")
        titulo_paso.setStyleSheet("font-size: 18px; font-weight: bold;")

        subtitulo_paso = QLabel("Selecciona el tipo de permiso y especifique el motivo")
        subtitulo_paso.setStyleSheet("color: #999; font-size: 13px;")

        principal_titulo_layout.addWidget(titulo_paso)
        principal_titulo_layout.addWidget(subtitulo_paso)

        principal_layout.addLayout(principal_titulo_layout)

        # --- COLUMNA 1 --- 
        tipo_label = QLabel("Tipo de permiso *")
        tipo_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        principal_col1_layout.addWidget(tipo_label)

        tarjetas_layout = QHBoxLayout() # Sin self
        tarjetas_layout.setSpacing(15)

        col1 = QVBoxLayout() # Sin self
        col1.setSpacing(15)
        self.tarjeta_familiar = PermisoTarjeta("assets/familia.png", "Salida familiar", "Visitada a familiares directos por motivos justificados")
        self.tarjeta_educativo = PermisoTarjeta("assets/educacion.png", "Permiso educativo", "Asistencia a actividades educativas o exámenes")
        self.tarjeta_defuncion = PermisoTarjeta("assets/cruz.png", "Permiso por defunción", "Asistencia a funeral de familiar directo")
        col1.addWidget(self.tarjeta_familiar)
        col1.addWidget(self.tarjeta_educativo)
        col1.addWidget(self.tarjeta_defuncion)

        col2 = QVBoxLayout() # Sin self
        col2.setSpacing(15)
        self.tarjeta_medico = PermisoTarjeta("assets/corazon.png", "Permiso médico", "Atención médica especializada o acompañamiento")
        self.tarjeta_laboral = PermisoTarjeta("assets/negocio.png", "Permiso laboral", "Actividades laborales o entrevistas de trabajo")
        self.tarjeta_juridico = PermisoTarjeta("assets/justicia.png", "Permiso jurídico", "Asistencia a citas legales o judiciales")
        col2.addWidget(self.tarjeta_medico)
        col2.addWidget(self.tarjeta_laboral)
        col2.addWidget(self.tarjeta_juridico)        

        tarjetas_layout.addLayout(col1)
        tarjetas_layout.addLayout(col2)
        tarjetas_layout.addStretch()

        principal_col1_layout.addLayout(tarjetas_layout)

        motivo_label = QLabel("Motivo específico *")
        motivo_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        principal_col1_layout.addWidget(motivo_label)
        
        self.motivo_texto = QLineEdit()
        self.motivo_texto.setPlaceholderText("Ingrese el motivo específico...")
        self.estilo_input(self.motivo_texto)

        principal_col1_layout.addWidget(self.motivo_texto)
        principal_contenido_layout.addLayout(principal_col1_layout)

        # --- COLUMNA 2 ---
        desc_label = QLabel("Descripción detallada del motivo *")
        desc_label.setStyleSheet("font-weight: bold; margin-top: 10px;")

        principal_col2_layout.addWidget(desc_label)

        self.desc_texto = QTextEdit()
        self.desc_texto.setPlaceholderText("Describa el motivo de su solicitud...")
        self.desc_texto.setFixedHeight(100)
        self.desc_texto.setStyleSheet("border: 2px solid #E0E0E0; border-radius: 8px; padding: 10px;")

        principal_col2_layout.addWidget(self.desc_texto)

        urgencia_label = QLabel("Nivel de urgencia *")
        urgencia_label.setStyleSheet("font-weight: bold; margin-top: 10px;")

        principal_col2_layout.addWidget(urgencia_label)

        urgencia_layout = QHBoxLayout() # Sin self
        self.urgencia_botones = QButtonGroup(self)              

        self.boton_normal = QCheckBox("Normal")
        self.boton_importante = QCheckBox("Importante")
        self.boton_urgente = QCheckBox("Urgente")
        
        self.urgencia_botones.addButton(self.boton_normal)
        self.urgencia_botones.addButton(self.boton_importante)
        self.urgencia_botones.addButton(self.boton_urgente)

        for boton in [self.boton_normal, self.boton_importante, self.boton_urgente]:
            urgencia_layout.addWidget(boton)

        principal_col2_layout.addLayout(urgencia_layout)
        principal_contenido_layout.addLayout(principal_col2_layout)
        principal_layout.addLayout(principal_contenido_layout)

    def estilo_input(self, widget):
        widget.setStyleSheet("""
            QLineEdit { border: 2px solid #E0E0E0; border-radius: 8px; padding: 10px; min-height: 20px; }
            QLineEdit:focus { border-color: #2196F3; }
        """)

class Paso2Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.iniciar_ui()
    
    def iniciar_ui(self):
        principal_layout = QVBoxLayout(self)
        principal_layout.setSpacing(20)

        # CORRECCIÓN: Sin self
        principal_titulo_layout = QVBoxLayout()
        
        titulo_paso = QLabel("Fecha y Destino")
        titulo_paso.setStyleSheet("font-size: 18px; font-weight: bold;")

        subtitulo_paso = QLabel("Especifique las fechas, horarios y lugar del permiso")
        subtitulo_paso.setStyleSheet("color: #999; font-size: 13px;")

        principal_titulo_layout.addWidget(titulo_paso)
        principal_titulo_layout.addWidget(subtitulo_paso)
        principal_layout.addLayout(principal_titulo_layout)

        # --- FECHAS ---
        fechas_layout = QHBoxLayout() # Sin self
        fechas_layout.setSpacing(20) 

        inicio_layout = QVBoxLayout() # Sin self
        inicio_label = QLabel("Fecha de Inicio *")
        inicio_label.setStyleSheet("font-weight: bold;")
        self.fecha_inicio = QDateEdit()
        self.fecha_inicio.setCalendarPopup(True)
        self.fecha_inicio.setDate(QDate.currentDate())
        self.estilo_date(self.fecha_inicio)

        inicio_layout.addWidget(inicio_label)
        inicio_layout.addWidget(self.fecha_inicio)

        fin_layout = QVBoxLayout() # Sin self
        fin_label = QLabel("Fecha de Fin *")
        fin_label.setStyleSheet("font-weight: bold;")
        self.fecha_fin = QDateEdit()
        self.fecha_fin.setCalendarPopup(True)
        self.fecha_fin.setDate(QDate.currentDate())
        self.estilo_date(self.fecha_fin)
        fin_layout.addWidget(fin_label)
        fin_layout.addWidget(self.fecha_fin)

        fechas_layout.addLayout(inicio_layout)
        fechas_layout.addLayout(fin_layout)
        fechas_layout.addStretch()

        principal_layout.addLayout(fechas_layout)

        # --- HORARIOS ---
        horarios_layout = QHBoxLayout() # Sin self
        horarios_layout.setSpacing(20)

        salida_layout = QVBoxLayout() # Sin self
        salida_label = QLabel("Hora de Salida *")
        salida_label.setStyleSheet("font-weight: bold;")
        self.hora_salida = QTimeEdit()
        self.hora_salida.setTime(QTime.currentTime())
        self.estilo_time(self.hora_salida)
        salida_layout.addWidget(salida_label)
        salida_layout.addWidget(self.hora_salida)

        llegada_layout = QVBoxLayout() # Sin self
        llegada_label = QLabel("Hora de Llegada *")
        llegada_label.setStyleSheet("font-weight: bold;")
        self.hora_llegada = QTimeEdit()
        self.hora_llegada.setTime(QTime.currentTime())
        self.estilo_time(self.hora_llegada)
        llegada_layout.addWidget(llegada_label)
        llegada_layout.addWidget(self.hora_llegada)

        horarios_layout.addLayout(salida_layout)
        horarios_layout.addLayout(llegada_layout)
        # Se debe añadir el layout de horarios al principal
        principal_layout.addLayout(horarios_layout) 

        # --- DESTINO ---
        destino_layout = QHBoxLayout() # Sin self
        destino_layout.setSpacing(20)

        destino_principal_layout = QVBoxLayout() # Sin self
        destino_label = QLabel("Destino Principal *")
        destino_label.setStyleSheet("font-weight: bold;")
        self.destino_texto = QLineEdit()
        self.destino_texto.setPlaceholderText("Ingrese el destino principal...")
        self.estilo_input(self.destino_texto)
        destino_principal_layout.addWidget(destino_label)
        destino_principal_layout.addWidget(self.destino_texto)

        ciudad_layout = QVBoxLayout() # Sin self
        ciudad_label = QLabel("Ciudad *")
        ciudad_label.setStyleSheet("font-weight: bold;")
        self.ciudad_texto = QLineEdit()
        self.ciudad_texto.setPlaceholderText("Ciudad...")
        self.estilo_input(self.ciudad_texto)
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
        direccion_label.setStyleSheet("font-weight: bold;")
        self.direccion_texto = QLineEdit()
        self.direccion_texto.setPlaceholderText("Calle, número, referencias...")
        self.estilo_input(self.direccion_texto)
        direccion_completa_layout.addWidget(direccion_label)
        direccion_completa_layout.addWidget(self.direccion_texto)

        codigo_layout = QVBoxLayout() # Sin self
        codigo_label = QLabel("Código postal")
        codigo_label.setStyleSheet("font-weight: bold;")
        self.codigo_input = QLineEdit()
        self.codigo_input.setPlaceholderText("C.P.")
        self.estilo_input(self.codigo_input)
        codigo_layout.addWidget(codigo_label)
        codigo_layout.addWidget(self.codigo_input)
        
        direccion_layout.addLayout(direccion_completa_layout, 2)
        direccion_layout.addLayout(codigo_layout, 1)

        principal_layout.addLayout(direccion_layout)
        principal_layout.addStretch()

    def estilo_input(self, widget):
        widget.setStyleSheet("QLineEdit { border: 2px solid #E0E0E0; border-radius: 8px; padding: 10px; min-height: 20px; }")

    def estilo_date(self, widget):
        widget.setStyleSheet("QDateEdit { border: 2px solid #E0E0E0; border-radius: 8px; padding: 10px; min-height: 20px; }")
    
    def estilo_time(self, widget):
        widget.setStyleSheet("QTimeEdit { border: 2px solid #E0E0E0; border-radius: 8px; padding: 10px; min-height: 20px; }")


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
        titulo_paso.setStyleSheet("font-size: 18px; font-weight: bold;")

        subtitulo_paso = QLabel("Proporcione información de contacto y detalles adicionales")
        subtitulo_paso.setStyleSheet("color: #999; font-size: 13px;")

        principal_titulo_layout.addWidget(titulo_paso)
        principal_titulo_layout.addWidget(subtitulo_paso)

        principal_layout.addLayout(principal_titulo_layout)

        cont_prin_label = QLabel("Contacto Principal")
        cont_prin_label.setStyleSheet("font-weight: bold; font-size: 14px; margin-top: 10px;")
        principal_layout.addWidget(cont_prin_label)

        # --- FILA 1 ---
        fila1_layout = QHBoxLayout() # Sin self
        fila1_layout.setSpacing(15)

        nombre_prin_layout = QVBoxLayout() # Sin self
        nombre_prin_label = QLabel("Nombre Completo")        
        nombre_prin_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        self.nombre_prin_texto = QLineEdit()
        self.nombre_prin_texto.setPlaceholderText("Nombre y apellidos...")
        self.nombre_prin_texto.setStyleSheet(self.estilo())
        nombre_prin_layout.addWidget(nombre_prin_label)
        nombre_prin_layout.addWidget(self.nombre_prin_texto)

        telefono_prin_layout = QVBoxLayout() # Sin self
        telefono_prin_label = QLabel("Teléfono *")
        telefono_prin_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        self.telefono_prin_texto = QLineEdit()
        self.telefono_prin_texto.setPlaceholderText("Número de teléfono...")
        self.telefono_prin_texto.setStyleSheet(self.estilo())
        telefono_prin_layout.addWidget(telefono_prin_label)
        telefono_prin_layout.addWidget(self.telefono_prin_texto)

        relacion_prin_layout = QVBoxLayout() # Sin self
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
        direccion_prin_layout = QVBoxLayout() # Sin self
        direccion_prin_label = QLabel("Dirección Completa *")
        direccion_prin_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        self.direccion_prin_texto = QLineEdit()
        self.direccion_prin_texto.setPlaceholderText("Dirección completa del contacto...")
        self.direccion_prin_texto.setStyleSheet(self.estilo())
        direccion_prin_layout.addWidget(direccion_prin_label)
        direccion_prin_layout.addWidget(self.direccion_prin_texto)
        # Falta añadirlo al layout principal
        principal_layout.addLayout(direccion_prin_layout)

        # Contacto Secundario
        cont_secun_label = QLabel("Contacto Secundario")
        cont_secun_label.setStyleSheet("font-weight: bold; font-size: 14px; margin-top: 15px;")    

        principal_layout.addWidget(cont_secun_label)

        # -- FILA 2 ---
        fila2_layout = QHBoxLayout() 
        fila2_layout.setSpacing(15)

        nombre_secun_layout = QVBoxLayout()
        nombre_secun_label = QLabel("Nombre Completo")
        nombre_secun_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        self.nombre_secun_texto = QLineEdit()
        self.nombre_secun_texto.setPlaceholderText("Nombre y apellidos...")
        self.nombre_secun_texto.setStyleSheet(self.estilo())
        nombre_secun_layout.addWidget(nombre_secun_label)
        nombre_secun_layout.addWidget(self.nombre_secun_texto)

        telefono_secun_layout = QVBoxLayout() 
        telefono_secun_label = QLabel("Teléfono")
        telefono_secun_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        self.telefono_secun_texto = QLineEdit()
        self.telefono_secun_texto.setPlaceholderText("Número de teléfono...")
        self.telefono_secun_texto.setStyleSheet(self.estilo())
        telefono_secun_layout.addWidget(telefono_secun_label)
        telefono_secun_layout.addWidget(self.telefono_secun_texto)
        
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
    def __init__(self, parent=None):
        super().__init__(parent)
        self.iniciar_ui()
    
    def iniciar_ui(self):
        principal_layout = QHBoxLayout(self)
        principal_layout.setSpacing(20)

        # --- Columna izquierda ---
        columna_izq = QVBoxLayout()
        columna_izq.setSpacing(15)

        # Documentos requeridos
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

        docs_subtitulo = QLabel("Seleccione los documentos que adjuntará con su solicitud")
        docs_subtitulo.setStyleSheet("color: #666; font-size: 11px;")
        docs_layout.addWidget(docs_subtitulo)

        self.doc_identidad = QCheckBox("Documento de identidad del familiar")
        self.doc_relacion = QCheckBox("Comprobante de relación familiar")
        self.doc_invitacion = QCheckBox("Carta de invitación")

        for checkbox in [self.doc_identidad, self.doc_relacion, self.doc_invitacion]:
            checkbox.setStyleSheet("QCheckBox { spacing: 8px; font-size: 13px; }")
            docs_layout.addWidget(checkbox)

        columna_izq.addWidget(docs_frame)

        # Compromisos
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

        compromisos_subtitulo = QLabel("Seleccione los compromisos que acepta cumplir")
        compromisos_subtitulo.setStyleSheet("color: #666; font-size: 11px;")
        compromisos_layout.addWidget(compromisos_subtitulo)

        self.comp1 = QCheckBox("Cumplir estrictamente con los horarios establecidos")
        self.comp2 = QCheckBox("Mantener contacto permanente con la institución")
        self.comp3 = QCheckBox("No consumir alcohol ni sustancias prohibidas")
        self.comp4 = QCheckBox("Presentar comprobantes de las actividades realizadas")
        self.comp5 = QCheckBox("Informar cualquier cambio en la programación")
        self.comp6 = QCheckBox("No alejarse del lugar autorizado sin permiso")

        for checkbox in [self.comp1, self.comp2, self.comp3, 
                         self.comp4, self.comp5, self.comp6]:
            checkbox.setStyleSheet("QCheckBox { spacing: 8px; font-size: 13px; }")
            compromisos_layout.addWidget(checkbox)
        
        columna_izq.addWidget(compromisos_frame)

        # --- Columna derecha ---
        columna_der = QVBoxLayout() 

        observaciones_frame = QFrame()
        observaciones_frame.setStyleSheet("""
            QFrame {
                background-color: #FAFAFA;
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        observaciones_layout = QVBoxLayout(observaciones_frame)

        observaciones_titulo = QLabel("Observaciones Adicionales")
        observaciones_titulo.setStyleSheet("font-weight: bold; font-size: 14px;")
        observaciones_layout.addWidget(observaciones_titulo)

        observaciones_subtitulos = QLabel("Comparta información adicional relevante")
        observaciones_subtitulos.setStyleSheet("color: #666; font-size: 11px;")
        observaciones_layout.addWidget(observaciones_subtitulos)

        self.observaciones_texto = QTextEdit()
        self.observaciones_texto.setPlaceholderText("Comentario adicional...")
        self.observaciones_texto.setMinimumHeight(400)
        self.observaciones_texto.setStyleSheet("QTextEdit { background-color: white; border: 1px solid #CCC; }")
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
        principal_layout.setContentsMargins(30, 20, 30, 20)
        principal_layout.setSpacing(0)

        # --- ENCABEZADO --- 
        encabezado_layout = QVBoxLayout()
        encabezado_layout.setSpacing(5)

        # Titulo
        titulo = QLabel("Nueva Solicitud Permiso")
        titulo.setStyleSheet("font-size: 24px; font-weight: bold;")

        self.descripcion_paso = QLabel("Paso 1 de 4 - Complete toda la información requerida")
        self.descripcion_paso.setStyleSheet("color: #666; font-size: 14px;")

        encabezado_layout.addWidget(titulo)
        encabezado_layout.addWidget(self.descripcion_paso)

        principal_layout.addLayout(encabezado_layout)

        # Indicador pasos
        self.indicador_pasos = IndicadorPaso()
        principal_layout.addWidget(self.indicador_pasos)

        # Scroll para el contenido
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")

        # Widget contenedor para los pasos
        contenido_widget = QWidget()
        contenido_layout = QVBoxLayout(contenido_widget)
        contenido_layout.setContentsMargins(0, 20, 0, 20)

        # Frame para el contenido con borde
        self.contenido_frame = QFrame()
        self.contenido_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #E0E0E0;
                border-radius: 12px;
                padding: 30px;
            }
        """)

        frame_layout = QVBoxLayout(self.contenido_frame)

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

        frame_layout.addWidget(self.stacked_widget)

        contenido_layout.addWidget(self.contenido_frame)
        
        scroll.setWidget(contenido_widget) 
        
        principal_layout.addWidget(scroll)

        # --- BOTONES NAVEGACION ---
        botones_layout = QHBoxLayout() # Sin self
        botones_layout.setContentsMargins(0, 20, 0, 0)

        self.boton_anterior = QPushButton("Anterior")
        self.boton_anterior.setFixedSize(120, 45)
        self.boton_anterior.setEnabled(False)
        self.boton_anterior.setStyleSheet("""
            QPushButton {
                background-color: #333;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #555;
            }
            QPushButton:disabled {
                background-color: #CCC;
                color: #888;
            }
        """)

        self.boton_siguiente = QPushButton("Siguiente")
        self.boton_siguiente.setFixedSize(120, 45)
        self.boton_siguiente.setStyleSheet("""
            QPushButton {
                background-color: #000;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #333;
            }
        """)

        botones_layout.addWidget(self.boton_anterior)
        botones_layout.addStretch()
        botones_layout.addWidget(self.boton_siguiente)

        principal_layout.addLayout(botones_layout)

        # Conectar botones
        #self.boton_siguiente.clicked.connect(self.ir_siguiente)
        #self.boton_anterior.clicked.connect(self.ir_anterior)

        self.setStyleSheet("QWidget { background-color: #F5F5F5; }")

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
        self.boton_anterior.setEnabled(paso > 1)
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
        self.descripcion_paso.setText(descripciones[paso-1])


    def mostrar_validacion_error(self, mensaje):
        QMessageBox.critical(self, "Error de Validación", mensaje)