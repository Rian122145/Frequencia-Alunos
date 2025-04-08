# Frequência de Alunos

Este projeto é uma aplicação para gerenciar a frequência de alunos em turmas. Ele permite adicionar e editar alunos, turmas e registrar a presença dos alunos.

## Funcionalidades

- **Cadastro de Turmas**: Criação de turmas únicas (não permite nomes duplicados).
- **Cadastro de Alunos**: Adição de novos alunos ao sistema.
- **Gerenciamento de Turmas**: Adicionar alunos a turmas, impedindo duplicidade.
- **Registro de Presenças**: Marcar presença de alunos em datas específicas.
- **Consulta de Frequência**: Visualizar a frequência de alunos por turma e data ou por aluno.

## Estrutura do Projeto

- **controllers/**: Contém a lógica de controle da aplicação.
  - `aluno_controller.py`: Gerencia operações relacionadas aos alunos.
  - `turma_controller.py`: Gerencia operações relacionadas às turmas.
  - `presenca_controller.py`: Gerencia operações de presença.

- **models/**: Contém os modelos que representam os dados da aplicação.
  - `aluno.py`: Define a classe Aluno.
  - `turma.py`: Define a classe Turma.
  - `presenca.py`: Define a classe Presenca.
  - `database.py`: Configura a conexão e estrutura do banco de dados.

- **views/**: Contém as interfaces gráficas da aplicação.
  - `main_window.py`: Interface principal da aplicação.
  - `cadastro_aluno.py`: Interface para cadastro de alunos.
  - `cadastro_turma.py`: Interface para cadastro de turmas.
  - `marcar_presenca.py`: Interface para registrar presenças.
  - `consultar_frequencia.py`: Interface para consultar frequência.

- **main.py**: Ponto de entrada da aplicação.

## Como Executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/Rian122145/Frequencia-Alunos
   ```

2. Navegue até o diretório do projeto:
   ```bash
   cd frequencia_alunos
   ```

3. Instale as dependências necessárias:
   ```bash
   pip install -r requirements.txt
   ```

4. Execute o projeto:
   ```bash
   python main.py
   ```

## Requisitos

- Python 3.8 ou superior.
- PyQt5 para a interface gráfica.
- SQLite para o banco de dados.

## Observações

- Certifique-se de que o banco de dados `frequencia.db` será criado automaticamente na primeira execução.