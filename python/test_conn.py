import psycopg2
import sys
import getpass
import os
import subprocess
import shutil


caminho_script = '../schema.sql'

caminho_psql = shutil.which("psql")
if not caminho_psql:
    print("Erro: 'psql' não encontrado no PATH. Instale o cliente do PostgreSQL ou adicione ao PATH.")
    sys.exit(1)

if not os.path.exists(caminho_script):
    print(f"Erro: arquivo de schema não encontrado em {caminho_script}")
    sys.exit(1)



# Pega o user
host = os.getenv("PGHOST", "localhost")
port = os.getenv("PGPORT", "5432")
user = os.getenv("PGUSER") or getpass.getuser()
db_inicial = os.getenv("PGDATABASE", "postgres")

#FAZER VERIFICAÇÃO SE EU PASSAR NULO
password = os.getenv("PGPASSWORD")
if not password:
    try:
        password = getpass.getpass(f"Senha do PostgreSQL para o usuario {user}: ") # pra pegar a senha do user
        print(f"Tentando conectar como: {user}")
    except (KeyboardInterrupt, EOFError):
        print("Erro na inserção da senha")
        sys.exit(1)

env = os.environ.copy()
env["PGPASSWORD"] = password

cmd = [
        caminho_psql,
        "-h", host,
        "-p", port,
        "-U", user,
        "-d", db_inicial,
        "-v", "ON_ERROR_STOP=1",
        "-f", caminho_script,
    ]

print(f"Executando schema via psql:\n  Host={host} Port={port} User={user} DB inicial={db_inicial}\n  Arquivo={caminho_script}")
try:
    subprocess.run(cmd, check=True, env=env, text=True, capture_output=True)
    print("script criado!!")
except subprocess.CalledProcessError as e:
    print(f"Erro: {e}")
    sys.exit(e.returncode)

#colocar o comando \copy nas requisções, para gerar o csv



