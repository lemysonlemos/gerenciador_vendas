🚀 Passo a Passo para Rodar o Projeto

1. Clonar o repositório
git clone

2. Escolha uma das 3 opções para rodar o projeto:

🐳 1. Usando Docker
No arquivo gerenciador/settings.py, descomente a configuração de DATABASES referente ao Docker.
Comente as outras duas opções (PostgreSQL local e Heroku).
# Rode o docker
docker-compose up --build

🐘 2. Usando PostgreSQL local
Crie o banco no seu PostgreSQL.
No arquivo gerenciador/settings.py, descomente a configuração de DATABASES referente ao PostgreSQL local.
Comente as outras duas opções (Docker e Heroku).
# Crie o banco e rode as migrações
python manage.py migrate
# Inicie o servidor
python manage.py runserver

☁️ 3. Usando Heroku
No arquivo gerenciador/settings.py, descomente a configuração de DATABASES referente ao Heroku.
Comente as outras duas opções (Docker e PostgreSQL local).
Descomente SECRET_KEY = os.getenv("SECRET_KEY") e import dj_database_url
Suba o projeto para o Heroku conforme sua configuração padrão.

OBS: para rodar via docker ou postgreslocal comente
SECRET_KEY = os.getenv("SECRET_KEY") e import dj_database_url
e descomente o SECRET_KEY

3. Rodar as Migrações(mesmo no heroku)
python manage.py migrate

4. Executar o Projeto
Se estiver usando PostgreSQL local:
python manage.py runserver

5. Criar um Cliente
Acesse a URL do projeto (ex: http://127.0.0.1:8000/ ou http://localhost:8000/) e faça o cadastro como Cliente.

6. Ativar Acesso de Admin
Depois de cadastrar um cliente, rode os comandos no terminal:
python manage.py ativar_perfil_admin <cpf>
python manage.py ativar_superusuario_admin <cpf>

7. Acessar como Funcionário
Vá para a tela inicial.
Escolha a opção "Funcionário".
Faça login com o CPF e a senha do cliente ativado como admin.

🧑‍💼 Perfis do Sistema
Admin:
Pode adicionar e editar itens, fabricantes, clientes, lojas, funcionários, estoque e catálogo.
Pode processar compras e acessar o dashboard completo.

Gerente:
Pode fazer alterações apenas na loja em que está vinculado, com quase todos os poderes de admin, menos de adicionar loja.

Vendedor:
Pode visualizar o estoque, as compras, o dashboard e os clientes.
Pode vender produtos no catálogo da loja em que está vinculado.

Cliente:
Pode editar seu próprio perfil.
Pode visualizar e realizar compras pelo catálogo.
Pode acompanhar o status das suas compras.

🔄 Fluxo de estoque
Faça a adição dos itens, fabricantes e por fim do catálogo, adicione imagem para o catálogo) na opção catálogo do menu.
Depois na opção estoque, em adicionar estoque, selecione o catalogo e insira a quantidade que tem em estoque.
A visualização final fica em catálogo.


🔄 Fluxo de Compra
Após a compra (pelo cliente ou vendedor), a compra fica com status "Em processamento".
Um Gerente ou Admin deve finalizar a compra manualmente.

💡 Observação
Este é um projeto inicial e simples, pensado para proporcionar um primeiro contato com o Django. 
Fique à vontade para melhorar, modificar ou implementar novas funcionalidades!



