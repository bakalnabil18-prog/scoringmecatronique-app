import { useState, useEffect, useRef } from "react";

// ═══════════════════════════════════════════════════════════════
// DATABASE — 8 MODULES COMPLETS
// ═══════════════════════════════════════════════════════════════

const DB_SCHEMA = {
  // ── MODULE 1: ROBOTS INDUSTRIELS ──────────────────────────
  robots: {
    label: "Robots Industriels", icon: "🤖", color: "#3b82f6",
    weight: 0.18,
    blocs: {
      identification: {
        label: "Bloc 1 — Identification Technique",
        fields: {
          typeRobot:        { label: "Type de robot",              type: "select", options: ["6 axes","5 axes","SCARA","Delta"], required: true },
          cobots:           { label: "Cobots présents",            type: "bool", required: true },
          celluleModulaire: { label: "Cellules robotisées modulaires", type: "bool" },
          marqueModele:     { label: "Marque & Modèle",            type: "text",   placeholder: "ex: FANUC R-2000iC" },
          anneeInstall:     { label: "Année d'installation",       type: "number", placeholder: "ex: 2019" },
          integrationReseau:{ label: "Intégration réseau",         type: "select", options: ["Isolé","Connecté MES","Connecté Cloud"], required: true },
        }
      },
      quantitatif: {
        label: "Bloc 2 — Données Quantitatives",
        fields: {
          nombreRobots:     { label: "Nombre total",               type: "number", required: true },
          valeurUnitaire:   { label: "Valeur unitaire (MAD)",      type: "number", placeholder: "ex: 500 000" },
          valeurTotaleParc: { label: "Valeur totale parc (MAD)",   type: "number", placeholder: "Calculée auto" },
          heuresFonct:      { label: "Heures moy. fonctionnement / an", type: "number", placeholder: "ex: 6 000" },
          mtbfRobots:       { label: "MTBF (heures)",              type: "number", hint: "Mean Time Between Failures" },
          mttrRobots:       { label: "MTTR (heures)",              type: "number", hint: "Mean Time To Repair" },
        }
      },
      scoring: {
        label: "Bloc 3 — Variables de Scoring",
        fields: {
          niveauRedondance:    { label: "Niveau redondance",           type: "select", options: ["Faible","Moyen","Élevé"], required: true, scoreKey: true },
          contratMaintenance:  { label: "Contrat maintenance constructeur", type: "bool", scoreKey: true },
          majFirmware:         { label: "Mise à jour firmware régulière",   type: "bool", scoreKey: true },
          historiquePannes:    { label: "Historique pannes 3 ans",     type: "select", options: ["0 panne","1-2 pannes","3-5 pannes","> 5 pannes"], scoreKey: true },
          capteursPredicifs:   { label: "Capteurs prédictifs présents", type: "bool", scoreKey: true },
          dependanceProduction:{ label: "Dépendance production",       type: "select", options: ["Faible","Moyenne","Critique"], required: true, scoreKey: true },
        }
      }
    }
  },

  // ── MODULE 2: MACHINES CNC ────────────────────────────────
  cnc: {
    label: "Machines CNC & Usinage", icon: "⚙️", color: "#8b5cf6",
    weight: 0.14,
    blocs: {
      identification: {
        label: "Bloc 1 — Identification",
        fields: {
          typeCNC:     { label: "Type CNC",          type: "select", options: ["3 axes","5 axes","Multi-broche"], required: true },
          marqueCNC:   { label: "Marque",             type: "text",   placeholder: "ex: DMG Mori, Mazak" },
          anneeCNC:    { label: "Année fabrication",  type: "number", placeholder: "ex: 2018" },
          automationCNC: { label: "Automatisation",   type: "select", options: ["Manuel","Semi-auto","Full auto"], required: true },
          interfaceMESERP: { label: "Interface MES / ERP", type: "bool" },
        }
      },
      technique: {
        label: "Bloc 2 — Données Techniques",
        fields: {
          nombreCNC:        { label: "Nombre total CNC",          type: "number", required: true },
          valeurUnitCNC:    { label: "Valeur unitaire (MAD)",     type: "number" },
          heuresCumulCNC:   { label: "Heures fonctionnement cumulées", type: "number" },
          typeRefroid:      { label: "Type refroidissement",      type: "select", options: ["Air","Eau","Huile","Mixte"] },
          sensibiliteElec:  { label: "Sensibilité électrique",    type: "bool", scoreKey: true },
          variateurFreq:    { label: "Variateurs de fréquence",   type: "bool" },
        }
      },
      risque: {
        label: "Bloc 3 — Indicateurs de Risque",
        fields: {
          freqMaintenancePrev: { label: "Fréquence maintenance préventive", type: "select", options: ["Mensuelle","Trimestrielle","Semestrielle","Annuelle","Aucune"], scoreKey: true },
          maintenancePredCNC:  { label: "Maintenance prédictive",           type: "bool", scoreKey: true },
          historiqueDomElec:   { label: "Historique dommage électrique",    type: "select", options: ["Aucun","1-2 incidents","3+ incidents"], scoreKey: true },
          protectionSurtension:{ label: "Protection surtension installée",  type: "bool", scoreKey: true },
          upsDedié:            { label: "Onduleur (UPS) dédié",             type: "bool", scoreKey: true },
        }
      }
    }
  },

  // ── MODULE 3: SYSTÈME CYBER-PHYSIQUE ─────────────────────
  cps: {
    label: "Système Cyber-Physique (CPS)", icon: "🌐", color: "#06b6d4",
    weight: 0.18,
    blocs: {
      architecture: {
        label: "Bloc 1 — Architecture CPS",
        fields: {
          presenceSCADA:    { label: "Présence SCADA",          type: "bool", scoreKey: true },
          mesIntegre:       { label: "MES intégré",             type: "bool", scoreKey: true },
          erpConnecte:      { label: "ERP connecté production", type: "bool" },
          cloudExterne:     { label: "Cloud externe",           type: "bool" },
          protocoleIndustriel: { label: "Protocole industriel", type: "select", options: ["OPC-UA","Modbus","Profinet","Autre"], scoreKey: true },
          segmentationReseau:  { label: "Niveau segmentation réseau", type: "select", options: ["Faible","Moyenne","Élevée"], scoreKey: true },
        }
      },
      infrastructureIT: {
        label: "Bloc 2 — Infrastructure IT",
        fields: {
          typeServeurs:       { label: "Type serveurs",               type: "select", options: ["Sur site","Cloud hybride","Cloud pur"] },
          redondanceServeurs: { label: "Redondance serveurs",         type: "bool", scoreKey: true },
          backupQuotidien:    { label: "Backup quotidien automatisé", type: "bool", scoreKey: true },
          rto:                { label: "RTO estimé (heures)",         type: "number", hint: "Recovery Time Objective", scoreKey: true },
          parefeuIndustriel:  { label: "Pare-feu industriel",         type: "bool", scoreKey: true },
          auditCyber:         { label: "Audit cybersécurité annuel",  type: "bool", scoreKey: true },
        }
      },
      assurantiel: {
        label: "Bloc 3 — Indicateurs Assurantiels",
        fields: {
          dependanceCPS:      { label: "Dépendance production au CPS", type: "select", options: ["Faible","Moyen","Critique"], required: true, scoreKey: true },
          historiqueIncidIT:  { label: "Historique incidents IT",      type: "select", options: ["Aucun","1-2/an","3+/an"], scoreKey: true },
          tempsMoyArretIT:    { label: "Temps moyen arrêt / incident IT (h)", type: "number" },
          planContinuite:     { label: "Plan de continuité (PCA)",     type: "bool", scoreKey: true },
          simulationCrise:    { label: "Simulation de crise annuelle", type: "bool", scoreKey: true },
        }
      }
    }
  },

  // ── MODULE 4: INFRASTRUCTURE ÉLECTRIQUE ──────────────────
  electrique: {
    label: "Infrastructure Électrique", icon: "⚡", color: "#f59e0b",
    weight: 0.10,
    blocs: {
      equipement: {
        label: "Bloc 1 — Équipement Électrique",
        fields: {
          tableauBTMT:      { label: "Tableau BT/MT intelligent",     type: "bool", scoreKey: true },
          protectionDiff:   { label: "Protection différentiel avancée", type: "bool", scoreKey: true },
          monitoringEnergie:{ label: "Système monitoring énergétique", type: "bool" },
          upsIndustriel:    { label: "UPS industriel",                type: "bool", scoreKey: true },
          groupeElectrogene:{ label: "Groupe électrogène",            type: "bool", scoreKey: true },
        }
      },
      donnees: {
        label: "Bloc 2 — Données Électriques",
        fields: {
          puissanceInstallee:   { label: "Puissance installée totale (kW)", type: "number" },
          tauxChargeMoyen:      { label: "Taux de charge moyen (%)",        type: "number", scoreKey: true },
          incidentsElectriques: { label: "Incidents électriques / an",      type: "select", options: ["0","1-2","3-5","> 5"], scoreKey: true },
          miseALaTerre:         { label: "Mise à la terre conforme",        type: "bool", scoreKey: true },
        }
      },
      impactScoring: {
        label: "Bloc 3 — Impact Scoring Électrique",
        fields: {
          vulnerabiliteDomElec: { label: "Vulnérabilité dommage électrique", type: "select", options: ["Faible","Modérée","Élevée"], scoreKey: true },
          risqueCourtCircuit:   { label: "Risque court-circuit évalué",      type: "bool" },
          risquePropagIncendie: { label: "Risque propagation incendie",      type: "select", options: ["Faible","Modéré","Élevé"], scoreKey: true },
        }
      }
    }
  },

  // ── MODULE 5: SYSTÈME DE MAINTENANCE ─────────────────────
  maintenance: {
    label: "Système de Maintenance", icon: "🔧", color: "#10b981",
    weight: 0.20,
    blocs: {
      organisation: {
        label: "Bloc 1 — Organisation Maintenance",
        fields: {
          gmaoUtilisee:  { label: "GMAO utilisée",           type: "bool", scoreKey: true },
          typeMaintenance: { label: "Type maintenance dominant", type: "select", options: ["Corrective","Préventive","Prédictive"], required: true, scoreKey: true },
          existenceKPI:  { label: "KPIs maintenance définis", type: "bool", scoreKey: true },
        }
      },
      indicateurs: {
        label: "Bloc 2 — Indicateurs Quantifiables",
        fields: {
          mtbfGlobal:           { label: "MTBF global (heures)",          type: "number", hint: "Mean Time Between Failures", scoreKey: true },
          mttrGlobal:           { label: "MTTR global (heures)",          type: "number", hint: "Mean Time To Repair", scoreKey: true },
          tauxMaintPlanifie:    { label: "Taux maintenance planifiée (%)", type: "number", scoreKey: true },
          tauxRespectPlanning:  { label: "Taux respect planning (%)",      type: "number", scoreKey: true },
          budgetMaintenance:    { label: "Budget maintenance / valeur parc (%)", type: "number" },
        }
      },
      maturite: {
        label: "Bloc 3 — Maturité Maintenance",
        fields: {
          niveauDigitalisation: { label: "Niveau digitalisation (1 à 5)", type: "select", options: ["1","2","3","4","5"], scoreKey: true },
          maintConditionnelle:  { label: "Maintenance conditionnelle capteurs", type: "bool", scoreKey: true },
          iaPredictive:         { label: "IA prédictive utilisée",         type: "bool", scoreKey: true },
        }
      }
    }
  },

  // ── MODULE 6: ÉQUIPEMENTS MANUTENTION ────────────────────
  manutention: {
    label: "Équipements & Manutention", icon: "🏗️", color: "#f97316",
    weight: 0.08,
    blocs: {
      equipements: {
        label: "Bloc 1 — Équipements de Manutention",
        fields: {
          presenceAGV:     { label: "AGV (véhicules autonomes)", type: "bool", scoreKey: true },
          chariotsElev:    { label: "Chariots élévateurs",       type: "bool" },
          pontsRoulants:   { label: "Ponts roulants",            type: "bool" },
          palansElec:      { label: "Palans électriques",        type: "bool" },
          outillageSpecial:{ label: "Outillage spécialisé maint.", type: "bool" },
          atelierInterne:  { label: "Atelier interne dédié",     type: "bool", scoreKey: true },
          nombreEquipManu: { label: "Nombre total équipements",  type: "number" },
          ageMoyenManu:    { label: "Âge moyen équipements (ans)", type: "number" },
          disponibiliteManu: { label: "Disponibilité (%)",       type: "number", scoreKey: true },
          tempsMobilisation: { label: "Temps mobilisation moyen (min)", type: "number", scoreKey: true },
        }
      },
      scoring: {
        label: "Bloc 2 — Variables Scoring Manutention",
        fields: {
          manutentionAuto:   { label: "Manutention automatisée",      type: "bool", scoreKey: true },
          redondEquipCrit:   { label: "Redondance équipements critiques", type: "bool", scoreKey: true },
          disponibilite247:  { label: "Disponibilité immédiate 24/7", type: "bool", scoreKey: true },
          dependancePrestataire: { label: "Dépendance prestataire externe", type: "bool", scoreKey: true },
        }
      }
    }
  },

  // ── MODULE 7: STOCKAGE & PIÈCES DE RECHANGE ─────────────
  stockage: {
    label: "Stockage & Pièces de Rechange", icon: "📦", color: "#ec4899",
    weight: 0.08,
    blocs: {
      infrastructure: {
        label: "Bloc 1 — Infrastructure de Stockage",
        fields: {
          magasinCentral:    { label: "Magasin central pièces",            type: "bool", scoreKey: true },
          rayonnageIntelligent: { label: "Rayonnage intelligent",          type: "bool" },
          stockageVerticalAuto: { label: "Stockage vertical automatisé",  type: "bool", scoreKey: true },
          zonePiecesCrit:    { label: "Zone pièces critiques dédiée",      type: "bool", scoreKey: true },
          controleThermHumi: { label: "Contrôle température/humidité",    type: "bool" },
        }
      },
      gestionNumerique: {
        label: "Bloc 2 — Gestion Numérique Stock",
        fields: {
          integrationERPstock: { label: "Intégration ERP stock",           type: "bool", scoreKey: true },
          stockMinimumDefini:  { label: "Stock minimum défini",            type: "bool", scoreKey: true },
          analyseABC:          { label: "Analyse ABC des pièces",          type: "bool", scoreKey: true },
          delaiReappro:        { label: "Délai réappro. fournisseur (jours)", type: "number", scoreKey: true },
          tauxRuptureStock:    { label: "Taux rupture stock 12 mois",      type: "select", options: ["0%","< 5%","5-15%","> 15%"], scoreKey: true },
          suiviConsommation:   { label: "Suivi consommation / demande réelle", type: "bool" },
        }
      },
      performance: {
        label: "Bloc 3 — Indicateurs de Performance",
        fields: {
          tempsMoyDispPiece:   { label: "Temps moyen dispo pièce critique (h)", type: "number", scoreKey: true },
          pctPiecesCritStock:  { label: "% pièces critiques en stock",     type: "number", scoreKey: true },
          tauxRotationStock:   { label: "Taux rotation stock",             type: "number" },
          valeurStockParc:     { label: "Valeur stock / valeur parc (%)",  type: "number" },
          predictionConso:     { label: "Prédiction conso via historique", type: "bool", scoreKey: true },
        }
      },
      assurantiel: {
        label: "Bloc 4 — Variables Assurantielles",
        fields: {
          piecesCritRedond:    { label: "Pièces critiques redondantes",    type: "bool", scoreKey: true },
          fournisseursMultiples: { label: "Fournisseurs multiples",        type: "bool", scoreKey: true },
          contratApproSrioPri: { label: "Contrat appro. prioritaire",     type: "bool", scoreKey: true },
          simulationPenurie:   { label: "Simulation pénurie annuelle",    type: "bool", scoreKey: true },
        }
      }
    }
  },

  // ── MODULE 8: EFFICACITÉ INTERVENTION MAINTENANCE ────────
  intervention: {
    label: "Efficacité Intervention Maintenance", icon: "🚨", color: "#ef4444",
    weight: 0.04,
    blocs: {
      organisation: {
        label: "Bloc 1 — Organisation Intervention",
        fields: {
          equipeInterne:    { label: "Équipe maintenance interne",        type: "bool", scoreKey: true },
          techniciensCertif:{ label: "Techniciens certifiés constructeur", type: "bool", scoreKey: true },
          astreinte247:     { label: "Astreinte 24/7",                   type: "bool", scoreKey: true },
          slaInterne:       { label: "Temps réponse SLA interne (h)",    type: "number", scoreKey: true },
        }
      },
      indicateurs: {
        label: "Bloc 2 — Indicateurs Quantifiés",
        fields: {
          mttrMoyen:        { label: "MTTR moyen (heures)",               type: "number", scoreKey: true },
          pctInterv4h:      { label: "% interventions < 4h",             type: "number", scoreKey: true },
          pctIntervPlanif:  { label: "% interventions planifiées",        type: "number", scoreKey: true },
          tauxResolutionPP: { label: "Taux résolution 1er passage (%)",   type: "number", scoreKey: true },
          historiqueArret24:{ label: "Arrêts > 24h (3 dernières années)", type: "number", scoreKey: true },
        }
      },
      digitalisation: {
        label: "Bloc 3 — Digitalisation Intervention",
        fields: {
          gmaoMobile:       { label: "GMAO mobile",                       type: "bool", scoreKey: true },
          tracabiliteRT:    { label: "Traçabilité intervention temps réel", type: "bool", scoreKey: true },
          historiquePannesAnalyse: { label: "Historique pannes analysé",  type: "bool", scoreKey: true },
          dashboardKPI:     { label: "Dashboard KPI maintenance",         type: "bool", scoreKey: true },
        }
      }
    }
  }
};

