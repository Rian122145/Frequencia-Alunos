from .database import get_connection

class Presenca:
    @staticmethod
    def marcar(aluno_id, data, presente):
        conn = get_connection()
        cursor = conn.cursor()
        
        # Verifica se já existe para update
        cursor.execute("""
            SELECT id FROM presencas 
            WHERE aluno_id = ? AND data = ?
        """, (aluno_id, data))
        existente = cursor.fetchone()
        
        if existente:
            cursor.execute("""
                UPDATE presencas
                SET presente = ?
                WHERE aluno_id = ? AND data = ?
            """, (int(presente), aluno_id, data))
        else:
            cursor.execute("""
                INSERT INTO presencas (aluno_id, data, presente)
                VALUES (?, ?, ?)
            """, (aluno_id, data, int(presente)))
            
        conn.commit()
        conn.close()

    @staticmethod
    def listar_por_turma_e_data(turma_id, data):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.nome, p.presente
            FROM presencas p
            JOIN alunos a ON p.aluno_id = a.id
            WHERE a.turma_id = ? AND p.data = ?
        """, (turma_id, data))
        resultado = cursor.fetchall()
        conn.close()
        return resultado

    @staticmethod
    def listar_por_aluno(aluno_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT data, presente
            FROM presencas
            WHERE aluno_id = ?
            ORDER BY data
        """, (aluno_id,))
        resultado = cursor.fetchall()
        conn.close()
        return resultado
    
    @staticmethod
    def calcular_porcentagem_presenca(aluno_id, data_min, data_max):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT t.nome, 
                   COUNT(p.presente) AS total_aulas, 
                   SUM(p.presente) AS total_presencas
            FROM presencas p
            JOIN alunos a ON a.id = p.aluno_id
            JOIN turmas t ON t.id = a.turma_id
            WHERE p.aluno_id = ? AND p.data BETWEEN ? AND ?
            GROUP BY t.nome
        """, (aluno_id, data_min, data_max))
        resultados = cursor.fetchall()
        conn.close()

        relatorio = []
        for row in resultados:
            turma = row[0]
            total_aulas = row[1] or 0
            total_presencas = row[2] or 0
            porcentagem = (total_presencas / total_aulas) * 100 if total_aulas > 0 else 0
            relatorio.append({"turma": turma, "porcentagem": round(porcentagem, 2)})

        return relatorio
