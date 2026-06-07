import sys

from PyQt6.QtWidgets import QApplication

from ui.main_window import MemoryOSWindow


app = QApplication(sys.argv)

window = MemoryOSWindow()

window.show()

sys.exit(app.exec())