from pathlib import Path


def get_pdf_files(folder_path):

    folder = Path(folder_path)

    return folder.rglob("*.pdf")