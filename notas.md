# ANOTAÇÕES


## ER - DIAGRAMA
 -- 04/10
- Não sei se na tabela instrutores a coluna biografia seja text ou varchar

- Os cursos podem ter mais de uma categoria??

- decimal ou float?

- nivel do curso, talvez seja um enum?? -> usar check nessa condições

- o que seria ordem na tabela modulos??

- tipo deve ser enum?? -> check

- lembrar de setar os not null

- status da tabela matriculas talvez enum?? ->check

- nota talvez seja enum -> usar check


https://dbdiagram.io/d/ER-mini_projeto_casa_digital-663ab0839e85a46d55408b02

 -- 06/10
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

 -- 08/10

- criação da tabela certificados, relacionada com  matricula
 - colocar um trigger/procedure para verificar se ha matricula está concluida, para gerar o certificado

- colocar alguma regra na tabela matricula para verificar qual campo é prioridade para conclusao:
    se campo 'data de conclusão' for preenchida, ou quando o campo 'status' ser alteradado para "concluida"

- criei a tabela cupom e vou colocar na ordem de pgamentos, provavelmente devo fazer um check ou trigger/procedure para verificar se o cupom é valido
