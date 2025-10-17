import streamlit as st
import plotly.graph_objects as go
import random

# --- CONFIGURATION ---
st.set_page_config(page_title="BO Score", layout="wide")

# --- STYLE GLOBAL ---
st.markdown("""
    <style>
        .stApp {
            background-color: #f8f9fb;
            color: #2b2b2b;
            font-family: 'Segoe UI', sans-serif;
        }
        h1, h2, h3 {
            font-weight: 500;
            color: #1d3557;
        }
        .section-title {
            font-size: 1.1rem;
            font-weight: 600;
            color: #3a506b;
            margin-top: 1.5rem;
            margin-bottom: 0.5rem;
        }
        .client-box {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 1rem 1.5rem;
            border: 1px solid #dee2e6;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        }
        .score-box {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 1.5rem;
            border: 1px solid #dee2e6;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05);
            text-align: center;
        }
        .stSlider label {
            color: #2b2b2b !important;
            font-weight: 400 !important;
        }
        .stRadio label {
            color: #2b2b2b !important;
        }
        textarea {
            border-radius: 8px !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- EN-TÊTE ---
st.markdown("## BO Score — Système d’évaluation IA des dossiers d’investissement")
st.markdown("<hr>", unsafe_allow_html=True)

# --- CLIENTS FACTICES ---
clients = [
    {"nom": "GreenHydro SAS", "secteur": "Énergies renouvelables", "montant": "2,4 M€", "pays": "France", "analyste": "A. Morel"},
    {"nom": "NeoTech Ventures", "secteur": "Technologies médicales", "montant": "1,8 M€", "pays": "Suisse", "analyste": "M. El Amrani"},
    {"nom": "BlueWave Capital", "secteur": "Finance durable", "montant": "3,6 M€", "pays": "Belgique", "analyste": "L. Dupont"},
    {"nom": "AgriNova Ltd", "secteur": "AgriTech", "montant": "1,2 M€", "pays": "Pays-Bas", "analyste": "C. Bernard"}
]

client = random.choice(clients)

# --- DISPOSITION PRINCIPALE ---
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

# --- SCORE ---
with col2:
    st.markdown("<div class='section-title'>Résultat du BO Score</div>", unsafe_allow_html=True)
    score = (
        solidite * 0.3
        + rentabilite * 0.25
        + experience * 0.2
        + (10 - risque) * 0.15
        + alignement * 0.1
    )

    # Couleur du cercle
    if score < 5:
        color = "#c44d56"  # rouge doux
    elif score < 8:
        color = "#d3a84f"  # beige/doré
    else:
        color = "#5ba67c"  # vert doux

    fig = go.Figure(go.Pie(
        values=[score, 10 - score],
        hole=0.7,
        marker_colors=[color, "#f1f3f5"],
        textinfo="none"
    ))

    fig.add_annotation(
        text=f"<span style='font-size:36px; color:{color}'>{score:.1f}</span><br><span style='font-size:18px;'>/10</span>",
        x=0.5, y=0.5, showarrow=False
    )

    fig.update_layout(
        showlegend=False,
        margin=dict(t=0, b=0, l=0, r=0),
        paper_bgcolor="#ffffff",
        height=300
    )

    st.markdown("<div class='score-box'>", unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)

    if score >= 8:
        st.success("Dossier très favorable : excellente solidité et forte rentabilité.")
    elif score >= 6:
        st.warning("Dossier intéressant : nécessite une validation approfondie.")
    else:
        st.error("Dossier à risque : plusieurs indicateurs faibles.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- VALIDATION HUMAINE ---
st.markdown("<hr>", unsafe_allow_html=True)
st.subheader("Validation par l’analyste")

validation = st.radio(
    "Décision finale :",
    ["En attente", "Valider le dossier", "Rejeter le dossier"],
    horizontal=True
)

commentaire = st.text_area("Commentaires ou observations")

if validation != "En attente":
    st.success(f"Décision enregistrée : **{validation}**")
    if commentaire:
        st.info(f"Commentaire : {commentaire}")

st.markdown("<hr>", unsafe_allow_html=True)
st.caption("© 2025 BO Score — IA d’aide à la décision. Tous droits réservés.")
