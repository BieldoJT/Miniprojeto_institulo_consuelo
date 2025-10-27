
--Listar todos os cursos com nome da(s) categoria(s) e do instrutor
SELECT
  c.id,
  c.titulo,
  i.nome        AS instrutor,
  cat.nome      AS categorias
FROM cursos c
JOIN instrutores i        ON i.id = c.instrutor_id
LEFT JOIN categorias_cursos cc ON cc.curso_id = c.id
LEFT JOIN categorias cat       ON cat.id = cc.categoria_id
GROUP BY c.id, c.titulo, i.nome, cat.nome
ORDER BY c.titulo;

--Listar todos os alunos matriculados em um curso específico
SELECT a.id, a.nome, a.email, m.status, m.data_matricula
FROM matriculas m
JOIN alunos a ON a.id = m.aluno_id
WHERE m.curso_id = :curso_id
ORDER BY a.nome;

--Exibir todas as aulas de um curso ordenadas por módulo e ordem
SELECT
  m.titulo      AS modulo,
  m.ordem       AS ordem_modulo,
  a.titulo      AS aula,
  a.ordem_aula,
  a.duracao_minutos,
  a.tipo
FROM modulos m
JOIN aulas a ON a.modulo_id = m.id
WHERE m.curso_id = :curso_id
ORDER BY m.ordem, a.ordem_aula;


--Média de avaliações de cada curso
SELECT
  c.id,
  c.titulo,
  ROUND(AVG(av.nota)::numeric, 2) AS media_nota,
  COUNT(av.id)                    AS qt_avaliacoes
FROM cursos c
LEFT JOIN matriculas m ON m.curso_id = c.id
LEFT JOIN avaliacoes av ON av.matricula_id = m.id
GROUP BY c.id, c.titulo
ORDER BY media_nota DESC NULLS LAST;


--Quantos alunos estão matriculados por curso
SELECT
  c.id,
  c.titulo,
  COUNT(DISTINCT m.aluno_id) AS alunos_matriculados
FROM cursos c
LEFT JOIN matriculas m ON m.curso_id = c.id
GROUP BY c.id, c.titulo
ORDER BY alunos_matriculados DESC, c.titulo;

--Faturamento total por categoria (considerando ordens pagas)
SELECT
  cat.id,
  cat.nome AS categoria,
  COALESCE(SUM(op.valor_a_pagar),0) AS faturamento
FROM categorias cat
LEFT JOIN categorias_cursos cc ON cc.categoria_id = cat.id
LEFT JOIN cursos c            ON c.id = cc.curso_id
LEFT JOIN matriculas m        ON m.curso_id = c.id
LEFT JOIN ordem_pagamentos op ON op.matricula_id = m.id AND op.status = 'pago'
GROUP BY cat.id, cat.nome
ORDER BY faturamento DESC, cat.nome;

--Curso com maior número de matrículas ativas
SELECT c.id, c.titulo, COUNT(*) AS matriculas_ativas
FROM cursos c
JOIN matriculas m ON m.curso_id = c.id
WHERE m.status = 'ativa'
GROUP BY c.id, c.titulo
ORDER BY matriculas_ativas DESC, c.titulo
LIMIT 1;

--Alunos, cursos matriculados e % de conclusão por matrícula
WITH total_aulas_por_curso AS (
  SELECT c.id AS curso_id, COUNT(a.id) AS total_aulas
  FROM cursos c
  JOIN modulos m ON m.curso_id = c.id
  JOIN aulas a   ON a.modulo_id = m.id
  GROUP BY c.id
),
aulas_concluidas_por_matricula AS (
  SELECT m.id AS matricula_id, COUNT(*) AS concluidas
  FROM progresso_aulas pa
  JOIN matriculas m ON m.id = pa.matricula_id
  WHERE pa.concluida = TRUE
  GROUP BY m.id
)
SELECT
  a.id         AS aluno_id,
  a.nome       AS aluno,
  c.id         AS curso_id,
  c.titulo     AS curso,
  m.status,
  ROUND( 100.0 * COALESCE(ac.concluidas,0) / NULLIF(t.total_aulas,0), 1) AS pct_conclusao
FROM matriculas m
JOIN alunos a  ON a.id = m.aluno_id
JOIN cursos c  ON c.id = m.curso_id
LEFT JOIN total_aulas_por_curso t  ON t.curso_id = c.id
LEFT JOIN aulas_concluidas_por_matricula ac ON ac.matricula_id = m.id
ORDER BY a.nome, c.titulo;



--Relatório completo de um curso (instrutor, nº alunos, média de avaliações, faturamento)
SELECT
  c.id,
  c.titulo,
  i.nome AS instrutor,
  COUNT(DISTINCT m.aluno_id)                 AS qt_alunos,
  ROUND(AVG(av.nota)::numeric, 2)            AS media_nota,
  COALESCE(SUM(CASE WHEN op.status='pago' THEN op.valor_a_pagar END),0) AS faturamento
FROM cursos c
JOIN instrutores i   ON i.id = c.instrutor_id
LEFT JOIN matriculas m        ON m.curso_id = c.id
LEFT JOIN avaliacoes av       ON av.matricula_id = m.id
LEFT JOIN ordem_pagamentos op ON op.matricula_id = m.id
WHERE c.id = :curso_id
GROUP BY c.id, c.titulo, i.nome;


--Instrutores com quantidade de cursos, total de alunos e média geral de avaliações
SELECT
  i.id,
  i.nome AS instrutor,
  COUNT(DISTINCT c.id)                    AS qt_cursos,
  COUNT(DISTINCT m.id)                    AS qt_matriculas,
  ROUND(AVG(av.nota)::numeric, 2)         AS media_geral_avaliacoes
FROM instrutores i
LEFT JOIN cursos c       ON c.instrutor_id = i.id
LEFT JOIN matriculas m   ON m.curso_id = c.id
LEFT JOIN avaliacoes av  ON av.matricula_id = m.id
GROUP BY i.id, i.nome
ORDER BY qt_cursos DESC, qt_matriculas DESC, i.nome;

--Top 5 cursos mais rentáveis (somando ordens pagas)

SELECT
  c.id,
  c.titulo,
  SUM(op.valor_a_pagar) AS receita
FROM cursos c
JOIN matriculas m        ON m.curso_id = c.id
JOIN ordem_pagamentos op ON op.matricula_id = m.id
WHERE op.status = 'pago'
GROUP BY c.id, c.titulo
ORDER BY receita DESC
LIMIT 5;


--Alunos que não concluíram nenhum curso nos últimos 6 meses
SELECT a.id, a.nome, a.email
FROM alunos a
WHERE NOT EXISTS (
  SELECT 1
  FROM matriculas m
  WHERE m.aluno_id = a.id
    AND m.status = 'concluida'
    AND m.data_conclusao >= NOW() - INTERVAL '6 months'
)
ORDER BY a.nome;

