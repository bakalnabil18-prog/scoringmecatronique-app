import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# ============================================================
# CONFIG STREAMLIT
# ============================================================
st.set_page_config(
    page_title="Underwriting Analytics Pro",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# DESIGN PROFESSIONNEL ENTERPRISE
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=Inter:wght@400;500;600;700&family=Poppins:wght@600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, sans-serif;
    }
    
    body {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0f0f22 100%);
        color: #e8eaed;
    }
    
    .stApp {
        background: #0a0e27;
    }
    
    /* HEADER */
    .header-section {
        background: linear-gradient(90deg, rgba(13, 27, 42, 0.95) 0%, rgba(31, 47, 72, 0.95) 100%);
        border-bottom: 1px solid rgba(88, 166, 255, 0.2);
        padding: 28px 32px;
        margin: -64px -64px 32px -64px;
        backdrop-filter: blur(10px);
    }
    
    .header-title {
        font-family: 'Poppins', sans-serif;
        font-size: 28px;
        font-weight: 700;
        color: #e8eaed;
    }
    
    .header-subtitle {
        font-size: 12px;
        color: #9aa0a6;
        margin-top: 4px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* CARD */
    .card {
        background: linear-gradient(135deg, rgba(31, 47, 72, 0.4) 0%, rgba(21, 34, 53, 0.3) 100%);
        border: 1px solid rgba(88, 166, 255, 0.15);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
        transition: all 0.3s;
        backdrop-filter: blur(8px);
    }
    
    .card:hover {
        border-color: rgba(88, 166, 255, 0.4);
        box-shadow: 0 8px 32px rgba(88, 166, 255, 0.1);
    }
    
    /* SCORE */
    .score-display {
        text-align: center;
        padding: 16px;
    }
    
    .score-number {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 42px;
        font-weight: 600;
        margin: 8px 0;
    }
    
    .score-label {
        font-size: 11px;
        color: #9aa0a6;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 12px;
    }
    
    .score-excellent { color: #34c759; }
    .score-good { color: #58a6ff; }
    .score-warning { color: #fbbf24; }
    .score-critical { color: #ef4444; }
    
    /* INPUT */
    .input-section {
        background: rgba(21, 34, 53, 0.5);
        border: 1px solid rgba(88, 166, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
    }
    
    .section-title {
        font-size: 12px;
        color: #9aa0a6;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
        margin-bottom: 14px;
    }
    
    /* METRIC BOX */
    .metric-box {
        background: rgba(31, 47, 72, 0.3);
        border-radius: 8px;
        padding: 12px;
        text-align: center;
        border: 1px solid rgba(88, 166, 255, 0.1);
    }
    
    .metric-value {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 20px;
        font-weight: 600;
        color: #e8eaed;
    }
    
    .metric-label {
        font-size: 9px;
        color: #9aa0a6;
        margin-top: 4px;
        text-transform: uppercase;
    }
    
    /* BUTTON */
    .stButton > button {
        background: linear-gradient(135deg, #0066cc 0%, #0052a3 100%) !important;
        border: none !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 12px 24px !important;
        border-radius: 8px !important;
        width: 100%;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #0080ff 0%, #0066cc 100%) !important;
        box-shadow: 0 8px 24px rgba(0, 102, 204, 0.3) !important;
    }
    
    /* TABS */
    .stTabs [aria-selected="true"] {
        border-bottom: 2px solid #0066cc !important;
    }
    
    /* INPUT/SELECT */
    [data-baseweb="input"], [data-baseweb="select"] {
        background-color: rgba(31, 47, 72, 0.3) !important;
        border-color: rgba(88, 166, 255, 0.15) !important;
        color: #e8eaed !important;
    }
    
    h1, h2, h3 { color: #e8eaed !important; }
    
    /* BREAKDOWN TABLE */
    .breakdown-item {
        display: flex;
        justify-content: space-between;
        padding: 8px 0;
        border-bottom: 1px solid rgba(88, 166, 255, 0.1);
        font-size: 12px;
    }
    
    .breakdown-label { color: #9aa0a6; }
    .breakdown-value { color: #e8eaed; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================
st.markdown("""
<div class="header-section">
    <div>
        <div class="header-title">📊 UNDERWRITING ANALYTICS PRO</div>
        <div class="header-subtitle">Maroc | Industrie 4.0 | Scoring Avancé + ERP + Stockage</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# LAYOUT PRINCIPAL
# ============================================================
col_input, col_output = st.columns([1.3, 2.7])

# ============================================================
# COLONNE GAUCHE — INPUTS COMPLETS
# ============================================================
with col_input:
    
    # SECTION 1: CONFIGURATION DE BASE
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">⚙️ Configuration</div>', unsafe_allow_html=True)
    
    secteur = st.selectbox("Secteur", ["🏭 Textile", "🥕 Agroalimentaire", "⛏️ Mines", "⚗️ Chimie", "🏗️ Construction"])
    preset = st.radio("Scenario", ["Manuel", "Cas A (Faible)", "Cas B (Moyen)", "Cas C (Élevé)"], horizontal=True)
    
    st.markdown('</div><div class="input-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🎯 Équipement</div>', unsafe_allow_html=True)
    
    equipment_id = st.text_input("ID Équipement", "EQ-2024-001")
    equipment_type = st.text_input("Type", "Métier automatisé")
    col_a, col_b = st.columns(2)
    with col_a:
        replacement_value = st.number_input("Valeur ($k)", 2500, step=100) * 1000
    with col_b:
        age_years = st.number_input("Âge (ans)", 3, step=1, min_value=0, max_value=30)
    
    # SECTION 2: PERFORMANCE & CAPTEURS
    st.markdown('</div><div class="input-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">⚡ Performance & IoT</div>', unsafe_allow_html=True)
    
    mtbf = st.slider("MTBF (heures)", 5000, 100000, 50000, step=5000)
    automation = st.select_slider("Automatisation", [1, 2, 3, 4], value=4)
    sensors = st.select_slider("Capteurs IoT", [1, 2, 3, 4], value=4)
    
    col_v, col_t, col_e = st.columns(3)
    with col_v:
        vib_health = st.slider("Vibration", 0, 100, 90)
    with col_t:
        temp_health = st.slider("Température", 0, 100, 88)
    with col_e:
        elec_health = st.slider("Électrique", 0, 100, 92)
    
    # SECTION 3: MAINTENANCE STRATÉGIE
    st.markdown('</div><div class="input-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🔧 Maintenance</div>', unsafe_allow_html=True)
    
    maint_strat = st.selectbox("Stratégie", ["Corrective", "Preventive", "Predictive"])
    gmao = st.checkbox("GMAO Active", value=True)
    training = st.slider("Formation Team (1-5)", 1, 5, 4)
    
    # SECTION 4: ÉQUIPEMENTS DE MANUTENTION & MAINTENANCE
    st.markdown('</div><div class="input-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🏗️ Équipements Maintenance</div>', unsafe_allow_html=True)
    
    st.caption("Équipements utilisés pour la manutention et intervention")
    
    tools_modern = st.selectbox(
        "État équipements maintenance",
        ["Ancien/Manuel", "Semi-moderne", "Moderne", "Très moderne (Robotisé)"],
        help="État des outils, appareils de levage, équipements manutention"
    )
    
    tools_score = {"Ancien/Manuel": 0.3, "Semi-moderne": 0.6, "Moderne": 0.85, "Très moderne (Robotisé)": 1.0}[tools_modern]
    
    lift_safety = st.checkbox("Équipements levage certifiés", value=True)
    diagnostic_tools = st.checkbox("Outils diagnostic avancés", value=True)
    
    # SECTION 5: SYSTÈMES ERP & HISTORIQUE
    st.markdown('</div><div class="input-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">💻 Systèmes ERP</div>', unsafe_allow_html=True)
    
    st.caption("Sélectionnez les systèmes en usage (ordre évolution)")
    
    erp_systems = []
    col1, col2 = st.columns(2)
    
    with col1:
        if st.checkbox("Papier/Excel", value=False):
            erp_systems.append(("Papier/Excel", 0))
        if st.checkbox("CMMS Basique", value=False):
            erp_systems.append(("CMMS Basique", 1))
        if st.checkbox("SAP/Oracle", value=False):
            erp_systems.append(("SAP/Oracle", 2))
    
    with col2:
        if st.checkbox("Infor/IFS", value=False):
            erp_systems.append(("Infor/IFS", 3))
        if st.checkbox("Domotic IoT", value=False):
            erp_systems.append(("Domotic IoT", 4))
        if st.checkbox("AI Predictive", value=False):
            erp_systems.append(("AI Predictive", 5))
    
    # SECTION 6: STOCKAGE & PIÈCES DÉTACHÉES
    st.markdown('</div><div class="input-section">', uppercase_heading=True)
    st.markdown('<div class="section-title">📦 Stockage Pièces Détachées</div>', unsafe_allow_html=True)
    
    st.caption("Gestion du stock et système de recharge")
    
    storage_type = st.selectbox(
        "Système de stockage",
        ["Manuel (fiches)", "Basique (Excel)", "Logiciel CMMS", "Automatisé (WMS)", "Predictive (AI+IoT)"],
        help="Système de gestion des stocks"
    )
    
    storage_score = {
        "Manuel (fiches)": 0.2,
        "Basique (Excel)": 0.4,
        "Logiciel CMMS": 0.65,
        "Automatisé (WMS)": 0.85,
        "Predictive (AI+IoT)": 1.0
    }[storage_type]
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        stock_coverage = st.slider("Couverture stock (%)", 0, 100, 75, help="% de pièces critiques en stock")
    with col_s2:
        reorder_efficiency = st.slider("Efficacité recharge (%)", 0, 100, 80, help="% de recharges à temps")
    
    # SECTION 7: EFFICACITÉ INTERVENTION
    st.markdown('</div><div class="input-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">⚡ Efficacité Intervention</div>', unsafe_allow_html=True)
    
    st.caption("Métriques de performance des interventions")
    
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        mttr = st.number_input("MTTR (heures)", 0.5, 48.0, 2.5, step=0.5, help="Mean Time To Repair")
    with col_e2:
        intervention_compliance = st.slider("Respect délais (%)", 0, 100, 85)
    
    col_e3, col_e4 = st.columns(2)
    with col_e3:
        first_fix_rate = st.slider("Taux réparation 1ère (%) ", 0, 100, 92, help="% réparations réussies au 1er essai")
    with col_e4:
        tech_availability = st.slider("Dispo techniciens (%)", 0, 100, 95)
    
    # BUTTON ANALYZE
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div style="margin-top: 20px;"></div>', unsafe_allow_html=True)
    analyze = st.button("▶ ANALYSER COMPLÈTEMENT", use_container_width=True)


# ============================================================
# COLONNE DROITE — RÉSULTATS COMPLETS
# ============================================================
with col_output:
    
    if analyze or 'analyzed' in st.session_state:
        st.session_state.analyzed = True
        
        # ============================================================
        # CALCUL DES SCORES AVANCÉS
        # ============================================================
        
        # 1. ROBUSTESSE (35%)
        robustness = (
            automation * 10 +
            sensors * 10 +
            (100 - age_years * 2) +
            (vib_health * 0.3 + temp_health * 0.3 + elec_health * 0.4)
        ) / 5.5
        robustness = np.clip(robustness, 0, 100)
        
        # 2. MAINTENANCE (45%)
        maint_base = (1 if maint_strat == "Predictive" else 0.7 if maint_strat == "Preventive" else 0.3) * 25
        maint_gmao = (30 if gmao else 15)
        maint_training = training * 8
        maint_equipment = tools_score * 15  # Score équipements
        maint_erp = (len(erp_systems) * 2) if erp_systems else 0  # ERP evolution
        
        maintenance = maint_base + maint_gmao + maint_training + maint_equipment + maint_erp
        maintenance = np.clip(maintenance, 0, 100)
        
        # 3. GOUVERNANCE (20%)
        governance = 75 + (training * 2) + (15 if maint_strat == "Predictive" else 0)
        governance = np.clip(governance, 0, 100)
        
        # 4. STOCKAGE & SUPPLY CHAIN (15%) — NOUVEAU PILIER
        storage_base = storage_score * 40
        storage_coverage_score = (stock_coverage / 100) * 30
        storage_efficiency = (reorder_efficiency / 100) * 30
        
        storage_pillar = storage_base + storage_coverage_score + storage_efficiency
        storage_pillar = np.clip(storage_pillar, 0, 100)
        
        # 5. EFFICACITÉ INTERVENTION (15%) — NOUVEAU PILIER
        mttr_norm = np.clip((24 - mttr) / 24 * 100, 0, 100)  # Normalisé
        intervention_base = (mttr_norm + intervention_compliance + first_fix_rate + tech_availability) / 4
        
        intervention_pillar = intervention_base * 0.8 + (tools_score * 100) * 0.2  # Équipements influent
        intervention_pillar = np.clip(intervention_pillar, 0, 100)
        
        # SCORE GLOBAL — PONDÉRATION FINALE
        global_score = (
            robustness * 0.25 +      # 25% (au lieu de 35%)
            maintenance * 0.30 +      # 30% (au lieu de 45%)
            governance * 0.15 +       # 15% (au lieu de 20%)
            storage_pillar * 0.15 +   # 15% NOUVEAU
            intervention_pillar * 0.15 # 15% NOUVEAU
        )
        
        # ============================================================
        # DÉTERMINATION DU RISQUE
        # ============================================================
        
        if global_score >= 75:
            risk_level = "FAIBLE"
            risk_color = "score-excellent"
            risk_emoji = "✅"
            classe = "Classe 1"
            franchise = "5,000"
            taux = 0.50
        elif global_score >= 50:
            risk_level = "MOYEN"
            risk_color = "score-good"
            risk_emoji = "⚠️"
            classe = "Classe 2"
            franchise = "15,000"
            taux = 0.85
        elif global_score >= 25:
            risk_level = "ÉLEVÉ"
            risk_color = "score-warning"
            risk_emoji = "⚠️ ⚠️"
            classe = "Classe 3"
            franchise = "30,000"
            taux = 1.50
        else:
            risk_level = "TRÈS ÉLEVÉ"
            risk_color = "score-critical"
            risk_emoji = "🔴"
            classe = "Classe 4"
            franchise = "50,000"
            taux = 2.50
        
        # Calculs financiers
        prime_ht = replacement_value * (taux / 100)
        tva = prime_ht * 0.20
        total_ttc = prime_ht + tva
        
        # ============================================================
        # AFFICHAGE — KPI PRINCIPAL (5 PILIERS)
        # ============================================================
        
        st.markdown("""
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 20px;">
        """, unsafe_allow_html=True)
        
        # Score global (span 2)
        st.markdown(f"""
        <div class="card" style="grid-column: 1 / -1;">
            <div class="score-display">
                <div class="score-label">SCORE GLOBAL</div>
                <div class="score-number {risk_color}">{global_score:.1f}/100</div>
                <div style="font-size: 13px; color: #e8eaed; margin-top: 8px;">{risk_emoji} {risk_level} | {classe}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 5 Piliers
        pillars = [
            ("🔧 Robustesse", robustness, "25%", "score-good"),
            ("🎯 Maintenance", maintenance, "30%", "score-good"),
            ("📋 Gouvernance", governance, "15%", "score-excellent"),
            ("📦 Stockage/Supply", storage_pillar, "15%", "score-good"),
            ("⚡ Efficacité", intervention_pillar, "15%", "score-good"),
        ]
        
        for i, (label, score, weight, color) in enumerate(pillars):
            if i % 2 == 0:
                st.markdown('<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">', unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="card">
                <div class="score-label">{label}</div>
                <div class="score-number {color}">{score:.0f}</div>
                <div style="font-size: 10px; color: #9aa0a6;">{weight}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if (i + 1) % 2 == 0 or i == len(pillars) - 1:
                st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # ============================================================
        # CLASSIFICATION & PRIME
        # ============================================================
        
        col_class, col_prime = st.columns(2)
        
        with col_class:
            st.markdown(f"""
            <div class="card">
                <div class="score-label">Classification</div>
                <div style="font-size: 28px; font-weight: 600; color: #e8eaed; margin: 8px 0;">{classe}</div>
                <div class="breakdown-item">
                    <span class="breakdown-label">Franchise:</span>
                    <span class="breakdown-value">{franchise} DH</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_prime:
            st.markdown(f"""
            <div class="card">
                <div class="score-label">Prime Annuelle</div>
                <div style="font-size: 28px; font-weight: 600; color: #34c759; margin: 8px 0;">{total_ttc:,.0f} DH</div>
                <div class="breakdown-item">
                    <span class="breakdown-label">Taux:</span>
                    <span class="breakdown-value">{taux:.2f}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # ============================================================
        # DÉTAILS STOCKAGE & ERP
        # ============================================================
        
        st.markdown("<hr style='margin: 16px 0; border-color: rgba(88, 166, 255, 0.1);'>", unsafe_allow_html=True)
        
        col_storage, col_erp = st.columns(2)
        
        with col_storage:
            st.markdown(f"""
            <div class="card">
                <div class="score-label">📦 Stockage Détails</div>
                <div class="breakdown-item">
                    <span class="breakdown-label">Système:</span>
                    <span class="breakdown-value">{storage_type}</span>
                </div>
                <div class="breakdown-item">
                    <span class="breakdown-label">Couverture:</span>
                    <span class="breakdown-value">{stock_coverage}%</span>
                </div>
                <div class="breakdown-item">
                    <span class="breakdown-label">Efficacité:</span>
                    <span class="breakdown-value">{reorder_efficiency}%</span>
                </div>
                <div class="breakdown-item">
                    <span class="breakdown-label">Score Pilier:</span>
                    <span class="breakdown-value">{storage_pillar:.0f}/100</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_erp:
            st.markdown(f"""
            <div class="card">
                <div class="score-label">💻 ERP & Systèmes</div>
            """, unsafe_allow_html=True)
            
            if erp_systems:
                # Sort by evolution level
                erp_sorted = sorted(erp_systems, key=lambda x: x[1])
                erp_text = " → ".join([sys[0] for sys in erp_sorted])
                st.markdown(f"""
                <div style="font-size: 11px; color: #58a6ff; margin: 8px 0; font-family: 'IBM Plex Mono';">
                    {erp_text}
                </div>
                """, unsafe_allow_html=True)
                
                for sys, level in erp_sorted:
                    evolution = ["Aucune", "Basique", "Intermédiaire", "Avancée", "Intelligence", "IA/Prédiction"][level]
                    st.markdown(f"""
                    <div class="breakdown-item">
                        <span class="breakdown-label">{sys}</span>
                        <span class="breakdown-value">L{level+1}: {evolution}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown('<div style="color: #9aa0a6; font-size: 11px;">Aucun système configuré</div>', unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # ============================================================
        # EFFICACITÉ INTERVENTION DÉTAIL
        # ============================================================
        
        st.markdown("<hr style='margin: 16px 0; border-color: rgba(88, 166, 255, 0.1);'>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="card">
            <div class="score-label">⚡ Efficacité Intervention</div>
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 8px;">
                <div class="metric-box">
                    <div class="metric-label">MTTR</div>
                    <div class="metric-value">{mttr:.1f}h</div>
                </div>
                <div class="metric-box">
                    <div class="metric-label">Respect délais</div>
                    <div class="metric-value">{intervention_compliance}%</div>
                </div>
                <div class="metric-box">
                    <div class="metric-label">Taux réparation 1ère</div>
                    <div class="metric-value">{first_fix_rate}%</div>
                </div>
                <div class="metric-box">
                    <div class="metric-label">Dispo Tech</div>
                    <div class="metric-value">{tech_availability}%</div>
                </div>
            </div>
            <div style="margin-top: 12px; padding-top: 12px; border-top: 1px solid rgba(88, 166, 255, 0.1);">
                <div class="breakdown-item">
                    <span class="breakdown-label">Score Pilier:</span>
                    <span class="breakdown-value">{intervention_pillar:.0f}/100</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # ============================================================
        # GRAPHIQUE RADAR — 5 PILIERS
        # ============================================================
        
        st.markdown("<hr style='margin: 16px 0; border-color: rgba(88, 166, 255, 0.1);'>", unsafe_allow_html=True)
        
        fig_radar = go.Figure(data=go.Scatterpolar(
            r=[robustness, maintenance, governance, storage_pillar, intervention_pillar],
            theta=['Robustesse', 'Maintenance', 'Gouvernance', 'Stockage', 'Efficacité'],
            fill='toself',
            line=dict(color='#0066cc'),
            fillcolor='rgba(0, 102, 204, 0.25)'
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], gridcolor='rgba(88, 166, 255, 0.1)'),
                bgcolor='transparent',
                angularaxis=dict(gridcolor='rgba(88, 166, 255, 0.1)')
            ),
            font=dict(size=10, color='#9aa0a6'),
            paper_bgcolor='rgba(31, 47, 72, 0.3)',
            plot_bgcolor='transparent',
            height=400,
            margin=dict(l=50, r=50, t=50, b=50),
            showlegend=False
        )
        
        st.plotly_chart(fig_radar, use_container_width=True, config={'displayModeBar': False})
        
        # ============================================================
        # RECOMMANDATIONS FINALES
        # ============================================================
        
        st.markdown("<hr style='margin: 16px 0; border-color: rgba(88, 166, 255, 0.1);'>", unsafe_allow_html=True)
        st.markdown('<div class="section-title">💡 Recommandations Prioritaires</div>', unsafe_allow_html=True)
        
        recs = []
        
        if storage_pillar < 60:
            recs.append(("🔴 Système stockage", "Migrer vers WMS/Predictive pour optimiser couverture stock"))
        
        if intervention_pillar < 70:
            recs.append(("🔴 Efficacité intervention", f"MTTR={mttr}h | Target: <2h. Augmenter dispo techniciens"))
        
        if len(erp_systems) < 2:
            recs.append(("⚠️ ERP & Systèmes", "Intégrer CMMS avancé ou migrate SAP pour meilleur suivi"))
        
        if maint_strat != "Predictive":
            recs.append(("⚠️ Maintenance", "Déployer maintenance prédictive (capteurs IoT existants)"))
        
        if global_score >= 75:
            recs.insert(0, ("✅ Excellent", "Maintenir configurations actuelles - ROI: +45%"))
        
        for icon, rec in recs[:5]:  # Top 5
            st.markdown(f"""
            <div style="background: rgba(31, 47, 72, 0.3); border-left: 3px solid #0066cc; padding: 12px; margin-bottom: 8px; border-radius: 6px; font-size: 12px;">
                <strong>{icon}</strong><br/>{rec}
            </div>
            """, unsafe_allow_html=True)
    
    else:
        st.markdown("""
        <div style="text-align: center; padding: 80px 40px; color: #9aa0a6;">
            <div style="font-size: 32px; margin-bottom: 16px;">📊</div>
            <div style="font-size: 16px; margin-bottom: 8px;">Prêt à analyser en détail</div>
            <div style="font-size: 12px;">Remplissez tous les critères (équipements, stockage, ERP, efficacité)</div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# FOOTER
# ============================================================
st.markdown("<hr style='margin: 24px 0; border-color: rgba(88, 166, 255, 0.1);'>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; font-size: 10px; color: #6e7681; padding: 16px 0;">
    UNDERWRITING ANALYTICS PRO v3.0 | Maroc © 2026 | Production
    <br/>Scoring: Robustesse (25%) • Maintenance (30%) • Gouvernance (15%) • Stockage (15%) • Efficacité (15%)
</div>
""", unsafe_allow_html=True)
