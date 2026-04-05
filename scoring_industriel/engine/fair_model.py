"""
fair_model.py
═══════════════════════════════════════════════════════════════════
Adaptation du modèle FAIR (Factor Analysis of Information Risk)
au contexte industriel OT — PFE Nabil EL BAKAL, ENSA Kénitra 2025

FAIR original :   Risque = LEF × LM
Notre adaptation : Risque Industriel 4.0 = f(Indice C) × f(100 − Indice B)

Correspondance :
  TCF  (Threat Contact Frequency)  →  Indice C : exposition cyber OT
  Vulnerability                    →  Fragilité IT + absence segmentation
  LEF  (Loss Event Frequency)      →  f(Indice C)
  PLEF (Primary Loss)              →  Coût dommage matériel (tableau 2.7.9)
  SLEF (Secondary Loss)            →  PE numérique allongée
  LM   (Loss Magnitude)            →  f(100 − Indice B)
  Risk                             →  Score Global inversé
"""

from dataclasses import dataclass, field
from typing import Dict, Tuple
from .data_models import FormData, ScoreResult


# ══════════════════════════════════════════════════════
#  DATACLASSES FAIR
# ══════════════════════════════════════════════════════

@dataclass
class FAIRComponentes:
    """Composantes FAIR calculées à partir des indices du prototype."""

    # ── Fréquence ────────────────────────────────────────────────
    tcf_score: float = 0.0          # Threat Contact Frequency (0-100)
    tcf_label: str = ""             # Basse / Modérée / Élevée / Très élevée
    vulnerability_score: float = 0.0
    vulnerability_label: str = ""

    lef_annuelle_min: float = 0.0   # Sinistres/an — borne basse
    lef_annuelle_max: float = 0.0   # Sinistres/an — borne haute
    lef_label: str = ""

    # ── Magnitude ────────────────────────────────────────────────
    primary_loss_min: float = 0.0   # MAD — dommage direct min
    primary_loss_max: float = 0.0   # MAD — dommage direct max
    secondary_loss_min: float = 0.0 # MAD — PE numérique + indirect min
    secondary_loss_max: float = 0.0 # MAD — PE numérique + indirect max
    total_lm_min: float = 0.0       # MAD — perte totale min
    total_lm_max: float = 0.0       # MAD — perte totale max
    lm_label: str = ""

    # ── Risque agrégé ─────────────────────────────────────────────
    risk_annuel_min: float = 0.0    # MAD/an — perte annuelle attendue min
    risk_annuel_max: float = 0.0    # MAD/an — perte annuelle attendue max
    risk_label: str = ""
    risk_color: str = "#ef4444"

    # ── Multiplicateur PE numérique ───────────────────────────────
    pe_multiplier: float = 1.0      # Facteur d'allongement PE vs industrie 3.0
    pe_weeks_min: int = 0
    pe_weeks_max: int = 0
    pe_label: str = ""

    # ── Correspondance FAIR → Indices ────────────────────────────
    mapping: Dict[str, str] = field(default_factory=dict)


@dataclass
class FAIRResult:
    """Résultat complet de l'analyse FAIR."""
    composantes: FAIRComponentes = field(default_factory=FAIRComponentes)
    score_indice_a: int = 0
    score_indice_b: int = 0
    score_indice_c: int = 0
    score_global: int = 0
    narrative: str = ""
    limites: list = field(default_factory=list)


# ══════════════════════════════════════════════════════
#  CALCUL TCF — Threat Contact Frequency
# ══════════════════════════════════════════════════════

def _compute_tcf(data: FormData, score_c: int) -> Tuple[float, str]:
    """
    TCF = fréquence à laquelle une menace entre en contact avec les actifs OT.
    Proxy : Indice C (exposition) pondéré par des facteurs contextuels.
    """
    # Base : Indice C normalise la probabilité d'exposition
    tcf = score_c * 0.7  # L'indice C capte 70% du TCF

    # Bonus d'exposition si accès distants non contrôlés
    if data.cps.infrastructure_it.audit_cyber != "oui":
        tcf += 8
    if data.cps.architecture.segmentation_reseau == "Faible":
        tcf += 12
    elif data.cps.architecture.segmentation_reseau == "Moyenne":
        tcf += 5

    # Incidents IT historiques = preuve de contact passé
    inc_map = {"3+/an": 15, "1-2/an": 8, "Aucun": 0}
    tcf += inc_map.get(getattr(data.cps.assurantiel, "historique_incid_it", "Aucun"), 0)

    tcf = min(100, max(0, round(tcf)))

    if tcf >= 70:   label = "Très élevée"
    elif tcf >= 45: label = "Élevée"
    elif tcf >= 25: label = "Modérée"
    else:           label = "Basse"

    return tcf, label


