from db.entrevista_db import (
    listar_ultimas_entrevistas_por_interno,
    obtener_ultimas_entrevistas_interno,
)
from db.interno_db import encontrar_internos_por_num_rc
from db.solicitud_db import listar_solicitudes_por_interno, listar_solicitudes_profesional
from models.interno import Interno


class ProfesionalInternosController:
    """
    Controlador para la gestión de internos.
    """
    def __init__(self, controlador):
        self.controlador = controlador

    def _cargar_internos_para_solicitudes(self, solicitudes):
        rcs = []
        for solicitud in solicitudes:
            num_rc = getattr(solicitud, "id_interno", None)
            if num_rc is not None:
                rcs.append(num_rc)

        datos_internos = encontrar_internos_por_num_rc(list(set(rcs)))
        internos = []
        for dato in datos_internos:
            internos.append(
                Interno(
                    id_usuario=dato[1],
                    nombre=dato[8],
                    email=dato[9],
                    contrasena=dato[10],
                    rol=dato[11],
                    num_RC=dato[0],
                    situacion_legal=dato[2],
                    delito=dato[3],
                    fecha_nac=dato[5],
                    condena=dato[4],
                    fecha_ingreso=dato[6],
                    modulo=dato[7],
                    lugar_nacimiento=dato[12] if len(dato) > 12 else "",
                    nombre_contacto_emergencia=dato[13] if len(dato) > 13 else "",
                    relacion_contacto_emergencia=dato[14] if len(dato) > 14 else "",
                    numero_contacto_emergencia=dato[15] if len(dato) > 15 else "",
                )
            )
        return internos

    def mostrar_perfil_interno(self, interno):
        self.controlador._vista_origen_perfil_interno = "solicitudes"
        self._abrir_perfil_interno(interno)

    def mostrar_perfil_interno_desde_detalle(self, interno):
        self.controlador._vista_origen_perfil_interno = "detalle_solicitud"
        self._abrir_perfil_interno(interno)

    def mostrar_perfil_interno_desde_internos(self, interno):
        self.controlador._vista_origen_perfil_interno = "internos"
        self._abrir_perfil_interno(interno)

    def _abrir_perfil_interno(self, interno):
        if interno is None:
            return
        entrevistas = listar_ultimas_entrevistas_por_interno(interno.num_RC, limite=5)
        solicitudes = listar_solicitudes_por_interno(interno.num_RC)
        self.controlador.ventana_profesional.pantalla_perfil_interno.cargar_perfil(
            interno=interno,
            entrevistas=entrevistas,
            solicitudes=solicitudes,
        )
        self.controlador.ventana_profesional.mostrar_pantalla_perfil_interno()

    def volver_desde_perfil_interno(self):
        if self.controlador._vista_origen_perfil_interno == "internos":
            self.mostrar_lista_internos_asignados()
            return
        if self.controlador._vista_origen_perfil_interno == "detalle_solicitud":
            self.controlador.ventana_profesional.stacked_widget.setCurrentWidget(
                self.controlador.ventana_profesional.pantalla_detalle_solicitud
            )
            self.controlador.ventana_profesional.establecer_titulo_pantalla("Solicitud")
            return
        self.controlador.recargar_lista_actual()

    def _obtener_interno_de_solicitud(self, solicitud):
        if solicitud is None:
            return None

        candidato = getattr(solicitud, "interno", None)
        if candidato is not None:
            return candidato

        id_interno = getattr(solicitud, "id_interno", None)
        if id_interno is None:
            return None

        internos = self._cargar_internos_para_solicitudes([solicitud])
        return internos[0] if internos else None

    def mostrar_lista_internos_asignados(self):
        if not self.controlador.profesional:
            return

        filas = listar_solicitudes_profesional(self.controlador.profesional.id_usuario)
        if not filas:
            self.controlador.ventana_profesional.pantalla_lista_internos.cargar_datos([])
            self.controlador.ventana_profesional.stacked_widget.setCurrentWidget(
                self.controlador.ventana_profesional.pantalla_lista_internos
            )
            self.controlador.ventana_profesional.establecer_titulo_pantalla("Internos asignados")
            return

        ultima_solicitud_por_rc = {}
        for fila in filas:
            num_rc = fila[1]
            if num_rc not in ultima_solicitud_por_rc:
                ultima_solicitud_por_rc[num_rc] = fila

        datos_internos = encontrar_internos_por_num_rc(list(ultima_solicitud_por_rc.keys()))
        internos = []
        for dato in datos_internos:
            internos.append(
                Interno(
                    id_usuario=dato[1],
                    nombre=dato[8],
                    email=dato[9],
                    contrasena=dato[10],
                    rol=dato[11],
                    num_RC=dato[0],
                    situacion_legal=dato[2],
                    delito=dato[3],
                    fecha_nac=dato[5],
                    condena=dato[4],
                    fecha_ingreso=dato[6],
                    modulo=dato[7],
                    lugar_nacimiento=dato[12] if len(dato) > 12 else "",
                    nombre_contacto_emergencia=dato[13] if len(dato) > 13 else "",
                    relacion_contacto_emergencia=dato[14] if len(dato) > 14 else "",
                    numero_contacto_emergencia=dato[15] if len(dato) > 15 else "",
                )
            )

        internos_ordenados = sorted(internos, key=lambda x: str(getattr(x, "nombre", "")).lower())
        datos_tarjetas = []
        for interno in internos_ordenados:
            entrevistas = obtener_ultimas_entrevistas_interno(interno.num_RC, limite=2)
            ultima_entrevista = entrevistas[0] if entrevistas else None
            entrevista_anterior = entrevistas[1] if len(entrevistas) > 1 else None
            fecha_ult = ultima_entrevista[1] if ultima_entrevista else "-"
            puntuacion = ultima_entrevista[2] if ultima_entrevista else None
            puntuacion_anterior = entrevista_anterior[2] if entrevista_anterior else None
            datos_tarjetas.append(
                {
                    "interno": interno,
                    "id_ultima_entrevista": ultima_entrevista[0] if ultima_entrevista else None,
                    "fecha_ultima_entrevista": fecha_ult,
                    "puntuacion_ia": puntuacion,
                    "tendencia_riesgo": self._calcular_tendencia_riesgo(
                        puntuacion, puntuacion_anterior
                    ),
                }
            )

        pantalla = self.controlador.ventana_profesional.pantalla_lista_internos
        pantalla.cargar_datos(datos_tarjetas)
        self.controlador.ventana_profesional.stacked_widget.setCurrentWidget(pantalla)
        self.controlador.ventana_profesional.establecer_titulo_pantalla("Internos asignados")

    @staticmethod
    def _calcular_tendencia_riesgo(actual, anterior):
        if actual is None or anterior is None:
            return None
        try:
            v_actual = float(actual)
            v_anterior = float(anterior)
        except (TypeError, ValueError):
            return None

        if v_actual > v_anterior:
            return "sube"
        if v_actual < v_anterior:
            return "baja"
        return "igual"
