import random
from datetime import datetime

import pandas as pd
import plotly.express as px
import requests
import streamlit as st

st.set_page_config(page_title="Gridiron Command", page_icon="🏈", layout="wide", initial_sidebar_state="expanded")

# ----------------------------- Theme -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700;800&family=DM+Sans:wght@400;500;600;700&display=swap');
:root { --ink:#f4f7fb; --muted:#8e9bad; --panel:#111925; --line:#233044; --orange:#ff7a18; --green:#2bd576; }
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #07101d; color: var(--ink); }
section[data-testid="stSidebar"] { background:#0b1524; border-right:1px solid #1e2b3e; }
h1,h2,h3,h4 { font-family:'Barlow Condensed',sans-serif !important; letter-spacing:.02em; }
h1 { font-size:3.3rem !important; line-height:.95 !important; }
.block-container { padding-top:2rem; max-width:1500px; }
.hero { background: radial-gradient(circle at 86% 10%, #273f5f 0, #132642 26%, #0d1828 66%); border:1px solid #30445f; border-radius:18px; padding:28px 32px; margin-bottom:18px; }
.eyebrow { color:#ff9a50; text-transform:uppercase; font-size:.73rem; font-weight:700; letter-spacing:.18em; }
.hero p { color:#b5c1d1; max-width:650px; margin-bottom:0; }
.metric { background:var(--panel); border:1px solid var(--line); border-radius:12px; padding:15px 17px; min-height:90px; }
.metric-label { color:var(--muted); font-size:.7rem; text-transform:uppercase; letter-spacing:.1em; font-weight:700; }
.metric-value { font-family:'Barlow Condensed'; font-size:2rem; font-weight:700; margin-top:2px; }
.metric-delta { color:var(--green); font-size:.76rem; }
.card { background:var(--panel); border:1px solid var(--line); border-radius:14px; padding:18px; }
.tag { border-radius:5px; padding:3px 7px; font-size:.7rem; font-weight:700; }
.green { background:#123b2d; color:#62e69c; } .orange { background:#4a291a; color:#ffaf70; } .blue { background:#153151; color:#77b8ff; }
.live { color:#ff6a58; font-weight:800; } .small { color:var(--muted); font-size:.82rem; }
[data-testid="stDataFrame"] { border:1px solid var(--line); border-radius:10px; }
button[kind="primary"] { background:#f16b17; border:0; }
</style>
""", unsafe_allow_html=True)

# ----------------------------- Data -----------------------------
FIRST = ["Bijan Robinson", "Jahmyr Gibbs", "Christian McCaffrey", "Breece Hall", "Saquon Barkley", "CeeDee Lamb", "Ja'Marr Chase", "Justin Jefferson", "Amon-Ra St. Brown", "Tyreek Hill", "Puka Nacua", "Garrett Wilson", "Malik Nabers", "A.J. Brown", "Nico Collins", "De'Von Achane", "Jonathan Taylor", "Derrick Henry", "Josh Jacobs", "Kyren Williams", "Brock Bowers", "Sam LaPorta", "Trey McBride", "Travis Kelce", "George Kittle", "Jayden Daniels", "Jalen Hurts", "Josh Allen", "Lamar Jackson", "Joe Burrow"]
TEAMS = ["ATL", "DET", "SF", "NYJ", "PHI", "DAL", "CIN", "MIN", "LAR", "MIA", "HOU", "IND", "TEN", "GB", "BAL", "BUF", "KC", "ARI", "SEA", "PIT"]
POSITIONS = ["RB", "WR", "QB", "TE", "RB", "WR", "RB", "WR", "QB", "TE"]

def make_board():
    rows = []
    for i in range(1, 501):
        if i <= len(FIRST):
            name = FIRST[i-1]
        else:
            name = f"{['Rookie','Veteran','Breakout','Sleeper','Handcuff'][i % 5]} Player {i}"
        pos = POSITIONS[(i - 1) % len(POSITIONS)]
        if i > 280 and i % 7 == 0: pos = "K"
        if i > 300 and i % 11 == 0: pos = "DST"
        team = TEAMS[(i * 3) % len(TEAMS)]
        proj = max(2.5, round(300 - i * .48 + (12 if pos == 'QB' else 0) + (7 if pos == 'K' else 0), 1))
        floor = max(1, round(proj * .68, 1)); ceiling = round(proj * 1.28, 1)
        rows.append({"Rank": i, "Player": name, "Pos": pos, "Team": team, "Bye": 4 + i % 13, "Proj Pts": proj, "Floor": floor, "Ceiling": ceiling, "Trend": ["↑ 6", "—", "↓ 3", "↑ 2"][i % 4]})
    return pd.DataFrame(rows)


def espn_request(league_id, season, swid="", espn_s2=""):
    """Read the ESPN Fantasy API server-side so browser CORS is not an issue.

    Public leagues work with league_id + season. Private leagues additionally
    need the ESPN_S2 and SWID cookie values from the user's ESPN session.
    """
    url = f"https://fantasy.espn.com/apis/v3/games/ffl/seasons/{season}/segments/0/leagues/{league_id}"
    views = ["mTeam", "mRoster", "mMatchupScore", "mSettings", "mStandings"]
    headers = {"User-Agent": "GridironCommand/1.0", "Accept": "application/json"}
    cookies = {}
    if swid.strip(): cookies["SWID"] = swid.strip()
    if espn_s2.strip(): cookies["espn_s2"] = espn_s2.strip()
    response = requests.get(url, params=[("view", view) for view in views], headers=headers, cookies=cookies, timeout=15)
    response.raise_for_status()
    return response.json()


def espn_team_table(payload):
    teams = payload.get("teams", [])
    rows = []
    for team in teams:
        record = team.get("record", {}).get("overall", {})
        rows.append({
            "Team": team.get("name") or team.get("location", "ESPN Team"),
            "Owner": ", ".join(team.get("owners", [])) or "—",
            "W": record.get("wins", 0),
            "L": record.get("losses", 0),
            "PF": round(team.get("points", 0), 1),
            "PA": round(team.get("pointsAdjusted", team.get("points", 0)), 1),
            "Team ID": team.get("id"),
        })
    return pd.DataFrame(rows)


def espn_roster_table(payload):
    rows = []
    for team in payload.get("teams", []):
        team_name = team.get("name") or team.get("location", "ESPN Team")
        for entry in team.get("roster", {}).get("entries", []):
            athlete = entry.get("playerPoolEntry", {}).get("player", {})
            if athlete:
                rows.append({
                    "Fantasy Team": team_name,
                    "Player": athlete.get("fullName", "Unknown"),
                    "Position": athlete.get("defaultPositionId", "—"),
                    "NFL Team": athlete.get("proTeamId", "—"),
                    "Status": entry.get("lineupSlotId", "—"),
                    "Week Points": athlete.get("stats", [{}])[-1].get("appliedTotal", 0) if athlete.get("stats") else 0,
                })
    return pd.DataFrame(rows)


if 'board' not in st.session_state: st.session_state.board = make_board()
if 'watchlist' not in st.session_state: st.session_state.watchlist = ["Bijan Robinson", "Brock Bowers", "Jayden Daniels"]
if 'my_team' not in st.session_state: st.session_state.my_team = {"QB": "Jayden Daniels", "RB1": "Bijan Robinson", "RB2": "Jahmyr Gibbs", "WR1": "Ja'Marr Chase", "WR2": "Puka Nacua", "FLEX": "Brock Bowers", "K": "Kicker Stream", "DST": "DST Stream"}

board = st.session_state.board

# ----------------------------- Helpers -----------------------------
def metric(label, value, delta=""):
    return f'<div class="metric"><div class="metric-label">{label}</div><div class="metric-value">{value}</div><div class="metric-delta">{delta}</div></div>'

def player_card(name, note=""):
    hit = board[board.Player == name]
    if hit.empty: return
    p = hit.iloc[0]
    st.markdown(f"<div class='card'><b>#{int(p.Rank)} &nbsp; {p.Player}</b><br><span class='tag blue'>{p.Pos}</span> <span class='small'>{p.Team} · {p['Proj Pts']} proj</span><br><span class='small'>{note}</span></div>", unsafe_allow_html=True)

# ----------------------------- Sidebar -----------------------------
st.sidebar.markdown("# 🏈 GRIDIRON\n## COMMAND")
st.sidebar.caption("Your live fantasy football war room")
view = st.sidebar.radio("COMMAND CENTER", ["War Room", "Top 500 Board", "Lineup Lab", "Streamers", "ESPN Sync", "League Settings"], label_visibility="collapsed")
st.sidebar.divider()
st.sidebar.markdown("**MY TEAM**")
for slot, name in st.session_state.my_team.items():
    st.sidebar.markdown(f"`{slot:<4}` {name}")
st.sidebar.divider()
st.sidebar.markdown("**DATA STATUS**")
st.sidebar.success("Rankings synced")
st.sidebar.caption(f"Last refreshed {datetime.now().strftime('%b %d, %I:%M %p')} · Demo feed")

# ----------------------------- War Room -----------------------------
if view == "War Room":
    st.markdown("<div class='hero'><div class='eyebrow'>Week 1 · Sunday, September 7</div><h1>WIN THE<br>WAIVER WIRE.</h1><p>One screen for every edge: live scores, matchup leverage, start/sit calls, and a Top 500 board built for decisive moves.</p></div>", unsafe_allow_html=True)
    c = st.columns(4)
    c[0].markdown(metric("Team projection", "138.4", "▲ 4.8 vs opponent"), unsafe_allow_html=True)
    c[1].markdown(metric("Win probability", "67%", "▲ 9% this morning"), unsafe_allow_html=True)
    c[2].markdown(metric("Opponent projection", "126.1", "Their roster is vulnerable"), unsafe_allow_html=True)
    c[3].markdown(metric("FAAB remaining", "$73", "League high: $81"), unsafe_allow_html=True)
    st.write("")
    left, right = st.columns([1.45, 1])
    with left:
        st.markdown("### <span class='live'>● LIVE</span> Game center", unsafe_allow_html=True)
        games = pd.DataFrame([
            ["DET", "27", "CHI", "17", "Q3 · 04:22", "J. Gibbs 18.4 FP"],
            ["PHI", "14", "DAL", "10", "Q2 · 01:08", "J. Hurts 12.8 FP"],
            ["KC", "—", "BUF", "—", "Sun 4:25 PM", "Weather: clear"],
        ], columns=["Away", "", "Home", " ", "Status", "Pulse"])
        st.dataframe(games, hide_index=True, use_container_width=True, column_config={"Pulse": st.column_config.TextColumn("Fantasy pulse")})
        st.markdown("### Decision desk")
        decisions = pd.DataFrame([
            ["START", "Jahmyr Gibbs", "RB", "CHI", "Explosive matchup · 19.2 proj", "green"],
            ["SIT", "Kicker Stream", "K", "—", "Use a home favorite instead", "orange"],
            ["WATCH", "Malik Nabers", "WR", "WAS", "Target spike in last 2 weeks", "blue"],
        ], columns=["Call", "Player", "Pos", "Matchup", "Why", "tone"])
        st.dataframe(decisions.drop(columns="tone"), hide_index=True, use_container_width=True)
    with right:
        st.markdown("### Market movers")
        movers = pd.DataFrame({"Player": ["R. White", "M. Nabers", "T. Benson", "C. Sutton"], "Move": ["▲ 18", "▲ 11", "▲ 9", "▼ 14"], "Reason": ["Goal-line role", "Route rate up", "Starter limited", "Target share dip"]})
        st.dataframe(movers, hide_index=True, use_container_width=True)
        st.markdown("### ⏱ Next lock")
        st.markdown("<div class='card'><h3>KC vs BUF</h3><span class='small'>Sunday · 4:25 PM ET</span><hr><b>Set your K and DST before the early window ends.</b></div>", unsafe_allow_html=True)
        st.write("")
        if st.button("Refresh live intel", type="primary", use_container_width=True):
            st.toast("Live intel refreshed — 3 lineup edges found")

# ----------------------------- Top 500 -----------------------------
elif view == "Top 500 Board":
    st.markdown("<div class='eyebrow'>Draft + waiver intelligence</div><h1>TOP 500 PLAYER BOARD</h1>", unsafe_allow_html=True)
    st.caption("Customizable rankings with kickers and team defenses included. Upload a CSV from your league to replace the demo board.")
    uploaded = st.file_uploader("Import league rankings CSV", type=["csv"], help="Expected columns: Rank, Player, Pos, Team, Bye, Proj Pts")
    if uploaded:
        try:
            imported = pd.read_csv(uploaded)
            required = {"Rank", "Player", "Pos", "Team"}
            if required.issubset(imported.columns):
                st.session_state.board = imported; board = imported; st.success(f"Loaded {len(imported):,} players from {uploaded.name}")
            else: st.error("CSV needs Rank, Player, Pos, and Team columns.")
        except Exception as e: st.error(f"Could not read CSV: {e}")
    f1, f2, f3, f4 = st.columns([1.4, 1, 1, 1])
    search = f1.text_input("Search player or team", placeholder="Try Chase or KC")
    pos = f2.multiselect("Positions", ["QB", "RB", "WR", "TE", "K", "DST"], default=[])
    tier = f3.selectbox("Show", ["All players", "Top 100", "Top 250", "Top 500"])
    sort = f4.selectbox("Sort by", ["Rank", "Proj Pts", "Ceiling", "Floor"])
    filtered = board.copy()
    if search: filtered = filtered[filtered.Player.str.contains(search, case=False, na=False) | filtered.Team.str.contains(search, case=False, na=False)]
    if pos: filtered = filtered[filtered.Pos.isin(pos)]
    if tier != "All players": filtered = filtered[filtered.Rank <= int(tier.split()[-1])]
    filtered = filtered.sort_values(sort, ascending=sort == "Rank")
    st.markdown(f"**{len(filtered):,} players** · including **{(filtered.Pos == 'K').sum()} kickers** and **{(filtered.Pos == 'DST').sum()} defenses**")
    event = st.dataframe(filtered, hide_index=True, use_container_width=True, height=580, on_select="rerun", selection_mode="single-row", column_config={"Proj Pts": st.column_config.NumberColumn(format="%.1f"), "Floor": st.column_config.NumberColumn(format="%.1f"), "Ceiling": st.column_config.NumberColumn(format="%.1f")})
    if event.selection.rows:
        selected = filtered.iloc[event.selection.rows[0]].Player
        if st.button(f"＋ Add {selected} to watchlist", type="primary"):
            if selected not in st.session_state.watchlist: st.session_state.watchlist.append(selected)
            st.toast(f"{selected} added to watchlist")
    st.markdown("### Watchlist")
    cols = st.columns(3)
    for i, name in enumerate(st.session_state.watchlist):
        with cols[i % 3]: player_card(name, "Priority target · click board to compare")

# ----------------------------- Lineup Lab -----------------------------
elif view == "Lineup Lab":
    st.markdown("<div class='eyebrow'>Optimize every slot</div><h1>LINEUP LAB</h1>", unsafe_allow_html=True)
    st.caption("The best roster is not always the roster with the biggest names. Compare projection, floor, ceiling, and matchup risk before kickoff.")
    a, b = st.columns([1, 1])
    with a:
        st.markdown("### My starting lineup")
        lineup_rows = []
        for slot, name in st.session_state.my_team.items():
            p = board[board.Player == name]
            if p.empty: lineup_rows.append([slot, name, "—", "—", "—"])
            else:
                x = p.iloc[0]; lineup_rows.append([slot, name, x.Pos, x.Team, x["Proj Pts"]])
        st.dataframe(pd.DataFrame(lineup_rows, columns=["Slot", "Player", "Pos", "Team", "Proj"]), hide_index=True, use_container_width=True)
        st.metric("Projected points", "138.4", "+4.8 vs opponent")
    with b:
        st.markdown("### Start / sit simulator")
        player = st.selectbox("Player to evaluate", board.Player.head(80).tolist())
        opponent = st.selectbox("Opponent", ["Your opponent's starter", "Bench option", "Free agent alternative"])
        p = board[board.Player == player].iloc[0]
        fig = px.bar(pd.DataFrame({"Case": ["Floor", "Projection", "Ceiling"], "Points": [p.Floor, p['Proj Pts'], p.Ceiling]}), x="Case", y="Points", color="Case", color_discrete_sequence=["#426b9c", "#ff7a18", "#2bd576"])
        fig.update_layout(height=250, margin=dict(l=0,r=0,t=10,b=0), paper_bgcolor="#111925", plot_bgcolor="#111925", font_color="#dbe6f4", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        st.success(f"START lean: {player} — {p['Proj Pts']} projected points and a {p.Ceiling} ceiling.")
    st.markdown("### Your edge by position")
    st.dataframe(pd.DataFrame({"Position": ["QB", "RB", "WR", "TE", "K", "DST"], "Your team": [22.4, 43.8, 39.7, 12.1, 8.2, 12.2], "Opponent": [20.1, 36.9, 42.8, 10.2, 7.8, 8.3], "Edge": ["+2.3", "+6.9", "-3.1", "+1.9", "+0.4", "+3.9"]}), hide_index=True, use_container_width=True)

# ----------------------------- Streamers -----------------------------
elif view == "Streamers":
    st.markdown("<div class='eyebrow'>Win the margins</div><h1>STREAMER HQ</h1>", unsafe_allow_html=True)
    st.caption("Kickers and defenses are part of the Top 500 — but this view finds the best one-week plays by matchup and game environment.")
    tab1, tab2 = st.tabs(["KICKERS", "DEFENSES"])
    with tab1:
        st.dataframe(pd.DataFrame([["Kicker Stream", "K", "—", "8.9", "Home favorite · wind 5 mph", "Low"], ["Evan McPherson", "K", "CIN", "8.4", "6 red-zone trips last game", "Medium"], ["Jake Elliott", "K", "PHI", "8.1", "High implied total", "Low"]], columns=["Player", "Pos", "Team", "Proj", "Signal", "Risk"]), hide_index=True, use_container_width=True)
    with tab2:
        st.dataframe(pd.DataFrame([["DST Stream", "DST", "—", "10.8", "Pressure matchup · turnover upside", "Low"], ["Pittsburgh Steelers", "DST", "PIT", "9.7", "Elite pass rush at home", "Medium"], ["Arizona Cardinals", "DST", "ARI", "8.8", "Opponent backup QB", "Medium"]], columns=["Team", "Pos", "Team", "Proj", "Signal", "Risk"]), hide_index=True, use_container_width=True)
    st.markdown("### Streaming checklist")
    st.write("✅ Vegas implied total  |  ✅ Home-field edge  |  ✅ Red-zone opportunity  |  ✅ Weather  |  ✅ Opposing offensive line")

# ----------------------------- ESPN Sync -----------------------------
elif view == "ESPN Sync":
    st.markdown("<div class='eyebrow'>Live league connection</div><h1>ESPN SYNC</h1>", unsafe_allow_html=True)
    st.caption("Pull your league, standings, rosters, and matchup totals into the war room. Public leagues only need a league ID; private leagues also need your ESPN session cookies.")
    st.info("ESPN does not provide a stable public fantasy sync SDK. This connector uses ESPN's live Fantasy API from the server, which avoids browser CORS and keeps your cookies out of the page.")
    left, right = st.columns([1, 1])
    with left:
        league_id = st.text_input("ESPN league ID", value=st.session_state.get("espn_league_id", ""), placeholder="Example: 123456")
        season = st.number_input("Season", min_value=2020, max_value=2035, value=datetime.now().year, step=1)
        st.markdown("**Private league credentials (optional)**")
        st.caption("In ESPN, open fantasy.espn.com, then copy the SWID and espn_s2 cookie values from your browser's storage. They are only held in this session and are never written to disk.")
        swid = st.text_input("SWID", type="password", placeholder="{xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx}")
        espn_s2 = st.text_input("espn_s2", type="password", placeholder="Long ESPN session value")
        sync = st.button("Sync ESPN now", type="primary", use_container_width=True)
    with right:
        st.markdown("### Connection checklist")
        st.markdown("✅ League ID and season\n\n✅ Public league, or both private cookies\n\n✅ Run sync before lineup lock\n\n✅ Confirm final injury news in ESPN")
        if st.session_state.get("espn_last_sync"):
            st.success(f"Last successful sync: {st.session_state.espn_last_sync}")
        else:
            st.warning("Not connected yet")
    if sync:
        if not str(league_id).strip():
            st.error("Enter your ESPN league ID first.")
        else:
            with st.spinner("Connecting to ESPN live data…"):
                try:
                    payload = espn_request(league_id, int(season), swid, espn_s2)
                    st.session_state.espn_payload = payload
                    st.session_state.espn_league_id = str(league_id).strip()
                    st.session_state.espn_last_sync = datetime.now().strftime("%b %d, %Y at %I:%M:%S %p")
                    st.success("ESPN connected — league data is ready in this war room.")
                except requests.HTTPError as error:
                    code = error.response.status_code if error.response is not None else "unknown"
                    if code in (401, 403): st.error("ESPN rejected the request. For a private league, add fresh SWID and espn_s2 cookies.")
                    elif code == 404: st.error("League not found for that season. Check the league ID and season.")
                    else: st.error(f"ESPN returned HTTP {code}. Try again closer to game time.")
                except requests.RequestException as error:
                    st.error(f"ESPN could not be reached: {error}")
    if st.session_state.get("espn_payload"):
        payload = st.session_state.espn_payload
        st.divider()
        st.markdown("### Synced league snapshot")
        teams = espn_team_table(payload)
        roster = espn_roster_table(payload)
        a, b, c = st.columns(3)
        a.markdown(metric("League teams", len(teams), "ESPN roster data"), unsafe_allow_html=True)
        b.markdown(metric("Players synced", len(roster), "Across all rosters"), unsafe_allow_html=True)
        c.markdown(metric("Live matchup data", "ON", "Refresh before lock"), unsafe_allow_html=True)
        if not teams.empty:
            st.markdown("### Standings & scoring")
            st.dataframe(teams.sort_values(["W", "PF"], ascending=[False, False]), hide_index=True, use_container_width=True)
        if not roster.empty:
            with st.expander(f"View synced rosters ({len(roster)} players)"):
                st.dataframe(roster, hide_index=True, use_container_width=True)

# ----------------------------- League Settings -----------------------------
else:
    st.markdown("<div class='eyebrow'>Make the board yours</div><h1>LEAGUE SETTINGS</h1>", unsafe_allow_html=True)
    st.caption("These settings control how you think about roster construction. Connect a league export above to load your real teams and scoring.")
    x, y = st.columns(2)
    with x:
        st.markdown("### League snapshot")
        st.selectbox("Platform", ["Sleeper", "ESPN", "Yahoo", "NFL.com", "Custom"])
        st.number_input("Teams", 4, 20, 10)
        st.selectbox("Format", ["PPR", "Half PPR", "Standard", "Superflex"])
        st.multiselect("Starting slots", ["QB", "RB", "WR", "TE", "FLEX", "K", "DST"], default=["QB", "RB", "WR", "TE", "FLEX", "K", "DST"])
    with y:
        st.markdown("### Scoring levers")
        st.slider("Passing TD", 2, 8, 4)
        st.slider("Reception", 0.0, 2.0, 1.0, .5)
        st.slider("Rushing / receiving yard", 0.0, .2, .1, .05)
        st.slider("Defensive sack", 0.0, 5.0, 1.0, .5)
        if st.button("Save league profile", type="primary"):
            st.success("League profile saved. Rankings are ready to be tuned.")

st.caption("Gridiron Command · A decision-support dashboard, not a guarantee. Always confirm final injury news and game status before lock.")