# ══════════════════════════════════════════════════════
#  CALCUL VULNERABILITY
# ══════════════════════════════════════════════════════

def _compute_vulnerability(data: FormData, score_c: int) -> Tuple[float, str]:
    """
    Vulnerability = probabilité que la menace réussisse à exploiter l'actif.
    Proxy : Fragilité IT + absence de défenses actives.
    """
    v = 0.0

    # Absence de défenses actives
    if data.cps.infrastructure_it.parefeu_industriel != "oui":  v += 20
    if data.cps.infrastructure_it.backup_quotidien != "oui":    v += 15
    if data.cps.infrastructure_it.redondance_serveurs != "oui": v += 12
    if data.robots.scoring.maj_firmware != "oui":               v += 10
    if data.cps.assurantiel.simulation_crise != "oui":          v += 8

    # Normaliser sur 100
    v = min(100, max(0, round(v)))

    if v >= 65:   label = "Critique"
    elif v >= 40: label = "Élevée"
    elif v >= 20: label = "Modérée"
    else:         label = "Faible"

    return v, label


# ══════════════════════════════════════════════════════
#  CALCUL LEF — Loss Event Frequency
# ══════════════════════════════════════════════════════

def _compute_lef(tcf: float, vulnerability: float, score_c: int) -> Tuple[float, float, str]:
    """
    LEF = TCF × Vulnerability → fréquence annuelle sinistres.
    Traduit en nombre de sinistres/an attendus.
    """
    # Formule FAIR simplifiée : LEF ∝ TCF × Vulnerability / 10000
    lef_raw = (tcf * vulnerability) / 10000.0

    # Calibration sur données sectorielles (fourchettes)
    if score_c >= 70:
        lef_min, lef_max = 2.0, 5.0
        label = "Très fréquents (2–5 sinistres/an)"
    elif score_c >= 45:
        lef_min, lef_max = 1.0, 2.5
        label = "Fréquents (1–2.5 sinistres/an)"
    elif score_c >= 25:
        lef_min, lef_max = 0.5, 1.2
        label = "Modérés (0.5–1.2 sinistres/an)"
    else:
        lef_min, lef_max = 0.2, 0.8
        label = "Faibles (0.2–0.8 sinistres/an)"

    return lef_min, lef_max, label


# ══════════════════════════════════════════════════════
#  CALCUL LOSS MAGNITUDE
# ══════════════════════════════════════════════════════

def _compute_loss_magnitude(
    data: FormData,
    score_b: int,
    score_c: int
) -> Tuple[float, float, float, float, float, float, float, int, int, str]:
    """
    LM = Primary Loss + Secondary Loss.
    Primary  = dommage matériel direct (bris machine)
    Secondary = PE numérique allongée + pénalités + forensique
    """

    # ── Estimation dommage primaire ────────────────────────────────
    # Basé sur le profil d'équipements et valeurs déclarées
    robots_val = getattr(data.robots.quantitatif, "valeur_totale_parc_mad", None) or 0
    cnc_val    = (getattr(data.cnc.technique, "nombre_cnc", None) or 0) * \
                 (getattr(data.cnc.technique, "valeur_unitaire_mad", None) or 200_000)

    # Estimation basique si pas de données
    base_primary = max(robots_val * 0.15, cnc_val * 0.20, 150_000)
    primary_min = round(base_primary * 0.6, -3)
    primary_max = round(base_primary * 2.5, -3)

    # ── Multiplicateur PE numérique ────────────────────────────────
    # Basé sur Indice B (résilience) et ISP (backup PLC)
    backup_ok   = data.cps.infrastructure_it.backup_quotidien == "oui"
    pca_ok      = data.cps.assurantiel.plan_continuite == "oui"
    mttr        = data.maintenance.indicateurs.mttr_global or 12

    if score_b >= 75 and backup_ok and pca_ok:
        pe_mult = 1.2
        weeks_min, weeks_max = 1, 2
        pe_label = "PE courte — résilience élevée (+20% vs physique)"
    elif score_b >= 55:
        pe_mult = 2.0
        weeks_min, weeks_max = 2, 6
        pe_label = "PE modérée — allongement numérique ×2"
    elif score_b >= 35:
        pe_mult = 4.0
        weeks_min, weeks_max = 4, 16
        pe_label = "PE longue — allongement numérique ×4"
    else:
        pe_mult = 8.0
        weeks_min, weeks_max = 8, 26
        pe_label = "PE critique — reconstruction logicielle / forensique"

    # Marge brute journalière estimée
    ca = data.identification.ca_annuel_mad or 30_000_000
    marge_journaliere = ca * 0.30 / 365

    secondary_min = round(marge_journaliere * weeks_min * 7 * 0.6, -3)
    secondary_max = round(marge_journaliere * weeks_max * 7, -3)

    total_min = primary_min + secondary_min
    total_max = primary_max + secondary_max

    if total_max >= 10_000_000: lm_label = "Catastrophique (>10M MAD)"
    elif total_max >= 3_000_000: lm_label = "Grave (3–10M MAD)"
    elif total_max >= 500_000:  lm_label = "Modérée (500K–3M MAD)"
    else:                       lm_label = "Limitée (<500K MAD)"

    return (
        primary_min, primary_max,
        secondary_min, secondary_max,
        total_min, total_max,
        pe_mult, weeks_min, weeks_max,
        lm_label, pe_label
    )


