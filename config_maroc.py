"""
Configuration Marocaine - Assurance Industrie 4.0
Localisation pour le marché marocain
"""

# ============================================================
# 📍 LOCALISATION MAROCAINE
# ============================================================

MAROC_CONFIG = {
    "devise": "DH",
    "pays": "Maroc",
    "langue": "Français marocain",
    "tva_standard": 0.20,  # 20% TVA au Maroc
    "tva_reduite": 0.10,   # 10% TVA réduite
}

# ============================================================
# 💰 DEVISES & CONVERSIONS
# ============================================================

DEVISES = {
    "DH": "Dirham marocain",
    "EUR": "Euro (référence)",
    "USD": "Dollar américain",
}

TAUX_CHANGE = {
    "DH_EUR": 0.095,  # 1 DH = ~0.095 EUR
    "DH_USD": 0.10,   # 1 DH = ~0.10 USD
    "EUR_DH": 10.5,   # 1 EUR = ~10.5 DH
    "USD_DH": 10.0,   # 1 USD = ~10 DH
}

# ============================================================
# 🏢 SECTEURS INDUSTRIELS MAROCAINS
# ============================================================

SECTEURS_MAROC = {
    "textile_confection": {
        "nom": "Textile & Confection",
        "code": "TC",
        "importance": "Très élevée (30% exports marocains)",
        "regions": ["Fès", "Casablanca", "Tanger"],
        "risques_specifiques": [
            "Risque social (nombreux employés)",
            "Arrêts fréquents (équipements importés)",
            "Qualité alimentation électrique variable",
        ],
        "taux_base_pct": 0.8,  # 0.8% de la valeur
    },
    
    "agroalimentaire": {
        "nom": "Agroalimentaire & Conserves",
        "code": "AA",
        "importance": "Élevée (secteur stratégique)",
        "regions": ["Agadir", "Marrakech", "Fès"],
        "risques_specifiques": [
            "Risque climatique (sécheresse)",
            "Équipements frigorifiques critiques",
            "Contamination produits",
        ],
        "taux_base_pct": 1.2,
    },
    
    "mines_phosphates": {
        "nom": "Mines & Phosphates",
        "code": "MP",
        "importance": "Très élevée (patrimoine national)",
        "regions": ["Khouribga", "Youssoufia", "Béni-Mellal"],
        "risques_specifiques": [
            "Équipements lourds (très coûteux)",
            "Environnement hostile (poussière)",
            "Arrêts = pertes très élevées",
        ],
        "taux_base_pct": 1.5,
    },
    
    "chimie_pharmacie": {
        "nom": "Chimie & Pharmacie",
        "code": "CP",
        "importance": "Élevée (croissante)",
        "regions": ["Casablanca", "Rabat", "Skhirat"],
        "risques_specifiques": [
            "Risque de contamination",
            "Conformité normative stricte",
            "Équipements sensibles",
        ],
        "taux_base_pct": 1.0,
    },
    
    "construction_materiaux": {
        "nom": "Construction & Matériaux",
        "code": "CM",
        "importance": "Moyenne (liée au BTP)",
        "regions": ["Casablanca", "Marrakech", "Fès"],
        "risques_specifiques": [
            "Équipements mobiles (carrières)",
            "Poussière/humidité",
            "Arrêts saisonniers",
        ],
        "taux_base_pct": 0.9,
    },
    
    "energie_eau": {
        "nom": "Énergie & Eau",
        "code": "EW",
        "importance": "Très élevée (infrastructure)",
        "regions": ["National"],
        "risques_specifiques": [
            "Régulation très stricte",
            "Enjeux de continuité vitaux",
            "Investissements énormes",
        ],
        "taux_base_pct": 0.6,
    },
    
    "autres": {
        "nom": "Autres secteurs",
        "code": "AUT",
        "importance": "Variable",
        "regions": ["National"],
        "risques_specifiques": [],
        "taux_base_pct": 1.0,
    }
}

