from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QListWidget,
    QLabel,
    QListWidgetItem,
    QFileDialog,
    QApplication,
    QTextEdit
    )
from PyQt6.QtCore import Qt, QSize
from ui.reindex_worker import ReindexWorker
from ui.styles import MAIN_STYLE
from semantic_search import SemanticSearch
import os
from config_manager import ConfigManager
from pipeline import Pipeline
import time
from database import DatabaseManager


class MemoryOSWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.search_engine = SemanticSearch()
        self.config = ConfigManager()
        self.pipeline = Pipeline()
        
        self.setWindowTitle("🧠 MemoryOS")
        self.resize(1200, 700)

        self.setStyleSheet(MAIN_STYLE)

        self.setup_ui()

    def setup_ui(self):

        main_layout = QHBoxLayout()

        # Sidebar
        sidebar = QVBoxLayout()

        logo = QLabel("🧠 MemoryOS")
        logo.setStyleSheet(
            "font-size:24px;font-weight:bold;"
        )

        sidebar.addWidget(logo)

        self.search_page_btn = QPushButton("🔍 Search")
        self.search_page_btn.clicked.connect(self.show_search)
        
        self.ai_page_btn = QPushButton("🤖 AI Assistant")
        self.folder_page_btn = QPushButton("📂 Folders")
        self.folder_page_btn.clicked.connect(self.show_folders)
        
        self.settings_page_btn = QPushButton("⚙ Settings")

        sidebar.addWidget(self.search_page_btn)
        sidebar.addWidget(self.ai_page_btn)
        sidebar.addWidget(self.folder_page_btn)
        sidebar.addWidget(self.settings_page_btn)

        sidebar.addStretch()

        # Main Content
        content = QVBoxLayout()

        title = QLabel(
            "Search Your Digital Memory"
        )
        self.status_label = QLabel(
            "Status: Ready"
        )
        
        self.search_stats_label = QLabel(
            ""
        )
        
        self.db = DatabaseManager()
        file_count = self.db.count_files()
        chunk_count = self.db.count_chunks()
        folder_count = len(self.config.load_folders())
        
        dashboard_layout = QHBoxLayout()

        self.files_label = QLabel(
            f"📄 Files: {file_count}"
        )

        self.chunks_label = QLabel(
            f"🧩 Chunks: {chunk_count}"
        )

        self.folders_label = QLabel(
            f"📂 Folders: {folder_count}"
        )

        dashboard_layout.addWidget(
            self.files_label
        )

        dashboard_layout.addWidget(
            self.chunks_label
        )

        dashboard_layout.addWidget(
            self.folders_label
        )

        title.setStyleSheet(
            "font-size:22px;font-weight:bold;"
        )

        content.addWidget(title)
        content.addWidget(self.status_label)
        content.addWidget(self.search_stats_label)
        content.addLayout(dashboard_layout)

        search_layout = QHBoxLayout()

        self.search_box = QLineEdit()

        self.search_box.setPlaceholderText(
            "What are you looking for?"
        )

        self.search_button = QPushButton(
            "Search"
        )
        self.search_button.clicked.connect(
            self.perform_search
        )
        self.search_box.returnPressed.connect(
            self.perform_search
        )

        search_layout.addWidget(
            self.search_box
        )

        search_layout.addWidget(
            self.search_button
        )

        content.addLayout(
            search_layout
        )
        
        self.folder_list = QListWidget()
        self.folder_list.hide()

        
        # content.addWidget(
        #     self.results_list
        # )
        # self.results_list = QHBoxWidget()
        
        results_layout = QHBoxLayout()
        
        
        self.preview_panel = QTextEdit()
        self.preview_panel.setStyleSheet("""
            font-size: 14px;
            padding: 10px;
            """)
        self.preview_panel.setReadOnly(True)
        self.preview_panel.setPlainText(
            "Select a file for preview"
        )

        # self.preview_panel.QTextEdit()
        self.preview_panel.setReadOnly(True)
        
        self.preview_panel.setAlignment(
            Qt.AlignmentFlag.AlignTop
        )
        
        
        self.results_list = QListWidget()
        self.results_list.setSpacing(10)
        
        results_layout.addWidget(
            self.results_list,
            2
        )
        results_layout.addWidget(
            self.preview_panel,
            3
        )
        
        content.addLayout(
            results_layout
        )

        content.addWidget(
            self.folder_list
        )

        bottom_bar = QHBoxLayout()

        self.add_folder_btn = QPushButton(
            "📂 Add Folder"
        )
        self.add_folder_btn.clicked.connect(
            self.add_folder
        )
        
        self.remove_folder_btn = QPushButton(
            "🗑️ Remove Folder"
        )
        self.remove_folder_btn.clicked.connect(
            self.remove_folder
        )

        self.reindex_btn = QPushButton(
            "🔄 Reindex"
        )
        self.reindex_btn.clicked.connect(
            self.reindex_files
        )

        self.ai_btn = QPushButton(
            "🤖 Ask AI"
        )

        bottom_bar.addWidget(
            self.add_folder_btn
        )
        
        bottom_bar.addWidget(
            self.remove_folder_btn
        )

        bottom_bar.addWidget(
            self.reindex_btn
        )

        bottom_bar.addWidget(
            self.ai_btn
        )

        content.addLayout(
            bottom_bar
        )

        main_layout.addLayout(
            sidebar,
            1
        )

        main_layout.addLayout(
            content,
            4
        )

        self.setLayout(
            main_layout
        )

        
        
        self.results_list.itemDoubleClicked.connect(
            self.open_file
        )
        
        self.results_list.itemClicked.connect(
            self.show_preview
        )
        
        
        
