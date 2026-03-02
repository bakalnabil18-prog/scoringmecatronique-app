# ============================================================
# CRITÈRES DE PRÉVENTION AVANCÉS
# Maintenance Industrielle 4.0 - Maroc
# ============================================================

PREVENTION_CRITERIA = {
    
    # 1. PRÉVENTION PRÉDICTIVE (IoT & Analytics)
    "predictive_maintenance": {
        "nom": "Maintenance Prédictive",
        "importance": "Critique",
        "impact_score": 15,  # Points de scoring
        "critères": {
            "iot_sensors_deployed": {
                "label": "Capteurs IoT déployés",
                "scores": {
                    "none": 0,          # Aucun
                    "partial": 5,       # Partiel (< 50%)
                    "majority": 10,     # Majorité (50-80%)
                    "full": 15          # Complet (> 80%)
                }
            },
            "predictive_analytics": {
                "label": "Analyse prédictive active",
                "scores": {
                    "manual": 0,        # Aucune
                    "basic": 5,         # De base
                    "advanced": 10,     # Avancée
                    "ai_powered": 15    # IA/ML
                }
            },
            "remaining_useful_life": {
                "label": "RUL (Durée de vie utile) calculée",
                "scores": {
                    "not_available": 0,
                    "estimated": 5,
                    "calculated_monthly": 10,
                    "real_time": 15
                }
            }
        }
    },
    
    # 2. GESTION DES CONDITIONS (Condition-Based Maintenance)
    "condition_monitoring": {
        "nom": "Monitoring de Conditions",
        "importance": "Très Importante",
        "impact_score": 12,
        "critères": {
            "vibration_monitoring": {
                "label": "Monitoring vibrations",
                "scores": {
                    "none": 0,
                    "manual_periodic": 3,
                    "automated_alert": 8,
                    "real_time_dashboard": 12
                }
            },
            "thermal_monitoring": {
                "label": "Monitoring thermique",
                "scores": {
                    "none": 0,
                    "manual_checks": 3,
                    "automated_alerts": 8,
                    "predictive_trending": 12
                }
            },
            "oil_analysis_program": {
                "label": "Programme d'analyse d'huile",
                "scores": {
                    "none": 0,
                    "annual": 4,
                    "quarterly": 8,
                    "monthly_plus": 12
                }
            },
            "ultrasound_testing": {
                "label": "Test ultrason",
                "scores": {
                    "none": 0,
                    "annual": 3,
                    "quarterly": 8,
                    "monthly": 12
                }
            }
        }
    },
    
    # 3. MAINTENANCE BASÉE SUR LA FIABILITÉ (RCM)
    "reliability_centered_maintenance": {
        "nom": "Maintenance Centrée sur Fiabilité (RCM)",
        "importance": "Très Importante",
        "impact_score": 14,
        "critères": {
            "rcm_analysis_performed": {
                "label": "Analyse RCM complétée",
                "scores": {
                    "not_done": 0,
                    "in_progress": 5,
                    "completed_2years": 10,
                    "completed_current": 14
                }
            },
            "fmeca_documentation": {
                "label": "Documentation FMECA",
                "scores": {
                    "none": 0,
                    "partial": 5,
                    "complete": 10,
                    "regularly_updated": 14
                }
            },
            "criticality_assessment": {
                "label": "Évaluation criticité",
                "scores": {
                    "not_documented": 0,
                    "basic": 5,
                    "detailed": 10,
                    "updated_regularly": 14
                }
            }
        }
    },
    
    # 4. LEAN MAINTENANCE
    "lean_maintenance": {
        "nom": "Maintenance Lean (5S/TPM)",
        "importance": "Importante",
        "impact_score": 10,
        "critères": {
            "5s_implementation": {
                "label": "Implémentation 5S",
                "scores": {
                    "not_implemented": 0,
                    "partial_1_3": 3,
                    "3_4_elements": 6,
                    "all_5_maintained": 10
                }
            },
            "tpm_implementation": {
                "label": "Maintenance Productive Totale",
                "scores": {
                    "none": 0,
                    "autonomous_maint": 4,
                    "planned_maint": 7,
                    "full_tpm": 10
                }
            },
            "visual_management": {
                "label": "Gestion visuelle",
                "scores": {
                    "none": 0,
                    "partial": 4,
                    "comprehensive": 8,
                    "automated": 10
                }
            }
        }
    },
    
    # 5. MANAGEMENT DE PIÈCES DÉTACHÉES
    "spare_parts_management": {
        "nom": "Gestion Pièces Détachées Optimisée",
        "importance": "Critique",
        "impact_score": 13,
        "critères": {
            "spare_parts_inventory": {
                "label": "Stock pièces critiques",
                "scores": {
                    "none": 0,
                    "basic": 4,
                    "optimized": 9,
                    "predictive_stocking": 13
                }
            },
            "supplier_agreements": {
                "label": "Accords fournisseurs",
                "scores": {
                    "none": 0,
                    "transactional": 4,
                    "partnership": 9,
                    "strategic_alliance": 13
                }
            },
            "critical_parts_redundancy": {
                "label": "Redondance pièces critiques",
                "scores": {
                    "none": 0,
                    "partial": 5,
                    "major_components": 9,
                    "complete": 13
                }
            }
        }
    },
    
    # 6. FORMATION & COMPÉTENCES
    "skills_development": {
        "nom": "Développement Compétences Maintenance",
        "importance": "Très Importante",
        "impact_score": 11,
        "critères": {
            "technician_certification": {
                "label": "Certification techniciens",
                "scores": {
                    "none": 0,
                    "25_percent": 3,
                    "50_percent": 6,
                    "75_percent_plus": 11
                }
            },
            "training_hours_per_year": {
                "label": "Heures formation/an par personne",
                "scores": {
                    "zero": 0,
                    "less_than_40": 3,
                    "40_80": 7,
                    "more_than_80": 11
                }
            },
            "technical_knowledge_transfer": {
                "label": "Transfert connaissances (mentoring)",
                "scores": {
                    "none": 0,
                    "informal": 4,
                    "structured_program": 8,
                    "documented_system": 11
                }
            }
        }
    },
    
    # 7. PLANIFICATION & SCHEDULING
    "planning_execution": {
        "nom": "Planification & Exécution",
        "importance": "Très Importante",
        "impact_score": 11,
        "critères": {
            "work_order_system": {
                "label": "Système ordres de travail",
                "scores": {
                    "none": 0,
                    "manual": 4,
                    "basic_digital": 7,
                    "advanced_with_analytics": 11
                }
            },
            "schedule_compliance": {
                "label": "Conformité planning (%)",
                "scores": {
                    "less_than_50": 0,
                    "50_70": 3,
                    "70_85": 7,
                    "more_than_85": 11
                }
            },
            "preventive_schedule_adherence": {
                "label": "Respect maintenance préventive",
                "scores": {
                    "0_25_percent": 0,
                    "25_50_percent": 3,
                    "50_75_percent": 7,
                    "75_percent_plus": 11
                }
            }
        }
    },
    
    # 8. QUALITÉ & DOCUMENTATION
    "quality_documentation": {
        "nom": "Qualité & Documentation",
        "importance": "Importante",
        "impact_score": 9,
        "critères": {
            "equipment_history_records": {
                "label": "Historique équipement",
                "scores": {
                    "none": 0,
                    "basic": 3,
                    "comprehensive": 6,
                    "detailed_with_trends": 9
                }
            },
            "maintenance_manuals": {
                "label": "Manuels maintenance",
                "scores": {
                    "none": 0,
                    "original_only": 2,
                    "original_plus_custom": 6,
                    "translated_digital": 9
                }
            },
            "quality_audits": {
                "label": "Audits qualité maintenance",
                "scores": {
                    "none": 0,
                    "annual": 3,
                    "semi_annual": 6,
                    "quarterly_plus": 9
                }
            }
        }
    },
    
    # 9. SÉCURITÉ & CONFORMITÉ
    "safety_compliance": {
        "nom": "Sécurité & Conformité",
        "importance": "Critique",
        "impact_score": 12,
        "critères": {
            "lockout_tagout_program": {
                "label": "Programme LOTO complet",
                "scores": {
                    "none": 0,
                    "informal": 3,
                    "documented": 8,
                    "certified": 12
                }
            },
            "safety_training": {
                "label": "Formation sécurité",
                "scores": {
                    "none": 0,
                    "annual": 4,
                    "semi_annual": 8,
                    "quarterly_plus": 12
                }
            },
            "maintenance_incidents_tracking": {
                "label": "Tracking incidents maintenance",
                "scores": {
                    "none": 0,
                    "basic": 4,
                    "detailed_analysis": 8,
                    "preventive_actions": 12
                }
            }
        }
    },
    
    # 10. CONTINUITÉ D'EXPLOITATION
    "business_continuity": {
        "nom": "Continuité d'Exploitation",
        "importance": "Critique",
        "impact_score": 13,
        "critères": {
            "backup_equipment": {
                "label": "Équipements de secours",
                "scores": {
                    "none": 0,
                    "partial": 5,
                    "major_components": 9,
                    "full_redundancy": 13
                }
            },
            "emergency_response_plan": {
                "label": "Plan réponse urgence",
                "scores": {
                    "none": 0,
                    "basic": 4,
                    "detailed": 9,
                    "tested_regularly": 13
                }
            },
            "supplier_emergency_contacts": {
                "label": "Contacts fournisseurs urgence",
                "scores": {
                    "none": 0,
                    "limited": 5,
                    "comprehensive": 9,
                    "24_7_available": 13
                }
            }
        }
    }
}


