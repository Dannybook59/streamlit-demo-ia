import streamlit as st
import plotly.graph_objects as go

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Eurinvest Connect - IA Scoring",
    page_icon="💼",
    layout="centered"
)

# --- STYLE PERSONNALISÉ ---
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #0d1117 0%, #1c2331 100%);
            color: #f0f0f0;
        }
        h1, h2, h3 {
            color: #00b4d8 !important;
            text-align: center;
        }
        .block-container {
            padding: 2rem 3rem;
            background-color: rgba(255, 255, 255, 0.05);
            border-radius: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }
    </style>
""", unsafe_allow_html=True)

# --- EN-TÊTE ---
st.title("💼 Eurinvest Connect")
st.markdown("### Outil d’aide à la décision IA & validation humaine")

st.markdown("---")

# --- SECTION : ÉVALUATION DES CRITÈRES ---
st.header("1️⃣ Évaluation des critères")

col1, col2 = st.columns(2)
with col1:
    solidite = st.slider("Solidité financière", 0, 10, 6)
    experience = st.slider("Expérience de l’équipe dirigeante", 0, 10, 7)
    rentabilite = st.slider("Rentabilité estimée du projet", 0, 10, 5)
with col2:
    risque = st.slider("Risque sectoriel", 0, 10, 4)
    alignement = st.slider("Alignement stratégique avec le fonds", 0, 10, 6)

st.markdown("---")

# --- CALCUL DU SCORE ---
st.header("2️⃣ Résultat du scoring IA")

score = (
    solidite * 0.3
    + rentabilite * 0.25
    + experience * 0.2
    + (10 - risque) * 0.15
    + alignement * 0.1
)

# --- VISUALISATION CIRCULAIRE DU SCORE ---
fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=score,
    domain={'x': [0, 1], 'y': [0, 1]},
    title={'text': "Score global", 'font': {'size': 20, 'color': '#90e0ef'}},
    gauge={
        'axis': {'range': [0, 10], 'tickwidth': 1, 'tickcolor': "#90e0ef"},
        'bar': {'color': "#00b4d8"},
        'bgcolor': "rgba(0,0,0,0)",
        'borderwidth': 2


