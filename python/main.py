import subprocess
import sys
import os
from pathlib import Path

from inicia_db import rodar_script
from csv_para_sql import read_csv_to_sql
from utils import run

INPATH = "out_csv"
DBNAME = "edutech"  # ajuste se necessário
# tabelas para gerar INSERTs a partir dos CSVs em out_csv/
TABELAS_PADRAO = ["alunos","instrutores", "categorias", "cursos", "categorias_cursos", "modulos",
                  "aulas", "matriculas", "progresso_aulas", "avaliacoes"]





def existe_arquivo(nome):
    return Path(nome).exists()


def main_admin(env):
    while True:
        print("MENU")
        print("DIGITE UMA OPÇÃO:")
        print("1: GERAR DADOS/CSV")
        print("2: VALIDAR CSV")
        print("3: IMPORTAR CSV (CSV -> SQL -> APLICAR NO BANCO)")
        print("4: EXPORTAR CSV (CSV -> SQL -> APLICAR NO BANCO)")
        print("5: PROCESSAR RELATÓRIOS + EXEMPLO DE QUERY")
        print("6: SAIR")
        try:
            resposta_usuario = int(input("> ").strip())
            os.system('clear')
        except (TypeError, KeyboardInterrupt, ValueError):
            print("insira um numero valido")
            continue

        if resposta_usuario == 1:
            if existe_arquivo("gerar_dados.py"):
                run(["python3", "gerar_dados.py"], env)
            else:
                print("Arquivo gerar_dados.py não encontrado; pulando...")

        elif resposta_usuario == 2:
            if existe_arquivo("validador_csv.py"):
                run(["python3", "validador_csv.py"], env)
            else:
                print("Arquivo validador_csv.py não encontrado; pulando...")

        elif resposta_usuario == 3:
            if not Path(INPATH).exists():
                print(f"Pasta {INPATH} não encontrada. Crie/importe seus CSVs antes.")
                continue

            print("Gerando ../script.sql a partir dos CSVs...")
            try:
                read_csv_to_sql(TABELAS_PADRAO)
            except Exception as e:
                print(f"Falha ao gerar script.sql: {e}")
                continue

            script_path = Path("../script.sql")
            if not script_path.exists():
                print("script.sql não encontrado após a geração.")
                continue

            print("Aplicando script.sql no banco...")
            run(["psql", "-d", DBNAME, "-f", str(script_path)], env)

        elif resposta_usuario == 4:
            run(["python3", "exportar_csv.py"], env)

        elif resposta_usuario == 5:
            if existe_arquivo("processador_relatorios.py"):
                 run(["python3", "processador_relatorios.py"], env)
            else:
                print("Arquivo processador_relatorios.py não encontrado; pulando...")
            run(["psql", "-d", DBNAME, "-c", "SELECT * FROM ordem_pagamentos LIMIT 5;"], env)

        elif resposta_usuario == 6:
            print("Saindo...")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    print("BEM VINDO!!")
    print("Iniciando o banco de dados (aplicando schema.sql)...")
    env, creds = rodar_script(criar_pgpass=False)

    # Refina o env para todas as chamadas subsequentes (Opção A)
    env = os.environ.copy() | {
        "PGPASSWORD": creds["password"],
        "PGUSER": creds["user"],
        "PGHOST": creds["host"],
        "PGPORT": creds["port"],
    }

    # segue fluxo normal do programa, sem novos prompts de senha
    main_admin(env)
