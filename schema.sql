\c postgres;
DROP DATABASE IF EXISTS edutech;
CREATE DATABASE edutech;
\c edutech;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS citext;

drop table if exists alunos cascade;
create table alunos (
	id serial primary key,
	nome varchar(50) not null,
	email citext not null unique,
	data_nascimento date not null,
	data_cadastro timestamp not null default now()
);

comment on table alunos is 'Alunos da plataforma';
comment on column alunos.email is 'Email único por aluno (case-insentisive)';

drop table if exists instrutores cascade;
create table instrutores (
	id serial primary key,
	nome varchar(50) not null,
	email citext not null unique,
	especialidade varchar(100) not null,
	biografia varchar(300) not null,
	data_cadastro timestamp not null default now(),
	ultima_alteracao timestamp not null default now()
);

comment on table instrutores is 'Instrutores dos cursos da plataforma';
comment on column instrutores.email is 'Email único por instrutor';

drop table if exists categorias cascade;
create table categorias (
	id serial primary key,
	nome varchar(100) not null unique,
	descricao text not null
);

comment on table categorias is 'Categorias dos cursos';


drop table if exists cursos cascade;
create table cursos (
	id serial primary key,
	instrutor_id integer not null REFERENCES instrutores(id) on delete restrict,
	titulo varchar(100) not null unique,
	descricao varchar(250) not null,
	nivel varchar(20) not null check(nivel in ('iniciante','intermediario','avançado')),
	preco numeric(5,2) not null check(preco >= 0),
	carga_horaria integer not null check(carga_horaria > 0),
	data_criacao timestamp not null default now(),
	ultima_alteracao timestamp not null default now()
);

comment on table cursos is 'Informacaoes dos cursos publicados por instrutores';
comment on column cursos.nivel is 'Possui os niveis iniciante, intermediario e avançado';
comment on column cursos.preco is 'Valor do curso, não pode ser negativo';



drop table if exists categorias_cursos cascade;
create table categorias_cursos (
	curso_id integer not null references cursos(id) on delete cascade,
	categoria_id integer not null references categorias(id) on delete restrict,
	primary key (curso_id, categoria_id)
);
-- cascade para apagar os cursos
-- restrict para não permitir apagar se estiver em uso

comment on table categorias_cursos is 'relação entre categorias e cursos';


drop table if exists modulos cascade;
create table modulos (
	id serial primary key,
	curso_id integer not null references cursos(id) on delete cascade,
	titulo varchar(50) not null,
	ordem integer not null,
	descricao varchar(200) not null,
	unique (curso_id, ordem)
);

comment on table modulos is 'modulos dos curso e suas ordens';





drop table if exists aulas cascade;
create table aulas (
	id serial primary key,
	modulo_id integer not null references modulos(id) on delete cascade,
	titulo varchar(50) not null,
	ordem_aula integer not null,
	duracao_minutos integer not null check(duracao_minutos >= 0),
	tipo varchar(20) not null check(tipo in ('video', 'texto', 'quiz')),
	unique(modulo_id, ordem_aula)
);

comment on table aulas is 'Informações das aulas dos modulos dos cursos';
comment on column aulas.ordem_aula is 'ordem das aulas dentro do modulo';



-- o campo valor_pago, mudei para valor_curso//
drop table if exists matriculas cascade;
create table matriculas (
	id serial primary key,
	aluno_id integer not null references alunos(id) on delete cascade,
	curso_id integer not null references cursos(id) on delete cascade,
	data_matricula timestamp not null default now(),
	status varchar(10) not null check(status in ('ativa', 'concluida', 'cancelada', 'pendente')) default 'pendente',
	data_conclusao timestamp default null,
	unique (aluno_id, curso_id)
);

drop table if exists progresso_aulas cascade;
create table progresso_aulas (
	matricula_id integer not null references matriculas(id) on delete cascade,
	aulas_id integer not null references aulas(id) on delete cascade,
	concluida boolean not null default false,
	data_conclusao timestamp,
	primary key  (matricula_id, aulas_id)
);

--remover o curso_id do avalição, pois matriculas ja posssui o id do curso

drop table if exists avaliacoes cascade;
create table avaliacoes (
	id serial primary key,
	matricula_id integer not null references matriculas(id) on delete cascade,
	nota integer not null check(nota >=1 and nota <= 5),
	comentario varchar(200),
	data_avaliacao date not null default now()
);



