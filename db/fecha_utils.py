from datetime import date, datetime


_FORMATOS_FECHA = (
    "%Y-%m-%d",
    "%d/%m/%Y",
    "%d-%m-%Y",
    "%Y/%m/%d",
    "%Y-%m-%d %H:%M",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%dT%H:%M",
    "%Y-%m-%dT%H:%M:%S",
)


def normalizar_fecha(fecha):
    """
    Devuelve la fecha en formato YYYY-MM-DD.
    Acepta date/datetime o strings en formatos comunes heredados.
    """
    if fecha is None:
        return None

    if isinstance(fecha, datetime):
        return fecha.date().isoformat()

    if isinstance(fecha, date):
        return fecha.isoformat()

    texto = str(fecha).strip()
    if not texto:
        return None

    # Intenta ISO (incluye casos con hora y separador 'T').
    try:
        return datetime.fromisoformat(texto.replace("Z", "+00:00")).date().isoformat()
    except ValueError:
        pass

    for formato in _FORMATOS_FECHA:
        try:
            return datetime.strptime(texto, formato).date().isoformat()
        except ValueError:
            continue

    raise ValueError(f"Formato de fecha no valido: {fecha}. Usa YYYY-MM-DD.")
