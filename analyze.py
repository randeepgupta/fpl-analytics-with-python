import pandas as pd
from pathlib import Path
from src.fpl import fetch_bootstrap, decode_elements

OUT = Path("out")
OUT.mkdir(exist_ok=True)

def main():
    bootstrap = fetch_bootstrap()
    elements, teams, types = decode_elements(bootstrap)
    df = pd.DataFrame(elements)

    # Basic filters for "reliable minutes"
    reliable = df[df["minutes"] >= 180]  # roughly 2 full games worth

    # Value metric: expected points next GW per million price
    df["value_ep_next"] = (df["ep_next"]) / (df["now_cost"].replace(0, 0.1))
    reliable["value_ep_next"] = (reliable["ep_next"]) / (reliable["now_cost"].replace(0, 0.1))

    # Top overall value picks
    top_value = reliable.sort_values("value_ep_next", ascending=False).head(15)
    # Captaincy: top expected points with some form
    captain = reliable[reliable["form"] >= 2.5].sort_values("ep_next", ascending=False).head(10)
    # Budget picks under 6.5m
    budget = reliable[reliable["now_cost"] <= 6.5].sort_values("value_ep_next", ascending=False).head(15)

    top_value.to_csv(OUT / "top_value.csv", index=False)
    captain.to_csv(OUT / "captain_picks.csv", index=False)
    budget.to_csv(OUT / "budget_gems.csv", index=False)

    pd.set_option("display.max_columns", 8)
    print("\n=== TOP VALUE (next GW, per £m) ===")
    print(top_value[["web_name", "team", "position", "now_cost", "ep_next", "value_ep_next"]])
    print("\n=== CAPTAIN PICKS (EP next + form) ===")
    print(captain[["web_name", "team", "position", "now_cost", "ep_next", "form"]])
    print("\n=== BUDGET GEMS (<= 6.5m) ===")
    print(budget[["web_name", "team", "position", "now_cost", "ep_next", "value_ep_next"]])

if __name__ == "__main__":
    main()
