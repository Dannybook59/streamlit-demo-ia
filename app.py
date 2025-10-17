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
        overflow: hidden !important;
        height: 100vh !important;
    }
    h1, h2, h3, label, .stMarkdown, p, div, span {
        color: #3D2C8D !important;
    }
    h1#bo-score {
        text-align: center;
        color: #3D2C8D;
        font-size: 3rem;
        margin-bottom: 0.5rem;
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
        margin: 0.8rem 0;
    }
    .comment-box {
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
# LAYOUT
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

# --- SCORE CENTRAL AVEC COMPTEUR FLUIDE ---
with r2c2:
    color = score_color(score_100)
    placeholder = st.empty()

    steps = max(5, int(score_100 // 2))
    for val in range(0, int(score_100) + 1, steps):
        fig = go.Figure(go.Pie(
            values=[val, 100 - val],
            hole=0.8,
            marker_colors=[score_color(val), "#EFEAFB"],
            textinfo="none",
            sort=False,
            direction="clockwise"
        ))
        fig.add_annotation(
            text=f"<span style='font-size:70px; color:{score_color(val)}; font-weight:700'>{val}</span>",
            x=0.5, y=0.5, showarrow=False
        )
        fig.update_layout(showlegend=False, margin=dict(t=0,b=0,l=0,r=0), paper_bgcolor="#FFFFFF", height=340)
        placeholder.plotly_chart(fig, use_container_width=True)
        time.sleep(0.02)

# --- AJOUT 1 : SYNTHÈSE IA ---
with r2c2:
    if score_100 >= 80:
        resume = "Projet robuste avec excellente rentabilité et faible risque. Opportunité recommandée."
    elif score_100 >= 50:
        resume = "Projet prometteur, mais nécessite une vérification du risque et de la rentabilité."
    else:
        resume = "Risque élevé et rentabilité incertaine. Prudence conseillée avant validation."
    st.info(f"📋 Synthèse IA : {resume}")

# --- AJOUT 2 : RADAR CHART ---
with r2c1:
    radar_fig = go.Figure()
    radar_fig.add_trace(go.Scatterpolar(
        r=[solidite, experience, rentabilite, 10 - risque, alignement],
        theta=["Solidité", "Expérience", "Rentabilité", "Risque", "Alignement"],
        fill='toself',
        fillcolor="rgba(61,44,141,0.25)",
        line_color="#3D2C8D"
    ))
    radar_fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0,10])),
        showlegend=False,
        paper_bgcolor="#FFFFFF",
        margin=dict(t=0,b=0,l=0,r=0),
        height=320
    )
    st.plotly_chart(radar_fig, use_container_width=True)

# --- AJOUT 3 : RISQUES DÉTECTÉS ---
with r2c3:
    risques = []
    if risque > 7: risques.append("Risque sectoriel élevé")
    if rentabilite < 5: risques.append("Rentabilité faible")
    if alignement < 5: risques.append("Alignement stratégique insuffisant")
    if solidite < 4: risques.append("Solidité financière limitée")

    if risques:
        st.warning("⚠️ Risques détectés : " + ", ".join(risques))
    else:
        st.success("Aucun risque majeur détecté ✅")

# --- INDICATEURS COMPLÉMENTAIRES ---
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
    commentaire = st.text_area("Commentaires / observations", height=100, label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)

    # --- RECOMMANDATION SELON SCORE ---
    if score_100 >= 80:
        synthese = f"Score {score_100:.0f} : excellent dossier. Validation recommandée ✅"
        tone = "success"
    elif 50 <= score_100 < 80:
        synthese = f"Score {score_100:.0f} : dossier prometteur, à vérifier ⚠️"
        tone = "warning"
    else:
        synthese = f"Score {score_100:.0f} : dossier à risque élevé. Validation non conseillée ❌"
        tone = "error"

    getattr(st, tone)(synthese)
    if commentaire:
        st.info(f"Commentaire : {commentaire}")

st.caption("© 2025 BO Score — IA d’aide à la décision enrichie (Radar + Synthèse + Risques).")
