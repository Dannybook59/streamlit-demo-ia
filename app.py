import streamlit as st
import plotly.graph_objects as go
import random

# =========================
# CONFIG & STYLE
# =========================
st.set_page_config(page_title="BO Score", layout="wide")

st.markdown("""
<style>
  .stApp { background:#FFFFFF; color:#3D2C8D; font-family:'Segoe UI',system-ui,sans-serif; }
  h1#bo-score { text-align:center; color:#3D2C8D; font-size:3rem; margin:0.2rem 0 0.6rem; font-weight:700; }
  .section { font-size:1.05rem; font-weight:600; color:#3D2C8D; margin-bottom:0.4rem; }
  .card { border:2px solid #C7B8F5; border-radius:10px; background:#FFF; padding:0.9rem 1rem; }
  .radio-box { border:2px solid #C7B8F5; border-radius:10px; background:#FFF; padding:0.6rem 0.9rem; }
  .comment-box { border:2px solid #C7B8F5; border-radius:10px; background:#FFF; padding:0.6rem 0.9rem; }
  textarea { background:#FFF !important; color:#3D2C8D !important; border:1px solid #C7B8F5 !important; border-radius:6px !important; }
  .metrics .metric-label { color:#3D2C8D !important; }
  hr { border:none; border-top:1px solid #E6E0FB; margin:0.6rem 0 1rem; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 id='bo-score'>BO Score</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# =========================
# DONNÉES CLIENT FACTICES
# =========================
clients = [
    {"nom":"GreenHydro SAS","secteur":"Énergies renouvelables","montant":"2,4 M€","pays":"France","analyste":"A. Morel"},
    {"nom":"NeoTech Ventures","secteur":"Technologies médicales","montant":"1,8 M€","pays":"Suisse","analyste":"M. El Amrani"},
    {"nom":"BlueWave Capital","secteur":"Finance durable","montant":"3,6 M€","pays":"Belgique","analyste":"L. Dupont"},
    {"nom":"AgriNova Ltd","secteur":"AgriTech","montant":"1,2 M€","pays":"Pays-Bas","analyste":"C. Bernard"},
]
client = random.choice(clients)

# =========================
# LAYOUT (tout tient sur l'écran)
# =========================
left, center, right = st.columns([1.2, 1, 1.2])

# --- FICHE CLIENT (gauche) ---
with left:
    st.markdown("<div class='section'>Dossier client</div>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class='card'>
          <b>Entreprise :</b> {client['nom']}<br>
          <b>Secteur :</b> {client['secteur']}<br>
          <b>Montant demandé :</b> {client['montant']}<br>
          <b>Pays :</b> {client['pays']}<br>
          <b>Analyste référent :</b> {client['analyste']}
        </div>
        """,
        unsafe_allow_html=True
    )

# Sliders dans un expander pour éviter le scroll
with left.expander("Ajuster les critères (ouvrir pour modifier)"):
    solidite    = st.slider("Solidité financière", 0, 10, 6)
    experience  = st.slider("Expérience de l’équipe dirigeante", 0, 10, 7)
    rentabilite = st.slider("Rentabilité estimée du projet", 0, 10, 5)
    risque      = st.slider("Risque sectoriel", 0, 10, 4)
    alignement  = st.slider("Alignement stratégique", 0, 10, 6)

# Valeurs par défaut si l'expander reste fermé (garde l'état précédent si ouvert)
if "solidite" not in locals():
    solidite, experience, rentabilite, risque, alignement = 6, 7, 5, 4, 6

# --- Calcul score ---
score_10 = (
    solidite * 0.30
    + rentabilite * 0.25
    + experience * 0.20
    + (10 - risque) * 0.15
    + alignement * 0.10
)
score_100 = round(score_10 * 10, 1)

def score_color(v):
    if v < 50:  return "#E63946"  # rouge
    if v < 80:  return "#F4A261"  # orange/jaune
    return "#2A9D8F"              # vert

# --- CERCLE SCORE (centre) ---
with center:
    color = score_color(score_100)
    fig = go.Figure(go.Pie(
        values=[score_100, 100 - score_100],
        hole=0.80,
        marker_colors=[color, "#EFEAFB"],
        textinfo="none",
        sort=False,
        direction="clockwise"
    ))
    fig.add_annotation(
        text=f"<span style='font-size:70px; color:{color}; font-weight:700'>{int(score_100)}</span>",
        x=0.5, y=0.5, showarrow=False
    )
    fig.update_layout(showlegend=False, margin=dict(t=0,b=0,l=0,r=0), paper_bgcolor="#FFFFFF", height=330)
    st.plotly_chart(fig, use_container_width=True)

# --- INDICATEURS (droite) ---
with right:
    st.markdown("<div class='section'>Indicateurs complémentaires</div>", unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    m1.metric("Rendement", f"{round(rentabilite*1.2,1)} %")
    m2.metric("Risque ajusté", f"{round((10-risque)*10,1)} / 100")
    m3.metric("Maturité", f"{round(experience*10,1)} / 100")

# =========================
# VALIDATION & COMMENTAIRE (pleine largeur)
# =========================
st.markdown("<hr>", unsafe_allow_html=True)
c1, c2 = st.columns([1, 2])

with c1:
    st.markdown("<div class='section'>Décision</div>", unsafe_allow_html=True)
    st.markdown("<div class='radio-box'>", unsafe_allow_html=True)
    decision = st.radio("Décision finale :", ["En attente", "Valider le dossier", "Rejeter le dossier"], horizontal=True)
    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown("<div class='section'>Commentaires</div>", unsafe_allow_html=True)
    st.markdown("<div class='comment-box'>", unsafe_allow_html=True)
    commentaire = st.text_area("Commentaires / observations", height=100, label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)

# Recommandation logique selon le score
if score_100 >= 80:
    synthese = f"Score {int(score_100)} : excellent dossier. Validation recommandée ✅"
    st.success(synthese)
elif score_100 >= 50:
    synthese = f"Score {int(score_100)} : dossier prometteur, vérifications complémentaires conseillées ⚠️"
    st.warning(synthese)
else:
    synthese = f"Score {int(score_100)} : dossier à risque élevé. Validation non conseillée ❌"
    st.error(synthese)

if commentaire:
    st.info(f"Commentaire : {commentaire}")

st.caption("© 2025 BO Score — Interface stable, fond blanc & texte violet foncé.")


