from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class SensorSeriesSummary:
    """Résumé de séries temporelles (fenêtre récente)."""
    mean: float
    std: float
    min: float
    max: float
    slope_per_day: float
    last: float

@dataclass
class DataQualityMetrics:
    completeness: float
    latency_seconds: float
    calibration_age_days: int
    drift_flag: bool
    outlier_rate: float

@dataclass
class EquipmentProfile:
    equipment_id: str
    equipment_type: str
    replacement_value: float
    age_years: float
    mtbf_hours: Optional[float]
    criticality: int
    redundancy: bool
    environment_severity: int

@dataclass
class MaintenanceProfile:
    gmao_present: bool
    preventive_compliance: float
    mean_response_days: float
    spare_parts_ready: bool
    last_major_overhaul_days: int

@dataclass
class IoTFeatures:
    vibration: SensorSeriesSummary
    temperature: SensorSeriesSummary
    electrical_current: SensorSeriesSummary
    power_factor_last: Optional[float] = None
    thd_last: Optional[float] = None

@dataclass
class UnderwritingInput:
    equipment: EquipmentProfile
    maintenance: MaintenanceProfile
    data_quality: DataQualityMetrics
    features: IoTFeatures
    as_of: datetime = field(default_factory=datetime.utcnow)

@dataclass
class GateResult:
    eligible: bool
    conditions: List[str]
    reasons: List[str]
    dq_score: int

@dataclass
class HealthScoreResult:
    score: int
    band: str
    drivers: List[str]

@dataclass
class SurvivalResult:
    p_fail_30d: float
    p_fail_90d: float
    rul_days: int
    hazard_level: str
    explanation: List[str]

@dataclass
class UWDecision:
    decision: str
    risk_tier: str
    recommended_deductible_hours: int
    recommended_limit_dm: float
    recommended_limit_bi: float
    base_premium: float
    adjusted_premium: float
    clauses: List[str]
    drivers: List[str]
