#!/usr/bin/python3
# gerador_dados.py
import csv
import random
from datetime import datetime, timedelta, date
from faker import Faker

# usar o NFKD - Normal Form Decomposition, para remover os acentos das palavras
import unicodedata


from utils import garantir_pasta, escolha_ponderada


def remover_acentos(texto):
    """Remove acentos e cedilhas de uma string usando unicodedata."""
    return "".join(
        c for c in unicodedata.normalize("NFKD", texto)
        if not unicodedata.combining(c)
    )

fake = Faker("pt_BR")
random.seed(42)
Faker.seed(42)

# ---------- CONFIG ----------
OUTDIR = "out_csv"
QT = {
    "alunos": 300,
    "instrutores": 25,
    "categorias": 12,
    "cursos": 80,
    "modulos_por_curso": (3, 6),     # min, max
    "aulas_por_modulo": (4, 8),      # min, max
    "matriculas": 600,
    "avaliacoes_pct": 0.55,          # % das matrículas com avaliações
}
NIVEIS = ["iniciante", "intermediario", "avançado"]
TIPOS_AULA = ["video", "texto", "quiz"]
ESPECIALIDADES = [
    "Python", "SQL", "Data Science", "Machine Learning", "Excel & BI",
    "Desenvolvimento Web", "UI/UX", "Redes", "Segurança da Informação",
    "Gestão de Projetos", "Marketing Digital", "NoSQL", "Cloud"
]
CATEGORIAS_BASE = [
    "Programação", "Dados", "Cloud", "Segurança", "Gestão", "Marketing",
    "Web", "UX/UI", "Finanças", "Produtividade", "NoSQL", "Excel & BI"
]

HOJE = datetime.now()

# ---------- HELPERS ----------
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

# ---------- GERADORES ----------
def gerar_alunos(quantidade):
    alunos = []
    emails = set()
    for i in range(1, quantidade + 1):
        nome = f"{fake.first_name()} {fake.last_name()}"
        # garantir unicidade simples
        base = f"{nome.lower().replace(' ', '')}{i}"
        base_normalizada = remover_acentos(base)
        email = f"{base_normalizada}@mail.com"
        while email in emails:
            email = f"{base}{random.randint(1,999)}@mail.com"
        emails.add(email)
        alunos.append({
            "id": i,
            "nome": nome,
            "email": email,  # citext no banco cuida de case-insensitive
            "data_nascimento": idade_min_max().isoformat(),
            "data_cadastro": dt_ultimos_2_anos().strftime("%Y-%m-%d %H:%M:%S"),
        })
    return alunos

def gerar_instrutores(quantidade):
    instrutores = []
    emails = set()
    for i in range(1, quantidade + 1):
        nome = f"{fake.first_name()} {fake.last_name()}"
        base = f"{nome.lower().replace(' ', '')}{i}"
        base_normalizada = remover_acentos(base)
        email = f"{base_normalizada}@edutech.com"
        while email in emails:
            email = f"{base}{random.randint(1,999)}@edutech.com"
        emails.add(email)
        esp = random.choice(ESPECIALIDADES)
        biografia = fake.text(max_nb_chars=280).replace("\n", " ")
        cadastro = dt_ultimos_2_anos()
        ultima_alt = cadastro + timedelta(days=random.randint(0, 60))
        if ultima_alt > HOJE:
            ultima_alt = HOJE
        instrutores.append({
            "id": i,
            "nome": nome,
            "email": email,
            "especialidade": esp,
            "biografia": biografia,
            "data_cadastro": cadastro.strftime("%Y-%m-%d %H:%M:%S"),
            "ultima_alteracao": ultima_alt.strftime("%Y-%m-%d %H:%M:%S"),
        })
    return instrutores

def gerar_categorias():
    categorias = []
    for i, nome in enumerate(CATEGORIAS_BASE, start=1):
        categorias.append({
            "id": i,
            "nome": nome,
            "descricao": f"Cursos da categoria {nome}"
        })
    return categorias

