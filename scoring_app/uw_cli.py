from datetime import datetime

from engine.data_models import (
    SensorSeriesSummary, DataQualityMetrics, EquipmentProfile,
    MaintenanceProfile, IoTFeatures, UnderwritingInput
)
from engine.pipeline import run_underwriting
from engine.reporting import save_underwriting_report


def ask_float(prompt, default):
    val = input(f"{prompt} [{default}]: ").strip()
    return float(val) if val else float(default)


def ask_int(prompt, default):
    val = input(f"{prompt} [{default}]: ").strip()
    return int(val) if val else int(default)


def ask_bool(prompt, default):
    val = input(f"{prompt} (y/n) [{default}]: ").strip().lower()
    if not val:
        return default.lower() == "y"
    return val.startswith("y")


def main():
    print("\n=== UNDERWRITING TOOL — IoT Equipment ===")

    # ===== Equipment =====
    equipment = EquipmentProfile(
        equipment_id=input("Equipment ID [EQ-01]: ") or "EQ-01",
        equipment_type=input("Type [Machine]: ") or "Machine",
        replacement_value=ask_float("Replacement value", 200000),
        age_years=ask_float("Age (years)", 5),
        mtbf_hours=ask_float("MTBF (hours)", 40000),
        criticality=ask_int("Criticality (1-5)", 3),
        redundancy=ask_bool("Redundancy available?", "n"),
        environment_severity=ask_int("Environment severity (1-5)", 3),
    )

    # ===== Maintenance =====
    maintenance = MaintenanceProfile(
        gmao_present=True,
        preventive_compliance=ask_float("Preventive compliance (0-1)", 0.85),
        mean_response_days=ask_float("Mean response days", 7),
        spare_parts_ready=ask_bool("Spare parts ready?", "y"),
        last_major_overhaul_days=ask_int("Last overhaul (days)", 300),
    )

    # ===== Data Quality =====
    dq = DataQualityMetrics(
        completeness=ask_float("Data completeness (0-1)", 0.95),
        latency_seconds=ask_float("Latency (sec)", 60),
        calibration_age_days=ask_int("Calibration age (days)", 200),
        drift_flag=ask_bool("Drift detected?", "n"),
        outlier_rate=ask_float("Outlier rate (0-1)", 0.02),
    )

    # ===== IoT =====
    features = IoTFeatures(
        vibration=SensorSeriesSummary(
            mean=ask_float("Vibration mean", 2.5),
            std=0.3,
            min=2.0,
            max=4.0,
            slope_per_day=ask_float("Vibration slope/day", 0.1),
            last=ask_float("Vibration last", 2.8),
        ),
        temperature=SensorSeriesSummary(
            mean=ask_float("Temperature mean", 45),
            std=4,
            min=40,
            max=80,
            slope_per_day=ask_float("Temperature slope/day", 0.2),
            last=ask_float("Temperature last", 55),
        ),
        electrical_current=SensorSeriesSummary(
            mean=ask_float("Current mean", 200),
            std=15,
            min=180,
            max=300,
            slope_per_day=ask_float("Current slope/day", 0.1),
            last=ask_float("Current last", 230),
        ),
        power_factor_last=ask_float("Power factor", 0.95),
        thd_last=ask_float("THD (%)", 5),
    )

    uw_in = UnderwritingInput(
        equipment=equipment,
        maintenance=maintenance,
        data_quality=dq,
        features=features,
        as_of=datetime.utcnow(),
    )

    decision = run_underwriting(uw_in)
    save_underwriting_report(uw_in, decision, out_dir="outputs")

    print("\n=== RESULT ===")
    print("Decision:", decision.decision)
    print("Risk tier:", decision.risk_tier)
    print("Adjusted premium:", round(decision.adjusted_premium, 2))
    print("Report saved in outputs/")


if __name__ == "__main__":
    main()