def calculate_prevention_score(prevention_data):
    """
    Calcule le score de prévention total basé sur les critères.
    
    Args:
        prevention_data (dict): Dictionnaire avec clés = critères et valeurs = scores
    
    Returns:
        tuple: (score_total, breakdown_par_categorie)
    """
    total_score = 0
    max_score = 0
    breakdown = {}
    
    for category, info in PREVENTION_CRITERIA.items():
        category_score = 0
        category_max = info['impact_score']
        
        if category in prevention_data:
            for criterion, criterion_info in info['critères'].items():
                if criterion in prevention_data[category]:
                    score_level = prevention_data[category][criterion]
                    criterion_score = criterion_info['scores'].get(score_level, 0)
                    category_score += criterion_score / len(info['critères']) * info['impact_score'] / 15
        
        total_score += category_score
        max_score += info['impact_score']
        breakdown[info['nom']] = {
            'score': category_score,
            'max': category_max,
            'pct': (category_score / category_max * 100) if category_max > 0 else 0
        }
    
    global_pct = (total_score / max_score * 100) if max_score > 0 else 0
    
    return {
        'total_score': total_score,
        'max_score': max_score,
        'percentage': global_pct,
        'breakdown': breakdown,
        'rating': 'EXCELLENT' if global_pct >= 80 else 'TRÈS BON' if global_pct >= 60 else 'BON' if global_pct >= 40 else 'À AMÉLIORER'
    }


