# Assistant Projet Rénovation – Diagramme de Gantt

Application Streamlit pour planifier un projet de rénovation. Sélectionnez l'état du projet et la date de début, modifiez les durées des phases, et visualisez un diagramme de Gantt interactif avec délais du maître d'ouvrage.

## 📌 À propos

Cet outil permet de:
- **Visualiser** le planning complet d'un projet de rénovation énergétique
- **Personnaliser** les durées de chaque phase selon vos besoins
- **Comprendre** les différentes étapes grâce à un glossaire intégré
- **Exporter** le diagramme de Gantt pour vos présentations

## 🚀 Installation

### Prérequis
- Python 3.7 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. Cloner le dépôt:
```bash
git clone https://github.com/benjaminlallemand44/Projet_renovation_Gantt.git
cd Projet_renovation_Gantt
```

2. Installer les dépendances:
```bash
pip install -r requirements.txt
```

3. Lancer l'application:
```bash
streamlit run main.py
```

L'application s'ouvrira automatiquement dans votre navigateur par défaut.

## 📊 Fonctionnalités

### États du projet disponibles
1. **Nous n'avons pas encore effectué d'audit énergétique**
   - Rédaction du programme
   - Analyse du site et audit énergétique
   - Restitution et validation

2. **Nous venons de recevoir les comptes rendus des études préalables**
   - Analyse des comptes-rendus
   - Prise de décision
   - Rédaction du programme de travaux

3. **Nous souhaitons faire intervenir un AMO Programmiste**
   - Choix de l'AMO
   - Déroulement et analyse

4. **Nous voulons lancer notre marché de recrutement de maîtrise d'oeuvre**
   - Rédaction des cahiers des charges
   - Publication et sélection

5. **Nous venons de sélectionner notre équipe de maîtrise d'oeuvre**
   - Toutes les phases MOE (Loi MOP)

### Catégories de phases
- **🏠 Études préalables**: Préparation et analyse initiale
- **🏢 AMO Programmiste**: Assistance à maîtrise d'ouvrage
- **📋 Sélection MOE**: Recrutement de la maîtrise d'œuvre
- **🏗️ MOE (Loi MOP)**: Mission de maîtrise d'œuvre complète

### Phases MOE détaillées
- **DIAG**: Diagnostic et études d'esquisse
- **APS**: Avant-Projet Sommaire
- **APD**: Avant-Projet Définitif
- **PRO**: Études de Projet
- **DCE**: Dossier de Consultation des Entreprises
- **ACT/AMT**: Assistance passation marchés
- **VISA**: Visa Études d'Exécution
- **DET**: Direction Exécution Travaux
- **AOR**: Assistance aux opérations de réception

## 🎨 Glossaire

Un glossaire complet est intégré dans l'application pour expliquer chaque phase:
- **Glossaire simplifié**: Affiché en tooltip sur les champs
- **Glossaire complet**: Disponible sous le diagramme de Gantt

## 📈 Exemple d'utilisation

1. Sélectionnez votre état actuel dans le menu déroulant
2. Choisissez une date de début pour votre projet
3. Ajustez les durées des phases si nécessaire (en semaines)
4. Cliquez sur "Générer le diagramme de Gantt"
5. Visualisez et interagissez avec le diagramme

## 🔧 Déploiement

### Sur Streamlit Community Cloud

1. Poussez votre code sur GitHub
2. Connectez-vous à [Streamlit Community Cloud](https://share.streamlit.io)
3. Cliquez sur "New app"
4. Sélectionnez votre dépôt et le fichier `main.py`
5. Déployez!

### Configuration requise
- Fichier `requirements.txt` à la racine
- Fichier `main.py` comme point d'entrée

## 📁 Structure du projet

```
Projet_renovation_Gantt/
├── main.py              # Point d'entrée de l'application
├── config.py            # Configuration et constantes
├── gantt.py             # Logique de génération du Gantt
├── ui.py                # Interface utilisateur Streamlit
├── tests/               # Tests unitaires
│   ├── __init__.py
│   ├── test_config.py   # Tests de configuration
│   ├── test_phases.py   # Tests de génération des phases
│   └── test_gantt.py    # Tests du diagramme de Gantt
├── old/                # Anciennes versions (archivées)
├── images/              # Images (logo)
├── requirements.txt     # Dépendances
├── README.md            # Documentation
└── .gitignore           # Fichiers à ignorer
```

## 🤝 Contribution

Les contributions sont les bienvenues! Pour contribuer:

1. Forkez le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/ma-fonctionnalite`)
3. Commitez vos changements (`git commit -m 'feat: ajouter ma fonctionnalité'`)
4. Poussez vers la branche (`git push origin feature/ma-fonctionnalite`)
5. Ouvrez une Pull Request

### Conventions de commit
Nous utilisons [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:` pour les nouvelles fonctionnalités
- `fix:` pour les corrections de bugs
- `docs:` pour les modifications de documentation
- `refactor:` pour les refactorisations de code
- `test:` pour l'ajout de tests

## 📝 Historique des versions

- **v1.0.0**: Version initiale avec diagramme de Gantt de base
- **v1.1.0**: Ajout des catégories et du glossaire
- **v1.2.0**: Refactorisation en modules séparés
- **v1.3.0**: Ajout des tests unitaires

## 🎓 Technologies utilisées

- **Python 3.12**
- **Streamlit 1.28.0**: Framework pour l'interface web
- **Pandas 2.0.3**: Manipulation des données
- **Plotly 5.15.0**: Visualisation interactive
- **Pytest 7.4.0**: Tests unitaires

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🆘 Support

Pour toute question ou problème, veuillez ouvrir une issue sur GitHub.

---

**Développé avec ❤️ pour les projets de rénovation énergétique**
