from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QScrollArea,
    QGridLayout,
)
from datetime import date, datetime

from gui.estilos import *


class PantallaPerfilInternoProfesional(QWidget):
    volver = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._iniciar_ui()

    def _iniciar_ui(self):
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(10, 0, 60, 30)
        layout_principal.setSpacing(30)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet(ESTILO_SCROLL)

        contenedor = QWidget()
        self.layout_contenido = QVBoxLayout(contenedor)
        self.layout_contenido.setContentsMargins(10, 0, 10, 30)
        self.layout_contenido.setSpacing(30)

        self._crear_bloque_cabecera()
        self._crear_bloque_datos()
        self._crear_bloque_entrevistas()
        self._crear_bloque_historial()

        self.layout_contenido.addStretch()
        scroll.setWidget(contenedor)
        layout_principal.addWidget(scroll, 1)

        fila_inferior = QHBoxLayout()
        fila_inferior.addStretch()
        self.boton_volver = QPushButton("Volver")
        self.boton_volver.setCursor(Qt.PointingHandCursor)
        self.boton_volver.setStyleSheet(ESTILO_BOTON_SIG_ATR)
        self.boton_volver.clicked.connect(self.volver.emit)
        fila_inferior.addWidget(self.boton_volver)
        layout_principal.addLayout(fila_inferior)

    def _crear_bloque_cabecera(self):
        frame = QFrame()
        frame.setObjectName("apartado")
        frame.setStyleSheet(ESTILO_APARTADO_FRAME)
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(18, 12, 18, 12)

        self.lbl_avatar = QLabel("IN")
        self.lbl_avatar.setFixedSize(52, 52)
        self.lbl_avatar.setAlignment(Qt.AlignCenter)
        self.lbl_avatar.setStyleSheet(ESTILO_BOTON_PERFIL)
        layout.addWidget(self.lbl_avatar, alignment=Qt.AlignTop)

        bloque = QVBoxLayout()
        self.lbl_nombre = QLabel("-")
        self.lbl_nombre.setStyleSheet(ESTILO_TITULO_PASO_ENCA)
        self.lbl_rc = QLabel("-")
        self.lbl_rc.setStyleSheet(ESTILO_SUBTITULO_SOLICITUD)
        bloque.addWidget(self.lbl_nombre)
        bloque.addWidget(self.lbl_rc)
        layout.addLayout(bloque, 1)

        self.layout_contenido.addWidget(frame)

    def _crear_bloque_datos(self):
        fila = QHBoxLayout()
        fila.setSpacing(30)

        # Datos personales
        frame_datos = QFrame()
        frame_datos.setObjectName("apartado")
        frame_datos.setStyleSheet(ESTILO_APARTADO_FRAME)
        datos_layout = QVBoxLayout(frame_datos)
        datos_layout.setSpacing(8)

        fila_titulo_datos = QHBoxLayout()
        fila_titulo_datos.setSpacing(8)

        tit = QLabel("Datos")
        tit.setStyleSheet(ESTILO_TITULO_APARTADO_SOLICITUD)
        icono_datos = QLabel()
        tam_icono = tit.fontMetrics().height() + 10
        pixmap = QPixmap("assets/interno.png").scaled(
            tam_icono, tam_icono, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        icono_datos.setPixmap(pixmap)
        icono_datos.setFixedSize(tam_icono, tam_icono)

        fila_titulo_datos.addWidget(icono_datos, alignment=Qt.AlignVCenter)
        fila_titulo_datos.addWidget(tit, alignment=Qt.AlignVCenter)
        fila_titulo_datos.addStretch()
        datos_layout.addLayout(fila_titulo_datos)
        datos_layout.addSpacing(8)

        grid_datos = QGridLayout()
        grid_datos.setHorizontalSpacing(30)
        grid_datos.setVerticalSpacing(14)

        self.lbl_lugar_nac_val = self._crear_bloque_info(grid_datos, 0, 0, "Lugar de Nacimiento")
        self.lbl_fecha_nac_val = self._crear_bloque_info(grid_datos, 0, 1, "Fecha de Nacimiento")
        self.lbl_contacto_emer_val = self._crear_bloque_info(grid_datos, 1, 0, "Contacto de Emergencia", colspan=2)
        self.lbl_numero_emer_val = self._crear_bloque_info(grid_datos, 2, 0, "", colspan=2, mostrar_titulo=False)

        datos_layout.addLayout(grid_datos)
        datos_layout.addStretch()

        # Info legal
        frame_legal = QFrame()
        frame_legal.setObjectName("apartado")
        frame_legal.setStyleSheet(ESTILO_APARTADO_FRAME)
        legal_layout = QVBoxLayout(frame_legal)
        legal_layout.setSpacing(8)

        fila_titulo_legal = QHBoxLayout()
        fila_titulo_legal.setContentsMargins(0, 0, 0, 0)
        fila_titulo_legal.setSpacing(8)

        tit_legal = QLabel("Información Legal")
        tit_legal.setStyleSheet(ESTILO_TITULO_APARTADO_SOLICITUD)
        icono_legal = QLabel()
        tam_icono_legal = tit_legal.fontMetrics().height() + 5
        pixmap_legal = QPixmap("assets/justicia.png").scaled(
            tam_icono_legal, tam_icono_legal, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        icono_legal.setPixmap(pixmap_legal)
        icono_legal.setFixedSize(tam_icono_legal, tam_icono_legal)
        icono_legal.setAlignment(Qt.AlignCenter)
        fila_titulo_legal.addWidget(icono_legal, alignment=Qt.AlignVCenter)
        fila_titulo_legal.addWidget(tit_legal, alignment=Qt.AlignVCenter)
        fila_titulo_legal.addStretch()
        legal_layout.addLayout(fila_titulo_legal)
        legal_layout.addSpacing(8)

        grid_legal = QGridLayout()
        grid_legal.setHorizontalSpacing(30)
        grid_legal.setVerticalSpacing(14)

        self.lbl_delito_val = self._crear_bloque_info(grid_legal, 0, 0, "Delito")
        self.lbl_condena_val = self._crear_bloque_info(grid_legal, 0, 1, "Condena")
        self.lbl_fecha_ingreso_val = self._crear_bloque_info(grid_legal, 1, 0, "Fecha de Ingreso")
        self.lbl_tiempo_restante_val = self._crear_bloque_info(grid_legal, 1, 1, "Tiempo Restante")
        self.lbl_situacion_val = self._crear_bloque_info(grid_legal, 2, 0, "Situación legal")
        self.lbl_modulo_val = self._crear_bloque_info(grid_legal, 2, 1, "Módulo")

        legal_layout.addLayout(grid_legal)
        legal_layout.addStretch()

        fila.addWidget(frame_datos, 1)
        fila.addWidget(frame_legal, 1)
        self.layout_contenido.addLayout(fila)

    def _crear_bloque_info(self, grid, fila, col, titulo, colspan=1, mostrar_titulo=True):
        cont = QVBoxLayout()
        cont.setSpacing(2)
        if mostrar_titulo:
            lbl_tit = QLabel(titulo)
            lbl_tit.setStyleSheet(ESTILO_DATO_PRINCIPAL_SOLICITUD)
            cont.addWidget(lbl_tit)
        lbl_val = QLabel("-")
        lbl_val.setStyleSheet(ESTILO_TEXTO)
        lbl_val.setWordWrap(True)
        cont.addWidget(lbl_val)
        grid.addLayout(cont, fila, col, 1, colspan)
        return lbl_val

    def _calcular_tiempo_restante(self, fecha_ingreso, condena_anos):
        try:
            ingreso = datetime.strptime(str(fecha_ingreso), "%Y-%m-%d").date()
            anos = float(condena_anos)
            fin = date(int(ingreso.year + anos), ingreso.month, ingreso.day)
        except Exception:
            return "-"

        hoy = date.today()
        if fin <= hoy:
            return "Cumplida"

        dias = (fin - hoy).days
        anos_rest = dias // 365
        meses_rest = (dias % 365) // 30
        return f"{anos_rest} años {meses_rest} meses"

    def _crear_bloque_entrevistas(self):
        self.frame_entrevistas = QFrame()
        self.frame_entrevistas.setObjectName("apartado")
        self.frame_entrevistas.setStyleSheet(ESTILO_APARTADO_FRAME)
        self.layout_entrevistas = QVBoxLayout(self.frame_entrevistas)
        self.layout_entrevistas.setSpacing(8)

        fila_titulo_entrevistas = QHBoxLayout()
        fila_titulo_entrevistas.setContentsMargins(0, 0, 0, 0)
        fila_titulo_entrevistas.setSpacing(8)

        titulo = QLabel("Últimas entrevistas")
        titulo.setStyleSheet(ESTILO_TITULO_APARTADO_SOLICITUD)
        icono_entrevistas = QLabel()
        tam_icono = titulo.fontMetrics().height() + 5
        pixmap = QPixmap("assets/entrevista.png").scaled(
            tam_icono, tam_icono, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        icono_entrevistas.setPixmap(pixmap)
        icono_entrevistas.setFixedSize(tam_icono, tam_icono)
        icono_entrevistas.setAlignment(Qt.AlignCenter)

        fila_titulo_entrevistas.addWidget(icono_entrevistas, alignment=Qt.AlignVCenter)
        fila_titulo_entrevistas.addWidget(titulo, alignment=Qt.AlignVCenter)
        fila_titulo_entrevistas.addStretch()
        self.layout_entrevistas.addLayout(fila_titulo_entrevistas)
        self.layout_entrevistas.addSpacing(8)

        self.layout_contenido.addWidget(self.frame_entrevistas)

    def _crear_bloque_historial(self):
        self.frame_historial = QFrame()
        self.frame_historial.setObjectName("apartado")
        self.frame_historial.setStyleSheet(ESTILO_APARTADO_FRAME)
        self.layout_historial = QVBoxLayout(self.frame_historial)
        self.layout_historial.setSpacing(8)

        fila_titulo_historial = QHBoxLayout()
        fila_titulo_historial.setContentsMargins(0, 0, 0, 0)
        fila_titulo_historial.setSpacing(8)

        titulo = QLabel("Historial de Solicitudes de Permisos")
        titulo.setStyleSheet(ESTILO_TITULO_APARTADO_SOLICITUD)
        icono_historial = QLabel()
        tam_icono = titulo.fontMetrics().height()+ 5
        pixmap = QPixmap("assets/historial.png").scaled(
            tam_icono, tam_icono, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        icono_historial.setPixmap(pixmap)
        icono_historial.setFixedSize(tam_icono, tam_icono)
        icono_historial.setAlignment(Qt.AlignCenter)

        fila_titulo_historial.addWidget(icono_historial, alignment=Qt.AlignVCenter)
        fila_titulo_historial.addWidget(titulo, alignment=Qt.AlignVCenter)
        fila_titulo_historial.addStretch()
        self.layout_historial.addLayout(fila_titulo_historial)
        self.layout_historial.addSpacing(8)

        self.layout_contenido.addWidget(self.frame_historial)

    def _limpiar_items(self, layout):
        while layout.count() > 1:
            item = layout.takeAt(1)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def _iniciales(self, nombre):
        partes = [p for p in str(nombre or "").split() if p]
        if not partes:
            return "--"
        if len(partes) == 1:
            return partes[0][:2].upper()
        return (partes[0][0] + partes[1][0]).upper()

    @staticmethod
    def _normalizar_tipo_solicitud(tipo):
        texto = str(tipo or "").strip().lower()
        mapa_tildes = {
            "medico": "Médico",
            "defuncion": "Defunción",
            "juridico": "Jurídico",
        }
        if texto in mapa_tildes:
            return mapa_tildes[texto]
        return texto.capitalize() if texto else "-"

    def cargar_perfil(self, interno, entrevistas, solicitudes):
        self.lbl_nombre.setText(str(getattr(interno, "nombre", "") or "-"))
        self.lbl_rc.setText(f"RC-{getattr(interno, 'num_RC', '-')}")
        self.lbl_avatar.setText(self._iniciales(getattr(interno, "nombre", "")))

        self.lbl_lugar_nac_val.setText(f"{getattr(interno, 'lugar_nacimiento', '') or '-'}")
        self.lbl_fecha_nac_val.setText(f"{getattr(interno, 'fecha_nac', '') or '-'}")

        contacto = getattr(interno, "nombre_contacto_emergencia", "") or "-"
        relacion = getattr(interno, "relacion_contacto_emergencia", "") or "-"
        numero = getattr(interno, "numero_contacto_emergencia", "") or "-"
        self.lbl_contacto_emer_val.setText(f"{contacto} - {relacion}")
        self.lbl_numero_emer_val.setText(f"{numero}")

        delito = getattr(interno, "delito", "") or "-"
        condena = getattr(interno, "condena", "") or "-"
        fecha_ing = getattr(interno, "fecha_ingreso", "") or "-"
        situacion = getattr(interno, "situacion_legal", "") or "-"
        modulo = getattr(interno, "modulo", "") or "-"

        self.lbl_delito_val.setText(str(delito))
        self.lbl_condena_val.setText(f"{condena} años")
        self.lbl_fecha_ingreso_val.setText(str(fecha_ing))
        self.lbl_tiempo_restante_val.setText(self._calcular_tiempo_restante(fecha_ing, condena))
        self.lbl_situacion_val.setText(str(situacion))
        self.lbl_modulo_val.setText(str(modulo))

        self._pintar_entrevistas(entrevistas or [])
        self._pintar_historial(solicitudes or [])

    def _pintar_entrevistas(self, entrevistas):
        self._limpiar_items(self.layout_entrevistas)
        if not entrevistas:
            vacio = QLabel("No hay entrevistas registradas.")
            vacio.setStyleSheet(ESTILO_DATO_SECUNDARIO_SOLICITUD)
            self.layout_entrevistas.addWidget(vacio)
            return

        for entrevista in entrevistas:            
            id_entrevista, _, fecha, puntuacion, _ = entrevista[:5]
            comentario_prof = entrevista[5] if len(entrevista) > 5 else ""
            nombre_prof = entrevista[6] if len(entrevista) > 6 else ""
            card = QFrame()
            card.setStyleSheet(
                "QFrame { background-color: #F5F5F5; border: 1px solid #D9D9D9; border-radius: 10px; }"
            )
            layout = QVBoxLayout(card)
            layout.setContentsMargins(14, 10, 14, 10)
            layout.setSpacing(4)

            fila_cabecera = QHBoxLayout()
            fila_cabecera.setContentsMargins(0, 0, 0, 0)
            titulo = QLabel(f"Entrevista #{int(id_entrevista):04d}")
            titulo.setStyleSheet(ESTILO_TITULO_ENTREVISTA)
            fecha_lbl = QLabel(str(fecha or "-"))
            fecha_lbl.setStyleSheet(ESTILO_FECHA_ENTREVISTA)
            fila_cabecera.addWidget(titulo)
            fila_cabecera.addStretch()
            fila_cabecera.addWidget(fecha_lbl)

            autor_texto = f"Dr. {nombre_prof}" if str(nombre_prof or "").strip() else "Profesional no asignado"
            autor_lbl = QLabel(autor_texto)
            autor_lbl.setStyleSheet(ESTILO_AUTOR_ENTREVISTA)

            comentario_texto = str(comentario_prof or "").strip() or "Sin comentario de entrevista disponible."
            texto_lbl = QLabel(comentario_texto)
            texto_lbl.setStyleSheet(ESTILO_COMENTARIO_ENTREVISTA)
            texto_lbl.setWordWrap(True)

            fila_pie = QHBoxLayout()
            fila_pie.setContentsMargins(0, 0, 0, 0)
            fila_pie.addStretch()
            puntuacion_txt = "0000" if puntuacion is None else str(puntuacion)
            puntuacion_lbl = QLabel(f"Puntuación: {puntuacion_txt}")
            puntuacion_lbl.setStyleSheet(ESTILO_PUNTUACION_ENTREVISTA)
            fila_pie.addWidget(puntuacion_lbl)

            layout.addLayout(fila_cabecera)
            layout.addWidget(autor_lbl)
            layout.addWidget(texto_lbl)
            layout.addLayout(fila_pie)
            self.layout_entrevistas.addWidget(card)

    def _pintar_historial(self, solicitudes):
        self._limpiar_items(self.layout_historial)
        if not solicitudes:
            vacio = QLabel("No hay solicitudes para este interno.")
            vacio.setStyleSheet(ESTILO_DATO_SECUNDARIO_SOLICITUD)
            self.layout_historial.addWidget(vacio)
            return

        for fila in solicitudes:
            id_solicitud = fila[0]
            estado = str(fila[27] or "").lower()
            estado_txt, color = ESTADOS_SOLICITUD_COLOR.get(estado, ("-", "#D3D3D3"))
            tipo = self._normalizar_tipo_solicitud(fila[2])
            motivo = str(fila[3] or "-")
            fecha = str(fila[6] or "-")

            card = QFrame()
            card.setStyleSheet(
                "QFrame { background-color: #F5F5F5; border: 1px solid #D9D9D9; border-radius: 10px; }"
            )
            lay = QHBoxLayout(card)
            lay.setContentsMargins(12, 10, 12, 10)
            lay.setSpacing(10)

            texto = QVBoxLayout()
            fila_titulo = QHBoxLayout()
            fila_titulo.setContentsMargins(0, 0, 0, 0)            
            titulo = QLabel(f"{tipo} #{id_solicitud}")
            titulo.setStyleSheet(ESTILO_TITULO_ENTREVISTA)                    
            fila_titulo.addWidget(titulo)
            fila_titulo.addSpacing(8)           
            fila_titulo.addStretch()

            lbl_motivo = QLabel(motivo)
            lbl_motivo.setStyleSheet(ESTILO_COMENTARIO_ENTREVISTA)
            lbl_motivo.setWordWrap(True)
            texto.addLayout(fila_titulo)
            texto.addWidget(lbl_motivo)

            lateral = QVBoxLayout()
            lbl_fecha = QLabel(fecha)
            lbl_fecha.setStyleSheet(ESTILO_FECHA_ENTREVISTA)
            lbl_fecha.setAlignment(Qt.AlignRight)
            badge = QLabel(estado_txt)
            badge.setAlignment(Qt.AlignCenter)
            badge.setStyleSheet(
                f"background-color: {color}; color: #1A1A1A; border-radius: 8px; padding: 2px 10px; font-size: 9pt;"
            )
            lateral.addWidget(lbl_fecha)
            lateral.addWidget(badge)
            lateral.addStretch()

            lay.addLayout(texto, 1)
            lay.addLayout(lateral)
            self.layout_historial.addWidget(card)
