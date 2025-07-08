# 📦 Gerenciador de Estoque e Vendas

## ℹ️ Sobre

Este projeto é um **Gerenciador de Estoque e Vendas** desenvolvido para demonstrar habilidades em desenvolvimento web com Python (Flask), HTML, CSS (Bootstrap) e SQLite. O sistema permite o controle completo de produtos em estoque, registro de vendas e consultas, além de contar com autenticação de usuários (login e cadastro).

O objetivo é oferecer uma solução simples, responsiva e intuitiva para gestão de estoque, ideal para pequenas empresas, com foco em usabilidade e boas práticas de programação.

### ✨ Funcionalidades principais

-  **Login e Cadastro de Usuários:**  
  Apenas usuários autenticados podem acessar o sistema. O cadastro exige nome, e-mail, senha e CPF.

-  **Cadastro de Produtos:**  
  Permite adicionar novos produtos ao estoque, informando nome, descrição, quantidade e preço.

-  **Edição e Exclusão de Produtos:**  
  Produtos podem ser editados ou removidos facilmente através da interface.

-  **Registro de Vendas:**  
  Usuários podem registrar vendas, que automaticamente atualizam o estoque.

-  **Consultas e Busca:**  
  É possível buscar produtos pelo nome, facilitando a localização de itens no estoque.

-  **Dashboard Resumido:**  
  Exibe estatísticas rápidas, como total de produtos em estoque e total de produtos vendidos.

-  **Responsividade:**  
  Interface adaptada para desktop e dispositivos móveis, garantindo boa experiência em qualquer tela.

-  **Logout:**  
  O usuário pode sair do sistema a qualquer momento, retornando à tela de login.

### ⚙️ Como funciona

Após realizar o cadastro e login, o usuário tem acesso ao painel principal, onde pode:
-  Cadastrar, editar e excluir produtos do estoque.
-  Registrar vendas de produtos.
-  Consultar produtos e visualizar estatísticas.
-  Sair do sistema com segurança.

Todos os dados são armazenados em um banco de dados SQLite, garantindo persistência das informações.

## 🛠️ Tecnologias Utilizadas

-  **Python** — Lógica de backend e servidor web (Flask)
-  **HTML5** — Estrutura das páginas web
-  **CSS3** — Estilização das páginas
-  **Bootstrap** — Framework CSS para responsividade e componentes visuais
-  **SQLite** — Banco de dados relacional leve e integrado
-  **JavaScript** — Funcionalidades dinâmicas no frontend (quando necessário)
-  **Flask** — Framework web para Python
-  **Bootstrap Icons** — Ícones modernos e responsivos

## ▶️ Como Executar

Siga o passo a passo abaixo para rodar o Gerenciador de Estoque e Vendas em sua máquina:

1. **Clone o repositório**
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
   ```

2. **Crie e ative um ambiente virtual (opcional, mas recomendado)**
   - **Windows:**
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   - **Linux/Mac:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Instale as dependências**
   ```bash
   pip install flask
   ```

4. **Configure o banco de dados**
   - O banco SQLite será criado automaticamente na primeira execução, caso não exista.

5. **Execute o servidor**
   - No diretório do projeto, rode:
     ```bash
     python backend/main.py
     ```
   - Ou, se estiver usando Linux/Mac:
     ```bash
     python3 backend/main.py
     ```

6. **Acesse o sistema**
   - Abra o navegador e acesse: [http://localhost:5000](http://localhost:5000)

7. **Crie seu usuário**
   - Clique em “Cadastre-se” na tela de login para criar seu usuário e começar a usar o sistema.

---

**Observações:**
- Certifique-se de ter o Python 3.7 ou superior instalado.
- Para sair do ambiente virtual, use o comando `deactivate`.
- Caso queira redefinir o banco de dados, basta apagar o arquivo `.db` gerado na pasta do projeto.
