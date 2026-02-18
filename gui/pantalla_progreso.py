from PyQt5.QtWidgets import (
    QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QFrame, QScrollArea, QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap

from gui.estilos import *

class IndicadorProgreso(QWidget):
    """
    Idicador de progreso de la entrevista
    """
    def __init__(self, fech_ent = "", estado = "iniciada", parent = None):
        super().__init__(parent)
        self.fech_ent = fech_ent
        self.estado = estado 

        #Iconos para pasos
        self.icono_realizado = QPixmap("assets/realizado.png").scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)     
        self.icono_pendiente = QPixmap("assets/pendiente.png").scaled(105, 105, Qt.KeepAspectRatio, Qt.SmoothTransformation)   
        self.icono_rechazado = QPixmap("assets/rechazado.png").scaled(97, 97, Qt.KeepAspectRatio, Qt.SmoothTransformation)  
        self.icono_circulo = QPixmap("assets/circulo.png").scaled(90, 90, Qt.KeepAspectRatio, Qt.SmoothTransformation) 

        self.iniciar_ui()

    def actualizar_datos_indicador(self, fech_ent, estado):
        self.fech_ent = fech_ent
        self.estado = estado

        # -------- PASO 2 ICONO --------
        if self.fech_ent != "":
            self.icono_2_lbl.setPixmap(self.icono_realizado)
        else:
            self.icono_2_lbl.setPixmap(self.icono_pendiente)

        # -------- PASO 3 ICONO --------
        if self.estado == "pendiente":
            self.icono_3_lbl.setPixmap(self.icono_pendiente)
        elif self.estado == "iniciada":
            self.icono_3_lbl.setPixmap(self.icono_circulo)
        elif self.estado == "rechazada":
            self.icono_3_lbl.setPixmap(self.icono_rechazado)
        else:
            self.icono_3_lbl.setPixmap(self.icono_realizado)

        # -------- PASO 4 ICONO --------
        if self.estado in ["cancelada", "rechazada"]:
            self.icono_4_lbl.setPixmap(self.icono_rechazado)
        elif self.estado == "aceptada":
            self.icono_4_lbl.setPixmap(self.icono_realizado)
        else:
            self.icono_4_lbl.setPixmap(self.icono_circulo)

        # -------- LINEAS --------
        self.actualizar_linea(self.linea_2, self.estado in ["aceptada", "rechazada", "cancelada", "pendiente"])
        self.actualizar_linea(self.linea_3, self.estado in ["aceptada", "rechazada", "cancelada"])

        # -------- TEXTOS --------
        if self.estado == "aceptada":
            self.subtitulo_4_lbl.setText("La solicitud ha sido aceptada")
        elif self.estado == "rechazada":
            self.subtitulo_4_lbl.setText("La solicitud ha sido rechazada")
        elif self.estado == "cancelada":
            self.subtitulo_4_lbl.setText("La solicitud ha sido cancelada")
        else:
            self.subtitulo_4_lbl.setText("")

        if self.estado != "iniciada":
            self.subtitulo_3_lbl.setText("Análisis inteligente y valoración personal en curso")
        else:
            self.subtitulo_3_lbl.setText("")

    def actualizar_linea(self, linea, activa):
        if activa:
            linea.setStyleSheet("background-color: black;")
        else:
            linea.setStyleSheet("background-color: #B7B6B6;")



    def iniciar_ui(self):
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(0, 15, 0, 0)
        layout_principal.setSpacing(0)    

        # Paso 1: Solicitud iniciada
        paso_1 = QHBoxLayout() 
        paso_1.setContentsMargins(0 , 0 , 0, 0)       
        paso_1.setAlignment(Qt.AlignTop)

        widget_1 = QWidget()
        widget_1.setFixedWidth(100)

        # Icono + linea paso 1
        columna_1 = QVBoxLayout(widget_1)
        columna_1.setContentsMargins(0, 0, 0, 0)
        columna_1.setSpacing(0)
        columna_1.setAlignment(Qt.AlignTop)
        
        self.icono_1_lbl = QLabel()
        self.icono_1_lbl.setFixedSize(100, 100)    
        self.icono_1_lbl.setPixmap(self.icono_realizado)        

        columna_1.addWidget(self.icono_1_lbl)

        self.linea_1 = self.crear_linea(True)  
        self.linea_1.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        columna_1.addWidget(self.linea_1, alignment=Qt.AlignHCenter)

        # Texto paso 1
        texto_1 = QVBoxLayout()
        texto_1.setContentsMargins(0, 10, 0, 20)
        texto_1.setSpacing(5)        

        # Titulo 1
        titulo_1_lbl = QLabel("Solicitud enviada")
        titulo_1_lbl.setStyleSheet(ESTILO_DATO_PRINCIPAL_SOLICITUD)        
        subtitulo_1_lbl = QLabel("Datos del permiso registrado por el usuario")
        subtitulo_1_lbl.setStyleSheet(ESTILO_TEXTO)

        texto_1.addWidget(titulo_1_lbl)
        texto_1.addWidget(subtitulo_1_lbl)
        texto_1.addStretch()

        paso_1.addWidget(widget_1)
        paso_1.addLayout(texto_1)                            
        layout_principal.addLayout(paso_1)    

        # Paso 2: Entrevista realizada
        paso_2 = QHBoxLayout() 
        paso_2.setContentsMargins(0 , 0, 0, 0)      
        paso_2.setAlignment(Qt.AlignTop)

        widget_2 = QWidget()
        widget_2.setFixedWidth(100)

        columna_2 = QVBoxLayout(widget_2)   
        columna_2.setContentsMargins(0, 0, 0, 0) 
        columna_2.setSpacing(0)
        columna_2.setAlignment(Qt.AlignTop)

        self.icono_2_lbl = QLabel()
        self.icono_2_lbl.setFixedSize(100, 100)      
        # Icono segun si hay o no entrevista
        if self.fech_ent != "":
            icono = self.icono_realizado
        else:
            icono = self.icono_pendiente

        self.icono_2_lbl.setPixmap(icono)      
        columna_2.addWidget(self.icono_2_lbl)

        self.linea_2 = self.crear_linea(self.estado == "aceptada" or self.estado == "rechazada" or self.estado == "cancelada" or self.estado == "pendiente")  
        self.linea_2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        columna_2.addWidget(self.linea_2, 0, Qt.AlignHCenter)

        # Texto paso 2
        texto_2 = QVBoxLayout()
        texto_2.setSpacing(5)
        texto_2.setContentsMargins(0, 10, 0, 20)

        # Titulo 2
        titulo_2_lbl = QLabel("Entrevista realizada")
        titulo_2_lbl.setStyleSheet(ESTILO_DATO_PRINCIPAL_SOLICITUD)        
        subtitulo_2_lbl = QLabel("Entrevista inicial completada y enviada")
        subtitulo_2_lbl.setStyleSheet(ESTILO_TEXTO)

        texto_2.addWidget(titulo_2_lbl)
        texto_2.addWidget(subtitulo_2_lbl)
        if self.fech_ent != "":
             self.fecha_2_lbl = QLabel(self.fech_ent) 
             self.fecha_2_lbl.setStyleSheet(ESTILO_SUBTITULO_PASO)
             texto_2.addWidget(self.fecha_2_lbl)
        texto_2.addStretch()

        paso_2.addWidget(widget_2)
        paso_2.addLayout(texto_2)
        layout_principal.addLayout(paso_2)

        # Paso 3: Evaluacion
        paso_3 = QHBoxLayout()
        paso_3.setContentsMargins(0, 0, 0, 0)
        paso_3.setAlignment(Qt.AlignTop)

        widget_3 = QWidget()
        widget_3.setFixedWidth(100)

        # Icono + linea paso 3
        columna_3 = QVBoxLayout(widget_3)
        columna_3.setContentsMargins(0, 0, 0, 0)
        columna_3.setSpacing(0)
        columna_3.setAlignment(Qt.AlignTop)
        
        if self.estado == "pendiente":
            icono = self.icono_pendiente
        elif self.estado == "iniciada":
            icono = self.icono_circulo
        elif self.estado == "rechazada":
            icono = self.icono_rechazado
        else:
            icono = self.icono_realizado
        
        self.icono_3_lbl = QLabel()
        self.icono_3_lbl.setFixedSize(100, 100)  
        self.icono_3_lbl.setPixmap(icono)      
         
        columna_3.addWidget(self.icono_3_lbl)

        self.linea_3 = self.crear_linea(self.estado == "aceptada" or self.estado == "rechazada" or self.estado == "cancelada")
        self.linea_3.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        columna_3.addWidget(self.linea_3, 0, Qt.AlignHCenter)

        # Texto paso 3
        texto_3 = QVBoxLayout()
        texto_3.setContentsMargins(0, 10, 0, 20)
        texto_3.setSpacing(5)        

        # Titulo 1
        titulo_3_lbl = QLabel("Evaluación en curso")
        titulo_3_lbl.setStyleSheet(ESTILO_DATO_PRINCIPAL_SOLICITUD)
        if self.estado != "iniciada":
            sub = "Análisis inteligente y valoración personal en curso"
        else:
            sub = ""         
        self.subtitulo_3_lbl = QLabel(sub)
        self.subtitulo_3_lbl.setStyleSheet(ESTILO_TEXTO)

        texto_3.addWidget(titulo_3_lbl)
        texto_3.addWidget(self.subtitulo_3_lbl)
        texto_3.addStretch()

        paso_3.addWidget(widget_3)
        paso_3.addLayout(texto_3)
        layout_principal.addLayout(paso_3)

        # Paso 4: Decision
        paso_4 = QHBoxLayout() 
        paso_4.setContentsMargins(0 , 0 , 0, 0)       
        paso_4.setAlignment(Qt.AlignTop)

        widget_4 = QWidget()
        widget_4.setFixedWidth(100)

        # Icono paso 4
        columna_4 = QVBoxLayout(widget_4)
        columna_4.setContentsMargins(0, 0, 0, 0)
        columna_4.setSpacing(0)
        columna_4.setAlignment(Qt.AlignTop)

        if self.estado == "cancelada" or self.estado == "rechazada":
            icono = self.icono_rechazado
        elif self.estado == "aceptada":
            icono = self.icono_realizado
        else:
            icono = self.icono_circulo
        
        self.icono_4_lbl = QLabel()
        self.icono_4_lbl.setFixedSize(100, 100)    
        self.icono_4_lbl.setPixmap(icono)        

        columna_4.addWidget(self.icono_4_lbl)

        # Texto paso 4
        texto_4 = QVBoxLayout()
        texto_4.setContentsMargins(0, 10, 0, 20)
        texto_4.setSpacing(5)        

        # Titulo 4
        titulo_4_lbl = QLabel("Resolución final")
        titulo_4_lbl.setStyleSheet(ESTILO_DATO_PRINCIPAL_SOLICITUD)   
        if self.estado == "aceptada":
            resolucion = "La solicitud ha sido aceptada"
        elif self.estado == "rechazada":
            resolucion = "La soliciud ha sido rechazada"
        elif self.estado == "cancelada":
            resolucion = "La solicitud ha sido cancelada"    
        else:
            resolucion = "" 
        self.subtitulo_4_lbl = QLabel(resolucion)
        self.subtitulo_4_lbl.setStyleSheet(ESTILO_TEXTO)

        texto_4.addWidget(titulo_4_lbl)
        texto_4.addWidget(self.subtitulo_4_lbl)
        texto_4.addStretch()

        paso_4.addWidget(widget_4)
        paso_4.addLayout(texto_4)                            
        layout_principal.addLayout(paso_4)   
        

        layout_principal.addStretch()
    
    def crear_linea(self, hecho = False):

        if hecho is False:
            color = "#B7B6B6"
        else:
            color = "black"    

        linea = QFrame()
        linea.setStyleSheet(f"background-color: {color}")
        linea.setFixedWidth(6)
        linea.setFixedHeight(130) 
        
        return linea   
    
    def limpiar_layout(self):
        layout = self.layout()
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    sublayout = item.layout()
                    if sublayout is not None:
                        self.limpiar_sublayout(sublayout)

