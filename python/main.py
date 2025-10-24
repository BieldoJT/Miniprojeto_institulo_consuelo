import subprocess
import sys
import os
from inicia_db import rodar_script
from csv_para_sql import read_csv_to_sql
INPATH = "out_csv"

def main_admin():
	while(1):
		print("MENU")
		print("DIGITE USAR OPÇÃO:")
		print("1: GERAR DADOS\n2:VALIDAR CSV\n3:RODAR O SCRIPT\n4:PROCESSAR RELATÓRIOS\n5: SAIR")
		try:
			resposta_usuario = int(input())
			os.system('clear')
		except (TypeError, KeyboardInterrupt, ValueError):
			print("insira um numero valido")
			continue
		if resposta_usuario == 1:
			subprocess.run(["python3", "gerar_dados.py"])
		elif resposta_usuario == 2:
			subprocess.run(["python3", "validador_csv.py"])
		elif resposta_usuario == 3:
			print("Fazer alguma coisa aqui!!")
			continue
		elif resposta_usuario == 4:
			subprocess.run(["python3", "processador_relatorios.py"])
			subprocess.run(["psql","-U", "bieldojt", "-d", "edutech", "-c",
				   "SELECT *FROM alunos"])
		elif resposta_usuario == 5:
			print("Obriado pelo uso!")
			sys.exit(0)

def popula_banco():
	lista_csv = list(["alunos","instrutores", "categorias", "cursos", "categorias_cursos", "modulos", "aulas", "matriculas", "progresso_aulas", "avaliacoes"])
	read_csv_to_sql(lista_csv)
	subprocess.run(["psql","-U", "bieldojt", "-d", "edutech", "-f", "../script.sql"])
	print("todos os insert realizados")





if __name__ == "__main__":
	print("BEM VINDO!!")
	print("Iniciando o banco de dados!")
	rodar_script()
	print("gerando dados...")
	subprocess.run(["python3", "gerar_dados.py"])
	print("populando o banco de dados...")
	popula_banco()



	main_admin()
