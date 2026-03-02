import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Underwriting Analytics Pro", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=Inter:wght@400;500;600;700&family=Poppins:wght@600;700&display=swap');
* { font-family: 'Inter', -apple-system, sans-serif; }
body { background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0f0f22 100%); color: #e8eaed; }
.stApp { background: #0a0e27; }
.header-section { background: linear-gradient(90deg, rgba(13, 27, 42, 0.95) 0%, rgba(31, 47, 72, 0.95) 100%); border-bottom: 1px solid rgba(88, 166, 255, 0.2); padding: 28px 32px; margin: -64px -64px 32px -64px; backdrop-filter: blur(10px); }
.header-title { font-family: 'Poppins', sans-serif; font-size: 28px; font-weight: 700; color: #e8eaed; }
.header-subtitle { font-size: 12px; color: #9aa0a6; margin-top: 4px; text-transform: uppercase; letter-spacing: 1px; }
.card { background: linear-gradient(135deg, rgba(31, 47, 72, 0.4) 0%, rgba(21, 34, 53, 0.3) 100%); border: 1px solid rgba(88, 166, 255, 0.15); border-radius: 12px; padding: 20px; margin-bottom: 16px; transition: all 0.3s; backdrop-filter: blur(8px); }
.card:hover { border-color: rgba(88, 166, 255, 0.4); box-shadow: 0 8px 32px rgba(88, 166, 255, 0.1); }
.score-number { font-family: 'IBM Plex Mono', monospace; font-size: 42px; font-weight: 600; margin: 8px 0; }
.score-label { font-size: 11px; color: #9aa0a6; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px; }
.score-excellent { color: #34c759; }
.score-good { color: #58a6ff; }
.score-warning { color: #fbbf24; }
.score-critical { color: #ef4444; }
.input-section { background: rgba(21, 34, 53, 0.5); border: 1px solid rgba(88, 166, 255, 0.1); border-radius: 12px; padding: 20px; margin-bottom: 16px; }
.section-title { font-size: 12px; color: #9aa0a6; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; margin-bottom: 14px; }
.metric-box { background: rgba(31, 47, 72, 0.3); border-radius: 8px; padding: 12px; text-align: center; border: 1px solid rgba(88, 166, 255, 0.1); }
.metric-value { font-family: 'IBM Plex Mono', monospace; font-size: 20px; font-weight: 600; color: #e8eaed; }
.metric-label { font-size: 9px; color: #9aa0a6; margin-top: 4px; text-transform: uppercase; }
.stButton > button { background: linear-gradient(135deg, #0066cc 0%, #0052a3 100%) !important; border: none !important; color: white !important; font-weight: 600 !important; padding: 12px 24px !important; border-radius: 8px !important; width: 100%; }
.stButton > button:hover { background: linear-gradient(135deg, #0080ff 0%, #0066cc 100%) !important; box-shadow: 0 8px 24px rgba(0, 102, 204, 0.3) !important; }
.breakdown-item { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid rgba(88, 166, 255, 0.1); font-size: 12px; }
.breakdown-label { color: #9aa0a6; }
.breakdown-value { color: #e8eaed; font-weight: 600; }
h1, h2, h3 { color: #e8eaed !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-section"><div><div class="header-title">📊 UNDERWRITING ANALYTICS PRO</div><div class="header-subtitle">Maroc | Industrie 4.0 | 5 Piliers de Scoring</div></div></div>', unsafe_allow_html=True)

col_input, col_output = st.columns([1.3, 2.7])

with col_input:
    st.markdown('<div class="input-section"><div class="section-title">⚙️ Configuration</div>', unsafe_allow_html=True)
    secteur = st.selectbox("Secteur", ["🏭 Textile", "🥕 Agroalimentaire", "⛏️ Mines", "⚗️ Chimie", "🏗️ Construction"])
    preset = st.radio("Scenario", ["Manuel", "Cas A", "Cas B", "Cas C"], horizontal=True)
    
    st.markdown('</div><div class="input-section"><div class="section-title">🎯 Équipement</div>', unsafe_allow_html=True)
    equipment_id = st.text_input("ID Équipement", "EQ-2024-001")
    equipment_type = st.text_input("Type", "Métier automatisé")
    
    col_a, col_b = st.columns(2)
    with col_a:
        replacement_value = st.number_input("Valeur ($k)", value=2500, step=100) * 1000
    with col_b:
        age_years = st.number_input("Âge (ans)", value=3, step=1, min_value=0, max_value=30)
    
    st.markdown('</div><div class="input-section"><div class="section-title">⚡ Performance & IoT</div>', unsafe_allow_html=True)
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
    
    st.markdown('</div><div class="input-section"><div class="section-title">🔧 Maintenance</div>', unsafe_allow_html=True)
    maint_strat = st.selectbox("Stratégie", ["Corrective", "Preventive", "Predictive"])
    gmao = st.checkbox("GMAO Active", value=True)
    training = st.slider("Formation Team (1-5)", 1, 5, 4)
    
    st.markdown('</div><div class="input-section"><div class="section-title">🏗️ Équipements Maintenance</div>', unsafe_allow_html=True)
    tools_modern = st.selectbox("État équipements", ["Ancien/Manuel", "Semi-moderne", "Moderne", "Très moderne"])
    tools_score = {"Ancien/Manuel": 0.3, "Semi-moderne": 0.6, "Moderne": 0.85, "Très moderne": 1.0}[tools_modern]
    lift_safety = st.checkbox("Levage certifiés", value=True)
    diagnostic_tools = st.checkbox("Outils diagnosis avancés", value=True)
    
    st.markdown('</div><div class="input-section"><div class="section-title">📦 Stockage Pièces</div>', unsafe_allow_html=True)
    storage_type = st.selectbox("Système", ["Manuel (fiches)", "Basique (Excel)", "CMMS", "WMS", "Predictive (AI+IoT)"])
    storage_score = {"Manuel (fiches)": 0.2, "Basique (Excel)": 0.4, "CMMS": 0.65, "WMS": 0.85, "Predictive (AI+IoT)": 1.0}[storage_type]
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        stock_coverage = st.slider("Couverture stock (%)", 0, 100, 75)
    with col_s2:
        reorder_efficiency = st.slider("Efficacité recharge (%)", 0, 100, 80)
    
    st.markdown('</div><div class="input-section"><div class="section-title">⚡ Efficacité Intervention</div>', unsafe_allow_html=True)
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        mttr = st.number_input("MTTR (heures)", value=2.5, step=0.5, min_value=0.5, max_value=48.0)
    with col_e2:
        intervention_compliance = st.slider("Respect délais (%)", 0, 100, 85)
    col_e3, col_e4 = st.columns(2)
    with col_e3:
        first_fix_rate = st.slider("Taux réparation 1ère (%)", 0, 100, 92)
    with col_e4:
        tech_availability = st.slider("Dispo techniciens (%)", 0, 100, 95)
    
    st.markdown('</div><div class="input-section"><div class="section-title">💻 Systèmes ERP</div>', unsafe_allow_html=True)
    erp_systems = []
    col1, col2 = st.columns(2)
    with col1:
        if st.checkbox("Papier/Excel"):
            erp_systems.append(("Papier/Excel", 0))
        if st.checkbox("CMMS Basique"):
            erp_systems.append(("CMMS Basique", 1))
        if st.checkbox("SAP/Oracle"):
            erp_systems.append(("SAP/Oracle", 2))
    with col2:
        if st.checkbox("Infor/IFS"):
            erp_systems.append(("Infor/IFS", 3))
        if st.checkbox("Domotic IoT"):
            erp_systems.append(("Domotic IoT", 4))
        if st.checkbox("AI Predictive"):
            erp_systems.append(("AI Predictive", 5))
    
    st.markdown('</div>', unsafe_allow_html=True)
    analyze = st.button("▶ ANALYSER", use_container_width=True)

with col_output:
    if analyze or 'analyzed' in st.session_state:
        st.session_state.analyzed = True
        
        robustness = ((automation * 10 + sensors * 10 + (100 - age_years * 2) + (vib_health * 0.3 + temp_health * 0.3 + elec_health * 0.4)) / 5.5)
        robustness = np.clip(robustness, 0, 100)
        
        maintenance = ((1 if maint_strat == "Predictive" else 0.7 if maint_strat == "Preventive" else 0.3) * 25 + (30 if gmao else 15) + training * 8 + tools_score * 15 + (len(erp_systems) * 2 if erp_systems else 0))
        maintenance = np.clip(maintenance, 0, 100)
        
        governance = np.clip(75 + training * 2 + (15 if maint_strat == "Predictive" else 0), 0, 100)
        
        storage_pillar = np.clip(storage_score * 40 + (stock_coverage / 100) * 30 + (reorder_efficiency / 100) * 30, 0, 100)
        
        mttr_norm = np.clip((24 - mttr) / 24 * 100, 0, 100)
        intervention_pillar = np.clip((mttr_norm + intervention_compliance + first_fix_rate + tech_availability) / 4 * 0.8 + (tools_score * 100) * 0.2, 0, 100)
        
        global_score = robustness * 0.25 + maintenance * 0.30 + governance * 0.15 + storage_pillar * 0.15 + intervention_pillar * 0.15
        
        if global_score >= 75:
            risk_level, risk_color, risk_emoji, classe, franchise, taux = "FAIBLE", "score-excellent", "✅", "Classe 1", "5,000", 0.50
        elif global_score >= 50:
            risk_level, risk_color, risk_emoji, classe, franchise, taux = "MOYEN", "score-good", "⚠️", "Classe 2", "15,000", 0.85
        elif global_score >= 25:
            risk_level, risk_color, risk_emoji, classe, franchise, taux = "ÉLEVÉ", "score-warning", "⚠️⚠️", "Classe 3", "30,000", 1.50
        else:
            risk_level, risk_color, risk_emoji, classe, franchise, taux = "TRÈS ÉLEVÉ", "score-critical", "🔴", "Classe 4", "50,000", 2.50
        
        prime_ht = replacement_value * (taux / 100)
        tva = prime_ht * 0.20
        total_ttc = prime_ht + tva
        
        st.markdown(f'<div class="card" style="grid-column: 1 / -1; text-align: center;"><div class="score-label">SCORE GLOBAL</div><div class="score-number {risk_color}">{global_score:.1f}/100</div><div style="font-size: 13px; color: #e8eaed;">{risk_emoji} {risk_level} | {classe}</div></div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'<div class="card"><div class="score-label">🔧 Robustesse (25%)</div><div class="score-number score-good">{robustness:.0f}</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="card"><div class="score-label">🎯 Maintenance (30%)</div><div class="score-number score-good">{maintenance:.0f}</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="card"><div class="score-label">📋 Gouvernance (15%)</div><div class="score-number score-excellent">{governance:.0f}</div></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'<div class="card"><div class="score-label">📦 Stockage (15%)</div><div class="score-number score-good">{storage_pillar:.0f}</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="card"><div class="score-label">⚡ Efficacité (15%)</div><div class="score-number score-good">{intervention_pillar:.0f}</div></div>', unsafe_allow_html=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'<div class="card"><div class="score-label">Classification</div><div style="font-size: 28px; font-weight: 600; color: #e8eaed;">{classe}</div><div class="breakdown-item"><span class="breakdown-label">Franchise:</span><span class="breakdown-value">{franchise} DH</span></div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="card"><div class="score-label">Prime Annuelle</div><div style="font-size: 28px; font-weight: 600; color: #34c759;">{total_ttc:,.0f} DH</div><div class="breakdown-item"><span class="breakdown-label">Taux:</span><span class="breakdown-value">{taux:.2f}%</span></div></div>', unsafe_allow_html=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'<div class="card"><div class="score-label">📦 Stockage</div><div class="breakdown-item"><span class="breakdown-label">Système:</span><span class="breakdown-value">{storage_type}</span></div><div class="breakdown-item"><span class="breakdown-label">Couverture:</span><span class="breakdown-value">{stock_coverage}%</span></div><div class="breakdown-item"><span class="breakdown-label">Score:</span><span class="breakdown-value">{storage_pillar:.0f}/100</span></div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="card"><div class="score-label">💻 ERP</div>', unsafe_allow_html=True)
            if erp_systems:
                erp_sorted = sorted(erp_systems, key=lambda x: x[1])
                for sys, level in erp_sorted:
                    evolution = ["L0: Aucune", "L1: Basique", "L2: Intermédiaire", "L3: Avancée", "L4: Intelligence", "L5: IA"][level]
                    st.markdown(f'<div class="breakdown-item"><span class="breakdown-label">{sys}</span><span class="breakdown-value">{evolution}</span></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div style="color: #9aa0a6; font-size: 11px;">Aucun système</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        st.markdown(f'<div class="card"><div class="score-label">⚡ Efficacité Intervention</div><div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 8px;"><div class="metric-box"><div class="metric-label">MTTR</div><div class="metric-value">{mttr:.1f}h</div></div><div class="metric-box"><div class="metric-label">Délais</div><div class="metric-value">{intervention_compliance}%</div></div><div class="metric-box"><div class="metric-label">1ère fois</div><div class="metric-value">{first_fix_rate}%</div></div><div class="metric-box"><div class="metric-label">Dispo</div><div class="metric-value">{tech_availability}%</div></div></div><div style="margin-top: 12px; padding-top: 12px; border-top: 1px solid rgba(88, 166, 255, 0.1);"><div class="breakdown-item"><span class="breakdown-label">Score:</span><span class="breakdown-value">{intervention_pillar:.0f}/100</span></div></div></div>', unsafe_allow_html=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        fig_radar = go.Figure(data=go.Scatterpolar(
            r=[robustness, maintenance, governance, storage_pillar, intervention_pillar],
            theta=['Robustesse', 'Maintenance', 'Gouvernance', 'Stockage', 'Efficacité'],
            fill='toself',
            line=dict(color='#0066cc'),
            fillcolor='rgba(0, 102, 204, 0.25)'
        ))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100], gridcolor='rgba(88, 166, 255, 0.1)'), bgcolor='transparent'), font=dict(size=10, color='#9aa0a6'), paper_bgcolor='rgba(31, 47, 72, 0.3)', plot_bgcolor='transparent', height=350, showlegend=False)
        st.plotly_chart(fig_radar, use_container_width=True, config={'displayModeBar': False})
        
    else:
        st.markdown('<div style="text-align: center; padding: 80px 40px; color: #9aa0a6;"><div style="font-size: 32px;">📊</div><div style="font-size: 16px;">Prêt à analyser</div></div>', unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown('<div style="text-align: center; font-size: 10px; color: #6e7681; padding: 16px;">UNDERWRITING ANALYTICS PRO v3.2 | Maroc © 2026</div>', unsafe_allow_html=True)