# ══════════════════════════════════════════════════════
#  CALCUL RISQUE ANNUEL
# ══════════════════════════════════════════════════════

def _compute_annual_risk(
    lef_min: float, lef_max: float,
    total_lm_min: float, total_lm_max: float,
    score_global: int
) -> Tuple[float, float, str, str]:
    """
    Risque annuel = LEF × LM.
    Représente la perte financière annuelle attendue (ALE — Annual Loss Expectancy).
    """
    risk_min = round(lef_min * total_lm_min, -3)
    risk_max = round(lef_max * total_lm_max, -3)

    if score_global >= 80:
        label = "Risque maîtrisé — prime standard"
        color = "#10b981"
    elif score_global >= 65:
        label = "Risque modéré — prime légèrement majorée"
        color = "#3b82f6"
    elif score_global >= 45:
        label = "Risque significatif — prime majorée +15 à 35%"
        color = "#f59e0b"
    elif score_global >= 25:
        label = "Risque élevé — surprime + conditions particulières"
        color = "#ef4444"
    else:
        label = "Risque critique — tarification individuelle / refus"
        color = "#7f1d1d"

    return risk_min, risk_max, label, color


# ══════════════════════════════════════════════════════
#  CORRESPONDANCE FAIR ↔ INDICES
# ══════════════════════════════════════════════════════

def _build_mapping(score_a: int, score_b: int, score_c: int) -> Dict[str, str]:
    """Tableau de correspondance FAIR ↔ Indices du prototype."""
    return {
        "TCF (Threat Contact Frequency)":
            f"Indice C = {score_c} → Exposition cyber OT "
            f"({'élevée' if score_c > 50 else 'maîtrisée'})",
        "Vulnerability":
            f"Fragilité IT + Absence segmentation "
            f"(composantes Indice C)",
        "LEF (Loss Event Frequency)":
            f"f(Indice C = {score_c}) → fréquence sinistres industriels",
        "Primary Loss (PLEF)":
            f"Dommages matériels directs — robots, CNC, SCADA "
            f"(tableau équipements ch.2)",
        "Secondary Loss (SLEF)":
            f"PE numérique × multiplicateur f(Indice B = {score_b}) "
            f"+ pénalités contractuelles",
        "Loss Magnitude (LM)":
            f"f(100 − Indice B = {100 - score_b}) → "
            f"capacité absorption inversée",
        "Risk (LEF × LM)":
            f"Score Global inversé = {100 - score_b * 0.45:.0f} "
            f"→ perte annuelle attendue (ALE)",
    }


# ══════════════════════════════════════════════════════
#  NARRATIVE FAIR
# ══════════════════════════════════════════════════════

def _build_narrative(composantes: FAIRComponentes, score_global: int, nom: str) -> str:
    """Génère la narrative FAIR en langage souscripteur."""
    nom = nom or "Ce site industriel"

    if score_global >= 80:
        return (
            f"{nom} présente un profil FAIR favorable. La fréquence d'exposition aux menaces "
            f"est maîtrisée (TCF : {composantes.tcf_label}) et la capacité d'absorption "
            f"des pertes est élevée. La perte annuelle attendue est bornée et prévisible."
        )
    elif score_global >= 65:
        return (
            f"{nom} présente un profil FAIR intermédiaire. Quelques vulnérabilités résiduelles "
            f"(TCF : {composantes.tcf_label}) sont compensées par une résilience opérationnelle "
            f"correcte. Des mesures de prévention ciblées permettraient de réduire "
            f"significativement la magnitude des pertes secondaires."
        )
    elif score_global >= 45:
        return (
            f"{nom} présente un profil FAIR préoccupant. La fréquence d'exposition "
            f"({composantes.tcf_label}) combinée à une résilience insuffisante génère "
            f"un risque d'allongement PE numérique estimé à ×{composantes.pe_multiplier:.0f} "
            f"par rapport à l'industrie 3.0. Conditions de souscription renforcées recommandées."
        )
    else:
        return (
            f"{nom} présente un profil FAIR critique. L'exposition élevée aux menaces "
            f"({composantes.tcf_label}), combinée à des vulnérabilités structurelles multiples "
            f"et une résilience insuffisante, génère une perte annuelle attendue "
            f"potentiellement catastrophique. Visite terrain et audit OT préalables requis."
        )


