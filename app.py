import streamlit as st
import plotly.graph_objects as go
import random
import time

# =========================
# CONFIG & STYLE
# =========================
st.set_page_config(page_title="BO Score", layout="wide")

st.markdown("""
<style>
    html, body, .stApp {
        background-color: #FFFFFF;
        color: #3D2C8D;
        font-family: 'Segoe UI', sans-serif;
        height: 100vh !important;
    }
    h1#bo-score {
        text-align: center;
        color: #3D2C8D;
        font-size: 3rem;
        margin-top: -0.5rem;
        margin-bottom: 0.3rem;
        font-weight: 700;
    }
    .section {
        font-size: 1.1rem;
        font-weight: 600;
        color: #3D2C8D;
        margin-top: 0.8rem;
        margin-bottom: 0.5rem;
    }
    hr { border: none; border-top: 1px solid #C7B8F5; margin: 0.8rem 0; }
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
</style>
""", unsafe_allow_html=True)

# --- TITRE ---
st.markdown("<h1 id='bo-score'>BO Score</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# =========================
# DONNÉES FACTICES ENTREPRISE
# =========================
clients = [
    {"nom": "GreenHydro SAS", "secteur": "Énergies renouvelables", "montant": "2,4 M€", "pays": "France", "analyste": "A. Morel",
     "description": "GreenHydro SAS développe des infrastructures de production d’hydrogène vert. L’entreprise vise à décarboner le transport industriel en Europe.",
     "docs": ["Présentation corporate.pdf", "Business Plan 2025.xlsx", "Étude de marché Hydrogène.pdf"]},
    {"nom": "NeoTech Ventures", "secteur": "Technologies médicales", "montant": "1,8 M€", "pays": "Suisse", "analyste": "M. El Amrani",
     "description": "NeoTech conçoit des dispositifs médicaux connectés pour la télésurveillance de patients chroniques. Objectif : réduire les coûts hospitaliers.",
     "docs": ["Pitch Deck NeoTech.pdf", "Prévisionnel financier.xlsx", "Rapport clinique.pdf"]},
    {"nom": "BlueWave Capital", "secteur": "Finance durable", "montant": "3,6 M€", "pays": "Belgique", "analyste": "L. Dupont",
     "description": "BlueWave Capital investit dans des projets à impact environnemental positif. Fonds labellisé ISR et GreenFin.",
     "docs": ["Présentation fonds ISR.pdf", "Portefeuille 2024.xlsx", "Charte ESG.pdf"]}
]
client = random.choice(clients)

# =========================
# NAVIGATION ENTRE LES ONGLETS
# =========================
tab_dashboard, tab_dossier = st.tabs(["📊 Tableau de bord IA", "📁 Dossier entreprise"])

# =========================
# 1️⃣ ONGLET TABLEAU DE BORD
# =========================
with tab_dashboard:
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
            """,
            unsafe_allow_html=True
        )

        st.markdown("<hr>", unsafe_allow_html=True)
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

    def score_color(val):
        if val < 50: return "#E63946"
        elif val < 80: return "#F4A261"
        else: return "#2A9D8F"

    with col2:
        color = score_color(score_100)
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
        fig.update_layout(showlegend=False, margin=dict(t=0,b=0,l=0,r=0), paper_bgcolor="#FFFFFF", height=340)
        st.plotly_chart(fig, use_container_width=True)

    # --- INDICATEURS ---
    with col3:
        st.markdown("<div class='section'>Indicateurs complémentaires</div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.metric("Rendement", f"{round(rentabilite * 1.2, 1)} %")
        c2.metric("Risque ajusté", f"{round((10 - risque) * 10, 1)} / 100")
        c3.metric("Maturité", f"{round(experience * 10, 1)} / 100")

    # --- VALIDATION ---
    st.markdown("<hr>", unsafe_allow_html=True)
    c1, c2 = st.columns([1, 2])

    with c1:
        st.markdown("<div class='section'>Décision</div>", unsafe_allow_html=True)
        st.markdown("<div class='radio-group'>", unsafe_allow_html=True)
        decision = st.radio("Décision finale :", ["En attente", "Valider le dossier", "Rejeter le dossier"], horizontal=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='section'>Commentaires</div>", unsafe_allow_html=True)
        st.markdown("<div class='comment-box'>", unsafe_allow_html=True)
        commentaire = st.text_area("Commentaires / observations", height=100, label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)

    # Synthèse finale
    if score_100 >= 80:
        st.success(f"✅ Score {score_100:.0f} — Dossier solide, validation recommandée.")
    elif score_100 >= 50:
        st.warning(f"⚠️ Score {score_100:.0f} — Dossier intéressant, à vérifier.")
    else:
        st.error(f"❌ Score {score_100:.0f} — Risque élevé, validation non conseillée.")
    if commentaire:
        st.info(f"💬 Commentaire : {commentaire}")

# =========================
# 2️⃣ ONGLET DOSSIER ENTREPRISE
# =========================
with tab_dossier:
    st.markdown(f"## 📁 Dossier complet — {client['nom']}")
    st.write(client["description"])

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### 📄 Documents disponibles :")
    for doc in client["docs"]:
        st.markdown(f"- {doc}")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### 🧾 Informations administratives :")
    st.markdown(f"""
    **Pays :** {client['pays']}  
    **Secteur d’activité :** {client['secteur']}  
    **Montant demandé :** {client['montant']}  
    **Analyste en charge :** {client['analyste']}
    """)
