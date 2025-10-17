import streamlit as st
import plotly.graph_objects as go
import random

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="BO Score - Scoring IA",
    layout="centered"
)

# --- STYLE PERSONNALISÉ ---
st.markdown("""
    <style>
        .stApp {
            background-color: #f7f9fb;
            color: #2b2b2b;
            font-family: 'Segoe UI', sans-serif;
        }
        h1, h2, h3 {
            color: #1e2a38 !important;
            font-weight: 400 !important;
            text-align: center;
        }
        .client-box {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 1.2rem 2rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 3px 10px rgba(0,0,0,0.05);
            border: 1px solid #e0e4e8;
        }
        .block-container {
            padding: 2rem 3rem;
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
st.title("BO Score")
st.markdown("### Système d’évaluation IA des dossiers d’investissement")
st.markdown("---")

# --- DONNÉES CLIENT FACTICES ---
clients = [
    {
        "nom": "GreenHydro SAS",
        "secteur": "Énergies renouvelables",
        "montant": "2,4 M€",
        "pays": "France",
        "analyste": "A. Morel"
    },
    {
        "nom": "NeoTech Ventures",
        "secteur": "Technologies médicales",
        "montant": "1,8 M€",
        "pays": "Suisse",
        "analyste": "M. El Amrani"
    },
    {
        "nom": "BlueWave Capital",
        "secteur": "Finance durable",
        "montant": "3,6 M€",
        "pays": "Belgique",
        "analyste": "L. Dupont"
    },
    {
        "nom": "AgriNova Ltd",
        "secteur": "AgriTech",
        "montant": "1,2 M€",
        "pays": "Pays-Bas",
        "analyste": "C. Bernard"
    }
]

client = random.choice(clients)

# --- FICHE CLIENT ---
st.subheader("Dossier client")
st.markdown(
    f"""
    <div class='client-box'>
        <b>Nom de l’entreprise :</b> {client['nom']}<br>
        <b>Secteur :</b> {client['secteur']}<br>
        <b>Montant de l’investissement :</b> {client['montant']}<br>
        <b>Pays :</b> {client['pays']}<br>
        <b>Analyste référent :</b> {client['analyste']}
    </div>
    """,
    unsafe_allow_html=True
)

# --- SAISIE DES CRITÈRES ---
st.header("1. Évaluation des critères")

col1, col2 = st.columns(2)
with col1:
    solidite = st.slider("Solidité financière", 0, 10, 6)
    experience = st.slider("Expérience de l’équipe dirigeante", 0, 10, 7)
    rentabilite = st.slider("Rentabilité estimée du projet", 0, 10, 5)
with col2:
    risque = st.slider("Risque sectoriel", 0, 10, 4)
    alignement = st.slider("Alignement stratégique", 0, 10, 6)

st.markdown("---")

# --- CALCUL DU SCORE ---
st.header("2. Résultat du BO Score")

score = (
    solidite * 0.3
    + rentabilite * 0.25
    + experience * 0.2
    + (10 - risque) * 0.15
    + alignement * 0.1
)

# --- COULEUR DU CERCLE SELON LE SCORE ---
if score < 5:
    circle_color = "#e63946"  # Rouge
elif score < 8:
    circle_color = "#fcbf49"  # Jaune
else:
    circle_color = "#2a9d8f"  # Vert

# --- VISUEL : CERCLE PLEIN DU SCORE ---
fig = go.Figure(go.Pie(
    values=[score, 10 - score],
    hole=0.7,
    marker_colors=[circle_color, "#eaecef"],
    textinfo="none"
))

fig.add_annotation(
    text=f"<span style='font-size:36px; color:{circle_color}'>{score:.1f}</span><br><span style='font-size:18px;'>/10</span>",
    x=0.5, y=0.5, showarrow=False
)

fig.update_layout(
    showlegend=False,
    margin=dict(t=0, b=0, l=0, r=0),
    paper_bgcolor="#f7f9fb",
    plot_bgcolor="#f7f9fb",
    height=300
)

st.plotly_chart(fig, use_container_width=True)

# --- INTERPRÉTATION DU SCORE ---
if score >= 8:
    st.success("Dossier très favorable : excellente solidité et forte rentabilité.")
elif score >= 6:
    st.warning("Dossier intéressant : nécessite une validation approfondie.")
else:
    st.error("Dossier à risque : plusieurs indicateurs faibles.")

st.markdown("---")

# --- VALIDATION HUMAINE ---
st.header("3. Validation par l’analyste")
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

st.markdown("---")
st.caption("© 2025 BO Score — IA d’aide à la décision. Tous droits réservés.")
