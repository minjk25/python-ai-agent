# AI Code Assistant

An AI-powered coding agent built in Python that can autonomously explore, read, execute, and modify code in your codebase.

## Overview

This project is an AI agent that uses `Google's Gemini API` to assist with coding tasks. The agent can:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

The agent operates in a loop, making function calls to interact with your codebase until it completes the requested task.

## Requirements

- Python 3.13+
- A Google Gemini API key

## Installation

1. Clone the repository
   ```bash
   git clone https://github.com/minjk25/python-ai-agent.git

   cd python-ai-agent
   ```
2. Install dependencies using [uv](https://github.com/astral-sh/uv):
   ```bash
   uv sync
   ```
3. Create a `.env` file in the project root and add your Gemini API key:
   ```bash
   GEMINI_API_KEY=your_api_key_here
   ```
## Usage

Run the agent with a prompt:
```bash
uv run main.py "Your prompt here"
```
Enable verbose output to see token usage and function call details:
```bash
uv run main.py "Your prompt here" --verbose
```

## Project Structure
```bash
├── main.py              # Entry point and main agent loop
├── prompts.py           # System prompt configuration
├── config.py            # Configuration constants
├── call_function.py     # Function call dispatcher
├── functions/           # Available tool functions
│   ├── get_file_content.py
│   ├── get_files_info.py
│   ├── run_python_file.py
│   └── write_file.py
├── calculator/          # Sample calculator app for testing
│   ├── main.py
│   └── pkg/
│       ├── calculator.py
│       └── render.py
└── pyproject.toml       # Project dependencies
```
## Dependencies
- `google-genai` - Google Gemini API client
- `python-dotenv` - Environment variable management

## Documentation & Resources

- [Google Gemini API Documentation](https://ai.google.dev/docs)
- [Google GenAI Python SDK](https://github.com/google-gemini/generative-ai-python)
- [Function Calling Guide](https://ai.google.dev/gemini-api/docs/function-calling)
- [Boot.dev](https://boot.dev)
