"""
dashboard_fair.py
═══════════════════════════════════════════════════════════════════
Interface Streamlit — Analyse FAIR Industrielle 4.0
Affiche l'analyse FAIR complète après calcul du scoring.

Sections :
  1. En-tête explicatif FAIR
  2. Équation FAIR ↔ Indices
  3. Fréquence (TCF + Vulnerability + LEF)
  4. Magnitude (Primary + Secondary + Total LM)
  5. Risque Annuel Attendu (ALE)
  6. Tableau de correspondance FAIR / Indices
  7. Limites du modèle
"""

import streamlit as st
from engine.fair_model import FAIRResult, format_mad


# ══════════════════════════════════════════════════════
#  COULEURS ET HELPERS
# ══════════════════════════════════════════════════════

def _score_badge(valeur: float, inverse: bool = False) -> str:
    """Retourne une couleur selon le niveau du score."""
    if inverse:
        # Plus c'est haut, plus c'est mauvais (vulnérabilité)
        if valeur >= 65: return "#ef4444"
        if valeur >= 40: return "#f59e0b"
        return "#10b981"
    else:
        if valeur >= 70: return "#10b981"
        if valeur >= 40: return "#f59e0b"
        return "#ef4444"


def _card(titre: str, valeur: str, sous_titre: str, color: str, icon: str = ""):
    st.markdown(f"""
    <div style="
        background:{color}12; border:1px solid {color}30;
        border-radius:10px; padding:14px 16px; text-align:center;
        height:100%;
    ">
        <div style="font-size:18px; margin-bottom:4px;">{icon}</div>
        <div style="font-size:20px; font-weight:800; color:{color};
            font-family:'Sora',sans-serif; line-height:1.1;">{valeur}</div>
        <div style="font-size:10px; font-weight:700; color:#1e293b;
            font-family:'Sora',sans-serif; margin-top:4px;">{titre}</div>
        <div style="font-size:9px; color:#64748b;
            font-family:'Sora',sans-serif; margin-top:2px;
            line-height:1.3;">{sous_titre}</div>
    </div>
    """, unsafe_allow_html=True)


