# chunker.py

def chunk_text(text, chunk_size=500):

    paragraphs = text.split("\n")

    chunks = []

    current_chunk = ""

    for para in paragraphs:

        para = para.strip()

        if not para:
            continue

        if len(current_chunk) + len(para) < chunk_size:

            current_chunk += para + "\n"

        else:

            chunks.append(current_chunk)

            current_chunk = para + "\n"

    if current_chunk:

        chunks.append(current_chunk)

    return chunks