def gerar_cursos(quantidade, instrutores):
    cursos = []
    usados = set()
    for i in range(1, quantidade + 1):
        instrutor_id = random.choice(instrutores)["id"]
        # título único simples
        titulo = f"{random.choice(['Curso', 'Formação', 'Bootcamp'])} {fake.word().capitalize()} {i}"
        while titulo in usados:
            titulo = f"{random.choice(['Curso', 'Formação'])} {fake.word().capitalize()} {i+random.randint(1,999)}"
        usados.add(titulo)
        desc = fake.sentence(nb_words=12)
        nivel = escolha_ponderada(NIVEIS)
        preco = preco_aleatorio()
        ch = carga_horaria_aleatoria()
        criacao = dt_ultimos_2_anos()
        ultima = criacao + timedelta(days=random.randint(0, 45))
        if ultima > HOJE:
            ultima = HOJE
        cursos.append({
            "id": i,
            "instrutor_id": instrutor_id,
            "titulo": titulo,
            "descricao": desc,
            "nivel": nivel,
            "preco": f"{preco:.2f}",
            "carga_horaria": ch,
            "data_criacao": criacao.strftime("%Y-%m-%d %H:%M:%S"),
            "ultima_alteracao": ultima.strftime("%Y-%m-%d %H:%M:%S"),
        })
    return cursos

def vincular_categorias(cursos, categorias):
    rel = []
    for c in cursos:
        qtd = random.randint(1, 3)
        cats = random.sample(categorias, k=qtd)
        for cat in cats:
            rel.append({"curso_id": c["id"], "categoria_id": cat["id"]})
    # garantir (curso_id, categoria_id) únicos
    vistos = set()
    final = []
    for r in rel:
        k = (r["curso_id"], r["categoria_id"])
        if k not in vistos:
            vistos.add(k)
            final.append(r)
    return final

def gerar_modulos(cursos):
    modulos = []
    mid = 1
    for c in cursos:
        qtd = random.randint(*QT["modulos_por_curso"])
        for ordem in range(1, qtd + 1):
            modulos.append({
                "id": mid,
                "curso_id": c["id"],
                "titulo": f"Módulo {ordem}",
                "ordem": ordem,
                "descricao": fake.sentence(nb_words=10)
            })
            mid += 1
    return modulos

def gerar_aulas(curso_id, quantidade, modulo_id_inicio, modulo_id_fim):
    # função conforme solicitado, mas o gerador global usa abaixo
    aulas = []
    aid = 1
    for _ in range(quantidade):
        modulo_id = random.randint(modulo_id_inicio, modulo_id_fim)
        aulas.append({
            "id": aid,
            "modulo_id": modulo_id,
            "titulo": f"Aula {aid}",
            "ordem_aula": random.randint(1, 12),
            "duracao_minutos": random.randint(5, 25),
            "tipo": random.choice(TIPOS_AULA),
        })
        aid += 1
    return aulas

def gerar_aulas_para_modulos(modulos):
    aulas = []
    aid = 1
    for m in modulos:
        qtd = random.randint(*QT["aulas_por_modulo"])
        for ordem in range(1, qtd + 1):
            aulas.append({
                "id": aid,
                "modulo_id": m["id"],
                "titulo": f"Aula {ordem}",
                "ordem_aula": ordem,
                "duracao_minutos": random.randint(5, 25),
                "tipo": random.choice(TIPOS_AULA),
            })
            aid += 1
    return aulas

def gerar_matriculas(quantidade, alunos, cursos):
    existentes = set()
    matriculas = []
    for i in range(1, quantidade + 1):
        aluno = random.choice(alunos)["id"]
        curso = random.choice(cursos)["id"]
        while (aluno, curso) in existentes:
            aluno = random.choice(alunos)["id"]
            curso = random.choice(cursos)["id"]
        existentes.add((aluno, curso))
        data_m = dt_ultimos_2_anos()
        status = random.choices(
            ["pendente", "ativa", "concluida", "cancelada"],
            weights=[15, 55, 20, 10],
            k=1
        )[0]
        data_conc = None
        if status == "concluida":
            data_conc = (data_m + timedelta(days=random.randint(5, 120)))
            if data_conc > HOJE:
                data_conc = HOJE
        matriculas.append({
            "id": i,
            "aluno_id": aluno,
            "curso_id": curso,
            "data_matricula": data_m.strftime("%Y-%m-%d %H:%M:%S"),
            "status": status,
            "data_conclusao": data_conc.strftime("%Y-%m-%d %H:%M:%S") if data_conc else ""
        })
    return matriculas

