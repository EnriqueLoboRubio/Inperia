import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).resolve().parents[1] / "db" / "database.db"
ESTADO_SIN_EVALUACION = "sin evaluación"


def resetear_evaluacion_entrevistas(db_path=DB_PATH):
    conexion = sqlite3.connect(db_path)
    cursor = conexion.cursor()

    try:
        cursor.execute(
            """
            UPDATE entrevistas
            SET puntuacion_ia = NULL,
                puntuacion_profesional = NULL,
                estado_evaluacion_ia = ?
            """,
            (ESTADO_SIN_EVALUACION,),
        )

        cursor.execute(
            """
            UPDATE respuestas
            SET nivel_ia = NULL,
                analisis_ia = NULL,
                nivel_profesional = NULL
            """
        )

        cursor.execute("DELETE FROM comentarios_ia_ent")
        cursor.execute("DELETE FROM comentarios_entrevista_mensajes")
        cursor.execute("DELETE FROM comentarios_pre")

        cursor.execute(
            """
            UPDATE solicitudes
            SET estado = 'pendiente',
                conclusiones_profesional = NULL
            WHERE id IN (
                SELECT DISTINCT id_solicitud
                FROM entrevistas
                WHERE id_solicitud IS NOT NULL
            )
            """
        )

        conexion.commit()
    finally:
        conexion.close()


def main():
    resetear_evaluacion_entrevistas()
    print(f"Evaluacion de entrevistas reseteada en: {DB_PATH}")


if __name__ == "__main__":
    main()
