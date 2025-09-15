# pages/current_leaderboard.py
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px
from datetime import datetime


# Days Left
current_date = datetime.today() 
target_date = datetime(2025, 10, 16)
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


# Read data from Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)


@st.cache_data(ttl=300)
def load_data():
    try:
        # Use default sheet
        data = conn.read()
        df = pd.DataFrame(data)
        
        # Clean the data
        if 'Distance' in df.columns:
            df['Distance'] = pd.to_numeric(df['Distance'], errors='coerce').round(2)
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.date
        
        # Filter out archived entries - handle multiple formats
        if 'Archive' in df.columns:
            # Convert various True representations to a standard format
            df['Archive'] = df['Archive'].astype(str).str.upper().str.strip()
            archived_values = ['TRUE', 'T', '1', 'YES', 'Y']
            
            # Keep only rows where Archive is NOT in archived_values
            df = df[~df['Archive'].isin(archived_values)]
            
            total_entries = len(data)
            current_entries = len(df)
            archived_entries = total_entries - current_entries
            
            #st.info(f"📊 Showing {current_entries} current entries ({archived_entries} archived entries filtered out)")
        
        df = df.dropna()
        return df
        
    except Exception as e:
        st.error(f"Failed to load data: {str(e)}")
        return pd.DataFrame()


def display_statistics_2x2(df):
    """Display key statistics in mobile-friendly 2x2 layout at the top"""
    if df.empty:
        st.warning("No data available for statistics")
        return
    
    st.subheader("📊 Current Statistics")
    
    # Calculate statistics
    total_distance = df['Distance'].sum()
    total_runs = len(df)
    avg_distance = df['Distance'].mean()
    active_runners = df['Runner'].nunique() if 'Runner' in df.columns else df['Team'].nunique()
    
    # MOBILE-FRIENDLY: 2x2 layout using two rows of columns
    # Row 1: Total Distance and Total Runs
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            label="🏃‍♂️ Total Distance", 
            value=f"{total_distance:.1f} km",
            help="Combined distance of all participants"
        )
    with col2:
        st.metric(
            label="📈 Total Runs", 
            value=f"{total_runs:,}",
            help="Total number of recorded runs"
        )
    
    # Row 2: Average Distance and Active Runners
    col3, col4 = st.columns(2)
    with col3:
        st.metric(
            label="📊 Average Distance", 
            value=f"{avg_distance:.1f} km",
            help="Average distance per run"
        )
    with col4:
        st.metric(
            label="👥 Active Runners", 
            value=f"{active_runners}",
            help="Number of active participants"
        )
    
    st.markdown("---")


df = load_data()


if df.empty:
    st.warning("⚠️ No data available. Please check your Google Sheets connection.")
    st.stop()


# ADD STATISTICS AT THE TOP (NEW SECTION)
display_statistics_2x2(df)


# Dynamic team-member mapping from actual data
team_member_map = {}
for _, row in df.iterrows():
    team = row['Team']
    runner = row['Runner']
    if team not in team_member_map:
        team_member_map[team] = []
    if runner not in team_member_map[team]:
        team_member_map[team].append(runner)


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
    team_list = list(team_member_map.keys())
    selected_team = st.selectbox("Select a team to see member contributions:", team_list)
    df_team = df[df['Team'] == selected_team]
    member_contrib = df_team.groupby('Runner')['Distance'].sum().reset_index()
    member_contrib['Distance'] = member_contrib['Distance'].round(2)
    
    if not member_contrib.empty:
        sunburst_df = pd.DataFrame({
            'Team': [selected_team]*len(member_contrib),
            'Runner': member_contrib['Runner'],
            'Distance': member_contrib['Distance']
        })
        
        fig_sunburst = px.sunburst(
            sunburst_df,
            path=['Team', 'Runner'],
            values='Distance',
            title=f'{selected_team} Member Contributions',
            color='Distance',
            color_continuous_scale='Blues'
        )
        fig_sunburst.update_layout(margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(fig_sunburst, use_container_width=True)
        
        member_contrib_sorted = member_contrib.sort_values('Distance', ascending=False)
        member_contrib_sorted['Rank'] = range(1, len(member_contrib_sorted) + 1)
        st.dataframe(
            member_contrib_sorted[['Rank', 'Runner', 'Distance']],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.warning(f"No data found for {selected_team}")


st.markdown("---")


# --- INDIVIDUAL LEADERBOARD ---
st.subheader("Individual Leaderboard")


individual_view = st.radio(
    "View:", 
    ["Table", "Bar Chart"], 
    key="individual_view", 
    horizontal=True
)


individual_stats = (
    df.groupby(['Runner', 'Team'], as_index=False)['Distance']
    .sum()
    .sort_values(by='Distance', ascending=False)
    .reset_index(drop=True)
)
individual_stats['Distance'] = individual_stats['Distance'].round(2)


individual_stats['Pos'] = ''
for i in range(len(individual_stats)):
    individual_stats.loc[i, 'Pos'] = medals[i] if i < 3 else str(i+1)


if individual_view == "Table":
    st.markdown(
        render_bootstrap_dark_table(
            individual_stats.head(20),
            columns=["Pos", "Runner", "Team", "Distance"],
            headers=["Pos", "Runner", "Team", "Distance (km)"]
        ),
        unsafe_allow_html=True
    )
elif individual_view == "Bar Chart":
    top_individuals = individual_stats.head(10).sort_values('Distance', ascending=True)
    fig_individual = px.bar(
        top_individuals,
        x='Distance',
        y='Runner',
        orientation='h',
        text='Distance',
        color='Team',
        labels={'Distance': 'Total Distance (km)', 'Runner': 'Runner'},
        title='Top 10 Individual Performers'
    )
    fig_individual.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig_individual.update_layout(
        yaxis={'categoryorder':'total ascending'},
        margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    st.plotly_chart(fig_individual, use_container_width=True)


st.markdown("---")

# Add this at the very end of your file, after all the existing code

st.markdown("<br><br>", unsafe_allow_html=True)

# Add to Home Screen Instructions
st.markdown("""
---
<div style="text-align: center; padding: 2rem 1rem; background-color: rgba(255,255,255,0.02); border-radius: 8px; margin-top: 2rem;">
    <h4 style="color: rgba(255,255,255,0.8); margin-bottom: 1rem;">📱 Add to Home Screen</h4>
    
    <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 2rem; margin-top: 1.5rem;">
        
        <div style="text-align: left; max-width: 300px;">
            <h5 style="color: #ff6b6b; margin-bottom: 0.5rem;">🤖 Android</h5>
            <p style="font-size: 0.9rem; color: rgba(255,255,255,0.7); line-height: 1.4;">
                1. Tap the menu (⋮) in your browser<br>
                2. Select "Add to Home screen"<br>
                3. Tap "Add" to confirm
            </p>
        </div>
        
        <div style="text-align: left; max-width: 300px;">
            <h5 style="color: #ff6b6b; margin-bottom: 0.5rem;">🍎 iPhone</h5>
            <p style="font-size: 0.9rem; color: rgba(255,255,255,0.7); line-height: 1.4;">
                1. Tap the share button (⬆️)<br>
                2. Scroll down and tap "Add to Home Screen"<br>
                3. Tap "Add" to confirm
            </p>
        </div>
        
    </div>
    
    <p style="font-size: 0.8rem; color: rgba(255,255,255,0.5); margin-top: 1.5rem;">
        Access the leaderboard instantly like a native app!
    </p>
</div>
""", unsafe_allow_html=True)
