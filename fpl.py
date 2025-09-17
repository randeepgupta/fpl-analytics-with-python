import json
from pathlib import Path
from typing import Dict, Any, List, Tuple

import requests

BOOTSTRAP_URL = "https://fantasy.premierleague.com/api/bootstrap-static/"
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
SAMPLE_BOOTSTRAP = DATA_DIR / "sample_bootstrap.json"

POSITION = {1: "GK", 2: "DEF", 3: "MID", 4: "FWD"}

def fetch_bootstrap(timeout: float = 10.0) -> Dict[str, Any]:
    """
    Fetch FPL bootstrap; on failure, return bundled sample.
    """
    try:
        r = requests.get(BOOTSTRAP_URL, timeout=timeout)
        r.raise_for_status()
        return r.json()
    except Exception:
        return json.loads(SAMPLE_BOOTSTRAP.read_text(encoding="utf-8"))

def decode_elements(bootstrap: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], Dict[int, str], Dict[int, str]]:
    teams = {t["id"]: t["name"] for t in bootstrap.get("teams", [])}
    types = {t["id"]: t["singular_name_short"] for t in bootstrap.get("element_types", [])}
    elements = []
    for e in bootstrap.get("elements", []):
        elements.append({
            "id": e["id"],
            "first_name": e["first_name"],
            "second_name": e["second_name"],
            "web_name": e.get("web_name") or e["second_name"],
            "team": teams.get(e["team"], str(e["team"])),
            "position": types.get(e["element_type"], str(e["element_type"])),
            "now_cost": e["now_cost"] / 10.0,
            "total_points": e.get("total_points", 0),
            "form": float(e.get("form", "0") or 0),
            "ep_next": float(e.get("ep_next", "0") or 0),
            "minutes": e.get("minutes", 0),
            "selected_by_percent": float((e.get("selected_by_percent") or "0").replace("%", "")),
        })
    return elements, teams, types
