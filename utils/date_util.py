
from datetime import datetime, timedelta
from typing import Optional, Tuple


def _format_period(month: int, year: int) -> str:
    months_es = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]
    return f"{months_es[month - 1]} del {year}"

def parse_date(date_string):
    """Convierte una cadena de fecha en un objeto datetime."""
    try:
        return datetime.strptime(date_string, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Formato de fecha inválido. Usa YYYY-MM-DD.")

def resolve_period(
        since:Optional[str] = None,
        until:Optional[str] = None,
        days:Optional[int] = None
    )-> Tuple[int, int]:
    """Determina el período de tiempo a partir de las opciones proporcionadas."""
    if since:
        dt = datetime.strptime(since, "%Y-%m-%d")
        return dt.month, dt.year

    if until:
        dt = datetime.strptime(until, "%Y-%m-%d")
        return dt.month, dt.year
    
    dt = datetime.now() - timedelta(days=days)
    return dt.month, dt.year
