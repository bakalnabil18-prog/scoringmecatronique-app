"""
Advanced Scoring Module
Scoring professionnel multi-piliers pour l'assurance industrielle
"""

from dataclasses import dataclass
from typing import List, Dict
import numpy as np


@dataclass
class RobustnessScore:
    """Robustesse mécatronique (0-100)"""
    score: float
    drivers: List[str]
    details: Dict


@dataclass
class MaintenanceScore:
    """Maturité de maintenance (0-100)"""
    score: float
    drivers: List[str]
    details: Dict


@dataclass
class GovernanceScore:
    """Gouvernance technique (0-100)"""
    score: float
    drivers: List[str]
    details: Dict


@dataclass
class AdvancedScoringResult:
    """Résultat complet du scoring avancé"""
    global_score: float
    risk_level: str  # "FAIBLE" / "MOYEN" / "ÉLEVÉ"
    robustness: RobustnessScore
    maintenance: MaintenanceScore
    governance: GovernanceScore
    dominant_risks: List[str]
    recommendations: List[str]
    prevention_priorities: List[str]


# ============================================================
# 1️⃣ SCORING ROBUSTESSE MÉCATRONIQUE
# ============================================================

def score_robustness(
    equipment_age_years: float,
    automation_level: int,  # 1=manual, 2=semi-auto, 3=full-auto, 4=IoT
    sensor_coverage: int,   # 1=none, 2=basic, 3=advanced, 4=comprehensive
    redundancy: float,      # 0-1
    control_system_type: str,  # "legacy" / "modern" / "advanced"
    vibration_health: float,  # 0-100
    temperature_health: float,  # 0-100
    electrical_health: float,  # 0-100
) -> RobustnessScore:
    """
    Scoring de la robustesse mécatronique.
    
    Facteurs:
    - Âge de l'équipement (plus récent = meilleur)
    - Niveau d'automatisation (plus élevé = détection meilleure)
    - Couverture capteurs (plus complète = meilleure visibilité)
    - Redondance (> 0 = résilience)
    - Type de système de contrôle (moderne > legacy)
    - Santé capteurs (vibration, température, électrique)
    """
    
    drivers = []
    details = {}
    
    # --- Age equipment ---
    if equipment_age_years <= 5:
        age_score = 95
        drivers.append("✓ Équipement récent (< 5 ans) → faible risque structurel")
    elif equipment_age_years <= 10:
        age_score = 85
        drivers.append("⚠ Équipement moyen âge (5-10 ans) → risque structurel modéré")
    elif equipment_age_years <= 15:
        age_score = 70
        drivers.append("⚠ Équipement vieillissant (10-15 ans) → dégradation progressive")
    else:
        age_score = 50
        drivers.append("❌ Équipement ancien (> 15 ans) → risque structurel élevé")
    
    details['age_score'] = age_score
    
    # --- Automation level ---
    automation_scores = {1: 40, 2: 60, 3: 85, 4: 95}
    automation_score = automation_scores.get(automation_level, 40)
    
    if automation_level == 1:
        drivers.append("⚠ Équipement manuel → faible détectabilité des anomalies")
    elif automation_level == 2:
        drivers.append("⚠ Semi-automatisé → détectabilité intermédiaire")
    elif automation_level == 3:
        drivers.append("✓ Automatisé → détection précoce possible")
    else:
        drivers.append("✓✓ Connecté IoT → excellente visibilité temps-réel")
    
    details['automation_score'] = automation_score
    
    # --- Sensor coverage ---
    sensor_scores = {1: 30, 2: 55, 3: 80, 4: 95}
    sensor_score = sensor_scores.get(sensor_coverage, 30)
    
    if sensor_coverage == 1:
        drivers.append("❌ Aucune instrumentation → aveugle aux dérives")
    elif sensor_coverage == 2:
        drivers.append("⚠ Instrumentation basique → couverture limitée")
    elif sensor_coverage == 3:
        drivers.append("✓ Instrumentation avancée → couverture satisfaisante")
    else:
        drivers.append("✓✓ Instrumentation complète → détection exhaustive")
    
    details['sensor_score'] = sensor_score
    
    # --- Redundancy ---
    redundancy_score = 50 + (redundancy * 50)  # 50 si pas de redondance, 100 si redondance totale
    
    if redundancy == 0:
        drivers.append("❌ Pas de redondance → risque de perte d'exploitation total")
    elif redundancy < 0.5:
        drivers.append("⚠ Redondance partielle → résilience limitée")
    else:
        drivers.append("✓ Redondance présente → perte d'exploitation réduite")
    
    details['redundancy_score'] = redundancy_score
    
    # --- Control system ---
    control_scores = {"legacy": 50, "modern": 80, "advanced": 95}
    control_score = control_scores.get(control_system_type, 50)
    
    if control_system_type == "legacy":
        drivers.append("❌ PLC/SCADA legacy → maintenance complexe")
    elif control_system_type == "modern":
        drivers.append("✓ Système de contrôle moderne → facilité de maintenance")
    else:
        drivers.append("✓✓ Système avancé → excellente maintenabilité")
    
    details['control_score'] = control_score
    
    # --- Sensor health (moyenne) ---
    health_avg = (vibration_health + temperature_health + electrical_health) / 3
    health_score = health_avg * 0.8 + 20  # Normalize to 0-100
    
    if health_avg < 30:
        drivers.append("❌ Santé capteurs critique → intervention urgente")
    elif health_avg < 60:
        drivers.append("⚠ Santé capteurs dégradée → surveillance requise")
    else:
        drivers.append("✓ Santé capteurs acceptable")
    
    details['health_score'] = health_score
    
    # --- Global robustness ---
    robustness_score = np.mean([
        age_score * 0.2,
        automation_score * 0.2,
        sensor_score * 0.2,
        redundancy_score * 0.2,
        control_score * 0.15,
        health_score * 0.05
    ])
    
    robustness_score = float(np.clip(robustness_score, 0, 100))
    
    return RobustnessScore(
        score=robustness_score,
        drivers=drivers,
        details=details
    )


