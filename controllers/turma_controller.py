from models.turma import Turma  # Importa a classe Turma
from models.database import get_connection


class TurmaController:
    @staticmethod
    def criar_turma(nome):
        if not nome.strip():
            raise ValueError("O nome da turma não pode ser vazio.")
        Turma.adicionar(nome)

    @staticmethod
    def listar_turmas():
        return [Turma(id=row[0], nome=row[1]) for row in Turma.listar()]

    @staticmethod
    def buscar_turma(turma_id):
        return Turma.buscar_por_id(turma_id)
