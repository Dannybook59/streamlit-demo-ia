import streamlit as st
import plotly.graph_objects as go
import random

# =========================
# CONFIG & THEME (violet clair)
# =========================
st.set_page_config(page_title="BO Score", layout="wide")

st.markdown("""
<style>
    .stApp{background:#EFEAFB; color:#2b2b2b; font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;}
    h1,h2,h3{color:#4B3C8A; font-weight:600;}
    .card{
        background:#FFFFFF;
        border:1px solid #DCCEF7;
        border-radius:16px;
        padding:16px 18px;
        box-shadow:0 4px 14px rgba(75,60,138,.08);
    }
    .section{font-size:1.05rem; font-weight:600; color:#5A4CA1; margin:0 0 10px 0;}
    .muted{color:#616161; font-size:.92rem;}
    hr{border:none; border-top:1px solid #DCCEF7; margin:12px 0;}
</style>
""", unsafe_allow_html=True)

st.markdown("## BO Score — Évaluation IA des dossiers d’investissement")

# =========================
# FAKE CLIENT (au chargement)
# =========================
clients = [
    {"nom":"GreenHydro SAS","secteur":"Énergies renouvelables","montant":"2,4 M€","pays":"France","analyste":"A. Morel"},
    {"nom":"NeoTech Ventures","secteur":"Technologies médicales","montant":"1,8 M€","pays":"Suisse","analyste":"M. El Amrani"},
    {"nom":"BlueWave Capital","secteur":"Finance durable","montant":"3,6 M€","pays":"Belgique","analyste":"L. Dupont"},
    {"nom":"AgriNova Ltd","secteur":"AgriTech","montant":"1,2 M€","pays":"Pays-Bas","analyste":"C. Bernard"},
]
client = random.choice(clients)

# =========================
# LAYOUT RADIAL (3 x 3)
# =========================
# Ligne 1 : TL (fiche) | centre vide | TR (indicateurs)
r1c1, r1c2, r1c3 = st.columns([1,1,1])
# Ligne 2 : (vide) | CENTRE (score) | (vide)
r2c1, r2c2, r2c3 = st.columns([1,1,1])
# Ligne 3 : BL (sliders) | centre vide | BR (validation)
r3c1, r3c2, r3c3 = st.columns([1,1,1])

# --------- Top-Left : FICHE CLIENT ---------
with r1c1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section'>Dossier client</div>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class='muted'>
        <b>Entreprise :</b> {client['nom']}<br>
        <b>Secteur :</b> {client['secteur']}<br>
        <b>Montant demandé :</b> {client['montant']}<br>
        <b>Pays :</b> {client['pays']}<br>
        <b>Analyste référent :</b> {client['analyste']}
        </div>
        """, unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

# --------- Bottom-Left : CRITÈRES (sliders / interactif) ---------
with r3c1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section'>Évaluation des critères</div>", unsafe_allow_html=True)
    solidite    = st.slider("Solidité financière",             0, 10, 6)
    experience  = st.slider("Expérience de l’équipe dirigeante",0, 10, 7)
    rentabilite = st.slider("Rentabilité estimée du projet",    0, 10, 5)
    risque      = st.slider("Risque sectoriel",                 0, 10, 4)
    alignement  = st.slider("Alignement stratégique",           0, 10, 6)
    st.markdown("</div>", unsafe_allow_html=True)

# --------- SCORE (calcul commun) ---------
score = (
    solidite * 0.30
    + rentabilite * 0.25
    + experience * 0.20
    + (10 - risque) * 0.15
    + alignement * 0.10
)

def score_color(val: float) -> str:
    if val < 5:   return "#E63946"  # rouge doux
    if val < 8:   return "#F4A261"  # jaune chaud
    return "#2A9D8F"                # vert doux

# --------- Centre : CERCLE DE SCORE ---------
with r2c2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section'>Score global</div>", unsafe_allow_html=True)

    color = score_color(score)
    fig = go.Figure(go.Pie(
        values=[score, 10 - score],
        hole=0.72,
        marker_colors=[color, "#EFEAFB"],
        textinfo="none"
    ))
    fig.add_annotation(
        text=f"<span style='font-size:40px; color:{color}'>{score:.1f}</span><br><span style='font-size:16px; color:#666'>/10</span>",
        x=0.5, y=0.5, showarrow=False
    )
    fig.update_layout(
        showlegend=False,
        margin=dict(t=0,b=0,l=0,r=0),
        paper_bgcolor="#FFFFFF",
        height=320,
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --------- Top-Right : INDICATEURS COMPLÉMENTAIRES ---------
with r1c3:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section'>Indicateurs complémentaires</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Potentiel rendement", f"{round(rentabilite * 1.2, 1)} %")
    c2.metric("Risque ajusté",       f"{round((10 - risque) * 10, 1)} / 100")
    c3.metric("Maturité projet",     f"{round(experience * 10, 1)} / 100")
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='muted'>Poids critères — Solidité 30%, Rentabilité 25%, Expérience 20%, "
        f"Risque 15% (inversé), Alignement 10%.</div>", unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

# --------- Bottom-Right : VALIDATION + SYNTHÈSE ---------
with r3c3:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section'>Validation par l’analyste</div>", unsafe_allow_html=True)
    decision = st.radio("Décision finale :", ["En attente","Valider le dossier","Rejeter le dossier"], horizontal=True)
    commentaire = st.text_area("Commentaires / réserves")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='section'>Résumé décisionnel</div>", unsafe_allow_html=True)

    if decision == "Valider le dossier":
        synthese = f"Score {score:.1f}/10 : profil favorable. Indicateurs solides ; validation recommandée."
        tone = "success"
    elif decision == "Rejeter le dossier":
        synthese = f"Score {score:.1f}/10 : profil insuffisant au regard du risque/rentabilité ; validation non conseillée."
        tone = "error"
    else:
        synthese = f"Score {score:.1f}/10 : décision en attente d’éléments complémentaires."
        tone = "warning"

    getattr(st, tone)(synthese)
    if commentaire:
        st.info(f"Commentaire : {commentaire}")
    st.markdown("</div>", unsafe_allow_html=True)

# --------- Footer ---------
st.caption("© 2025 BO Score — IA d’aide à la décision. Thème violet clair, layout radial.")
