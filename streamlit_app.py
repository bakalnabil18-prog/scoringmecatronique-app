import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json
import os
import sys

# Import configurations
sys.path.insert(0, os.path.dirname(__file__))
from advanced_scoring import (
    score_robustness,
    score_maintenance_maturity,
    score_governance,
    compute_advanced_scoring
)
from config_maroc import (
    SECTEURS_MAROC, TERMINOLOGIE_ASSURANCE_MAROC, CLASSES_RISQUE_MAROC,
    FRANCHISES_MAROC_DH, TAUX_PRIMES_SECTEUR, MESSAGES_MAROC,
    REGLEMENTATIONS_MAROC, RISQUES_SPECIFIQUES_MAROC, ASSUREURS_MAROC,
    MAROC_CONFIG, DEVISES
)

from engine.data_models import (
    EquipmentProfile, MaintenanceProfile, DataQualityMetrics,
    IoTFeatures, SensorSeriesSummary, UnderwritingInput
)


# ============================================================
# CONFIG & STYLING MAROCAIN — THÈME MÉCATRONIQUE
# ============================================================
st.set_page_config(
    page_title="Underwriting Maroc | Industrie 4.0",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "Système de Scoring Assurance Industrielle — Maroc 🇲🇦"}
)

# Design mécatronique — Bleu acier + Gris industriel + Orange
st.markdown("""
<style>
    /* Variables couleurs mécatronique */
    :root {
        --primary-dark: #0a1f3e;        /* Bleu acier foncé */
        --primary: #1a3a5c;             /* Bleu acier */
        --secondary: #00a651;           /* Vert technologie */
        --accent: #ff6b35;              /* Orange industrie */
        --gray-light: #f0f2f5;          /* Gris clair */
        --gray-dark: #2d3436;           /* Gris sombre */
        --success: #10b981;
        --danger: #ef4444;
        --warning: #f59e0b;
    }
    
    /* Background mécatronique */
    body {
        background: linear-gradient(135deg, #0a1f3e 0%, #1a3a5c 25%, #2d3436 50%, #1a3a5c 75%, #0a1f3e 100%);
        background-attachment: fixed;
        color: #2d3436;
    }
    
    .stApp {
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><rect fill="%231a3a5c" width="100" height="100"/><circle cx="10" cy="10" r="2" fill="%23ff6b35" opacity="0.1"/><circle cx="50" cy="50" r="2" fill="%2300a651" opacity="0.05"/></svg>');
    }
    
    /* Header mécatronique premium */
    .main-header {
        background: linear-gradient(90deg, #0a1f3e 0%, #1a3a5c 50%, #2d3436 100%);
        color: white;
        padding: 40px 30px;
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4), 
                    inset 0 1px 0 rgba(255, 255, 255, 0.1);
        border: 2px solid #ff6b35;
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 200px;
        height: 200px;
        background: radial-gradient(circle, rgba(255, 107, 53, 0.1) 0%, transparent 70%);
        border-radius: 50%;
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5em;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .main-header p {
        margin: 10px 0 0 0;
        font-size: 1.1em;
        opacity: 0.95;
        font-weight: 300;
    }
    
    /* Score cards mécatronique */
    .score-card {
        background: white;
        border-radius: 12px;
        padding: 25px;
        border-left: 6px solid #1a3a5c;
        border-top: 3px solid #ff6b35;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1),
                    0 2px 0 rgba(255, 107, 53, 0.5);
        margin: 15px 0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .score-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 25px rgba(0, 0, 0, 0.15),
                    0 2px 0 rgba(255, 107, 53, 0.7);
    }
    
    .score-card.robustness {
        border-left-color: #0066cc;
        border-top-color: #ff6b35;
    }
    
    .score-card.maintenance {
        border-left-color: #00a651;
        border-top-color: #ff6b35;
    }
    
    .score-card.governance {
        border-left-color: #ff6b35;
        border-top-color: #0a1f3e;
    }
    
    /* Risk level badge */
    .risk-badge {
        display: inline-block;
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 1.1em;
        border: 2px solid #1a3a5c;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .risk-badge.faible {
        background: #d1fae5;
        color: #00a651;
        border-color: #00a651;
    }
    
    .risk-badge.moyen {
        background: #fef3c7;
        color: #92400e;
        border-color: #f59e0b;
    }
    
    .risk-badge.élevé {
        background: #fee2e2;
        color: #8b0000;
        border-color: #ef4444;
    }
    
    /* Driver items */
    .driver-item {
        background: linear-gradient(90deg, #f9fafb 0%, #f0f2f5 100%);
        border-left: 4px solid #1a3a5c;
        border-top: 2px solid #ff6b35;
        padding: 14px;
        margin: 10px 0;
        border-radius: 6px;
        font-size: 0.95em;
        line-height: 1.6;
    }
    
    /* Form section headers */
    .form-section-header {
        font-size: 1.3em;
        font-weight: 700;
        color: #0a1f3e;
        margin: 25px 0 15px 0;
        padding-bottom: 10px;
        border-bottom: 3px solid #ff6b35;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a1f3e 0%, #1a3a5c 100%);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        border-bottom: 3px solid #ff6b35;
    }
    
    .stTabs [aria-selected="true"] {
        border-bottom: 3px solid #ff6b35 !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #1a3a5c 0%, #2d3436 100%);
        color: white;
        border: 2px solid #ff6b35;
        font-weight: 700;
        padding: 12px 24px;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #ff6b35 0%, #ff8a5c 100%);
        border-color: #0a1f3e;
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        color: #1a3a5c;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# PRESETS MAROCAINS
# ============================================================
def get_preset_maroc(case):
    presets = {
        "🏭 Textile Casablanca — FAIBLE RISQUE": {
            "secteur": "textile_confection",
            "equipment_id": "METIER-01",
            "equipment_type": "Métier à tisser automatisé",
            "replacement_value": 2500000.0,
            "age_years": 3.0,
            "mtbf_hours": 50000.0,
            "criticality": 4,
            "redundancy": True,
            "environment_severity": 2,
            "automation_level": 4,
            "sensor_coverage": 4,
            "control_system_type": "advanced",
            "maintenance_strategy": "predictive",
            "gmao_operational": True,
            "team_structure": 4,
            "manufacturer_contract": True,
            "preventive_frequency_days": 30,
            "maintenance_backlog_ratio": 0.0,
            "technician_training_level": 5,
            "spare_parts_availability": 4,
            "procedures_formalized": True,
            "pca_exists": True,
            "pca_tested": True,
            "audit_frequency_months": 6,
            "iso_certifications": ["ISO9001", "ISO45001"],
            "operator_training_level": 5,
            "documentation_quality": 4,
            "incident_tracking_system": True,
            "anomaly_detection_formalized": True,
            "continuity_test_frequency_months": 6,
            "vibration_health": 90,
            "temperature_health": 88,
            "electrical_health": 92,
            "completeness": 0.99,
            "latency_seconds": 30.0,
            "calibration_age_days": 120,
            "drift_flag": False,
            "outlier_rate": 0.01,
        },
        
        "🥕 Agroalimentaire Agadir — RISQUE MOYEN": {
            "secteur": "agroalimentaire",
            "equipment_id": "TEINTURE-03",
            "equipment_type": "Chaîne de teinture",
            "replacement_value": 1800000.0,
            "age_years": 8.0,
            "mtbf_hours": 25000.0,
            "criticality": 5,
            "redundancy": False,
            "environment_severity": 3,
            "automation_level": 2,
            "sensor_coverage": 3,
            "control_system_type": "modern",
            "maintenance_strategy": "preventive",
            "gmao_operational": True,
            "team_structure": 3,
            "manufacturer_contract": False,
            "preventive_frequency_days": 45,
            "maintenance_backlog_ratio": 0.10,
            "technician_training_level": 3,
            "spare_parts_availability": 2,
            "procedures_formalized": True,
            "pca_exists": True,
            "pca_tested": False,
            "audit_frequency_months": 12,
            "iso_certifications": ["ISO9001"],
            "operator_training_level": 3,
            "documentation_quality": 2,
            "incident_tracking_system": True,
            "anomaly_detection_formalized": False,
            "continuity_test_frequency_months": 12,
            "vibration_health": 55,
            "temperature_health": 60,
            "electrical_health": 58,
            "completeness": 0.95,
            "latency_seconds": 60.0,
            "calibration_age_days": 300,
            "drift_flag": True,
            "outlier_rate": 0.02,
        },
        
        "⛏️ Mines Phosphates Khouribga — RISQUE ÉLEVÉ": {
            "secteur": "mines_phosphates",
            "equipment_id": "EXCAVATRICE-12",
            "equipment_type": "Excavatrice lourde",
            "replacement_value": 45000000.0,
            "age_years": 12.0,
            "mtbf_hours": 15000.0,
            "criticality": 5,
            "redundancy": False,
            "environment_severity": 5,
            "automation_level": 1,
            "sensor_coverage": 1,
            "control_system_type": "legacy",
            "maintenance_strategy": "corrective",
            "gmao_operational": False,
            "team_structure": 1,
            "manufacturer_contract": False,
            "preventive_frequency_days": 120,
            "maintenance_backlog_ratio": 0.35,
            "technician_training_level": 2,
            "spare_parts_availability": 1,
            "procedures_formalized": False,
            "pca_exists": False,
            "pca_tested": False,
            "audit_frequency_months": 999,
            "iso_certifications": [],
            "operator_training_level": 2,
            "documentation_quality": 1,
            "incident_tracking_system": False,
            "anomaly_detection_formalized": False,
            "continuity_test_frequency_months": 999,
            "vibration_health": 20,
            "temperature_health": 25,
            "electrical_health": 22,
            "completeness": 0.80,
            "latency_seconds": 600.0,
            "calibration_age_days": 1200,
            "drift_flag": True,
            "outlier_rate": 0.08,
        },
    }
    return presets.get(case, {})


# ============================================================
# HEADER MÉCATRONIQUE
# ============================================================
st.markdown("""
<div class="main-header">
    <h1>🏭 UNDERWRITING MAROC</h1>
    <p>Système de Scoring Industrie 4.0 — Mécatronique Avancée</p>
</div>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================
st.sidebar.markdown("## ⚙️ Configuration")
st.sidebar.markdown("---")

# Secteur
secteur_labels = {
    "textile_confection": "🏭 Textile & Confection",
    "agroalimentaire": "🥕 Agroalimentaire",
    "mines_phosphates": "⛏️ Mines & Phosphates",
    "chimie_pharmacie": "⚗️ Chimie & Pharmacie",
    "construction_materiaux": "🏗️ Construction",
    "energie_eau": "⚡ Énergie & Eau",
    "autres": "📦 Autres",
}

secteur_selected = st.sidebar.selectbox(
    "Choisir secteur",
    list(secteur_labels.keys()),
    format_func=lambda x: secteur_labels[x]
)

if secteur_selected != "autres":
    secteur_info = SECTEURS_MAROC[secteur_selected]
    st.sidebar.markdown(f"""
    **{secteur_info['nom']}**
    - Taux base: {secteur_info['taux_base_pct']}%
    - Régions: {", ".join(secteur_info['regions'][:2])}
    """)

st.sidebar.markdown("---")

# Presets
preset_options = {
    "Manuel": None,
    "🏭 Textile Casablanca": "🏭 Textile Casablanca — FAIBLE RISQUE",
    "🥕 Agroalimentaire Agadir": "🥕 Agroalimentaire Agadir — RISQUE MOYEN",
    "⛏️ Mines Khouribga": "⛏️ Mines Phosphates Khouribga — RISQUE ÉLEVÉ",
}

case_selected = st.sidebar.selectbox("Preset", list(preset_options.keys()))
preset_data = get_preset_maroc(preset_options[case_selected]) if preset_options[case_selected] else {}


# ============================================================
# ONGLETS
# ============================================================
tab1, tab2, tab3, tab4 = st.tabs(["📝 Saisie Équipement", "📊 Scoring 3-Piliers", "🎯 Décision", "💰 Finance"])


# ============================================================
# TAB 1 — SAISIE ÉQUIPEMENT
# ============================================================
with tab1:
    st.header("Formulaire Saisie Équipement")
    st.caption(f"Secteur: {secteur_labels[secteur_selected]}")
    
    if secteur_selected != "autres":
        secteur_data = SECTEURS_MAROC[secteur_selected]
        st.info(f"**{secteur_data['nom']}** — {secteur_data['importance']}")
    
    # Equipment
    st.markdown('<div class="form-section-header">⚙️ Équipement & Infrastructure</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        equipment_id = st.text_input("ID Équipement", value=preset_data.get("equipment_id", "EQ-01"))
    with col2:
        equipment_type = st.text_input("Type", value=preset_data.get("equipment_type", "Machine"))
    with col3:
        replacement_value = st.number_input("Valeur d'équipement", min_value=10000.0, value=float(preset_data.get("replacement_value", 500000.0)), step=50000.0, format="%.0f")
    with col4:
        age_years = st.number_input("Âge (années)", min_value=0.0, value=float(preset_data.get("age_years", 5.0)), step=1.0)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        mtbf_hours = st.number_input("MTBF (heures)", min_value=100.0, value=float(preset_data.get("mtbf_hours", 40000.0)), step=1000.0)
    with col2:
        criticality = st.slider("Criticité (1-5)", 1, 5, int(preset_data.get("criticality", 3)))
    with col3:
        redundancy = st.checkbox("Redondance", value=bool(preset_data.get("redundancy", False)))
    with col4:
        environment_severity = st.slider("Sévérité env. (1-5)", 1, 5, int(preset_data.get("environment_severity", 3)))
    
    # Technology
    st.markdown('<div class="form-section-header">🔧 Technologie & Automatisation</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        automation_level = st.selectbox("Automatisation", ["Manuel (1)", "Semi-auto (2)", "Automatisé (3)", "IoT (4)"], index=int(preset_data.get("automation_level", 1)) - 1)
        automation_level = int(automation_level.split("(")[1].strip(")"))
    with col2:
        sensor_coverage = st.selectbox("Capteurs", ["Aucun (1)", "Basique (2)", "Avancée (3)", "Complète (4)"], index=int(preset_data.get("sensor_coverage", 1)) - 1)
        sensor_coverage = int(sensor_coverage.split("(")[1].strip(")"))
    with col3:
        control_system_type = st.selectbox("Système de contrôle", ["Legacy", "Modern", "Advanced"], index={"legacy": 0, "modern": 1, "advanced": 2}.get(preset_data.get("control_system_type", "legacy"), 0))
        control_system_type = control_system_type.lower()
    with col4:
        vibration_health = st.slider("Santé vibration (0-100)", 0, 100, int(preset_data.get("vibration_health", 50)))
    
    # Maintenance
    st.markdown('<div class="form-section-header">🔧 Maintenance & Exploitation</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        maintenance_strategy = st.selectbox("Stratégie", ["Corrective", "Preventive", "Predictive"], index={"corrective": 0, "preventive": 1, "predictive": 2}.get(preset_data.get("maintenance_strategy", "preventive"), 0))
    with col2:
        gmao_operational = st.checkbox("GMAO opérationnelle", value=bool(preset_data.get("gmao_operational", False)))
    with col3:
        preventive_compliance = st.slider("Conformité prév. (0-1)", 0.0, 1.0, float(preset_data.get("preventive_compliance", 0.85)), 0.01)
    with col4:
        mean_response_days = st.number_input("Temps réponse (jours)", min_value=0.0, value=float(preset_data.get("mean_response_days", 7.0)), step=1.0)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        team_structure = st.selectbox("Équipe", ["Informelle (1)", "Basique (2)", "Structurée (3)", "Certifiée (4)"], index=int(preset_data.get("team_structure", 2)) - 1)
        team_structure = int(team_structure.split("(")[1].strip(")"))
    with col2:
        technician_training_level = st.slider("Formation tech. (1-5)", 1, 5, int(preset_data.get("technician_training_level", 3)))
    with col3:
        spare_parts_availability = st.selectbox("Pièces détachées", ["Faible (1)", "Basique (2)", "Bonne (3)", "Excellente (4)"], index=int(preset_data.get("spare_parts_availability", 2)) - 1)
        spare_parts_availability = int(spare_parts_availability.split("(")[1].strip(")"))
    with col4:
        preventive_frequency_days = st.number_input("Fréquence prév. (jours)", min_value=1, value=int(preset_data.get("preventive_frequency_days", 90)), step=10)
    
    # Governance
    st.markdown('<div class="form-section-header">📋 Gouvernance & Conformité</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        procedures_formalized = st.checkbox("Procédures formalisées", value=bool(preset_data.get("procedures_formalized", False)))
    with col2:
        pca_exists = st.checkbox("PCA en place", value=bool(preset_data.get("pca_exists", False)))
    with col3:
        pca_tested = st.checkbox("PCA testé", value=bool(preset_data.get("pca_tested", False)))
    with col4:
        audit_frequency_months = st.number_input("Audit (mois)", min_value=1, value=int(preset_data.get("audit_frequency_months", 12)), step=6)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        operator_training_level = st.slider("Formation opér. (1-5)", 1, 5, int(preset_data.get("operator_training_level", 3)))
    with col2:
        documentation_quality = st.selectbox("Documentation", ["Faible (1)", "Basique (2)", "Bonne (3)", "Excellente (4)"], index=int(preset_data.get("documentation_quality", 2)) - 1)
        documentation_quality = int(documentation_quality.split("(")[1].strip(")"))
    with col3:
        incident_tracking_system = st.checkbox("Tracking incidents", value=bool(preset_data.get("incident_tracking_system", False)))
    with col4:
        anomaly_detection_formalized = st.checkbox("Détection anomalies", value=bool(preset_data.get("anomaly_detection_formalized", False)))
    
    col1, col2, col3 = st.columns(3)
    with col1:
        maintenance_backlog_ratio = st.slider("Arriéré maint. (0-1)", 0.0, 1.0, float(preset_data.get("maintenance_backlog_ratio", 0.1)), 0.01)
    with col2:
        temperature_health = st.slider("Santé temp. (0-100)", 0, 100, int(preset_data.get("temperature_health", 50)))
    with col3:
        electrical_health = st.slider("Santé électrique (0-100)", 0, 100, int(preset_data.get("electrical_health", 50)))
    
    # Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 LANCER ANALYSE", key="analyze_btn", use_container_width=True):
            try:
                equipment = EquipmentProfile(
                    equipment_id=equipment_id,
                    equipment_type=equipment_type,
                    replacement_value=float(replacement_value),
                    age_years=float(age_years),
                    mtbf_hours=float(mtbf_hours),
                    criticality=int(criticality),
                    redundancy=bool(redundancy),
                    environment_severity=int(environment_severity),
                )
                
                robustness = score_robustness(
                    equipment_age_years=float(age_years),
                    automation_level=automation_level,
                    sensor_coverage=sensor_coverage,
                    redundancy=float(redundancy),
                    control_system_type=control_system_type,
                    vibration_health=float(vibration_health),
                    temperature_health=float(temperature_health),
                    electrical_health=float(electrical_health),
                )
                
                maintenance = score_maintenance_maturity(
                    maintenance_strategy=maintenance_strategy.lower(),
                    gmao_operational=gmao_operational,
                    pm_compliance=preventive_compliance,
                    team_structure=team_structure,
                    manufacturer_contract=preset_data.get("manufacturer_contract", False),
                    preventive_frequency_days=int(preventive_frequency_days),
                    maintenance_backlog_ratio=float(maintenance_backlog_ratio),
                    technician_training_level=technician_training_level,
                    spare_parts_availability=spare_parts_availability,
                )
                
                governance = score_governance(
                    procedures_formalized=procedures_formalized,
                    pca_exists=pca_exists,
                    pca_tested=pca_tested,
                    audit_frequency_months=int(audit_frequency_months),
                    iso_certifications=["ISO"] * 0,
                    operator_training_level=operator_training_level,
                    documentation_quality=documentation_quality,
                    incident_tracking_system=incident_tracking_system,
                    anomaly_detection_formalized=anomaly_detection_formalized,
                    continuity_test_frequency_months=preset_data.get("continuity_test_frequency_months", 12),
                )
                
                advanced_result = compute_advanced_scoring(robustness, maintenance, governance)
                
                st.session_state.robustness = robustness
                st.session_state.maintenance = maintenance
                st.session_state.governance = governance
                st.session_state.advanced_result = advanced_result
                st.session_state.equipment = equipment
                st.session_state.secteur_selected = secteur_selected
                
                st.success("✅ Analyse complétée! Consultez les autres onglets.")
            
            except Exception as e:
                st.error(f"❌ Erreur: {str(e)}")


# ============================================================
# TAB 2 — SCORING 3-PILIERS
# ============================================================
with tab2:
    st.header("Scoring Avancé — 3 Piliers")
    
    if hasattr(st.session_state, 'advanced_result'):
        result = st.session_state.advanced_result
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            risk_color = "faible" if result.risk_level == "FAIBLE" else ("moyen" if result.risk_level == "MOYEN" else "élevé")
            st.markdown(f"""
            <div class="score-card" style="text-align: center;">
                <h3>Score Global</h3>
                <div style="font-size: 3em; font-weight: 700; color: #1a3a5c; margin: 15px 0;">{result.global_score:.1f}/100</div>
                <div class="risk-badge {risk_color}">{result.risk_level}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="score-card robustness">
                <h4>🔧 Robustesse (35%)</h4>
                <div style="font-size: 2.5em; font-weight: 700; color: #0066cc; margin: 10px 0;">{result.robustness.score:.0f}</div>
            </div>
            """, unsafe_allow_html=True)
            for driver in result.robustness.drivers[:3]:
                st.markdown(f'<div class="driver-item">{driver}</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="score-card maintenance">
                <h4>🎯 Maintenance (45%)</h4>
                <div style="font-size: 2.5em; font-weight: 700; color: #00a651; margin: 10px 0;">{result.maintenance.score:.0f}</div>
            </div>
            """, unsafe_allow_html=True)
            for driver in result.maintenance.drivers[:3]:
                st.markdown(f'<div class="driver-item">{driver}</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="score-card governance">
                <h4>📋 Gouvernance (20%)</h4>
                <div style="font-size: 2.5em; font-weight: 700; color: #ff6b35; margin: 10px 0;">{result.governance.score:.0f}</div>
            </div>
            """, unsafe_allow_html=True)
            for driver in result.governance.drivers[:3]:
                st.markdown(f'<div class="driver-item">{driver}</div>', unsafe_allow_html=True)
        
        with col2:
            fig_radar = go.Figure(data=go.Scatterpolar(
                r=[result.robustness.score, result.maintenance.score, result.governance.score],
                theta=['Robustesse', 'Maintenance', 'Gouvernance'],
                fill='toself',
                line_color='#ff6b35'
            ))
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100], gridcolor='#ddd')),
                showlegend=False,
                height=400,
                title="Profil de Risque",
                template="plotly_white"
            )
            st.plotly_chart(fig_radar, use_container_width=True)
    else:
        st.info("👈 Complétez d'abord le formulaire")


# ============================================================
# TAB 3 — DÉCISION
# ============================================================
with tab3:
    st.header("Décision & Recommandations")
    
    if hasattr(st.session_state, 'advanced_result'):
        result = st.session_state.advanced_result
        equipment = st.session_state.equipment
        
        if result.global_score >= 75:
            classe = CLASSES_RISQUE_MAROC["classe_1"]
        elif result.global_score >= 50:
            classe = CLASSES_RISQUE_MAROC["classe_2"]
        elif result.global_score >= 25:
            classe = CLASSES_RISQUE_MAROC["classe_3"]
        else:
            classe = CLASSES_RISQUE_MAROC["classe_4"]
        
        st.markdown(f"""
        ### Classification
        **{classe['nom']}** | Score: {result.global_score:.0f}
        - Franchise recommandée: {classe['franchise_dh']}
        - Taux prime: {classe['taux_prime']}
        """)
        
        st.markdown("### 💡 Recommandations")
        for i, rec in enumerate(result.recommendations, 1):
            st.markdown(f'<div style="background: #f0f2f5; border-left: 4px solid #ff6b35; padding: 12px; margin: 8px 0; border-radius: 6px;">{i}. {rec}</div>', unsafe_allow_html=True)
    else:
        st.info("👈 Complétez d'abord le formulaire")


# ============================================================
# TAB 4 — ANALYSE FINANCIÈRE
# ============================================================
with tab4:
    st.header("Analyse Financière")
    
    if hasattr(st.session_state, 'advanced_result'):
        result = st.session_state.advanced_result
        equipment = st.session_state.equipment
        secteur = st.session_state.secteur_selected
        
        if result.global_score >= 75:
            taux_min, taux_max = 0.4, 0.6
        elif result.global_score >= 50:
            taux_min, taux_max = 0.7, 1.2
        elif result.global_score >= 25:
            taux_min, taux_max = 1.3, 2.0
        else:
            taux_min, taux_max = 2.0, 4.0
        
        taux_moyen = (taux_min + taux_max) / 2
        secteur_data = SECTEURS_MAROC.get(secteur, {})
        taux_secteur = secteur_data.get("taux_base_pct", 1.0)
        
        prime_ht = equipment.replacement_value * (taux_secteur / 100)
        tva = prime_ht * 0.20
        total_ttc = prime_ht + tva
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Valeur", f"{equipment.replacement_value:,.0f}")
        with col2:
            st.metric("Taux", f"{taux_secteur:.2f}%")
        with col3:
            st.metric("Prime HT", f"{prime_ht:,.0f}")
        with col4:
            st.metric("Prime TTC", f"{total_ttc:,.0f}")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            ### Détail Calcul
            - Valeur: {equipment.replacement_value:,.0f}
            - Taux: {taux_secteur}%
            - Prime HT: {prime_ht:,.0f}
            - TVA 20%: {tva:,.0f}
            - **Total: {total_ttc:,.0f}**
            """)
        
        with col2:
            fig_pie = px.pie(
                names=['Prime HT', 'TVA'],
                values=[prime_ht, tva],
                title="Composition",
                color_discrete_sequence=['#1a3a5c', '#ff6b35']
            )
            st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("👈 Complétez d'abord le formulaire")


# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9em; padding: 20px;">
    <p>🇲🇦 <strong>Underwriting Maroc</strong> | Industrie 4.0 | Scoring Mécatronique</p>
    <p>Code Assurances Maroc | ACPR | Normes ISO</p>
    <p>© 2026 — Version 2.0</p>
</div>
""", unsafe_allow_html=True)