// ═══════════════════════════════════════════════════════════════
// SCORING ENGINE — 3 INDICES + 4 OUTPUTS
// ═══════════════════════════════════════════════════════════════

function computeScoreEngine(data) {
  const v = data;

  // ── SCORE MATURITÉ MÉCATRONIQUE (automatisation + capteurs + CPS + infra)
  let maturite = 0;
  // Robots
  if (v.integrationReseau === "Connecté Cloud") maturite += 12;
  else if (v.integrationReseau === "Connecté MES") maturite += 7;
  if (v.cobots === "oui") maturite += 6;
  if (v.celluleModulaire === "oui") maturite += 5;
  if (v.capteursPredicifs === "oui") maturite += 10;
  // CNC
  if (v.automationCNC === "Full auto") maturite += 10;
  else if (v.automationCNC === "Semi-auto") maturite += 5;
  if (v.interfaceMESERP === "oui") maturite += 5;
  if (v.maintenancePredCNC === "oui") maturite += 7;
  // CPS
  if (v.presenceSCADA === "oui") maturite += 8;
  if (v.mesIntegre === "oui") maturite += 7;
  if (v.protocoleIndustriel === "OPC-UA") maturite += 5;
  if (v.auditCyber === "oui") maturite += 5;
  // Manutention
  if (v.presenceAGV === "oui") maturite += 6;
  if (v.manutentionAuto === "oui") maturite += 4;
  // Maintenance
  if (v.iaPredictive === "oui") maturite += 8;
  if (v.maintConditionnelle === "oui") maturite += 6;
  const niveauDig = parseInt(v.niveauDigitalisation) || 0;
  maturite += niveauDig * 2;
  // Stockage
  if (v.stockageVerticalAuto === "oui") maturite += 4;
  if (v.predictionConso === "oui") maturite += 5;

  // ── SCORE RÉSILIENCE OPÉRATIONNELLE (maintenance + pièces + intervention + redondance)
  let resilience = 0;
  // Maintenance
  if (v.typeMaintenance === "Prédictive") resilience += 18;
  else if (v.typeMaintenance === "Préventive") resilience += 10;
  if (v.gmaoUtilisee === "oui") resilience += 8;
  if (v.existenceKPI === "oui") resilience += 5;
  const mttrG = parseFloat(v.mttrGlobal) || 99;
  if (mttrG < 2) resilience += 10;
  else if (mttrG < 4) resilience += 7;
  else if (mttrG < 8) resilience += 4;
  const tauxPlan = parseFloat(v.tauxMaintPlanifie) || 0;
  if (tauxPlan > 80) resilience += 8;
  else if (tauxPlan > 60) resilience += 5;
  // Intervention
  if (v.astreinte247 === "oui") resilience += 7;
  if (v.equipeInterne === "oui") resilience += 6;
  if (v.gmaoMobile === "oui") resilience += 4;
  if (v.tracabiliteRT === "oui") resilience += 4;
  const pct4h = parseFloat(v.pctInterv4h) || 0;
  if (pct4h > 80) resilience += 6;
  else if (pct4h > 60) resilience += 3;
  // Stockage
  if (v.piecesCritRedond === "oui") resilience += 8;
  if (v.fournisseursMultiples === "oui") resilience += 5;
  const pctStock = parseFloat(v.pctPiecesCritStock) || 0;
  if (pctStock > 90) resilience += 6;
  else if (pctStock > 70) resilience += 3;
  if (v.contratApproSrioPri === "oui") resilience += 4;
  // Redondance systèmes
  if (v.niveauRedondance === "Élevé") resilience += 7;
  else if (v.niveauRedondance === "Moyen") resilience += 3;
  if (v.redondanceServeurs === "oui") resilience += 5;
  if (v.planContinuite === "oui") resilience += 7;
  if (v.simulationCrise === "oui") resilience += 4;

  // ── SCORE VULNÉRABILITÉ SYSTÉMIQUE (inversé: haut = vulnérable)
  let vulne = 0;
  // Dépendance réseau
  if (v.dependanceCPS === "Critique") vulne += 20;
  else if (v.dependanceCPS === "Moyen") vulne += 10;
  if (v.dependanceProduction === "Critique") vulne += 15;
  else if (v.dependanceProduction === "Moyenne") vulne += 8;
  // Absence redondance IT
  if (v.redondanceServeurs !== "oui") vulne += 12;
  if (v.backupQuotidien !== "oui") vulne += 8;
  if (v.parefeuIndustriel !== "oui") vulne += 8;
  if (v.auditCyber !== "oui") vulne += 5;
  // Centralisation excessive
  if (v.segmentationReseau === "Faible") vulne += 10;
  else if (v.segmentationReseau === "Moyenne") vulne += 5;
  // Fragilité électrique
  if (v.upsIndustriel !== "oui") vulne += 6;
  if (v.miseALaTerre !== "oui") vulne += 6;
  if (v.incidentsElectriques === "> 5") vulne += 8;
  else if (v.incidentsElectriques === "3-5") vulne += 4;
  if (v.vulnerabiliteDomElec === "Élevée") vulne += 8;
  else if (v.vulnerabiliteDomElec === "Modérée") vulne += 4;
  // Historique incidents
  if (v.historiqueIncidIT === "3+/an") vulne += 8;
  else if (v.historiqueIncidIT === "1-2/an") vulne += 4;
  if (v.historiqueArret24 > 3) vulne += 6;
  else if (v.historiqueArret24 > 1) vulne += 3;

  // ── MODULE SCORES (pour radar)
  const moduleScores = {
    robots: computeModuleScore_robots(v),
    cnc: computeModuleScore_cnc(v),
    cps: computeModuleScore_cps(v),
    electrique: computeModuleScore_elec(v),
    maintenance: computeModuleScore_maintenance(v),
    stockage: computeModuleScore_stockage(v),
    manutention: computeModuleScore_manutention(v),
    intervention: computeModuleScore_intervention(v),
  };

  const clamp = v => Math.min(100, Math.max(0, Math.round(v)));
  const scoreMaturite = clamp(maturite);
  const scoreResilience = clamp(resilience);
  const scoreVulnerabilite = clamp(vulne);
  // Score global = maturité 35% + résilience 45% + (100-vulnérabilité) 20%
  const scoreGlobal = clamp(scoreMaturite * 0.35 + scoreResilience * 0.45 + (100 - scoreVulnerabilite) * 0.20);

  return { scoreMaturite, scoreResilience, scoreVulnerabilite, scoreGlobal, moduleScores };
}

