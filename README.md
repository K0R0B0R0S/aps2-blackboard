# Sistema de Controle de Estoque com Arquitetura Blackboard

Este projeto implementa um sistema de controle e abastecimento de estoque para lojas de varejo, utilizando a arquitetura **Blackboard**. O sistema gerencia níveis de estoque, histórico de vendas, dados de fornecedores e histórico de compras, com módulos especialistas para atualização e reposição de estoque.

---

## 📋 Funcionalidades

- **Blackboard (Memória Compartilhada):**
  - Armazena dados centrais, como níveis de estoque, histórico de vendas, dados de fornecedores e histórico de compras.

- **Módulos Especialistas:**
  - **Lojas de Varejo:** Atualizam o Blackboard a cada venda realizada.
  - **Reposição de Estoque:** Sugere ordens de compra ou transferências de produtos entre lojas com base no estoque disponível.

- **Banco de Dados:**
  - Armazena informações sobre lojas, produtos, estoque, fornecedores, compras e vendas.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem de Programação:** Python
- **Banco de Dados:** PostgreSQL
- **ORM:** SQLAlchemy
- **Ferramenta de Migração:** Alembic
- **Arquitetura:** Blackboard

---

## 🚀 Como Executar o Projeto

### Pré-requisitos

- Python 3.8 ou superior.
- Pip (gerenciador de pacotes do Python).
- Banco de dados configurado PostgreSQL.

### Passos para Configuração

1. **Clone o Repositório:**

   ```bash
   git clone https://github.com/seu-usuario/aps2-blackboard.git
   cd aps2-blackboard
   ```

2. **Crie um Ambiente Virtual (Opcional, mas Recomendado)**

    ```bash
    python -m venv venv
    ```

    - No windows
        ```bash
        venv\Scripts\activate
        ```
    
    - No linux
        ```bash
        source venv/bin/activate
        ```

3. **Instale as Dependências**
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure o Banco de Dados**:
    - Crie um arquivo .env na raiz do projeto e adicione a URL de conexão do banco de dados. Para Postgres:
    ```
    CONNECTION_URI=postgresql://postgres:root@localhost:5455/blackboard
    ```

5. **Execute as Migrations e Insira Dados de Brinquedo**:
    ```bash
    cd ./backend #Caso não esteja na pasta
    alembic upgrade head
    python -m src.database.seed
    ```

6. **Execute o Projeto**:
    ```bash
    cd ./backend #Caso não esteja na pasta
    python main.py
    ```