def _progress_bar(valeur: float, max_val: float, color: str, label: str):
    pct = min(100, int(valeur / max_val * 100)) if max_val else 0
    st.markdown(f"""
    <div style="margin-bottom:8px;">
        <div style="display:flex; justify-content:space-between; margin-bottom:3px;">
            <span style="font-size:10px; color:#374151;
                font-family:'Sora',sans-serif;">{label}</span>
            <span style="font-size:10px; font-weight:700; color:{color};
                font-family:'Sora',sans-serif;">{valeur:.0f}</span>
        </div>
        <div style="background:#e2e8f0; border-radius:4px; height:8px;">
            <div style="background:{color}; width:{pct}%;
                height:100%; border-radius:4px;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
#  SECTION 1 — EN-TÊTE FAIR
# ══════════════════════════════════════════════════════

def render_fair_header():
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #0f2244 0%, #1d4ed8 100%);
        border-radius: 12px; padding: 20px 24px; margin-bottom: 20px;
        color: white;
    ">
        <div style="font-size:18px; font-weight:800;
            font-family:'Sora',sans-serif; margin-bottom:6px;">
            📐 Analyse FAIR — Factor Analysis of Information Risk
        </div>
        <div style="font-size:11px; opacity:0.9; line-height:1.6;
            font-family:'Sora',sans-serif;">
            Adaptation du framework FAIR (Open Group) au contexte industriel OT.
            Traduit le score de risque en <strong>perte financière annuelle attendue (ALE)</strong>
            directement exploitable par les souscripteurs et Risk Managers.
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
#  SECTION 2 — ÉQUATION FAIR ↔ INDICES
# ══════════════════════════════════════════════════════

def render_fair_equation(fair: FAIRResult):
    st.markdown("#### ⚡ Équation FAIR Adaptée")

    sa, sb, sc = fair.score_indice_a, fair.score_indice_b, fair.score_indice_c

    st.markdown(f"""
    <div style="background:#f0f4ff; border-radius:10px; padding:16px 20px;
        border-left:4px solid #1d4ed8; margin-bottom:16px;">
        <div style="font-size:11px; color:#374151; margin-bottom:10px;
            font-family:'Sora',sans-serif;">
            <b>FAIR Original :</b>
            <code style="background:#1d4ed8; color:white; padding:2px 8px;
                border-radius:4px; margin-left:8px;">Risque = LEF × LM</code>
        </div>
        <div style="font-size:11px; color:#374151; margin-bottom:10px;
            font-family:'Sora',sans-serif;">
            <b>Notre Adaptation :</b>
            <code style="background:#0f2244; color:white; padding:2px 8px;
                border-radius:4px; margin-left:8px;">
                Risque 4.0 = f(Indice C={sc}) × f(100 − Indice B={sb})
            </code>
        </div>
        <div style="font-size:10px; color:#64748b; line-height:1.6;
            font-family:'Sora',sans-serif;">
            <b>Originalité vs FAIR standard :</b> Intégration explicite de la
            <b>résilience opérationnelle</b> (Indice B) comme modérateur de la magnitude —
            dimension absente du framework FAIR original mais déterminante dans le
            contexte industriel OT marocain.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Mapping indices → composantes FAIR
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div style="background:#3b82f612; border:1px solid #3b82f630;
            border-radius:8px; padding:12px; text-align:center;">
            <div style="font-size:22px; font-weight:800; color:#3b82f6;">A={sa}</div>
            <div style="font-size:9px; color:#374151; font-weight:700;
                margin-top:4px;">Maturité Mécatronique</div>
            <div style="font-size:8px; color:#64748b; margin-top:3px;">
                → Capacité de détection précoce<br>Modérateur TCAP
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style="background:#10b98112; border:1px solid #10b98130;
            border-radius:8px; padding:12px; text-align:center;">
            <div style="font-size:22px; font-weight:800; color:#10b981;">B={sb}</div>
            <div style="font-size:9px; color:#374151; font-weight:700;
                margin-top:4px;">Résilience Opérationnelle</div>
            <div style="font-size:8px; color:#64748b; margin-top:3px;">
                → Modérateur Loss Magnitude<br>Absent de FAIR standard ★
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div style="background:#ef444412; border:1px solid #ef444430;
            border-radius:8px; padding:12px; text-align:center;">
            <div style="font-size:22px; font-weight:800; color:#ef4444;">C={sc}</div>
            <div style="font-size:9px; color:#374151; font-weight:700;
                margin-top:4px;">Vulnérabilité Systémique</div>
            <div style="font-size:8px; color:#64748b; margin-top:3px;">
                → TCF + Vulnerability FAIR<br>Fréquence des pertes (LEF)
            </div>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
#  SECTION 3 — FRÉQUENCE
# ══════════════════════════════════════════════════════

def render_fair_frequence(fair: FAIRResult):
    c = fair.composantes
    st.markdown("#### 📊 Composante Fréquence (LEF)")

    col1, col2, col3 = st.columns(3)
    with col1:
        color_tcf = _score_badge(c.tcf_score, inverse=True)
        _card("TCF", f"{c.tcf_score:.0f}/100", c.tcf_label,
              color_tcf, "🎯")
    with col2:
        color_v = _score_badge(c.vulnerability_score, inverse=True)
        _card("Vulnerability", f"{c.vulnerability_score:.0f}/100",
              c.vulnerability_label, color_v, "🔓")
    with col3:
        _card("LEF (sinistres/an)",
              f"{c.lef_annuelle_min:.1f} – {c.lef_annuelle_max:.1f}",
              c.lef_label, c.risk_color, "⚡")

    st.markdown("")

    # Barres de progression
    col_a, col_b = st.columns(2)
    with col_a:
        _progress_bar(c.tcf_score, 100,
                      _score_badge(c.tcf_score, inverse=True),
                      "Threat Contact Frequency")
    with col_b:
        _progress_bar(c.vulnerability_score, 100,
                      _score_badge(c.vulnerability_score, inverse=True),
                      "Vulnerability Score")


# ══════════════════════════════════════════════════════
#  SECTION 4 — MAGNITUDE
# ══════════════════════════════════════════════════════

def render_fair_magnitude(fair: FAIRResult):
    c = fair.composantes
    st.markdown("#### 💰 Composante Magnitude (LM)")

    col1, col2, col3 = st.columns(3)
    with col1:
        _card(
            "Primary Loss",
            f"{format_mad(c.primary_loss_min)} – {format_mad(c.primary_loss_max)}",
            "Dommage matériel direct (BDM)",
            "#3b82f6", "🔧"
        )
    with col2:
        _card(
            "Secondary Loss (PE numérique)",
            f"{format_mad(c.secondary_loss_min)} – {format_mad(c.secondary_loss_max)}",
            c.pe_label,
            "#f59e0b", "⏱️"
        )
    with col3:
        _card(
            "Total LM",
            f"{format_mad(c.total_lm_min)} – {format_mad(c.total_lm_max)}",
            c.lm_label,
            c.risk_color, "📉"
        )

    # Box multiplicateur PE
    st.markdown(f"""
    <div style="
        background:#fffbeb; border:1px solid #f59e0b40;
        border-radius:8px; padding:12px 16px; margin-top:12px;
    ">
        <div style="display:flex; align-items:center; gap:10px;">
            <span style="font-size:24px;">×{c.pe_multiplier:.0f}</span>
            <div>
                <div style="font-size:11px; font-weight:700; color:#92400e;
                    font-family:'Sora',sans-serif;">
                    Multiplicateur PE Numérique (vs Industrie 3.0)
                </div>
                <div style="font-size:10px; color:#64748b;
                    font-family:'Sora',sans-serif; margin-top:2px;">
                    Durée estimée : <b>{c.pe_weeks_min} – {c.pe_weeks_max} semaines</b>
                    — {c.pe_label}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
#  SECTION 5 — RISQUE ANNUEL (ALE)
# ══════════════════════════════════════════════════════

def render_fair_risk_annuel(fair: FAIRResult):
    c = fair.composantes
    st.markdown("#### 🎯 Risque Annuel Attendu — ALE (Annual Loss Expectancy)")

    # Grande carte centrale
    st.markdown(f"""
    <div style="
        background:{c.risk_color}10; border:2px solid {c.risk_color}40;
        border-radius:12px; padding:20px 24px; text-align:center;
        margin-bottom:16px;
    ">
        <div style="font-size:13px; font-weight:700; color:#374151;
            font-family:'Sora',sans-serif; margin-bottom:8px;">
            Perte Annuelle Attendue (ALE = LEF × LM)
        </div>
        <div style="font-size:28px; font-weight:800; color:{c.risk_color};
            font-family:'Sora',sans-serif; line-height:1.1;">
            {format_mad(c.risk_annuel_min)} – {format_mad(c.risk_annuel_max)}
        </div>
        <div style="font-size:11px; color:{c.risk_color}; font-weight:600;
            font-family:'Sora',sans-serif; margin-top:8px;">
            {c.risk_label}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Narrative
    if fair.narrative:
        st.markdown(f"""
        <div style="
            background:#f8fafc; border-radius:8px; padding:12px 16px;
            border-left:3px solid #1d4ed8; margin-bottom:12px;
        ">
            <div style="font-size:10px; color:#374151; line-height:1.6;
                font-family:'Sora',sans-serif;">
                {fair.narrative}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Grille tarifaire directe
    st.markdown("**Orientation souscription issue de l'ALE :**")

    sg = fair.score_global
    rows = [
        ("80–100", "Excellence 4.0",     "Prime de base ou réduite",    "#10b981", sg >= 80),
        ("65–79",  "Maturité avancée",   "Prime standard",              "#3b82f6", 65 <= sg < 80),
        ("45–64",  "Intermédiaire",      "Prime majorée +15 à 35%",     "#f59e0b", 45 <= sg < 65),
        ("25–44",  "Maturité faible",    "Surprime + visite terrain",   "#ef4444", 25 <= sg < 45),
        ("0–24",   "Risque critique",    "Tarification individuelle",   "#7f1d1d", sg < 25),
    ]

    for score_range, profil, action, color, is_current in rows:
        bg = f"{color}25" if is_current else "#f8fafc"
        border = f"2px solid {color}" if is_current else "1px solid #e2e8f0"
        marker = " ◀ Votre profil" if is_current else ""

        st.markdown(f"""
        <div style="
            background:{bg}; border:{border}; border-radius:7px;
            padding:8px 14px; margin-bottom:5px;
            display:flex; justify-content:space-between; align-items:center;
        ">
            <span style="font-size:10px; font-weight:700; color:{color};
                font-family:'Sora',sans-serif; min-width:40px;">{score_range}</span>
            <span style="font-size:10px; color:#374151;
                font-family:'Sora',sans-serif; flex:1; margin:0 8px;">{profil}</span>
            <span style="font-size:10px; color:#64748b;
                font-family:'Sora',sans-serif;">{action}{marker}</span>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
#  SECTION 6 — TABLEAU DE CORRESPONDANCE
# ══════════════════════════════════════════════════════

def render_fair_mapping(fair: FAIRResult):
    st.markdown("#### 🔗 Tableau de Correspondance FAIR ↔ Indices du Prototype")

    st.markdown("""
    <div style="font-size:10px; color:#64748b; margin-bottom:10px;
        font-family:'Sora',sans-serif;">
        Ce tableau démontre que le prototype est une
        <b>implémentation opérationnelle du modèle FAIR</b>
        adaptée au contexte industriel OT marocain.
    </div>
    """, unsafe_allow_html=True)

    fair_rows = [
        ("TCF", "Threat Contact Frequency",
         "Fréquence d'exposition aux menaces",
         f"Indice C ({fair.score_indice_c}) → exposition cyber OT",
         "#ef4444"),
        ("TCAP", "Threat Capability",
         "Capacité de la menace à causer un dommage",
         "IND-05 Cyber-Physical Coupling + IND-13 Cyber-Hygiène OT",
         "#f59e0b"),
        ("Vulnérabilité", "Vulnerability",
         "Probabilité que la menace réussisse",
         "Fragilité IT : absence pare-feu, backup, segmentation",
         "#f59e0b"),
        ("LEF", "Loss Event Frequency",
         "Fréquence annuelle des événements de perte",
         f"f(Indice C={fair.score_indice_c}) → "
         f"{fair.composantes.lef_annuelle_min:.1f}–{fair.composantes.lef_annuelle_max:.1f} sinistres/an",
         "#ef4444"),
        ("PLEF", "Primary Loss",
         "Coût direct (dommage matériel)",
         "Tableau équipements 2.7.9 : BDM robot, CNC, SCADA",
         "#3b82f6"),
        ("SLEF", "Secondary Loss",
         "PE numérique + pénalités + forensique",
         f"f(Indice B={fair.score_indice_b}) → ×{fair.composantes.pe_multiplier:.0f} vs PE physique",
         "#f59e0b"),
        ("LM", "Loss Magnitude",
         "Coût total du sinistre",
         f"f(100−B={100-fair.score_indice_b}) → capacité absorption inversée",
         "#ef4444"),
        ("RISK", "Annual Loss Expectancy",
         "Perte financière annuelle attendue",
         f"LEF × LM = {format_mad(fair.composantes.risk_annuel_min)}–"
         f"{format_mad(fair.composantes.risk_annuel_max)}/an",
         fair.composantes.risk_color),
    ]

    for abrev, nom_fair, definition, implementation, color in fair_rows:
        st.markdown(f"""
        <div style="
            border-left:3px solid {color}; background:{color}08;
            border-radius:5px; padding:8px 12px; margin-bottom:6px;
        ">
            <div style="display:flex; gap:8px; align-items:flex-start;">
                <span style="
                    font-size:9px; font-weight:800; color:white;
                    background:{color}; border-radius:3px;
                    padding:2px 6px; white-space:nowrap; min-width:36px;
                    text-align:center; font-family:'Sora',sans-serif;">{abrev}</span>
                <div style="flex:1;">
                    <div style="font-size:10px; font-weight:700; color:#0f2244;
                        font-family:'Sora',sans-serif;">{nom_fair}</div>
                    <div style="font-size:9px; color:#64748b;
                        font-family:'Sora',sans-serif;">{definition}</div>
                    <div style="font-size:9px; color:{color}; font-weight:600;
                        font-family:'Sora',sans-serif; margin-top:2px;">
                        → {implementation}
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
#  SECTION 7 — LIMITES DU MODÈLE
# ══════════════════════════════════════════════════════

def render_fair_limites(fair: FAIRResult):
    with st.expander("⚠️ Limites méthodologiques du modèle FAIR adapté", expanded=False):
        st.markdown("""
        <div style="font-size:10px; color:#374151; line-height:1.6;
            font-family:'Sora',sans-serif; margin-bottom:8px;">
            Ces limites sont inhérentes à l'adaptation d'un framework IT vers le contexte
            industriel OT. Elles sont identifiées explicitement pour guider l'évolution
            du modèle lors de la Phase 2 (calibration statistique).
        </div>
        """, unsafe_allow_html=True)

        for i, limite in enumerate(fair.limites, 1):
            st.markdown(f"""
            <div style="
                background:#fef9ec; border-left:3px solid #f59e0b;
                border-radius:4px; padding:8px 12px; margin-bottom:6px;
            ">
                <span style="font-size:10px; color:#92400e;
                    font-family:'Sora',sans-serif;">
                    <b>Limite {i} —</b> {limite}
                </span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div style="font-size:9px; color:#64748b; margin-top:8px;
            font-family:'Sora',sans-serif; font-style:italic;">
            📌 Phase 2 (feuille de route) : calibration Monte Carlo sur données
            sinistralité réelles du portefeuille RMA → transformation des fourchettes
            d'expert en distributions de probabilité statistiques.
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
#  FONCTION PRINCIPALE DE RENDU
# ══════════════════════════════════════════════════════

def render_fair_analysis(fair: FAIRResult):
    """
    Rendu complet de l'analyse FAIR dans l'interface Streamlit.
    À appeler depuis layout.py après calcul du scoring.
    """
    render_fair_header()

    # Onglets pour organiser le contenu
    tab1, tab2, tab3, tab4 = st.tabs([
        "⚡ Équation & Indices",
        "📊 Fréquence & Magnitude",
        "🎯 Risque Annuel (ALE)",
        "🔗 Correspondance FAIR",
    ])

    with tab1:
        render_fair_equation(fair)

    with tab2:
        render_fair_frequence(fair)
        st.markdown("---")
        render_fair_magnitude(fair)

    with tab3:
        render_fair_risk_annuel(fair)

    with tab4:
        render_fair_mapping(fair)
        st.markdown("---")
        render_fair_limites(fair)
