from dataclasses import dataclass
from datetime import datetime

from PyQt5.QtCore import QThread, pyqtSignal

from db.comentario_ia_entrevista_db import agregar_comentario_ia
from db.entrevista_db import (
    actualizar_estado_evaluacion_ia_entrevista,
    actualizar_puntuacion_entrevista,
)
from db.pregunta_db import obtener_preguntas_como_diccionario
from db.respuesta_db import actualizar_analisis_ia_respuesta
from ia.ollama_provider import OllamaProvider
from ia.parser_respuesta import parsear_causas_principales_ia, parsear_respuesta_ia
from ia.prompt_builder import PromptBuilder
from utils.ecuacion_riesgo import calcular_puntuacion_total_desde_resultados


BAREMOS_RIESGO = [
    (887.5, "muy bajo", "5 %"),
    (910.0, "bajo", "10 %"),
    (920.0, "bajo", "15 %"),
    (928.0, "normal", "20 %"),
    (932.5, "normal", "25 %"),
    (940.0, "normal", "30 %"),
    (942.5, "normal", "35 %"),
    (945.0, "elevado", "40 %"),
    (947.5, "elevado", "45 %"),
    (955.5, "elevado", "50 %"),
    (959.0, "elevado", "55 %"),
    (962.5, "bastante elevado", "60 %"),
    (966.25, "bastante elevado", "65 %"),
    (970.0, "bastante elevado", "70 %"),
    (977.0, "bastante elevado", "75 %"),
    (985.0, "muy elevado", "80 %"),
    (988.75, "muy elevado", "85 %"),
    (992.5, "muy elevado", "90 %"),
    (996.5, "muy elevado", "95 %"),
]


@dataclass
class ResultadoAnalisisPregunta:
    id_pregunta: int
    nivel: int
    justificacion: str


class AnalisisService:
    def __init__(self, provider=None, prompt_builder=None):
        self.provider = provider or OllamaProvider()
        self.prompt_builder = prompt_builder or PromptBuilder()
        self._preguntas = obtener_preguntas_como_diccionario()

    def analizar_pregunta(self, id_pregunta, respuesta):
        prompt = self.prompt_builder.construir_prompt(id_pregunta, respuesta)
        bruto = self.provider.generar(prompt)
        parseado = parsear_respuesta_ia(bruto)
        return ResultadoAnalisisPregunta(
            id_pregunta=int(id_pregunta),
            nivel=int(parseado["nivel"]),
            justificacion=str(parseado["justificacion"]).strip(),
        )

    def calcular_puntuacion_global(self, resultados):
        if not resultados:
            return -1
        try:
            return calcular_puntuacion_total_desde_resultados(resultados, atributo_valor="nivel")
        except ValueError:
            return -1

    def construir_conclusion_entrevista(self, resultados, preguntas_entrevista, puntuacion):
        causas = self._generar_causas_principales(resultados, preguntas_entrevista)
        return self._formatear_conclusion(puntuacion, causas)

    def _generar_causas_principales(self, resultados, preguntas_entrevista):
        prompt = self.prompt_builder.construir_prompt_conclusion_entrevista(
            entrevista=preguntas_entrevista,
            resultados=[
                {
                    "id_pregunta": int(r.id_pregunta),
                    "nivel": int(r.nivel),
                    "justificacion": str(r.justificacion).strip(),
                }
                for r in list(resultados or [])
            ],
        )
        bruto = self.provider.generar(prompt)
        parseado = parsear_causas_principales_ia(bruto)
        return list(parseado.get("causas", []))

    @staticmethod
    def _clasificar_riesgo_desde_puntuacion(puntuacion):
        try:
            valor = float(puntuacion)
        except (TypeError, ValueError):
            return "-", "-"

        for limite, riesgo, porcentaje in BAREMOS_RIESGO:
            if valor <= limite:
                return porcentaje, riesgo
        return "100 %", "maximo"

    def _construir_contexto_entrevista(self, preguntas):
        contexto = []
        for item in list(preguntas or []):
            id_pregunta = int(item.get("id_pregunta", 0) or 0)
            texto_pregunta = self._preguntas.get(str(id_pregunta), {}).get("texto", "")
            contexto.append(
                {
                    "id_pregunta": id_pregunta,
                    "pregunta": str(texto_pregunta or "").strip(),
                    "respuesta": str(item.get("respuesta", "") or "").strip(),
                }
            )
        return contexto

    def _formatear_conclusion(self, puntuacion, causas):
        porcentaje, riesgo = self._clasificar_riesgo_desde_puntuacion(puntuacion)
        if not causas:
            causas_texto = "no se han podido identificar causas principales."
        else:
            causas_texto = " ".join(
                f"{indice}. {str(causa).strip().rstrip('.')}."
                for indice, causa in enumerate(causas, start=1)
            )
        return (
            f"El resultado obtenido es del {porcentaje}, lo que significa un riesgo {riesgo}. "
            f"Las principales causas son: {causas_texto}"
        )


