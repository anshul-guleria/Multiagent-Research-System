# Multiagent Research System

An AI-powered research assistant that uses multiple specialized agents to search, read, write, and critique comprehensive research reports on any topic.

## Features

- **Multi-Agent Architecture**: Four specialized agents working in sequence
  - **Search Agent**: Finds recent and reliable information using web search
  - **Reader Agent**: Scrapes and extracts detailed content from relevant URLs
  - **Writer Agent**: Generates structured reports with introduction, key findings, conclusion, and sources
  - **Critic Agent**: Reviews and scores the report with constructive feedback

- **Modern Web Interface**: Clean, light-themed UI built with Flask
  - Real-time progress tracking with animated step indicators
  - Markdown rendering for formatted reports
  - PDF export functionality

- **LangGraph Workflow**: Orchestrates agent execution using a compiled state graph

## Tech Stack

| Layer | Technology |
|---|---|
| LLM | Groq (llama-3.1-8b-instant) |
| Orchestration | LangGraph, LangChain |
| Backend | Flask |
| Search | DuckDuckGo Search |
| Scraping | BeautifulSoup4 |
| PDF | fpdf |
| Frontend | HTML/CSS/JS, marked.js |

## Project Structure

```
Multiagent-Research-System/
├── agents/
│   ├── search_agent.py      # Web search agent
│   └── reader_agent.py      # Content scraping agent
├── chains/
│   └── chain.py             # Writer and critic LLM chains
├── graph/
│   └── builder.py           # LangGraph workflow builder
├── llm/
│   └── groq_service.py      # Groq LLM configuration
├── pipeline/
│   └── pipeline.py          # Legacy LCEL pipeline
├── schema/
│   └── agent_state.py       # Shared state schema
├── tools/
│   ├── web_search_tool.py   # DuckDuckGo search tool
│   └── scrape_tool.py       # Web scraping tool
├── templates/
│   └── index.html           # Web UI
├── app.py                   # Flask application
├── main.py                  # CLI entry point
└── requirements.txt
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Multiagent-Research-System
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate       # Windows
source .venv/bin/activate    # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
```

Get a free Groq API key at: https://console.groq.com

## Usage

### Web Interface

```bash
python app.py
```

Open `http://127.0.0.1:5000`, enter a topic, and click **Research**. Download the final report as a PDF once complete.

### Command Line

```bash
python main.py
```

Enter your research topic when prompted. Results are printed to the terminal.

## How It Works

```
Topic Input
    │
    ▼
Search Agent  ──►  Reader Agent  ──►  Writer Agent  ──►  Critic Agent
(DuckDuckGo)       (Scrape URL)        (Report)           (Feedback)
```

1. **Search**: Queries DuckDuckGo for recent information on the topic
2. **Read**: Picks the most relevant URL and scrapes its full content
3. **Write**: Synthesizes gathered data into a structured report
4. **Critique**: Scores the report and provides strengths, improvements, and a verdict

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Serves the web interface |
| POST | `/research` | Runs the research pipeline |
| POST | `/download` | Returns the report as a PDF file |

### `/research`
```json
// Request
{ "topic": "Quantum Computing in 2025" }

// Response
{ "report": "...", "feedback": "..." }
```

### `/download`
```json
// Request
{ "topic": "...", "report": "...", "feedback": "..." }
// Response: PDF file download
```

## Requirements

- Python 3.11+
- Groq API key
- Internet connection for web search and scraping

## License

MIT