# ============================================================
# 📋 TERMINOLOGIE ASSURANCE MAROCAINE
# ============================================================

TERMINOLOGIE_ASSURANCE_MAROC = {
    # Concepts généraux
    "risque": "Risque",
    "sinistre": "Sinistre",
    "franchise": "Franchise / Côte de risque",
    "prime": "Prime d'assurance",
    "taux": "Taux de prime",
    "couverture": "Garantie / Couverture",
    "exclusion": "Exclusion",
    "deductible": "Franchise (montant)",
    "limit": "Limite / Somme assurée",
    
    # Dommages matériels
    "bdm": "Bris de Machine (BDM)",
    "dommages_materiels": "Dommages Matériels Directs",
    "perte_exploitation": "Perte d'Exploitation (PE)",
    "pertes_indirectes": "Pertes Indirectes",
    "frais_supplementaires": "Frais Supplémentaires d'Exploitation",
    
    # Types de couvertures
    "couv_principale": "Couverture Principale",
    "couv_additionnelle": "Couverture Additionnelle / Extension",
    "avenant": "Avenant",
    "clause": "Clause / Condition",
    
    # Inspection & Audit
    "inspection": "Inspection technique",
    "audit": "Audit de risque",
    "visite_proposant": "Visite du proposant",
    "expertise": "Expertise technique",
    
    # Sinistralité
    "sinistralite": "Sinistralité / Fréquence sinistres",
    "cout_moyen": "Coût moyen des sinistres",
    "frequence": "Fréquence",
    "severite": "Sévérité",
    
    # Régulation marocaine
    "acpr": "Autorité de Contrôle Prudentiel et de Résolution",
    "bkam": "Bank Al-Maghrib",
    "fga": "Fonds de Garantie d'Assurance",
    "pca": "Plan de Continuité d'Activité",
}

# ============================================================
# ⚖️ RÉGLEMENTATIONS & NORMES MAROCAINES
# ============================================================

REGLEMENTATIONS_MAROC = {
    "code_assurance": {
        "nom": "Code des Assurances (Maroc)",
        "annee": 2002,
        "dernière_maj": 2023,
        "lien": "Loi n°17-99",
        "points_clés": [
            "Obligation de déclaration sinistres (48h)",
            "Transparence de l'assuré (devoir de déclaration)",
            "Droit de résiliation annuelle",
            "Médiation en cas de litige",
        ]
    },
    
    "normes_iso": {
        "ISO_9001": "Système de Management de la Qualité",
        "ISO_45001": "Santé-Sécurité au Travail (remplace OHSAS 18001)",
        "ISO_50001": "Management de l'Énergie",
        "ISO_27001": "Sécurité de l'information",
        "ISO_13849": "Sécurité des machines",
        "ISO_14001": "Environnement",
    },
    
    "normes_locales": {
        "CNAM": {
            "nom": "Caisse Nationale de l'Assurance Maladie",
            "obligatoire": True,
            "impact": "Obligation couverture sociale salariés",
        },
        "CNSS": {
            "nom": "Caisse Nationale de Sécurité Sociale",
            "obligatoire": True,
            "impact": "Retraite et allocations familiales",
        },
        "OP": {
            "nom": "Office de la Protection Sociale (régime général)",
            "obligatoire": True,
            "impact": "Couverture salariés du secteur privé",
        }
    },
    
    "certifications_sectorielles": {
        "ecocert": "Certification Écologique (agroalimentaire)",
        "haccp": "Système HACCP (agroalimentaire)",
        "pme_excellence": "Label PME Excellence Maroc",
        "qualité_maroc": "Label Qualité Maroc",
    }
}

# ============================================================
# 🎯 RISQUES SPÉCIFIQUES MAROC
# ============================================================

