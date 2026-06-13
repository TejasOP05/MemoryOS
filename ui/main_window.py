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
    QTextEdit,
    QComboBox,
    QStackedWidget,
    QMessageBox,
    QProgressBar
)
from PyQt6.QtCore import Qt, QSize
from ui.reindex_worker import ReindexWorker
from ui.styles import MAIN_STYLE
from semantic_search import SemanticSearch
from config_manager import ConfigManager
from pipeline import Pipeline
from database import DatabaseManager
import os
import time


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

    # ------------------------------------------------------------------ #
    #  UI Setup                                                            #
    # ------------------------------------------------------------------ #

    def setup_ui(self):
        root = QHBoxLayout(self)
        root.addLayout(self._build_sidebar(), 1)
        root.addLayout(self._build_content(), 4)

    # -- Sidebar -------------------------------------------------------- #

    def _build_sidebar(self):
        layout = QVBoxLayout()

        logo = QLabel("🧠 MemoryOS")
        logo.setStyleSheet("font-size:24px; font-weight:bold;")
        layout.addWidget(logo)

        nav_buttons = [
            ("🔍 Search",       self.show_search),
            ("🤖 AI Assistant", self.show_ai),
            ("📂 Folders",      self.show_folders),
            ("⚙ Settings",     self.show_settings),
        ]
        for label, slot in nav_buttons:
            btn = QPushButton(label)
            btn.clicked.connect(slot)
            layout.addWidget(btn)

        layout.addStretch()
        return layout

    # -- Content area --------------------------------------------------- #

    def _build_content(self):
        layout = QVBoxLayout()

        # Dashboard header (always visible)
        layout.addWidget(self._build_dashboard())

        # Stacked pages
        self.pages = QStackedWidget()
        self.pages.addWidget(self._build_search_page())   # index 0
        self.pages.addWidget(self._build_ai_page())        # index 1
        self.pages.addWidget(self._build_folders_page())   # index 2
        self.pages.addWidget(self._build_settings_page())  # index 3
        layout.addWidget(self.pages)

        # Bottom action bar (always visible)
        layout.addLayout(self._build_bottom_bar())

        return layout

    def _build_dashboard(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel("Search Your Digital Memory")
        title.setStyleSheet("font-size:22px; font-weight:bold;")
        layout.addWidget(title)

        self.status_label = QLabel("Status: Ready")
        layout.addWidget(self.status_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)

        self.search_stats_label = QLabel("")
        layout.addWidget(self.search_stats_label)

        db = DatabaseManager()
        stats_row = QHBoxLayout()
        self.files_label  = QLabel(f"📄 Files: {db.count_files()}")
        self.chunks_label = QLabel(f"🧩 Chunks: {db.count_chunks()}")
        self.folders_label = QLabel(f"📂 Folders: {len(self.config.load_folders())}")
        for lbl in (self.files_label, self.chunks_label, self.folders_label):
            stats_row.addWidget(lbl)
        layout.addLayout(stats_row)

        return widget

    # -- Pages ---------------------------------------------------------- #

    def _build_search_page(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Search bar
        bar = QHBoxLayout()
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("What are you looking for?")
        self.search_box.returnPressed.connect(self.perform_search)

        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self.perform_search)

        bar.addWidget(self.search_box)
        bar.addWidget(search_btn)
        layout.addLayout(bar)

        # Results + preview
        results_row = QHBoxLayout()

        self.results_list = QListWidget()
        self.results_list.setSpacing(10)
        self.results_list.itemClicked.connect(self.show_preview)
        self.results_list.itemDoubleClicked.connect(self.open_file)

        self.preview_panel = QTextEdit()
        self.preview_panel.setStyleSheet("font-size:14px; padding:10px;")
        self.preview_panel.setReadOnly(True)
        self.preview_panel.setPlainText("Select a file to preview")

        results_row.addWidget(self.results_list, 2)
        results_row.addWidget(self.preview_panel, 3)
        layout.addLayout(results_row)

        return widget

    def _build_ai_page(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        title = QLabel("🤖 AI Assistant")
        title.setStyleSheet("font-size:20px; font-weight:bold;")
        layout.addWidget(title)

        layout.addWidget(QLabel("AI Assistant coming soon."))
        layout.addStretch()
        return widget

    def _build_folders_page(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        title = QLabel("📂 Folders")
        title.setStyleSheet("font-size:20px; font-weight:bold;")
        layout.addWidget(title)

        self.folder_list = QListWidget()
        layout.addWidget(self.folder_list)

        return widget

    def _build_settings_page(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        title = QLabel("⚙ Settings")
        title.setStyleSheet("font-size:20px; font-weight:bold;")
        layout.addWidget(title)

        # Theme Dropdown
        layout.addWidget(QLabel("Theme"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light"])
        self.theme_combo.currentTextChanged.connect(self.change_theme)
        layout.addWidget(self.theme_combo)
        layout.addSpacing(20)
        
        # Statistical Info
        stats_title = QLabel("Database Information")
        stats_title.setStyleSheet("font-size:20px; font-weight:bold")
        layout.addWidget(stats_title)
        self.settings_stats_label = QLabel()
        layout.addWidget(self.settings_stats_label)
        layout.addSpacing(20)
        
        # Reset Data
        clear_btn = QPushButton("🗑️ Clear Indexed Data")
        clear_btn.clicked.connect(self.clear_indexed_data)
        layout.addWidget(clear_btn)
        layout.addSpacing(20)

        layout.addStretch()
        return widget

    def _build_bottom_bar(self):
        bar = QHBoxLayout()
        buttons = [
            ("📂 Add Folder",    self.add_folder),
            ("🗑️ Remove Folder", self.remove_folder),
            ("🔄 Reindex",       self.reindex_files),
            ("🤖 Ask AI",        self.show_ai),
        ]
        for label, slot in buttons:
            btn = QPushButton(label)
            btn.clicked.connect(slot)
            if label == "🔄 Reindex":
                self.reindex_btn = btn          # keep ref to toggle enabled state
            bar.addWidget(btn)
        return bar

    # ------------------------------------------------------------------ #
    #  Navigation                                                          #
    # ------------------------------------------------------------------ #

    def show_search(self):
        self.reset_preview()
        self.pages.setCurrentIndex(0)

    def show_ai(self):
        self.reset_preview()
        self.pages.setCurrentIndex(1)

    def show_folders(self):
        self.reset_preview()
        self.pages.setCurrentIndex(2)
        self._refresh_folder_list()

    def show_settings(self):
        self.reset_preview()
        self.refresh_settings_stats()
        self.pages.setCurrentIndex(3)

    # ------------------------------------------------------------------ #
    #  Actions                                                             #
    # ------------------------------------------------------------------ #

    def perform_search(self):
        query = self.search_box.text().strip()
        if not query:
            return

        self.show_search()
        self.results_list.clear()

        start = time.time()
        results = self.search_engine.search(query)
        elapsed = round(time.time() - start, 2)

        if not results:
            self.results_list.addItem("No results found.")
            self.search_stats_label.setText("No results found.")
            return

        self.search_stats_label.setText(
            f"Found {len(results)} results in {elapsed}s"
        )

        for filename, path, text, score in results:
            folder = os.path.basename(os.path.dirname(path))
            item = QListWidgetItem(f"📄 {filename}\n📁 {folder}")
            item.setSizeHint(QSize(100, 70))
            item.setData(Qt.ItemDataRole.UserRole,     path)
            item.setData(Qt.ItemDataRole.UserRole + 1, {"filename": filename, "text": text})
            self.results_list.addItem(item)

    def open_file(self, item):
        path = item.data(Qt.ItemDataRole.UserRole)
        os.startfile(path)

    def show_preview(self, item):
        data = item.data(Qt.ItemDataRole.UserRole + 1)
        self.preview_panel.setPlainText(
            f"{data['filename']}\n\n{'━' * 50}\n\n{data['text']}"
        )

    def add_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder to Add")
        if folder:
            self.config.save_folder(folder)
            self.refresh_dashboard()

    def remove_folder(self):
        item = self.folder_list.currentItem()
        if not item:
            return
        self.config.remove_folder(item.text())
        self._refresh_folder_list()
        self.refresh_dashboard()

    def reindex_files(self):
        self.status_label.setText("Status: Reindexing…")
        self.progress_bar.show()
        self.progress_bar.setRange(0,0) 
        self.reindex_btn.setEnabled(False)

        self.worker = ReindexWorker()
        self.worker.finished.connect(self._on_reindex_finished)
        self.worker.start()

    def _on_reindex_finished(self):
        self.status_label.setText("Status: Reloading search engine…")
        self.search_engine = SemanticSearch()
        self.refresh_dashboard()
        self.progress_bar.hide()
        self.reindex_btn.setEnabled(True)
        self.status_label.setText("Status: Ready")

    def change_theme(self, theme):
        from ui.styles import MAIN_STYLE, LIGHT_STYLE
        self.setStyleSheet(MAIN_STYLE if theme == "Dark" else LIGHT_STYLE)
        
    def clear_indexed_data(self):
        reply = QMessageBox.question(self, "Confirm Delete", "This will delete all indexed files and chunks.\nContinue?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply != QMessageBox.StandardButton.Yes:
            return
        db = DatabaseManager()
        db.cursor.execute("DELETE FROM embeddings")
        db.cursor.execute("DELETE FROM chunks")
        db.cursor.execute("DELETE FROM files")
        db.conn.commit()
        db.close()
        
        self.results_list.clear()
        self.preview_panel.setPlainText("Select a file to Preview")
        self.refresh_dashboard()
        self.status_label.setText("Staturs: Database Cleared")
        pritn("All data cleaned")

    # ------------------------------------------------------------------ #
    #  Helpers                                                             #
    # ------------------------------------------------------------------ #

    def _refresh_folder_list(self):
        self.folder_list.clear()
        for folder in self.config.load_folders():
            self.folder_list.addItem(folder)

    def refresh_dashboard(self):
        db = DatabaseManager()
        self.files_label.setText(f"📄 Files: {db.count_files()}")
        self.chunks_label.setText(f"🧩 Chunks: {db.count_chunks()}")
        self.folders_label.setText(f"📂 Folders: {len(self.config.load_folders())}")
        db.close()
        
    def reset_preview(self):
        self.preview_panel.setPlainText("Select a file to preview")
        self.results_list.clear()
        self.search_stats_label.setText("")
        
    def refresh_settings_stats(self):
        db = DatabaseManager()
        stats = f"""
            📄 Files: {db.count_files()}
            🧩 Chunks: {db.count_chunks()}
            📂 {len(self.config.load_folders())}
            """
        self.settings_stats_label.setText(stats)
        db.close