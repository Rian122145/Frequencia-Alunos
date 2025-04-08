from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QComboBox, QDateEdit, QCheckBox, QMessageBox, QScrollArea, QSpacerItem, QSizePolicy, QFrame
)
from PyQt5.QtCore import QDate, Qt

from controllers.turma_controller import TurmaController
from controllers.aluno_controller import AlunoController
from controllers.presenca_controller import PresencaController


class MarcarPresencaWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #ffffff; font-size: 14px;")  # Fundo branco
        self.layout = QVBoxLayout()

        # Adiciona espaçamento superior
        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Contêiner para o formulário
        self.frame_formulario = QFrame()
        self.frame_formulario.setStyleSheet("background-color: #98fb98; border-radius: 10px;")  # Verde médio com bordas arredondadas
        self.frame_formulario.setFixedSize(500, 500)
        self.frame_formulario_layout = QVBoxLayout()

        # Formulário
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
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setStyleSheet("""
            background-color: #ffffff;  /* Fundo branco */
            border: 2px solid #32cd32;  /* Verde vibrante */
            border-radius: 15px;
            padding: 10px;
            font-size: 16px;
            color: #000000;  /* Texto preto */
        """)

        self.checkboxes_alunos = []
        self.scroll_area = QScrollArea()
        self.scroll_widget = QWidget()
        self.scroll_widget.setStyleSheet("background-color: #ffffff;")  # Fundo branco
        self.scroll_widget.setFixedWidth(400)

        self.scroll_area.setStyleSheet("""
            QScrollArea {
            background-color: #ffffff;  /* Fundo branco */
            border: 2px solid #32cd32;  /* Verde vibrante */
            border-radius: 15px;
            }
            QScrollBar:vertical {
            border: none;
            background: #f0f0f0;  /* Cinza claro */
            width: 10px;
            margin: 0px;
            }
            QScrollBar::handle:vertical {
            background: #32cd32;  /* Verde vibrante */
            border-radius: 5px;
            min-height: 20px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;  /* Remove botões de incremento/decremento */
            }
        """)
        self.scroll_area.setFixedSize(400, 200)
        self.scroll_area.setFrameShape(QScrollArea.NoFrame)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_layout = QVBoxLayout(self.scroll_widget)

        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_widget)

        self.btn_carregar_alunos = QPushButton("Carregar Alunos")
        self.btn_carregar_alunos.setStyleSheet("""
            background-color: #32cd32;  /* Verde vibrante */
            color: white;
            border: none;
            border-radius: 15px;
            padding: 10px;
        """)
        
        self.btn_salvar = QPushButton("Salvar Presença")
        self.btn_salvar.setStyleSheet("""
            background-color: #32cd32;  /* Verde vibrante */
            color: white;
            border: none;
            border-radius: 15px;
            padding: 10px;
        """)

        self.frame_formulario_layout.addWidget(QLabel("Turma:"), alignment=Qt.AlignCenter)
        self.frame_formulario_layout.addWidget(self.combo_turma, alignment=Qt.AlignCenter)
        self.frame_formulario_layout.addWidget(QLabel("Data:"), alignment=Qt.AlignCenter)
        self.frame_formulario_layout.addWidget(self.date_edit, alignment=Qt.AlignCenter)
        self.frame_formulario_layout.addWidget(self.btn_carregar_alunos, alignment=Qt.AlignCenter)
        self.frame_formulario_layout.addWidget(QLabel("Alunos:"), alignment=Qt.AlignCenter)
        self.frame_formulario_layout.addWidget(self.scroll_area, alignment=Qt.AlignCenter)
        self.frame_formulario_layout.addWidget(self.btn_salvar, alignment=Qt.AlignCenter)

        self.frame_formulario.setLayout(self.frame_formulario_layout)
        self.layout.addWidget(self.frame_formulario, alignment=Qt.AlignCenter)

        # Adiciona espaçamento inferior
        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(self.layout)

        self.btn_carregar_alunos.clicked.connect(self.carregar_alunos)
        self.btn_salvar.clicked.connect(self.salvar_presenca)

        self.carregar_turmas()

    def carregar_turmas(self):
        turmas = TurmaController.listar_turmas()
        self.combo_turma.clear()
        for turma in turmas:
            self.combo_turma.addItem(turma.nome, turma.id)

    def carregar_alunos(self):
        try:
            turma_id = self.combo_turma.currentData()
            data = self.date_edit.date().toString("yyyy-MM-dd")
            
            if turma_id is None:
                return

            # Remove os widgets antigos do layout de alunos
            for i in reversed(range(self.scroll_layout.count())):
                widget = self.scroll_layout.itemAt(i).widget()
                if widget is not None:
                    widget.setParent(None)

            # Obtém todos os alunos da turma com suas presenças para a data selecionada
            presencas = PresencaController.obter_presencas_por_turma_data(turma_id, data)
            
            self.checkboxes_alunos = []

            for presenca in presencas:
                checkbox = QCheckBox(presenca["nome"])
                checkbox.setProperty("aluno_id", presenca["id"])
                checkbox.setChecked(presenca["presente"])  # Marca se o aluno esteve presente
                self.scroll_layout.addWidget(checkbox)
                self.checkboxes_alunos.append(checkbox)

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar alunos: {str(e)}")

    def salvar_presenca(self):
        turma_id = self.combo_turma.currentData()
        data = self.date_edit.date().toString("yyyy-MM-dd")
        presencas = []

        for checkbox in self.checkboxes_alunos:
            aluno_id = checkbox.property("aluno_id")
            presente = checkbox.isChecked()
            presencas.append((aluno_id, turma_id, data, presente))

        try:
            for aluno_id, turma_id, data, presente in presencas:
                PresencaController.registrar_presenca(aluno_id, turma_id, data, presente)
            QMessageBox.information(self, "Sucesso", "Presenças salvas com sucesso!")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao salvar presença: {str(e)}")