RISQUES_SPECIFIQUES_MAROC = {
    "risque_climatique": {
        "nom": "Risque Climatique",
        "description": "Sécheresses, inondations, tempêtes",
        "probabilite": "Moyenne à élevée",
        "secteurs_touches": ["agroalimentaire", "energie_eau"],
        "impact": "Interruptions fréquentes",
        "couvertures": ["Assurance météo", "Assurance récolte"],
    },
    
    "risque_politique": {
        "nom": "Risque Politique & Social",
        "description": "Grèves, instabilité sociale (rare)",
        "probabilite": "Faible mais possible",
        "secteurs_touches": ["textile_confection", "mines_phosphates"],
        "impact": "Arrêts imprévisibles",
        "couvertures": ["Riot & Civil Commotion"],
    },
    
    "risque_change": {
        "nom": "Risque de Change DH/EUR",
        "description": "Volatilité devise marocaine",
        "probabilite": "Élevée (marché émergent)",
        "secteurs_touches": ["Tous"],
        "impact": "Coûts pièces détachées importées",
        "couvertures": ["Contrats à taux fixe", "Hedging"],
    },
    
    "risque_approvisionnement": {
        "nom": "Risque d'Approvisionnement",
        "description": "Délai pièces importées (1-3 mois)",
        "probabilite": "Élevée",
        "secteurs_touches": ["Tous les secteurs modernes"],
        "impact": "Arrêts prolongés",
        "couvertures": ["Stock de pièces critiques", "Fournisseurs alternatifs"],
    },
    
    "risque_alimentation_electrique": {
        "nom": "Risque Alimentation Électrique",
        "description": "Coupures, baisses tension (région-dépendant)",
        "probabilite": "Variable par région",
        "secteurs_touches": ["Tous"],
        "impact": "Dommages électriques équipements",
        "couvertures": ["Parasurtenseurs", "Génératrices"],
    },
    
    "risque_qualite_eau": {
        "nom": "Risque Qualité Eau",
        "description": "Eau dure, salinité (zones côtières)",
        "probabilite": "Variable par région",
        "secteurs_touches": ["agroalimentaire", "energie_eau"],
        "impact": "Calcaire = usure accélérée",
        "couvertures": ["Adoucisseurs", "Traitements"],
    }
}

# ============================================================
# 💼 CLASSES DE RISQUE MAROCAINES
# ============================================================

CLASSES_RISQUE_MAROC = {
    "classe_1": {
        "nom": "Risque Minimal",
        "score": "75-100",
        "franchise_dh": "5 000 - 10 000",
        "taux_prime": "0.4% - 0.6%",
        "conditions": [
            "Équipement récent (< 5 ans)",
            "Maintenance prédictive établie",
            "Procédures formalisées",
            "Formation personnel ✓",
        ],
        "secteur_exemple": "Agroalimentaire moderne (Agadir)",
    },
    
    "classe_2": {
        "nom": "Risque Acceptable",
        "score": "50-74",
        "franchise_dh": "10 000 - 25 000",
        "taux_prime": "0.7% - 1.2%",
        "conditions": [
            "Équipement moyen âge (5-10 ans)",
            "Maintenance préventive OK",
            "Inspection recommandée",
        ],
        "secteur_exemple": "Textile Casablanca (moyen)",
    },
    
    "classe_3": {
        "nom": "Risque Élevé",
        "score": "25-49",
        "franchise_dh": "25 000 - 50 000",
        "taux_prime": "1.3% - 2.0%",
        "conditions": [
            "Équipement ancien (10-15 ans)",
            "Maintenance corrective",
            "Audit obligatoire",
            "Monitoring IoT recommandé",
        ],
        "secteur_exemple": "Manufacture traditionnelle",
    },
    
    "classe_4": {
        "nom": "Risque Très Élevé",
        "score": "< 25",
        "franchise_dh": "50 000 +",
        "taux_prime": "2.0% - 4.0%",
        "conditions": [
            "Équipement très ancien (> 15 ans)",
            "Pas de maintenance structurée",
            "Plan d'amélioration obligatoire",
            "Audit annuel obligatoire",
        ],
        "secteur_exemple": "Ateliers informels",
    }
}

