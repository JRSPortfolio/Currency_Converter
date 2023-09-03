from interface import EuroInterface
from PyQt6.QtWidgets import QApplication
import sys

def main():
    app = QApplication(sys.argv)
    window = EuroInterface()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':         
    main()
