import getpass
import psycopg2

# Pega o user
current_user = getpass.getuser()

#FAZER VERIFICAÇÃO SE EU PASSAR NULO

cur_password = getpass.getpass("Senha do PostgreSQL: ") # pra pegar a senha do user
print(f"Tentando conectar como: {current_user}")

try:
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        user=current_user,
        password=cur_password,
        dbname="postgres"
    )
    conn.autocommit = True
    cur = conn.cursor()
    print("Conexão bem-sucedida!")
except psycopg2.Error as e:
    print("Erro ao conectar:", e)
