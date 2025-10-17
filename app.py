import streamlit as st
import plotly.graph_objects as go
import random

# =========================
# CONFIG & STYLE
# =========================
st.set_page_config(page_title="CriteriA", layout="wide")

# --- LOGO CRITERIA ---
st.markdown(
    """
    <style>
        .criteria-logo {
            font-family: 'Segoe UI', sans-serif;
            font-weight: 700;
            font-size: 3rem;
            text-align: center;
            margin-top: -0.5rem;
            margin-bottom: 0.5rem;
            color: #3D2C8D;
        }
        .criteria-logo span {
            color: #7A5AF8; /* Violet plus clair pour le IA */
        }
        .criteria-tagline {
            text-align: center;
            font-size: 1.1rem;
            color: #7A5AF8;
            margin-top: -0.5rem;
            margin-bottom: 1rem;
            font-weight: 400;
        }
    </style>

    <h1 class='criteria-logo'>Criteri<span>IA</span></h1>
    <div class='criteria-tagline'>Analyse intelligente des dossiers d’investissement</div>
    <hr style='border-top: 1px solid #C7B8F5; margin-top:0.2rem'>
    """,
    unsafe_allow_html=True
)

# --- COULEURS & CSS GLOBAL ---
st.markdown("""
<style>
    :root {
        --main-color: #3D2C8D;
        --light-bg: #FFFFFF;
    }
    html, body, .stApp {
        background-color: var(--light-bg);
        color: var(--main-color);
        font-family: 'Segoe UI', sans-serif;
        overflow: hidden !important;
        height: 100vh !important;
    }
    h1, h2, h3, h4, h5, h6, label, p, div, span, .stMarkdown, .stText, .stSelectbox, .stRadio, .stMetric {
        color: var(--main-color) !important;
    }
    .comment-box, .radio-group {
        border: 2px solid #C7B8F5;
        border-radius: 8px;
        background-color: var(--light-bg);
        padding: 0.8rem;
    }
    textarea {
        background-color: var(--light-bg) !important;
        color: var(--main-color) !important;
        border: 1px solid #C7B8F5 !important;
        border-radius: 6px !important;
    }
    hr {
        border: none;
        border-top: 1px solid #C7B8F5;
        margin: 0.8rem 0;
    }
    .section {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--main-color);
        margin-top: 0.8rem;
        margin-bottom: 0.5rem;
    }
    button[data-baseweb="tab"] {
        color: var(--main-color) !important;
        font-weight: 600 !important;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        height: 90vh;
        overflow: hidden !important;
    }
</style>
""", unsafe_allow_html=True)

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
# ONGLET NAVIGATION
# =========================
tab_dashboard, tab_dossier = st.tabs(["Tableau de bord", "Dossier entreprise"])

