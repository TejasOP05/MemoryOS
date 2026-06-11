from config_manager import ConfigManager
from indexer import run_indexing

class Pipeline:
    def __init__(self):
        self.config = ConfigManager()
        
    def reindex_all(self):
        folders = self.config.load_folders()
        
        if not folders:
            print("No folders")
            return

        for folder in folders:
            print(f"Indexing {folder}")
            run_indexing(folder)
        print("Indexing complete")