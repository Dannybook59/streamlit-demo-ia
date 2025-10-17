import streamlit as st
import plotly.graph_objects as go
import random

# --- CONFIGURATION ---
st.set_page_config(page_title="BO Score", layout="wide")

# --- STYLE GLOBAL ---
st.markdown("""
    <style>
        .stApp {
            background-color: #f7f5fb;
            color: #2d2a32;
            font-family: 'Segoe UI', sans-serif;
        }
        h1, h2, h3 {
            font-weight: 500;
            color: #4b3c8a;
        }
        .section-title {
            font-size: 1.1rem;
            font-weight: 600;
            color: #5e4fa2;
            margin-top: 1.5rem;
            margin-bottom: 0.5rem;
        }
        .client-box, .score-box, .summary-box {
            background-color: #ffffff;
            border-radius: 12px;
            padding: 1rem 1.5rem;
            border: 1px solid #e2def0;
            box-shadow: 0 2px 6px rgba(75, 60, 138, 0.05);
            margin-bottom: 1.5rem;
        }
        .metric-label {
            color: #6a637a;
            font-size: 0.9rem;
        }
        .metric-value {
            font-weight: 600;
            font-size: 1.1rem;
            color: #4b3c8a;
        }
        .stSlider label, .stRadio label {
            color: #2d2a32 !important;
            font-weight: 400 !important;
        }
        textarea {
            border-radius: 8px !important;
        }
        hr {
            border: none;
            border-top: 1px solid #e1dcf3;
            margin: 1rem 0;
        }
    </style>
""", unsafe_allow_html=True)

# --- EN-TÊTE ---
st.markdown("<h2>BO Score — Évaluation IA des dossiers d’investissement</h2>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# --- CLIENTS FACTICES ---
clients = [
    {"nom": "GreenHydro SAS", "secteur": "Énergies renouvelables", "montant": "2,4 M€", "pays": "France", "analyste": "A. Morel"},
    {"nom": "NeoTech Ventures", "secteur": "Technologies médicales", "montant": "1,8 M€", "pays": "Suisse", "analyste": "M. El Amrani"},
    {"nom": "BlueWave Capital", "secteur": "Finance durabl
