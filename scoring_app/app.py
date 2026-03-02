from datetime import datetime
from engine.data_models import (
    SensorSeriesSummary, DataQualityMetrics, EquipmentProfile,
    MaintenanceProfile, IoTFeatures, UnderwritingInput
)
from engine.pipeline import run_underwriting

def main():
    equipment = EquipmentProfile(
        equipment_id="INJ-01",
        equipment_type="Injection",
        replacement_value=500_000,
        age_years=8,
        mtbf_hours=40_000,
        criticality=5,
        redundancy=False,
        environment_severity=3
    )

    maintenance = MaintenanceProfile(
        gmao_present=True,
        preventive_compliance=0.82,
        mean_response_days=10,
        spare_parts_ready=True,
        last_major_overhaul_days=420
    )

    dq = DataQualityMetrics(
        completeness=0.96,
        latency_seconds=120,
        calibration_age_days=240,
        drift_flag=False,
        outlier_rate=0.02
    )

    features = IoTFeatures(
        vibration=SensorSeriesSummary(mean=2.5, std=0.3, min=1.9, max=4.2, slope_per_day=0.25, last=3.8),
        temperature=SensorSeriesSummary(mean=48, std=4, min=40, max=85, slope_per_day=0.60, last=82),
        electrical_current=SensorSeriesSummary(mean=250, std=20, min=220, max=340, slope_per_day=0.18, last=310),
        power_factor_last=0.88,
        thd_last=12.0
    )

    uw_in = UnderwritingInput(
        equipment=equipment,
        maintenance=maintenance,
        data_quality=dq,
        features=features,
        as_of=datetime.utcnow()
    )

    decision = run_underwriting(uw_in)

    print("\n=== UNDERWRITING RESULT ===")
    print("Decision:", decision.decision)
    print("Risk tier:", decision.risk_tier)
    print("Deductible (hours):", decision.recommended_deductible_hours)
    print("DM limit:", decision.recommended_limit_dm)
    print("BI limit:", round(decision.recommended_limit_bi, 2))
    print("Base premium:", round(decision.base_premium, 2))
    print("Adjusted premium:", round(decision.adjusted_premium, 2))
    print("\nClauses:")
    for c in decision.clauses:
        print("-", c)

    print("\nKey drivers:")
    for d in decision.drivers[:12]:
        print("-", d)

if __name__ == "__main__":
    main()
