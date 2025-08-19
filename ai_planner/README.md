# Personal AI Planner

An attractive Streamlit app that automates daily planning, schedules tasks on your calendar, and generates insights using an optional LLM.

## Features
- Task inbox with priorities, durations, due dates, and tags
- One-click "Plan my day" that schedules tasks into your available time
- Calendar view (timeline) and ICS export
- Optional LLM suggestions/summaries (OpenAI or Anthropic). Falls back to local heuristics if no key
- SQLite storage (local), no cloud required
- Clean, modern UI with light/dark theme

## Quick Start

1. Create a virtual environment and install dependencies:
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

2. Run the app:
```bash
streamlit run app.py
```

3. (Optional) Set your API key(s) in `.env`:
```bash
cp .env.example .env
# edit the file to add OPENAI_API_KEY or ANTHROPIC_API_KEY
```

## Project Structure
```
ai_planner/
  app.py
  core/
    db.py
    models.py
    planner.py
    llm.py
  ui/
    components.py
  pages/
    1_Tasks.py
    2_Calendar.py
    3_Insights.py
  assets/
    styles.css
  .streamlit/
    config.toml
```

## Notes
- Data is stored in `data/ai_planner.db` in the project directory
- ICS exports are written to `exports/` by default
- Streamlit reruns the script on interactions; state is persisted via the database
