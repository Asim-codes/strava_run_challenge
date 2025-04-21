import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Leaderboard", page_icon="🏅", layout="wide")

# Inject Bootstrap CSS
st.markdown("""
<link rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css"
      crossorigin="anonymous">
""", unsafe_allow_html=True)

# --- Hardcoded team-member mapping ---
team_member_map = {
    "Team A": ["Asim", "Ijaz", "Jaskeat"],
    "Team B": ["Alfred", "Angelo", "Miho"],
    "Team C": ["Arminder", "Siddhant", "Yrral"],
    "Team D": ["Gladys", "Jonathan", "Luis"],
    "Team E": ["John", "Rishi", "Timothy"],
    "Team F": ["Alan", "Anurag", "Matthew"]
}

# Read data from Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

@st.cache_data(ttl=300)
def load_data():
    data = conn.read()
    df = pd.DataFrame(data)
    df['Distance'] = pd.to_numeric(df['Distance']).round(2)
    df['Date'] = pd.to_datetime(df['Date']).dt.date  # Only date, no time
    return df

df = load_data()

# Team leaderboard (all teams, sum across all dates)
team_stats = (
    df.groupby('Team', as_index=False)['Distance']
    .sum()
    .sort_values(by='Distance', ascending=False)
    .reset_index(drop=True)
)
team_stats['Distance'] = team_stats['Distance'].round(2)

# Add medals to top 3 teams
medals = ['🥇', '🥈', '🥉']
team_stats['Pos'] = ''
for i in range(len(team_stats)):
    team_stats.loc[i, 'Pos'] = medals[i] if i < 3 else str(i+1)

# --- Build TeamDisplay column with members underneath ---
def team_with_members(team):
    members = ", ".join(team_member_map.get(team, []))
    return f"""
    <div>
        <span style="font-weight:600">{team}</span><br>
        <span style="font-size:0.85em; color:#bbb;">{members}</span>
    </div>
    """

team_stats["TeamDisplay"] = team_stats["Team"].apply(team_with_members)

# --- Render Bootstrap dark table ---
def render_bootstrap_dark_table(df, columns, headers):
    html = """
    <table class="table table-dark table-striped table-hover align-middle" data-bs-theme="dark" style="border-radius: 0.5em; overflow: hidden;">
    <thead>
    <tr>
    """
    for header in headers:
        html += f"<th scope='col'>{header}</th>"
    html += "</tr></thead><tbody>"
    for _, row in df.iterrows():
        html += "<tr>"
        for col in columns:
            html += f"<td>{row[col]}</td>"
        html += "</tr>"
    html += "</tbody></table>"
    return html

st.title("Leaderboard")

# --- REFRESH BUTTON ---
if st.button("🔄 Refresh Data"):
    st.cache_data.clear()

# --- Team Leaderboard: Toggle Table/Bar Chart ---
st.subheader("Team Leaderboard")
team_view = st.radio("View:", ["Table", "Bar Chart"], key="team_view", horizontal=True)
if team_view == "Table":
    st.markdown(
        render_bootstrap_dark_table(
            team_stats,
            columns=["Pos", "TeamDisplay", "Distance"],
            headers=["Pos", "Team", "Distance (km)"]
        ),
        unsafe_allow_html=True
    )
else:
    # --- TEAM HORIZONTAL BAR CHART ---
    fig_team = px.bar(
        team_stats.sort_values('Distance', ascending=True),  # Smallest at bottom
        x='Distance',
        y='Team',
        orientation='h',
        text='Distance',
        color='Distance',
        color_continuous_scale='viridis',
        labels={'Distance': 'Total Distance (km)', 'Team': 'Team'},
        title='Team Leaderboard'
    )
    fig_team.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig_team.update_layout(
        yaxis={'categoryorder':'total ascending'},
        showlegend=False,
        margin=dict(l=10, r=10, t=30, b=10)
    )
    st.plotly_chart(fig_team, use_container_width=True)

# --- Individual Leaderboard: Top 10 Individuals ---
st.subheader("Top 10 Individuals")
runner_stats = (
    df.groupby('Runner', as_index=False)['Distance']
    .sum()
    .sort_values(by='Distance', ascending=False)
    .reset_index(drop=True)
    .head(10)
)
runner_stats['Distance'] = runner_stats['Distance'].round(2)
runner_stats['Pos'] = ''
for i in range(len(runner_stats)):
    runner_stats.loc[i, 'Pos'] = medals[i] if i < 3 else str(i+1)

indiv_view = st.radio("View:", ["Table", "Bar Chart"], key="indiv_view", horizontal=True)
if indiv_view == "Table":
    st.markdown(
        render_bootstrap_dark_table(
            runner_stats,
            columns=["Pos", "Runner", "Distance"],
            headers=["Pos", "Runner", "Distance (km)"]
        ),
        unsafe_allow_html=True
    )
else:
    # --- INDIVIDUAL HORIZONTAL BAR CHART ---
    fig_runner = px.bar(
        runner_stats.sort_values('Distance', ascending=True),
        x='Distance',
        y='Runner',
        orientation='h',
        text='Distance',
        color='Distance',
        color_continuous_scale='plasma',
        labels={'Distance': 'Total Distance (km)', 'Runner': 'Runner'},
        title='Top 10 Individuals'
    )
    fig_runner.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig_runner.update_layout(
        yaxis={'categoryorder':'total ascending'},
        showlegend=False,
        margin=dict(l=10, r=10, t=30, b=10)
    )
    st.plotly_chart(fig_runner, use_container_width=True)

st.caption("Tip: For best experience on mobile, add this page to your home screen!")
st.caption("Android: In Chrome, tap ⋮ > Add to Home screen > Add.")
st.caption("iPhone: In Safari, tap Share > Add to Home Screen > Add.")
