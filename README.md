Meu DinDin | Controle Financeiro Pessoal



O Meu DinDin é uma aplicação web que desenvolvi para facilitar o controle de receitas e despesas pessoais.



A ideia do projeto é oferecer uma ferramenta simples, na qual cada usuário possa acompanhar sua movimentação financeira em um só lugar, com acesso individual e dados separados por conta.



Acesse o sistema: https://meudindin-b259.onrender.com/



Conheça o sistema



Tela de login







Cadastro de usuários







Dashboard financeiro











Histórico de transações







Cadastro de receitas e despesas







O que o sistema faz



Permite criar uma conta e acessar o sistema com autenticação.



Mantém novos cadastros aguardando aprovação do administrador.



Organiza receitas e despesas em um painel financeiro.



Permite registrar e consultar transações.



Organiza as movimentações por categoria e data.



Garante que cada usuário tenha acesso somente aos próprios dados.



Disponibiliza uma API REST para operações financeiras.



Conta com documentação da API por meio do Swagger.



Tecnologias utilizadas



Python e Django: desenvolvimento da aplicação e das regras de negócio.



Django REST Framework: construção da API.



PostgreSQL: armazenamento dos dados.



HTML e CSS: estrutura e apresentação das páginas.



Git e GitHub: versionamento e organização do código.



Render: publicação da aplicação.



Segurança e backup



Um dos pontos que priorizei no desenvolvimento foi a separação dos dados entre usuários. Cada conta possui suas próprias transações, sem acesso às movimentações de outras pessoas.



Também implementei uma rotina de backup do PostgreSQL. Além de automatizar a geração das cópias, realizei um teste de restauração em um banco local separado para verificar se os dados poderiam ser recuperados.



Sobre o desenvolvimento



Este projeto faz parte da minha evolução prática com Python e desenvolvimento web. Durante sua construção, trabalhei com autenticação, permissões, operações com banco de dados, criação de APIs e publicação de aplicações.



Mais do que desenvolver as funcionalidades, o projeto também me permitiu lidar com questões importantes de um sistema em funcionamento, como isolamento de dados, manutenção e recuperação de informações.



Desenvolvedor



Jonatas Balthazar Nascimento



GitHub: https://github.com/JohnBalth



LinkedIn: https://www.linkedin.com/in/jonatas-balthazar-120298202

