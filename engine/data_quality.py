from .data_models import DataQualityMetrics, GateResult

def compute_dq_score(dq: DataQualityMetrics) -> int:
    # Completeness
    if dq.completeness >= 0.98:
        c = 95
    elif dq.completeness >= 0.95:
        c = 85
    elif dq.completeness >= 0.90:
        c = 70
    else:
        c = 40

    # Latency
    if dq.latency_seconds <= 60:
        l = 95
    elif dq.latency_seconds <= 3600:
        l = 85
    elif dq.latency_seconds <= 86400:
        l = 60
    else:
        l = 35

    # Calibration
    if dq.calibration_age_days <= 365:
        cal = 90
    elif dq.calibration_age_days <= 730:
        cal = 65
    else:
        cal = 35

    # Outliers
    if dq.outlier_rate <= 0.01:
        o = 90
    elif dq.outlier_rate <= 0.05:
        o = 70
    else:
        o = 45

    # Drift
    d = 40 if dq.drift_flag else 90

    score = round(
        0.35 * c +
        0.20 * l +
        0.20 * cal +
        0.15 * o +
        0.10 * d
    )
    return max(0, min(100, score))


def data_quality_gate(dq: DataQualityMetrics) -> GateResult:
    score = compute_dq_score(dq)
    conditions = []
    reasons = []

    eligible = True

    # Blocages forts
    if dq.completeness < 0.90:
        eligible = False
        reasons.append("Complétude < 90%.")

    if dq.calibration_age_days > 730:
        eligible = False
        reasons.append("Calibration capteurs > 2 ans.")

    if dq.latency_seconds > 86400:
        eligible = False
        reasons.append("Latence > 24h.")

    # Conditions non bloquantes
    if dq.drift_flag:
        conditions.append("Mettre en place détection de drift.")

    if 0.90 <= dq.completeness < 0.95:
        conditions.append("Améliorer complétude ≥95%.")

    if 365 < dq.calibration_age_days <= 730:
        conditions.append("Recalibrer capteurs sous 30 jours.")

    return GateResult(
        eligible=eligible,
        conditions=conditions,
        reasons=reasons,
        dq_score=score
    )
