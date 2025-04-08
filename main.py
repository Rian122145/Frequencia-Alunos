from PyQt5.QtWidgets import QApplication, QPushButton
from PyQt5.QtCore import Qt
import sys

from views.main_window import MainWindow
from models.database import create_tables

if __name__ == "__main__":
    create_tables()  # Cria as tabelas do SQLite

    app = QApplication(sys.argv)

    # Define um tema global para a aplicação
    app.setStyleSheet("""
        QWidget {
            background-color: #f5f5f5;  /* Fundo cinza claro */
            font-family: Arial, sans-serif;
            font-size: 14px;
        }
        QLabel {
            color: #333333;  /* Texto cinza escuro */
            font-weight: bold;
        }
        QPushButton {
            background-color: #4CAF50;  /* Verde moderno */
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px;
        }
        QPushButton:hover {
            background-color: #45a049;  /* Verde mais escuro ao passar o mouse */
        }
        QPushButton:pressed {
            background-color: #3e8e41;  /* Verde ainda mais escuro ao pressionar */
        }
        QFrame {
            background-color: #ffffff;  /* Fundo branco */
        }
        QScrollArea {
            border: none;
        }
    """)

    window = MainWindow()

    # Define o cursor de ponteiro para todos os botões
    for button in window.findChildren(QPushButton):
        button.setCursor(Qt.PointingHandCursor)

    window.show()
    sys.exit(app.exec_())
