import time

from google import genai
from google.genai.errors import APIError

from config import GEMINI_API_KEY, MODEL_NAME


client = genai.Client(api_key=GEMINI_API_KEY)


SUMMARY_PROMPT = """
Maintain technical context for a sequential Agentic AI class transcript.

Previous context:
{old_summary}

Current chunk:
{current_chunk}

Update the context using the current chunk.

Keep only information useful for understanding future chunks:
- technical concepts and definitions
- terminology, components, nodes, tools, functions, frameworks
- architecture, workflows, relationships, and dependencies
- implementation details, code behavior, parameters, and state changes
- important examples, comparisons, and references such as "this node" or "that tool"

Rules:
- Preserve technical terminology.
- Do not invent or add outside information.
- Remove greetings, filler, class management, and casual conversation.
- Avoid unnecessary repetition.
- If the current chunk corrects or extends previous information, update it.
- Keep it concise but retain context needed for future chunks.
- Do not write study notes, conclusions, recommendations, or lecture summaries.
- Do not mention "the teacher" or "the lecture".

Return only the updated technical context.
"""


NOTES_PROMPT = """
You are creating detailed study notes from an Agentic AI class transcript.

Previous technical context:
{context}

Current cleaned transcript:
{chunk}

Create detailed study notes from the current transcript.

Rules:
- Preserve all important technical and conceptual information from the transcript.
- Do not remove technical details, explanations, examples, workflows, or code-related information.
- You may add short connecting sentences when necessary to make the explanation easier to understand.
- Do not add information that is not supported by the transcript or context.
- Preserve technical terminology, names, and relationships accurately.
- Use the previous context only to understand references such as "this node", "that tool", "previous approach", etc.
- Do not copy the previous technical context into the notes unless the current chunk requires it for understanding.
- Do not create a summary or conclusion.
- Do not add a section such as "Summary", "Key Takeaways", or "Conclusion".
- Do not convert the content into a summary.
- Return only the detailed study notes.

Current chunk has priority if there is any conflict with the previous context.
"""


def generate_content(
    prompt: str,
    max_retries: int = 3,
    initial_delay: float = 2.0
) -> str:

    delay = initial_delay

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )

            if not response.text:
                raise ValueError("Gemini returned an empty response.")

            return response.text.strip()

        except APIError as e:

            if attempt < max_retries - 1:
                print(
                    f"Gemini API call failed: {e}. "
                    f"Retrying in {delay:.1f} seconds..."
                )

                time.sleep(delay)
                delay *= 2

            else:
                raise e


def create_summary(
    old_summary: str,
    current_chunk: str
) -> str:

    prompt = SUMMARY_PROMPT.format(
        old_summary=old_summary or "No previous technical context.",
        current_chunk=current_chunk
    )

    return generate_content(prompt)


def create_notes(
    current_chunk: str,
    technical_context: str
) -> str:

    prompt = NOTES_PROMPT.format(
        context=technical_context or "No previous technical context.",
        chunk=current_chunk
    )

    return generate_content(prompt)


def process_cleaned_chunk(
    chunk: str,
    previous_context: str = ""
) -> tuple[str, str]:

    if not chunk or not chunk.strip():
        return "", previous_context

    updated_context = create_summary(
        old_summary=previous_context,
        current_chunk=chunk
    )

    notes = create_notes(
        current_chunk=chunk,
        technical_context=updated_context
    )

    return notes, updated_context