comment on table matriculas is 'Informações das matriculas dos alunos nos cursos';
comment on column matriculas.status is 'Situação da matricula do aluno';

drop table if exists ordem_pagamentos cascade;
create table ordem_pagamentos (
	id uuid primary key default uuid_generate_v4(),
	matricula_id integer not null references matriculas(id) on delete cascade,
	valor_a_pagar numeric(5,2) not null check(valor_a_pagar >= 0),
	status varchar(20) not null check(status in ('pendente', 'pago','reembolsado' ,'cancelado')) default 'pendente',
	criado_em timestamp not null default now(),
	pago_em timestamp
);

drop table if exists certificados cascade;
create table certificados (
	id uuid primary key default uuid_generate_v4(),
	matricula_id integer not null references matriculas(id) on delete cascade,
	data_criacao timestamp not null default now(),
	data_emissao timestamp
);

-- tratar os limites de preço no python ou aqui??
 -- INDEXES


-- Index das chaves estrangeiras
create index if not exists idx_cursos_instrutor on cursos(instrutor_id);
create index if not exists idx_cc_categorias_id on categorias_cursos(categoria_id);
create index if not exists idx_pg_aulas_aula on progresso_aulas(aulas_id);
create index if not exists idx_avaliacoes_matricula on avaliacoes(matricula_id);
create index if not exists idx_ordem_pg_matricula on ordem_pagamentos(matricula_id);

-- outros indexes
create index if not exists idx_matriculas_curso_ativas on matriculas(curso_id) where status='ativa';
create index if not exists idx_certificados_matricula_a_emitir on certificados(matricula_id) where data_emissao is NULL;
create index if not exists idx_ordem_pg_pendentes on ordem_pagamentos(matricula_id, criado_em) where status='pendente';






/*=======================================================================*/
--  VIEWS
/*=======================================================================*/



CREATE OR REPLACE VIEW v_cursos_com_detalhes AS
SELECT
  c.id,
  c.titulo,
  i.nome AS instrutor,
  STRING_AGG(DISTINCT cat.nome, ', ' ORDER BY cat.nome) AS categorias,
  c.preco,
  c.nivel,
  c.carga_horaria,
  c.data_criacao
FROM cursos c
JOIN instrutores i           ON i.id = c.instrutor_id
LEFT JOIN categorias_cursos cc ON cc.curso_id = c.id
LEFT JOIN categorias cat        ON cat.id = cc.categoria_id
GROUP BY c.id, c.titulo, i.nome, c.preco, c.nivel, c.carga_horaria, c.data_criacao;



CREATE OR REPLACE VIEW v_faturamento_por_curso AS
SELECT
  c.id AS curso_id,
  c.titulo,
  SUM(CASE WHEN op.status='pago' THEN op.valor_a_pagar END) AS receita
FROM cursos c
LEFT JOIN matriculas m        ON m.curso_id = c.id
LEFT JOIN ordem_pagamentos op ON op.matricula_id = m.id
GROUP BY c.id, c.titulo;




CREATE OR REPLACE VIEW v_avaliacoes_por_curso AS
SELECT
  c.id AS curso_id,
  c.titulo,
  ROUND(AVG(av.nota)::numeric, 2) AS media_nota,
  COUNT(av.id)                    AS qt_avaliacoes
FROM cursos c
LEFT JOIN matriculas m ON m.curso_id = c.id
LEFT JOIN avaliacoes av ON av.matricula_id = m.id
GROUP BY c.id, c.titulo;








/*=======================================================================*/
-- Triggers, Procedurese e Funções
/*=======================================================================*/


/*-----------------------------FUNÇÔES-----------------------------------*/
/*Função que altera a coluna ultima_alteração para now()*/
create or replace function setar_ultima_alteracao()
returns trigger
language plpgsql
as $$
begin
	new.ultima_alteracao := now();
	return new;
end;
$$;

create or replace function setar_conclusao_aula()
returns trigger
language plpgsql
as $$
begin
if old.concluida is distinct from new.concluida then
	if new.concluida is true then
		new.data_conclusao := now();
	else
		new.data_conclusao := NULL;
	end if;
end if;
return new;
end;
$$;

