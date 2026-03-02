import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from .data_models import UnderwritingInput, UWDecision


def _json_safe(obj):
    """Convertit objets non sérialisables (datetime…)."""
    if isinstance(obj, datetime):
        return obj.isoformat() + "Z"
    raise TypeError(f"Type non sérialisable: {type(obj)}")


def save_underwriting_report(uw_in: UnderwritingInput, decision: UWDecision, out_dir: str = "outputs") -> None:
    Path(out_dir).mkdir(parents=True, exist_ok=True)

    payload = {
        "meta": {
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "equipment_id": uw_in.equipment.equipment_id,
            "equipment_type": uw_in.equipment.equipment_type,
            "as_of": uw_in.as_of.isoformat() + "Z",
        },
        "input": asdict(uw_in),
        "decision": asdict(decision),
    }

    base = f"uw_report_{uw_in.equipment.equipment_id}"
    json_path = Path(out_dir) / f"{base}.json"
    txt_path = Path(out_dir) / f"{base}.txt"

    # ✅ FIX ICI : default=_json_safe
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False, default=_json_safe)

    # ===== Version texte =====
    lines = []
    lines.append("RAPPORT DE SOUSCRIPTION – Panne Équipement + IoT + Maintenance Prédictive")
    lines.append("=" * 78)
    lines.append(f"Équipement        : {uw_in.equipment.equipment_id} ({uw_in.equipment.equipment_type})")
    lines.append(f"Date analyse      : {payload['meta']['generated_at']}")
    lines.append("")
    lines.append("1) DÉCISION")
    lines.append(f"- Décision        : {decision.decision}")
    lines.append(f"- Tier de risque   : {decision.risk_tier}")
    lines.append(f"- Franchise temps  : {decision.recommended_deductible_hours} h")
    lines.append("")
    lines.append("2) PARAMÈTRES RECOMMANDÉS")
    lines.append(f"- Limite DM        : {decision.recommended_limit_dm:,.0f}")
    lines.append(f"- Limite PE (BI)   : {decision.recommended_limit_bi:,.0f}")
    lines.append(f"- Prime base       : {decision.base_premium:,.2f}")
    lines.append(f"- Prime ajustée    : {decision.adjusted_premium:,.2f}")
    lines.append("")
    lines.append("3) CLAUSES / CONDITIONS")
    for c in decision.clauses:
        lines.append(f"- {c}")
    lines.append("")
    lines.append("4) DRIVERS TECHNIQUES")
    for d in decision.drivers[:18]:
        lines.append(f"- {d}")

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
