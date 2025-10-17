import streamlit as st

st.set_page_config(page_title="Score IA - Eurinvest Connect", layout="centered")

st.title("📊 Évaluation automatique d’un dossier d’investissement")
st.markdown("### Outil d’aide à la décision (IA + validation humaine)")

st.divider()

st.header("1️⃣ Informations du dossier")

col1, col2 = st.columns(2)
with col1:
    solidite = st.slider("Solidité financière", 0, 10, 5)
    experience = st.slider("Expérience de l’équipe dirigeante", 0, 10, 5)
    rentabilite = st.slider("Rentabilité estimée du projet", 0, 10, 5)
with col2:
    risque = st.slider("Risque sectoriel", 0, 10, 5)
    alignement = st.slider("Alignement stratégique avec le fonds", 0, 10, 5)

st.divider()

st.header("2️⃣ Résultat du scoring")

score = (
    solidite * 0.3
    + rentabilite * 0.25
    + experience * 0.2
    + (10 - risque) * 0.15
    + alignement * 0.1
)

st.metric("Score global", f"{score:.1f} / 10")

if score >= 8:
    st.success("✅ Dossier très favorable : excellente solidité et forte rentabilité.")
elif score >= 6:
    st.warning("⚠️ Dossier intéressant : nécessite une validation approfondie sur certains aspects.")
else:
    st.error("❌ Dossier à risque : plusieurs indicateurs financiers sont faibles.")

st.divider()

st.header("3️⃣ Validation humaine obligatoire")
validation = st.radio(
    "Décision de l'analyste :",
    ("En attente", "Valider le dossier", "Rejeter le dossier"),
    index=0,
)

commentaire = st.text_area("Commentaires de l'analyste (facultatif)")

if validation != "En attente":
    st.success(f"Décision enregistrée : **{validation}** ✅")
    if commentaire:
        st.info(f"🗒️ Commentaire : {commentaire}")

st.divider()
st.caption("💡 L’IA assiste la décision, mais la validation finale reste humaine.")
