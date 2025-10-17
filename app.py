import streamlit as st
import plotly.graph_objects as go
import random
import time

# --- CONFIGURATION GLOBALE ---
st.set_page_config(page_title="BO Score", layout="wide")

# --- STYLE ---
st.markdown("""
<style>
html, body, .stApp {
    background-color: #FFFFFF;
    color: #3D2C8D;
    font-family: 'Segoe UI', sans-serif;
    overflow: hidden !important;
    height: 100vh !important;
}
h1#bo-score {
    text-align: center;
    color: #3D2C8D;
    font-size: 3rem;
    margin-bottom: 0.5rem;
    font-weight: 700;
}
.section {
    font-size: 1.1rem;
    font-weight: 600;
    color: #3D2C8D;
}
.halo-container {
    position: relative;
    width: 300px;
    height: 300px;
    margin: auto;
}
.halo-glow {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    border-radius: 50%;
    animation: pulse 3s ease-in-out infinite;
    z-index: 0;
}
@keyframes pulse {
    0% { box-shadow: 0 0 30px 10px rgba(61,44,141,0.15); }
    50% { box-shadow: 0 0 60px 25px rgba(61,44,141,0.35); }
    100% { box-shadow: 0 0 30px 10px rgba(61,44,141,0.15); }
}
.comment-box {
    border: 2px solid #C7B8F5;
    border-radius: 8px;
    background-color: #FFFFFF;
    padding: 0.8rem;
}
.radio-group {
    border: 2px solid #C7B8F5;
    border-radius: 8px;
    padding: 0.8rem;
    background-color: #FFFFFF;
}
</style>
""", unsafe_allow_html=True)

# --- TITRE ---
st.markdown("<h1 id='bo-score'>BO Score</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# --- CLIENT FACTICE ---
clients = [
    {"nom": "GreenHydro SAS", "secteur": "Énergies renouvelables", "montant": "2,4 M€", "pays": "France", "analyste": "A. Morel"},
    {"nom": "NeoTech Ventures", "secteur": "Technologies médicales", "montant": "1,8 M€", "pays": "Suisse", "analyste": "M. El Amrani"},
    {"nom": "BlueWave Capital", "secteur": "Finance durable", "montant": "3,6 M€", "pays": "Belgique", "analyste": "L. Dupont"},
    {"nom": "AgriNova Ltd", "secteur": "AgriTech", "montant": "1,2 M€", "pays": "Pays-Bas", "analyste": "C. Bernard"}
]
client = random.choice(clients)

# --- FONCTION COULEUR ---
def score_color(val):
    if val < 50: return "#E63946"  # rouge
    elif val < 80: return "#F4A261"  # orange
    else: return "#2A9D8F"  # vert

# --- MISE EN PAGE ---
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.markdown("<div class='section'>Dossier client</div>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <b>Entreprise :</b> {client['nom']}<br>
        <b>Secteur :</b> {client['secteur']}<br>
        <b>Montant demandé :</b> {client['montant']}<br>
        <b>Pays :</b> {client['pays']}<br>
        <b>Analyste référent :</b> {client['analyste']}
        """, unsafe_allow_html=True
    )

# --- SLIDERS ---
solidite = st.slider("Solidité financière", 0, 10, 6)
experience = st.slider("Expérience de l’équipe dirigeante", 0, 10, 7)
rentabilite = st.slider("Rentabilité estimée du projet", 0, 10, 5)
risque = st.slider("Risque sectoriel", 0, 10, 4)
alignement = st.slider("Alignement stratégique", 0, 10, 6)

# --- SCORE ---
score_10 = (
    solidite * 0.30
    + rentabilite * 0.25
    + experience * 0.20
    + (10 - risque) * 0.15
    + alignement * 0.10
)
score_100 = round(score_10 * 10, 1)

# --- SCORE CERCLE ---
with col2:
    color = score_color(score_100)
    st.markdown(
        f"""
        <div class="halo-container">
            <div class="halo-glow" style="box-shadow: 0 0 60px 25px {color}40;"></div>
        </div>
        """,
        unsafe_allow_html=True
    )

    placeholder = st.empty()
    for val in range(0, int(score_100) + 1, 3):
        fig = go.Figure(go.Pie(
            values=[val, 100 - val],
            hole=0.8,
            marker_colors=[score_color(val), "#EFEAFB"],
            textinfo="none",
            sort=False,
            direction="clockwise"
        ))
        fig.add_annotation(
            text=f"<span style='font-size:70px; color:{score_color(val)}; font-weight:700'>{val}</span>",
            x=0.5, y=0.5, showarrow=False
        )
        fig.update_layout(
            showlegend=False,
            margin=dict(t=0, b=0, l=0, r=0),
            paper_bgcolor="#FFFFFF",
            height=300,
        )
        placeholder.plotly_chart(fig, use_container_width=True)
        time.sleep(0.02)

# --- INDICATEURS ---
with col3:
    st.markdown("<div class='section'>Indicateurs complémentaires</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Rendement", f"{round(rentabilite * 1.2, 1)} %")
    c2.metric("Risque ajusté", f"{round((10 - risque) * 10, 1)} / 100")
    c3.metric("Maturité", f"{round(experience * 10, 1)} / 100")