# Exemple d'utilisation
PREVENTION_SCORING_EXAMPLE = {
    "predictive_maintenance": {
        "iot_sensors_deployed": "full",
        "predictive_analytics": "ai_powered",
        "remaining_useful_life": "real_time"
    },
    "condition_monitoring": {
        "vibration_monitoring": "real_time_dashboard",
        "thermal_monitoring": "predictive_trending",
        "oil_analysis_program": "monthly_plus",
        "ultrasound_testing": "monthly"
    },
    "reliability_centered_maintenance": {
        "rcm_analysis_performed": "completed_current",
        "fmeca_documentation": "regularly_updated",
        "criticality_assessment": "updated_regularly"
    },
    "lean_maintenance": {
        "5s_implementation": "all_5_maintained",
        "tpm_implementation": "full_tpm",
        "visual_management": "automated"
    },
    "spare_parts_management": {
        "spare_parts_inventory": "predictive_stocking",
        "supplier_agreements": "strategic_alliance",
        "critical_parts_redundancy": "complete"
    },
    "skills_development": {
        "technician_certification": "75_percent_plus",
        "training_hours_per_year": "more_than_80",
        "technical_knowledge_transfer": "documented_system"
    },
    "planning_execution": {
        "work_order_system": "advanced_with_analytics",
        "schedule_compliance": "more_than_85",
        "preventive_schedule_adherence": "75_percent_plus"
    },
    "quality_documentation": {
        "equipment_history_records": "detailed_with_trends",
        "maintenance_manuals": "translated_digital",
        "quality_audits": "quarterly_plus"
    },
    "safety_compliance": {
        "lockout_tagout_program": "certified",
        "safety_training": "quarterly_plus",
        "maintenance_incidents_tracking": "preventive_actions"
    },
    "business_continuity": {
        "backup_equipment": "full_redundancy",
        "emergency_response_plan": "tested_regularly",
        "supplier_emergency_contacts": "24_7_available"
    }
}
