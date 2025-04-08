import sqlite3

# Caminho do arquivo do banco de dados
DB_NAME = "frequencia.db"

def get_connection():
    """Retorna uma conexão ativa com o banco de dados SQLite."""
    return sqlite3.connect(DB_NAME)

def create_tables():
    """Cria as tabelas do sistema, se ainda não existirem."""
    conn = get_connection()
    cursor = conn.cursor()

    # Tabela de turmas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS turmas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        )
    ''')

    # Tabela de alunos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        )
    ''')

    # Tabela de relacionamento entre alunos e turmas (muitos para muitos)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS aluno_turma (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno_id INTEGER NOT NULL,
            turma_id INTEGER NOT NULL,
            FOREIGN KEY (aluno_id) REFERENCES alunos(id),
            FOREIGN KEY (turma_id) REFERENCES turmas(id),
            UNIQUE(aluno_id, turma_id)
        )
    ''')

    # Tabela de presenças
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS presencas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aluno_id INTEGER NOT NULL,
        turma_id INTEGER NOT NULL,
        data TEXT NOT NULL,
        presente INTEGER NOT NULL,
        FOREIGN KEY (aluno_id) REFERENCES alunos(id),
        FOREIGN KEY (turma_id) REFERENCES turmas(id),
        UNIQUE(aluno_id, turma_id, data)
    )
    ''')

    conn.commit()
    conn.close()
