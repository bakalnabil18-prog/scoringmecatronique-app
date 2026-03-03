
# ═══════════════════════════════════════════════════════════════
# PROTOTYPE SCORING MÉCATRONIQUE – VERSION FOND BLANC
# ═══════════════════════════════════════════════════════════════

import streamlit as st
import plotly.graph_objects as go
from advanced_scoring import calculer_score_global

st.set_page_config(
    page_title="Scoring Mécatronique Industrie 4.0",
    layout="wide"
)

# FORCER BACKGROUND BLANC
st.markdown("""
<style>
.stApp {
    background-color: white;
}

html, body, [class*="css"]  {
    background-color: white !important;
    color: black;
}

.block-container {
    padding-top: 2rem;
}

h1, h2, h3 {
    color: black;
}

div[data-testid="stMetricValue"] {
    font-size: 28px;
}
</style>
""", unsafe_allow_html=True)

st.title("🔎 Prototype de Scoring Mécatronique – Industrie 4.0")
st.markdown("Évaluation technique du risque industriel basée sur la maturité mécatronique et maintenance.")

# ───────────────────────────────────────────────────────────────
# INPUTS
# ───────────────────────────────────────────────────────────────

st.header("1️⃣ Données générales")

col1, col2 = st.columns(2)

with col1:
    valeur_remplacement = st.number_input(
        "Valeur de remplacement (valeur équipement)",
        min_value=0,
        step=10000
    )

with col2:
    niveau_automatisation = st.slider(
        "Niveau d'automatisation (%)",
        0, 100, 50
    )

st.header("2️⃣ Maintenance & Prévention")

col3, col4 = st.columns(2)

with col3:
    equipement_manutention = st.selectbox(
        "Équipements de maintenance pour manutention",
        ["Faible", "Moyen", "Élevé"]
    )

    stockage_piece = st.selectbox(
        "Système de stockage pièces de rechange",
        ["Désorganisé", "Structuré", "Optimisé"]
    )

with col4:
    efficacite_intervention = st.slider(
        "Délai moyen d’intervention (jours)",
        0, 30, 5
    )

    systeme_maintenance = st.selectbox(
        "Système maintenance intégré",
        [
            "Papier / Excel",
            "GMAO",
            "ERP (module PM)",
            "EAM",
            "IIoT + Maintenance prédictive"
        ]
    )

# ───────────────────────────────────────────────────────────────
# CALCUL
# ───────────────────────────────────────────────────────────────

if st.button("Calculer le Score de Risque"):

    resultats = calculer_score_global(
        valeur_remplacement,
        niveau_automatisation,
        equipement_manutention,
        stockage_piece,
        efficacite_intervention,
        systeme_maintenance
    )

    score_global = resultats["score_global"]
    niveau_risque = resultats["niveau_risque"]
    details = resultats["details"]

    st.header("📊 Résultats")

    col5, col6 = st.columns(2)

    with col5:
        st.metric("Score Global", f"{score_global}/100")

    with col6:
        st.metric("Niveau de Risque", niveau_risque)

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=[details["mecatronique"],
           details["maintenance"],
           details["gouvernance"]],
        theta=["Mécatronique", "Maintenance", "Gouvernance"],
        fill='toself'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=False,
        height=400,
        paper_bgcolor="white",
        plot_bgcolor="white"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Recommandations")

    for rec in resultats["recommandations"]:
        st.write(f"- {rec}")
