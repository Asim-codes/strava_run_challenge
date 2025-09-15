import streamlit as st

st.set_page_config(
    page_title="Leaderboard System", 
    page_icon="🏅", 
    layout="wide"
)

# Mobile-friendly navigation using st.navigation
current_leaderboard_page = st.Page(
    "pages/current_leaderboard.py", 
    title="Current Leaderboard", 
    icon="🏆"
)
archive_page = st.Page(
    "pages/archive.py", 
    title="Archive", 
    icon="🗃️"
)

pg = st.navigation([current_leaderboard_page, archive_page])
pg.run()