function computeModuleScore_robots(v) {
  let s = 0;
  if (v.integrationReseau === "Connecté Cloud") s += 25; else if (v.integrationReseau === "Connecté MES") s += 15;
  if (v.niveauRedondance === "Élevé") s += 25; else if (v.niveauRedondance === "Moyen") s += 12;
  if (v.contratMaintenance === "oui") s += 15;
  if (v.capteursPredicifs === "oui") s += 20;
  if (v.historiquePannes === "0 panne") s += 15; else if (v.historiquePannes === "1-2 pannes") s += 8;
  return Math.min(100, s);
}

function computeModuleScore_cnc(v) {
  let s = 0;
  if (v.automationCNC === "Full auto") s += 25; else if (v.automationCNC === "Semi-auto") s += 13;
  if (v.upsDedié === "oui") s += 20;
  if (v.protectionSurtension === "oui") s += 15;
  if (v.maintenancePredCNC === "oui") s += 20;
  if (v.sensibiliteElec !== "oui") s += 10;
  if (v.freqMaintenancePrev === "Mensuelle") s += 10; else if (v.freqMaintenancePrev === "Trimestrielle") s += 6;
  return Math.min(100, s);
}

function computeModuleScore_cps(v) {
  let s = 0;
  if (v.presenceSCADA === "oui") s += 12;
  if (v.mesIntegre === "oui") s += 12;
  if (v.redondanceServeurs === "oui") s += 18;
  if (v.backupQuotidien === "oui") s += 12;
  if (v.parefeuIndustriel === "oui") s += 12;
  if (v.auditCyber === "oui") s += 12;
  if (v.segmentationReseau === "Élevée") s += 10; else if (v.segmentationReseau === "Moyenne") s += 5;
  if (v.planContinuite === "oui") s += 12;
  return Math.min(100, s);
}