# =========================
# 1️⃣ TABLEAU DE BORD
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
        if val < 50: return "#E63946"
        elif val < 80: return "#F4A261"
        else: return "#2A9D8F"

    # --- SCORE CENTRAL ---
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
        fig.update_layout(showlegend=False, margin=dict(t=0,b=0,l=0,r=0), paper_bgcolor="#FFFFFF", height=320)
        st.plotly_chart(fig, use_container_width=True)

    # --- INDICATEURS + COMMENTAIRE SCORE ---
    with col3:
        st.markdown("<div class='section'>Indicateurs complémentaires</div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.metric("Rendement", f"{round(rentabilite * 1.2, 1)} %")
        c2.metric("Risque ajusté", f"{round((10 - risque) * 10, 1)} / 100")
        c3.metric("Maturité", f"{round(experience * 10, 1)} / 100")

        # Résumé du score directement sous les indicateurs (avec vraies couleurs)
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
            f"""
            <div style="{style} padding:10px 15px; border-radius:6px; margin-top:15px;
                        font-weight:700; font-size:1.05rem;">
                {message}
            </div>
            """,
            unsafe_allow_html=True
        )

    # --- VALIDATION ET COMMENTAIRE (ronds à droite) ---
    st.markdown("<hr>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1.3, 1.2, 1.5])

    with col1:
        st.markdown("<div class='section'>Synthèse du dossier</div>", unsafe_allow_html=True)
        st.write("""
        Vérifiez les critères principaux et les indicateurs avant de formuler
        une décision finale. Utilisez les curseurs pour ajuster les valeurs si
        nécessaire, puis validez votre recommandation dans la colonne de droite.
        """)

    with col3:
        st.markdown("<div class='section'>Décision finale</div>", unsafe_allow_html=True)
        st.markdown("<div class='radio-group'>", unsafe_allow_html=True)
        decision = st.radio(
            "Choisir une option :",
            ["En attente", "Valider le dossier", "Rejeter le dossier"],
            horizontal=True
        )
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='section' style='margin-top:10px;'>Commentaires</div>", unsafe_allow_html=True)
        st.markdown("<div class='comment-box'>", unsafe_allow_html=True)
        commentaire = st.text_area("Commentaires / observations", height=90, label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)

# =========================
# 2️⃣ ONGLET DOSSIER ENTREPRISE (exemple NeoTech)
# =========================
with tab_dossier:
    st.markdown("## Dossier complet — NeoTech Ventures")

    st.markdown("""
    **Présentation de l’entreprise :**  
    NeoTech Ventures est une société suisse spécialisée dans le développement de dispositifs médicaux connectés et de solutions d’analyse de données de santé basées sur l’intelligence artificielle.  
    Fondée en 2019 à Lausanne, elle accompagne les hôpitaux et laboratoires pharmaceutiques dans la digitalisation du suivi patient et l’optimisation des diagnostics.

    L’entreprise a récemment finalisé un prototype de capteur biométrique portable, capable de suivre en temps réel les paramètres vitaux et d’envoyer des alertes prédictives en cas d’anomalie.  
    Le projet vise une mise sur le marché en Europe courant 2026.
    """)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### Objectifs du financement :")
    st.markdown("""
    - Finaliser la certification CE du dispositif médical (classe IIb)  
    - Industrialiser la production (sous-traitance prévue en Allemagne)  
    - Étendre les équipes R&D et Data Science  
    - Lancer la phase pilote dans 5 hôpitaux partenaires européens  
    - Renforcer le département conformité RGPD et cybersécurité
    """)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### Indicateurs clés :")
    st.markdown("""
    - **Chiffre d’affaires prévisionnel 2026 :** 8,2 M€  
    - **Croissance annuelle moyenne prévue :** +42 %  
    - **Marge brute projetée :** 63 %  
    - **Taux de rétention client attendu :** 85 %  
    - **Nombre d’hôpitaux partenaires :** 12 à fin 2026  
    """)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### Équipe dirigeante :")
    st.markdown("""
    - **Sophie Lemoine — CEO :** 12 ans d’expérience en medtech et ex-responsable innovation chez Philips Healthcare.  
    - **Dr. Marc Keller — CTO :** docteur en biophysique, spécialiste en IA médicale et traitement du signal.  
    - **Anna Weber — CFO :** ancienne consultante EY, experte en financement early stage et conformité ISO 13485.  
    """)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### Documents disponibles :")
    st.markdown("""
    - Business Plan 2025–2028 — projections financières et stratégie de croissance  
    - Étude de marché — tendances du monitoring médical connecté en Europe  
    - Rapport technique — architecture du capteur NeoSense et conformité médicale  
    - Pitch Deck — présentation investisseurs  
    - Contrats de partenariat — CHUV Lausanne, Charité Berlin, Hôpital Européen de Marseille  
    """)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### Informations administratives :")
    st.markdown("""
    **Pays :** Suisse 🇨🇭  
    **Secteur d’activité :** Technologies médicales / IA Santé  
    **Montant demandé :** 1,8 M€  
    **Analyste en charge :** M. El Amrani  
    **Statut juridique :** SA – capital social 2,5 M CHF  
    **Date de création :** 2019  
    **Siège social :** EPFL Innovation Park, Lausanne  
    """)
