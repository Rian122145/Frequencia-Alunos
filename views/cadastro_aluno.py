from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QMessageBox, QSizePolicy, QSpacerItem, QFrame, QTabWidget
)
from PyQt5.QtCore import Qt
from controllers.turma_controller import TurmaController
from controllers.aluno_controller import AlunoController

class CadastroAlunoWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #ffffff; font-size: 14px;")  # Fundo branco
        self.layout = QVBoxLayout()

        # Adiciona espaçamento superior
        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Contêiner para o formulário
        self.frame_formulario = QFrame()
        self.frame_formulario.setStyleSheet("background-color: #98fb98; border-radius: 10px;")  # Verde médio com bordas arredondadas
        self.frame_formulario.setFixedSize(400, 300)
        self.frame_formulario_layout = QVBoxLayout()

        # Formulário para o novo aluno
        self.label_nome = QLabel("Nome do Aluno:")
        self.label_nome.setAlignment(Qt.AlignCenter)
        self.input_nome = QLineEdit()
        self.input_nome.setStyleSheet("""
            background-color: #ffffff;  /* Fundo branco */
            border: 2px solid #32cd32;  /* Verde vibrante */
            border-radius: 15px;
            padding: 10px;
            font-size: 16px;
            color: #000000;  /* Texto preto */
            min-width: 200px;  /* Largura mínima */
            min-height: 30px;  /* Altura mínima */
        """)
        self.input_nome.setAlignment(Qt.AlignCenter)

        self.btn_cadastrar = QPushButton("Cadastrar")
        self.btn_cadastrar.setStyleSheet("""
            background-color: #32cd32;  /* Verde vibrante */
            color: white;
            border: none;
            border-radius: 15px;
            padding: 10px;
        """)

        # Formulário para associar aluno à turma
        self.label_turma = QLabel("Turma:")
        self.label_turma.setAlignment(Qt.AlignCenter)
        self.combo_turma = QComboBox()
        self.combo_turma.setStyleSheet("""
            background-color: #ffffff;  /* Fundo branco */
            border: 2px solid #32cd32;  /* Verde vibrante */
            border-radius: 15px;
            padding: 10px;
            font-size: 16px;
            color: #000000;  /* Texto preto */
            min-width: 200px;  /* Largura mínima */
            min-height: 30px;  /* Altura mínima */
        """)

        self.btn_adicionar_turma = QPushButton("Adicionar à Turma")
        self.btn_adicionar_turma.setStyleSheet("""
            background-color: #32cd32;
            color: white;
            border: none;
            border-radius: 15px;
            padding: 10px;
        """)

        # Criar combo box para selecionar aluno existente
        self.label_aluno_existente = QLabel("Aluno Existente:")
        self.label_aluno_existente.setAlignment(Qt.AlignCenter)
        self.combo_aluno = QComboBox()
        self.combo_aluno.setStyleSheet("""
            background-color: #ffffff;
            border: 2px solid #32cd32;
            border-radius: 15px;
            padding: 10px;
            font-size: 16px;
            color: #000000;
            min-width: 200px;
            min-height: 30px;
        """)

        # Adiciona abas para escolher entre criar novo aluno ou adicionar turma
        self.tabs = QTabWidget()

        # Aba de novo aluno
        self.tab_novo = QWidget()
        self.tab_novo_layout = QVBoxLayout()
        self.tab_novo_layout.addWidget(self.label_nome, alignment=Qt.AlignCenter)
        self.tab_novo_layout.addWidget(self.input_nome, alignment=Qt.AlignCenter)
        self.tab_novo_layout.addWidget(self.btn_cadastrar, alignment=Qt.AlignCenter)
        self.tab_novo.setLayout(self.tab_novo_layout)

        # Aba de adicionar turma
        self.tab_adicionar = QWidget()
        self.tab_adicionar_layout = QVBoxLayout()
        self.tab_adicionar_layout.addWidget(self.label_aluno_existente, alignment=Qt.AlignCenter)
        self.tab_adicionar_layout.addWidget(self.combo_aluno, alignment=Qt.AlignCenter)
        self.tab_adicionar_layout.addWidget(self.label_turma, alignment=Qt.AlignCenter)
        self.tab_adicionar_layout.addWidget(self.combo_turma, alignment=Qt.AlignCenter)
        self.tab_adicionar_layout.addWidget(self.btn_adicionar_turma, alignment=Qt.AlignCenter)
        self.tab_adicionar.setLayout(self.tab_adicionar_layout)

        self.tabs.addTab(self.tab_novo, "Novo Aluno")
        self.tabs.addTab(self.tab_adicionar, "Adicionar à Turma")

        self.frame_formulario_layout.addWidget(self.tabs)

        self.frame_formulario.setLayout(self.frame_formulario_layout)
        self.layout.addWidget(self.frame_formulario, alignment=Qt.AlignCenter)

        # Adiciona espaçamento inferior
        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(self.layout)

        self.btn_cadastrar.clicked.connect(self.cadastrar_aluno)
        self.btn_adicionar_turma.clicked.connect(self.adicionar_aluno_turma)

        self.carregar_turmas()
        self.carregar_alunos_existentes()

    def carregar_turmas(self):
        try:
            turmas = TurmaController.listar_turmas()
            self.combo_turma.clear()
            for turma in turmas:
                self.combo_turma.addItem(turma.nome, turma.id)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar turmas: {str(e)}")

    def carregar_alunos_existentes(self):
        try:
            alunos = AlunoController.listar_todos_alunos()
            self.combo_aluno.clear()
            for aluno in alunos:
                self.combo_aluno.addItem(aluno.nome, aluno.id)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar alunos: {str(e)}")

    def cadastrar_aluno(self):
        nome = self.input_nome.text().strip()

        if not nome:
            QMessageBox.warning(self, "Erro", "O nome do aluno não pode ser vazio.")
            return

        try:
            AlunoController.criar_aluno(nome)
            QMessageBox.information(self, "Sucesso", "Aluno cadastrado com sucesso!")
            self.input_nome.clear()
            # Atualiza a lista de alunos existentes após cadastro
            self.carregar_alunos_existentes()
        except ValueError as e:
            QMessageBox.warning(self, "Erro", str(e))

    def adicionar_aluno_turma(self):
        aluno_id = self.combo_aluno.currentData()
        turma_id = self.combo_turma.currentData()

        try:
            AlunoController.adicionar_aluno_turma(aluno_id, turma_id)
            QMessageBox.information(self, "Sucesso", "Aluno adicionado à turma com sucesso!")
        except ValueError as e:
            QMessageBox.warning(self, "Erro", str(e))
