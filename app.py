import streamlit as st
import plotly.graph_objects as go
import random

# =========================
# CONFIG & STYLE
# =========================
st.set_page_config(page_title="BO Score", layout="wide")

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
    /* TITRE */
    h1#bo-score {
        text-align: center;
        color: var(--main-color);
        font-size: 3rem;
        margin-bottom: 0.5rem;
        margin-top: -0.5rem;
        font-weight: 700;
    }
    /* TEXTES GLOBAUX */
    h1, h2, h3, h4, h5, h6, label, p, div, span, .stMarkdown, .stText, .stSelectbox, .stRadio, .stMetric {
        color: var(--main-color) !important;
    }
    /* SLIDERS */
    .stSlider label, .stSlider span {
        color: var(--main-color) !important;
    }
    /* RADIO & COMMENTAIRES */
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
    /* LIGNES & SECTION TITRES */
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
    /* TABS */
    button[data-baseweb="tab"] {
        color: var(--main-color) !important;
        font-weight: 600 !important;
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
# ONGLET NAVIGATION EN HAUT
# =========================
tab_dashboard, tab_dossier = st.tabs(["Tableau de bord", "Dossier entreprise"])

# =========================
# 1️⃣ ONGLET : TABLEAU DE BORD
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
        if val < 50:
            return "#E63946"
        elif val < 80:
            return "#F4A261"
        else:
            return "#2A9D8F"

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

    # --- SYNTHÈSE SCORE ---
    if score_100 >= 80:
        st.success(f"Score {score_100:.0f} — Dossier solide, validation recommandée.")
    elif score_100 >= 50:
        st.warning(f"Score {score_100:.0f} — Dossier intéressant, à vérifier.")
    else:
        st.error(f"Score {score_100:.0f} — Risque élevé, validation non conseillée.")
    if commentaire:
        st.info(f"Commentaire : {commentaire}")

# =========================
# 2️⃣ ONGLET : DOSSIER ENTREPRISE
# =========================
with tab_dossier:
    st.markdown(f"## Dossier complet — {client['nom']}")
    st.write("""
    **Présentation de l’entreprise :**  
    GreenHydro SAS développe des infrastructures de production d’hydrogène vert destinées aux
    industries lourdes et au transport. L’objectif est de réduire les émissions carbone tout en
    optimisant les coûts de production énergétique.
    """)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### Documents disponibles :")
    st.markdown("""
    - Pitch Deck — Présentation du projet  
    - Business Plan 2025 — Projection financière  
    - Étude de marché — Potentiel européen de l’hydrogène  
    - Équipe & bios — CV et expertise de l’équipe dirigeante  
    - Projections financières — Données prévisionnelles 2025–2027  
    - Checklist due diligence — Documents juridiques et conformité  
    """)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### Informations administratives :")
    st.markdown(f"""
    **Pays :** {client['pays']}  
    **Secteur d’activité :** {client['secteur']}  
    **Montant demandé :** {client['montant']}  
    **Analyste en charge :** {client['analyste']}
    """)

st.caption("© 2025 BO Score — Interface professionnelle et cohérente.")
