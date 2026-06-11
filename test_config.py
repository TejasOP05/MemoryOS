from config_manager import ConfigManager

config = ConfigManager()

config.save_folder(
    r"C:\Users\hp\Downloads"
)

print(
    config.load_folders()
)