# pages/archive.py

import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px
from datetime import datetime

st.title("🗃️ Archive Results")
st.markdown("---")

# Initialize connection
conn = st.connection("gsheets", type=GSheetsConnection)

@st.cache_data(ttl=300)
def load_archived_data():
    """Load all archived data from default sheet"""
    try:
        data = conn.read()
        df = pd.DataFrame(data)
        # Clean the data
        if 'Distance' in df.columns:
            df['Distance'] = pd.to_numeric(df['Distance'], errors='coerce').round(2)
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.date
        # Filter for archived entries only
        if 'Archive' in df.columns:
            df['Archive'] = df['Archive'].astype(str).str.upper().str.strip()
            archived_values = ['TRUE', 'T', '1', 'YES', 'Y']
            df = df[df['Archive'].isin(archived_values)] # Keep only archived entries
        df = df.dropna()
        return df
    except Exception as e:
        st.error(f"Failed to load archived data: {str(e)}")
        return pd.DataFrame()

def get_available_periods(df):
    """Get list of available periods from the data"""
    if df.empty or 'Period' not in df.columns:
        return []
    return sorted(df['Period'].unique(), reverse=True) # Most recent first

def display_team_results(df, period_name):
    """Display team results for a specific period - MOBILE FRIENDLY VERSION"""
    if df is None or df.empty:
        st.warning(f"No data available for {period_name}")
        return

    st.subheader(f"Team Results - {period_name}")

    # Calculate team scores and sort by distance (highest first)
    team_stats = (
        df.groupby('Team')['Distance']
        .sum()
        .reset_index()
        .sort_values('Distance', ascending=False) # Sort by distance DESC
        .reset_index(drop=True)
    )

    team_stats['Distance'] = team_stats['Distance'].round(2)
    team_stats['Rank'] = range(1, len(team_stats) + 1) # Rank based on sorted order

    # Add medals
    medals = ['🥇', '🥈', '🥉']
    team_stats['Medal'] = ''
    for i in range(len(team_stats)):
        team_stats.loc[i, 'Medal'] = medals[i] if i < 3 else str(i+1)

    # MOBILE-FRIENDLY: Stack table and chart vertically
    # Display team results table
    st.dataframe(
        team_stats[['Medal', 'Team', 'Distance']],
        use_container_width=True,
        hide_index=True,
        column_config={
            "Medal": "Rank",
            "Distance": st.column_config.NumberColumn(
                "Distance (km)",
                format="%.2f"
            )
        }
    )

    # Display chart below the table
    if len(team_stats) > 1:
        # Chart sorted by distance (lowest to highest for horizontal bar)
        fig = px.bar(
            team_stats.sort_values('Distance', ascending=True), # For horizontal bar chart
            x='Distance',
            y='Team',
            orientation='h',
            title=f"Team Performance - {period_name}",
            color='Distance',
            color_continuous_scale='Blues',
            text='Distance'
        )
        fig.update_traces(texttemplate='%{text:.1f}', textposition='outside')
        fig.update_layout(
            showlegend=False,
            height=300,
            yaxis={'categoryorder':'total ascending'} # Ensures proper ordering
        )
        st.plotly_chart(fig, use_container_width=True)

