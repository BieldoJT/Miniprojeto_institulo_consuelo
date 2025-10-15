create schema if not exists Edutech;
SET search_path TO Edutech;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

drop table if exists alunos cascade;
create table alunos (
	id serial primary key,
	nome varchar(50) not null,
	email varchar(254) not null unique,
	data_nascimento date not null,
	data_cadastro timestamp not null default now()
);

comment on table alunos is 'Alunos da plataforma';
comment on column alunos.email is 'Email único por aluno (case-insentisive)';

drop table if exists instrutores cascade;
create table instrutores (
	id serial primary key,
	nome varchar(50) not null,
	email varchar(254) not null unique,
	especialidade varchar(100) not null,
	biografia varchar(300)
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



--remover o curso_id do avalição, pois matriculas ja posssui o id do curso

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
	data_matricula timestamp not null,
	status varchar(10) not null check(status in ('ativa', 'concluida', 'cancelada', 'reservada')),
	data_conclusao timestamp,
	unique (aluno_id, curso_id)
);



comment on table matriculas is 'Informações das matriculas dos alunos nos cursos';
comment on column matriculas.status is 'Situação da matricula do aluno';

drop table if exists ordem_pagamentos cascade;
create table ordem_pagamentos (
	id uuid primary key,
	matricula_id integer not null references matriculas(id) on delete cascade,
	valor_a_pagar numeric(5,2) not null check(valor_a_pagar >= 0),
	status varchar(20) not null check(status in ('pendente', 'pago','reembolsado')),
	criado_em timestamp not null,
	pago_em timestamp
);

drop table if exists pagamentos cascade;
create table pagamentos (
	id uuid primary key,
	ordem_id uuid not null references ordem_pagamentos(id) on delete cascade,
	forma_pagamento varchar(20) not null check(forma_pagamento  in ('pix', 'debito', 'credito')),
	status_pagamento varchar(20) not null check(status_pagamento in ('confirmado','falho', 'reembolsado')),
	data_criacao timestamp not null
);

drop table if exists certificados cascade;
create table certificados (
	id uuid primary key,
	matricula_id integer not null references matriculas(id) on delete cascade,
	data_criacao timestamp not null,
	data_emissao timestamp
);

-- tratar os limites de preço no python ou aqui??




