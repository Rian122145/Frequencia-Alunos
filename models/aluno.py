from .database import get_connection
import sqlite3

class Aluno:
    def __init__(self, id=None, nome=""):
        self.id = id
        self.nome = nome
        self.turmas = []  # Lista de IDs de turmas do aluno

    @staticmethod
    def adicionar(nome, turma_id=None):
        conn = get_connection()
        cursor = conn.cursor()
        
        # Inserir o aluno
        cursor.execute("INSERT INTO alunos (nome) VALUES (?)", (nome,))
        aluno_id = cursor.lastrowid
        
        # Associar o aluno à turma apenas se uma turma for especificada
        if turma_id is not None:
            cursor.execute("INSERT INTO aluno_turma (aluno_id, turma_id) VALUES (?, ?)", 
                        (aluno_id, turma_id))
        
        conn.commit()
        conn.close()
        return aluno_id

    @staticmethod
    def adicionar_turma(aluno_id, turma_id):
        conn = get_connection()
        cursor = conn.cursor()
        
        # Verificar se o aluno já está na turma
        cursor.execute("""
            SELECT id FROM aluno_turma 
            WHERE aluno_id = ? AND turma_id = ?
        """, (aluno_id, turma_id))
        
        if cursor.fetchone():
            conn.close()
            raise ValueError("Este aluno já está cadastrado nesta turma.")
            
        try:
            cursor.execute("INSERT INTO aluno_turma (aluno_id, turma_id) VALUES (?, ?)", 
                          (aluno_id, turma_id))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            # Caso haja algum outro erro de integridade
            conn.rollback()
            raise ValueError("Erro ao adicionar aluno na turma.")
        finally:
            conn.close()

    @staticmethod
    def listar_por_turma(turma_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.id, a.nome 
            FROM alunos a
            JOIN aluno_turma at ON a.id = at.aluno_id
            WHERE at.turma_id = ?
        """, (turma_id,))
        alunos = cursor.fetchall()
        conn.close()
        return alunos

    @staticmethod
    def listar_turmas_por_aluno(aluno_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT t.id, t.nome 
            FROM turmas t
            JOIN aluno_turma at ON t.id = at.turma_id
            WHERE at.aluno_id = ?
        """, (aluno_id,))
        turmas = cursor.fetchall()
        conn.close()
        return turmas

    @staticmethod
    def buscar_por_id(aluno_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome FROM alunos WHERE id = ?", (aluno_id,))
        aluno = cursor.fetchone()
        conn.close()
        return aluno

    @staticmethod
    def listar_todos():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome FROM alunos")
        alunos = cursor.fetchall()
        conn.close()
        return alunos
