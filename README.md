# 🧠 Plataforma de Gerenciamento de Cursos — Guia de Execução

## 🧩 1. Pré-requisitos

- **PostgreSQL instalado** (necessário o cliente `psql`).
  - Teste no terminal:
    ```bash
    psql --version
    ```
- **Usuário do PostgreSQL com permissão de criar banco de dados** (`CREATEDB`):
    ```sql
    ALTER ROLE seu_usuario CREATEDB;
    ```
- **Python 3.10+** (recomendado) e `pip` instalados.

> ⚠️ **Importante:** O projeto usa o `psql` para rodar os scripts SQL. Sem ele configurado no PATH, a inicialização do banco não funcionará.

---

## 📁 2. Estrutura do projeto

```
/python
  main.py
  inicia_db.py
  gerar_dados.py
  exportar_csv.py
  csv_para_sql.py
  validador_csv.py
  processador_relatorios.py
  utils.py
/schema.sql
/dados.sql
/data/               ← pasta de entrada/saída dos CSVs
```

---

## ⚙️ 3. Configurar variáveis de ambiente (opcional)

Você pode definir as credenciais do Postgres para evitar digitar a senha a cada execução:

```bash
export PGHOST=localhost
export PGPORT=5432
export PGUSER=seu_usuario
export PGPASSWORD=sua_senha
export PGDATABASE=postgres
```

> 💡 **Dica:** para evitar digitar senha ao usar o `psql`, configure o arquivo `~/.pgpass`:
> ```
> host:port:database:usuario:senha
> ```

---

## 🐍 4. Instalar dependências do Python

Dentro da pasta `python/`:

```bash
cd python
python3 -m venv .venv
source .venv/bin/activate        # Windows (PowerShell): .venv\Scripts\Activate.ps1
pip install -r ../requirements.txt
```

---

## ▶️ 5. Executar o programa

Rode o programa **a partir da pasta `python/`**:

```bash
cd python
python3 main.py
```

Na primeira execução, o sistema:

1. Cria o banco e aplica o `schema.sql`.
2. Salva temporariamente as credenciais durante a sessão.
3. Exibe o **menu interativo** para gerenciamento do banco e dados.

---

## 📋 6. Menu principal

Ao rodar o `main.py`, você verá:

```
1: GERAR DADOS/CSV
2: VALIDAR CSV
3: IMPORTAR CSV (CSV -> SQL -> APLICAR NO BANCO)
4: EXPORTAR CSV
5: PROCESSAR RELATÓRIOS + EXEMPLOS DE CONSULTAS
6: SAIR
```

### Explicação das opções:

| Opção | Função |
|-------|--------|
| **1** | Gera dados fictícios e salva em `../data/*.csv` |
| **2** | Valida estrutura e integridade dos CSVs |
| **3** | Converte CSVs em `dados.sql` e insere no banco |
| **4** | Exporta todas as tabelas do banco em CSV |
| **5** | Gera relatórios e executa consultas de exemplo |
| **6** | Encerra o programa |

> 💡 O banco padrão é **`edutech`**, configurável em `python/main.py`.
> A pasta padrão dos CSVs é **`../data/`**.

---

## 🔄 7. Fluxos de uso comuns

### 🧱 A) Criar banco do zero
```bash
python3 main.py
# Escolher opções:
1 → 2 → 3 → (opcional 5)
```

### 📤 B) Exportar dados existentes do banco
```bash
python3 main.py
# Escolher opção 4
```

---

## 🚨 8. Erros comuns

| Erro | Solução |
|------|----------|
| `psql: command not found` | Instale o cliente PostgreSQL (`sudo apt install postgresql-client`) |
| `permission denied to create database` | Dê permissão com `ALTER ROLE seu_usuario CREATEDB;` |
| `password authentication failed` | Verifique usuário/senha/arquivo `pg_hba.conf` |
| `connection refused` | Ajuste `PGHOST` e `PGPORT` (padrões: `localhost:5432`) |
| CSV inválido | Use a opção **2 (Validar CSV)** para ver os erros detalhados |

---

## 🧭 9. Comandos rápidos (resumo)

```bash
# Entrar na pasta e ativar venv
cd python
python3 -m venv .venv && source .venv/bin/activate
pip install -r ../requirements.txt

# Configurar variáveis (opcional)
export PGHOST=localhost PGPORT=5432 PGUSER=seu_usuario PGPASSWORD=sua_senha PGDATABASE=postgres

# Executar
python3 main.py
```

---

## ✅ 10. Resultado final

Após seguir os passos acima, o projeto estará pronto para:

- Criar automaticamente o banco e as tabelas (`schema.sql`);
- Gerar dados sintéticos e validá-los;
- Popular o banco a partir dos CSVs;
- Exportar e processar relatórios completos via menu interativo.

---

**Autor:** Projeto Edutech — Sistema de Gerenciamento de Cursos
**Banco:** PostgreSQL
**Execução:** `python3 main.py` (dentro da pasta `python/`)
