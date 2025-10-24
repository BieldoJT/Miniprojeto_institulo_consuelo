from datetime import datetime
import os
import random
import re
import subprocess
import sys

# usar o NFKD - Normal Form Decomposition, para remover os acentos das palavras
import unicodedata
from datetime import datetime, timedelta, date

HOJE = datetime.now()

EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

def formatar_dinheiro(valor: float) -> str:
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def calcular_taxa_conclusao(aulas_concluidas: int, total_aulas: int) -> float:
    if total_aulas <= 0:
        return 0.0
    return round((aulas_concluidas / total_aulas) * 100, 2)

def validar_email(email: str) -> bool:
    return EMAIL_REGEX.match(email or "") is not None

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

def dt_ultimos_2_anos():
    dias = random.randint(0, 730)  # 2 anos ~ 730 dias
    segundos = random.randint(0, 86400)
    return HOJE - timedelta(days=dias, seconds=segundos)

def preco_aleatorio():
    # 49,90 a 499,90 (intervalo simples)
    return round(random.uniform(49.9, 499.9), 2)

def carga_horaria_aleatoria():
    return random.randint(6, 80)

def idade_min_max(idade_min=16, idade_max=60):
    anos = random.randint(idade_min, idade_max)
    nasc = date.today() - timedelta(days=int(anos * 365.25))
    # espalhar o dia do ano
    nasc = nasc - timedelta(days=random.randint(0, 364))
    return nasc


def remover_acentos(texto):
    """Remove acentos e cedilhas de uma string usando unicodedata."""
    return "".join(
        c for c in unicodedata.normalize("NFKD", texto)
        if not unicodedata.combining(c))

def executar_processo(cmd, new_env):

    try:
        subprocess.run(cmd, check=True, env=new_env, text=True, capture_output=True)
        print("script criado!!")
    except subprocess.CalledProcessError as e:
        print(f"Erro: { e.stderr}")
        sys.exit(e.returncode)
