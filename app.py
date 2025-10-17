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
        .metric-box {
            background-color: rgba(255,255,255,0.08);
            border-radius: 12px;
            padding: 0.8rem;
            text-align: center;
            font-size: 1.1rem;
        }
    </style>
""", unsafe_allow_html=True)

# --- EN-TÊTE ---
st.title("📊 BO Score")
st.markdown("### IA d’analyse et de notation des dossiers d’investissement")
st.markdown("---")

# --- GÉNÉRATION ALÉATOIRE DE CLIENT FACTICE ---
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
    rentabilite = st.slider("Rentabilité estimée du