# ══════════════════════════════════════════════════════
#  FONCTION PRINCIPALE
# ══════════════════════════════════════════════════════

def compute_fair_analysis(data: FormData, result: ScoreResult) -> FAIRResult:
    """
    Calcule l'analyse FAIR complète à partir des scores du prototype.

    Args:
        data   : FormData — données saisies par l'utilisateur
        result : ScoreResult — résultats déjà calculés par le pipeline

    Returns:
        FAIRResult — analyse FAIR complète
    """
    sa = result.score_maturite
    sb = result.score_resilience
    sc = result.score_vulnerabilite
    sg = result.score_global
    nom = data.identification.entreprise or "Ce site"

    # ── 1. TCF ────────────────────────────────────────────────────
    tcf, tcf_label = _compute_tcf(data, sc)

    # ── 2. Vulnerability ─────────────────────────────────────────
    vuln, vuln_label = _compute_vulnerability(data, sc)

    # ── 3. LEF ────────────────────────────────────────────────────
    lef_min, lef_max, lef_label = _compute_lef(tcf, vuln, sc)

    # ── 4. Loss Magnitude ─────────────────────────────────────────
    (
        primary_min, primary_max,
        secondary_min, secondary_max,
        total_min, total_max,
        pe_mult, weeks_min, weeks_max,
        lm_label, pe_label
    ) = _compute_loss_magnitude(data, sb, sc)

    # ── 5. Risque Annuel ─────────────────────────────────────────
    risk_min, risk_max, risk_label, risk_color = _compute_annual_risk(
        lef_min, lef_max, total_min, total_max, sg
    )

    # ── 6. Correspondance ────────────────────────────────────────
    mapping = _build_mapping(sa, sb, sc)

    # ── 7. Assembler composantes ─────────────────────────────────
    composantes = FAIRComponentes(
        tcf_score=tcf,
        tcf_label=tcf_label,
        vulnerability_score=vuln,
        vulnerability_label=vuln_label,
        lef_annuelle_min=lef_min,
        lef_annuelle_max=lef_max,
        lef_label=lef_label,
        primary_loss_min=primary_min,
        primary_loss_max=primary_max,
        secondary_loss_min=secondary_min,
        secondary_loss_max=secondary_max,
        total_lm_min=total_min,
        total_lm_max=total_max,
        lm_label=lm_label,
        risk_annuel_min=risk_min,
        risk_annuel_max=risk_max,
        risk_label=risk_label,
        risk_color=risk_color,
        pe_multiplier=pe_mult,
        pe_weeks_min=weeks_min,
        pe_weeks_max=weeks_max,
        pe_label=pe_label,
        mapping=mapping,
    )

    # ── 8. Limites du modèle ─────────────────────────────────────
    limites = [
        "Données de fréquence calibrées sur estimations expertes — "
        "la calibration statistique (Phase 2) affiner ces fourchettes.",
        "FAIR standard ne modélise pas la résilience opérationnelle — "
        "l'Indice B comble cette lacune (absent du framework original).",
        "Les pertes secondaires (forensique, pénalités contractuelles) "
        "sont estimées par fourchettes — à affiner lors de la visite de risque.",
    ]

    # ── 9. Narrative ─────────────────────────────────────────────
    narrative = _build_narrative(composantes, sg, nom)

    return FAIRResult(
        composantes=composantes,
        score_indice_a=sa,
        score_indice_b=sb,
        score_indice_c=sc,
        score_global=sg,
        narrative=narrative,
        limites=limites,
    )


def format_mad(valeur: float) -> str:
    """Formate un montant en MAD de manière lisible."""
    if valeur >= 1_000_000:
        return f"{valeur/1_000_000:.1f}M MAD"
    elif valeur >= 1_000:
        return f"{valeur/1_000:.0f}K MAD"
    else:
        return f"{valeur:.0f} MAD"
