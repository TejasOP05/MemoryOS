from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QListWidget,
    QLabel,
    QListWidgetItem
)
from ui.styles import MAIN_STYLE
from semantic_search import SemanticSearch


class MemoryOSWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.search_engine = SemanticSearch()
        
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
        self.ai_page_btn = QPushButton("🤖 AI Assistant")
        self.folder_page_btn = QPushButton("📂 Folders")
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

        title.setStyleSheet(
            "font-size:22px;font-weight:bold;"
        )

        content.addWidget(title)

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

        self.results_list = QListWidget()

        content.addWidget(
            self.results_list
        )

        bottom_bar = QHBoxLayout()

        self.add_folder_btn = QPushButton(
            "📂 Add Folder"
        )

        self.reindex_btn = QPushButton(
            "🔄 Reindex"
        )

        self.ai_btn = QPushButton(
            "🤖 Ask AI"
        )

        bottom_bar.addWidget(
            self.add_folder_btn
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

        # Dummy data
        self.results_list.addItem(
            QListWidgetItem(
                "📄 res3.pdf\nSGPA: 7.86"
            )
        )

        self.results_list.addItem(
            QListWidgetItem(
                "📄 UNDERTAKING.pdf\nPlacement Drive Document"
            )
        )
    
    def perform_search(self):
        query = self.search_box.text()
        if not query:
            return
        
        self.results_list.clear()
        results = self.search_engine.search(query)
        
        if not results:
            self.results_list.addItem(
                "No results found."
            )
            return
        
        for filename, path, text, score in results:
            item_text = f"📄 {filename}\nSCORE: {score:.2f}"
            self.results_list.addItem(item_text)
            
                