# ----------------------------------------------------------------------------------------------------------------------------------------
        
        
        
    def perform_search(self):
        start_time = time.time()
        
        query = self.search_box.text()
        if not query:
            return
        
        self.results_list.clear()
        results = self.search_engine.search(query)

        search_time = round(time.time() - start_time, 2)

        if not results:
            self.results_list.addItem(
                "No results found."
            )
            self.search_stats_label.setText(
                "No results found."
            )
            return
        
        self.search_stats_label.setText(
            f"Found {len(results)} results in {search_time} seconds"
        )
        
        for filename, path, text, score in results:
            preview = text[:100]
            preview = preview.replace("\n", " ")
            folder = os.path.basename(os.path.dirname(path))
            item = QListWidgetItem(f"📄 {filename}\n📁 {folder}...")
            item.setSizeHint(QSize(100,70))
            item.setData(Qt.ItemDataRole.UserRole, path)  # Store the file path for later use
            item.setData(Qt.ItemDataRole.UserRole + 1, {"filename": filename, "text": text})  # Store the file path for later use
            self.results_list.addItem(item)

    def open_file(self, item):
        path = item.data(Qt.ItemDataRole.UserRole)
        os.startfile(path)
        
    def add_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Folder to Add"
        )
        if not folder:
            return
        self.config.save_folder(folder)
        print(f"Added folder: {folder}")
        
    # def reindex_files(self):
    #     self.status_label.setText("Status: Reindexing...")
    #     QApplication.processEvents()  # Update UI
    #     self.pipeline.reindex_all()
        
    #     self.status_label.setText("Status: Reloding Search Engine...")
    #     QApplication.processEvents()  # Update UI
    #     self.search_engine = SemanticSearch()
        
    #     self.refresh_dashboard()
    #     self.status_label.setText("Status: Ready")
    #     QApplication.processEvents()  # Update UI
        
    def reindex_files(self):
        self.status_label.setText(
            "Status: Reindexing..."
        )

        self.reindex_btn.setEnabled(
            False
        )

        self.worker = ReindexWorker()

        self.worker.finished.connect(
            self.reindex_finished
        )
        self.worker.start()
         
    def reindex_finished(self):
        self.status_label.setText(
            "Status: Reloading Search Engine..."
        )

        self.search_engine = SemanticSearch()

        self.refresh_dashboard()

        self.reindex_btn.setEnabled(
            True
        )

        self.status_label.setText(
            "Status: Ready"
        )
                
                
                
                
    def show_folders(self):
        self.results_list.hide()
        self.preview_panel.hide()
        self.folder_list.show()
        self.folder_list.clear()
        folders = self.config.load_folders()
        for folder in folders:
            self.folder_list.addItem(folder)
            
    def show_search(self):
        self.folder_list.hide()
        self.results_list.show()
        self.preview_panel.show()
        
    def remove_folder(self):
        item = self.folder_list.currentItem()
        if not item:
            return
        folder = item.text()
        self.config.remove_folder(folder)
        
        self.show_folders()
        
    def refresh_dashboard(self):

        db = DatabaseManager()

        self.files_label.setText(
            f"📄 Files: {db.count_files()}"
        )

        self.chunks_label.setText(
            f"🧩 Chunks: {db.count_chunks()}"
        )

        self.folders_label.setText(
            f"📂 Folders: {len(self.config.load_folders())}"
        )

        db.close()
        
    def show_preview(self, item):

        data = item.data(
            Qt.ItemDataRole.UserRole + 1
        )
        filename = data['filename']
        text = data['text']
        preview_text = (
            f"{filename}\n{'='*50}\n{text}"
        )
        self.preview_panel.setPlainText(
            preview_text
        )