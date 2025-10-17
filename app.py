import streamlit as st
import plotly.graph_objects as go
import random

# =========================
# CONFIG & STYLE
# =========================
st.set_page_config(page_title="BO Score", layout="wide")

st.markdown("""
<style>
    .stApp {
        background-color: #FFFFFF;
        color: #3D2C8D;
        font-family: 'Segoe UI', sans-serif;
    }
    h1, h2, h3, label, .stMarkdown, p, div, span {
        color: #3D2C8D !important;
    }
    h1#bo-score {
        text-align: center;
        color: #3D2C8D;
        font-size: 3rem;
        margin-bottom: 1.5rem;
        margin-top: -0.5rem;
        font-weight: 700;
    }
    .section {
        font-size: 1.1rem;
        font-weight: 600;
        color: #3D2C8D;
        margin-top: 0.8rem;
        margin-bottom: 0.5rem;
    }
    hr {
        border: none;
        border-top: 1px solid #C7B8F5;
        margin: 1rem 0;
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
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# --- TITRE PRINCIPAL ---
st.markdown("<h1 id='bo-score'>BO Score</h1>", unsafe_allow_html=True)
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
# LAYOUT RADIAL
# =========================
r1c1, r1c2, r1c3 = st.columns([1, 1, 1])
r2c1, r2c2, r2c3 = st.columns([1, 1, 1])
r3c1, r3c2, r3c3 = st.columns([1, 1, 1])

# --- FICHE CLIENT ---
with r1c1:
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

# --- SLIDERS (CRITÈRES) ---
with r3c1:
    st.markdown("<div class='section'>Évaluation des critères</div>", unsafe_allow_html=True)
    solidite = st.slider("Solidité financière", 0, 10, 6)
    experience = st.slider("Expérience de l’équipe dirigeante", 0, 10, 7)
    rentabilite = st.slider("Rentabilité estimée du projet", 0, 10, 5)
    risque = st.slider("Risque sectoriel", 0, 10, 4)
    alignement = st.slider("Alignement stratégique", 0, 10, 6)

# --- SCORE CALCUL ---
score_10 = (
    solidite * 0.30
    + rentabilite * 0.25
    + experience * 0.20
    + (10 - risque) * 0.15
    + alignement * 0.10
)
score_100 = round(score_10 * 10, 1)

def score_color(val):
    if val < 50:
        return "#E63946"  # rouge
    elif val < 80:
        return "#F4A261"  # jaune
    else:
        return "#2A9D8F"  # vert

# --- SCORE CENTRAL ---
with r2c2:
    color = score_color(score_100)
    fig = go.Figure(go.Pie(
        values=[score_100, 100 - score_100],
        hole=0.8,
        marker_colors=[color, "#EFEAFB"],
        textinfo="none"
    ))
    fig.add_annotation(
        text=f"<span style='font-size:46px; color:{color}; font-weight:600'>{score_100:.0f}</span><br><span style='font-size:18px; color:#3D2C8D;'>/100</span>",
        x=0.5, y=0.5, showarrow=False
    )
    fig.update_layout(
        showlegend=False,
        margin=dict(t=0, b=0, l=0, r=0),
        paper_bgcolor="#FFFFFF",
        height=360,
    )
    st.plotly_chart(fig, use_container_width=True)

# --- INDICATEURS ---
with r1c3:
    st.markdown("<div class='section'>Indicateurs complémentaires</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Potentiel rendement", f"{round(rentabilite * 1.2, 1)} %")
    c2.metric("Risque ajusté", f"{round((10 - risque) * 10, 1)} / 100")
    c3.metric("Maturité projet", f"{round(experience * 10, 1)} / 100")

# --- VALIDATION ---
with r3c3:
    st.markdown("<div class='section'>Validation par l’analyste</div>", unsafe_allow_html=True)
    st.markdown("<div class='radio-group'>", unsafe_allow_html=True)
    decision = st.radio("Décision finale :", ["En attente", "Valider le dossier", "Rejeter le dossier"], horizontal=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='comment-box'>", unsafe_allow_html=True)
    commentaire = st.text_area("Commentaires / observations", height=120, label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)

    if decision == "Valider le dossier":
        synthese = f"Score {score_100:.0f}/100 : profil favorable. Validation recommandée."
        tone = "success"
    elif decision == "Rejeter le dossier":
        synthese = f"Score {score_100:.0f}/100 : profil insuffisant. Validation non conseillée."
        tone = "error"
    else:
        synthese = f"Score {score_100:.0f}/100 : décision en attente."
        tone = "warning"

    getattr(st, tone)(synthese)
    if commentaire:
        st.info(f"Commentaire : {commentaire}")

st.caption("© 2025 BO Score — IA d’aide à la décision. Thème blanc & texte violet foncé.")