# ============================================================
# 🏪 FRANCHISES MAROCAINES STANDARDS
# ============================================================

FRANCHISES_MAROC_DH = {
    "micro_entreprise": {
        "chiffre_affaires": "< 500 000 DH",
        "franchise_min": 2500,
        "franchise_rec": 5000,
        "classe_typique": "Classe 2-3",
    },
    
    "pme": {
        "chiffre_affaires": "500 000 - 50 M DH",
        "franchise_min": 5000,
        "franchise_rec": 15000,
        "classe_typique": "Classe 2",
    },
    
    "pmi": {
        "chiffre_affaires": "50 M - 500 M DH",
        "franchise_min": 10000,
        "franchise_rec": 25000,
        "classe_typique": "Classe 1-2",
    },
    
    "grande_entreprise": {
        "chiffre_affaires": "> 500 M DH",
        "franchise_min": 25000,
        "franchise_rec": 50000,
        "classe_typique": "Classe 1",
    }
}

# ============================================================
# 📊 TAUX PRIMES MAROCAINS PAR SECTEUR
# ============================================================

TAUX_PRIMES_SECTEUR = {
    "textile_confection": {
        "taux_base": 0.80,  # % de la valeur assurée
        "majorations": {
            "risque_social_eleve": 0.10,
            "equipement_ancien": 0.15,
            "pas_gmao": 0.20,
        },
        "reductions": {
            "maintenance_predictive": -0.15,
            "iso_9001": -0.10,
            "audit_annuel": -0.05,
        }
    },
    
    "agroalimentaire": {
        "taux_base": 1.20,
        "majorations": {
            "risque_climatique": 0.20,
            "zones_secheresses": 0.25,
            "pas_haccp": 0.15,
        },
        "reductions": {
            "assurance_recolte": -0.20,
            "systeme_irrigation_modern": -0.10,
            "certification_iso": -0.10,
        }
    },
    
    "mines_phosphates": {
        "taux_base": 1.50,
        "majorations": {
            "environnement_hostile": 0.25,
            "equipements_tres_lourds": 0.30,
            "pas_securite": 0.35,
        },
        "reductions": {
            "maintenance_predictive_iot": -0.25,
            "iso_45001": -0.15,
            "plan_continuite": -0.20,
        }
    },
    
    "chimie_pharmacie": {
        "taux_base": 1.00,
        "majorations": {
            "substances_dangereuses": 0.30,
            "risque_contamination": 0.20,
            "non_conforme_normes": 0.40,
        },
        "reductions": {
            "iso_27001_it": -0.15,
            "systeme_securite_avance": -0.20,
            "certification_ecocert": -0.10,
        }
    }
}

# ============================================================
# 👥 ACTEURS MARCHE ASSURANCE MAROC
# ============================================================

ASSUREURS_MAROC = [
    {
        "nom": "ALLIANZ MAROC",
        "specialite": "Tous risques, dommages matériels",
        "presence": "Casablanca, Rabat, Fès",
    },
    {
        "nom": "AXA ASSURANCE MAROC",
        "specialite": "Tous risques, IARD",
        "presence": "Casablanca, Marrakech",
    },
    {
        "nom": "SAHAM ASSURANCE",
        "specialite": "Dommages, responsabilité civile",
        "presence": "National",
    },
    {
        "nom": "ZURICH MAROC",
        "specialite": "Assurances IARD, construction",
        "presence": "Casablanca, Agadir",
    },
    {
        "nom": "WAFA ASSURANCE",
        "specialite": "Tous risques, dommages",
        "presence": "National",
    },
]

# ============================================================
# 📞 CONTACTS UTILES
# ============================================================

