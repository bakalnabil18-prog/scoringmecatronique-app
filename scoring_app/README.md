# 🏭 Underwriting Maroc — Industrie 4.0

## 🇲🇦 Système de Scoring Assurance pour le Marché Marocain

Prototype de scoring multi-piliers pour l'assurance industrielle au Maroc.

### ✨ Fonctionnalités

- ✅ 3 piliers de scoring: Robustesse, Maintenance, Gouvernance
- ✅ 6 secteurs marocains: Textile, Agroalimentaire, Mines, Chimie, Construction, Énergie
- ✅ Devise marocaine (DH) + TVA 20%
- ✅ Conformité ACPR & Code Assurances Maroc
- ✅ 3 presets régionaux (Casablanca, Agadir, Khouribga)
- ✅ Interface moderne avec Streamlit

### 🚀 Installation
```bash
pip install streamlit plotly pandas numpy
```

### ▶️ Lancement
```bash
cd C:\scoring_app
streamlit run underwriting_app.py
```

L'app s'ouvre sur: http://localhost:8501

### 📋 Fichiers Clés

- `underwriting_app.py` - Interface Streamlit marocaine
- `advanced_scoring.py` - Module de scoring
- `config_maroc.py` - Configuration marocaine
- `engine/` - Modules de calcul

### 🇲🇦 Localisation

- **Devise:** Dirham (DH)
- **Secteurs:** Textile, Agroalim, Mines, Chimie, Construction, Énergie
- **Régions:** Casablanca, Fès, Tanger, Agadir, Khouribga, Marrakech
- **Normes:** ISO, ACPR, Code Assurances Maroc

### 📊 Utilisation

1. Choisissez un secteur (sidebar)
2. Chargez un preset ou mode manuel
3. Cliquez « LANCER SCORING »
4. Consultez les résultats en DH

### 👥 Auteur

Développé pour l'Université/École d'Ingénieur - Maroc

### 📄 Licence

MIT License - Libre d'utilisation

© 2026 - Underwriting Maroc
```

#### **ÉTAPE 3: Coller dans Notepad**
```
Ctrl + V (ou clic droit → Coller)
```

#### **ÉTAPE 4: Sauvegarder**
```
Ctrl + S
Nom: README.md
Type: Tous les fichiers (*.*)
Lieu: C:\scoring_app\
Cliquez: Enregistrer
```

✅ **FICHIER 1 CRÉÉ!**

---

### **FICHIER 2: .gitignore**

**Même procédure!** Mais avec ce contenu:
```
__pycache__/
*.pyc
.streamlit/
.env
outputs/
*.log
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store
.pytest_cache/
.coverage
.cache/
```

**Sauvegarder avec le nom:** `.gitignore` (exactement)

✅ **FICHIER 2 CRÉÉ!**

---

## ✅ **VÉRIFICATION**

**Ouvrez l'Explorateur** (Windows + E)
**Allez à:** `C:\scoring_app\`

**Vous devez voir:**
```
✓ README.md          ← NOUVEAU
✓ .gitignore         ← NOUVEAU
✓ underwriting_app.py
✓ advanced_scoring.py
✓ config_maroc.py
✓ engine/