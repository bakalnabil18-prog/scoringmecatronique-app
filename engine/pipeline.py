from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List

from .data_models import UnderwritingInput
from .data_quality import data_quality_gate
from .health_score import compute_health_score
from .survival import compute_survival
from .underwriting import underwriting_decision, UnderwritingDecision


def _safe_get(obj: Any, name: str, default=None):
    return getattr(obj, name, default)


def _band_from_score(score: float) -> str:
    if score >= 75:
        return "GREEN"
    if score >= 50:
        return "YELLOW"
    return "RED"


@dataclass
class HealthAdapter:
    score: float
    band: str
    drivers: List[str]


# =========================================================
# ⭐⭐⭐ FONCTION PRINCIPALE (celle que Streamlit importe)
# =========================================================
def run_underwriting(uw_in: UnderwritingInput) -> UnderwritingDecision:
    """
    Pipeline assureur complet.
    """

    # -----------------------------
    # 1) Data Quality
    # -----------------------------
    dq_metrics = data_quality_gate(uw_in.data_quality)

    # -----------------------------
    # 2) Health score
    # -----------------------------
    try:
        health_raw = compute_health_score(
            uw_in.features,
            uw_in.equipment,
            uw_in.maintenance,
        )
    except TypeError:
        try:
            health_raw = compute_health_score(uw_in.features)
        except TypeError:
            health_raw = compute_health_score(features=uw_in.features)

    # Adapter → garantir .score + .band
    if isinstance(health_raw, (int, float)):
        score = float(health_raw)
        health = HealthAdapter(
            score=score,
            band=_band_from_score(score),
            drivers=[],
        )
    else:
        score = float(_safe_get(health_raw, "score", 0.0))
        band = _safe_get(health_raw, "band", _band_from_score(score))
        drivers = list(_safe_get(health_raw, "drivers", []))
        health = HealthAdapter(score=score, band=str(band), drivers=drivers)

    # -----------------------------
    # 3) Survival
    # -----------------------------
    survival = None

    try:
        survival = compute_survival(uw_in.equipment, uw_in.maintenance, health)
    except TypeError:
        pass

    if survival is None:
        try:
            survival = compute_survival(health)
        except TypeError:
            pass

    if survival is None:
        try:
            survival = compute_survival(float(health.score))
        except TypeError as e:
            raise TypeError(
                "Signature compute_survival incompatible."
            ) from e

    p30 = _safe_get(survival, "prob_30d", _safe_get(survival, "p_fail_30d", None))
    rul_days = _safe_get(survival, "rul_days", _safe_get(survival, "rul", None))
    hazard = _safe_get(survival, "hazard_level", _safe_get(survival, "hazard", None))

    if p30 is None or rul_days is None:
        raise ValueError(
            "compute_survival() doit retourner prob_30d et rul_days."
        )

    # -----------------------------
    # 4) Underwriting decision
    # -----------------------------
    decision = underwriting_decision(
        equipment=uw_in.equipment,
        maintenance=uw_in.maintenance,
        data_quality=dq_metrics,
        health_score=float(health.score),
        failure_probability_30d=float(p30),
        rul_days=float(rul_days),
    )

    # Enrichissement drivers
    extra: List[str] = []
    extra.append(f"Health band={health.band}")
    extra.append(f"P(fail 30d)={float(p30)*100:.2f}%, RUL≈{int(float(rul_days))} jours")

    if hazard is not None:
        extra.append(f"hazard={hazard}")

    dq_score = _safe_get(dq_metrics, "score", None)
    if dq_score is not None:
        extra.append(f"DQ Score={float(dq_score):.0f}/100")

    for d in health.drivers:
        extra.append(d)

    if hasattr(decision, "drivers"):
        for line in extra:
            if line not in decision.drivers:
                decision.drivers.append(line)

    return decision