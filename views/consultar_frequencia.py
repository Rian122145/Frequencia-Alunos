from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox, QSpacerItem, QSizePolicy, 
    QFrame, QHeaderView, QDateEdit
)
from PyQt5.QtCore import Qt, QDate
from controllers.turma_controller import TurmaController
from controllers.aluno_controller import AlunoController
from controllers.presenca_controller import PresencaController


class ConsultarFrequenciaWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #ffffff; font-size: 14px;")
        self.layout = QVBoxLayout()

        # Botões de alternância no topo
        self.header_layout = QHBoxLayout()
        self.btn_por_turma_data = self.criar_botao("Por Turma e Data")
        self.btn_por_aluno = self.criar_botao("Por Aluno")
        self.header_layout.addWidget(self.btn_por_turma_data)
        self.header_layout.addWidget(self.btn_por_aluno)
        self.layout.addLayout(self.header_layout)

        # Contêiner para as telas
        self.frame_formulario = QFrame()
        self.frame_formulario.setStyleSheet("background-color: #98fb98; border-radius: 10px;")
        self.frame_formulario.setFixedSize(600, 500)
        self.frame_formulario_layout = QVBoxLayout()
        self.frame_formulario.setLayout(self.frame_formulario_layout)
        self.layout.addWidget(self.frame_formulario, alignment=Qt.AlignCenter)

        # Adiciona espaçamento inferior
        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.setLayout(self.layout)

        # Conexões
        self.btn_por_turma_data.clicked.connect(self.mostrar_tela_por_turma_data)
        self.btn_por_aluno.clicked.connect(self.mostrar_tela_por_aluno)

        # Inicialmente, exibe a tela "Por Turma e Data"
        self.mostrar_tela_por_turma_data()
    
    def criar_botao(self, texto):
        """Cria um botão com estilo padrão"""
        btn = QPushButton(texto)
        btn.setStyleSheet("""
            background-color: #32cd32;
            color: white;
            border: none;
            border-radius: 15px;
            padding: 10px;
        """)
        return btn
    
    def criar_combo_box(self):
        """Cria um combo box com estilo padrão"""
        combo = QComboBox()
        combo.setStyleSheet("""
            background-color: #ffffff;
            border: 2px solid #32cd32;
            border-radius: 15px;
            padding: 10px;
            font-size: 16px;
            color: #000000;
        """)
        return combo
    
    def criar_date_edit(self):
        """Cria um date edit com estilo padrão"""
        date_edit = QDateEdit()
        date_edit.setDate(QDate.currentDate())
        date_edit.setCalendarPopup(True)
        date_edit.setStyleSheet("""
            background-color: #ffffff;
            border: 2px solid #32cd32;
            border-radius: 15px;
            padding: 10px;
            font-size: 16px;
            color: #000000;
        """)
        return date_edit
    
    def criar_tabela(self, colunas):
        """Cria uma tabela com estilo padrão"""
        tabela = QTableWidget()
        tabela.setColumnCount(len(colunas))
        tabela.setHorizontalHeaderLabels(colunas)
        tabela.horizontalHeader().setStyleSheet("""
            QHeaderView::section { background-color: #32cd32; color: white; padding: 10px; }
        """)
        tabela.setStyleSheet("""
            QTableWidget { background-color: #ffffff; border: 2px solid #32cd32; border-radius: 15px; }
        """)
        tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        return tabela

    def criar_tela_por_turma_data(self):
        """Cria a tela para consulta por turma e data."""
        layout = QVBoxLayout()

        # Formulário
        form_layout = QVBoxLayout()
        self.combo_turma = self.criar_combo_box()
        self.carregar_turmas()
        self.date_edit_turma = self.criar_date_edit()
        
        btn_consultar_turma = self.criar_botao("Consultar")
        btn_consultar_turma.clicked.connect(self.consultar_por_turma_data)
        
        form_layout.addWidget(QLabel("Turma:"))
        form_layout.addWidget(self.combo_turma)
        form_layout.addWidget(QLabel("Data:"))
        form_layout.addWidget(self.date_edit_turma)
        form_layout.addWidget(btn_consultar_turma, alignment=Qt.AlignCenter)

        # Tabela de resultados
        self.tabela_frequencia = self.criar_tabela(["Aluno", "Presente"])

        layout.addLayout(form_layout)
        layout.addWidget(self.tabela_frequencia)
        return layout

    def criar_tela_por_aluno(self):
        """Cria a tela para consulta por aluno."""
        layout = QVBoxLayout()

        # Formulário
        form_layout = QVBoxLayout()
        self.combo_aluno = self.criar_combo_box()
        self.carregar_alunos()
        self.date_edit_min = self.criar_date_edit()
        self.date_edit_max = self.criar_date_edit()
        
        btn_consultar_aluno = self.criar_botao("Consultar")
        btn_consultar_aluno.clicked.connect(self.consultar_por_aluno)
        
        form_layout.addWidget(QLabel("Aluno:"))
        form_layout.addWidget(self.combo_aluno)
        form_layout.addWidget(QLabel("Data:"))
        form_layout.addWidget(self.date_edit_min)
        form_layout.addWidget(QLabel("até"))
        form_layout.addWidget(self.date_edit_max)
        form_layout.addWidget(btn_consultar_aluno, alignment=Qt.AlignCenter)

        # Tabela de resultados
        self.tabela_frequencia = self.criar_tabela(["Turma", "Porcentagem"])

        layout.addLayout(form_layout)
        layout.addWidget(self.tabela_frequencia)
        return layout

    def mostrar_tela_por_turma_data(self):
        """Exibe a tela de consulta por turma e data."""
        self.limpar_layout(self.frame_formulario_layout)
        novo_layout = self.criar_tela_por_turma_data()
        self.frame_formulario_layout.addLayout(novo_layout)

    def mostrar_tela_por_aluno(self):
        """Exibe a tela de consulta por aluno."""
        self.limpar_layout(self.frame_formulario_layout)
        novo_layout = self.criar_tela_por_aluno()
        self.frame_formulario_layout.addLayout(novo_layout)

    def limpar_layout(self, layout):
        """Remove todos os widgets de um layout."""
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            elif item.layout() is not None:
                self.limpar_layout(item.layout())

    def carregar_turmas(self):
        try:
            turmas = TurmaController.listar_turmas()
            self.combo_turma.clear()
            for turma in turmas:
                self.combo_turma.addItem(turma.nome, turma.id)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar turmas: {str(e)}")

    def carregar_alunos(self):
        try:
            alunos = AlunoController.listar_todos_alunos()
            self.combo_aluno.clear()
            for aluno in alunos:
                self.combo_aluno.addItem(aluno.nome, aluno.id)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar alunos: {str(e)}")

    def consultar_por_turma_data(self):
        turma_id = self.combo_turma.currentData()
        data = self.date_edit_turma.date().toString("yyyy-MM-dd")

        if not turma_id:
            QMessageBox.warning(self, "Aviso", "Por favor, selecione uma turma.")
            return

        try:
            presencas = PresencaController.listar_presencas_por_turma_data(turma_id, data)
            self.tabela_frequencia.setRowCount(0)
            for i, presenca in enumerate(presencas):
                self.tabela_frequencia.insertRow(i)
                self.tabela_frequencia.setItem(i, 0, QTableWidgetItem(presenca[0]))
                self.tabela_frequencia.setItem(i, 1, QTableWidgetItem("Sim" if presenca[1] else "Não"))
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao consultar frequência: {str(e)}")

    def consultar_por_aluno(self):
        aluno_id = self.combo_aluno.currentData()
        data_min = self.date_edit_min.date().toString("yyyy-MM-dd")
        data_max = self.date_edit_max.date().toString("yyyy-MM-dd")
        
        if not aluno_id:
            QMessageBox.warning(self, "Aviso", "Por favor, selecione um aluno.")
            return
            
        try:
            relatorio = PresencaController.calcular_porcentagem_presenca(aluno_id, data_min, data_max)
            self.tabela_frequencia.setRowCount(0)
            for i, item in enumerate(relatorio):
                self.tabela_frequencia.insertRow(i)
                self.tabela_frequencia.setItem(i, 0, QTableWidgetItem(item["turma"]))
                self.tabela_frequencia.setItem(i, 1, QTableWidgetItem(f"{item['porcentagem']}%"))
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao consultar relatório: {str(e)}")
