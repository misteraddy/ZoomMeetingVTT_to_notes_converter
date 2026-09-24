from pathlib import Path


def save_notes(text: str, filename: str) -> str:

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / f"{Path(filename).stem}_notes.txt"

    output_file.write_text(
        text,
        encoding="utf-8"
    )

    return str(output_file)