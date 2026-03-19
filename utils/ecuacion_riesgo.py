import math

from db.riesgo_ponderacion_db import obtener_ponderaciones_riesgo_como_diccionario


TERMINO_INDEPENDIENTE_RIESGO = -3.238
ESCALA_RIESGO = 1000.0
TOTAL_VARIABLES_RIESGO = 10


def obtener_ponderaciones_riesgo():
    ponderaciones = obtener_ponderaciones_riesgo_como_diccionario(force_refresh=False)
    if not ponderaciones:
        raise ValueError("No hay ponderaciones de riesgo cargadas en memoria.")
    return ponderaciones


def normalizar_niveles_riesgo(niveles, total_variables=TOTAL_VARIABLES_RIESGO):
    lista = list(niveles or [])
    if len(lista) != int(total_variables):
        raise ValueError(f"Se esperaban {int(total_variables)} niveles de riesgo y se recibieron {len(lista)}.")

    ponderaciones = obtener_ponderaciones_riesgo()
    normalizados = []
    for indice, nivel in enumerate(lista, start=1):
        try:
            nivel_int = int(nivel)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"El nivel de la pregunta {indice} no es valido: {nivel!r}") from exc

        ponderaciones_pregunta = ponderaciones.get(indice, {})
        if nivel_int not in ponderaciones_pregunta:
            raise ValueError(
                f"El nivel {nivel_int} no tiene ponderacion definida para la pregunta {indice}."
            )
        normalizados.append(nivel_int)
    return normalizados


def convertir_niveles_a_valores_riesgo(niveles, total_variables=TOTAL_VARIABLES_RIESGO):
    niveles_normalizados = normalizar_niveles_riesgo(niveles, total_variables=total_variables)
    ponderaciones = obtener_ponderaciones_riesgo()
    return [ponderaciones[indice][nivel] for indice, nivel in enumerate(niveles_normalizados, start=1)]


def calcular_x_riesgo_desde_valores(valores, termino_independiente=TERMINO_INDEPENDIENTE_RIESGO):
    return float(termino_independiente) + sum(float(valor) for valor in valores)


def calcular_x_riesgo(niveles, termino_independiente=TERMINO_INDEPENDIENTE_RIESGO):
    valores = convertir_niveles_a_valores_riesgo(niveles)
    return calcular_x_riesgo_desde_valores(valores, termino_independiente=termino_independiente)


def calcular_puntuacion_total_riesgo(
    niveles,
    termino_independiente=TERMINO_INDEPENDIENTE_RIESGO,
    escala=ESCALA_RIESGO,
    decimales=2,
):
    x = calcular_x_riesgo(niveles, termino_independiente=termino_independiente)
    exp_x = math.exp(x)
    riesgo = (exp_x / (1.0 + exp_x)) * float(escala)
    return round(riesgo, int(decimales))


def extraer_niveles_riesgo_desde_resultados(resultados, atributo_valor="nivel", total_variables=TOTAL_VARIABLES_RIESGO):
    niveles_por_pregunta = {}
    for resultado in resultados or []:
        try:
            id_pregunta = int(getattr(resultado, "id_pregunta"))
        except (AttributeError, TypeError, ValueError) as exc:
            raise ValueError("Cada resultado debe incluir un id_pregunta numerico.") from exc

        if not 1 <= id_pregunta <= int(total_variables):
            raise ValueError(f"El id_pregunta {id_pregunta} esta fuera del rango 1-{int(total_variables)}.")

        if not hasattr(resultado, atributo_valor):
            raise ValueError(f"Cada resultado debe incluir el atributo {atributo_valor!r}.")

        niveles_por_pregunta[id_pregunta] = getattr(resultado, atributo_valor)

    if len(niveles_por_pregunta) != int(total_variables):
        raise ValueError(
            f"Se esperaban resultados para {int(total_variables)} variables y se recibieron {len(niveles_por_pregunta)}."
        )

    return [niveles_por_pregunta[indice] for indice in range(1, int(total_variables) + 1)]


def calcular_puntuacion_total_desde_resultados(
    resultados,
    atributo_valor="nivel",
    termino_independiente=TERMINO_INDEPENDIENTE_RIESGO,
    escala=ESCALA_RIESGO,
    decimales=2,
):
    niveles = extraer_niveles_riesgo_desde_resultados(resultados, atributo_valor=atributo_valor)
    return calcular_puntuacion_total_riesgo(
        niveles,
        termino_independiente=termino_independiente,
        escala=escala,
        decimales=decimales,
    )


def calcular_puntuacion_total_ia(niveles):
    return calcular_puntuacion_total_riesgo(niveles)


def calcular_puntuacion_total_profesional(niveles):
    return calcular_puntuacion_total_riesgo(niveles)
