from models.aluno import Aluno
from models.turma import Turma

class AlunoController:
    @staticmethod
    def criar_aluno(nome):
        if not nome.strip():
            raise ValueError("O nome do aluno não pode ser vazio.")
        return Aluno.adicionar(nome)

    @staticmethod
    def adicionar_aluno_turma(aluno_id, turma_id):
        if not Turma.buscar_por_id(turma_id):
            raise ValueError("Turma não encontrada.")
        if not Aluno.buscar_por_id(aluno_id):
            raise ValueError("Aluno não encontrado.")
        return Aluno.adicionar_turma(aluno_id, turma_id)

    @staticmethod
    def listar_alunos_por_turma(turma_id):
        alunos_data = Aluno.listar_por_turma(turma_id)
        return [Aluno(id=row[0], nome=row[1]) for row in alunos_data]

    @staticmethod
    def listar_turmas_por_aluno(aluno_id):
        from models.turma import Turma
        turmas_data = Aluno.listar_turmas_por_aluno(aluno_id)
        return [Turma(id=row[0], nome=row[1]) for row in turmas_data]

    @staticmethod
    def buscar_aluno(aluno_id):
        dados = Aluno.buscar_por_id(aluno_id)
        if dados:
            return Aluno(id=dados[0], nome=dados[1])
        return None

    @staticmethod
    def listar_todos_alunos():
        """Lista todos os alunos independentemente da turma."""
        alunos_data = Aluno.listar_todos()
        return [Aluno(id=row[0], nome=row[1]) for row in alunos_data]
