# FPL Analytics with Python

Analyze Fantasy Premier League data with Python and Streamlit — uncover top value picks, captain candidates, and budget gems.

A small, beginner-friendly project to explore **Fantasy Premier League** data with Python.
- Fetches live FPL bootstrap data (public endpoint) with a **graceful offline fallback** to sample data.
- CLI for quick analysis (top value picks, captaincy candidates, budget gems).
- Simple **Streamlit app** for filtering/sorting and basic charts.

> Works even without internet using the provided sample dataset, so you can demo locally right away.

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Run CLI analysis (writes CSVs to ./out)
python analyze.py

# Launch the mini web app
streamlit run app.py
```

## What it does
- **Value score** = `ep_next / (now_cost / 10)` → estimates points-per-million for next GW.
- **Captain picks** = top players by `ep_next` with a minimum expected minutes and form.
- **Budget filter** for quick squad building ideas.
- **Positions** and **teams** are decoded for readability.

## Files
```
src/fpl.py             # fetching + helpers (with offline fallback)
analyze.py             # CLI to print tables & save CSVs
app.py                 # Streamlit mini app
data/sample_bootstrap.json  # tiny snapshot to run offline
out/                   # created on first run for CSV outputs
```

## Notes
- Live data comes from FPL's public endpoint: `https://fantasy.premierleague.com/api/bootstrap-static/` (no auth).
- This project is **for educational use** and not affiliated with the Premier League.

## Roadmap (easy wins)
- Add fixtures difficulty integration
- Simple "team planner" that maximizes value under a budget
- Export shortlist as CSV for sharing
