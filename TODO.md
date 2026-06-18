# 🚀 Roadmaps & TODOs

Ce document centralise les tâches et la vision stratégique pour l'évolution de **bg-remover-cli** vers une solution autonome et accessible au plus grand nombre.

---

## 🎯 Objectif : Application Autonome & Portable
Transformer l'outil CLI actuel en une application "Zero-Install" (portable) dotée d'une interface graphique, permettant une utilisation simple sans connaissances techniques (Python, Terminal, etc.).

### 🏗️ Architecture & Confinement
- [ ] **Détection de l'environnement** : Implémenter la logique `sys.frozen` pour identifier si l'app tourne en mode script ou compilé.
- [ ] **Isolation des ressources** : Créer un dossier `models_cache` au sein du répertoire de l'application pour stocker les poids BiRefNet.
- [ ] **Gestion des variables d'environnement** : Forcer `HF_HOME` et les caches de modèles vers le dossier local de l'app pour éviter de polluer le système de l'utilisateur.

### 🎨 Interface Graphique (GUI)
- [ ] **Intégration Gradio** : Développer une interface simple avec `gr.Blocks`.
    - [ ] Sélecteur de fichier (FilePicker).
    - [ ] Prévisualisation Avant/Après.
    - [ ] Choix du mode de qualité (Standard/High/Pro).
- [ ] **Système de Diagnostic** : Afficher une barre de progression claire lors du premier téléchargement des modèles (plusieurs Go).

### 📦 Packaging & Distribution (PyInstaller)
- [ ] **Configuration PyInstaller** : Créer un fichier `.spec` optimisé pour `--onedir`.
- [ ] **Stratégie Multi-OS** :
    - [ ] **Windows** : Sortie `.zip` avec exécutable `.exe`.
    - [ ] **macOS** : Bundle `.app` (signature/notarisation à prévoir).
    - [ ] **Linux** : Archive `.tar.gz` (préservation des permissions d'exécution).
- [ ] **CI/CD Automation** : (Optionnel) Configurer GitHub Actions pour générer les releases automatiquement.

### 🐧 Spécificités Linux
- [ ] **Script de lancement** : S'assurer que les permissions `+x` sont gérées ou documentées.
- [ ] **Format Tarball** : Utiliser `tar -czf` pour la compression afin de garantir l'intégrité des métadonnées système.

---

## 📝 Guide de Mise en Œuvre (Mémo Technique)

### Logique de confinement du stockage
```python
import os
import sys

# Détection du dossier racine de l'app
if getattr(sys, 'frozen', False):
    APP_ROOT = os.path.dirname(sys.executable)
else:
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))

# Confinement des modèles
MODELS_DIR = os.path.join(APP_ROOT, "internal_models")
os.environ["HF_HOME"] = MODELS_DIR
```

### Flow Utilisateur Cible
1. **Téléchargement** : L'utilisateur récupère l'archive de ~50 Mo (code + runtime).
2. **Premier Lancement** : Téléchargement automatique des ~2-3 Go de modèles BiRefNet directement dans le dossier de l'app.
3. **Usage** : Drag & drop d'image -> Résultat transparent.
4. **Suppression** : Un simple "Glisser vers la corbeille" du dossier supprime 100% des données (app + modèles).

---

## ✅ Tâches Immédiates
- [ ] Créer un prototype `bgremove/gui.py`.
- [ ] Tester le téléchargement conditionnel des modèles dans un dossier arbitraire.
- [ ] Valider une première compilation `pyinstaller` sur Linux.
