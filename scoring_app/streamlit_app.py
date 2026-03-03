import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# ============================================================
# CONFIG & DESIGN
# ============================================================
st.set_page_config(
    page_title="Underwriting Maroc — 8 Modules",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=Inter:wght@400;500;600;700&family=Poppins:wght@600;700&display=swap');
* { font-family: 'Inter', -apple-system, sans-serif; }
body { background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0f0f22 100%); color: #e8eaed; }
.stApp { background: #0a0e27; }
.header-section { background: linear-gradient(90deg, rgba(13, 27, 42, 0.95) 0%, rgba(31, 47, 72, 0.95) 100%); border-bottom: 1px solid rgba(88, 166, 255, 0.2); padding: 24px 32px; margin: -64px -64px 32px -64px; }
.header-title { font-family: 'Poppins', sans-serif; font-size: 26px; font-weight: 700; color: #e8eaed; }
.header-subtitle { font-size: 12px; color: #9aa0a6; margin-top: 4px; text-transform: uppercase; letter-spacing: 1px; }
.card { background: linear-gradient(135deg, rgba(31, 47, 72, 0.4) 0%, rgba(21, 34, 53, 0.3) 100%); border: 1px solid rgba(88, 166, 255, 0.15); border-radius: 12px; padding: 18px; margin-bottom: 12px; transition: all 0.3s; }
.card:hover { border-color: rgba(88, 166, 255, 0.4); box-shadow: 0 8px 32px rgba(88, 166, 255, 0.1); }
.score-number { font-family: 'IBM Plex Mono', monospace; font-size: 36px; font-weight: 600; margin: 8px 0; }
.score-label { font-size: 11px; color: #9aa0a6; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }
.score-excellent { color: #34c759; }
.score-good { color: #58a6ff; }
.score-warning { color: #fbbf24; }
.score-critical { color: #ef4444; }
.input-section { background: rgba(21, 34, 53, 0.5); border: 1px solid rgba(88, 166, 255, 0.1); border-radius: 12px; padding: 18px; margin-bottom: 14px; }
.section-title { font-size: 12px; color: #9aa0a6; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; margin-bottom: 12px; }
.metric-box { background: rgba(31, 47, 72, 0.3); border-radius: 8px; padding: 12px; text-align: center; border: 1px solid rgba(88, 166, 255, 0.1); }
.metric-value { font-family: 'IBM Plex Mono', monospace; font-size: 18px; font-weight: 600; color: #e8eaed; }
.metric-label { font-size: 9px; color: #9aa0a6; margin-top: 4px; text-transform: uppercase; }
.stButton > button { background: linear-gradient(135deg, #0066cc 0%, #0052a3 100%) !important; border: none !important; color: white !important; font-weight: 600 !important; padding: 12px 24px !important; border-radius: 8px !important; width: 100%; }
.stButton > button:hover { background: linear-gradient(135deg, #0080ff 0%, #0066cc 100%) !important; box-shadow: 0 8px 24px rgba(0, 102, 204, 0.3) !important; }
.breakdown-item { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid rgba(88, 166, 255, 0.1); font-size: 12px; }
.breakdown-label { color: #9aa0a6; }
.breakdown-value { color: #e8eaed; font-weight: 600; }
h1, h2, h3 { color: #e8eaed !important; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================
st.markdown("""
<div class="header-section">
    <div class="header-title">📊 UNDERWRITING MAROC — 8 Modules</div>
    <div class="header-subtitle">Robots • CNC • CPS • Infrastructure • Maintenance • Stockage • RH • Cyber</div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# DÉFINITION DES 8 MODULES
# ============================================================
MODULES = {
    "robots": {
        "label": "🤖 Robots Industriels",
        "weight": 0.18,
        "description": "Automatisation, cobots, redondance, maintenance",
        "metrics": ["Type robot", "Nombre", "MTBF", "Redondance", "Contrat maintenance"]
    },
    "cnc": {
        "label": "⚙️ Machines CNC",
        "weight": 0.14,
        "description": "Usinage, automatisation, refroidissement, protections",
        "metrics": ["Type CNC", "Nombre", "Automatisation", "Maintenance préventive", "Protections électriques"]
    },
    "cps": {
        "label": "🌐 Systèmes Cyber-Physique",
        "weight": 0.18,
        "description": "SCADA, MES, ERP, intégration digitale",
        "metrics": ["SCADA", "MES", "ERP", "Segmentation réseau", "Backup"]
    },
    "infra": {
        "label": "⚡ Infrastructure Électrique",
        "weight": 0.12,
        "description": "Alimentation, secours, harmonique, continuité",
        "metrics": ["Tension primaire", "Générateur secours", "Onduleur", "THD", "Protection"]
    },
    "maint": {
        "label": "🔧 Maintenance & GMAO",
        "weight": 0.14,
        "description": "Stratégie, GMAO, prédictive, formations",
        "metrics": ["Stratégie", "GMAO", "Prédictive", "Formation", "MTTR"]
    },
    "stock": {
        "label": "📦 Stockage & Supply Chain",
        "weight": 0.12,
        "description": "Stocks, pièces critiques, logistique, MRP",
        "metrics": ["Système stockage", "Couverture", "Efficacité recharge", "Supplier agreement"]
    },
    "rh": {
        "label": "👥 Ressources Humaines",
        "weight": 0.06,
        "description": "Formations, certifications, turnover, expertise",
        "metrics": ["Formation/an", "Certifications", "Expertise", "Turnover"]
    },
    "cyber": {
        "label": "🔒 Cybersécurité & Continuité",
        "weight": 0.06,
        "description": "Sécurité, cyber, PCA, audit, incidents",
        "metrics": ["Pare-feu", "Audit cyber", "PCA", "Incidents", "Recovery time"]
    }
}

# ============================================================
# LAYOUT PRINCIPAL
# ============================================================
col_input, col_output = st.columns([1.3, 2.7])

# ============================================================
# COLONNE GAUCHE — INPUTS
# ============================================================
with col_input:
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">⚙️ Configuration</div>', unsafe_allow_html=True)
    
    entreprise = st.text_input("Entreprise", "Votre Société")
    secteur = st.selectbox(
        "Secteur",
        ["🏭 Textile", "🥕 Agroalimentaire", "⛏️ Mines", "⚗️ Chimie", "🏗️ Construction", "⚡ Énergie"]
    )
    preset = st.radio("Scenario", ["Manuel", "Cas A (Faible)", "Cas B (Moyen)", "Cas C (Élevé)"], horizontal=True)
    
    st.markdown('</div><div class="input-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📋 Équipement</div>', unsafe_allow_html=True)
    
    equipment_id = st.text_input("ID Équipement", "EQ-2024-001")
    equipment_type = st.text_input("Type", "Machine automatisée")
    
    col_a, col_b = st.columns(2)
    with col_a:
        replacement_value = st.number_input("Valeur (MAD)", value=2500000, step=100000)
    with col_b:
        age_years = st.number_input("Âge (ans)", value=3, step=1, min_value=0, max_value=30)
    
    # ============================================================
    # TABS POUR CHAQUE MODULE
    # ============================================================
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📊 Modules (8)</div>', unsafe_allow_html=True)
    
    tabs = st.tabs([m["label"] for m in MODULES.values()])
    
    scores_input = {}
    
    # MODULE 1: ROBOTS
    with tabs[0]:
        st.markdown("#### 🤖 Robots Industriels")
        type_robot = st.selectbox("Type", ["6 axes", "5 axes", "SCARA", "Delta"], key="robots_type")
        cobots = st.checkbox("Cobots présents", value=True, key="robots_cobots")
        nombre_robots = st.slider("Nombre total", 1, 50, 5, key="robots_nombre")
        mtbf_robots = st.number_input("MTBF (heures)", value=50000, step=1000, key="robots_mtbf")
        redondance = st.select_slider("Redondance", ["Faible", "Moyen", "Élevé"], value="Moyen", key="robots_redond")
        contrat_maint = st.checkbox("Contrat maintenance constructeur", value=True, key="robots_contrat")
        scores_input["robots"] = (85 if contrat_maint else 60) + (10 if cobots else 0)
    
    # MODULE 2: CNC
    with tabs[1]:
        st.markdown("#### ⚙️ Machines CNC")
        type_cnc = st.selectbox("Type CNC", ["3 axes", "5 axes", "Multi-broche"], key="cnc_type")
        nombre_cnc = st.slider("Nombre total", 1, 30, 3, key="cnc_nombre")
        auto_cnc = st.select_slider("Automatisation", ["Manuel", "Semi-auto", "Full auto"], value="Semi-auto", key="cnc_auto")
        freq_maint_cnc = st.select_slider("Fréquence maintenance", ["Aucune", "Annuelle", "Semestrielle", "Trimestrielle", "Mensuelle"], value="Mensuelle", key="cnc_freq")
        protection_elec = st.checkbox("Protection surtension", value=True, key="cnc_prot")
        scores_input["cnc"] = 75 + (20 if freq_maint_cnc in ["Mensuelle", "Trimestrielle"] else 0)
    
    # MODULE 3: CPS
    with tabs[2]:
        st.markdown("#### 🌐 Systèmes Cyber-Physique")
        scada = st.checkbox("SCADA présent", value=True, key="cps_scada")
        mes = st.checkbox("MES intégré", value=True, key="cps_mes")
        erp = st.checkbox("ERP connecté", value=False, key="cps_erp")
        cloud = st.checkbox("Cloud externe", value=False, key="cps_cloud")
        segmentation = st.select_slider("Segmentation réseau", ["Faible", "Moyenne", "Élevée"], value="Moyenne", key="cps_seg")
        backup = st.checkbox("Backup quotidien", value=True, key="cps_backup")
        scores_input["cps"] = (80 if scada else 40) + (10 if mes else 0) + (10 if backup else 0)
    
    # MODULE 4: INFRASTRUCTURE
    with tabs[3]:
        st.markdown("#### ⚡ Infrastructure Électrique")
        tension = st.selectbox("Tension primaire", ["10 kV", "15 kV", "20 kV"], key="infra_tension")
        puissance = st.number_input("Puissance totale (kW)", value=500, step=50, key="infra_pwr")
        generateur = st.checkbox("Générateur secours", value=True, key="infra_gen")
        onduleur = st.checkbox("Onduleur (UPS) central", value=False, key="infra_ups")
        thd = st.slider("THD (%)", 0, 20, 5, key="infra_thd")
        scores_input["infra"] = (70 if generateur else 40) + (15 if onduleur else 0)
    
    # MODULE 5: MAINTENANCE
    with tabs[4]:
        st.markdown("#### 🔧 Maintenance & GMAO")
        maint_strat = st.selectbox("Stratégie", ["Corrective", "Preventive", "Predictive"], key="maint_strat")
        gmao = st.checkbox("GMAO opérationnelle", value=True, key="maint_gmao")
        predictive = st.checkbox("Maintenance prédictive", value=False, key="maint_pred")
        formation_team = st.slider("Formation team (1-5)", 1, 5, 4, key="maint_form")
        mttr = st.number_input("MTTR (heures)", value=2.5, step=0.5, key="maint_mttr")
        scores_input["maint"] = (1 if maint_strat == "Predictive" else 0.7 if maint_strat == "Preventive" else 0.3) * 30 + formation_team * 8
    
    # MODULE 6: STOCKAGE
    with tabs[5]:
        st.markdown("#### 📦 Stockage & Supply Chain")
        storage_type = st.selectbox("Système stockage", ["Manuel", "Excel", "CMMS", "WMS", "Predictive"], key="stock_sys")
        storage_score_map = {"Manuel": 0.2, "Excel": 0.4, "CMMS": 0.65, "WMS": 0.85, "Predictive": 1.0}
        stock_coverage = st.slider("Couverture stock (%)", 0, 100, 75, key="stock_couv")
        reorder_efficiency = st.slider("Efficacité recharge (%)", 0, 100, 80, key="stock_eff")
        supplier_agreement = st.checkbox("Supplier agreement SLA", value=True, key="stock_sla")
        scores_input["stock"] = (storage_score_map[storage_type] * 40 + (stock_coverage / 100) * 30 + (reorder_efficiency / 100) * 30)
    
    # MODULE 7: RH
    with tabs[6]:
        st.markdown("#### 👥 Ressources Humaines")
        formation_hours = st.number_input("Heures formation/personne/an", value=40, step=5, key="rh_form")
        certifications = st.slider("% personnel certifié", 0, 100, 60, key="rh_cert")
        expertise = st.select_slider("Niveau expertise", ["Faible", "Moyen", "Élevé"], value="Moyen", key="rh_exp")
        turnover = st.slider("Turnover annuel (%)", 0, 50, 15, key="rh_turn")
        scores_input["rh"] = (formation_hours / 40) * 30 + (certifications / 100) * 40 + (30 - turnover)
    
    # MODULE 8: CYBER
    with tabs[7]:
        st.markdown("#### 🔒 Cybersécurité & Continuité")
        firewall = st.checkbox("Pare-feu industriel", value=True, key="cyber_fw")
        audit_cyber = st.checkbox("Audit cybersécurité annuel", value=False, key="cyber_audit")
        pca = st.checkbox("PCA testé", value=False, key="cyber_pca")
        incidents_year = st.number_input("Incidents IT/an", value=2, step=1, key="cyber_inc")
        recovery_time = st.number_input("Temps recovery (heures)", value=4.0, step=0.5, key="cyber_rto")
        scores_input["cyber"] = (30 if firewall else 10) + (20 if audit_cyber else 0) + (20 if pca else 0) + max(0, 20 - incidents_year * 5)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div style="margin-top: 20px;"></div>', unsafe_allow_html=True)
    analyze = st.button("▶ ANALYSER COMPLÈTEMENT", use_container_width=True)


# ============================================================
# COLONNE DROITE — RÉSULTATS
# ============================================================
with col_output:
    
    if analyze or 'analyzed' in st.session_state:
        st.session_state.analyzed = True
        
        # ============================================================
        # CALCUL DES SCORES
        # ============================================================
        
        # Scores normalisés 0-100 pour chaque module
        final_scores = {}
        for key in MODULES:
            score = scores_input.get(key, 50)
            final_scores[key] = np.clip(score, 0, 100)
        
        # 5 PILIERS DE SCORING
        robustness = (final_scores["robots"] + final_scores["cnc"] + final_scores["infra"]) / 3
        robustness = np.clip(robustness, 0, 100)
        
        maintenance = (final_scores["maint"] * 2 + final_scores["robots"] + final_scores["cnc"]) / 4
        maintenance = np.clip(maintenance, 0, 100)
        
        governance = (final_scores["rh"] + final_scores["cyber"]) / 2
        governance = np.clip(governance, 0, 100)
        
        storage_pillar = final_scores["stock"]
        
        intervention_pillar = final_scores["maint"]  # MTTR + efficacité intervention
        
        # SCORE GLOBAL PONDÉRÉ (5 piliers)
        global_score = (
            robustness * 0.25 +
            maintenance * 0.30 +
            governance * 0.15 +
            storage_pillar * 0.15 +
            intervention_pillar * 0.15
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
            risk_emoji = "⚠️⚠️"
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
        # AFFICHAGE — KPI PRINCIPAL
        # ============================================================
        
        st.markdown(f"""
        <div class="card" style="grid-column: 1 / -1;">
            <div style="text-align: center;">
                <div class="score-label">SCORE GLOBAL</div>
                <div class="score-number {risk_color}">{global_score:.1f}/100</div>
                <div style="font-size: 13px; color: #e8eaed; margin-top: 8px;">{risk_emoji} {risk_level} | {classe}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<hr style='margin: 12px 0; border-color: rgba(88, 166, 255, 0.1);'>", unsafe_allow_html=True)
        
        # 5 PILIERS
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="card">
                <div class="score-label">🔧 Robustesse (25%)</div>
                <div class="score-number score-good">{robustness:.0f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="card">
                <div class="score-label">🎯 Maintenance (30%)</div>
                <div class="score-number score-good">{maintenance:.0f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="card">
                <div class="score-label">📋 Gouvernance (15%)</div>
                <div class="score-number score-excellent">{governance:.0f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="card">
                <div class="score-label">📦 Stockage (15%)</div>
                <div class="score-number score-good">{storage_pillar:.0f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="card">
                <div class="score-label">⚡ Efficacité (15%)</div>
                <div class="score-number score-good">{intervention_pillar:.0f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<hr style='margin: 12px 0; border-color: rgba(88, 166, 255, 0.1);'>", unsafe_allow_html=True)
        
        # CLASSIFICATION & PRIME
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="card">
                <div class="score-label">Classification</div>
                <div style="font-size: 24px; font-weight: 600; color: #e8eaed; margin: 8px 0;">{classe}</div>
                <div class="breakdown-item">
                    <span class="breakdown-label">Franchise:</span>
                    <span class="breakdown-value">{franchise} DH</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="card">
                <div class="score-label">Prime Annuelle</div>
                <div style="font-size: 24px; font-weight: 600; color: #34c759; margin: 8px 0;">{total_ttc:,.0f} DH</div>
                <div class="breakdown-item">
                    <span class="breakdown-label">Taux:</span>
                    <span class="breakdown-value">{taux:.2f}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<hr style='margin: 12px 0; border-color: rgba(88, 166, 255, 0.1);'>", unsafe_allow_html=True)
        
        # DÉTAILS 8 MODULES
        st.markdown('<div style="font-size: 12px; color: #9aa0a6; text-transform: uppercase; margin-bottom: 12px; font-weight: 600;">📊 Scores par Module (8)</div>', unsafe_allow_html=True)
        
        cols = st.columns(4)
        for idx, (key, mod) in enumerate(MODULES.items()):
            with cols[idx % 4]:
                score = final_scores[key]
                if score >= 75:
                    color = "score-excellent"
                elif score >= 50:
                    color = "score-good"
                elif score >= 25:
                    color = "score-warning"
                else:
                    color = "score-critical"
                
                st.markdown(f"""
                <div class="card">
                    <div class="score-label">{mod['label'].split()[0]}</div>
                    <div class="score-number {color}">{score:.0f}</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<hr style='margin: 12px 0; border-color: rgba(88, 166, 255, 0.1);'>", unsafe_allow_html=True)
        
        # RADAR CHART — 8 MODULES
        fig_radar = go.Figure(data=go.Scatterpolar(
            r=[final_scores[k] for k in MODULES],
            theta=[MODULES[k]["label"].split()[1] for k in MODULES],
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
            height=350,
            showlegend=False
        )
        
        st.plotly_chart(fig_radar, use_container_width=True, config={'displayModeBar': False})
        
        st.markdown("<hr style='margin: 12px 0; border-color: rgba(88, 166, 255, 0.1);'>", unsafe_allow_html=True)
        
        # SYNTHÈSE SOUSCRIPTEUR
        st.markdown('<div style="font-size: 12px; color: #9aa0a6; text-transform: uppercase; margin-bottom: 12px; font-weight: 600;">📋 Synthèse Souscripteur</div>', unsafe_allow_html=True)
        
        synthese = f"""
        **Entreprise:** {entreprise}  
        **Secteur:** {secteur}  
        **Équipement:** {equipment_type} (ID: {equipment_id})  
        **Valeur assurée:** {replacement_value:,.0f} MAD  
        **Date d'analyse:** {datetime.now().strftime('%d/%m/%Y')}
        
        ---
        
        **Score Global:** {global_score:.1f}/100  
        **Profil de Risque:** {risk_level}  
        **Classification:** {classe}  
        **Franchise:** {franchise} DH  
        **Prime HT:** {prime_ht:,.0f} DH  
        **Prime TTC:** {total_ttc:,.0f} DH/an  
        
        ---
        
        {entreprise} présente **{['une résilience industrielle avancée', 'un profil intermédiaire', 'un niveau de vulnérabilité élevé'][0 if global_score >= 75 else 1 if global_score >= 50 else 2]}**.
        """
        
        st.info(synthese)
        
        # RECOMMANDATIONS
        st.markdown("<hr style='margin: 12px 0; border-color: rgba(88, 166, 255, 0.1);'>", unsafe_allow_html=True)
        st.markdown('<div style="font-size: 12px; color: #9aa0a6; text-transform: uppercase; margin-bottom: 12px; font-weight: 600;">💡 Recommandations Prioritaires</div>', unsafe_allow_html=True)
        
        recs = []
        for key, mod in MODULES.items():
            if final_scores[key] < 50:
                recs.append((key, mod["label"], final_scores[key], "CRITIQUE"))
            elif final_scores[key] < 70:
                recs.append((key, mod["label"], final_scores[key], "MAJEURE"))
        
        if recs:
            for key, label, score, level in recs[:5]:
                if level == "CRITIQUE":
                    st.error(f"🔴 **{label}** (Score: {score:.0f}) — Action urgente requise")
                else:
                    st.warning(f"⚠️ **{label}** (Score: {score:.0f}) — Zone de fragilité identifiée")
        else:
            st.success("✅ **Tous les modules sont dans des zones acceptables!** Continuer surveillance régulière.")
    
    else:
        st.markdown("""
        <div style="text-align: center; padding: 80px 40px; color: #9aa0a6;">
            <div style="font-size: 32px; margin-bottom: 16px;">📊</div>
            <div style="font-size: 16px; margin-bottom: 8px;">Prêt à analyser</div>
            <div style="font-size: 12px;">Remplissez les 8 modules et cliquez sur ANALYSER COMPLÈTEMENT</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<hr style='margin: 24px 0; border-color: rgba(88, 166, 255, 0.1);'>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; font-size: 10px; color: #6e7681; padding: 16px 0;">
    UNDERWRITING MAROC COMPLETE v4.0 | 8 Modules • 5 Piliers • Scoring Avancé | Maroc © 2026
</div>
""", unsafe_allow_html=True)
