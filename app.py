import streamlit as st
import plotly.graph_objects as go
import random

# --- CONFIGURATION ---
st.set_page_config(page_title="BO Score", layout="wide")

# --- STYLE GLOBAL ---
st.markdown("""
    <style>
        .stApp {
            background-color: #E9E3F9; /* violet très clair */
            color: #2B2730;
            font-family: 'Segoe UI', sans-serif;
        }
        h1, h2, h3 {
            font-weight: 600;
            color: #4B3C8A; /* violet profond */
        }
        .section-title {
            font-size: 1.1rem;
            font-weight: 600;
            color: #5A4CA1;
            margin-top: 1.2rem;
            margin-bottom: 0.6rem;
        }
        .client-box, .score-box, .summary-box {
            background-color: #F8F6FC;
            border-radius: 10px;
            padding: 1rem 1.5rem;
            border: 1px solid #D2C9F2;
            box-shadow: 0 2px 8px rgba(75, 60, 138, 0.08);
            margin-bottom: 1.5rem;
        }
        .metric-label {
            color: #4B4B4B;
            font-size: 0.9rem;
        }
        .metric-value {
            font-weight: 600;
            font-size: 1.1rem;
            color: #4B3C8A;
        }
        .stSlider label, .stRadio label {
            color: #2B2730 !important;
            font-weight: 400 !important;
        }
        textarea {
            border-radius: 8px !important;
        }
        hr {
            border: none;
            border-top: 1px solid #C9BFEF;
            margin: 1rem 0;
        }
    </style>
""", unsafe_allow_html=True)

# --- EN-TÊTE ---
st.markdown("<h2>BO Score — Évaluation IA des dossiers d’investissement</h2>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# --- CLIENTS FACTICES ---
clients = [
    {"nom": "GreenHydro SAS", "secteur": "Énergies renouvelables", "montant": "2,4 M€", "pays": "France", "analyste": "A. Morel"},
    {"nom": "NeoTech Ventures", "secteur": "Technologies médicales", "montant": "1,8 M€", "pays": "Suisse", "analyste": "M. El Amrani"},
    {"nom": "BlueWave Capital", "secteur": "Finance durable", "montant": "3,6 M€", "pays": "Belgique", "analyste": "L. Dupont"},
    {"nom": "AgriNova Ltd", "secteur": "AgriTech", "montant": "1,2 M€", "pays": "Pays-Bas", "analyste": "C. Bernard"}
]
client = random.choice(clients)

# --- DISPOSITION ---
col1, col2 = st.columns([1, 1])

# --- FICHE CLIENT ---
with col1:
    st.markdown("<div class='section-title'>Dossier client</div>", unsafe_allow_html=True)
    st.markdown(f"""
        <div class='client-box'>
            <b>Nom de l’entreprise :</b> {client['nom']}<br>
            <b>Secteur :</b> {client['secteur']}<br>
            <b>Montant demandé :</b> {client['montant']}<br>
            <b>Pays :</b> {client['pays']}<br>
            <b>Analyste référent :</b> {client['analyste']}
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Évaluation des critères</div>", unsafe_allow_html=True)
    solidite = st.slider("Solidité financière", 0, 10, 6)
    experience = st.slider("Expérience de l’équipe dirigeante", 0, 10, 7)
    rentabilite = st.slider("Rentabilité estimée du projet", 0, 10, 5)
    risque = st.slider("Risque sectoriel", 0, 10, 4)
    alignement = st.slider("Alignement stratégique", 0, 10, 6)

# --- SCORE + INDICATEURS ---
with col2:
    st.markdown("<div class='section-title'>Résultat du BO Score</div>", unsafe_allow_html=True)
    score = (
        solidite * 0.3
        + rentabilite * 0.25
        + experience * 0.2
        + (10 - risque) * 0.15
        + alignement * 0.1
    )

    # Couleurs du score (rouge → jaune → vert)
    if score < 5:
        color = "#E63946"
    elif score < 8:
        color = "#F4A261"
    else:
        color = "#2A9D8F"

    fig = go.Figure(go.Pie(
        values=[score, 10 - score],
        hole=0.7,
        marker_colors=[color, "#E9E3F9"],
        textinfo="none"
    ))
    fig.add_annotation(
        text=f"<span style='font-size:36px; color:{color}'>{score:.1f}</span><br><span style='font-size:18px;'>/10</span>",
        x=0.5, y=0.5, showarrow=False
    )
    fig.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0), paper_bgcolor="#F8F6FC", height=280)

    st.markdown("<div class='score-box'>", unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)

    # Indicateurs complémentaires
    st.markdown("##### Indicateurs complémentaires")
    colA, colB, colC = st.columns(3)
    colA.metric("Potentiel de rendement", f"{round(rentabilite * 1.2, 1)} %")
    colB.metric("Risque ajusté", f"{round((10 - risque) * 10, 1)} / 100")
    colC.metric("Maturité du projet", f"{round(experience * 10, 1)} / 100")

    if score >= 8:
        st.success("✅ Dossier très favorable : excellente solidité et forte rentabilité.")
    elif score >= 6:
        st.warning("⚠️ Dossier intéressant : nécessite une validation approfondie.")
    else:
        st.error("❌ Dossier à risque : plusieurs indicateurs faibles.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- VALIDATION ---
st.markdown("<hr>", unsafe_allow_html=True)
st.subheader("Validation par l’analyste")

validation = st.radio(
    "Décision finale :",
    ["En attente", "Valider le dossier", "Rejeter le dossier"],
    horizontal=True
)
commentaire = st.text_area("Commentaires ou observations")

# --- SYNTHÈSE AUTOMATIQUE ---
if validation != "En attente":
    st.markdown("<div class='section-title'>Résumé décisionnel</div>", unsafe_allow_html=True)
    st.markdown("<div class='summary-box'>", unsafe_allow_html=True)

    if validation == "Valider le dossier":
        synthese = f"Le dossier **{client['nom']}** obtient un score de {score:.1f}/10. Les indicateurs financiers et stratégiques sont solides. La validation est recommandée."
    elif validation == "Rejeter le dossier":
        synthese = f"Le dossier **{client['nom']}** affiche un score de {score:.1f}/10, jugé insuffisant au regard du risque et de la rentabilité. La validation n’est pas conseillée."
    else:
        synthese = f"L’évaluation du dossier **{client['nom']}** (score {score:.1f}/10) reste en attente d’informations complémentaires."

    st.write(synthese)
    if commentaire:
        st.info(f"💬 Commentaire : {commentaire}")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)
st.caption("© 2025 BO Score — IA d’aide à la décision. Thème violet lisible.")
