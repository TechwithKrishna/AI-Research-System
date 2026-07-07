# AI Multi-Agent Research System

A multi-agent research pipeline that searches the web, scrapes the most relevant source, writes a report, and critiques it — now with a Streamlit UI on top.

## How It Works

The pipeline runs four stages in sequence:

1. **Search Agent** — finds recent, reliable sources on the given topic
2. **Reader Agent** — picks the most relevant URL from the search results and scrapes it for deeper content
3. **Writer Chain** — combines the search results and scraped content into a full report
4. **Critic Chain** — reviews the report and generates feedback

## Project Structure

```
Ai research system/
├── app.py              # Streamlit UI (run this to use the web interface)
├── pipelines.py         # Core pipeline logic (run_research_pipeline)
├── agents.py            # Agent/chain definitions (search, reader, writer, critic)
├── tools.py             # Tools used by the agents
├── .env                 # API keys / environment variables
├── requirements.txt     # Python dependencies
└── README.md
```

## Setup

1. **Clone / copy the project files** into a single folder as shown above.

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate      # macOS/Linux
   venv\Scripts\activate         # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install streamlit
   ```
   (Add `streamlit` to `requirements.txt` so it's installed automatically next time.)

4. **Set up your `.env` file** with the required API keys:
   ```
   GOOGLE_API_KEY=your_gemini_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   ```
   - **Gemini API** powers the LLM agents/chains (search, reader, writer, critic)
   - **Tavily** is used by the Search Agent to perform web searches

   Get a Gemini key from [Google AI Studio](https://aistudio.google.com/apikey) and a Tavily key from [tavily.com](https://tavily.com).

## Usage

### Option A — Terminal (original)

```bash
python pipelines.py
```

You'll be prompted to enter a research topic, and the pipeline will run end-to-end in the console.

### Option B — Streamlit UI (recommended)

```bash
streamlit run app.py
```

This opens a browser tab where you can:
- Enter a research topic and run the full pipeline with one click
- View the **Final Report**, **Critic Feedback**, raw **Search Results**, and **Scraped Content** in separate tabs
- Download the generated report as a `.md` file
- See a history of recently researched topics in the sidebar

## Output

`run_research_pipeline(topic)` returns a dictionary:

```python
{
    "search_result": "...",     # raw search agent output
    "scraped_content": "...",   # raw reader agent output
    "Report": "...",            # final written report
    "Feedback": "..."           # critic's feedback on the report
}
```

## Notes

- The Streamlit app calls `run_research_pipeline` as a single blocking call, so the UI shows a loading spinner for the full duration rather than live per-stage progress. If step-by-step progress is needed, `pipelines.py` can be refactored to yield after each stage.
- This project uses **Google Gemini** for the LLM agents/chains and **Tavily** for web search — make sure both `GOOGLE_API_KEY` and `TAVILY_API_KEY` are set in `.env` before running either the terminal or Streamlit version.
- Tavily has a free tier with a monthly search quota; if searches start failing, check your usage/limits on the Tavily dashboard.
- Gemini API calls are rate-limited depending on your tier — if you hit `429` errors, add retry/backoff logic in `agents.py` or slow down repeated runs.