# ============================================================
# 2️⃣ SCORING MATURITÉ MAINTENANCE
# ============================================================

def score_maintenance_maturity(
    maintenance_strategy: str,  # "corrective" / "preventive" / "predictive"
    gmao_operational: bool,
    pm_compliance: float,  # 0-1
    team_structure: int,  # 1=informal, 2=basic, 3=structured, 4=certified
    manufacturer_contract: bool,
    preventive_frequency_days: int,
    maintenance_backlog_ratio: float,  # 0-1
    technician_training_level: int,  # 1-5
    spare_parts_availability: int,  # 1=poor, 2=basic, 3=good, 4=excellent
    mean_response_days: float,  # délai moyen de prise en charge (jours)
    maintenance_system: str,  # "papier_excel" / "gmao_standalone" / "erp_pm" / "eam" / "iiot_predictive"
    handling_equipment_level: int,  # 1-4 (outillage de manutention maintenance)
    spare_parts_storage_maturity: int,  # 1-4 (organisation stockage)
    kitting_on_demand: bool,  # préparation pièces selon demande / bon de travail
) -> MaintenanceScore:
    """
    Scoring de la maturité de maintenance.
    
    Facteurs:
    - Stratégie maintenance (prédictive > préventive > corrective)
    - GMAO opérationnelle
    - Conformité planning préventif
    - Structure équipe
    - Contrats constructeur
    - Fréquence maintenance préventive
    - Arriéré de maintenance
    - Formation techniciens
    - Disponibilité pièces détachées
    """
    
    drivers = []
    details = {}
    
    # --- Maintenance strategy ---
    strategy_scores = {
        "corrective": 30,
        "preventive": 70,
        "predictive": 95
    }
    strategy_score = strategy_scores.get(maintenance_strategy, 30)
    
    if maintenance_strategy == "corrective":
        drivers.append("❌ Maintenance corrective → forte probabilité sinistre")
    elif maintenance_strategy == "preventive":
        drivers.append("✓ Maintenance préventive → réduction modérée du risque")
    else:
        drivers.append("✓✓ Maintenance prédictive → risque minimal")
    
    details['strategy_score'] = strategy_score
    
    # --- GMAO ---
    gmao_score = 85 if gmao_operational else 40
    
    if gmao_operational:
        drivers.append("✓ GMAO opérationnelle → traçabilité complète")
    else:
        drivers.append("❌ Pas de GMAO → incertitude assurantielle")
    
    details['gmao_score'] = gmao_score
    
    # --- PM compliance ---
    if pm_compliance >= 0.9:
        pm_score = 95
        drivers.append("✓✓ Excellente conformité préventif (> 90%)")
    elif pm_compliance >= 0.75:
        pm_score = 80
        drivers.append("✓ Bonne conformité préventif (75-90%)")
    elif pm_compliance >= 0.5:
        pm_score = 60
        drivers.append("⚠ Conformité moyen (50-75%)")
    else:
        pm_score = 30
        drivers.append("❌ Faible conformité préventif (< 50%)")
    
    details['pm_compliance_score'] = pm_score
    
    # --- Team structure ---
    team_scores = {1: 30, 2: 55, 3: 80, 4: 95}
    team_score = team_scores.get(team_structure, 30)
    
    if team_structure == 1:
        drivers.append("❌ Équipe informelle → risque d'erreur humaine élevé")
    elif team_structure == 2:
        drivers.append("⚠ Équipe basique → capacités limitées")
    elif team_structure == 3:
        drivers.append("✓ Équipe structurée → compétences validées")
    else:
        drivers.append("✓✓ Équipe certifiée → excellente fiabilité")
    
    details['team_score'] = team_score
    
    # --- Manufacturer contract ---
    contract_score = 80 if manufacturer_contract else 50
    
    if manufacturer_contract:
        drivers.append("✓ Contrat constructeur → support technique garanti")
    else:
        drivers.append("⚠ Pas de contrat → support incertain")
    
    details['contract_score'] = contract_score
    
    # --- Preventive frequency ---
    if preventive_frequency_days <= 30:
        freq_score = 95
        drivers.append("✓✓ Maintenance très fréquente (≤ 30j)")
    elif preventive_frequency_days <= 90:
        freq_score = 80
        drivers.append("✓ Maintenance régulière (< 90j)")
    elif preventive_frequency_days <= 180:
        freq_score = 60
        drivers.append("⚠ Maintenance peu fréquente (< 180j)")
    else:
        freq_score = 30
        drivers.append("❌ Maintenance rare (> 180j)")
    
    details['frequency_score'] = freq_score
    
    # --- Maintenance backlog ---
    backlog_score = 100 * (1 - maintenance_backlog_ratio)
    
    if maintenance_backlog_ratio == 0:
        drivers.append("✓ Aucun arriéré → réactivité totale")
    elif maintenance_backlog_ratio < 0.1:
        drivers.append("✓ Arriéré minimal (< 10%)")
    elif maintenance_backlog_ratio < 0.3:
        drivers.append("⚠ Arriéré modéré (10-30%)")
    else:
        drivers.append("❌ Arriéré important (> 30%) → risque de panne")
    
    details['backlog_score'] = backlog_score
    
    # --- Technician training ---
    training_score = technician_training_level * 20  # 1-5 → 20-100
    
    if technician_training_level < 2:
        drivers.append("❌ Formation insuffisante → erreurs probables")
    elif technician_training_level < 4:
        drivers.append("⚠ Formation basique")
    else:
        drivers.append("✓ Formation avancée → haute fiabilité")
    
    details['training_score'] = training_score
    
    # --- Spare parts ---
    parts_scores = {1: 30, 2: 55, 3: 80, 4: 95}
    parts_score = parts_scores.get(spare_parts_availability, 30)
    
    if spare_parts_availability == 1:
        drivers.append("❌ Pièces indisponibles → arrêt prolongé")
    elif spare_parts_availability == 2:
        drivers.append("⚠ Pièces basiques disponibles")
    elif spare_parts_availability == 3:
        drivers.append("✓ Bonne disponibilité pièces")
    else:
        drivers.append("✓✓ Pièces critiques en stock")
    
    details['parts_score'] = parts_score
    
    
    # --- Intervention efficiency (mean response / prise en charge) ---
    if mean_response_days <= 1:
        intervention_score = 95
        drivers.append("✓✓ Intervention très rapide (≤ 1 jour) → MTTR réduit")
    elif mean_response_days <= 3:
        intervention_score = 85
        drivers.append("✓ Intervention rapide (≤ 3 jours)")
    elif mean_response_days <= 7:
        intervention_score = 70
        drivers.append("⚠ Intervention moyenne (≤ 7 jours)")
    elif mean_response_days <= 14:
        intervention_score = 55
        drivers.append("⚠ Intervention lente (≤ 14 jours) → risque PE accru")
    else:
        intervention_score = 35
        drivers.append("❌ Intervention très lente (> 14 jours) → risque perte d'exploitation élevé")
    details['intervention_score'] = intervention_score

    # --- Maintenance system maturity (ordre d'évolution) ---
    system_scores = {
        "papier_excel": 35,        # registre papier / Excel
        "gmao_standalone": 65,     # GMAO indépendante
        "erp_pm": 80,              # module maintenance dans ERP (ex: SAP PM)
        "eam": 88,                 # EAM / CMMS enterprise (ex: IBM Maximo)
        "iiot_predictive": 95      # plateforme IIoT + analytics prédictif
    }
    system_score = system_scores.get(maintenance_system, 35)

    system_labels = {
        "papier_excel": "Papier/Excel",
        "gmao_standalone": "GMAO standalone",
        "erp_pm": "ERP (module maintenance/PM)",
        "eam": "EAM (ex: Maximo)",
        "iiot_predictive": "IIoT + Prédictif"
    }

    if maintenance_system == "papier_excel":
        drivers.append("❌ Système maintenance Papier/Excel → traçabilité faible")
    elif maintenance_system == "gmao_standalone":
        drivers.append("✓ GMAO standalone → planification et historiques")
    elif maintenance_system == "erp_pm":
        drivers.append("✓✓ ERP maintenance (PM) → intégration achats/stock/production")
    elif maintenance_system == "eam":
        drivers.append("✓✓ EAM (type Maximo) → gouvernance maintenance avancée")
    else:
        drivers.append("✓✓ IIoT + prédictif → optimisation continue et détection précoce")
    details['maintenance_system_score'] = system_score
    details['maintenance_system_label'] = system_labels.get(maintenance_system, maintenance_system)

    # --- Handling equipment for maintenance / manutention ---
    handling_scores = {1: 35, 2: 60, 3: 80, 4: 95}
    handling_score = handling_scores.get(handling_equipment_level, 35)

    if handling_equipment_level == 1:
        drivers.append("⚠ Outillage manutention maintenance faible → interventions risquées/lentes")
    elif handling_equipment_level == 2:
        drivers.append("✓ Manutention basique (palans/chariots) → capacité limitée")
    elif handling_equipment_level == 3:
        drivers.append("✓✓ Manutention adaptée (levage sécurisé, accès) → MTTR réduit")
    else:
        drivers.append("✓✓ Manutention avancée (nacelles, levage certifié) → sécurité & rapidité")
    details['handling_score'] = handling_score

    # --- Spare parts storage maturity (organisation + traçabilité) ---
    storage_scores = {1: 35, 2: 60, 3: 80, 4: 95}
    storage_score = storage_scores.get(spare_parts_storage_maturity, 35)

    if spare_parts_storage_maturity == 1:
        drivers.append("❌ Stock pièces non structuré → ruptures & erreurs")
    elif spare_parts_storage_maturity == 2:
        drivers.append("⚠ Stock structuré basique (emplacements) → visibilité partielle")
    elif spare_parts_storage_maturity == 3:
        drivers.append("✓ Stock géré (min/max, criticité) → disponibilité améliorée")
    else:
        drivers.append("✓✓ Stock optimisé (ABC/criticité, traçabilité) → arrêt réduit")
    details['storage_score'] = storage_score

    # --- Kitting / préparation pièces selon demande ---
    kitting_score = 90 if kitting_on_demand else 55
    if kitting_on_demand:
        drivers.append("✓ Préparation pièces à la demande (kitting) → intervention plus efficace")
    else:
        drivers.append("⚠ Pas de kitting → pertes de temps lors des interventions")
    details['kitting_score'] = kitting_score

    # --- Global maintenance (pondéré) ---
    weights = {
        "strategy": 0.18,
        "gmao": 0.10,
        "pm": 0.14,
        "team": 0.10,
        "contract": 0.06,
        "frequency": 0.07,
        "backlog": 0.07,
        "training": 0.06,
        "parts_availability": 0.07,
        "system": 0.07,
        "handling": 0.04,
        "storage": 0.04,
        "kitting": 0.03,
        "intervention": 0.07,
    }
    numerator = (
        strategy_score * weights["strategy"] +
        gmao_score * weights["gmao"] +
        pm_score * weights["pm"] +
        team_score * weights["team"] +
        contract_score * weights["contract"] +
        freq_score * weights["frequency"] +
        backlog_score * weights["backlog"] +
        training_score * weights["training"] +
        parts_score * weights["parts_availability"] +
        system_score * weights["system"] +
        handling_score * weights["handling"] +
        storage_score * weights["storage"] +
        kitting_score * weights["kitting"] +
        intervention_score * weights["intervention"]
    )
    maintenance_score = float(np.clip(numerator / sum(weights.values()), 0, 100))

    return MaintenanceScore(
        score=maintenance_score,
        drivers=drivers,
        details=details
    )


