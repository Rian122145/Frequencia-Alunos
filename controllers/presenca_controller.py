from models.database import get_connection

class PresencaController:
    @staticmethod
    def registrar_presenca(aluno_id, turma_id, data, presente):
        conn = get_connection()
        cursor = conn.cursor()

        # Verifica se já existe uma presença registrada para esse aluno, turma e data
        cursor.execute('''
            SELECT id FROM presencas
            WHERE aluno_id = ? AND turma_id = ? AND data = ?
        ''', (aluno_id, turma_id, data))
        existente = cursor.fetchone()

        if existente:
            # Atualiza a presença existente
            cursor.execute('''
                UPDATE presencas
                SET presente = ?
                WHERE aluno_id = ? AND turma_id = ? AND data = ?
            ''', (presente, aluno_id, turma_id, data))
        else:
            # Insere nova presença
            cursor.execute('''
                INSERT INTO presencas (aluno_id, turma_id, data, presente)
                VALUES (?, ?, ?, ?)
            ''', (aluno_id, turma_id, data, presente))

        conn.commit()
        conn.close()

    @staticmethod
    def obter_presencas_por_turma_data(turma_id, data):
        """Obtém as presenças para todos os alunos de uma turma em uma data específica.
           Se não houver registro para um aluno, assume-se que está ausente."""
        conn = get_connection()
        cursor = conn.cursor()
        
        # Primeiro, obtém todos os alunos da turma
        cursor.execute('''
            SELECT a.id, a.nome 
            FROM alunos a
            JOIN aluno_turma at ON a.id = at.aluno_id
            WHERE at.turma_id = ?
        ''', (turma_id,))
        
        alunos = cursor.fetchall()
        
        resultado = []
        # Para cada aluno, verifica se tem presença naquela data
        for aluno_id, nome in alunos:
            cursor.execute('''
                SELECT presente
                FROM presencas
                WHERE aluno_id = ? AND turma_id = ? AND data = ?
            ''', (aluno_id, turma_id, data))
            
            presenca = cursor.fetchone()
            presente = presenca[0] if presenca else 0  # Se não encontrou, considera ausente
            resultado.append({"id": aluno_id, "nome": nome, "presente": bool(presente)})
        
        conn.close()
        return resultado

    @staticmethod
    def listar_presencas_por_aluno(aluno_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT data, presente FROM presencas
            WHERE aluno_id = ?
            ORDER BY data
        ''', (aluno_id,))
        resultados = cursor.fetchall()
        conn.close()
        return [{"data": row[0], "presente": bool(row[1])} for row in resultados]

    @staticmethod
    def listar_presencas_por_turma_data(turma_id, data):
        """Lista as presenças registradas para uma turma em uma data específica."""
        # Sempre use obter_presencas_por_turma_data para garantir que todos os alunos
        # atuais da turma sejam considerados, independentemente de quando foram registradas as presenças
        return [(aluno["nome"], aluno["presente"]) for aluno in PresencaController.obter_presencas_por_turma_data(turma_id, data)]

    @staticmethod
    def calcular_porcentagem_presenca(aluno_id, data_min, data_max):
        """Calcula a porcentagem de presença de um aluno em cada uma de suas turmas
           durante um período de datas."""
        conn = get_connection()
        cursor = conn.cursor()
        
        # Obtém todas as turmas do aluno
        cursor.execute('''
            SELECT t.id, t.nome 
            FROM turmas t
            JOIN aluno_turma at ON t.id = at.turma_id
            WHERE at.aluno_id = ?
        ''', (aluno_id,))
        
        turmas = cursor.fetchall()
        resultados = []
        
        for turma_id, turma_nome in turmas:
            # Conta quantos dias existem no período
            import datetime
            start_date = datetime.datetime.strptime(data_min, "%Y-%m-%d")
            end_date = datetime.datetime.strptime(data_max, "%Y-%m-%d")
            delta = end_date - start_date
            dias_periodo = delta.days + 1  # +1 para incluir o último dia
            
            if dias_periodo <= 0:
                # Se período inválido
                resultados.append({"turma": turma_nome, "porcentagem": 0.0})
                continue
            
            # Conta quantas presenças o aluno teve nesta turma no período
            cursor.execute('''
                SELECT COUNT(*)
                FROM presencas
                WHERE aluno_id = ? AND turma_id = ? AND data BETWEEN ? AND ? AND presente = 1
            ''', (aluno_id, turma_id, data_min, data_max))
            
            dias_presentes = cursor.fetchone()[0] or 0
            
            # Calcula a porcentagem baseada em todos os dias do período
            porcentagem = (dias_presentes / dias_periodo) * 100
            resultados.append({"turma": turma_nome, "porcentagem": round(porcentagem, 2)})
        
        conn.close()
        return resultados