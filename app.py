import streamlit as st
import plotly.graph_objects as go
import random

# --- CONFIG ---
st.set_page_config(page_title="BO Score", layout="wide")

# --- STYLES ---
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
    margin-bottom: 1rem;
    font-weight: 700;
}
.section {
    font-size: 1.1rem;
    font-weight: 600;
    color: #3D2C8D;
}
.score-wrapper {
    position: relative;
    width: 280px;
    height: 280px;
    margin: auto;
}
.halo {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    border-radius: 50%;
    box-shadow: 0 0 60px 25px rgba(61,44,141,0.25);
    animation: pulse 3s ease-in-out infinite;
    z-index: 1;
}
@keyframes pulse {
    0% { box-shadow: 0 0 40px 15px rgba(61,44,141,0.15); }
    50% { box-shadow: 0 0 70px 25px rgba(61,44,141,0.35); }
    100% { box-shadow: 0 0 40px 15px rgba(61,44,141,0.15); }
}
.chart {
    position: absolute;
    top: 0;
    left: 0;
    z-index: 2;
}
</style>
""", unsafe_allow_html=True)

# --- TITRE ---
st.markdown("<h1 id='bo-score'>BO Score</h1>", unsafe_allow_html=True)

# --- CLIENT ---
clients = [
    {"nom": "GreenHydro SAS", "secteur": "Énergies renouvelables", "montant": "2,4 M€", "pays": "France", "analyste": "A. Morel"},
    {"nom": "NeoTech Ventures", "secteur": "Technologies médicales", "montant": "1,8 M€", "pays": "Suisse", "analyste": "M. El Amrani"},
    {"nom": "BlueWave Capital", "secteur": "Finance durable", "montant": "3,6 M€", "pays": "Belgique", "analyste": "L. Dupont"},
    {"nom": "AgriNova Ltd", "secteur": "AgriTech", "montant": "1,2 M€", "pays": "Pays-Bas", "analyste": "C. Bernard"}
]
client = random.choice(clients)

col1, col2, col3 = st.columns([1, 2, 1])

# --- INFOS CLIENT ---
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

# --- FONCTION COULEUR ---
def score_color(val):
    if val < 50: return "#E63946"  # rouge
    elif val < 80: return "#F4A261"  # orange
    else: return "#2A9D8F"  # vert

# --- SCORE ---
solidite = st.slider("Solidité financière", 0, 10, 6)
experience = st.slider("Expérience de l’équipe dirigeante", 0, 10, 7)
rentabilite = st.slider("Rentabilité estimée du projet", 0, 10, 5)
risque = st.slider("Risque sectoriel", 0, 10, 4)
alignement = st.slider("Alignement stratégique", 0, 10, 6)

score_10 = (
    solidite * 0.30
    + rentabilite * 0.25
    + experience * 0.20
    + (10 - risque) * 0.15
    + alignement * 0.10
)
score_100 = round(score_10 * 10, 1)
color = score_color(score_100)

# --- CERCLE + HALO ---
with col2:
    st.markdown(f"""
    <div class="score-wrapper">
        <div class="halo" style="box-shadow: 0 0 60px 25px {color}40;"></div>
        <div class="chart" id="chart"></div>
    </div>
    """, unsafe_allow_html=True)

    fig = go.Figure(go.Pie(
        values=[score_100, 100 - score_100],
        hole=0.8,
        marker_colors=[color, "#EFEAFB"],
        textinfo="none",
        sort=False,
        direction="clockwise"
    ))
    fig.add_annotation(
        text=f"<span style='font-size:70px; color:{color}; font-weight:700'>{int(score_100)}</span>",
        x=0.5, y=0.5, showarrow=False
    )
    fig.update_layout(
        showlegend=False,
        margin=dict(t=0, b=0, l=0, r=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=300,
    )
    st.plotly_chart(fig, use_container_width=True)

# --- INDICATEURS ---
with col3:
    st.markdown("<div class='section'>Indicateurs complémentaires</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Rendement", f"{round(rentabilite * 1.2, 1)} %")
    c2.metric("Risque ajusté", f"{round((10 - risque) * 10, 1)} / 100")
    c3.metric("Maturité", f"{round(experience * 10, 1)} / 100")