def display_individual_results(df, period_name):
    """Display individual member results for a specific period - MOBILE FRIENDLY VERSION"""
    if df is None or df.empty:
        return

    st.subheader(f"Individual Results - {period_name}")

    # Calculate individual scores and sort by distance (highest first)
    individual_stats = (
        df.groupby(['Runner', 'Team'])['Distance']
        .sum()
        .reset_index()
        .sort_values('Distance', ascending=False) # Sort by distance DESC
        .reset_index(drop=True)
    )

    individual_stats['Distance'] = individual_stats['Distance'].round(2)
    individual_stats['Rank'] = range(1, len(individual_stats) + 1) # Rank based on sorted order

    # Add medals
    medals = ['🥇', '🥈', '🥉']
    individual_stats['Medal'] = ''
    for i in range(len(individual_stats)):
        individual_stats.loc[i, 'Medal'] = medals[i] if i < 3 else str(i+1)

    # MOBILE-FRIENDLY: Stack table and chart vertically
    # Display individual results table
    st.dataframe(
        individual_stats[['Medal', 'Runner', 'Team', 'Distance']],
        use_container_width=True,
        hide_index=True,
        column_config={
            "Medal": "Rank",
            "Distance": st.column_config.NumberColumn(
                "Distance (km)",
                format="%.2f"
            )
        }
    )

    # Display chart below the table
    # Top performers chart - sorted by distance
    top_10 = individual_stats.head(10) # Show top 10 instead of 5
    if not top_10.empty:
        fig = px.bar(
            top_10.sort_values('Distance', ascending=True), # For horizontal bar chart
            x='Distance',
            y='Runner',
            orientation='h',
            title=f"Top 10 Performers - {period_name}",
            color='Distance',
            color_continuous_scale='Greens',
            text='Distance'
        )
        fig.update_traces(texttemplate='%{text:.1f}', textposition='outside')
        fig.update_layout(
            showlegend=False,
            height=400,
            yaxis={'categoryorder':'total ascending'} # Ensures proper ordering
        )
        st.plotly_chart(fig, use_container_width=True)

# Load all archived data
archived_data = load_archived_data()

if archived_data.empty:
    st.warning("⚠️ No archived data available.")
    st.stop()

# Get available periods
available_periods = get_available_periods(archived_data)

if not available_periods:
    st.warning("⚠️ No periods found in archived data.")
    st.stop()

# Display total archived entries info
total_entries = len(archived_data)
st.info(f"📊 Found {total_entries} archived entries across {len(available_periods)} periods")

# Period selection
st.sidebar.subheader("Select Archive Period")
selected_period = st.sidebar.selectbox(
    "Choose period to view:",
    options=available_periods,
    index=0 # Default to most recent period
)

if selected_period:
    # Filter data for selected period
    period_data = archived_data[archived_data['Period'] == selected_period]
    st.success(f"✅ Loaded {len(period_data)} entries for {selected_period}")

    # Display period info
    st.info(f"📊 Showing results for: **{selected_period}**")

    # Create tabs for different views (removed Raw Data tab)
    tab1, tab2, tab3 = st.tabs(["📈 Team Results", "👥 Individual Results", "📊 Period Stats"])

    with tab1:
        display_team_results(period_data, selected_period)

    with tab2:
        display_individual_results(period_data, selected_period)

    with tab3:
        st.subheader(f"Period Statistics - {selected_period}")
        
        # MOBILE-FRIENDLY: Stack metrics vertically instead of 4 columns
        total_distance = period_data['Distance'].sum()
        st.metric("Total Distance", f"{total_distance:.1f} km")
        
        total_runs = len(period_data)
        st.metric("Total Runs", total_runs)
        
        avg_distance = period_data['Distance'].mean()
        st.metric("Average Distance", f"{avg_distance:.1f} km")
        
        active_runners = period_data['Runner'].nunique()
        st.metric("Active Runners", active_runners)

    # Summary across all periods
    if st.sidebar.button("📊 Show Summary Across All Periods"):
        st.markdown("---")
        st.subheader("📊 Summary Across All Archive Periods")

        summary_data = []
        for period in available_periods:
            period_df = archived_data[archived_data['Period'] == period]
            if not period_df.empty:
                summary_data.append({
                    'Period': period,
                    'Teams': period_df['Team'].nunique(),
                    'Participants': period_df['Runner'].nunique(),
                    'Total Runs': len(period_df),
                    'Total Distance': round(period_df['Distance'].sum(), 1),
                    'Average Distance': round(period_df['Distance'].mean(), 1)
                })

        if summary_data:
            summary_df = pd.DataFrame(summary_data)
            st.dataframe(
                summary_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Total Distance": st.column_config.NumberColumn(
                        "Total Distance (km)",
                        format="%.1f"
                    ),
                    "Average Distance": st.column_config.NumberColumn(
                        "Average Distance (km)",
                        format="%.1f"
                    )
                }
            )

            # Chart showing total distance by period
            fig_summary = px.bar(
                summary_df,
                x='Period',
                y='Total Distance',
                title='Total Distance by Period',
                color='Total Distance',
                color_continuous_scale='viridis'
            )
            fig_summary.update_layout(showlegend=False)
            st.plotly_chart(fig_summary, use_container_width=True)
