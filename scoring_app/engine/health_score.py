from .data_models import IoTFeatures, HealthScoreResult

def _band(score: int) -> str:
    if score >= 75:
        return "GREEN"
    if score >= 50:
        return "YELLOW"
    if score >= 25:
        return "ORANGE"
    return "RED"

def _score_component_from_ratio(ratio: float, slope_per_day: float, penalties: int = 0) -> int:
    """
    ratio = last / baseline (ici baseline ~ mean, simplification PFE)
    slope_per_day = tendance (positive = dégradation)
    """
    # Base selon ratio
    if ratio <= 1.05:
        s = 85
    elif ratio <= 1.15:
        s = 70
    elif ratio <= 1.30:
        s = 50
    elif ratio <= 1.50:
        s = 30
    else:
        s = 10

    # Pénalité tendance
    if slope_per_day > 0.5:
        s -= 20
    elif slope_per_day > 0.2:
        s -= 10
    elif slope_per_day < -0.1:
        s += 5

    s -= penalties
    return max(0, min(100, s))

def compute_health_score(features: IoTFeatures) -> HealthScoreResult:
    drivers = []

    vib_ratio = features.vibration.last / max(1e-6, features.vibration.mean)
    temp_ratio = features.temperature.last / max(1e-6, features.temperature.mean)
    cur_ratio = features.electrical_current.last / max(1e-6, features.electrical_current.mean)

    # Pénalités électriques
    elec_pen = 0
    if features.power_factor_last is not None and features.power_factor_last < 0.90:
        elec_pen += 15
        drivers.append("Power factor bas (<0.90) → déséquilibre/charge réactive.")
    if features.thd_last is not None and features.thd_last > 10:
        elec_pen += 10
        drivers.append("THD élevé (>10%) → harmoniques / risque défaut électrique.")

    vib = _score_component_from_ratio(vib_ratio, features.vibration.slope_per_day)
    tmp = _score_component_from_ratio(temp_ratio, features.temperature.slope_per_day)
    ele = _score_component_from_ratio(cur_ratio, features.electrical_current.slope_per_day, penalties=elec_pen)

    # Pondération globale (simple et défendable)
    score = round(0.40 * vib + 0.30 * tmp + 0.30 * ele)

    # Drivers explicatifs
    if vib_ratio > 1.30:
        drivers.append("Vibration élevée vs baseline → roulements/désalignement probable.")
    if temp_ratio > 1.30:
        drivers.append("Température élevée vs baseline → surchauffe / lubrification/refroidissement.")
    if cur_ratio > 1.30:
        drivers.append("Courant élevé vs baseline → surcharge / frottement / rendement dégradé.")
    if features.vibration.slope_per_day > 0.2:
        drivers.append("Tendance vibration en hausse (dégradation accélérée).")
    if features.temperature.slope_per_day > 0.2:
        drivers.append("Tendance température en hausse (risque imminent).")

    band = _band(score)
    return HealthScoreResult(score=score, band=band, drivers=drivers)
