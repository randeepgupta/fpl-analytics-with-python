import pandas as pd
import streamlit as st
from src.fpl import fetch_bootstrap, decode_elements, POSITION

st.set_page_config(page_title="FPL Quick Insights", layout="wide")
st.title("FPL Quick Insights")

bootstrap = fetch_bootstrap()
elements, teams, types = decode_elements(bootstrap)
df = pd.DataFrame(elements)

left, right = st.columns([1,3])
with left:
    pos = st.multiselect("Positions", options=sorted(df["position"].unique()), default=list(sorted(df["position"].unique())))
    team = st.multiselect("Teams", options=sorted(df["team"].unique()), default=[])
    max_price = st.slider("Max price (m)", min_value=3.5, max_value=float(df["now_cost"].max()), value=float(df["now_cost"].max()))
    min_form = st.slider("Min form", min_value=0.0, max_value=float(df["form"].max()), value=0.0, step=0.1)
    min_minutes = st.slider("Min minutes (season)", min_value=0, max_value=int(df["minutes"].max()), value=180, step=30)
    sort_by = st.selectbox("Sort by", options=["value_ep_next", "ep_next", "form", "total_points"])

df["value_ep_next"] = df["ep_next"] / (df["now_cost"].replace(0, 0.1))
mask = df["position"].isin(pos) & (df["now_cost"] <= max_price) & (df["form"] >= min_form) & (df["minutes"] >= min_minutes)
if team:
    mask &= df["team"].isin(team)

st.subheader("Players")
st.dataframe(
    df.loc[mask, ["web_name", "team", "position", "now_cost", "ep_next", "form", "total_points", "selected_by_percent", "value_ep_next"]]
      .sort_values(sort_by, ascending=False)
      .reset_index(drop=True)
)

st.caption("Tip: 'value_ep_next' estimates points per million (next GW). Offline mode uses bundled sample data if the live API isn't reachable.")
