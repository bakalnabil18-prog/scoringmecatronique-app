from __future__ import annotations

from dataclasses import dataclass
from typing import List


# =========================================================
# UnderwritingDecision — version standardisée (UI + reporting)
# =========================================================

@dataclass
class UnderwritingDecision:
    decision: str
    risk_tier: str

    # Champs "standard" attendus par l'app/reporting
    recommended_deductible_hours: int
    recommended_limit_dm: float
    recommended_limit_bi: float

    base_premium: float
    adjusted_premium: float

    clauses: List[str]
    drivers: List[str]

    # --- Compatibilité avec anciens noms (si d'autres modules utilisent dm_limit/bi_limit) ---
    @property
    def dm_limit(self) -> float:
        return self.recommended_limit_dm

    @property
    def bi_limit(self) -> float:
        return self.recommended_limit_bi


# =========================================================
# Underwriting logic (simple & robuste)
# =========================================================

def underwriting_decision(
    equipment,
    maintenance,
    data_quality,
    health_score: float,
    failure_probability_30d: float,
    rul_days: float,
) -> UnderwritingDecision:

    drivers: List[str] = []
    clauses: List[str] = []

    # ---------------------------------------------
    # 1) Health band
    # ---------------------------------------------
    if health_score >= 75:
        band = "GREEN"
    elif health_score >= 50:
        band = "YELLOW"
    else:
        band = "RED"

    drivers.append(f"Health Score={health_score:.0f} ({band})")
    drivers.append(f"P(fail 30d)={failure_probability_30d*100:.2f}%, RUL≈{int(rul_days)} jours")

    # ---------------------------------------------
    # 2) Base decision / tier / deductible
    # ---------------------------------------------
    if band == "GREEN":
        decision = "ACCEPT"
        risk_tier = "A"
        deductible = 48
        clauses.append("Reporting mensuel Health Score + alertes critiques.")
    elif band == "YELLOW":
        decision = "ACCEPT_WITH_CONDITIONS"
        risk_tier = "C"
        deductible = 120
        clauses.append("Reporting mensuel Health Score + alertes critiques.")
        clauses.append("Recalibrer capteurs sous 30 jours.")
    else:
        decision = "ACCEPT_WITH_CONDITIONS"
        risk_tier = "C"
        deductible = 120
        clauses.append("Maintenance urgente sous 7 jours + re-audit avant maintien couverture.")
        clauses.append("Révision trimestrielle obligatoire (Health Score + P(panne)).")

    # ---------------------------------------------
    # 3) Data quality impact (si score dispo)
    # ---------------------------------------------
    dq_score = getattr(data_quality, "score", None)
    if dq_score is not None:
        drivers.append(f"DQ Score={float(dq_score):.0f}/100")
        if float(dq_score) < 75:
            clauses.append("Mettre en place détection de drift.")
            clauses.append("Améliorer qualité des données IoT.")

    # ---------------------------------------------
    # 4) Flags électriques si dispo dans features/equipment (selon ton modèle)
    # ---------------------------------------------
    # On essaie plusieurs emplacements possibles (selon ton data_models)
    pf = getattr(getattr(equipment, "features", None), "power_factor_last", None)
    if pf is None:
        pf = getattr(equipment, "power_factor_last", None)

    thd = getattr(getattr(equipment, "features", None), "thd_last", None)
    if thd is None:
        thd = getattr(equipment, "thd_last", None)

    if pf is not None and pf < 0.90:
        drivers.append("Power factor bas (<0.90) → déséquilibre/charge réactive.")

    if thd is not None and thd > 10:
        drivers.append("THD élevé (>10%) → harmoniques / risque défaut électrique.")

    # ---------------------------------------------
    # 5) Limits (DM + BI)
    # ---------------------------------------------
    replacement_value = float(getattr(equipment, "replacement_value", 100000.0))

    recommended_limit_dm = replacement_value
    # proxy BI: exemple 6.575% de DM (tu peux adapter)
    recommended_limit_bi = replacement_value * 0.06575

    # ---------------------------------------------
    # 6) Premium (proxy actuariel simple)
    # ---------------------------------------------
    base_rate = 0.017  # 1.7%
    base_premium = recommended_limit_dm * base_rate

    # surcharge selon band
    if band == "RED":
        adjusted_premium = base_premium * 1.6
        drivers.append("Health band RED pénalise le risque.")
    elif band == "YELLOW":
        adjusted_premium = base_premium * 1.15
    else:
        adjusted_premium = base_premium

    # Clause minimale commune
    clauses.append("Accès read-only aux logs IoT + journal des interventions maintenance.")

    # ---------------------------------------------
    # 7) Return (avec noms attendus par l'app)
    # ---------------------------------------------
    return UnderwritingDecision(
        decision=decision,
        risk_tier=risk_tier,
        recommended_deductible_hours=int(deductible),
        recommended_limit_dm=float(recommended_limit_dm),
        recommended_limit_bi=float(recommended_limit_bi),
        base_premium=float(base_premium),
        adjusted_premium=float(adjusted_premium),
        clauses=clauses,
        drivers=drivers,
    )