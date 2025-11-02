# modules/utils/formatters.py
import math

def fmt_currency(value):
    """Formata um valor numérico como moeda brasileira (R$)."""
    if value is None or math.isnan(value):
        return "R$ 0,00"
    try:
        # A lógica de substituição garante o formato correto para pt-BR
        return f"R$ {float(value):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except (ValueError, TypeError):
        return "R$ 0,00"

def fmt_age(value):
    """Formata um valor numérico como idade."""
    if value is None or math.isnan(value):
        return "—"
    return f"{float(value):.1f} anos"

def fmt_rating(value):
    """Formata um valor numérico como uma avaliação de 5 estrelas."""
    if value is None or math.isnan(value):
        return "—"
    return f"{float(value):.1f} / 5 ★"