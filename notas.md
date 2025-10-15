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

 -- 10/10
- com a autorização do julio, estou modificando algumas tabelas, atualmente criei a tabela CATEGORIAS_CURSOS que relaciona os cursos com as categorias, pois um curso pode ter mais de uma categoria

- pensei em criar o campo media, para relação da media do curso, mas não sei se vale a pena

- no cupom, verificar se a data de validade é valida (se a data que termina é antes da data da que começa) e se a porcentagem de desconto não é nula. Verificar o valor maximo que cupom cobre o desconto

- verificar os campos não nulos

- aparentemente, a modelagem está pronta

//dica do Fernando
PROCESSO PARA CRIAR UMA API
como vc vai receber
• estilo de processamento (batch ou streaming)
• como vc vai processar (ETL, ELT) ETL - extract transform load | extract load transform
• como vc vai disponibilizar esses dados (enpoint GET, pagina html)

 -- 14/10

- comecei a criação do script
 - - mudei alguns campos, e estou remodelando a logica do sistema de pagamentos para tonar memhlor com as triggers

 - IMPORTANTE!!!! Por conta da logica de pagamentos, eu tirei o campo valor_pago e coloquei na tabela ordem de pagamentos, para mander uma boa relação.
