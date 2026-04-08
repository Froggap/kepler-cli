
from datetime import datetime

def parse_date(date_string):
    """Convierte una cadena de fecha en un objeto datetime."""
    try:
        return datetime.strptime(date_string, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Formato de fecha inválido. Usa YYYY-MM-DD.")