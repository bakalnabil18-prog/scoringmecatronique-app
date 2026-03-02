import os
import pandas as pd

from engine.pipeline import run_underwriting
from engine.reporting import save_underwriting_report
import engine.data_models as dm


# -------------------------------------------------
# Utils robustes (compatibilité noms classes)
# -------------------------------------------------
def pick_attr(module, names):
    for n in names:
        if hasattr(module, n):
            return getattr(module, n)
    raise ImportError(f"Aucune classe trouvée parmi: {names}")


EquipmentCls = pick_attr(dm, ["EquipmentProfile", "EquipmentInfo", "Equipment"])
MaintenanceCls = pick_attr(dm, ["MaintenanceProfile", "MaintenanceInfo", "Maintenance"])
DataQualityCls = pick_attr(dm, ["DataQualityMetrics", "DataQualityInfo", "DataQuality"])
FeaturesOuterCls = pick_attr(dm, ["IoTFeatures", "Features", "EquipmentFeatures"])
SensorSummaryCls = pick_attr(dm, ["SensorSeriesSummary", "SensorSummary"])
UnderwritingInputCls = pick_attr(dm, ["UnderwritingInput"])


def build_instance(cls, **kwargs):
    try:
        return cls(**kwargs)
    except TypeError:
        allowed = {}
        ann = getattr(cls, "__annotations__", {})
        for k, v in kwargs.items():
            if k in ann:
                allowed[k] = v
        return cls(**allowed)


# -------------------------------------------------
# Build features
# -------------------------------------------------
def build_features(row):
    summary = build_instance(
        SensorSummaryCls,
        vibration_mean=row["vibration_mean"],
        vibration_last=row["vibration_last"],
        vibration_slope=row["vibration_slope"],
        temperature_mean=row["temperature_mean"],
        temperature_last=row["temperature_last"],
        temperature_slope=row["temperature_slope"],
        current_mean=row["current_mean"],
        current_last=row["current_last"],
        current_slope=row["current_slope"],
        power_factor_last=row["power_factor_last"],
        thd_last=row["thd_last"],
    )

    try:
        return build_instance(
            FeaturesOuterCls,
            summary=summary,
            sensors=summary,
            series=summary,
            data=summary,
            features=summary,
        )
    except TypeError:
        return summary


# -------------------------------------------------
# Run underwriting for one equipment
# -------------------------------------------------
def run_one(row, out_dir="outputs"):
    equipment = build_instance(
        EquipmentCls,
        equipment_id=row["equipment_id"],
        equipment_type=row["equipment_type"],
        replacement_value=row["replacement_value"],
        daily_gross_profit=row["daily_gross_profit"],
        age_years=row["age_years"],
        mtbf_hours=row["mtbf_hours"],
        criticality=row["criticality"],
        redundancy=row["redundancy"],
        environment_severity=row["environment_severity"],
    )

    maintenance = build_instance(
        MaintenanceCls,
        pm_compliance=row["pm_compliance"],
        last_pm_days=row["last_pm_days"],
        mttr_hours=row["mttr_hours"],
    )

    dq = build_instance(
        DataQualityCls,
        completeness=row["completeness"],
        calibration_age_days=row["calibration_age_days"],
        drift_detected=row["drift_detected"],
        latency_seconds=row["latency_seconds"],
    )

    features = build_features(row)

    uw_in = build_instance(
        UnderwritingInputCls,
        equipment=equipment,
        maintenance=maintenance,
        data_quality=dq,
        features=features,
    )

    decision = run_underwriting(uw_in)
    save_underwriting_report(uw_in, decision, out_dir=out_dir)

    return {
        "equipment_id": row["equipment_id"],
        "decision": decision.decision,
        "tier": decision.risk_tier,
        "adjusted_premium": float(decision.adjusted_premium),
    }


# -------------------------------------------------
# MAIN
# -------------------------------------------------
def main():
    os.makedirs("outputs", exist_ok=True)

    # portefeuille exemple
    data = [
        dict(
            equipment_id="CNC-01", equipment_type="CNC",
            replacement_value=350000, daily_gross_profit=800,
            age_years=6, mtbf_hours=40000, criticality=0.7,
            redundancy=0.4, environment_severity=0.2,
            vibration_mean=2.2, vibration_last=2.3, vibration_slope=0.02,
            temperature_mean=45, temperature_last=48, temperature_slope=0.05,
            current_mean=200, current_last=210, current_slope=0.05,
            power_factor_last=0.96, thd_last=4,
            completeness=0.97, calibration_age_days=120,
            drift_detected=False, latency_seconds=20,
            pm_compliance=0.95, last_pm_days=20, mttr_hours=6,
        ),
    ]

    df = pd.DataFrame(data)

    results = []
    for _, row in df.iterrows():
        results.append(run_one(row.to_dict()))

    print("\n=== PORTFOLIO RESULTS ===")
    print(pd.DataFrame(results))


if __name__ == "__main__":
    main()