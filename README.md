# LangGraphAgent: Command-Line Academic Research & Latest Developments Analysis Tool

LangGraphAgent is a robust, CLI-based tool for discovering, analyzing, and synthesizing the latest research advancements and technical developments across major academic fields. It leverages modern LLMs, LangGraph, LangChain, Pydantic, and Firecrawl for intelligent web search, structured extraction, and workflow orchestration.

## Features

- 🔍 **Academic Research Discovery**: Query recent advancements by "Field, Subtopic" (e.g., `Machine Learning, Image Processing`).
- 🧠 **LLM-Powered Extraction**: Uses OpenAI models for extracting structured research details and synthesizing trends.
- 🕸️ **Web Search & Scraping**: Integrates Firecrawl for searching and scraping research papers, blogs, and code repositories.
- 🛠️ **LangGraph Workflows**: Modular, robust pipelines for multi-step research analysis.
- 📝 **Pydantic Models**: Ensures type-safe, structured outputs for all research data.
- 🛡️ **Error Handling & Logging**: Defensive, user-friendly CLI with clear error reporting and progress updates.

## Agents Overview

### `advance-agent`
- **Explicit, Modular Workflow**: Uses LangGraph to orchestrate a four-step pipeline:
  1. **Search Sources**: Finds relevant research and technical content.
  2. **Extract Titles**: Identifies key advancements and their main links.
  3. **Extract Details**: Gathers structured details for each advancement.
  4. **Synthesize**: Summarizes trends and future directions.
- **Manual Routing**: Each step is explicitly managed, ensuring robust error handling and transparency.
- **Best for**: Users who want reliability, traceability, and detailed logs.

### `simple-agent`
- **Dynamic, LLM-Driven Workflow**: The LLM decides which Firecrawl tool to use (search or scrape) at each step.
- **Minimal Routing**: The agent is given only the LLM and Firecrawl tools; workflow is determined on-the-fly.
- **Best for**: Rapid prototyping, flexible research, or when you want the LLM to control the process.

## How It Works

1. **User Query**: Enter a query in the format `Field, Subtopic` (e.g., `Physics, Quantum Computing`).
2. **Search & Extraction**: The agent searches for the latest research, extracts structured details, and synthesizes insights.
3. **CLI Output**: Results are displayed with emoji-rich formatting, summaries, and error logs if any.

## Technologies Used
- [LangGraph](https://github.com/langchain-ai/langgraph): Graph-based workflow orchestration for LLMs.
- [LangChain](https://github.com/langchain-ai/langchain): LLM application framework.
- [Pydantic](https://docs.pydantic.dev/): Data validation and settings management.
- [Firecrawl](https://firecrawl.dev/): Web search and scraping API.
- [OpenAI](https://platform.openai.com/): LLMs for extraction and synthesis.

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/LangGraphAgent.git
   cd LangGraphAgent
   ```
2. **Install [uv](https://github.com/astral-sh/uv):**
   ```sh
   # On Windows, Mac, or Linux (see uv docs for details)
   pip install uv
   ```
3. **Sync dependencies:**
   ```sh
   uv sync
   ```
4. **Set up environment variables:**
   - Create a `.env` file with your API keys:
     ```env
     FIRECRAWL_API_KEY=your_firecrawl_key
     OPENAI_API_KEY=your_openai_key
     ```

## Usage

### Advanced Agent
```sh
cd advance-agent
uv run main.py
```

### Simple Agent
```sh
cd simple-agent
uv run main.py
```

Follow the CLI prompts to enter your research query.

## Output Example
```
🔍 Research Query (Field, Subtopic): Machine Learning, Image Processing
...
📊 Results for: Machine Learning -> Image Processing
============================================================
1. [Title] ...
   - Authors: ...
   - Paper Links: ...
   - Code Links: ...
   - Summary: ...
...
============================================================
```

## Notes
- Ensure your `.env` file is present and contains valid API keys.
- For best results, use clear, specific queries in the required format.
- All errors and warnings are logged and displayed in the CLI.
