from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QSpacerItem, QSizePolicy, QFrame
)
from PyQt5.QtCore import Qt
from controllers.turma_controller import TurmaController

class CadastroTurmaWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #ffffff; font-size: 14px;")  # Fundo branco
        self.layout = QVBoxLayout()

        # Adiciona espaçamento superior
        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Contêiner para o formulário
        self.frame_formulario = QFrame()
        self.frame_formulario.setStyleSheet("background-color: #98fb98; border-radius: 10px;")  # Verde médio com bordas arredondadas
        self.frame_formulario.setFixedSize(400, 200)
        self.frame_formulario_layout = QVBoxLayout()

        # Formulário
        self.label = QLabel("Nome da Turma:")
        self.label.setAlignment(Qt.AlignCenter)  # Centraliza o texto
        self.input_nome = QLineEdit()
        self.input_nome.setStyleSheet("""
            background-color: #ffffff;  /* Fundo branco */
            border: 2px solid #32cd32;  /* Verde vibrante */
            border-radius: 15px;
            padding: 10px;
            font-size: 16px;
            color: #000000;  /* Texto preto */
            min-width: 200px;  /* Largura mínima */
            max-width: 300px;  /* Largura máxima */
            min-height: 30px;  /* Altura mínima */
            max-height: 40px;  /* Altura máxima */
        """)
        self.input_nome.setAlignment(Qt.AlignCenter)  # Centraliza o texto no campo
        self.btn_cadastrar = QPushButton("Cadastrar")
        self.btn_cadastrar.setStyleSheet("""
            background-color: #32cd32;  /* Verde vibrante */
            color: white;
            border: none;
            border-radius: 15px;
            padding: 10px;
        """)

        self.frame_formulario_layout.addWidget(self.label, alignment=Qt.AlignCenter)
        self.frame_formulario_layout.addWidget(self.input_nome, alignment=Qt.AlignCenter)
        self.frame_formulario_layout.addWidget(self.btn_cadastrar, alignment=Qt.AlignCenter)

        self.frame_formulario.setLayout(self.frame_formulario_layout)
        self.layout.addWidget(self.frame_formulario, alignment=Qt.AlignCenter)

        # Adiciona espaçamento inferior
        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(self.layout)

        self.btn_cadastrar.clicked.connect(self.cadastrar_turma)

    def cadastrar_turma(self):
        nome = self.input_nome.text()

        try:
            TurmaController.criar_turma(nome)
            QMessageBox.information(self, "Sucesso", "Turma cadastrada com sucesso!")
            self.input_nome.clear()
        except ValueError as e:
            QMessageBox.warning(self, "Erro", str(e))
