## criar as funções que geram os relatorios.
# relacionar isso com o arquivo de conexão com o banco
# eu chamo a função, que retorna o csv então gero o relatório

#nas funções, verificar se o csv existe senão fazer a querry para gerar o csv

import pandas as pd
import os

#Análise de performance de instrutores
def relatorio_instrutores():
	print("relatorio deles")
	caminho_csv_instrutores = "../data/instrutores.csv"
	if not os.path.exists(caminho_csv_instrutores):
		print("csv dos instrutores não encontrado")
	df = pd.read_csv(caminho_csv_instrutores)
	print(df)



def printa():
	print("TA AQUI TEU RELATÓRIO")

if __name__ == "__main__":
	relatorio_instrutores()
