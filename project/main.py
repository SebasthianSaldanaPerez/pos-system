import ctypes
import os
import sys
from PySide6.QtGui import QIcon, QFont
from PySide6.QtWidgets import QApplication
from dotenv import load_dotenv

from database.connection import create_database_if_not_exists, Connection
from database.init_db import init_db
from ui.main_window import MainWindow


def main_database():
    create_database_if_not_exists()
    Connection.initialize()
    init_db()


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


if __name__ == '__main__':
    main_database()
    myappid = 'vicky.pos.app'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(resource_path('ui/assets/main_icon.ico')))
    app.setStyleSheet("""
    QWidget {
        background-color: white;
        font-size: 10pt;
        color: #2c3e50;
    }

    QLineEdit {
        padding: 6px 10px;
        border-radius: 8px;
        border: 1px solid #ddd;
        font-size: 10pt;
        color: #2c3e50;
        background-color: white;
    }

    QLineEdit:focus {
        border: 1px solid #3498db;
    }

    QPushButton {
        padding: 10px;
        font-size: 10pt;
        color: #2c3e50;
        border-radius: 8px;
    }

    QPushButton:hover {
        background-color: #f0f0f0;
    }

    QCheckBox {
        font-size: 10pt;
        color: #2c3e50;
    }

    QMenuBar {
        background-color: #ffffff;
        border-bottom: 1px solid #e0e0e0;
        padding: 6px;
        font-size: 10pt;
        color: #2c3e50;
    }

    QMenuBar::item {
        background-color: transparent;
        padding: 8px 14px;
        margin: 2px;
        border-radius: 6px;
    }

    QMenuBar::item:selected {
        background-color: #f0f4ff;
        color: #2c3e50;
    }

    QMenu {
        background-color: white;
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 6px;
        font-size: 10pt;
        color: #2c3e50;
    }

    QMenu::item {
        padding: 10px 20px;
        border-radius: 6px;
    }

    QMenu::item:selected {
        background-color: #e8f0fe;
    }

    QTableWidget {
        background-color: white;
        border-radius: 10px;
        gridline-color: #eee;
        font-size: 10pt;
        color: #2c3e50;
    }

    QHeaderView::section {
        background-color: #f8f9fa;
        padding: 8px;
        border: none;
        font-weight: bold;
        color: #2c3e50;
    }

    QTableWidget::item:selected {
        background-color: #d0e7ff;
        color: black;
    }

    QTableWidget::item:hover {
        background-color: #f5f5f5;
    }
    
    QScrollBar:vertical {
    background: transparent;
    width: 10px;
    margin: 4px 0 4px 0;
}

QScrollBar::handle:vertical {
    background: #cfd8dc;
    border-radius: 5px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background: #3498db;
}

QScrollBar::handle:vertical:pressed {
    background: #2980b9;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {
    background: none;
}
    """)
    font = QFont()
    font.setPointSize(12)
    app.setFont(font)
    window = MainWindow()
    window.showMaximized()
    load_dotenv()
    app.exec()

