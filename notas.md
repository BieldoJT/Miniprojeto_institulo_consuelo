# ANOTAÇÕES


## ER - DIAGRAMA
 -- 08/10
- Não sei se na tabela instrutores a coluna biografia seja text ou varchar

- Os cursos podem ter mais de uma categoria??

- decimal ou float?

- nivel do curso, talvez seja um enum??

- o que seria ordem na tabela campus??

- tipo deve ser enum??

- lembrar de setar os not null

- status da tabela matriculas talvez enum??

- nota talvez seja enum


https://dbdiagram.io/d/ER-mini_projeto_casa_digital-663ab0839e85a46d55408b02

 -- 10/06
- para todos os enuns USAR CHECK

- criar tabelas pagamento e ordem de pagamento

 - ordem pagamento
- - id
- - id_aluno
- - id_curso
- - forma_pagto (USAR CHECK para PIX, CREDITO, DEBITO, BOLETO)
- - valor ()
- - status_pagto (usar CHECK EM PENDENTE, PAGO, CANCELADO, REEMBOLSO)
- - data_criacao (nao nulo)
- - data_pagto (pode ser nulo)

- criar uma tabela de cupons???

 - pagamento
- - id
- - ordem_ptgo fk
- - forma_pagto (USAR CHECK para PIX, CREDITO, DEBITO, BOLETO)
- - status_pagto (Autorizado,Falhou,Reembolso)
- - data_criacao (nao nulo)

- Separar as avaliações por modulos do curso , para ter mais controle do alunos

- criar a coluna da situação da matricula
