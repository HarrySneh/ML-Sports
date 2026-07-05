# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from src.auth import login
from src.data_loader import load_all_data
from src.model import train_model
from src.api import get_live_matches
from dotenv import load_dotenv
load_dotenv()  # force load


# ---- MUST BE THE FIRST STREAMLIT COMMAND ----
st.set_page_config(page_title="Sports Analytics Pro", layout="wide")

# ---- SESSION STATE INITIALIZATION ----
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---- LOGIN SCREEN ----
if not st.session_state.logged_in:
    st.title("🔐 Login to Sports Analytics Platform")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            if login(username, password):
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid credentials")
    st.stop()  # Prevent the rest of the app from loading

# ---- LOGOUT BUTTON (sidebar) ----
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

# ---- LOAD DATA & MODEL (with spinners) ----
with st.spinner("Loading data..."):
    df = load_all_data()          # uses caching
    model, scaler = train_model(df)

# ---- HEADER ----
st.title("🏆 Sports Analytics Pro")
st.markdown("### Real-Time Multi-Sport Performance Dashboard")
st.markdown("---")

# ---- LIVE MATCHES ----
st.subheader("⚡ Live Football Matches")
matches = get_live_matches()
for m in matches[:5]:
    st.write(f"**{m['homeTeam']} vs {m['awayTeam']}** – {m['status']}")

# ---- SIDEBAR FILTERS ----
st.sidebar.title("📊 Controls")
sports = st.sidebar.multiselect(
    "Select Sport",
    df['sport'].unique(),
    default=df['sport'].unique()
)
filtered_df = df[df['sport'].isin(sports)]

# ---- PLAYER SEARCH ----
st.subheader("🔎 Player / Fighter Search")
search_name = st.text_input("Enter player or fighter name")
if search_name:
    results = filtered_df[filtered_df['Name'].str.contains(search_name, case=False, na=False)]
    if not results.empty:
        st.dataframe(results.head(10))
    else:
        st.warning("No results found")

# ---- KPIs ----
col1, col2, col3 = st.columns(3)
col1.metric("Athletes", len(filtered_df))
col2.metric("Avg Age", round(filtered_df['Age'].mean(), 1))
col3.metric("Avg Performance Score", round(filtered_df['performance_score'].mean(), 2))

# ---- VISUALISATIONS (Plotly) ----
st.subheader("📈 Performance Insights")
col4, col5 = st.columns(2)

with col4:
    fig_age = px.histogram(filtered_df, x='Age', nbins=30, title="Age Distribution")
    st.plotly_chart(fig_age, use_container_width=True)

with col5:
    fig_perf = px.box(filtered_df, x='sport', y='performance_score', title="Performance by Sport")
    st.plotly_chart(fig_perf, use_container_width=True)

st.subheader("📏 Athlete Physical Analysis")
fig_scatter = px.scatter(
    filtered_df,
    x='Height',
    y='Weight',
    color='sport',
    hover_data=['Name'],
    title="Height vs Weight"
)
st.plotly_chart(fig_scatter, use_container_width=True)

# ---- AI PREDICTOR ----
st.subheader("🧠 AI Performance Predictor")
col_age, col_height, col_weight = st.columns(3)
with col_age:
    age = st.slider("Age", 15, 45, 25)
with col_height:
    height = st.slider("Height (cm)", 150, 220, 175)
with col_weight:
    weight = st.slider("Weight (kg)", 50, 120, 70)

if st.button("Predict"):
    # Scale input using the fitted scaler
    input_scaled = scaler.transform([[age, height, weight]])
    pred = model.predict(input_scaled)[0]
    if pred == 1:
        st.success("🔥 High Performance Athlete")
    else:
        st.error("⚠️ Lower Performance Potential")

# ---- DATA TABLE ----
st.subheader("📋 Data Preview")
st.dataframe(filtered_df.head(50))

# ---- CUSTOM STYLING (optional) ----
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .st-bb { background-color: #262730; }
</style>
""", unsafe_allow_html=True)

# ---- PLAYER COMPARISON ----
st.subheader("⚖️ Player Comparison")
col_p1, col_p2 = st.columns(2)
with col_p1:
    player1 = st.selectbox("Select first player", filtered_df['Name'].unique())
with col_p2:
    player2 = st.selectbox("Select second player", filtered_df['Name'].unique())

if player1 and player2 and player1 != player2:
    p1 = filtered_df[filtered_df['Name'] == player1].iloc[0]
    p2 = filtered_df[filtered_df['Name'] == player2].iloc[0]
    comp_df = pd.DataFrame({
        'Metric': ['Age', 'Height', 'Weight', 'Performance'],
        player1: [p1['Age'], p1['Height'], p1['Weight'], p1['performance_score']],
        player2: [p2['Age'], p2['Height'], p2['Weight'], p2['performance_score']]
    })
    st.dataframe(comp_df)
    
    # Bar chart comparison
    fig_comp = px.bar(comp_df.melt(id_vars='Metric', var_name='Player', value_name='Value'),
                     x='Metric', y='Value', color='Player', barmode='group')
    st.plotly_chart(fig_comp, use_container_width=True)
    
# ---- PERFORMANCE TREND ----
if 'Date' in filtered_df.columns:
    st.subheader("📈 Performance Trends")
    # Convert to datetime
    filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])
    # Group by date and sport (or athlete)
    trend_data = filtered_df.groupby(['Date', 'sport'])['performance_score'].mean().reset_index()
    fig_trend = px.line(trend_data, x='Date', y='performance_score', color='sport',
                        title="Average Performance Over Time")
    st.plotly_chart(fig_trend, use_container_width=True)
    
# ---- EXPORT DATA ----
st.subheader("📥 Export Data")
csv = filtered_df.to_csv(index=False)
st.download_button(
    label="Download Filtered Data as CSV",
    data=csv,
    file_name="sports_data.csv",
    mime="text/csv"
)