function computeModuleScore_elec(v) {
  let s = 20;
  if (v.tableauBTMT === "oui") s += 15;
  if (v.protectionDiff === "oui") s += 15;
  if (v.upsIndustriel === "oui") s += 15;
  if (v.groupeElectrogene === "oui") s += 12;
  if (v.miseALaTerre === "oui") s += 15;
  if (v.incidentsElectriques === "0") s += 8;
  return Math.min(100, s);
}

function computeModuleScore_maintenance(v) {
  let s = 0;
  if (v.typeMaintenance === "Prédictive") s += 30; else if (v.typeMaintenance === "Préventive") s += 18;
  if (v.gmaoUtilisee === "oui") s += 15;
  if (v.iaPredictive === "oui") s += 20;
  if (v.maintConditionnelle === "oui") s += 15;
  const nd = parseInt(v.niveauDigitalisation) || 0;
  s += nd * 4;
  return Math.min(100, s);
}

function computeModuleScore_stockage(v) {
  let s = 10;
  if (v.piecesCritRedond === "oui") s += 22;
  if (v.fournisseursMultiples === "oui") s += 18;
  if (v.integrationERPstock === "oui") s += 12;
  if (v.analyseABC === "oui") s += 10;
  if (v.tauxRuptureStock === "0%") s += 18; else if (v.tauxRuptureStock === "< 5%") s += 10;
  if (v.stockMinimumDefini === "oui") s += 10;
  return Math.min(100, s);
}

function computeModuleScore_manutention(v) {
  let s = 15;
  if (v.presenceAGV === "oui") s += 20;
  if (v.manutentionAuto === "oui") s += 15;
  if (v.disponibilite247 === "oui") s += 20;
  if (v.redondEquipCrit === "oui") s += 15;
  if (v.dependancePrestataire !== "oui") s += 15;
  return Math.min(100, s);
}

function computeModuleScore_intervention(v) {
  let s = 0;
  if (v.astreinte247 === "oui") s += 18;
  if (v.equipeInterne === "oui") s += 15;
  if (v.techniciensCertif === "oui") s += 12;
  if (v.gmaoMobile === "oui") s += 10;
  if (v.tracabiliteRT === "oui") s += 10;
  if (v.dashboardKPI === "oui") s += 10;
  const pct4 = parseFloat(v.pctInterv4h) || 0;
  if (pct4 > 80) s += 15; else if (pct4 > 60) s += 8;
  const res = parseFloat(v.tauxResolutionPP) || 0;
  if (res > 85) s += 10;
  return Math.min(100, s);
}

