import os
import subprocess
import sys

from utils import run
from main import DBNAME
OUTDIR = "../data"


def lista_tabelas(env):
	result = subprocess.run(["psql", "-d", DBNAME, "-At",
			   "-c","SELECT tablename FROM pg_tables WHERE schemaname='public';"], env=env, text=True, capture_output=True)
	linhas = result.stdout.split()
	print(linhas)
	return linhas

def e(env):
	lista = lista_tabelas(env)
	#if not lista:
	#	print("Erro ao listar as tabelas")
	#	sys.exit(1)

	print("Gerando os CSV...")
	for tabela in lista:
		run(["psql", "-d", DBNAME,
	   "-c", f"\copy (SELECT * FROM {tabela}) TO {OUTDIR}/{tabela}.csv WITH (FORMAT CSV, HEADER);"], env)
	print(f"CSV gerados na pasta {OUTDIR}")


if __name__ == "__main__":
	env = os.environ.copy()
	e(env)







