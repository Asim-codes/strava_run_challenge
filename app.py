import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Leaderboard", page_icon="🏅", layout="wide")

# Days Left
current_date = datetime.today() 
target_date = datetime(2025, 5, 31)
days_left = (target_date - current_date).days

# Display Days Left segment
st.markdown(
    f"""
    <div style="display:block; text-align:left; margin-bottom:0.5em;">
        <div style="font-size:2.8em; font-weight:700; color:#FF4B4B; line-height:1;">{days_left}</div>
        <div style="font-size:1em; color:#555; letter-spacing:0.05em;">days left</div>
    </div>
    """,
    unsafe_allow_html=True
)
# Inject Bootstrap CSS
st.markdown("""
<link rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css"
      crossorigin="anonymous">
""", unsafe_allow_html=True)

# Hardcoded team-member mapping
team_member_map = {
    "Team A": ["Asim", "Ijaz", "Jaskeat"],
    "Team B": ["Alfred", "Angelo", "Miho"],
    "Team C": ["Arminder", "Siddhant", "Yrral"],
    "Team D": ["Gladys", "Jonathan", "Luis"],
    "Team E": ["John", "Rishi", "Timothy"],
    "Team F": ["Alan", "Anurag", "Matthew"],
    "Team G": [ "Karebu", "Siddharth", "Sneha"]
}

# Read data from Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

@st.cache_data(ttl=300)
def load_data():
    data = conn.read()
    df = pd.DataFrame(data)
    df['Distance'] = pd.to_numeric(df['Distance']).round(2)
    df['Date'] = pd.to_datetime(df['Date']).dt.date  
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

# Build TeamDisplay column with members underneath
def team_with_members(team):
    members = ", ".join(team_member_map.get(team, []))
    return f"""
    <div>
        <span style="font-weight:600">{team}</span><br>
        <span style="font-size:0.85em; color:#bbb;">{members}</span>
    </div>
    """

team_stats["TeamDisplay"] = team_stats["Team"].apply(team_with_members)

# Render Bootstrap dark table
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

# REFRESH BUTTON
if st.button("🔄 Refresh Data"):
    st.cache_data.clear()

# --- TEAM LEADERBOARD ---
st.subheader("Team Leaderboard")

# NEW: Add "Contribution" to the toggle
team_view = st.radio(
    "View:", 
    ["Table", "Bar Chart", "Contribution"], 
    key="team_view", 
    horizontal=True
)

if team_view == "Table":
    st.markdown(
        render_bootstrap_dark_table(
            team_stats,
            columns=["Pos", "TeamDisplay", "Distance"],
            headers=["Pos", "Team", "Distance (km)"]
        ),
        unsafe_allow_html=True
    )
elif team_view == "Bar Chart":
    # TEAM HORIZONTAL BAR CHART
    fig_team = px.bar(
        team_stats.sort_values('Distance', ascending=True),
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
    fig_team.update_coloraxes(showscale=False)
    st.plotly_chart(fig_team, use_container_width=True)
elif team_view == "Contribution":
    # --- NEW: STARBURST CHART FOR TEAM MEMBER CONTRIBUTIONS ---
    team_list = list(team_member_map.keys())
    selected_team = st.selectbox("Select a team to see member contributions:", team_list)
    # Filter data for the selected team
    df_team = df[df['Team'] == selected_team]
    # Group by member
    member_contrib = df_team.groupby('Runner')['Distance'].sum().reset_index()
    member_contrib['Distance'] = member_contrib['Distance'].round(2)
    # Prepare data for sunburst: root = Team, children = Members
    sunburst_df = pd.DataFrame({
        'Team': [selected_team]*len(member_contrib),
        'Member': member_contrib['Runner'],
        'Distance': member_contrib['Distance']
    })
    fig_sunburst = px.sunburst(
        sunburst_df,
        path=['Team', 'Member'],
        values='Distance',
        color='Distance',
        color_continuous_scale='Viridis',  # Vibrant, perceptually uniform
        hover_data={'Distance':':.2f'},    # Show distance with 2 decimals on hover
        title=f"{selected_team} - Member Contribution"
    )
    fig_sunburst.update_traces(
        marker=dict(line=dict(color='white', width=2)),  # White borders between segments
        textinfo='label+percent entry'                   # Show label and percent
    )
    fig_sunburst.update_layout(
        margin=dict(t=50, l=10, r=10, b=10),
        uniformtext=dict(minsize=10, mode='hide'),       # Hide text if too small
        sunburstcolorway=["#636efa", "#ef553b", "#00cc96", "#ab63fa", "#ffa15a", "#19d3f3"],
        extendsunburstcolors=True
    )

    st.plotly_chart(fig_sunburst, use_container_width=True)

# --- INDIVIDUAL LEADERBOARD ---
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

# Only keep Table and Bar Chart for individuals
indiv_view = st.radio(
    "View:", 
    ["Table", "Bar Chart"], 
    key="indiv_view", 
    horizontal=True
)

if indiv_view == "Table":
    st.markdown(
        render_bootstrap_dark_table(
            runner_stats,
            columns=["Pos", "Runner", "Distance"],
            headers=["Pos", "Runner", "Distance (km)"]
        ),
        unsafe_allow_html=True
    )
elif indiv_view == "Bar Chart":
    # INDIVIDUAL HORIZONTAL BAR CHART
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
    fig_runner.update_coloraxes(showscale=False)
    st.plotly_chart(fig_runner, use_container_width=True)

st.caption("Tip: For best experience on mobile, add this page to your home screen!")
st.caption("Android: In Chrome, tap ⋮ > Add to Home screen > Add.")
st.caption("iPhone: In Safari, tap Share > Add to Home Screen > Add.")