function generateZonesCritiques(scores, data) {
  const zones = [];
  if (scores.scoreVulnerabilite > 50 && data.redondanceServeurs !== "oui")
    zones.push({ level: "critique", desc: "Absence redondance serveur MES/CPS — risque systémique élevé" });
  const mttr = parseFloat(data.mttrGlobal) || 0;
  if (mttr > 12)
    zones.push({ level: "critique", desc: `MTTR global > 12h (${mttr}h) — allongement durée sinistre` });
  if (data.piecesCritRedond !== "oui" && data.tauxRuptureStock !== "0%")
    zones.push({ level: "majeur", desc: "Stock pièces critiques insuffisant — risque BDM aggravé" });
  if (data.dependanceCPS === "Critique" && data.planContinuite !== "oui")
    zones.push({ level: "critique", desc: "Dépendance CPS critique sans PCA — perte d'exploitation totale" });
  if (data.upsIndustriel !== "oui" && data.protectionSurtension !== "oui")
    zones.push({ level: "majeur", desc: "Infrastructure électrique non protégée — dommages électriques potentiels" });
  if (data.auditCyber !== "oui" && data.segmentationReseau === "Faible")
    zones.push({ level: "majeur", desc: "Réseau industriel non segmenté sans audit cyber annuel" });
  return zones;
}

function generateRecommandations(scores, data) {
  const recs = [];
  if (scores.scoreResilience < 50)
    recs.push({ priorite: "Urgente", action: "Passer à une maintenance prédictive via IA — impact direct sur MTTR et perte d'exploitation." });
  if (data.redondanceServeurs !== "oui")
    recs.push({ priorite: "Urgente", action: "Exiger redondance serveurs MES/SCADA — risque d'arrêt total de production." });
  if (data.planContinuite !== "oui")
    recs.push({ priorite: "Prioritaire", action: "Établir un Plan de Continuité d'Activité (PCA) avec simulation annuelle." });
  if (data.auditCyber !== "oui")
    recs.push({ priorite: "Prioritaire", action: "Programmer un audit cybersécurité annuel sur l'infrastructure industrielle." });
  if (data.fournisseursMultiples !== "oui")
    recs.push({ priorite: "Recommandée", action: "Diversifier les fournisseurs de pièces critiques pour réduire le risque BDM." });
  if (data.niveauRedondance === "Faible")
    recs.push({ priorite: "Recommandée", action: "Augmenter le niveau de redondance robotique pour réduire la criticité." });
  if (scores.scoreMaturite < 40)
    recs.push({ priorite: "Recommandée", action: "Accélérer l'intégration CPS : connecter les équipements au MES/Cloud." });
  return recs.slice(0, 5);
}

// ═══════════════════════════════════════════════════════════════
// INITIAL FORM STATE (flat map of all fields)
// ═══════════════════════════════════════════════════════════════

function buildInitialForm() {
  const form = { entreprise: "", secteur: "", ville: "" };
  Object.values(DB_SCHEMA).forEach(module => {
    Object.values(module.blocs).forEach(bloc => {
      Object.keys(bloc.fields).forEach(key => {
        form[key] = "";
      });
    });
  });
  return form;
}

// ═══════════════════════════════════════════════════════════════
// UI COMPONENTS
// ═══════════════════════════════════════════════════════════════

const C = {
  navy: "#0f2244",
  blue: "#1d4ed8",
  blue2: "#3b82f6",
  bg: "#f0f4ff",
  white: "#ffffff",
  border: "#e2e8f0",
  text: "#1e293b",
  muted: "#64748b",
  green: "#10b981",
  amber: "#f59e0b",
  red: "#ef4444",
};

function inp(overrides = {}) {
  return {
    border: `1px solid ${C.border}`,
    borderRadius: "7px",
    padding: "7px 11px",
    fontSize: "12px",
    fontFamily: "'Sora', sans-serif",
    color: C.text,
    background: "#fff",
    width: "100%",
    boxSizing: "border-box",
    outline: "none",
    ...overrides,
  };
}

function Field({ fieldKey, def, value, onChange }) {
  const base = inp();
  if (def.type === "bool") {
    return (
      <div style={{ display: "flex", flexDirection: "column", gap: "4px" }}>
        <label style={{ fontSize: "11px", fontWeight: "600", color: C.muted, fontFamily: "'Sora', sans-serif" }}>
          {def.label} {def.required && <span style={{ color: C.red }}>*</span>}
        </label>
        <select style={{ ...base, cursor: "pointer" }} value={value} onChange={e => onChange(fieldKey, e.target.value)}>
          <option value="">—</option>
          <option value="oui">✅ Oui</option>
          <option value="non">❌ Non</option>
        </select>
      </div>
    );
  }
  if (def.type === "select") {
    return (
      <div style={{ display: "flex", flexDirection: "column", gap: "4px" }}>
        <label style={{ fontSize: "11px", fontWeight: "600", color: C.muted, fontFamily: "'Sora', sans-serif" }}>
          {def.label} {def.required && <span style={{ color: C.red }}>*</span>}
        </label>
        <select style={{ ...base, cursor: "pointer" }} value={value} onChange={e => onChange(fieldKey, e.target.value)}>
          <option value="">Sélectionner...</option>
          {def.options.map(o => <option key={o} value={o}>{o}</option>)}
        </select>
      </div>
    );
  }
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "4px" }}>
      <label style={{ fontSize: "11px", fontWeight: "600", color: C.muted, fontFamily: "'Sora', sans-serif" }}>
        {def.label} {def.required && <span style={{ color: C.red }}>*</span>}
        {def.hint && <span style={{ color: "#94a3b8", fontWeight: "400" }}> ⓘ</span>}
      </label>
      <input style={base} type={def.type === "number" ? "number" : "text"} placeholder={def.placeholder || ""} value={value} onChange={e => onChange(fieldKey, e.target.value)} />
    </div>
  );
}

function Gauge({ score, size = 180 }) {
  const angle = -135 + (score / 100) * 270;
  const color = score >= 70 ? C.green : score >= 40 ? C.amber : C.red;
  const label = score >= 70 ? "Risque Faible" : score >= 40 ? "Risque Modéré" : "Risque Élevé";
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
      <svg width={size} height={size * 0.65} viewBox="0 0 200 130">
        <defs>
          <linearGradient id="g1" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor={C.red} />
            <stop offset="50%" stopColor={C.amber} />
            <stop offset="100%" stopColor={C.green} />
          </linearGradient>
        </defs>
        <path d="M 20 115 A 80 80 0 0 1 180 115" fill="none" stroke="#e2e8f0" strokeWidth="14" strokeLinecap="round" />
        <path d="M 20 115 A 80 80 0 0 1 180 115" fill="none" stroke="url(#g1)" strokeWidth="14" strokeLinecap="round" />
        <g transform={`rotate(${angle}, 100, 115)`}>
          <line x1="100" y1="115" x2="100" y2="45" stroke={C.navy} strokeWidth="2.5" strokeLinecap="round" />
          <circle cx="100" cy="115" r="5" fill={C.navy} />
        </g>
        <text x="100" y="93" textAnchor="middle" fontSize="10" fill={C.muted} fontFamily="'Sora', sans-serif" fontWeight="600">SCORE FINAL</text>
        <text x="100" y="116" textAnchor="middle" fontSize="28" fontWeight="800" fill={C.navy} fontFamily="'Sora', sans-serif">{score}</text>
        <text x="126" y="116" textAnchor="start" fontSize="13" fill={C.muted} fontFamily="'Sora', sans-serif">/ 100</text>
      </svg>
      <span style={{ background: color + "20", color, border: `1px solid ${color}50`, borderRadius: "20px", padding: "2px 14px", fontSize: "11px", fontWeight: "700", fontFamily: "'Sora', sans-serif" }}>{label}</span>
    </div>
  );
}

