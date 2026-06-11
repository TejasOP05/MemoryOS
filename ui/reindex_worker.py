from PyQt6.QtCore import QThread, pyqtSignal
from pipeline import Pipeline

class ReindexWorker(QThread):
    finished = pyqtSignal()

    def run(self):
        pipeline = Pipeline()
        pipeline.reindex_all()
        self.finished.emit()