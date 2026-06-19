# 🚀 Roadmaps & TODOs

Ce document centralise les tâches et la vision stratégique pour l'évolution de **bg-remover-cli** vers une solution autonome et accessible au plus grand nombre.

---

## 🎯 Objectif : Application Autonome & Portable
Transformer l'outil CLI actuel en une application "Zero-Install" (portable) dotée d'une interface graphique, permettant une utilisation simple sans connaissances techniques (Python, Terminal, etc.).

### 🏗️ Architecture & Confinement
- [x] **Détection de l'environnement** : Implémenter la logique `sys.frozen` pour identifier si l'app tourne en mode script ou compilé.
- [x] **Isolation des ressources** : Créer un dossier `internal_models` au sein du répertoire de l'application.
- [x] **Gestion des variables d'environnement** : Forcer `HF_HOME`, `TORCH_HOME` vers le dossier local de l'app.
- [x] **Analyse Intelligente** : Détection automatique de la complexité (cheveux/poils) et du contraste.
- [x] **Raffinement Matting** : Intégration du Guided Filter pour les détails fins.

### 🎨 Interface Graphique (GUI)
- [x] **Intégration Gradio** : Développer une interface simple avec `gr.Blocks`.
    - [x] Sélecteur de fichier.
    - [x] Prévisualisation du résultat.
    - [x] Choix du mode de qualité.
    - [x] Gestion des ombres portées et des fonds personnalisés.
- [ ] **Système de Diagnostic** : Améliorer le feedback lors du premier téléchargement des modèles (plusieurs Go).

### 📦 Packaging & Distribution (PyInstaller)
- [ ] **Configuration PyInstaller** : Créer un fichier `.spec` optimisé pour `--onedir`.
- [ ] **Inclusion des dépendances non-Python** : S'assurer que `cv2` et `torch` sont bien packagés.
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

## ✅ Tâches Complétées
- [x] Créer un prototype `bgremove/gui.py` fonctionnel.
- [x] Implémenter la logique de confinement dans `bgremove/utils/config.py`.
- [x] Ajouter le support Batch et les options d'ombres dans le CLI.
- [x] Automatiser la configuration du `build-system` dans `pyproject.toml`.

## 🛠️ Prochaines Étapes Prioritaires
- [ ] Créer le fichier `bgremove.spec` pour PyInstaller.
- [ ] Tester le lancement de l'exécutable sur une machine vierge (sans Python).
- [ ] Ajouter un modèle de fallback (ex: IS-Net) pour les cas de faible contraste.
- [ ] Intégrer un système de log plus robuste pour le débug utilisateur.
