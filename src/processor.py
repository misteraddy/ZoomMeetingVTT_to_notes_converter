from src.vtt_parser import parse_vtt
from src.chunker import create_chunks
from src.cleaner import clean_chunk
from src.second_processor import process_cleaned_chunk


def process_vtt(vtt_text: str) -> str:

    transcript = parse_vtt(vtt_text)

    chunks = create_chunks(transcript)

    processed_chunks = []

    conversation_summary = ""

    for chunk in chunks:

        cleaned_chunk = clean_chunk(chunk)

        if not cleaned_chunk.strip():
            continue

        processed_chunk, conversation_summary = process_cleaned_chunk(
            cleaned_chunk,
            conversation_summary
        )

        if processed_chunk.strip():
            processed_chunks.append(processed_chunk.strip())

    return "\n\n".join(processed_chunks)