/*Função que criar a ordem de pagamento apos criar a matricula*/
create or replace function criar_ordem_de_pagamento_na_matricula()
returns trigger
language plpgsql
as $$
declare preco_curso numeric(5,2);
declare id_matricula integer;
begin
	select preco into preco_curso from cursos where id = new.curso_id ;
	id_matricula := new.id;
	if new.status = 'pendente' then
		insert into ordem_pagamentos values (default, id_matricula, preco_curso, default, default);
	end if;
	if new.status = 'ativa' then
		insert into ordem_pagamentos values (default, id_matricula, preco_curso, 'pago', now(), default);
	end if;
	if new.status = 'concluida' then
		insert into ordem_pagamentos values (default, id_matricula, preco_curso, 'pago', now(), default);
	end if;
	if new.status = 'cancelada' then
		insert into ordem_pagamentos values (default, id_matricula, preco_curso, 'cancelado', default, default);
	end if;

	return new;
end;
$$;

create or replace function setar_matricula_alteracao_status()
returns trigger
language plpgsql
as $$
declare id_matricula integer;
begin
	id_matricula := new.matricula_id;
	if old.status is distinct from new.status then
		if new.status = 'pago' then
			new.pago_em := now();
			update matriculas set status = 'ativa' where id = id_matricula;
		end if;
		if new.status = 'cancelado' or new.status = 'reembolsado' then
			update matriculas set status = 'cancelada' where id = id_matricula;
		end if;
	end if;
	return new;
end;
$$;

create or replace function gerar_certificato()
returns trigger
language plpgsql
as $$
begin
	if old.status is distinct from new.status then
		if new.status = 'concluida' then
			insert into certificados values (default, new.id, default, default);
		end if;
	end if;
	return new;
end;
$$;




/*-----------------------------TRIGGERS-----------------------------------*/
drop trigger if exists trg_gerar_certificado_em_status_concluida on matriculas;
create trigger trg_gerar_certificado_em_status_concluida
after update on matriculas
for each row
when (old.status is distinct from new.status and new.status = 'concluida')
execute function gerar_certificato();


drop trigger if exists trg_muda_status_matricula_de_ordem_pagementos on ordem_pagamentos;
create trigger trg_muda_status_matricula_de_ordem_pagementos
before update or insert on ordem_pagamentos
for each row
execute function setar_matricula_alteracao_status();



/*Trigger para criar uma ordem de pagamento pendente para matricula*/
drop trigger if exists trg_criacao_ordem_pagamentos_na_matricula on matriculas;
create trigger trg_criacao_ordem_pagamentos_na_matricula
after insert on matriculas
for each row
execute function criar_ordem_de_pagamento_na_matricula();


/*Triggers nas tabelas reutilizando a função setar_ultima_alteracao*/
drop trigger if exists trg_ultima_alteracao_cursos on cursos;
create trigger trg_ultima_alteracao_cursos
before update on cursos
for each row
execute function setar_ultima_alteracao();

drop trigger if exists trg_ultima_alteracao_instrutores on instrutores;
create trigger trg_ultima_alteracao_instrutores
before update on instrutores
for each row
when (old is distinct from new)
execute function setar_ultima_alteracao();


/*Trigger para setar a data de conclusao e estiver concluida*/
drop trigger if exists trg_data_conclusao_progresso_aulas on progresso_aulas;
create trigger trg_data_conclusao_progresso_aulas
before update of concluida on progresso_aulas
for each row
when (old.concluida is distinct from new.concluida)
execute function setar_conclusao_aula();


/*-------------------------------------------------------------------------*/



-- comandos para testar a trigger
/*ultima alteração*/
/*
insert into alunos values (default, 'rafael', 'rafael@gmail.com', '2000-03-30');
insert into instrutores values (default,'Ricardo', 'ricardo@gmail.com', 'developer','Sou um des da programação mua hahaha');
insert into categorias values (default, 'python','cursin de python');
insert into cursos values (default, 1,'curso de python completo','um curso', 'iniciante',50.00,5,default, default);
insert into modulos values (default, 1,'um titulo', 1,'algun testo');
insert into matriculas values (default, 1,1,default, default, default);
insert into aulas values (default,1,'um moduli', 1,50.00,'quiz');
insert into progresso_aulas  values (1,1,default, default);
select * from progresso_aulas;

select * from matriculas;
select * from ordem_pagamentos op ;
update ordem_pagamentos op set status = 'pago' where matricula_id = 1;

update matriculas set status = 'concluida' where id=1;

select * from certificados;*/