def limpiar_sublayout(self, layout):
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget is not None:
            widget.deleteLater()
        else:
            sublayout = item.layout()
            if sublayout is not None:
                self.limpiar_sublayout(sublayout)

class PantallaProgresoInterno(QWidget):

    # Señales para botones
    ver_entrevista_signal = pyqtSignal()
    descargar_solicitud_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)        
        self.iniciar_ui()
        

    def iniciar_ui(self):

        # ---------- GRID PRINCIPAL ----------
        grid = QGridLayout()
        grid.setContentsMargins(10,0,60,30)
        grid.setHorizontalSpacing(30)
        grid.setVerticalSpacing(30)

        # definición de proporciones

        grid.setColumnStretch(0, 65)
        grid.setColumnStretch(1, 35)

        grid.setRowStretch(0, 80)
        grid.setRowStretch(1, 20)

        # ========== Resumen solicitud ==========

        resumen_frame = QFrame()
        resumen_frame.setObjectName("apartado")
        resumen_frame.setStyleSheet(ESTILO_APARTADO_FRAME)

        resumen_layout = QVBoxLayout(resumen_frame)

        # --- Encabezado ---
        encabezado_resumen = QHBoxLayout()
            
        # Icono documento
        doc_icon_label = QLabel(self)
        icono = QPixmap("assets/documento.png").scaled(70, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)     
        doc_icon_label.setPixmap(icono)
        doc_icon_label.setFixedSize(80,80)
        doc_icon_label.setStyleSheet("background: transparent; border: none;")

        encabezado_resumen.addWidget(doc_icon_label)

        titulo_layout = QVBoxLayout()
        titulo_layout.setSpacing(3)

        # Titulo
        self.titulo_resumen = QLabel("Solicitud #00000") # Cargar de objeto id de solicitud
        self.titulo_resumen.setStyleSheet(ESTILO_TITULO_PASO_ENCA)

        # Subtitulo
        self.subtitulo_resumen = QLabel("Solicitud de permiso de __________") # Cargar de objeto: tipo
        self.subtitulo_resumen.setStyleSheet(ESTILO_SUBTITULO_SOLICITUD)

        titulo_layout.addWidget(self.titulo_resumen)
        titulo_layout.addWidget(self.subtitulo_resumen)  

        encabezado_resumen.addLayout(titulo_layout)         
        encabezado_resumen.addStretch()       
            
        estado_layout = QHBoxLayout()

        # Icono estado
        estado_icon_label = QLabel(self)
        icono = QPixmap("assets/importante.png").scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        estado_icon_label.setPixmap(icono)
        estado_icon_label.setFixedSize(45,45)
        estado_icon_label.setStyleSheet("background: transparent; border: none;")

        estado_layout.addWidget(estado_icon_label)

        # Estado
        self.estado_label = QLabel("En revisión") # Cargar de objeto: estado, cambiar texto y color
        self.estado_label.setAlignment(Qt.AlignCenter) 
        self.estado_label.setFixedSize(140, 40)
        self.estado_label.setStyleSheet(ESTILO_ESTADO)

        estado_layout.addWidget(self.estado_label)

        encabezado_resumen.addLayout(estado_layout)

        resumen_layout.addLayout(encabezado_resumen)

        # Linea separadora
        linea_sep = QFrame()
        linea_sep.setFrameShape(QFrame.HLine)
        linea_sep.setStyleSheet("background-color: #E0E0E0; max-height: 1px;")

        resumen_layout.addWidget(linea_sep)

        # --- Scroll resumen ---
        scroll_resumen = QScrollArea()
        scroll_resumen.setWidgetResizable(True)
        scroll_resumen.setFrameShape(QFrame.NoFrame) 
        scroll_resumen.setStyleSheet("background-color: transparent;")    
        scroll_resumen.setStyleSheet(ESTILO_SCROLL)

        info_widget = QWidget()
        info_widget.setStyleSheet("background-color: transparent;")   
            
        info_layout = QVBoxLayout(info_widget)
        scroll_resumen.setWidget(info_widget)

        # Solicitante
        info_grid = QGridLayout()
        info_grid.setVerticalSpacing(40) # Espacio vertical entre filas
        info_grid.setHorizontalSpacing(20) # Espacio entre columnas

        # --- BLOQUE 1: SOLICITANTE ---
        # (Fila 0, Columna 0)        
        self.widget_solicitante = self.crear_dato_detalle(
            "assets/interno.png",      
            "Solicitante",             
            "Nombre Apellido1 Apellido2", 
            "Nº RC 00000"          
        )
        info_grid.addWidget(self.widget_solicitante, 0, 0)

        # --- BLOQUE 2: FECHAS ---
        # (Fila 0, Columna 1)
        self.widget_fechas = self.crear_dato_detalle(
            "assets/calendario.png", 
            "Fechas del Permiso",
            "00/00/0000 - 00/00/0000"
        )
        info_grid.addWidget(self.widget_fechas, 0, 1)

        # --- BLOQUE 3: DESTINO ---
        # (Fila 1, Columna 0)
        self.widget_destino = self.crear_dato_detalle(
            "assets/destino.png",
            "Destino",
            "Domicilio familiar - Calle Principal 123, Ciudad"
        )
  
        info_grid.addWidget(self.widget_destino, 1, 0, 1, 2) 
    
        info_layout.addLayout(info_grid)
        info_layout.addSpacing(40)

        # Motivo
        motivo_layout = QVBoxLayout()

        mot_tit_label = QLabel("Motivo del Permiso")
        mot_tit_label.setStyleSheet(ESTILO_DATO_PRINCIPAL_SOLICITUD)
        motivo_layout.addWidget(mot_tit_label)

        self.mot_label = QLabel("Visita por motivos de salud de familiar directo. Acompañamiento en tratamiento médico de la madre del solicitante.") # Cargar de objeto: motivo, cambiar texto
        self.mot_label.setStyleSheet(ESTILO_TEXTO)
        self.mot_label.setWordWrap(True)
        self.mot_label.setAlignment(Qt.AlignJustify)
        motivo_layout.addWidget(self.mot_label)

        info_layout.addLayout(motivo_layout)
        info_layout.addSpacing(40)

        # Observación
        observaciones_layout = QVBoxLayout()

        obs_tit_label = QLabel("Observaciones")
        obs_tit_label.setStyleSheet(ESTILO_DATO_PRINCIPAL_SOLICITUD)
        observaciones_layout.addWidget(obs_tit_label)       

        self.obs_label = QLabel("El solicitante ha mostrado buen comportamiento durante los últimos 6 meses. Se requiere verificación adicional de la documentación médica presentada.") # Cargar de objeto: observaciones, cambiar texto
        self.obs_label.setStyleSheet(ESTILO_TEXTO)
        self.obs_label.setWordWrap(True)
        self.obs_label.setAlignment(Qt.AlignJustify)
        observaciones_layout.addWidget(self.obs_label)

        self.prof_label = QLabel("Enrique Lobo - Profesional") 
        self.prof_label.setWordWrap(True)
        self.prof_label.setAlignment(Qt.AlignJustify)
        self.prof_label.setStyleSheet(ESTILO_SUBTITULO_PASO)
        observaciones_layout.addWidget(self.prof_label)

        info_layout.addLayout(observaciones_layout)     
        info_layout.addStretch()

        resumen_layout.addWidget(scroll_resumen)   

        grid.addWidget(resumen_frame, 0, 0)

        # ========== Documentacion y acciones ==========
        acciones_frame = QFrame()
        acciones_frame.setObjectName("apartado")
        acciones_frame.setStyleSheet(ESTILO_APARTADO_FRAME)

        acciones_layout = QVBoxLayout(acciones_frame)
        acciones_layout.setContentsMargins(30, 5, 30, 20)

        #Titulo
        titulo_acc = QLabel("Documentación y acciones")
        titulo_acc.setStyleSheet(ESTILO_TITULO_APARTADO_SOLICITUD)
        acciones_layout.addWidget(titulo_acc)
        acciones_layout.setSpacing(5)

        #Botones
        botones_layout = QHBoxLayout()       

        self.boton_solicitud = QPushButton("Descargar Solicitud")
        self.boton_solicitud.setFixedSize(250, 45) 
        self.boton_solicitud.setStyleSheet(ESTILO_BOTON_SIG_ATR)
        self.boton_solicitud.setCursor(Qt.PointingHandCursor)

        self.boton_entrevista = QPushButton("Ver Entrevista")
        self.boton_entrevista.setFixedSize(250, 45) 
        self.boton_entrevista.setStyleSheet(ESTILO_BOTON_SIG_ATR)
        self.boton_entrevista.setCursor(Qt.PointingHandCursor)

        self.boton_cancelar = QPushButton("Cancelar Solicitud")
        self.boton_cancelar.setFixedSize(250, 45) 
        self.boton_cancelar.setStyleSheet(ESTILO_BOTON_SIG_ATR)
        self.boton_cancelar.setCursor(Qt.PointingHandCursor)

        botones_layout.addWidget(self.boton_solicitud)
        botones_layout.addSpacing(80)
        botones_layout.addWidget(self.boton_entrevista)
        botones_layout.addSpacing(80)
        botones_layout.addWidget(self.boton_cancelar)       

        acciones_layout.addLayout(botones_layout)

        grid.addWidget(acciones_frame, 1, 0)

        # ========== Progreso solicitud ==========
        progreso_frame = QFrame()
        progreso_frame.setObjectName("apartado")
        progreso_frame.setStyleSheet(ESTILO_APARTADO_FRAME)

        progreso_layout = QVBoxLayout(progreso_frame)

        #Titulo 
        titulo_progreso = QLabel("Progreso de la Solicitud")
        titulo_progreso.setStyleSheet(ESTILO_TITULO_PASO_ENCA)   
        progreso_layout.addWidget(titulo_progreso, alignment=Qt.AlignCenter)

        #Subtitulo
        subtitulo_progreso = QLabel("Seguimiento del proceso de evalucación")
        subtitulo_progreso.setStyleSheet(ESTILO_SUBTITULO_SOLICITUD)   
        progreso_layout.addWidget(subtitulo_progreso, alignment=Qt.AlignCenter)
       

        self.indicador = IndicadorProgreso("17/27/2020", "aceptada")

        progreso_layout.addWidget(self.indicador)
        progreso_layout.addStretch()

        grid.addWidget(progreso_frame, 0, 1, 2, 1)

        self.setLayout(grid)

    def crear_dato_detalle(self, icono_path, titulo, linea1, linea2=None):
            """
            Crea un bloque de información con icono alineado arriba.
            icono_path: Ruta a la imagen
            titulo: Texto gris pequeño 
            linea1: Dato principal en negrita 
            linea2: Dato secundario opcional 
            """
            widget = QWidget()
            layout = QHBoxLayout(widget)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(15) # Espacio entre icono y texto
            layout.setAlignment(Qt.AlignTop)

            # --- ICONO ---
            lbl_icono = QLabel()
            lbl_icono.setFixedSize(40,40)
            lbl_icono.setScaledContents(True)
            
            # cargar imagen o usar texto si falla
            pixmap = QPixmap(icono_path)
            if not pixmap.isNull():            
                lbl_icono.setPixmap(pixmap.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:    
                lbl_icono.setText(icono_path) # emoji o letra
                lbl_icono.setStyleSheet("font-size: 20px; color: #000000;")
                
            lbl_icono.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

            # --- TEXTOS ---
            columna_texto = QVBoxLayout()
            columna_texto.setSpacing(5)
            columna_texto.setContentsMargins(0, 0, 0, 0)

            # Título pequeño
            self.lbl_titulo = QLabel(titulo)
            self.lbl_titulo.setStyleSheet(ESTILO_TITULO_DETALLE_SOLICITUD)
            columna_texto.addWidget(self.lbl_titulo)

            # Dato Principal
            self.lbl_l1 = QLabel(linea1)
            self.lbl_l1.setStyleSheet(ESTILO_DATO_PRINCIPAL_SOLICITUD)
            columna_texto.addWidget(self.lbl_l1)

            # Dato Secundario
            if linea2:
                self.lbl_l2 = QLabel(linea2)
                self.lbl_l2.setStyleSheet(ESTILO_DATO_SECUNDARIO_SOLICITUD)
                columna_texto.addWidget(self.lbl_l2)
            
            columna_texto.addStretch()
            
            layout_icono = QVBoxLayout()
            layout_icono.addWidget(lbl_icono)
            layout_icono.addStretch()

            layout.addLayout(layout_icono)
            layout.addLayout(columna_texto)
            
            return widget
    
    def cargar_datos_solicitud(self, solicitud, nombre_interno, num_RC):
        """
        Carga los datos de la solicitud en la interfaz
        """          

        # Actualizar titulo y subtitulo
        self.titulo_resumen.setText(f"Solicitud #{self.solicitud.id_solicitud}")

        tipo_traduccion = {
            "familiar": "Solicitud de permiso de salida familiar",
            "educativo": "Solicitud de permiso educativo",
            "defuncion": "Solicitud de permiso por defunción",
            "medico": "Solicitud de permiso médico",
            "laboral": "Solicitud de permiso laboral",
            "juridico": "Solicitud de permiso jurídico"
        }

        self.subtitulo_resumen.setText(tipo_traduccion.get(solicitud.tipo, "Solicitud de permiso"))

        # Actualizar estado
        self.actualizar_estado(solicitud.estado)

        # Actualizar info solicitante
        self.widget_solicitante.lbl_l1.setText(nombre_interno)
        self.widget_solicitante.lbl_l2.setText(num_RC)

        # Actualizar fechas
        self.widget_fechas.lbl_l1.setText(f"{solicitud.fecha_inicio} - {solicitud.fecha_fin}")

        # Actualizar destino
        self.widget_destino.lbl_l1.setText(f"{solicitud.direccion}, {solicitud.destino}")
        self.widget_destino.lbl_l2.setText(f"{solicitud.ciudad} - {solicitud.cod_pos}")

        # Motivo
        self.mot_label.setText(f"{solicitud.motivo}")

        # Observaciones
        if solicitud.observaciones == "":
            obs = "SIN OBSERVACIONES"
        else:
            obs = solicitud.observaciones

        self.obs_label.setText(obs)
        self.prof_label.setText("")

        # Actualizar progreso
        if solicitud.entrevista.fecha is None:
            fecha = ""
        else:
            fecha = solicitud.entrevista.fecha

        self.indicador.actualizar_datos_indicador(fecha, solicitud.estado)

    def actualizar_estado(self, estado):
        """
        Actualiza el badge de estado según el estado de la solicitud
        """
        estados_config = {
            "iniciada": ("Iniciada", "#3498DBAE"),
            "pendiente": ("En revisión", "#DB9334C8"),           
            "aceptada": ("Aceptada", "#27AE5FA6"),
            "rechazada": ("Rechazada", "#E74D3CAB"),
            "cancelada": ("Cancelada", "#95A5A6BA")
        }

        texto, color = estados_config.get(estado, ("En revisión", "#DB9334C8"))        
        self.estado_label.setText(texto)
        self.estado_label.setStyleSheet(ESTILO_ESTADO.replace("#D3D3D3", color))



        




            
          
       