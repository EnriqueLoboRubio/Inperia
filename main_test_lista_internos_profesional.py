import sys
from dataclasses import dataclass

from PyQt5.QtWidgets import QApplication

from gui.pantalla_lista_internos_profesional import PantallaListaInternosProfesional


@dataclass
class InternoMock:
    nombre: str
    num_RC: str
    delito: str
    condena: int
    fecha_ingreso: str


def _datos_mock():
    return [
        {
            "interno": InternoMock("Carlos Romero Diaz", "1001", "Robo con fuerza", 8, "2018-04-12"),
            "fecha_ultima_entrevista": "2026-02-20",
            "puntuacion_global": 903.25,
        },
        {
            "interno": InternoMock("Miguel Santos Pardo", "1002", "Lesiones", 5, "2020-09-03"),
            "fecha_ultima_entrevista": "2026-01-10",
            "puntuacion_global": 946.40,
        },
        {
            "interno": InternoMock("Juan Antonio Ruiz", "1003", "Hurto", 2, "2023-06-29"),
            "fecha_ultima_entrevista": None,
            "puntuacion_global": None,
        },
        {
            "interno": InternoMock("Pedro Moreno Gil", "1004", "Fraude", 6, "2019-11-15"),
            "fecha_ultima_entrevista": "2025-12-18",
            "puntuacion_global": 933.00,
        },
        {
            "interno": InternoMock("Luis Perez Calderon", "1005", "Amenazas", 3, "2024-02-01"),
            "fecha_ultima_entrevista": "2026-03-01",
            "puntuacion_global": 989.30,
        },
        {
            "interno": InternoMock("Rafael Vega Molina", "1006", "Daños", 4, "2021-07-21"),
            "fecha_ultima_entrevista": "2026-02-05",
            "puntuacion_global": 924.10,
        },
    ]


def main():
    app = QApplication(sys.argv)

    pantalla = PantallaListaInternosProfesional()
    pantalla.setWindowTitle("Test - Lista de internos (profesional)")
    pantalla.resize(1280, 760)
    pantalla.cargar_datos(_datos_mock())
    pantalla.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
