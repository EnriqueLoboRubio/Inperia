from PyQt5.QtCore import QStandardPaths
from PyQt5.QtWidgets import QFileDialog

from db.csv_db import (
    exportar_base_datos_a_csv,
    importar_base_datos_desde_csv,
    obtener_resumen_csv,
)


class AdministradorDatosController:
    """
    Controlador para la gestión de importación y exportación de datos del administrador.
    """

    def __init__(self, controlador):
        self.controlador = controlador

    def mostrar_pantalla_datos(self):
        pantalla = self.controlador.ventana_administrador.pantalla_datos
        resumen = obtener_resumen_csv()
        lineas = [
            f"Base de datos activa: {resumen.get('ruta_db', '-')}",
            "",
            "Tablas disponibles para CSV:",
        ]

        for tabla in resumen.get("tablas", []):
            lineas.append(f"- {tabla}")
        if not resumen.get("tablas"):
            lineas.append("- No hay tablas exportables.")

        pantalla.establecer_estado(
            "Exporta todas las tablas a una carpeta o importa una copia CSV existente."
        )
        pantalla.establecer_registro(lineas)
        self.controlador.ventana_administrador.stacked_widget.setCurrentWidget(pantalla)
        self.controlador.ventana_administrador.establecer_titulo_pantalla("Datos")

    def exportar_bd_csv(self):
        carpeta = QFileDialog.getExistingDirectory(
            self.controlador.ventana_administrador,
            "Seleccionar carpeta para exportar CSV",
            QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation),
        )

        if not carpeta:
            return

        try:
            resumen = exportar_base_datos_a_csv(carpeta)
        except Exception as e:
            self.controlador.ventana_administrador.pantalla_datos.establecer_estado(
                "La exportación no se ha completado."
            )
            self.controlador.msg.mostrar_advertencia(
                "Error al exportar",
                f"No se pudo exportar la base de datos a CSV:\n{str(e)}",
            )
            return

        lineas = [f"Exportación completada en: {carpeta}", ""]
        total_filas = 0
        for item in resumen:
            total_filas += int(item.get("filas", 0) or 0)
            lineas.append(f"- {item.get('tabla')}: {item.get('filas', 0)} filas")

        lineas.append("")
        lineas.append(f"Total de filas exportadas: {total_filas}")
        self.controlador.ventana_administrador.pantalla_datos.establecer_estado(
            "Exportación completada correctamente."
        )
        self.controlador.ventana_administrador.pantalla_datos.establecer_registro(lineas)
        self.controlador.msg.mostrar_mensaje(
            "Exportación completada",
            f"Se han generado los CSV en:\n{carpeta}",
        )

    def importar_bd_csv(self):
        confirmar = self.controlador.msg.mostrar_confirmacion(
            "Importar base de datos",
            "Esta acción reemplazará los datos actuales por los contenidos en los CSV seleccionados.\n"
            "¿Desea continuar?",
        )
        if not confirmar:
            return

        carpeta = QFileDialog.getExistingDirectory(
            self.controlador.ventana_administrador,
            "Seleccionar carpeta con CSV",
            QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation),
        )
        if not carpeta:
            return

        try:
            resumen = importar_base_datos_desde_csv(carpeta)
        except Exception as e:
            self.controlador.ventana_administrador.pantalla_datos.establecer_estado(
                "La importación no se ha completado."
            )
            self.controlador.msg.mostrar_advertencia(
                "Error al importar",
                f"No se pudo importar la base de datos desde CSV:\n{str(e)}",
            )
            return

        lineas = [f"Importación completada desde: {carpeta}", ""]
        total_filas = 0
        for item in resumen:
            total_filas += int(item.get("filas", 0) or 0)
            lineas.append(f"- {item.get('tabla')}: {item.get('filas', 0)} filas")

        lineas.append("")
        lineas.append(f"Total de filas importadas: {total_filas}")
        self.controlador.ventana_administrador.pantalla_datos.establecer_estado(
            "Importación completada correctamente."
        )
        self.controlador.ventana_administrador.pantalla_datos.establecer_registro(lineas)
        self.controlador.msg.mostrar_mensaje(
            "Importación completada",
            "La base de datos se ha actualizado desde los CSV seleccionados.",
        )