function RadarHex({ scores }) {
  const labels = ["Robots", "CNC", "CPS", "Élec.", "Maint.", "Stock", "Manu.", "Interv."];
  const cx = 120, cy = 120, r = 90;
  const n = labels.length;
  const toXY = (val, i) => {
    const angle = (i * 2 * Math.PI / n) - Math.PI / 2;
    const d = (val / 100) * r;
    return { x: cx + d * Math.cos(angle), y: cy + d * Math.sin(angle) };
  };
  const grid = [0.25, 0.5, 0.75, 1];
  const scoreArr = [scores.robots, scores.cnc, scores.cps, scores.electrique, scores.maintenance, scores.stockage, scores.manutention, scores.intervention];
  const pts = scoreArr.map((s, i) => toXY(s, i));
  return (
    <svg width="240" height="240" viewBox="0 0 240 240">
      {grid.map(g => {
        const gp = Array.from({ length: n }, (_, i) => {
          const angle = (i * 2 * Math.PI / n) - Math.PI / 2;
          return `${cx + g * r * Math.cos(angle)},${cy + g * r * Math.sin(angle)}`;
        }).join(" ");
        return <polygon key={g} points={gp} fill="none" stroke="#e2e8f0" strokeWidth="1" />;
      })}
      {Array.from({ length: n }, (_, i) => {
        const angle = (i * 2 * Math.PI / n) - Math.PI / 2;
        return <line key={i} x1={cx} y1={cy} x2={cx + r * Math.cos(angle)} y2={cy + r * Math.sin(angle)} stroke="#e2e8f0" strokeWidth="1" />;
      })}
      <polygon points={pts.map(p => `${p.x},${p.y}`).join(" ")} fill={C.blue2 + "25"} stroke={C.blue2} strokeWidth="2" />
      {pts.map((p, i) => <circle key={i} cx={p.x} cy={p.y} r="4" fill={C.blue2} />)}
      {labels.map((l, i) => {
        const angle = (i * 2 * Math.PI / n) - Math.PI / 2;
        const lx = cx + (r + 20) * Math.cos(angle);
        const ly = cy + (r + 20) * Math.sin(angle);
        return <text key={i} x={lx} y={ly} textAnchor="middle" dominantBaseline="middle" fontSize="9" fill={C.muted} fontFamily="'Sora', sans-serif" fontWeight="700">{l}</text>;
      })}
    </svg>
  );
}

function IndexCard({ label, score, icon, color, subtitle }) {
  return (
    <div style={{ background: color + "12", borderRadius: "10px", padding: "12px", border: `1px solid ${color}30`, flex: 1 }}>
      <div style={{ fontSize: "18px", marginBottom: "4px" }}>{icon}</div>
      <div style={{ fontSize: "22px", fontWeight: "800", color, fontFamily: "'Sora', sans-serif", lineHeight: 1 }}>{score}</div>
      <div style={{ fontSize: "9px", color: C.muted, fontWeight: "600", fontFamily: "'Sora', sans-serif", marginTop: "2px", lineHeight: 1.3 }}>{label}</div>
      {subtitle && <div style={{ fontSize: "8px", color: color, fontWeight: "700", marginTop: "2px" }}>{subtitle}</div>}
    </div>
  );
}

function TrafficLight({ label, score }) {
  const color = score >= 70 ? C.green : score >= 40 ? C.amber : C.red;
  const emoji = score >= 70 ? "🟢" : score >= 40 ? "🟡" : "🔴";
  const lvl = score >= 70 ? "BON" : score >= 40 ? "MOYEN" : "CRITIQUE";
  return (
    <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", padding: "6px 10px", background: "#f8fafc", borderRadius: "7px", marginBottom: "5px" }}>
      <span style={{ fontSize: "11px", color: C.text, fontFamily: "'Sora', sans-serif", fontWeight: "500" }}>{label}</span>
      <div style={{ display: "flex", alignItems: "center", gap: "5px" }}>
        <span style={{ fontSize: "11px", fontWeight: "800", color, fontFamily: "'Sora', sans-serif" }}>{score}</span>
        <span style={{ fontSize: "9px", color, fontWeight: "700", background: color + "20", borderRadius: "4px", padding: "1px 5px" }}>{lvl}</span>
      </div>
    </div>
  );
}

// ═══════════════════════════════════════════════════════════════
// MAIN APP
// ═══════════════════════════════════════════════════════════════

const MODULE_KEYS = Object.keys(DB_SCHEMA);
const STEPS = [
  { label: "Identification & Robots", modules: ["robots"] },
  { label: "CNC & Système CPS", modules: ["cnc", "cps"] },
  { label: "Électrique & Maintenance", modules: ["electrique", "maintenance"] },
  { label: "Manutention & Stockage", modules: ["manutention", "stockage"] },
  { label: "Intervention & Résultats", modules: ["intervention"] },
];

