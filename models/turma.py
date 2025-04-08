from .database import get_connection

class Turma:
    def __init__(self, id=None, nome=""):
        self.id = id
        self.nome = nome

    @staticmethod
    def adicionar(nome):
        conn = get_connection()
        cursor = conn.cursor()
        
        # Verificar se já existe uma turma com o mesmo nome
        cursor.execute('SELECT id FROM turmas WHERE nome = ?', (nome,))
        existente = cursor.fetchone()
        
        if existente:
            conn.close()
            raise ValueError(f"Já existe uma turma com o nome '{nome}'.")
            
        cursor.execute('INSERT INTO turmas (nome) VALUES (?)', (nome,))
        conn.commit()
        conn.close()

    @staticmethod
    def buscar_por_id(turma_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, nome FROM turmas WHERE id = ?', (turma_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Turma(id=row[0], nome=row[1])
        return None

    @staticmethod
    def listar():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome FROM turmas")
        turmas = cursor.fetchall()
        conn.close()
        return turmas
