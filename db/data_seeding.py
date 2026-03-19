from db.inicio_preguntas import iniciar_preguntas_seed
from db.inicio_ponderaciones_riesgo import iniciar_ponderaciones_riesgo_seed
from db.inicio_prompts import iniciar_prompts_seed
from db.riesgo_ponderacion_db import precargar_ponderaciones_riesgo


def ejecutar_data_seeding_inicial():
    """
    Ejecuta seeding idempotente al arrancar la app.
    Solo inserta datos base cuando las tablas estan vacias.
    """
    preguntas_insertadas = iniciar_preguntas_seed(force=False)
    prompts_insertados = iniciar_prompts_seed(force=False)
    ponderaciones_insertadas = iniciar_ponderaciones_riesgo_seed(force=False)
    precargar_ponderaciones_riesgo()

    return {
        "preguntas_insertadas": int(preguntas_insertadas),
        "prompts_insertados": int(prompts_insertados),
        "ponderaciones_riesgo_insertadas": int(ponderaciones_insertadas),
    }
