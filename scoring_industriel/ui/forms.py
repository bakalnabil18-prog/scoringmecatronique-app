"""
forms.py — Formulaires des 8 modules avec navigation par étapes
FIX : Persistance des données entre étapes via form_data dans session_state.
Chaque widget sauvegarde sa valeur dans st.session_state["form_data"][key]
au moment du rendu, de sorte que les données ne se perdent pas quand
Streamlit détruit les widgets des étapes précédentes.
"""

import streamlit as st
from .theme import MODULE_COLORS, MODULE_ICONS, MODULE_LABELS


# ══════════════════════════════════════════════════════════════
#  HELPERS — widgets persistants
# ══════════════════════════════════════════════════════════════

def _fd():
    """Raccourci vers le dictionnaire persistant form_data."""
    if "form_data" not in st.session_state:
        st.session_state["form_data"] = {}
    return st.session_state["form_data"]


def _get(key, default=""):
    """Lire une valeur sauvegardée (ou default si première visite)."""
    return _fd().get(key, default)


def _save(key, value):
    """Sauvegarder une valeur dans form_data."""
    _fd()[key] = value


def _selectbox(label, options, key, help=None):
    """Selectbox qui persiste sa valeur dans form_data."""
    saved = _get(key, options[0])
    # S'assurer que saved est dans options
    idx = options.index(saved) if saved in options else 0
    val = st.selectbox(label, options, index=idx, key=f"w_{key}", help=help)
    _save(key, val)
    return val


def _bool_select(label, key, hint=""):
    """Selectbox Oui/Non qui persiste."""
    opts = ["—", "✅ Oui", "❌ Non"]
    saved = _get(key, "—")
    idx = opts.index(saved) if saved in opts else 0
    val = st.selectbox(label, opts, index=idx, key=f"w_{key}", help=hint or None)
    _save(key, val)
    # Retourne 'oui' / 'non' / ''  pour compatibilité avec normaliser
    if "Oui" in val:
        return "oui"
    if "Non" in val:
        return "non"
    return ""


def _number(label, key, min_value=0.0, max_value=None, value=0.0, fmt="%.1f", help=None, step=None):
    """Number input qui persiste."""
    saved = _get(key, value)
    try:
        saved = float(saved) if saved not in (None, "") else value
    except (TypeError, ValueError):
        saved = value
    kwargs = dict(label=label, min_value=float(min_value), value=float(saved),
                  key=f"w_{key}", help=help, format=fmt)
    if max_value is not None:
        kwargs["max_value"] = float(max_value)
    if step is not None:
        kwargs["step"] = float(step)
    val = st.number_input(**kwargs)
    _save(key, val)
    return val


def _number_int(label, key, min_value=0, max_value=None, value=0, help=None):
    """Number input entier qui persiste."""
    saved = _get(key, value)
    try:
        saved = int(saved) if saved not in (None, "") else value
    except (TypeError, ValueError):
        saved = value
    kwargs = dict(label=label, min_value=int(min_value), value=int(saved),
                  key=f"w_{key}", help=help)
    if max_value is not None:
        kwargs["max_value"] = int(max_value)
    val = st.number_input(**kwargs)
    _save(key, val)
    return val


def _text(label, key, placeholder=""):
    """Text input qui persiste."""
    saved = _get(key, "")
    val = st.text_input(label, value=saved, key=f"w_{key}", placeholder=placeholder)
    _save(key, val)
    return val


