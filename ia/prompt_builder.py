from db.pregunta_db import obtener_preguntas_como_diccionario
from db.prompt_db import obtener_prompt_activo_por_pregunta


class PromptBuilder:
    def __init__(self):
        self._preguntas = obtener_preguntas_como_diccionario()

    def construir_prompt(self, id_pregunta, respuesta):
        pregunta_id = int(id_pregunta)
        datos_pregunta = self._preguntas.get(str(pregunta_id), {})
        texto_pregunta = str(datos_pregunta.get("texto", "") or "").strip()
        plantilla = obtener_prompt_activo_por_pregunta(pregunta_id)

        if plantilla and str(plantilla.get("plantilla", "")).strip():
            prompt = self._renderizar_plantilla(
                plantilla=str(plantilla["plantilla"]),
                pregunta=texto_pregunta,
                respuesta=str(respuesta or "").strip(),
            )
            return self._anadir_instruccion_json_estricta(prompt)

        return (
            "Eres un asistente experto en evaluacion penitenciaria.\n"
            f"Pregunta: {texto_pregunta}\n"
            f"Respuesta del interno: {str(respuesta or '').strip()}\n"
            "Devuelve solo JSON con este formato exacto: "
            '{"nivel": 0, "analisis": "motivo breve y claro"}'
        )

    def construir_prompt_conclusion_entrevista(self, entrevista, resultados):
        lineas_entrevista = []
        for item in list(entrevista or []):
            id_pregunta = int(item.get("id_pregunta", 0) or 0)
            pregunta = str(item.get("pregunta", "") or "").strip()
            respuesta = str(item.get("respuesta", "") or "").strip()
            lineas_entrevista.append(
                f"Pregunta {id_pregunta}: {pregunta}\nRespuesta {id_pregunta}: {respuesta}"
            )

        lineas_resultados = []
        for item in list(resultados or []):
            id_pregunta = int(item.get("id_pregunta", 0) or 0)
            nivel = int(item.get("nivel", 0) or 0)
            justificacion = str(item.get("justificacion", "") or "").strip()
            lineas_resultados.append(
                f"Pregunta {id_pregunta}: nivel {nivel}. Justificacion: {justificacion}"
            )

        return (
            "Eres un asistente experto en evaluación penitenciaria.\n"
            "Tu tarea es identificar solo las causas principales que explican la puntuación global de la entrevista.\n"
            "No menciones porcentaje, puntuación numérica ni tipo de riesgo.\n"
            "No repitas todas las preguntas. Sintetiza solo los aspectos más relevantes.\n"
            "Responde exclusivamente con JSON válido en una sola línea.\n"
            'Formato exacto esperado: {"causas": ["causa breve 1", "causa breve 2", "causa breve 3"]}\n'
            "Debe haber entre 2 y 4 causas, redactadas de forma breve y clara.\n"
            "No uses markdown ni añadas texto fuera del JSON.\n\n"
            "ENTREVISTA COMPLETA:\n"
            f"{chr(10).join(lineas_entrevista)}\n\n"
            "RESULTADOS DEL ANALISIS POR PREGUNTA:\n"
            f"{chr(10).join(lineas_resultados)}"
        )

    @staticmethod
    def _renderizar_plantilla(plantilla, pregunta, respuesta):
        texto = PromptBuilder._normalizar_plantilla(plantilla)
        texto = texto.replace("{pregunta}", str(pregunta or "").strip())
        texto = texto.replace("{respuesta}", str(respuesta or "").strip())
        return texto

    @staticmethod
    def _normalizar_plantilla(plantilla):
        texto = str(plantilla or "")
        texto = (
            texto.replace("â€œ", '"')
            .replace("â€", '"')
            .replace("â€˜", "'")
            .replace("â€™", "'")
        )

        if "{pregunta}" not in texto and texto.count("{respuesta}") >= 2:
            texto = texto.replace("{respuesta}", "{pregunta}", 1)

        return texto

    @staticmethod
    def _anadir_instruccion_json_estricta(prompt):
        sufijo = (
            "\n\nINSTRUCCION FINAL OBLIGATORIA:\n"
            'Responde exclusivamente con JSON valido en una sola linea.\n'
            'Formato exacto esperado: {"nivel": 0, "analisis": "motivo breve y claro"}\n'
            'No uses markdown, no uses comillas tipograficas, no anadas texto fuera del JSON.'
        )
        return f"{str(prompt or '').rstrip()}{sufijo}"
