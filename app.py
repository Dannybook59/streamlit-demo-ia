import streamlit as st
import plotly.graph_objects as go
import random

# =========================
# CONFIG & THEME (violet clair pro)
# =========================
st.set_page_config(page_title="BO Score", layout="wide")

st.markdown("""
<style>
    .stApp {
        background-color: #E7E3FA;
        color: #2E2B3F;
        font-family: 'Segoe UI', sans-serif;
    }
    h1, h2, h3 {
        color: #3D2C8D;
        font-weight: 600;
    }
    .section {
        font-size: 1.05rem;
        font-weight: 600;
        color: #4B3C8A;
        margin-top: 0.5rem;
        margin-bottom: 0.6rem;
    }
    .block {
        background-color: transparent;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .muted {
        color: #3A3548;
        font-size: 0.95rem;
    }
    hr {
        border: none;
        border-top: 1px solid #C6BCE8;
        margin: 0.8rem 0;
    }
    .metric {
        background-color: rgba(255, 255, 255, 0.15);
        border-radius: 10px;
        padding: 0.8rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h2>BO Score — Évaluation IA des dossiers d’investissement</h2>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# =========================
# CLIENTS FACTICES
# =========================
clients = [
    {"nom": "GreenHydro SAS", "secteur": "Énergies renouvelables", "montant": "2,4 M€", "pays": "France", "analyste": "A. Morel"},
    {"nom": "NeoTech Ventures", "secteur": "Technologies médicales", "montant": "1,8 M€", "pays": "Suisse", "analyste": "M. El Amrani"},
    {"nom": "BlueWave Capital", "secteur": "Finance durable", "montant": "3,6 M€", "pays": "Belgique", "analyste": "L. Dupont"},
    {"nom": "AgriNova Ltd", "secteur": "AgriTech", "montant": "1,2 M€", "pays": "Pays-Bas", "analyste": "C. Bernard"}
]
client = random.choice(clients)

# =========================
# LAYOUT RADIAL (3 x 3)
# =========================
r1c1, r1c2, r1c3 = st.columns([1, 1, 1])
r2c1, r2c2, r2c3 = st.columns([1, 1, 1])
r3c1, r3c2, r3c3 = st.columns([1, 1, 1])

# --- TOP LEFT : FICHE CLIENT ---
with r1c1:
    st.markdown("<div class='section'>Dossier client</div>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class='muted'>
        <b>Entreprise :</b> {client['nom']}<br>
        <b>Secteur :</b> {client['secteur']}<br>
        <b>Montant demandé :</b> {client['montant']}<br>
        <b>Pays :</b> {client['pays']}<br>
        <b>Analyste référent :</b> {client['analyste']}
        </div>
        """, unsafe_allow_html=True
    )

# --- BOTTOM LEFT : SLIDERS (CRITÈRES) ---
with r3c1:
    st.markdown("<div class='section'>Évaluation des critères</div>", unsafe_allow_html=True)
    solidite = st.slider("Solidité financière", 0, 10, 6)
    experience = st.slider("Expérience de l’équipe dirigeante", 0, 10, 7)
    rentabilite = st.slider("Rentabilité estimée du projet", 0, 10, 5)
    risque = st.slider("Risque sectoriel", 0, 10, 4)
    alignement = st.slider("Alignement stratégique", 0, 10, 6)

# --- SCORE CALCUL ---
score = (
    solidite * 0.30
    + rentabilite * 0.25
    + experience * 0.20
    + (10 - risque) * 0.15
    + alignement * 0.10
)

def score_color(val):
    if val < 5:
        return "#E63946"
    elif val < 8:
        return "#F4A261"
    else:
        return "#2A9D8F"

# --- CENTRE : SCORE ---
with r2c2:
    color = score_color(score)
    fig = go.Figure(go.Pie(
        values=[score, 10 - score],
        hole=0.8,
        marker_colors=[color, "#D3C7F7"],  # violet clair autour
        textinfo="none"
    ))
    fig.add_annotation(
        text=f"<span style='font-size:46px; color:{color}; font-weight:600'>{score:.1f}</span><br><span style='font-size:18px; color:#3E3A4F;'>/10</span>",
        x=0.5, y=0.5, showarrow=False
    )
    fig.update_layout(
        showlegend=False,
        margin=dict(t=0, b=0, l=0, r=0),
        paper_bgcolor="#E7E3FA",  # plus de fond blanc
        height=360,
    )
    st.plotly_chart(fig, use_container_width=True)

# --- TOP RIGHT : INDICATEURS ---
with r1c3:
    st.markdown("<div class='section'>Indicateurs complémentaires</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Potentiel rendement", f"{round(rentabilite * 1.2, 1)} %")
    c2.metric("Risque ajusté", f"{round((10 - risque) * 10, 1)} / 100")
    c3.metric("Maturité projet", f"{round(experience * 10, 1)} / 100")

# --- BOTTOM RIGHT : VALIDATION ---
with r3c3:
    st.markdown("<div class='section'>Validation par l’analyste</div>", unsafe_allow_html=True)
    decision = st.radio("Décision finale :", ["En attente", "Valider le dossier", "Rejeter le dossier"], horizontal=True)
    commentaire = st.text_area("Commentaires / observations")

    if decision == "Valider le dossier":
        synthese = f"Score {score:.1f}/10 : profil favorable. Validation recommandée."
        tone = "success"
    elif decision == "Rejeter le dossier":
        synthese = f"Score {score:.1f}/10 : profil insuffisant. Validation non conseillée."
        tone = "error"
    else:
        synthese = f"Score {score:.1f}/10 : décision en attente."
        tone = "warning"

    getattr(st, tone)(synthese)
    if commentaire:
        st.info(f"Commentaire : {commentaire}")

st.caption("© 2025 BO Score — IA d’aide à la décision. Design clair, contrasté et lisible.")
