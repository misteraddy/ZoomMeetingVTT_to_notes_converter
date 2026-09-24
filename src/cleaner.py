from google import genai
from config import GEMINI_API_KEY, MODEL_NAME
from google.genai.errors import APIError
import time


CLEANING_PROMPT = """
You are given a transcript from an Agentic AI live Zoom class.

From the transcript, extract only the sentences that contain useful technical or conceptual content for making study notes.

Rules:

1. Remove all filler words, greetings, confirmations, audience interactions, and unnecessary conversational sentences.

2. Remove repeated questions, repeated explanations, and repeated statements.

3. Remove phrases such as:

- "Tell me guys"
- "Is it clear?"
- "Yes or no?"
- "Got it?"
- "Let me..."
- "Okay"
- "Fine"
- "Great"
- "Fast"
- "Please..."
- "Can we start?"
- "Give me a thumbs up"

4. Keep only content that explains:

- concepts
- definitions
- workflows
- architecture
- code behavior
- technical reasoning
- important implementation details
- differences/comparisons
- examples that help understand the concept

5. Remove irrelevant class-management content such as breaks, GitHub announcements, network issues, Zoom issues, attendance, and casual conversation.

6. Remove repeated content even if it appears multiple times in slightly different wording.

7. Preserve the original wording and sentence structure as much as possible.

8. Do NOT paraphrase, rewrite, summarize, or improve the English.

9. Do NOT add any information that is not present in the transcript.

10. Do NOT correct technical terminology unless it is obviously a speech-to-text error that prevents understanding.

11. Keep technical terms exactly as they appear when possible, such as LLM, tool node, supervisor node, state, tool calling, conditional edge, LangGraph, etc.

12. Preserve useful examples and code-related explanations.

13. Return only the cleaned sentences. Do not add headings, explanations, comments, or a summary.

The output should read like concise study notes extracted directly from the teacher's transcript while retaining the original wording.

Transcript:

"""


client = genai.Client(api_key=GEMINI_API_KEY)

def clean_chunk(chunk: str, max_retries: int = 3, initial_delay: float = 2.0) -> str:
    """
    Cleans a single transcript chunk using Gemini API while handling
    rate limits and chunk size validation.
    """

    full_prompt = f"{CLEANING_PROMPT}\n{chunk}"
    
    delay = initial_delay
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=full_prompt,
            )
            return response.text.strip()
        
        except APIError as e:
            # Handle rate limiting (429) or transient backend errors
            if attempt < max_retries - 1:
                print(f"API call failed ({e}). Retrying in {delay:.1f} seconds...")
                time.sleep(delay)
                delay *= 2  # Exponential backoff
            else:
                raise e

    return ""


# def clean_chunk(chunk: str) -> str:
#     prompt = CLEANING_PROMPT + chunk

#     response = client.models.generate_content(
#         model=MODEL_NAME,
#         contents=prompt
#     )

#     return response.text.strip()