CONTACTS_MAROC = {
    "acpr": {
        "nom": "Autorité de Contrôle Prudentiel et de Résolution",
        "email": "contact@acpr-maroc.ma",
        "telephone": "+212 537 70 47 47",
        "site": "www.acpr-maroc.ma",
    },
    "fga": {
        "nom": "Fonds de Garantie d'Assurance",
        "email": "info@fga.ma",
        "telephone": "+212 5 22 47 94 94",
        "site": "www.fga.ma",
    },
    "bank_al_maghrib": {
        "nom": "Bank Al-Maghrib",
        "email": "contact@bam.ma",
        "telephone": "+212 5 37 57 57 57",
        "site": "www.bam.ma",
    }
}

# ============================================================
# 📝 TERMINOLOGIE SPÉCIFIQUE PAR SECTEUR
# ============================================================

TERMINOLOGIE_SECTEUR = {
    "textile": {
        "équipement_clé": "Métier à tisser, encolleur, teinturerie",
        "panne_typique": "Arrêt chaîne production",
        "délai_pièce": "2-3 mois (Chine/Europe)",
        "risque_spécifique": "Électricité instable → dommages moteurs",
    },
    
    "agroalimentaire": {
        "équipement_clé": "Chaîne de production, chambre froide, broyeur",
        "panne_typique": "Perte marchandise périssable",
        "délai_pièce": "1-2 mois",
        "risque_spécifique": "Contamination = perte totale lot",
    },
    
    "mines": {
        "équipement_clé": "Pelleteuse, excavatrice, convoyeur (millions DH)",
        "panne_typique": "Arrêt complet mine",
        "délai_pièce": "2-4 mois (importation)",
        "risque_spécifique": "Perte d'exploitation = 10M+ DH/jour",
    }
}

# ============================================================
# 🎯 MESSAGES & LABELS MAROCAINS
# ============================================================

MESSAGES_MAROC = {
    "bienvenue": "🏭 Underwriting Premium — Industrie 4.0 Maroc",
    "sous_titre": "Évaluation de risques industriels pour assureurs marocains",
    "selecteur_secteur": "Choisissez votre secteur d'activité",
    "franchise_label": "Franchise recommandée (DH)",
    "prime_label": "Prime d'assurance estimée (DH)",
    "taux_prime_label": "Taux de prime (%)",
    "somme_assure": "Somme assurée (DH)",
    "devise_maroc": "Dirham marocain",
    
    "risque_faible": "✅ Risque acceptable",
    "risque_moyen": "⚠️ Risque à surveiller",
    "risque_eleve": "🔴 Risque élevé - Action recommandée",
    
    "action_accepter": "Accepter le risque",
    "action_accepter_conditions": "Accepter avec conditions",
    "action_refuser": "Refuser le risque",
    "action_demander_audit": "Demander audit technique",
    
    "franchise_maxi": "Franchise maximale acceptée",
    "conditions_imposees": "Conditions imposées par l'assureur",
    "duree_assurance": "Durée de l'assurance (ans)",
    "date_effet": "Date d'effet de la garantie",
}

# ============================================================
# ✅ CHECKLIST CONFORMITÉ MAROCAINE
# ============================================================

CHECKLIST_CONFORMITE = {
    "legale": [
        "✓ Déclaration à ACPR",
        "✓ Conformité code assurances Maroc",
        "✓ Respect délai 48h déclaration sinistre",
        "✓ Droit de rétractation 14 jours",
        "✓ Médiation agréée ACPR",
    ],
    
    "secteur": [
        "✓ Respect normes ISO applicables",
        "✓ Conformité CNAM/CNSS/OP",
        "✓ Certification secteur (HACCP pour agroalim)",
        "✓ Conformité environnementale (loi 11-03)",
    ],
    
    "technique": [
        "✓ Inspection initial recommandée",
        "✓ Plan de continuité d'activité",
        "✓ Audit technique annuel (risques élevés)",
        "✓ Documentation maintenance disponible",
    ],
}

print("✅ Configuration Marocaine chargée")
print(f"🇲🇦 Devise: {MAROC_CONFIG['devise']}")
print(f"📍 Pays: {MAROC_CONFIG['pays']}")
print(f"🏢 Secteurs disponibles: {len(SECTEURS_MAROC)}")
