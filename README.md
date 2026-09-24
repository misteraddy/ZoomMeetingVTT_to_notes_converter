Here is the complete `README.md` content. Copy everything inside the code block into a file named `README.md`.

````markdown
# Meeting Note Maker

A Streamlit application that converts Zoom `.vtt` transcripts into detailed technical study notes using Google Gemini.

The application is designed for technical classes such as Agentic AI, Generative AI, LangChain, LangGraph, RAG, and related topics.

## Features

- Upload a Zoom `.vtt` transcript
- Parse VTT into plain transcript text
- Remove timestamps, cue numbers, and unnecessary VTT formatting
- Split transcripts into context-preserving chunks
- Clean unnecessary conversational content using Gemini
- Generate detailed technical study notes
- Maintain rolling technical context between chunks
- Preserve technical terminology and relationships
- Process chunks in their original order
- Download generated notes as a `.txt` file
- Generated notes can be kept in memory without saving them locally

## Workflow

```text
Zoom VTT File
      |
      v
VTT Parser
      |
      v
Plain Transcript
      |
      v
Chunking
      |
      v
LLM Cleaning
      |
      v
Cleaned Chunks
      |
      v
Technical Context + Note Generation
      |
      v
Detailed Notes
      |
      v
Combine Chunks
      |
      v
Download TXT
````

## Project Structure

```text
meeting_note_maker/
│
├── app.py
├── config.py
├── requirements.txt
├── .env
├── .gitignore
│
└── src/
    ├── __init__.py
    ├── vtt_parser.py
    ├── chunker.py
    ├── cleaner.py
    ├── second_processor.py
    └── processor.py
```

## Requirements

* Python 3.10+
* Google Gemini API key
* Streamlit

## Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd meeting_note_maker
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv note_venv
```

Activate the environment:

```bash
note_venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Do not commit the `.env` file to Git.

Example `.gitignore`:

```gitignore
.env
.venv/
venv/
note_venv/
__pycache__/
*.pyc
```

## Configuration

The Gemini API key and model configuration are stored in `config.py`.

Example:

```python
import os

from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

MODEL_NAME = "gemini-3.5-flash-lite"

MAX_CHUNK_CHARACTERS = 12000
MIN_CHUNK_CHARACTERS = 4000
```

## Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your browser.

Upload a `.vtt` file and click **Submit** to generate the study notes.

## VTT Processing

The application converts Zoom VTT content such as:

```text
WEBVTT

1
00:00:02.300 --> 00:00:04.940
Sunny: Please confirm in the chat?

2
00:00:08.570 --> 00:00:10.249
Sunny: So let's begin with the session.
```

into plain transcript text:

```text
Please confirm in the chat?

So let's begin with the session.
```

The VTT formatting is removed before sending the transcript to the LLM.

## Chunking

The transcript is divided into relatively large chunks while preserving line boundaries.

The purpose is to maintain enough context for technical explanations.

The application avoids creating unnecessarily small chunks because technical concepts may depend on information explained immediately before or after them.

Example:

```text
Chunk 1
    |
    +-- Concept
    +-- Definition
    +-- Example
    +-- Implementation details
          |
          v
Chunk 2
    |
    +-- Continuation
    +-- Code behavior
    +-- Further explanation
```

## LLM Processing

### 1. Transcript Cleaning

The cleaning stage removes unnecessary conversational content while preserving useful technical information.

It removes things such as:

* Greetings
* Filler words
* Audience interaction
* Repeated questions
* Class management
* Break announcements
* Zoom/network issues
* Casual conversation

It preserves:

* Technical concepts
* Definitions
* Architecture
* Workflows
* Code explanations
* Implementation details
* Technical comparisons
* Useful examples

The cleaning stage is designed to preserve the teacher's original technical wording as much as possible.

### 2. Detailed Note Generation

The second stage generates detailed study notes from the cleaned transcript.

The notes should:

* Preserve important technical information
* Preserve examples
* Preserve workflows
* Explain relationships between concepts
* Preserve technical terminology
* Add short connecting explanations when necessary
* Avoid unsupported information
* Avoid removing important details
* Avoid creating a separate summary

The output is intended to be detailed study material rather than a short summary.

## Rolling Technical Context

The application maintains technical context while processing sequential chunks.

```text
Chunk 1
   |
   v
Technical Context 1
   |
   v
Chunk 2 + Context 1
   |
   v
Technical Context 2
   |
   v
Chunk 3 + Context 2
```

This helps the LLM understand references such as:

```text
"this node"
"that tool"
"the previous approach"
"this state"
"the same function"
```

The technical context is used internally and is not directly included as the final output.

## Output

The processed chunks are combined in the same order as the original transcript.

```text
Processed Chunk 1

Processed Chunk 2

Processed Chunk 3
```

The final notes can be downloaded as a text file using Streamlit.

The application does not need to create a physical `.txt` file on the local machine.

Example:

```python
st.download_button(
    label="Download Notes",
    data=final_notes,
    file_name="meeting_notes.txt",
    mime="text/plain"
)
```

The generated notes remain in memory until they are downloaded or the Streamlit session ends.

## Gemini API Quota

The application uses the Google Gemini API.

Free-tier API projects have request and token limits. Large transcripts can consume the available quota quickly because each transcript chunk may require multiple API calls.

For example, with a two-stage architecture:

```text
10 chunks

Cleaning:
10 API requests

Notes + Context:
10 API requests

Total:
20 API requests
```

Therefore, large VTT files may reach the Gemini API rate limit.

If the API returns:

```text
429 RESOURCE_EXHAUSTED
```

it generally means the current API quota or rate limit has been exceeded.

The application should wait for the quota window to reset instead of continuously retrying requests.

## Error Handling

The Gemini processor includes retry logic for temporary API failures.

The general retry flow is:

```text
API Request
    |
    v
Request Failed
    |
    v
Wait
    |
    v
Retry
    |
    v
Wait Longer
    |
    v
Retry Again
```

Retrying does not bypass a hard quota limit.

If the Gemini API reports that the project has exceeded its quota, the application must wait for the quota window to reset or use an API project with higher limits.

## Security

Never hard-code the Gemini API key inside Python source code.

Use a `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Make sure `.env` is included in `.gitignore`:

```gitignore
.env
```

Never commit API keys to GitHub.

## Technologies

* Python
* Streamlit
* Google Gemini API
* `google-genai`
* `python-dotenv`

## Future Improvements

Possible future improvements:

* Reduce the number of Gemini API calls
* Combine cleaning and note generation
* Generate notes and technical context in a single LLM call
* Token-aware chunking
* Better speaker detection
* Progress bar
* Resume processing after API failure
* Markdown output
* PDF export
* DOCX export
* Multiple transcript processing
* Local/free LLM support
* Processing cache
* Improved rate-limit handling

## License

This project is intended for educational and personal use.

Add a license here if the project is published publicly.

```

Available next action: :contentReference[oaicite:0]{index=0}
```