# ============================================================
# 3️⃣ SCORING GOUVERNANCE TECHNIQUE
# ============================================================

def score_governance(
    procedures_formalized: bool,
    pca_exists: bool,
    pca_tested: bool,
    audit_frequency_months: int,
    iso_certifications: List[str],  # ["ISO27001", "ISO45001", ...]
    operator_training_level: int,  # 1-5
    documentation_quality: int,  # 1=poor, 2=basic, 3=good, 4=excellent
    incident_tracking_system: bool,
    anomaly_detection_formalized: bool,
    continuity_test_frequency_months: int,
) -> GovernanceScore:
    """
    Scoring de la gouvernance technique.
    
    Facteurs:
    - Procédures maintenance formalisées
    - Plan de continuité (PCA)
    - Test du PCA
    - Audits techniques périodiques
    - Certifications ISO pertinentes
    - Formation opérateurs
    - Qualité documentation
    - Système de tracking incidents
    - Détection anomalies formalisée
    - Fréquence test continuité
    """
    
    drivers = []
    details = {}
    
    # --- Procedures ---
    proc_score = 90 if procedures_formalized else 40
    
    if procedures_formalized:
        drivers.append("✓ Procédures formalisées → gouvernance établie")
    else:
        drivers.append("❌ Procédures informelles → risques d'erreur")
    
    details['procedures_score'] = proc_score
    
    # --- PCA ---
    pca_score = 50
    if pca_exists:
        pca_score = 75
        drivers.append("✓ PCA en place → continuité planifiée")
        if pca_tested:
            pca_score = 95
            drivers.append("✓✓ PCA testé régulièrement → fiabilité démontrée")
    else:
        drivers.append("❌ Pas de PCA → risque perte d'exploitation total")
    
    details['pca_score'] = pca_score
    
    # --- Audits ---
    if audit_frequency_months <= 12:
        audit_score = 95
        drivers.append("✓✓ Audits annuels (ou plus) → amélioration continue")
    elif audit_frequency_months <= 24:
        audit_score = 75
        drivers.append("✓ Audits bi-annuels")
    elif audit_frequency_months <= 36:
        audit_score = 55
        drivers.append("⚠ Audits peu fréquents (> 2 ans)")
    else:
        audit_score = 30
        drivers.append("❌ Aucun audit régulier")
    
    details['audit_score'] = audit_score
    
    # --- ISO certifications ---
    relevant_isos = ["ISO27001", "ISO45001", "ISO9001", "ISO50001"]
    iso_count = len([iso for iso in iso_certifications if iso in relevant_isos])
    iso_score = min(95, 50 + (iso_count * 15))
    
    if iso_count == 0:
        drivers.append("⚠ Aucune certification ISO → gouvernance basique")
    elif iso_count < 2:
        drivers.append("✓ Certification ISO présente → approche structurée")
    else:
        drivers.append("✓✓ Plusieurs certifications → excellence reconnue")
    
    details['iso_score'] = iso_score
    details['iso_count'] = iso_count
    
    # --- Operator training ---
    operator_score = operator_training_level * 20  # 1-5 → 20-100
    
    if operator_training_level < 2:
        drivers.append("❌ Formation opérateurs insuffisante")
    elif operator_training_level < 4:
        drivers.append("⚠ Formation opérateurs basique")
    else:
        drivers.append("✓ Formation opérateurs avancée")
    
    details['operator_score'] = operator_score
    
    # --- Documentation ---
    doc_scores = {1: 30, 2: 55, 3: 80, 4: 95}
    doc_score = doc_scores.get(documentation_quality, 30)
    
    if documentation_quality == 1:
        drivers.append("❌ Documentation absente → traçabilité nulle")
    elif documentation_quality == 2:
        drivers.append("⚠ Documentation basique")
    elif documentation_quality == 3:
        drivers.append("✓ Documentation correcte")
    else:
        drivers.append("✓✓ Documentation excellente → traçabilité complète")
    
    details['doc_score'] = doc_score
    
    # --- Incident tracking ---
    incident_score = 85 if incident_tracking_system else 40
    
    if incident_tracking_system:
        drivers.append("✓ Système tracking incidents → apprentissage continu")
    else:
        drivers.append("❌ Pas de tracking → pas de retour d'expérience")
    
    details['incident_score'] = incident_score
    
    # --- Anomaly detection ---
    anomaly_score = 85 if anomaly_detection_formalized else 40
    
    if anomaly_detection_formalized:
        drivers.append("✓ Détection anomalies formalisée → prévention active")
    else:
        drivers.append("❌ Pas de processus détection → réactivité seulement")
    
    details['anomaly_score'] = anomaly_score
    
    # --- Continuity test frequency ---
    if continuity_test_frequency_months <= 12:
        continuity_score = 95
        drivers.append("✓✓ Tests continuité annuels (ou plus)")
    elif continuity_test_frequency_months <= 24:
        continuity_score = 75
        drivers.append("✓ Tests continuité réguliers")
    else:
        continuity_score = 40
        drivers.append("⚠ Tests continuité rares ou absents")
    
    details['continuity_score'] = continuity_score
    
    # --- Global governance ---
    governance_score = np.mean([
        proc_score * 0.15,
        pca_score * 0.25,
        audit_score * 0.15,
        iso_score * 0.1,
        operator_score * 0.1,
        doc_score * 0.1,
        incident_score * 0.1,
        anomaly_score * 0.1,
        continuity_score * 0.1
    ])
    
    governance_score = float(np.clip(governance_score, 0, 100))
    
    return GovernanceScore(
        score=governance_score,
        drivers=drivers,
        details=details
    )


