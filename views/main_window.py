from PyQt5.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QLabel, QStackedWidget, QHBoxLayout, QApplication, QSpacerItem, QSizePolicy, QFrame
)
from PyQt5.QtCore import Qt  # Importação adicionada
from views.cadastro_turma import CadastroTurmaWindow
from views.cadastro_aluno import CadastroAlunoWindow
from views.marcar_presenca import MarcarPresencaWindow
from views.consultar_frequencia import ConsultarFrequenciaWindow

import sys

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Frequência de Alunos")
        self.setFixedSize(800, 600)  # Define um tamanho único para a janela
        self.setStyleSheet("background-color: #ffffff; font-size: 14px;")  # Fundo verde claro

        self.layout = QVBoxLayout()
        self.header_layout = QHBoxLayout()
        self.stack = QStackedWidget()  # Gerenciador de telas

        # Botão de voltar
        self.btn_voltar = QPushButton("←")
        self.btn_voltar.setFixedSize(30, 30)
        self.btn_voltar.clicked.connect(self.voltar_tela_principal)
        self.header_layout.addWidget(self.btn_voltar)
        self.header_layout.addStretch()  # Adiciona espaço vazio para alinhar o botão à esquerda
        self.layout.addLayout(self.header_layout)

        # Tela principal
        self.tela_principal = QWidget()
        self.tela_principal_layout = QVBoxLayout()

        # Adiciona espaçamento superior para centralizar o contêiner
        self.tela_principal_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Label principal
        self.label = QLabel("Sistema de Frequência de Alunos")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 32px; font-weight: bold; color: #000000;")  # Texto verde escuro
        self.tela_principal_layout.addWidget(self.label, alignment=Qt.AlignCenter)

        # Contêiner para os botões
        self.frame_botoes = QFrame()
        self.frame_botoes.setStyleSheet("background-color: #98fb98; border-radius: 10px;")  # Verde médio com bordas arredondadas
        self.frame_botoes.setFixedSize(300, 200)  # Aumenta o tamanho do contêiner
        self.frame_botoes_layout = QVBoxLayout()

        self.btn_cadastrar_turma = QPushButton("Cadastrar Turma")
        self.btn_cadastrar_aluno = QPushButton("Cadastrar Aluno")
        self.btn_marcar_presenca = QPushButton("Marcar Presença")
        self.btn_consultar_frequencia = QPushButton("Consultar Frequência")

        # Configura os botões para expandirem horizontalmente e adiciona estilo
        for btn in [self.btn_cadastrar_turma, self.btn_cadastrar_aluno, self.btn_marcar_presenca, self.btn_consultar_frequencia]:
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setStyleSheet("""
                background-color: #32cd32;  /* Verde vibrante */
                color: white;
                border: none;
                border-radius: 15px;
                padding: 10px;
            """)
            self.frame_botoes_layout.addWidget(btn)

        self.frame_botoes.setLayout(self.frame_botoes_layout)
        self.tela_principal_layout.addWidget(self.frame_botoes, alignment=Qt.AlignCenter)

        # Adiciona espaçamento inferior para centralizar o contêiner
        self.tela_principal_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.tela_principal.setLayout(self.tela_principal_layout)

        # Adiciona a tela principal ao stack
        self.stack.addWidget(self.tela_principal)

        # Conexões dos botões
        self.btn_cadastrar_turma.clicked.connect(self.abrir_cadastro_turma)
        self.btn_cadastrar_aluno.clicked.connect(self.abrir_cadastro_aluno)
        self.btn_marcar_presenca.clicked.connect(self.abrir_marcar_presenca)
        self.btn_consultar_frequencia.clicked.connect(self.abrir_consultar_frequencia)

        self.layout.addWidget(self.stack)
        self.setLayout(self.layout)

        # Inicialmente, o botão de voltar está oculto
        self.btn_voltar.hide()

    def adicionar_tela_secundaria(self, widget):
        """Adiciona uma tela secundária ao stack."""
        self.stack.addWidget(widget)
        self.stack.setCurrentWidget(widget)
        self.btn_voltar.show()  # Mostra o botão de voltar
        self.btn_voltar.setStyleSheet("""
                background-color: #f0f0f0;  /* Verde vibrante */
                color: black;
                padding: 10px;
            """)

    def voltar_tela_principal(self):
        """Retorna para a tela principal."""
        self.stack.setCurrentWidget(self.tela_principal)
        self.btn_voltar.hide()  # Oculta o botão de voltar

    def abrir_cadastro_turma(self):
        widget = CadastroTurmaWindow()
        self.adicionar_tela_secundaria(widget)

    def abrir_cadastro_aluno(self):
        widget = CadastroAlunoWindow()
        self.adicionar_tela_secundaria(widget)

    def abrir_marcar_presenca(self):
        widget = MarcarPresencaWindow()
        self.adicionar_tela_secundaria(widget)

    def abrir_consultar_frequencia(self):
        widget = ConsultarFrequenciaWindow()
        self.adicionar_tela_secundaria(widget)

# Código de teste direto
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
