# utils.py
from datetime import datetime
import hashlib
import os
import random
import re
import secrets

EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

def formatar_dinheiro(valor: float) -> str:
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def calcular_taxa_conclusao(aulas_concluidas: int, total_aulas: int) -> float:
    if total_aulas <= 0:
        return 0.0
    return round((aulas_concluidas / total_aulas) * 100, 2)

def validar_email(email: str) -> bool:
    return EMAIL_REGEX.match(email or "") is not None

def gerar_senha_hash() -> str:
    # simulação para futura API: hash de um token aleatório
    token = secrets.token_hex(16)
    return hashlib.sha256(token.encode()).hexdigest()

def formatar_data(dt) -> str:
    # ISO 8601 (amigável para COPY do PostgreSQL)
    if isinstance(dt, datetime):
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    return str(dt)

def garantir_pasta(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def escolha_ponderada(opcoes):
    # ajuda a variar um pouco sem lógica complexa
    return random.choice(opcoes)
