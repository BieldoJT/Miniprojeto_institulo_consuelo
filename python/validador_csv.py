import csv
import os
from datetime import datetime

from utils import validar_email, garantir_pasta

INPATH =  "../data"
REPORT =  "../data/relatorio_validacao.md"

def ler_csv(nome, obrigatorios=None):
    path = os.path.join(INPATH, nome)
    if not os.path.exists(path):
        return [], []
    with open(path, newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        rows = list(r)
    obrigatorios = obrigatorios or []
    erros = []
    for i, row in enumerate(rows, start=2):  # +1 header, +1 base 1
        for campo in obrigatorios:
            if not str(row.get(campo, "")).strip():
                erros.append(f"{nome}: linha {i} - campo obrigatório vazio: {campo}")
    return rows, erros

def is_int(v):
    try:
        int(str(v))
        return True
    except:
        return False

def is_float(v):
    try:
        float(str(v).replace(",", "."))
        return True
    except:
        return False


def is_data(v, com_tempo=False):
    try:
        if com_tempo:
            datetime.strptime(v, "%Y-%m-%d %H:%M:%S")
        else:
            datetime.strptime(v, "%Y-%m-%d")
        return True
    except:
        return False

def validar():
    garantir_pasta(INPATH)
    rel = []

    # ---- Carregar bases ----
    alunos, e1 = ler_csv("alunos.csv", ["id","nome","email","data_nascimento","data_cadastro"])
    instrutores, e2 = ler_csv("instrutores.csv", ["id","nome","email","especialidade","biografia","data_cadastro","ultima_alteracao"])
    categorias, e3 = ler_csv("categorias.csv", ["id","nome","descricao"])
    cursos, e4 = ler_csv("cursos.csv", ["id","instrutor_id","titulo","descricao","nivel","preco","carga_horaria","data_criacao","ultima_alteracao"])
    cat_cursos, e5 = ler_csv("categorias_cursos.csv", ["curso_id","categoria_id"])
    modulos, e6 = ler_csv("modulos.csv", ["id","curso_id","titulo","ordem","descricao"])
    aulas, e7 = ler_csv("aulas.csv", ["id","modulo_id","titulo","ordem_aula","duracao_minutos","tipo"])
    matriculas, e8 = ler_csv("matriculas.csv", ["id","aluno_id","curso_id","data_matricula","status"])
    progresso, e9 = ler_csv("progresso_aulas.csv", ["matricula_id","aulas_id","concluida"])
    avaliacoes, e10 = ler_csv("avaliacoes.csv", ["id","matricula_id","nota","data_avaliacao"])

    erros = e1+e2+e3+e4+e5+e6+e7+e8+e9+e10

    # ---- Formatos / tipos ----
    for a in alunos:
        if not validar_email(a["email"]):
            erros.append(f"alunos.csv: id {a['id']} - email inválido")
        if not is_data(a["data_nascimento"]):
            erros.append(f"alunos.csv: id {a['id']} - data_nascimento inválida (YYYY-MM-DD)")
        if not is_data(a["data_cadastro"], com_tempo=True):
            erros.append(f"alunos.csv: id {a['id']} - data_cadastro inválida (YYYY-MM-DD HH:MM:SS)")

    for i in instrutores:
        if not validar_email(i["email"]):
            erros.append(f"instrutores.csv: id {i['id']} - email inválido")
        if not is_data(i["data_cadastro"], com_tempo=True):
            erros.append(f"instrutores.csv: id {i['id']} - data_cadastro inválida")
        if not is_data(i["ultima_alteracao"], com_tempo=True):
            erros.append(f"instrutores.csv: id {i['id']} - ultima_alteracao inválida")

    niveis_validos = {"iniciante","intermediario","avançado"}
    for c in cursos:
        if c["nivel"] not in niveis_validos:
            erros.append(f"cursos.csv: id {c['id']} - nivel inválido")
        if not is_float(c["preco"]):
            erros.append(f"cursos.csv: id {c['id']} - preco não numérico")
        else:
            p = float(c["preco"].replace(",", "."))
            if not (49.9 <= p <= 499.9):
                erros.append(f"cursos.csv: id {c['id']} - preco fora do range (49.90 a 499.90)")
        if not is_int(c["carga_horaria"]):
            erros.append(f"cursos.csv: id {c['id']} - carga_horaria não inteiro")
        if not is_data(c["data_criacao"], com_tempo=True):
            erros.append(f"cursos.csv: id {c['id']} - data_criacao inválida")
        if not is_data(c["ultima_alteracao"], com_tempo=True):
            erros.append(f"cursos.csv: id {c['id']} - ultima_alteracao inválida")

    for a in aulas:
        if a["tipo"] not in {"video","texto","quiz"}:
            erros.append(f"aulas.csv: id {a['id']} - tipo inválido")
        if not is_int(a["duracao_minutos"]):
            erros.append(f"aulas.csv: id {a['id']} - duracao_minutos não inteiro")

    for m in matriculas:
        if m["status"] not in {"pendente","ativa","concluida","cancelada"}:
            erros.append(f"matriculas.csv: id {m['id']} - status inválido")
        if not is_data(m["data_matricula"], com_tempo=True):
            erros.append(f"matriculas.csv: id {m['id']} - data_matricula inválida")
        if m["data_conclusao"]:
            if not is_data(m["data_conclusao"], com_tempo=True):
                erros.append(f"matriculas.csv: id {m['id']} - data_conclusao inválida")

    for pr in progresso:
        if pr["concluida"] not in {"true","false"}:
            erros.append(f"progresso_aulas.csv: matricula {pr['matricula_id']}, aula {pr['aulas_id']} - concluida deve ser true/false")
        if pr["data_conclusao"] and not is_data(pr["data_conclusao"], com_tempo=True):
            erros.append(f"progresso_aulas.csv: matricula {pr['matricula_id']}, aula {pr['aulas_id']} - data_conclusao inválida")

    for av in avaliacoes:
        if not is_int(av["nota"]):
            erros.append(f"avaliacoes.csv: id {av['id']} - nota não inteira")
        else:
            n = int(av["nota"])
            if not (1 <= n <= 5):
                erros.append(f"avaliacoes.csv: id {av['id']} - nota fora do range 1..5")
        if not is_data(av["data_avaliacao"]):
            erros.append(f"avaliacoes.csv: id {av['id']} - data_avaliacao inválida")

    # ---- Duplicatas simples por ID ----
    def _dup_ids(rows, campo, nome):
        vistos, dups = set(), []
        for r in rows:
            k = r[campo]
            if k in vistos:
                dups.append(k)
            vistos.add(k)
        if dups:
            erros.append(f"{nome}: IDs duplicados -> {sorted(set(dups))[:10]}")

    _dup_ids(alunos, "id", "alunos.csv")
    _dup_ids(instrutores, "id", "instrutores.csv")
    _dup_ids(categorias, "id", "categorias.csv")
    _dup_ids(cursos, "id", "cursos.csv")
    _dup_ids(modulos, "id", "modulos.csv")
    _dup_ids(aulas, "id", "aulas.csv")
    _dup_ids(matriculas, "id", "matriculas.csv")
    _dup_ids(avaliacoes, "id", "avaliacoes.csv")

    # ---- Integridade referencial ----
    ids_alunos = {r["id"] for r in alunos}
    ids_instr = {r["id"] for r in instrutores}
    ids_cat = {r["id"] for r in categorias}
    ids_cursos = {r["id"] for r in cursos}
    ids_mod = {r["id"] for r in modulos}
    ids_aulas = {r["id"] for r in aulas}
    ids_mats = {r["id"] for r in matriculas}

    for c in cursos:
        if c["instrutor_id"] not in ids_instr:
            erros.append(f"cursos.csv: id {c['id']} - instrutor_id inexistente")

    # categorias_cursos PK composta (curso_id, categoria_id)
    vistos_cc = set()
    for cc in cat_cursos:
        k = (cc["curso_id"], cc["categoria_id"])
        if cc["curso_id"] not in ids_cursos:
            erros.append(f"categorias_cursos.csv: curso_id {cc['curso_id']} inexistente")
        if cc["categoria_id"] not in ids_cat:
            erros.append(f"categorias_cursos.csv: categoria_id {cc['categoria_id']} inexistente")
        if k in vistos_cc:
            erros.append(f"categorias_cursos.csv: duplicado {k}")
        vistos_cc.add(k)

    for m in modulos:
        if m["curso_id"] not in ids_cursos:
            erros.append(f"modulos.csv: id {m['id']} - curso_id inexistente")

    for a in aulas:
        if a["modulo_id"] not in ids_mod:
            erros.append(f"aulas.csv: id {a['id']} - modulo_id inexistente")

    vistos_mat = set()
    for m in matriculas:
        k = (m["aluno_id"], m["curso_id"])
        if m["aluno_id"] not in ids_alunos:
            erros.append(f"matriculas.csv: id {m['id']} - aluno_id inexistente")
        if m["curso_id"] not in ids_cursos:
            erros.append(f"matriculas.csv: id {m['id']} - curso_id inexistente")
        if k in vistos_mat:
            erros.append(f"matriculas.csv: duplicado (aluno_id, curso_id) {k}")
        vistos_mat.add(k)

    vistos_prog = set()
    for p in progresso:
        k = (p["matricula_id"], p["aulas_id"])
        if p["matricula_id"] not in ids_mats:
            erros.append(f"progresso_aulas.csv: matricula_id {p['matricula_id']} inexistente")
        if p["aulas_id"] not in ids_aulas:
            erros.append(f"progresso_aulas.csv: aulas_id {p['aulas_id']} inexistente")
        if k in vistos_prog:
            erros.append(f"progresso_aulas.csv: duplicado PK {k}")
        vistos_prog.add(k)

    for av in avaliacoes:
        if av["matricula_id"] not in ids_mats:
            erros.append(f"avaliacoes.csv: id {av['id']} - matricula_id inexistente")

    # ---- Relatório ----
    total = sum(1 for _ in erros)
    with open(REPORT, "w", encoding="utf-8") as f:
        if total == 0:
            f.write("# Relatório de Validação\n\n✅ Nenhum erro encontrado.\n")
        else:
            f.write("# Relatório de Validação\n\n")
            f.write(f"**Erros encontrados:** {total}\n\n")
            for e in erros:
                f.write(f"- {e}\n")

    print(f"✅ Validação concluída. Relatório: {REPORT}")

if __name__ == "__main__":
    validar()
