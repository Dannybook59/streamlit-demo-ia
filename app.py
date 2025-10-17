import streamlit as st
import plotly.graph_objects as go
import random

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="BO Score - IA Scoring",
    page_icon="📊",
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
        .client-box {
            background-color: rgba(255,255,255,0.05);
            border-radius: 15px;
            padding: 1rem 2rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }
    </style>
""", unsafe_allow_html=True)

# --- EN-TÊTE ---
st.title("📊 BO Score")
st.markdown("### IA d’analyse et de notation des dossiers d’investissement")
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
st.subheader("📁 Dossier client")
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
st.header("1️⃣ Évaluation des critères")

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
st.header("2️⃣ Résultat du scoring BO")

score = (
    solidite * 0.3
    + rentabilite * 0.25
    + experience * 0.2
    + (10 - risque) * 0.15
    + alignement * 0.1
)

# --- COULEUR DU CERCLE SELON LE SCORE ---
if score < 5:
    circle_color = "#ef476f"  # Rouge
elif score < 8:
    circle_color = "#ffd166"  # Jaune
else:
    circle_color = "#06d6a0"  # Vert

# --- VISUEL : CERCLE PLEIN DU SCORE ---
fig = go.Figure(go.Pie(
    values=[score, 10 - score],
    hole=0.7,
    marker_colors=[circle_color, "rgba(255,255,255,0.08)"],
    textinfo="none"
))

fig.add_annotation(
    text=f"<b>{score:.1f}</b><br>/10",
    x=0.5, y=0.5,
    font=dict(size=40, color=circle_color),
    showarrow=False
)

fig.update_layout(
    showlegend=False,
    margin=dict(t=0, b=0, l=0, r=0),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    height=320
)

st.plotly_chart(fig, use_container_width=True)

# --- INTERPRÉTATION DU SCORE ---
if score >= 8:
    st.success("✅ Dossier **très favorable** : excellente solidité et forte rentabilité.")
elif score >= 6:
    st.warning("⚠️ Dossier **intéressant** : nécessite une validation approfondie.")
else:
    st.error("❌ Dossier **à risque** : plusieurs indicateurs financiers sont faibles.")

st.markdown("---")

# --- VALIDATION HUMAINE ---
st.header("3️⃣ Validation par l’analyste")
validation = st.radio(
    "Décision finale :",
    ["En attente", "Valider le dossier", "Rejeter le dossier"],
    horizontal=True
)

commentaire = st.text_area("Commentaires ou observations")

if validation != "En attente":
    st.success(f"✅ Décision enregistrée : **{validation}**")
    if commentaire:
        st.info(f"💬 Commentaire : {commentaire}")

st.markdown("---")
st.caption("© 2025 BO Score — IA d’aide à la décision. RGPD & AMF compliant.")
