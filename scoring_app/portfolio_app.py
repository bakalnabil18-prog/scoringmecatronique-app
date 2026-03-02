import os
import pandas as pd
import streamlit as st

from portfolio import run_one  # réutilise le moteur batch


st.set_page_config(page_title="Portfolio UW Dashboard", layout="wide")
st.title("Portfolio Dashboard — Underwriting IoT")

out_dir = st.text_input("Output directory", value="outputs")
os.makedirs(out_dir, exist_ok=True)

st.subheader("Charger portefeuille")
uploaded = st.file_uploader("Upload CSV", type=["csv"])

default_rows = [
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
    dict(
        equipment_id="PUMP-07", equipment_type="Pump",
        replacement_value=120000, daily_gross_profit=400,
        age_years=10, mtbf_hours=20000, criticality=0.6,
        redundancy=0.2, environment_severity=0.5,
        vibration_mean=3.0, vibration_last=3.6, vibration_slope=0.15,
        temperature_mean=55, temperature_last=65, temperature_slope=0.25,
        current_mean=230, current_last=260, current_slope=0.15,
        power_factor_last=0.92, thd_last=7,
        completeness=0.90, calibration_age_days=420,
        drift_detected=True, latency_seconds=60,
        pm_compliance=0.75, last_pm_days=60, mttr_hours=12,
    ),
    dict(
        equipment_id="INJ-01", equipment_type="Injection",
        replacement_value=500000, daily_gross_profit=1200,
        age_years=14, mtbf_hours=12000, criticality=0.9,
        redundancy=0.1, environment_severity=0.6,
        vibration_mean=4.0, vibration_last=5.5, vibration_slope=0.40,
        temperature_mean=70, temperature_last=90, temperature_slope=0.60,
        current_mean=260, current_last=320, current_slope=0.30,
        power_factor_last=0.85, thd_last=15,
        completeness=0.82, calibration_age_days=700,
        drift_detected=True, latency_seconds=120,
        pm_compliance=0.55, last_pm_days=120, mttr_hours=24,
    ),
]

if uploaded:
    df_in = pd.read_csv(uploaded)
else:
    df_in = pd.DataFrame(default_rows)

st.dataframe(df_in, use_container_width=True)

if st.button("Run portfolio underwriting", type="primary"):
    results = []
    for _, row in df_in.iterrows():
        results.append(run_one(row.to_dict(), out_dir=out_dir))

    df_out = pd.DataFrame(results)

    st.success("Analyse terminée ✅")
    st.dataframe(df_out, use_container_width=True)

    csv_bytes = df_out.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Télécharger résultats CSV",
        data=csv_bytes,
        file_name="portfolio_results.csv",
        mime="text/csv",
    )