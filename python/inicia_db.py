import sys
import getpass
import os
import shutil

from utils import executar_processo

caminho_script = '../schema.sql'


def verificar_e_pegar_executavel_psql():
    caminho_psql = shutil.which("psql")
    if not caminho_psql:
        print("Erro: 'psql' não encontrado no PATH. Instale o cliente do PostgreSQL ou adicione ao PATH.")
        sys.exit(1)
    return caminho_psql

def verificar_caminho_script():
    if not os.path.exists(caminho_script):
        print(f"Erro: arquivo de schema não encontrado em {caminho_script}")
        sys.exit(1)

def pegar_comando_e_env():


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

    psql = verificar_e_pegar_executavel_psql()

    cmd = [
            psql,
            "-h", host,
            "-p", port,
            "-U", user,
            "-d", db_inicial,
            "-v", "ON_ERROR_STOP=1",
            "-f", caminho_script,
        ]

    return cmd,env


def rodar_script():
    cmd,env = pegar_comando_e_env()
    executar_processo(cmd,env)

if __name__ == "__main__":
    rodar_script()

#colocar o comando \copy nas requisções, para gerar o csv



