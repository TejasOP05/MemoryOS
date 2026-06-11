import json
import os

CONFIG_FILE = "config.json"

class ConfigManager:
    def __init__(self):
        if not os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "w") as f:
                json.dump({
                    'folders': []
                },
                          f,
                          indent=4
                          )
                
    def load_folders(self):
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
        return data['folders']

    def save_folder(self, folder):
        folders = self.load_folders()
        if folder not in folders:
            folders.append(folder)
            
        with open(CONFIG_FILE, "w") as f:
            json.dump({
                'folders': folders
            }, f, indent=4)
            
            
    def remove_folder(self, folder):
        folders = self.load_folders()
        if folder in folders:
            folders.remove(folder)
        with open(CONFIG_FILE, "w") as f:
            json.dump({
                'folders': folders
            }, f, indent=4)