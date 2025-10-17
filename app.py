import streamlit as st
import plotly.graph_objects as go
import random

st.set_page_config(page_title="CriteriA", layout="wide", initial_sidebar_state="collapsed")

# Force le thème clair
st.markdown("""
    <style>
        [data-testid="stAppViewContainer"], .stApp {
            background-color: #FFFFFF !important;
            color: #3D2C8D !important;
        }
        [data-testid="stHeader"] {
            background: none !important;
        }
        [data-testid="stToolbar"] { display: none !important; }
    </style>
""", unsafe_allow_html=True)


# =========================
# CONFIG & STYLE
# =========================
st.set_page_config(page_title="CriteriA", layout="wide")

# --- STYLE GLOBAL ---
st.markdown("""
<style>
    html, body, [class*="css"]  {
        margin: 0;
        padding: 0;
        overflow: hidden !important;
        height: 100vh !important;
        background-color: #FFFFFF !important;
        color: #3D2C8D !important;
        font-family: 'Segoe UI', sans-serif !important;
    }

    section.main > div { 
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        height: 100vh !important;
    }

    .criteria-logo {
        font-weight: 700;
        font-size: 2.8rem;
        text-align: center;
        color: #3D2C8D;
        margin-bottom: 0.3rem;
    }

    .criteria-logo span {
        color: #7A5AF8;
    }

    h1, h2, h3, h4, h5, h6, label, p, div, span {
        color: #3D2C8D !important;
    }

    .comment-box, .radio-group {
        border: 2px solid #C7B8F5;
        border-radius: 8px;
        background-color: #FFFFFF;
        padding: 0.8rem;
    }

    textarea {
        background-color: #FFFFFF !important;
        color: #3D2C8D !important;
        border: 1px solid #C7B8F5 !important;
        border-radius: 6px !important;
    }

    .section {
        font-size: 1.1rem;
        font-weight: 600;
        margin-top: 0.5rem;
        margin-bottom: 0.3rem;
    }

    hr {
        border: none;
        border-top: 1px solid #C7B8F5;
        margin: 0.3rem 0;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# CLIENTS
# =========================
clients = [
    {"nom": "GreenHydro SAS", "secteur": "Énergies renouvelables", "montant": "2,4 M€", "pays": "France", "analyste": "A. Morel"},
    {"nom": "NeoTech Ventures", "secteur": "Technologies médicales", "montant": "1,8 M€", "pays": "Suisse", "analyste": "M. El Amrani"},
    {"nom": "BlueWave Capital", "secteur": "Finance durable", "montant": "3,6 M€", "pays": "Belgique", "analyste": "L. Dupont"},
    {"nom": "AgriNova Ltd", "secteur": "AgriTech", "montant": "1,2 M€", "pays": "Pays-Bas", "analyste": "C. Bernard"}
]
client = random.choice(clients)

# =========================
# LAYOUT PRINCIPAL
# =========================
st.markdown("<h1 class='criteria-logo'>Criteri<span>IA</span></h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1.2, 1, 1.2])

# --- FICHE CLIENT ---
with col1:
    st.markdown("<div class='section'>Dossier client</div>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <b>Entreprise :</b> {client['nom']}<br>
        <b>Secteur :</b> {client['secteur']}<br>
        <b>Montant demandé :</b> {client['montant']}<br>
        <b>Pays :</b> {client['pays']}<br>
        <b>Analyste référent :</b> {client['analyste']}
        """, unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    solidite = st.slider("Solidité financière", 0, 10, 6)
    experience = st.slider("Expérience de l’équipe dirigeante", 0, 10, 7)
    rentabilite = st.slider("Rentabilité estimée du projet", 0, 10, 5)
    risque = st.slider("Risque sectoriel", 0, 10, 4)
    alignement = st.slider("Alignement stratégique", 0, 10, 6)

# --- SCORE ---
score_10 = (solidite * 0.3 + rentabilite * 0.25 + experience * 0.2 + (10 - risque) * 0.15 + alignement * 0.1)
score_100 = round(score_10 * 10, 1)

def score_color(val):
    if val < 50: return "#E63946"
    elif val < 80: return "#F4A261"
    else: return "#2A9D8F"

with col2:
    color = score_color(score_100)
    fig = go.Figure(go.Pie(values=[score_100, 100 - score_100],
                           hole=0.8, marker_colors=[color, "#EFEAFB"],
                           textinfo="none", sort=False, direction="clockwise"))
    fig.add_annotation(text=f"<span style='font-size:70px; color:{color}; font-weight:700'>{int(score_100)}</span>",
                       x=0.5, y=0.5, showarrow=False)
    fig.update_layout(showlegend=False, margin=dict(t=0,b=0,l=0,r=0),
                      paper_bgcolor="#FFFFFF", height=320)
    st.plotly_chart(fig, use_container_width=True)

# --- INDICATEURS + MESSAGE ---
with col3:
    st.markdown("<div class='section'>Indicateurs complémentaires</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Rendement", f"{round(rentabilite * 1.2, 1)} %")
    c2.metric("Risque ajusté", f"{round((10 - risque) * 10, 1)} / 100")
    c3.metric("Maturité", f"{round(experience * 10, 1)} / 100")

    # --- Message coloré ---
    if score_100 >= 80:
        message = f"Score {score_100:.0f} — Dossier solide, validation recommandée."
        style = "background-color:#E8F9F1; color:#2A9D8F; border-left:6px solid #2A9D8F;"
    elif score_100 >= 50:
        message = f"Score {score_100:.0f} — Dossier intéressant, à vérifier."
        style = "background-color:#FFF4E0; color:#F4A261; border-left:6px solid #F4A261;"
    else:
        message = f"Score {score_100:.0f} — Risque élevé, validation non conseillée."
        style = "background-color:#FDEAEA; color:#E63946; border-left:6px solid #E63946;"

    st.markdown(
        f"<div style='{style} padding:10px 15px; border-radius:6px; margin-top:15px; font-weight:700; font-size:1.05rem;'>{message}</div>",
        unsafe_allow_html=True
    )

# --- DECISION + COMMENTAIRES (fixes et regroupés à droite) ---
st.markdown("<hr>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1.3, 1.2, 1.5])

with col3:
    st.markdown("<div class='section'>Décision finale</div>", unsafe_allow_html=True)
    st.markdown("<div class='radio-group'>", unsafe_allow_html=True)
    decision = st.radio("Choisir une option :", ["En attente", "Valider le dossier", "Rejeter le dossier"], horizontal=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section' style='margin-top:10px;'>Commentaires</div>", unsafe_allow_html=True)
    st.markdown("<div class='comment-box'>", unsafe_allow_html=True)
    commentaire = st.text_area("Commentaires / observations", height=90, label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)