def _section_header(title, module_key):
    color = MODULE_COLORS.get(module_key, "#3b82f6")
    icon  = MODULE_ICONS.get(module_key, "🔹")
    label = MODULE_LABELS.get(module_key, title)
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:10px;
        padding:12px 16px; background:{color}12;
        border-radius:10px; border:1px solid {color}30; margin:8px 0 16px 0;">
        <div style="font-size:22px;">{icon}</div>
        <div>
            <div style="font-size:14px; font-weight:800; color:#0f2244;
                font-family:'Sora',sans-serif;">{label}</div>
            <div style="font-size:10px; color:#64748b;
                font-family:'Sora',sans-serif;">{title}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def _bloc_header(title, color="#3b82f6"):
    st.markdown(f"""
    <div style="font-size:11px; font-weight:700; color:{color};
        text-transform:uppercase; letter-spacing:0.8px;
        border-bottom:1px solid {color}30; padding-bottom:4px;
        margin:12px 0 10px 0; font-family:'Sora',sans-serif;">{title}</div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  ÉTAPE 0 — IDENTIFICATION
# ══════════════════════════════════════════════════════════════

def form_identification():
    st.markdown("### 🏢 Identification du Client")
    c1, c2, c3 = st.columns(3)
    with c1:
        _text("Nom de l'entreprise *", "entreprise", "AutoMaro SA")
    with c2:
        _selectbox("Secteur d'activité *", [
            "—", "automobile", "aeronautique", "agroalimentaire",
            "chimie_pharma", "metalurgie", "electronique", "textile", "btp", "autre"
        ], "secteur")
    with c3:
        _text("Ville *", "ville", "Casablanca")
    c4, c5 = st.columns(2)
    with c4:
        _number_int("Effectif (personnes)", "effectif", min_value=0)
    with c5:
        _number("CA annuel (MAD)", "ca_annuel_mad", min_value=0.0, fmt="%.0f")


# ══════════════════════════════════════════════════════════════
#  ÉTAPE 1 — ROBOTS
# ══════════════════════════════════════════════════════════════

def form_robots():
    color = MODULE_COLORS["robots"]
    _section_header("Module 1 — Poids scoring : 18%", "robots")

    _bloc_header("Bloc 1 — Identification Technique", color)
    c1, c2, c3 = st.columns(3)
    with c1:
        _selectbox("Type de robot *", ["—","6 axes","5 axes","SCARA","Delta"], "type_robot")
        _bool_select("Cobots présents *", "cobots")
    with c2:
        _bool_select("Cellules robotisées modulaires", "cellule_modulaire")
        _text("Marque & Modèle", "marque_modele", "FANUC R-2000iC")
    with c3:
        _number_int("Année d'installation", "annee_install", min_value=1990, max_value=2026, value=2020)
        _selectbox("Intégration réseau *", ["—","Isolé","Connecté MES","Connecté Cloud"], "integration_reseau")

    _bloc_header("Bloc 2 — Données Quantitatives", color)
    c1, c2, c3 = st.columns(3)
    with c1:
        _number_int("Nombre total robots *", "nombre_robots", min_value=0)
        _number("Valeur unitaire (MAD)", "valeur_unitaire_mad", min_value=0.0, fmt="%.0f")
    with c2:
        _number("Valeur totale parc (MAD)", "valeur_totale_parc_mad", min_value=0.0, fmt="%.0f")
        _number("Heures moy. fonctionnement / an", "heures_fonct_an", min_value=0.0)
    with c3:
        _number("MTBF robots (heures)", "mtbf_robots", min_value=0.0, help="Mean Time Between Failures")
        _number("MTTR robots (heures)", "mttr_robots", min_value=0.0, help="Mean Time To Repair")

    _bloc_header("Bloc 3 — Variables de Scoring", color)
    c1, c2, c3 = st.columns(3)
    with c1:
        _selectbox("Niveau redondance *", ["—","Faible","Moyen","Élevé"], "niveau_redondance")
        _bool_select("Contrat maintenance constructeur", "contrat_maintenance")
    with c2:
        _bool_select("Mise à jour firmware régulière", "maj_firmware")
        _selectbox("Historique pannes 3 ans", ["—","0 panne","1-2 pannes","3-5 pannes","> 5 pannes"], "historique_pannes")
    with c3:
        _bool_select("Capteurs prédictifs présents", "capteurs_predictifs")
        _selectbox("Dépendance production *", ["—","Faible","Moyenne","Critique"], "dependance_production")


# ══════════════════════════════════════════════════════════════
#  ÉTAPE 1 — CNC
# ══════════════════════════════════════════════════════════════

def form_cnc():
    color = MODULE_COLORS["cnc"]
    _section_header("Module 2 — Poids scoring : 14%", "cnc")

    _bloc_header("Bloc 1 — Identification CNC", color)
    c1, c2, c3 = st.columns(3)
    with c1:
        _selectbox("Type CNC *", ["—","3 axes","5 axes","Multi-broche"], "type_cnc")
        _text("Marque", "marque_cnc", "DMG Mori")
    with c2:
        _number_int("Année fabrication", "annee_cnc", min_value=1990, max_value=2026, value=2018)
        _selectbox("Automatisation *", ["—","Manuel","Semi-auto","Full auto"], "automation_cnc")
    with c3:
        _bool_select("Interface MES / ERP", "interface_mes_erp")

    _bloc_header("Bloc 2 — Données Techniques", color)
    c1, c2, c3 = st.columns(3)
    with c1:
        _number_int("Nombre total CNC *", "nombre_cnc", min_value=0)
        _number("Valeur unitaire (MAD)", "valeur_unit_cnc", min_value=0.0, fmt="%.0f")
    with c2:
        _number("Heures fonctionnement cumulées", "heures_cumul_cnc", min_value=0.0)
        _selectbox("Type refroidissement", ["—","Air","Eau","Huile","Mixte"], "type_refroid")
    with c3:
        _bool_select("Sensibilité électrique", "sensibilite_electrique")
        _bool_select("Variateurs de fréquence", "variateur_freq")

    _bloc_header("Bloc 3 — Indicateurs de Risque", color)
    c1, c2, c3 = st.columns(3)
    with c1:
        _selectbox("Fréquence maintenance préventive",
                   ["—","Mensuelle","Trimestrielle","Semestrielle","Annuelle","Aucune"],
                   "freq_maintenance_prev")
        _bool_select("Maintenance prédictive CNC", "maintenance_pred_cnc")
    with c2:
        _selectbox("Historique dommage électrique",
                   ["—","Aucun","1-2 incidents","3+ incidents"], "historique_dom_elec")
        _bool_select("Protection surtension installée", "protection_surtension")
    with c3:
        _bool_select("Onduleur (UPS) dédié CNC", "ups_dedie")


# ══════════════════════════════════════════════════════════════
#  ÉTAPE 2 — CPS
# ══════════════════════════════════════════════════════════════

def form_cps():
    color = MODULE_COLORS["cps"]
    _section_header("Module 3 — Poids scoring : 18%", "cps")

    _bloc_header("Bloc 1 — Architecture CPS", color)
    c1, c2, c3 = st.columns(3)
    with c1:
        _bool_select("Présence SCADA *", "presence_scada")
        _bool_select("MES intégré", "mes_integre")
    with c2:
        _bool_select("ERP connecté production", "erp_connecte")
        _bool_select("Cloud externe", "cloud_externe")
    with c3:
        _selectbox("Protocole industriel", ["—","OPC-UA","Modbus","Profinet","Autre"], "protocole_industriel")
        _selectbox("Segmentation réseau *", ["—","Faible","Moyenne","Élevée"], "segmentation_reseau")

    _bloc_header("Bloc 2 — Infrastructure IT", color)
    c1, c2, c3 = st.columns(3)
    with c1:
        _selectbox("Type serveurs", ["—","Sur site","Cloud hybride","Cloud pur"], "type_serveurs")
        _bool_select("Redondance serveurs *", "redondance_serveurs")
    with c2:
        _bool_select("Backup quotidien automatisé *", "backup_quotidien")
        _number("RTO estimé (heures)", "rto_heures", min_value=0.0, help="Recovery Time Objective")
    with c3:
        _bool_select("Pare-feu industriel *", "parefeu_industriel")
        _bool_select("Audit cybersécurité annuel *", "audit_cyber")

    _bloc_header("Bloc 3 — Indicateurs Assurantiels", color)
    c1, c2, c3 = st.columns(3)
    with c1:
        _selectbox("Dépendance production au CPS *", ["—","Faible","Moyen","Critique"], "dependance_cps")
        _selectbox("Historique incidents IT", ["—","Aucun","1-2/an","3+/an"], "historique_incid_it")
    with c2:
        _number("Temps moyen arrêt / incident IT (h)", "temps_moy_arret_it_h", min_value=0.0)
        _bool_select("Plan de continuité (PCA) *", "plan_continuite")
    with c3:
        _bool_select("Simulation de crise annuelle", "simulation_crise")


# ══════════════════════════════════════════════════════════════
#  ÉTAPE 3 — ÉLECTRIQUE
# ══════════════════════════════════════════════════════════════

def form_electrique():
    color = MODULE_COLORS["electrique"]
    _section_header("Module 4 — Poids scoring : 10%", "electrique")

    _bloc_header("Bloc 1 — Équipements Électriques", color)
    c1, c2, c3 = st.columns(3)
    with c1:
        _bool_select("Tableau BT/MT intelligent", "tableau_bt_mt")
        _bool_select("Protection différentiel avancée *", "protection_diff")
    with c2:
        _bool_select("Système monitoring énergétique", "monitoring_energie")
        _bool_select("UPS industriel *", "ups_industriel")
    with c3:
        _bool_select("Groupe électrogène", "groupe_electrogene")

    _bloc_header("Bloc 2 — Données Électriques", color)
    c1, c2 = st.columns(2)
    with c1:
        _number("Puissance installée totale (kW)", "puissance_installee_kw", min_value=0.0)
        _number("Taux de charge moyen (%)", "taux_charge_moyen_pct", min_value=0.0, max_value=100.0)
    with c2:
        _selectbox("Incidents électriques / an *", ["—","0","1-2","3-5","> 5"], "incidents_electriques")
        _bool_select("Mise à la terre conforme *", "mise_a_la_terre")

    _bloc_header("Bloc 3 — Impact Scoring", color)
    c1, c2, c3 = st.columns(3)
    with c1:
        _selectbox("Vulnérabilité dommage électrique", ["—","Faible","Modérée","Élevée"], "vulnerabilite_dom_elec")
    with c2:
        _bool_select("Risque court-circuit évalué", "risque_court_circuit")
    with c3:
        _selectbox("Risque propagation incendie", ["—","Faible","Modéré","Élevé"], "risque_propag_incendie")


# ══════════════════════════════════════════════════════════════
#  ÉTAPE 3 — MAINTENANCE
# ══════════════════════════════════════════════════════════════

def form_maintenance():
    color = MODULE_COLORS["maintenance"]
    _section_header("Module 5 — Poids scoring : 20% (bloc central PFE)", "maintenance")

    _bloc_header("Bloc 1 — Organisation Maintenance", color)
    c1, c2, c3 = st.columns(3)
    with c1:
        _bool_select("GMAO utilisée *", "gmao_utilisee")
    with c2:
        _selectbox("Type maintenance dominant *",
                   ["—","Corrective","Préventive","Prédictive"], "type_maintenance")
    with c3:
        _bool_select("KPIs maintenance définis", "existence_kpi")

    _bloc_header("Bloc 2 — Indicateurs Quantifiables", color)
    c1, c2, c3 = st.columns(3)
    with c1:
        _number("MTBF global (heures)", "mtbf_global", min_value=0.0, help="Mean Time Between Failures")
        _number("MTTR global (heures)", "mttr_global", min_value=0.0, help="Mean Time To Repair")
    with c2:
        _number("Taux maintenance planifiée (%)", "taux_maint_planifie_pct", min_value=0.0, max_value=100.0)
        _number("Taux respect planning (%)", "taux_respect_planning_pct", min_value=0.0, max_value=100.0)
    with c3:
        _number("Budget maintenance / valeur parc (%)", "budget_maintenance_pct_parc", min_value=0.0)

    _bloc_header("Bloc 3 — Maturité Maintenance", color)
    c1, c2, c3 = st.columns(3)
    with c1:
        _selectbox("Niveau digitalisation (1 à 5) *",
                   ["—","1","2","3","4","5"], "niveau_digitalisation",
                   help="1=Papier 3=GMAO 5=IA prédictive")
    with c2:
        _bool_select("Maintenance conditionnelle capteurs", "maint_conditionnelle")
    with c3:
        _bool_select("IA prédictive utilisée", "ia_predictive")


# ══════════════════════════════════════════════════════════════
#  ÉTAPE 4 — MANUTENTION
# ══════════════════════════════════════════════════════════════

def form_manutention():
    color = MODULE_COLORS["manutention"]
    _section_header("Module 6 — Influence directe MTTR", "manutention")

    _bloc_header("Bloc 1 — Équipements de Manutention", color)
    c1, c2, c3 = st.columns(3)
    with c1:
        _bool_select("AGV (véhicules autonomes)", "presence_agv")
        _bool_select("Chariots élévateurs", "chariots_elev")
        _bool_select("Ponts roulants", "ponts_roulants")
    with c2:
        _bool_select("Palans électriques", "palans_elec")
        _bool_select("Outillage spécialisé maintenance", "outillage_special")
        _bool_select("Atelier interne dédié", "atelier_interne")
    with c3:
        _number_int("Nombre total équipements", "nombre_equip_manu", min_value=0)
        _number("Âge moyen (ans)", "age_moyen_manu", min_value=0.0)
        _number("Disponibilité (%)", "disponibilite_manu_pct", min_value=0.0, max_value=100.0)

    _bloc_header("Bloc 2 — Variables Scoring Manutention", color)
    c1, c2, c3 = st.columns(3)
    with c1:
        _bool_select("Manutention automatisée", "manutention_auto")
        _number("Temps mobilisation moyen (min)", "temps_mobilisation_min", min_value=0.0)
    with c2:
        _bool_select("Redondance équipements critiques", "redond_equip_crit")
    with c3:
        _bool_select("Disponibilité immédiate 24/7", "disponibilite_247")
        _bool_select("Dépendance prestataire externe", "dependance_prestataire")


# ══════════════════════════════════════════════════════════════
#  ÉTAPE 4 — STOCKAGE
# ══════════════════════════════════════════════════════════════

def form_stockage():
    color = MODULE_COLORS["stockage"]
    _section_header("Module 7 — Impact BDM & durée sinistre", "stockage")

    _bloc_header("Bloc 1 — Infrastructure de Stockage", color)
    c1, c2, c3 = st.columns(3)
    with c1:
        _bool_select("Magasin central pièces", "magasin_central")
        _bool_select("Rayonnage intelligent", "rayonnage_intelligent")
    with c2:
        _bool_select("Stockage vertical automatisé", "stockage_vertical_auto")
        _bool_select("Zone pièces critiques dédiée", "zone_pieces_crit")
    with c3:
        _bool_select("Contrôle température/humidité", "controle_therm_humi")

    _bloc_header("Bloc 2 — Gestion Numérique Stock", color)
    c1, c2, c3 = st.columns(3)
    with c1:
        _bool_select("Intégration ERP stock *", "integration_erp_stock")
        _bool_select("Stock minimum défini", "stock_minimum_defini")
    with c2:
        _bool_select("Analyse ABC des pièces", "analyse_abc")
        _number("Délai réappro. fournisseur (jours)", "delai_reappro_jours", min_value=0.0)
    with c3:
        _selectbox("Taux rupture stock 12 mois *",
                   ["—","0%","< 5%","5-15%","> 15%"], "taux_rupture_stock")
        _bool_select("Suivi consommation / demande réelle", "suivi_consommation")

    _bloc_header("Bloc 3 — Indicateurs de Performance", color)
    c1, c2, c3 = st.columns(3)
    with c1:
        _number("Temps moyen dispo pièce critique (h)", "temps_moy_disp_piece_h", min_value=0.0)
        _number("% pièces critiques en stock", "pct_pieces_crit_stock", min_value=0.0, max_value=100.0)
    with c2:
        _number("Taux rotation stock", "taux_rotation_stock", min_value=0.0)
        _number("Valeur stock / valeur parc (%)", "valeur_stock_pct_parc", min_value=0.0)
    with c3:
        _bool_select("Prédiction conso via historique", "prediction_conso")

    _bloc_header("Bloc 4 — Variables Assurantielles", color)
    c1, c2, c3, c4 = st.columns(4)
    with c1: _bool_select("Pièces critiques redondantes *", "pieces_crit_redond")
    with c2: _bool_select("Fournisseurs multiples *", "fournisseurs_multiples")
    with c3: _bool_select("Contrat appro. prioritaire", "contrat_appro_prio")
    with c4: _bool_select("Simulation pénurie annuelle", "simulation_penurie")


# ══════════════════════════════════════════════════════════════
#  ÉTAPE 5 — INTERVENTION
# ══════════════════════════════════════════════════════════════

def form_intervention():
    color = MODULE_COLORS["intervention"]
    _section_header("Module 8 — Maturité opérationnelle", "intervention")

    _bloc_header("Bloc 1 — Organisation Intervention", color)
    c1, c2, c3, c4 = st.columns(4)
    with c1: _bool_select("Équipe maintenance interne *", "equipe_interne")
    with c2: _bool_select("Techniciens certifiés constructeur", "techniciens_certif")
    with c3: _bool_select("Astreinte 24/7 *", "astreinte_247")
    with c4: _number("SLA interne (heures)", "sla_interne_h", min_value=0.0)

    _bloc_header("Bloc 2 — Indicateurs Quantifiés", color)
    c1, c2, c3 = st.columns(3)
    with c1:
        _number("MTTR moyen (heures)", "mttr_moyen", min_value=0.0)
        _number("% interventions < 4h", "pct_interv_4h", min_value=0.0, max_value=100.0)
    with c2:
        _number("% interventions planifiées", "pct_interv_planif", min_value=0.0, max_value=100.0)
        _number("Taux résolution 1er passage (%)", "taux_resolution_pp", min_value=0.0, max_value=100.0)
    with c3:
        _number_int("Arrêts > 24h (3 dernières années)", "historique_arret_24h", min_value=0)

    _bloc_header("Bloc 3 — Digitalisation Intervention", color)
    c1, c2, c3, c4 = st.columns(4)
    with c1: _bool_select("GMAO mobile", "gmao_mobile")
    with c2: _bool_select("Traçabilité intervention temps réel", "tracabilite_rt")
    with c3: _bool_select("Historique pannes analysé", "historique_pannes_analyse")
    with c4: _bool_select("Dashboard KPI maintenance", "dashboard_kpi")


# ══════════════════════════════════════════════════════════════
#  STEPPER & NAVIGATION
# ══════════════════════════════════════════════════════════════

STEPS = [
    {"label": "Identification & Robots",   "forms": [form_identification, form_robots]},
    {"label": "CNC & Système CPS",         "forms": [form_cnc, form_cps]},
    {"label": "Électrique & Maintenance",  "forms": [form_electrique, form_maintenance]},
    {"label": "Manutention & Stockage",    "forms": [form_manutention, form_stockage]},
    {"label": "Intervention & Résultats",  "forms": [form_intervention]},
]


def render_stepper(current_step: int):
    cols = st.columns(len(STEPS))
    for i, (col, step) in enumerate(zip(cols, STEPS)):
        with col:
            done   = i < current_step
            active = i == current_step
            color  = "#1d4ed8" if active else ("#10b981" if done else "#e2e8f0")
            text_c = "#fff" if (active or done) else "#94a3b8"
            border = "box-shadow: 0 0 0 3px #3b82f680;" if active else ""
            st.markdown(f"""
            <div style="text-align:center;">
                <div style="width:28px; height:28px; border-radius:50%;
                    background:{color}; color:{text_c}; display:inline-flex;
                    align-items:center; justify-content:center;
                    font-size:12px; font-weight:800; {border}
                    font-family:'Sora',sans-serif;">{i+1}</div>
                <div style="font-size:9px; color:{'#1d4ed8' if active else '#64748b'};
                    font-weight:{'700' if active else '500'};
                    font-family:'Sora',sans-serif; margin-top:3px; line-height:1.2;">
                    {step['label']}
                </div>
            </div>
            """, unsafe_allow_html=True)


def render_step_forms(step_idx: int):
    if step_idx < len(STEPS):
        for form_fn in STEPS[step_idx]["forms"]:
            form_fn()
            st.divider()
