from config import MAX_CHUNK_CHARACTERS, MIN_CHUNK_CHARACTERS


def create_chunks(text: str) -> list[str]:
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    chunks = []
    current_chunk = []
    current_length = 0

    for line in lines:
        line_length = len(line)

        if (
            current_chunk
            and current_length + line_length > MAX_CHUNK_CHARACTERS
            and current_length >= MIN_CHUNK_CHARACTERS
        ):
            chunks.append("\n".join(current_chunk))

            current_chunk = []
            current_length = 0

        current_chunk.append(line)
        current_length += line_length + 1

    if current_chunk:
        chunks.append("\n".join(current_chunk))

    return chunks