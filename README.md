Projeto da cadeira de Desenvolvimento de Software para a Nuvem

Este projeto se trata de uma aplicação que é uma rede social de fotos, similar ao instagram.

Os dados dos usuários a serem salvos são: 
	● Nome Completo
	● Nick
	● Senha
	● E-mail
	● Foto Pessoal

O sistema deve permitir que se faça as seguintes operações: 
	1. Criar um usuário;
	2. Alterar dados de um usuário;
	3. Publicar fotos;
	4. Curtir/Descutir fotos de usuários;
	5. Visualizar perfil de outro usuário e suas fotos (todos podem ver informações dos outros usuários - não existe a necessidade de solicitar amizade ou deixar o perfil público ou privado);
	6. Buscar um usuário com base em seu nick;
	7. Listar fotos postadas em um intervalo de tempo. Para isso, devem ser fornecidas a Data Inicial e Data Final para filtro.

Imposições sobre o trabalho: 
	1. As informações dos usuários devem ser gravadas em uma instância de banco de dados relacional, criada pelo serviço Amazon RDS;
	2. As fotos que serão enviadas devem ser armazenadas utilizando o serviço Amazon S3;
	3. As curtidas que as imagens possuem deverão ser salvas usando o Amazon DynamoDB; 