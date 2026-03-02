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
from engine.pipeline import run_underwriting
from engine.reporting import save_underwriting_report


# ============================================================
# CONFIG & STYLING MAROCAIN
# ============================================================
st.set_page_config(
    page_title="Underwriting Maroc | Industrie 4.0",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "Système de Scoring Assurance Industrielle — Maroc 🇲🇦"}
)

# Design premium marocain (bleu royal + vert + or)
st.markdown("""
<style>
    /* Couleurs marocaines */
    :root {
        --primary: #003d5c;      /* Bleu royal marocain */
        --secondary: #00a651;    /* Vert marocain */
        --accent: #c69c6d;       /* Or marocain */
        --success: #10b981;
        --danger: #ef4444;
        --warning: #f59e0b;
    }
    
    /* Header marocain */
    .main-header {
        background: linear-gradient(135deg, #003d5c 0%, #005a7f 50%, #00a651 100%);
        color: white;
        padding: 30px;
        border-radius: 10px;
        margin-bottom: 30px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.2);
        border: 3px solid #c69c6d;
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.2em;
        font-weight: 700;
    }
    
    .main-header .flag {
        font-size: 2em;
        margin-right: 10px;
    }
    
    /* Score cards */
    .score-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        border-left: 6px solid #003d5c;
        border-top: 3px solid #c69c6d;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    
    .score-card.robustness {
        border-left-color: #0066cc;
        border-top-color: #003d5c;
    }
    
    .score-card.maintenance {
        border-left-color: #00a651;
        border-top-color: #006633;
    }
    
    .score-card.governance {
        border-left-color: #c69c6d;
        border-top-color: #8b6f47;
    }
    
    /* Risk level badge marocain */
    .risk-badge-maroc {
        display: inline-block;
        padding: 10px 20px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 1.1em;
        border: 2px solid #003d5c;
    }
    
    .risk-badge-maroc.faible {
        background: #d1fae5;
        color: #00a651;
        border-color: #00a651;
    }
    
    .risk-badge-maroc.moyen {
        background: #fef3c7;
        color: #92400e;
        border-color: #f59e0b;
    }
    
    .risk-badge-maroc.élevé {
        background: #fee2e2;
        color: #8b0000;
        border-color: #ef4444;
    }
    
    /* Driver items */
    .driver-item {
        background: #f9fafb;
        border-left: 4px solid #003d5c;
        border-top: 2px solid #c69c6d;
        padding: 12px;
        margin: 8px 0;
        border-radius: 6px;
        font-size: 0.95em;
        line-height: 1.6;
    }
    
    /* Form section */
    .form-section-header {
        font-size: 1.3em;
        font-weight: 700;
        color: #003d5c;
        margin: 20px 0 15px 0;
        padding-bottom: 10px;
        border-bottom: 3px solid #c69c6d;
    }
    
    /* Sector selector */
    .sector-selector {
        background: linear-gradient(90deg, #003d5c 0%, #00a651 100%);
        color: white;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    
    /* Button marocain */
    .button-maroc {
        background: linear-gradient(135deg, #003d5c 0%, #005a7f 100%) !important;
        border: 2px solid #c69c6d !important;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# PRESETS MAROCAINS AVANCÉS
# ============================================================
def get_preset_maroc(case):
    presets = {
        "🏭 Textile Casablanca — FAIBLE RISQUE": {
            "secteur": "textile_confection",
            "equipment_id": "METIER-01",
            "equipment_type": "Métier à tisser automatisé",
            "replacement_value": 2500000.0,  # En DH
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
            "equipment_type": "Excavatrice lourde (45M DH)",
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
# HEADER MAROCAIN
# ============================================================
st.markdown("""
<div class="main-header">
    <div style="display: flex; align-items: center;">
        <span class="flag">🇲🇦</span>
        <div>
            <h1>UNDERWRITING MAROC — Industrie 4.0</h1>
            <p style="margin: 5px 0; font-size: 1.1em; opacity: 0.95;">
                Système de Scoring pour Assurance Industrielle au Maroc
            </p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Devise affichée
col1, col2, col3 = st.columns([2, 1, 1])
with col2:
    st.metric("💱 Devise", "Dirham (DH)")
with col3:
    st.metric("📍 Marché", "Maroc")


# ============================================================
# SIDEBAR MAROCAIN
# ============================================================
st.sidebar.markdown("## 🇲🇦 Configuration Maroc")
st.sidebar.markdown("---")

# Secteur choix
secteur_labels = {
    "textile_confection": "🏭 Textile & Confection",
    "agroalimentaire": "🥕 Agroalimentaire",
    "mines_phosphates": "⛏️ Mines & Phosphates",
    "chimie_pharmacie": "⚗️ Chimie & Pharmacie",
    "construction_materiaux": "🏗️ Construction & Matériaux",
    "energie_eau": "⚡ Énergie & Eau",
    "autres": "📦 Autres secteurs",
}

secteur_selected = st.sidebar.selectbox(
    "🏢 Choisir secteur d'activité",
    list(secteur_labels.keys()),
    format_func=lambda x: secteur_labels[x]
)

# Info secteur
if secteur_selected != "autres":
    secteur_info = SECTEURS_MAROC[secteur_selected]
    st.sidebar.markdown(f"""
    **{secteur_info['nom']}**
    - Taux base: {secteur_info['taux_base_pct']}%
    - Régions: {", ".join(secteur_info['regions'])}
    """)

st.sidebar.markdown("---")

# Presets marocains
preset_options = {
    "Manuel": None,
    "🏭 Textile Casablanca — FAIBLE RISQUE": "🏭 Textile Casablanca — FAIBLE RISQUE",
    "🥕 Agroalimentaire Agadir — RISQUE MOYEN": "🥕 Agroalimentaire Agadir — RISQUE MOYEN",
    "⛏️ Mines Phosphates Khouribga — RISQUE ÉLEVÉ": "⛏️ Mines Phosphates Khouribga — RISQUE ÉLEVÉ",
}

case_selected = st.sidebar.selectbox(
    "⚡ Scénarios rapides (presets)",
    list(preset_options.keys())
)

preset_data = get_preset_maroc(preset_options[case_selected]) if preset_options[case_selected] else {}

st.sidebar.markdown("---")

st.sidebar.markdown("""
### 📖 Guide Utilisation
1. **Choisissez un secteur** (textile, agroalim, mines, etc.)
2. **Optionnel**: Charger un preset rapide
3. **Remplissez les données** d'équipement et maintenance
4. **Cliquez « ANALYSER »**
5. **Consultez les onglets** pour résultats détaillés

### 🇲🇦 Spécificités Maroc
- **Devise**: Dirham marocain (DH)
- **Réglementations**: Code assurances Maroc + ACPR
- **Secteurs locaux**: Textile, agroalim, mines, chimie
- **Normes**: ISO + certifications marocaines
- **Risques spécifiques**: Climat, approvisionnement, change
""")


# ============================================================
# ONGLETS
# ============================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📝 Saisie Équipement", 
    "📊 Scoring 3-Piliers", 
    "🎯 Décision & Recommandations", 
    "💰 Analyse Financière"
])


