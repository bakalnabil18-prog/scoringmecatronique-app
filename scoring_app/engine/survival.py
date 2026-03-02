import math
from .data_models import EquipmentProfile, MaintenanceProfile, HealthScoreResult, SurvivalResult


def weibull_survival(t_days: float, eta_days: float, beta: float) -> float:
    """Fonction de survie Weibull."""
    return math.exp(-((t_days / max(1e-6, eta_days)) ** beta))


def hazard_proxy(health: int, age_years: float,
                 maintenance: MaintenanceProfile,
                 criticality: int) -> float:
    """
    Proxy de risque 0..1.
    Plus proche de 1 = plus risqué.
    """
    h = 1 - (health / 100)                    # santé faible = risque haut
    a = min(1.0, age_years / 20.0)            # âge normalisé
    m = 1 - maintenance.preventive_compliance
    c = (criticality - 1) / 4.0

    proxy = 0.45*h + 0.25*a + 0.20*m + 0.10*c
    return max(0.0, min(1.0, proxy))


def compute_survival(
    equip: EquipmentProfile,
    maint: MaintenanceProfile,
    health: HealthScoreResult
) -> SurvivalResult:

    expl = []

    # =============================
    # 1) Proxy de risque
    # =============================
    hz = hazard_proxy(health.score, equip.age_years, maint, equip.criticality)

    # =============================
    # 2) Paramètres Weibull adaptatifs
    # =============================
    base_eta = 365 * 3  # 3 ans (hypothèse PFE)

    eta = base_eta * (1.2 - hz)
    eta = max(90, eta)

    beta = 1.5 + 2.0 * hz

    # =============================
    # 3) Probabilités brutes
    # =============================
    p30 = 1 - weibull_survival(30, eta, beta)
    p90 = 1 - weibull_survival(90, eta, beta)

    # =============================
    # 🔴 4) SANITY UNDERWRITING (CRITIQUE PFE)
    # =============================
    # On empêche une incohérence :
    # Health très mauvais ⇒ risque minimum imposé

    if health.band == "RED":
        p30 = max(p30, 0.25)
        p90 = max(p90, 0.55)
        expl.append("Override UW: Health RED ⇒ plancher de risque appliqué.")

    elif health.band == "ORANGE":
        p30 = max(p30, 0.12)
        p90 = max(p90, 0.35)
        expl.append("Override UW: Health ORANGE ⇒ plancher de risque appliqué.")

    # =============================
    # 5) RUL médian
    # =============================
    rul = int(round(eta * (math.log(2) ** (1.0 / beta))))
    rul = max(1, rul)

    # =============================
    # 6) Hazard level underwriting
    # =============================
    if p30 < 0.05:
        lvl = "LOW"
    elif p30 < 0.15:
        lvl = "MED"
    elif p30 < 0.30:
        lvl = "HIGH"
    else:
        lvl = "CRIT"

    # =============================
    # 7) Explications métier
    # =============================
    if health.band in ("ORANGE", "RED"):
        expl.append(f"Health band {health.band} pénalise le risque (score={health.score}).")

    if equip.age_years > 15:
        expl.append("Âge élevé → modes de défaillance plus imprévisibles.")

    if maint.preventive_compliance < 0.7:
        expl.append("Préventif insuffisant → risque accru.")

    expl.append(f"Weibull ajusté: eta≈{int(eta)}j, beta≈{beta:.2f}, proxy={hz:.2f}.")

    return SurvivalResult(
        p_fail_30d=float(p30),
        p_fail_90d=float(p90),
        rul_days=rul,
        hazard_level=lvl,
        explanation=expl
    )