def gerar_progresso_aulas(matriculas, aulas):
    progresso = []
    # mapear aulas por curso via modulos
    # (simples: escolher subconjunto de aulas quaisquer para marcar concluído)
    aula_ids = [a["id"] for a in aulas]
    for m in matriculas:
        total = random.randint(3, 12)
        concluidas = random.randint(0, total)
        escolhidas = random.sample(aula_ids, k=total)
        concluidas_ids = set(random.sample(escolhidas, k=concluidas))
        for aid in escolhidas:
            done = aid in concluidas_ids
            data_c = ""
            if done:
                data_c = (datetime.fromisoformat(m["data_matricula"]) +
                          timedelta(days=random.randint(1, 60)))
                if data_c > HOJE:
                    data_c = HOJE
                data_c = data_c.strftime("%Y-%m-%d %H:%M:%S")
            progresso.append({
                "matricula_id": m["id"],
                "aulas_id": aid,
                "concluida": "true" if done else "false",
                "data_conclusao": data_c
            })
    return progresso

def gerar_avaliacoes(matriculas):
    avals = []
    idx = 1
    for m in matriculas:
        if random.random() <= QT["avaliacoes_pct"]:
            avals.append({
                "id": idx,
                "matricula_id": m["id"],
                "nota": random.randint(1, 5),
                "comentario": fake.sentence(nb_words=10),
                "data_avaliacao": dt_ultimos_2_anos().date().isoformat()
            })
            idx += 1
    return avals

# ---------- EXPORT ----------
def _write_csv(path, rows, header):
    if not rows:
        return
    garantir_pasta(OUTDIR)
    with open(f"{OUTDIR}/{path}", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=header)
        w.writeheader()
        w.writerows(rows)

def exportar_para_csv(alunos, instrutores, categorias, cursos,
                      cat_cursos, modulos, aulas, matriculas,
                      progresso, avaliacoes):
    _write_csv("alunos.csv", alunos,
               ["id", "nome", "email", "data_nascimento", "data_cadastro"])
    _write_csv("instrutores.csv", instrutores,
               ["id", "nome", "email", "especialidade", "biografia", "data_cadastro", "ultima_alteracao"])
    _write_csv("categorias.csv", categorias, ["id", "nome", "descricao"])
    _write_csv("cursos.csv", cursos,
               ["id", "instrutor_id", "titulo", "descricao", "nivel", "preco",
                "carga_horaria", "data_criacao", "ultima_alteracao"])
    _write_csv("categorias_cursos.csv", cat_cursos, ["curso_id", "categoria_id"])
    _write_csv("modulos.csv", modulos, ["id", "curso_id", "titulo", "ordem", "descricao"])
    _write_csv("aulas.csv", aulas, ["id", "modulo_id", "titulo", "ordem_aula", "duracao_minutos", "tipo"])
    _write_csv("matriculas.csv", matriculas,
               ["id", "aluno_id", "curso_id", "data_matricula", "status", "data_conclusao"])
    _write_csv("progresso_aulas.csv", progresso,
               ["matricula_id", "aulas_id", "concluida", "data_conclusao"])
    _write_csv("avaliacoes.csv", avaliacoes,
               ["id", "matricula_id", "nota", "comentario", "data_avaliacao"])

# ---------- EXECUÇÃO SIMPLES ----------
if __name__ == "__main__":
    alunos = gerar_alunos(QT["alunos"])
    instrutores = gerar_instrutores(QT["instrutores"])
    categorias = gerar_categorias()
    cursos = gerar_cursos(QT["cursos"], instrutores)
    cat_cursos = vincular_categorias(cursos, categorias)
    modulos = gerar_modulos(cursos)
    aulas = gerar_aulas_para_modulos(modulos)
    matriculas = gerar_matriculas(QT["matriculas"], alunos, cursos)
    progresso = gerar_progresso_aulas(matriculas, aulas)
    avaliacoes = gerar_avaliacoes(matriculas)

    exportar_para_csv(alunos, instrutores, categorias, cursos,
                      cat_cursos, modulos, aulas, matriculas,
                      progresso, avaliacoes)
    print(f"✅ CSVs gerados em: {OUTDIR}/")

