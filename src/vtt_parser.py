import re


def parse_vtt(vtt_text: str) -> str:
    lines = vtt_text.splitlines()

    cleaned_lines = []
    previous_line = None

    timestamp_pattern = re.compile(
        r"^\d{2}:\d{2}:\d{2}\.\d{3}\s+-->\s+\d{2}:\d{2}:\d{2}\.\d{3}"
    )

    cue_number_pattern = re.compile(r"^\d+$")

    speaker_pattern = re.compile(
        r"^[A-Za-z0-9_ .-]+:\s*"
    )

    for line in lines:
        line = line.strip()

        if not line:
            continue

        if line == "WEBVTT":
            continue

        if timestamp_pattern.match(line):
            continue

        if cue_number_pattern.match(line):
            continue

        line = re.sub(speaker_pattern, "", line)

        if line == previous_line:
            continue

        cleaned_lines.append(line)
        previous_line = line

    return "\n\n".join(cleaned_lines)