# ============================================================
# AGRÉGATION SCORE GLOBAL
# ============================================================

def compute_advanced_scoring(
    robustness: RobustnessScore,
    maintenance: MaintenanceScore,
    governance: GovernanceScore,
) -> AdvancedScoringResult:
    """
    Agrège les 3 piliers en score global et recommandations.
    """
    
    # Score global (pondéré)
    global_score = float(np.clip(
        robustness.score * 0.35 +
        maintenance.score * 0.45 +
        governance.score * 0.20,
        0, 100
    ))
    
    # Risk level
    if global_score >= 75:
        risk_level = "FAIBLE"
    elif global_score >= 50:
        risk_level = "MOYEN"
    else:
        risk_level = "ÉLEVÉ"
    
    # Dominant risks (identifiés par score < 60)
    dominant_risks = []
    if robustness.score < 60:
        dominant_risks.append("🔴 Robustesse mécatronique insuffisante")
    if maintenance.score < 60:
        dominant_risks.append("🔴 Maturité maintenance très faible")
    if governance.score < 60:
        dominant_risks.append("🔴 Gouvernance technique inexistante")
    
    # Recommendations
    recommendations = []
    if robustness.score < 70:
        recommendations.append("Instrumenter l'équipement (capteurs IoT)")
        recommendations.append("Évaluer redondance des fonctions critiques")
    if maintenance.score < 70:
        recommendations.append("Passer à une stratégie préventive/prédictive")
        recommendations.append("Déployer une GMAO opérationnelle / module ERP maintenance")
    # Recos ciblées (prévention)
    ms = maintenance.details.get("maintenance_system_score", 100)
    storage = maintenance.details.get("storage_score", 100)
    handling = maintenance.details.get("handling_score", 100)
    intervention = maintenance.details.get("intervention_score", 100)

    if ms < 70:
        recommendations.append("Monter en maturité système maintenance (GMAO → ERP PM → EAM/IIoT)")
    if storage < 70:
        recommendations.append("Structurer le magasin pièces (criticité, min/max, traçabilité)")
    if handling < 70:
        recommendations.append("Renforcer les moyens de manutention/levage pour maintenance (sécurité + MTTR)")
    if intervention < 70:
        recommendations.append("Améliorer la réactivité intervention (SLA, astreintes, priorisation)")

    if governance.score < 70:
        recommendations.append("Formaliser procédures maintenance")
        recommendations.append("Mettre en place un PCA testé")
    
    # Prevention priorities
    prevention_priorities = []
    
    if robustness.score < 60:
        prevention_priorities.append("Priorité 1 : Réduire défauts structurels (modernisation équipement)")
    if maintenance.score < 60:
        prevention_priorities.append("Priorité 2 : Passer en maintenance prédictive")
    else:
        prevention_priorities.append("Priorité 2 : Renforcer discipline préventif (adhérence planning)")
    
    if governance.score < 60:
        prevention_priorities.append("Priorité 3 : Établir gouvernance (procédures, PCA, formation)")
    
    return AdvancedScoringResult(
        global_score=global_score,
        risk_level=risk_level,
        robustness=robustness,
        maintenance=maintenance,
        governance=governance,
        dominant_risks=dominant_risks if dominant_risks else ["✓ Aucun risque dominant détecté"],
        recommendations=recommendations if recommendations else ["✓ Configuration conforme à bonnes pratiques"],
        prevention_priorities=prevention_priorities,
    )