# ============================================================
# TAB 1 — SAISIE ÉQUIPEMENT MAROCAIN
# ============================================================
with tab1:
    st.header("Formulaire Saisie Équipement")
    st.caption(f"Secteur choisi: {secteur_labels[secteur_selected]}")
    
    # --- Secteur info box ---
    if secteur_selected != "autres":
        secteur_data = SECTEURS_MAROC[secteur_selected]
        st.info(f"""
        **{secteur_data['nom']}** 
        - Importance: {secteur_data['importance']}
        - Principales régions: {", ".join(secteur_data['regions'])}
        - Risques spécifiques: {", ".join(secteur_data['risques_specifiques'][:2])}
        """)
    
    # --- Equipment ---
    st.markdown('<div class="form-section-header">⚙️ ÉQUIPEMENT & INFRASTRUCTURE</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        equipment_id = st.text_input("ID Équipement", value=preset_data.get("equipment_id", "EQ-01"))
    with col2:
        equipment_type = st.text_input("Type d'équipement", value=preset_data.get("equipment_type", "Machine"))
    with col3:
        replacement_value = st.number_input(
            "Valeur de remplacement (DH)", 
            min_value=10000.0, 
            value=float(preset_data.get("replacement_value", 500000.0)), 
            step=50000.0,
            format="%.0f"
        )
    with col4:
        age_years = st.number_input("Âge (années)", min_value=0.0, value=float(preset_data.get("age_years", 5.0)), step=1.0)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        mtbf_hours = st.number_input("MTBF (heures)", min_value=100.0, value=float(preset_data.get("mtbf_hours", 40000.0)), step=1000.0)
    with col2:
        criticality = st.slider("Criticité (1-5)", 1, 5, int(preset_data.get("criticality", 3)))
    with col3:
        redundancy = st.checkbox("Redondance présente", value=bool(preset_data.get("redundancy", False)))
    with col4:
        environment_severity = st.slider("Sévérité environnement (1-5)", 1, 5, int(preset_data.get("environment_severity", 3)))
    
    # --- Technology ---
    st.markdown('<div class="form-section-header">🔧 TECHNOLOGIE & AUTOMATISATION</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        automation_level = st.selectbox(
            "Niveau automatisation", 
            ["Manuel (1)", "Semi-auto (2)", "Automatisé (3)", "IoT avancé (4)"],
            index=int(preset_data.get("automation_level", 1)) - 1
        )
        automation_level = int(automation_level.split("(")[1].strip(")"))
    with col2:
        sensor_coverage = st.selectbox(
            "Couverture capteurs",
            ["Aucun (1)", "Basique (2)", "Avancée (3)", "Complète (4)"],
            index=int(preset_data.get("sensor_coverage", 1)) - 1
        )
        sensor_coverage = int(sensor_coverage.split("(")[1].strip(")"))
    with col3:
        control_system_type = st.selectbox(
            "Système de contrôle", 
            ["Legacy (ancien)", "Modern (moderne)", "Advanced (avancé)"],
            index={"legacy": 0, "modern": 1, "advanced": 2}.get(preset_data.get("control_system_type", "legacy"), 0)
        )
        control_system_type = control_system_type.split("(")[0].strip().lower()
    with col4:
        vibration_health = st.slider("Santé vibration (0-100)", 0, 100, int(preset_data.get("vibration_health", 50)))
    
    # --- Maintenance ---
    st.markdown('<div class="form-section-header">🔧 MAINTENANCE & EXPLOITATION</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        maintenance_strategy = st.selectbox(
            "Stratégie maintenance", 
            ["Corrective", "Preventive", "Predictive"],
            index={"corrective": 0, "preventive": 1, "predictive": 2}.get(preset_data.get("maintenance_strategy", "preventive"), 0)
        )
    with col2:
        gmao_operational = st.checkbox("GMAO opérationnelle", value=bool(preset_data.get("gmao_operational", False)))
    with col3:
        preventive_compliance = st.slider("Conformité préventif (0-1)", 0.0, 1.0, float(preset_data.get("preventive_compliance", 0.85)), 0.01)
    with col4:
        mean_response_days = st.number_input("Temps réponse moy (jours)", min_value=0.0, value=float(preset_data.get("mean_response_days", 7.0)), step=1.0)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        team_structure = st.selectbox(
            "Structure équipe", 
            ["Informelle (1)", "Basique (2)", "Structurée (3)", "Certifiée (4)"],
            index=int(preset_data.get("team_structure", 2)) - 1
        )
        team_structure = int(team_structure.split("(")[1].strip(")"))
    with col2:
        technician_training_level = st.slider("Formation techniciens (1-5)", 1, 5, int(preset_data.get("technician_training_level", 3)))
    with col3:
        spare_parts_availability = st.selectbox(
            "Disponibilité pièces",
            ["Faible (1)", "Basique (2)", "Bonne (3)", "Excellente (4)"],
            index=int(preset_data.get("spare_parts_availability", 2)) - 1
        )
        spare_parts_availability = int(spare_parts_availability.split("(")[1].strip(")"))
    with col4:
        preventive_frequency_days = st.number_input("Fréquence prév (jours)", min_value=1, value=int(preset_data.get("preventive_frequency_days", 90)), step=10)
    
    # --- Governance ---
    st.markdown('<div class="form-section-header">📋 GOUVERNANCE & CONFORMITÉ</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        procedures_formalized = st.checkbox("Procédures formalisées", value=bool(preset_data.get("procedures_formalized", False)))
    with col2:
        pca_exists = st.checkbox("PCA en place", value=bool(preset_data.get("pca_exists", False)))
    with col3:
        audit_frequency_months = st.number_input("Fréquence audit (mois)", min_value=1, value=int(preset_data.get("audit_frequency_months", 12)), step=6)
    with col4:
        iso_certifications = st.number_input("Certifications ISO", min_value=0, max_value=5, value=len(preset_data.get("iso_certifications", [])))
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        maintenance_backlog_ratio = st.slider("Arriéré maintenance (0-1)", 0.0, 1.0, float(preset_data.get("maintenance_backlog_ratio", 0.1)), 0.01)
    with col2:
        operator_training_level = st.slider("Formation opérateurs (1-5)", 1, 5, int(preset_data.get("operator_training_level", 3)))
    with col3:
        incident_tracking_system = st.checkbox("Tracking incidents", value=bool(preset_data.get("incident_tracking_system", False)))
    with col4:
        anomaly_detection_formalized = st.checkbox("Détection anomalies", value=bool(preset_data.get("anomaly_detection_formalized", False)))
    
    col1, col2, col3 = st.columns(3)
    with col1:
        last_major_overhaul_days = st.number_input("Dernier overhaul (jours)", min_value=0, value=int(preset_data.get("last_major_overhaul_days", 300)), step=10)
    with col2:
        temperature_health = st.slider("Santé température (0-100)", 0, 100, int(preset_data.get("temperature_health", 50)))
    with col3:
        electrical_health = st.slider("Santé électrique (0-100)", 0, 100, int(preset_data.get("electrical_health", 50)))
    
    st.markdown("---")
    
    # Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 LANCER SCORING AVANCÉ", key="analyze_btn", use_container_width=True):
            try:
                # Build objects
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
                
                # Advanced scoring
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
                    pca_tested=preset_data.get("pca_tested", False),
                    audit_frequency_months=int(audit_frequency_months),
                    iso_certifications=["ISO" + str(i) for i in range(iso_certifications)],
                    operator_training_level=operator_training_level,
                    documentation_quality=preset_data.get("documentation_quality", 2),
                    incident_tracking_system=incident_tracking_system,
                    anomaly_detection_formalized=anomaly_detection_formalized,
                    continuity_test_frequency_months=preset_data.get("continuity_test_frequency_months", 12),
                )
                
                # Advanced result
                advanced_result = compute_advanced_scoring(robustness, maintenance, governance)
                
                # Store in session
                st.session_state.robustness = robustness
                st.session_state.maintenance = maintenance
                st.session_state.governance = governance
                st.session_state.advanced_result = advanced_result
                st.session_state.equipment = equipment
                st.session_state.secteur_selected = secteur_selected
                
                st.success("✅ Scoring avancé terminé! Consultez les onglets résultats.")
            
            except Exception as e:
                st.error(f"❌ Erreur: {str(e)}")


# ============================================================
# TAB 2 — SCORING 3-PILIERS MAROCAIN
# ============================================================
with tab2:
    st.header("📊 Scoring Avancé — 3 Piliers")
    
    if hasattr(st.session_state, 'advanced_result'):
        result = st.session_state.advanced_result
        secteur = st.session_state.secteur_selected
        
        # --- Affichage global ---
        col1, col2, col3 = st.columns(3)
        
        with col1:
            risk_color = "faible" if result.risk_level == "FAIBLE" else ("moyen" if result.risk_level == "MOYEN" else "élevé")
            st.markdown(f"""
            <div class="score-card" style="text-align: center;">
                <h3>Score Global de Risque</h3>
                <div style="font-size: 3em; font-weight: 700; color: #003d5c; margin: 15px 0;">{result.global_score:.1f} / 100</div>
                <div class="risk-badge-maroc {risk_color}">
                    {result.risk_level}
                </div>
                <p style="color: #666; font-size: 0.9em; margin-top: 10px;">
                    Pondération: Robustesse 35% | Maintenance 45% | Gouvernance 20%
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            rob_color = "good" if result.robustness.score >= 75 else ("warning" if result.robustness.score >= 50 else "danger")
            st.markdown(f"""
            <div class="score-card robustness">
                <h4>🔧 Robustesse Mécatronique (35%)</h4>
                <div style="font-size: 2.5em; font-weight: 700; color: #0066cc; margin: 10px 0;">{result.robustness.score:.0f}</div>
                <p style="color: #666; font-size: 0.85em;">État technique & instrumentation</p>
            </div>
            """, unsafe_allow_html=True)
            
            for driver in result.robustness.drivers[:3]:
                driver_class = "positive" if "✓✓" in driver else ("positive" if "✓" in driver else "danger" if "❌" in driver else "warning")
                st.markdown(f'<div class="driver-item {driver_class}">{driver}</div>', unsafe_allow_html=True)
        
        with col3:
            maint_color = "good" if result.maintenance.score >= 75 else ("warning" if result.maintenance.score >= 50 else "danger")
            st.markdown(f"""
            <div class="score-card maintenance">
                <h4>🎯 Maturité Maintenance (45%)</h4>
                <div style="font-size: 2.5em; font-weight: 700; color: #00a651; margin: 10px 0;">{result.maintenance.score:.0f}</div>
                <p style="color: #666; font-size: 0.85em;">Procédures & discipline</p>
            </div>
            """, unsafe_allow_html=True)
            
            for driver in result.maintenance.drivers[:3]:
                driver_class = "positive" if "✓✓" in driver else ("positive" if "✓" in driver else "danger" if "❌" in driver else "warning")
                st.markdown(f'<div class="driver-item {driver_class}">{driver}</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # --- Gouvernance ---
        col1, col2 = st.columns(2)
        
        with col1:
            gov_color = "good" if result.governance.score >= 75 else ("warning" if result.governance.score >= 50 else "danger")
            st.markdown(f"""
            <div class="score-card governance">
                <h4>📋 Gouvernance Technique (20%)</h4>
                <div style="font-size: 2.5em; font-weight: 700; color: #c69c6d; margin: 10px 0;">{result.governance.score:.0f}</div>
                <p style="color: #666; font-size: 0.85em;">Organisation & encadrement</p>
            </div>
            """, unsafe_allow_html=True)
            
            for driver in result.governance.drivers[:3]:
                driver_class = "positive" if "✓✓" in driver else ("positive" if "✓" in driver else "danger" if "❌" in driver else "warning")
                st.markdown(f'<div class="driver-item {driver_class}">{driver}</div>', unsafe_allow_html=True)
        
        with col2:
            # Radar chart
            fig_radar = go.Figure(data=go.Scatterpolar(
                r=[result.robustness.score, result.maintenance.score, result.governance.score],
                theta=['Robustesse', 'Maintenance', 'Gouvernance'],
                fill='toself',
                name='Score',
                line_color='#003d5c'
            ))
            
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                showlegend=False,
                height=400,
                title="Profil de Risque"
            )
            
            st.plotly_chart(fig_radar, use_container_width=True)
    
    else:
        st.info("👈 Remplissez le formulaire et cliquez 'LANCER SCORING'")


# ============================================================
# TAB 3 — DÉCISION & RECOMMANDATIONS MAROCAINES
# ============================================================
with tab3:
    st.header("🎯 Décision & Recommandations")
    
    if hasattr(st.session_state, 'advanced_result'):
        result = st.session_state.advanced_result
        equipment = st.session_state.equipment
        secteur = st.session_state.secteur_selected
        
        # Classe de risque marocaine
        if result.global_score >= 75:
            classe = CLASSES_RISQUE_MAROC["classe_1"]
        elif result.global_score >= 50:
            classe = CLASSES_RISQUE_MAROC["classe_2"]
        elif result.global_score >= 25:
            classe = CLASSES_RISQUE_MAROC["classe_3"]
        else:
            classe = CLASSES_RISQUE_MAROC["classe_4"]
        
        st.markdown(f"""
        ### Classification Marocaine
        **Classe: {classe['nom']}** | Score: {result.global_score:.0f}
        - Franchise recommandée: {classe['franchise_dh']} DH
        - Taux prime: {classe['taux_prime']}
        """)
        
        # Recommandations
        st.markdown("### 💡 Recommandations de Souscription")
        
        for i, rec in enumerate(result.recommendations, 1):
            st.markdown(f'<div style="background: #eff6ff; border-left: 4px solid #003d5c; padding: 12px; border-radius: 6px; margin: 8px 0;">{i}. {rec}</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Priorités de prévention
        st.markdown("### 🔴 Priorités de Prévention")
        
        for priority in result.prevention_priorities:
            priority_class = "danger" if "Priorité 1" in priority else ("warning" if "Priorité 2" in priority else "positive")
            st.markdown(f'<div class="driver-item {priority_class}">{priority}</div>', unsafe_allow_html=True)
    
    else:
        st.info("👈 Complétez d'abord le scoring")


# ============================================================
# TAB 4 — ANALYSE FINANCIÈRE MAROCAINE
# ============================================================
with tab4:
    st.header("💰 Analyse Financière — Maroc")
    
    if hasattr(st.session_state, 'advanced_result'):
        result = st.session_state.advanced_result
        equipment = st.session_state.equipment
        secteur = st.session_state.secteur_selected
        
        # Classe & taux
        if result.global_score >= 75:
            classe = CLASSES_RISQUE_MAROC["classe_1"]
            taux_min, taux_max = 0.4, 0.6
        elif result.global_score >= 50:
            classe = CLASSES_RISQUE_MAROC["classe_2"]
            taux_min, taux_max = 0.7, 1.2
        elif result.global_score >= 25:
            classe = CLASSES_RISQUE_MAROC["classe_3"]
            taux_min, taux_max = 1.3, 2.0
        else:
            classe = CLASSES_RISQUE_MAROC["classe_4"]
            taux_min, taux_max = 2.0, 4.0
        
        # Calculs
        taux_moyen = (taux_min + taux_max) / 2
        prime_base_dh = equipment.replacement_value * (taux_moyen / 100)
        
        # Majorations/réductions secteur
        secteur_data = SECTEURS_MAROC.get(secteur, {})
        taux_secteur = secteur_data.get("taux_base_pct", 1.0)
        prime_ajustee = equipment.replacement_value * (taux_secteur / 100)
        
        # TVA
        tva_dh = prime_ajustee * MAROC_CONFIG["tva_standard"]
        total_ttc = prime_ajustee + tva_dh
        
        # Affichage
        st.markdown(f"""
        ### 📊 Estimation de Prime — Maroc (DH)
        """)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Valeur Assurée", f"{equipment.replacement_value:,.0f} DH")
        with col2:
            st.metric("Taux Prime", f"{taux_secteur:.2f}%")
        with col3:
            st.metric("Prime HT", f"{prime_ajustee:,.0f} DH")
        with col4:
            st.metric("Prime TTC", f"{total_ttc:,.0f} DH")
        
        # Détail
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            ### Détail Calcul
            - **Valeur assurée**: {equipment.replacement_value:,.0f} DH
            - **Taux base secteur**: {taux_secteur}%
            - **Prime HT**: {prime_ajustee:,.0f} DH
            - **TVA 20%**: {tva_dh:,.0f} DH
            - **Total TTC**: {total_ttc:,.0f} DH
            
            ### Classe de Risque
            - **Classe**: {classe['nom']}
            - **Score Global**: {result.global_score:.1f}/100
            - **Franchise recommandée**: {classe['franchise_dh']} DH
            """)
        
        with col2:
            # Pie chart
            fig_pie = px.pie(
                names=['Prime HT', 'TVA 20%'],
                values=[prime_ajustee, tva_dh],
                title="Composition Prime (DH)",
                color_discrete_sequence=['#003d5c', '#c69c6d']
            )
            
            st.plotly_chart(fig_pie, use_container_width=True)
        
        # Export
        st.markdown("---")
        
        st.markdown("### 💾 Télécharger Analyse")
        
        rapport_text = f"""
🇲🇦 RAPPORT UNDERWRITING — MAROC
================================

Équipement: {equipment.equipment_id}
Secteur: {secteur_data.get('nom', 'Autre')}
Date: {datetime.now().strftime('%d/%m/%Y %H:%M')}

SCORING
-------
Score Global: {result.global_score:.1f}/100
Risque: {result.risk_level}
Classe: {classe['nom']}

COMPOSANTS
- Robustesse Mécatronique: {result.robustness.score:.0f}/100
- Maturité Maintenance: {result.maintenance.score:.0f}/100
- Gouvernance Technique: {result.governance.score:.0f}/100

PRIME D'ASSURANCE (DH)
--------------------
Valeur assurée: {equipment.replacement_value:,.0f} DH
Taux: {taux_secteur}%
Prime HT: {prime_ajustee:,.0f} DH
TVA 20%: {tva_dh:,.0f} DH
Total TTC: {total_ttc:,.0f} DH

Franchise recommandée: {classe['franchise_dh']} DH

RECOMMANDATIONS
{chr(10).join([f"- {rec}" for rec in result.recommendations])}

Rapport généré par Underwriting Maroc © 2026
"""
        
        st.download_button(
            "📥 Télécharger Rapport (TXT)",
            data=rapport_text,
            file_name=f"underwriting_maroc_{equipment.equipment_id}.txt",
            mime="text/plain",
        )
    
    else:
        st.info("👈 Complétez d'abord le scoring")


# ============================================================
# FOOTER MAROCAIN
# ============================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9em; padding: 20px;">
    <p>🇲🇦 <strong>Underwriting Maroc</strong> | Système de Scoring Industrie 4.0</p>
    <p>Conforme: Code Assurances Maroc | ACPR | Normes ISO</p>
    <p>© 2026 — Version 1.0 | Prototype Confidential</p>
</div>
""", unsafe_allow_html=True)
