import pandas as pd
import numpy as np
import os
from validador_csv import is_float, is_int

INPATH = "out_csv"
def read_csv_to_sql(lista_tabelas):
	with open("../script.sql", 'w') as f:
		for nome_tabela in lista_tabelas:
			path = os.path.join(INPATH, nome_tabela + '.csv')
			if not os.path.exists(path):
				print("erro aqui")
				return 0
			df = pd.read_csv(path, na_values=["nan", "NaN", "NONE", "None", "NULL", "null", ""])
			f.write(f"\n\n-- INSERT DE {nome_tabela.upper()}\n\n")
			f.write(f"INSERT INTO {nome_tabela} VALUES ")
			for index, row in df.iterrows():
				inserts_sql = []
				valores = []
				for v in row.values:
					if str(v) == "default":
						valores.append("NULL")
					elif (is_int(v) or is_float(v)):
						valores.append(str(v))
					# <<< detectar nulos de verdade (NaN/None/NaT) >>>
					else:
						# opcional: escapar aspas simples no texto
						s = str(v).replace("'", "''")
						valores.append(f"'{s}'")
				f.write(f"({', '.join(valores)})")
				if index != len(df.index) - 1:
					f.write(",\n")
				else:
					f.write(";\n")
				valores = []
				print(f"Insert da tabela {nome_tabela}...")
			print(inserts_sql)

