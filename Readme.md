# NetAssas : Architecture IDS/IPS Hybride par Machine Learning

![Python](https://img.shields.io/badge/Python-3.14-blue.svg)
![PyQt6](https://img.shields.io/badge/UI-PyQt6-green.svg)
![XGBoost](https://img.shields.io/badge/Model-XGBoost-orange.svg)
![Scikit-Learn](https://img.shields.io/badge/Model-Isolation%20Forest-yellow.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)

**NetAssas** est un Système de Détection et de Prévention d'Intrusions (IDS/IPS) autonome et en temps réel, conçu spécifiquement pour les environnements Windows. Face à l'inefficacité des pare-feux statiques traditionnels, cette application utilise une architecture d'Intelligence Artificielle "Double Filtre" pour analyser le trafic réseau, détecter les anomalies et bloquer activement les attaquants.

Projet de fin d'année réalisé au sein de la filière **Informatique Appliquée - Science des Données** à la **Faculté des Sciences d'El Jadida (Université Chouaïb Doukkali)**.

---

## Fonctionnalités Principales

* **Moteur IA Hybride (En Cascade) :**
  * **Filtre Supervisé (XGBoost) :** Détection ultra-rapide des signatures d'attaques connues (DDoS, Injections, Brute Force).
  * **Filtre Non-Supervisé (Isolation Forest) :** Analyse comportementale entraînée uniquement sur le trafic sain pour intercepter les attaques *Zero-Day* et les anomalies mathématiques.
* **Prévention Active (IPS) :** Interfaçage automatisé avec le pare-feu Windows (`netsh`) pour bannir instantanément les adresses IP compromises en quelques millisecondes.
* **Dashboard Interactif :** Interface graphique développée sous **PyQt6** pour une supervision dynamique des flux IP, des protocoles et des alertes de sécurité.
* **Auto-Protection :** Détection dynamique de l'adresse IP locale et mise sur liste blanche automatique pour éviter l'auto-blocage du système.
* **Optimisation Mémoire :** Purge automatique de la RAM graphique et de l'historique de l'IA tous les 500 paquets sains pour garantir une stabilité lors d'une exécution continue.

---

##  Installation & Utilisation

L'application a été empaquetée pour fonctionner de manière totalement autonome sur Windows, sans nécessiter l'installation de Python.
la version linux sera disponible au futur inshallah.

### 1. Prérequis Obligatoire
Pour que la capture de paquets réseau fonctionne sous Windows, vous **devez** avoir installé un pilote de capture réseau comme **Npcap** (généralement inclus avec Wireshark).
* [Télécharger Npcap](https://npcap.com/#download)

### 2. Lancement
1. Allez dans l'onglet **Releases** de ce dépôt GitHub.
2. Téléchargez l'archive `.zip` contenant l'exécutable.
3. Extrayez le dossier sur votre bureau.
4. Double-cliquez sur `NetAssas.exe`.
5. **Important :** Acceptez l'invite des droits d'administrateur (UAC). Ces droits sont obligatoires pour permettre au logiciel d'injecter des règles de blocage dans le pare-feu système.

---

## Pour les Développeurs

Si vous souhaitez modifier le code source ou recompiler l'application vous-même :

### 1. Préparation de l'environnement
```bash
# Cloner le dépôt
git clone https://github.com/ISAGIBD4/NetAssas.git
cd NetAssas

# Créer et activer l'environnement virtuel
python -m venv .venv
.venv\Scripts\activate

# Installer les dépendances (la liste des courses du projet)
pip install -r requirements.txt
```

### 2. Entraînement de l'IA (Optionnel)
Exécutez le script d'entraînement fourni sur une plateforme Cloud (comme Kaggle) avec les datasets de référence (CIC-IDS-2018 / UNSW-NB15) pour générer les 5 artefacts requis :
* `ids_scaler.pkl`
* `ids_encoder.pkl`
* `modele_supervise.pkl`
* `modele_non_supervise.pkl`
* `ids_features.pkl`

Placez ces 5 fichiers à la racine du projet.

### 3. Compilation avec PyInstaller
Pour regénérer l'exécutable Windows avec les droits d'administration inclus :
```bash
pip install pyinstaller
pyinstaller NetAssas.spec
```
L'exécutable final sera généré dans le répertoire `dist/NetAssas/`.

---

## Structure du Projet

```text
NetAssas/
│
├── main.py                    # Point d'entrée de l'application et GUI (PyQt6)
├── sniffer_thread.py          # Thread de capture réseau asynchrone (Scapy)
├── security_core.py           # Moteur IA hybride et logique de prévention (IPS)
│
├── *.pkl                      # Modèles Machine Learning pré-entraînés (Non inclus dans le code source)
├── NetAssas.spec              # Configuration de compilation PyInstaller
├── requirements.txt           # Liste exacte des dépendances Python nécessaires
└── README.md                  # Documentation du projet
```

---

## Auteurs & Remerciements

* **Mohammed Atir** - *Data cleaning & Machine learning*
* **Mehdi Saifie** - *Architecture Réseau & Developpement logiciel*

Nous tenons à exprimer notre profonde gratitude au **Dr. Aaroud Abdessadek** pour son encadrement, sa rigueur scientifique et ses conseils avisés tout au long de la conception de ce projet.
