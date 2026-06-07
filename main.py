from database import DatabaseManager
from extractor import extract_pdf_text
from scanner import get_pdf_files
from utils import calculate_hash
from chunker import chunk_text


db = DatabaseManager()

folder = "test_docs"

for file in get_pdf_files(folder):

    current_hash = calculate_hash(file)

    stored = db.get_file_by_path(
        str(file)
    )

    if stored is not None:

        stored_hash = stored[0]

        if current_hash == stored_hash:

            print(
                f"Skipping {file.name}"
            )

            continue

    print(
        f"Processing {file.name}"
    )

    text = extract_pdf_text(file)

    db.insert_file(
        str(file),
        file.name,
        file.stat().st_size,
        file.stat().st_mtime,
        current_hash,
        text
    )

    file_id = db.get_file_id(
        str(file)
    )
    db.delete_chunks(file_id)
    
    chunks = chunk_text(text)

    for index, chunk in enumerate(chunks):

        db.insert_chunk(
            file_id,
            index,
            chunk
        )

db.close()

print("Done")