class HiloAnalisisIA(QThread):
    senal_inicio_pregunta = pyqtSignal(int, str)
    senal_pregunta_analizada = pyqtSignal(object)
    senal_estado_entrevista = pyqtSignal(str)
    senal_analisis_finalizado = pyqtSignal(object)
    senal_error = pyqtSignal(str)

    def __init__(self, id_entrevista, preguntas, analizar_todas=False, parent=None):
        super().__init__(parent)
        self.id_entrevista = int(id_entrevista)
        self.preguntas = list(preguntas or [])
        self.analizar_todas = bool(analizar_todas)
        self.service = AnalisisService()

    def run(self):
        if not self.preguntas:
            self.senal_error.emit("No hay preguntas para analizar.")
            return

        resultados = []
        try:
            actualizar_estado_evaluacion_ia_entrevista(self.id_entrevista, "evaluando")
            self.senal_estado_entrevista.emit("evaluando")

            for item in self.preguntas:
                id_pregunta = int(item.get("id_pregunta"))
                respuesta = str(item.get("respuesta", "") or "").strip()
                self.senal_inicio_pregunta.emit(id_pregunta, "Analizando con IA...")

                if not respuesta:
                    raise RuntimeError(f"La pregunta {id_pregunta} no tiene respuesta.")

                resultado = self.service.analizar_pregunta(id_pregunta, respuesta)
                if not actualizar_analisis_ia_respuesta(
                    self.id_entrevista,
                    resultado.id_pregunta,
                    resultado.nivel,
                    resultado.justificacion,
                ):
                    raise RuntimeError(f"No se pudo guardar el analisis de la pregunta {id_pregunta}.")

                payload = {
                    "id_pregunta": resultado.id_pregunta,
                    "nivel": resultado.nivel,
                    "justificacion": resultado.justificacion,
                }
                resultados.append(resultado)
                self.senal_pregunta_analizada.emit(payload)

            puntuacion = None
            conclusion = None
            fecha_conclusion = None
            if self.analizar_todas:
                puntuacion = self.service.calcular_puntuacion_global(resultados)
                contexto_entrevista = self.service._construir_contexto_entrevista(self.preguntas)
                conclusion = self.service.construir_conclusion_entrevista(
                    resultados=resultados,
                    preguntas_entrevista=contexto_entrevista,
                    puntuacion=puntuacion,
                )
                fecha_conclusion = datetime.now().strftime("%Y-%m-%d")
                actualizar_puntuacion_entrevista(self.id_entrevista, puntuacion)
                agregar_comentario_ia(
                    self.id_entrevista,
                    conclusion,
                    fecha_conclusion,
                )

            actualizar_estado_evaluacion_ia_entrevista(self.id_entrevista, "evaluada")
            self.senal_estado_entrevista.emit("evaluada")
            self.senal_analisis_finalizado.emit(
                {
                    "analizar_todas": self.analizar_todas,
                    "puntuacion_ia": puntuacion,
                    "conclusion_entrevista": conclusion,
                    "fecha_conclusion_ia": fecha_conclusion,
                    "preguntas": [
                        {
                            "id_pregunta": r.id_pregunta,
                            "nivel": r.nivel,
                            "justificacion": r.justificacion,
                        }
                        for r in resultados
                    ],
                }
            )
        except Exception as exc:
            actualizar_estado_evaluacion_ia_entrevista(self.id_entrevista, "sin evaluacion")
            self.senal_estado_entrevista.emit("sin evaluacion")
            self.senal_error.emit(str(exc))