export default function App() {
  const [step, setStep] = useState(0);
  const [form, setForm] = useState(buildInitialForm);
  const [results, setResults] = useState(null);
  const [animated, setAnimated] = useState(false);

  const setField = (key, val) => setForm(f => ({ ...f, [key]: val }));

  const calculate = () => {
    const r = computeScoreEngine(form);
    setResults(r);
    setAnimated(false);
    setTimeout(() => setAnimated(true), 100);
  };

  useEffect(() => {
    if (results) {
      const r = computeScoreEngine(form);
      setResults(r);
    }
  }, [form]);

  const currentModules = STEPS[step]?.modules || [];
  const zones = results ? generateZonesCritiques(results, form) : [];
  const recs = results ? generateRecommandations(results, form) : [];

  const profil = results
    ? results.scoreGlobal >= 75 ? "Industrie 4.0 Avancé"
    : results.scoreGlobal >= 50 ? "Industrie 4.0 Intermédiaire"
    : results.scoreGlobal >= 30 ? "Industrie 3.0 en transition"
    : "Industrie traditionnelle"
    : "—";

  return (
    <div style={{ minHeight: "100vh", background: C.bg, fontFamily: "'Sora', sans-serif", padding: "16px" }}>
      <link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700;800&display=swap" rel="stylesheet" />

      {/* HEADER */}
      <div style={{
        background: `linear-gradient(135deg, ${C.navy} 0%, #1e3a8a 60%, #1d4ed8 100%)`,
        borderRadius: "14px", padding: "14px 22px", marginBottom: "16px",
        display: "flex", alignItems: "center", justifyContent: "space-between",
        boxShadow: "0 4px 24px rgba(29,78,216,0.25)"
      }}>
        <div>
          <div style={{ fontSize: "10px", color: "#93c5fd", fontWeight: "700", letterSpacing: "2px", textTransform: "uppercase" }}>Prototype PFE — Scoring Risque</div>
          <div style={{ fontSize: "18px", fontWeight: "800", color: "#fff", marginTop: "2px" }}>Évaluation Résilience Industrielle 4.0</div>
          <div style={{ fontSize: "10px", color: "#bfdbfe", marginTop: "2px" }}>8 modules · 3 indices · 4 outputs · Mécatronique × Maintenance × IARD</div>
        </div>
        <div style={{ textAlign: "right" }}>
          <div style={{ fontSize: "30px" }}>🏭</div>
          <div style={{ fontSize: "9px", color: "#93c5fd", fontWeight: "600" }}>v2.0 — Complet</div>
        </div>
      </div>

      <div style={{ display: "flex", gap: "16px", alignItems: "flex-start" }}>

        {/* ══ LEFT PANEL — FORMULAIRE ══ */}
        <div style={{ flex: "1 1 60%", minWidth: 0 }}>

          {/* Stepper */}
          <div style={{ background: C.white, borderRadius: "12px", border: `1px solid ${C.border}`, padding: "14px 18px", marginBottom: "14px" }}>
            <div style={{ fontSize: "13px", fontWeight: "700", color: C.navy, marginBottom: "10px" }}>Formulaire d'Analyse — Nouveau Scoring Industriel 4.0</div>
            <div style={{ display: "flex", alignItems: "center" }}>
              {STEPS.map((s, i) => (
                <div key={i} style={{ display: "flex", alignItems: "center", flex: 1 }}>
                  <div style={{ display: "flex", flexDirection: "column", alignItems: "center", cursor: "pointer" }} onClick={() => setStep(i)}>
                    <div style={{
                      width: "26px", height: "26px", borderRadius: "50%",
                      background: step > i ? C.blue : step === i ? C.blue2 : "#e2e8f0",
                      color: step >= i ? "#fff" : C.muted,
                      display: "flex", alignItems: "center", justifyContent: "center",
                      fontSize: "11px", fontWeight: "800",
                      boxShadow: step === i ? `0 0 0 3px ${C.blue2}40` : "none",
                      transition: "all 0.3s"
                    }}>{i + 1}</div>
                    <div style={{ fontSize: "9px", color: step === i ? C.blue2 : C.muted, fontWeight: step === i ? "700" : "500", marginTop: "3px", textAlign: "center", maxWidth: "70px", lineHeight: 1.2 }}>{s.label}</div>
                  </div>
                  {i < STEPS.length - 1 && <div style={{ flex: 1, height: "2px", background: step > i ? C.blue : "#e2e8f0", margin: "0 4px", marginBottom: "18px", transition: "background 0.3s" }} />}
                </div>
              ))}
            </div>
          </div>

          {/* Client identification (always visible on step 0) */}
          {step === 0 && (
            <div style={{ background: C.white, borderRadius: "12px", border: `1px solid ${C.border}`, padding: "16px", marginBottom: "14px" }}>
              <div style={{ fontSize: "13px", fontWeight: "700", color: C.navy, marginBottom: "12px" }}>Identification du Client</div>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: "10px" }}>
                <Field fieldKey="entreprise" def={{ label: "Nom de l'entreprise", type: "text", placeholder: "Entrez l'entreprise", required: true }} value={form.entreprise} onChange={setField} />
                <Field fieldKey="secteur" def={{ label: "Secteur d'activité", type: "select", options: ["Automobile","Aéronautique","Agroalimentaire","Chimie/Pharma","Métallurgie","Électronique","Textile","BTP","Autre"], required: true }} value={form.secteur} onChange={setField} />
                <Field fieldKey="ville" def={{ label: "Ville", type: "text", placeholder: "Entrez la ville", required: true }} value={form.ville} onChange={setField} />
              </div>
            </div>
          )}

          {/* Module forms */}
          {currentModules.map(modKey => {
            const mod = DB_SCHEMA[modKey];
            return (
              <div key={modKey} style={{ background: C.white, borderRadius: "12px", border: `1px solid ${C.border}`, padding: "16px", marginBottom: "14px" }}>
                <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "14px" }}>
                  <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                    <div style={{ width: "32px", height: "32px", borderRadius: "8px", background: mod.color + "20", display: "flex", alignItems: "center", justifyContent: "center", fontSize: "16px" }}>{mod.icon}</div>
                    <div>
                      <div style={{ fontSize: "13px", fontWeight: "700", color: C.navy }}>{mod.label}</div>
                      <div style={{ fontSize: "10px", color: C.muted }}>Poids scoring : {Math.round(mod.weight * 100)}%</div>
                    </div>
                  </div>
                  <div style={{ background: mod.color + "15", color: mod.color, borderRadius: "6px", padding: "2px 10px", fontSize: "10px", fontWeight: "700", border: `1px solid ${mod.color}30` }}>MODULE</div>
                </div>

                {Object.entries(mod.blocs).map(([blocKey, bloc]) => (
                  <div key={blocKey} style={{ marginBottom: "14px" }}>
                    <div style={{ fontSize: "11px", fontWeight: "700", color: mod.color, textTransform: "uppercase", letterSpacing: "0.5px", marginBottom: "8px", paddingBottom: "4px", borderBottom: `1px solid ${mod.color}20` }}>
                      {bloc.label}
                    </div>
                    <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: "8px" }}>
                      {Object.entries(bloc.fields).map(([fieldKey, def]) => (
                        <Field key={fieldKey} fieldKey={fieldKey} def={def} value={form[fieldKey]} onChange={setField} />
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            );
          })}

          {/* Navigation */}
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginTop: "8px" }}>
            <button
              onClick={() => setStep(s => Math.max(0, s - 1))}
              disabled={step === 0}
              style={{ padding: "9px 20px", borderRadius: "8px", border: `1px solid ${C.border}`, background: C.white, color: step === 0 ? "#cbd5e1" : C.text, cursor: step === 0 ? "default" : "pointer", fontSize: "12px", fontWeight: "700", fontFamily: "'Sora', sans-serif" }}
            >← Précédent</button>

            <div style={{ fontSize: "11px", color: C.muted, fontWeight: "500" }}>Étape {step + 1} / {STEPS.length}</div>

            {step < STEPS.length - 1 ? (
              <button
                onClick={() => setStep(s => Math.min(STEPS.length - 1, s + 1))}
                style={{ padding: "9px 20px", borderRadius: "8px", border: "none", background: `linear-gradient(90deg, ${C.blue} 0%, ${C.blue2} 100%)`, color: "#fff", cursor: "pointer", fontSize: "12px", fontWeight: "700", fontFamily: "'Sora', sans-serif", boxShadow: `0 3px 12px ${C.blue2}40` }}
              >Suivant →</button>
            ) : (
              <button
                onClick={calculate}
                style={{ padding: "9px 24px", borderRadius: "8px", border: "none", background: `linear-gradient(90deg, #059669 0%, ${C.green} 100%)`, color: "#fff", cursor: "pointer", fontSize: "12px", fontWeight: "700", fontFamily: "'Sora', sans-serif", boxShadow: `0 3px 12px ${C.green}50` }}
              >✅ Valider et Calculer</button>
            )}
          </div>
        </div>

        {/* ══ RIGHT PANEL — RÉSULTATS ══ */}
        <div style={{ flex: "0 0 310px", width: "310px" }}>
          <div style={{ background: C.white, borderRadius: "14px", border: `1px solid ${C.border}`, padding: "18px", position: "sticky", top: "16px", boxShadow: "0 2px 16px rgba(0,0,0,0.06)" }}>

            {/* Header résultats */}
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "14px" }}>
              <div style={{ fontSize: "13px", fontWeight: "700", color: C.navy }}>Résultats en Temps Réel</div>
              <div style={{ display: "flex", gap: "5px", fontSize: "14px", cursor: "pointer" }}>🌐 ℹ️</div>
            </div>

            {/* GAUGE */}
            <Gauge score={results ? results.scoreGlobal : 0} />

            {/* 3 INDICES PRINCIPAUX */}
            <div style={{ display: "flex", gap: "6px", marginTop: "14px" }}>
              <IndexCard label="Maturité Mécatronique" score={results ? results.scoreMaturite : "--"} icon="⚙️" color={C.blue2} subtitle="Automatisation + CPS" />
              <IndexCard label="Résilience Opérationnelle" score={results ? results.scoreResilience : "--"} icon="🛡️" color={C.green} subtitle="Maintenance + Stock" />
              <IndexCard label="Vulnérabilité Systémique" score={results ? results.scoreVulnerabilite : "--"} icon="🔎" color={C.red} subtitle="↓ = Moins vulnérable" />
            </div>

            {/* RADAR */}
            {results && (
              <div style={{ marginTop: "14px" }}>
                <div style={{ fontSize: "11px", fontWeight: "700", color: C.navy, marginBottom: "6px" }}>Répartition par Module</div>
                <div style={{ display: "flex", justifyContent: "center" }}>
                  <RadarHex scores={results.moduleScores} />
                </div>
              </div>
            )}

            {/* FEU TRICOLORE PAR MODULE */}
            {results && (
              <div style={{ marginTop: "10px" }}>
                <div style={{ fontSize: "11px", fontWeight: "700", color: C.navy, marginBottom: "6px" }}>Feu Tricolore — 8 Modules</div>
                {Object.entries(results.moduleScores).map(([key, score]) => (
                  <TrafficLight key={key} label={`${DB_SCHEMA[key]?.icon} ${DB_SCHEMA[key]?.label}`} score={score} />
                ))}
              </div>
            )}

            {/* SYNTHÈSE SOUSCRIPTEUR */}
            {results && (
              <div style={{ marginTop: "14px", background: "#eff6ff", borderRadius: "10px", padding: "12px", border: "1px solid #bfdbfe" }}>
                <div style={{ fontSize: "10px", fontWeight: "800", color: C.blue, textTransform: "uppercase", letterSpacing: "1px", marginBottom: "6px" }}>Synthèse Souscripteur</div>
                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "6px", marginBottom: "8px" }}>
                  {[
                    ["Profil industriel", profil],
                    ["Intégration digitale", results.scoreMaturite >= 60 ? "Élevée" : results.scoreMaturite >= 35 ? "Modérée" : "Faible"],
                    ["Résilience maintenance", results.scoreResilience >= 60 ? "Solide" : results.scoreResilience >= 35 ? "Modérée" : "Insuffisante"],
                    ["Vulnérabilité IT/Cyber", results.scoreVulnerabilite > 60 ? "Critique" : results.scoreVulnerabilite > 35 ? "Modérée" : "Faible"],
                  ].map(([l, v]) => (
                    <div key={l} style={{ background: C.white, borderRadius: "6px", padding: "6px 8px", border: "1px solid #dbeafe" }}>
                      <div style={{ fontSize: "9px", color: C.muted, fontWeight: "600" }}>{l}</div>
                      <div style={{ fontSize: "11px", color: C.blue, fontWeight: "700" }}>{v}</div>
                    </div>
                  ))}
                </div>
                <div style={{ fontSize: "10px", color: "#374151", lineHeight: 1.6 }}>
                  {form.entreprise && <strong>{form.entreprise}</strong>} présente {results.scoreGlobal >= 70 ? "une résilience industrielle avancée avec une bonne capacité d'absorption." : results.scoreGlobal >= 40 ? "un profil intermédiaire avec des zones de fragilité opérationnelle identifiées." : "un niveau de vulnérabilité élevé nécessitant des mesures correctives urgentes."}
                </div>
              </div>
            )}

            {/* ZONES CRITIQUES */}
            {results && zones.length > 0 && (
              <div style={{ marginTop: "12px" }}>
                <div style={{ fontSize: "11px", fontWeight: "700", color: C.red, marginBottom: "6px" }}>🗺️ Carte des Points Sensibles</div>
                {zones.map((z, i) => (
                  <div key={i} style={{
                    borderLeft: `3px solid ${z.level === "critique" ? C.red : C.amber}`,
                    background: z.level === "critique" ? "#fef2f2" : "#fffbeb",
                    borderRadius: "4px", padding: "6px 10px", marginBottom: "5px", fontSize: "10px", color: C.text
                  }}>
                    <span style={{ fontWeight: "700", color: z.level === "critique" ? C.red : C.amber }}>Zone {z.level === "critique" ? "CRITIQUE" : "MAJEURE"} :</span> {z.desc}
                  </div>
                ))}
              </div>
            )}

            {/* RECOMMANDATIONS */}
            {results && recs.length > 0 && (
              <div style={{ marginTop: "12px", borderTop: `1px solid ${C.border}`, paddingTop: "10px" }}>
                <div style={{ fontSize: "11px", fontWeight: "700", color: C.navy, marginBottom: "7px" }}>Recommandations</div>
                {recs.map((r, i) => (
                  <div key={i} style={{ display: "flex", gap: "7px", marginBottom: "7px", alignItems: "flex-start" }}>
                    <span style={{
                      fontSize: "8px", fontWeight: "800", padding: "2px 6px", borderRadius: "4px",
                      background: r.priorite === "Urgente" ? C.red + "20" : r.priorite === "Prioritaire" ? C.amber + "20" : C.green + "20",
                      color: r.priorite === "Urgente" ? C.red : r.priorite === "Prioritaire" ? C.amber : C.green,
                      whiteSpace: "nowrap", marginTop: "1px"
                    }}>{r.priorite}</span>
                    <span style={{ fontSize: "10px", color: C.text, lineHeight: 1.5 }}>{r.action}</span>
                  </div>
                ))}
              </div>
            )}

            {!results && (
              <div style={{ marginTop: "14px", padding: "20px", background: "#f8fafc", borderRadius: "10px", textAlign: "center" }}>
                <div style={{ fontSize: "32px", marginBottom: "8px" }}>📊</div>
                <div style={{ fontSize: "11px", color: C.muted, lineHeight: 1.6 }}>Remplissez les 5 étapes puis cliquez sur <strong style={{ color: C.blue }}>Valider et Calculer</strong></div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
