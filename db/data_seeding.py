from db.inicio_preguntas import iniciar_preguntas_seed
from db.inicio_prompts import iniciar_prompts_seed


def ejecutar_data_seeding_inicial():
    """
    Ejecuta seeding idempotente al arrancar la app.
    Solo inserta datos base cuando las tablas estan vacias.
    """
    preguntas_insertadas = iniciar_preguntas_seed(force=False)
    prompts_insertados = iniciar_prompts_seed(force=False)

    return {
        "preguntas_insertadas": int(preguntas_insertadas),
        "prompts_insertados": int(prompts_insertados),
    }
