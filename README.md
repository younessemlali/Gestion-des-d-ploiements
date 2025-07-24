# 🚀 Système de Gestion des Déploiements

Application Streamlit moderne pour la gestion automatisée des déploiements de plateformes client.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28.2-FF4B4B.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 📋 Fonctionnalités

- ✅ Interface moderne et intuitive
- ✅ Support de 8 plateformes différentes (Temporaris, Baps, Pilott, Pixid, PeoPulse, Fieldglass, Beeline, Instant)
- ✅ Génération automatique d'emails de déploiement
- ✅ Création de PDF de procédures personnalisées
- ✅ Historique des déploiements
- ✅ Tableau de bord avec statistiques
- ✅ Export direct des documents

## 🛠️ Installation

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. **Cloner le repository**
```bash
git clone https://github.com/votre-username/deployment-management.git
cd deployment-management
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

## 🚀 Lancement de l'application

### En local
```bash
streamlit run app.py
```

L'application sera accessible à l'adresse : `http://localhost:8501`

### Sur Streamlit Cloud

1. Connectez-vous à [Streamlit Cloud](https://share.streamlit.io/)
2. Déployez depuis votre repository GitHub
3. L'application sera accessible via une URL publique

## 📝 Utilisation

### 1. Sélection de la plateforme
- Choisissez parmi les 8 plateformes disponibles
- Les modules disponibles s'adaptent automatiquement

### 2. Configuration du déploiement
- Sélectionnez les modules souhaités
- Renseignez le nom du client
- Entrez le numéro SIRET

### 3. Génération des documents
- **Email** : Cliquez sur "Générer Email" pour créer le template
- **PDF** : Cliquez sur "Générer PDF" pour la procédure complète

### 4. Export et utilisation
- Copiez l'email directement depuis l'interface
- Téléchargez le PDF généré
- Consultez l'historique des déploiements

## 🏗️ Architecture

```
deployment-management/
│
├── app.py                 # Application principale Streamlit
├── requirements.txt       # Dépendances Python
├── README.md             # Documentation
├── .gitignore            # Fichiers à ignorer
├── config/               # Configurations
│   └── platforms.json    # Configuration des plateformes
└── utils/                # Utilitaires
    ├── email_generator.py
    └── pdf_generator.py
```

## 🔧 Configuration avancée

### Ajouter une nouvelle plateforme

Modifiez le dictionnaire `PLATFORMS` dans `app.py` :

```python
PLATFORMS = {
    "NouvellePlateforme": {
        "color": "#HexColor",
        "modules": ["Module1", "Module2", ...]
    }
}
```

### Personnaliser les templates

Les templates d'email et PDF peuvent être modifiés dans les fonctions :
- `generate_email()` pour les emails
- `generate_pdf()` pour les documents PDF

## 🔗 Intégration avec Google Apps Script

Cette application est conçue pour s'intégrer avec Google Apps Script via webhook :

```python
# Endpoint pour recevoir des données de GAS
@app.route('/webhook', methods=['POST'])
def handle_webhook():
    data = request.json
    # Traiter les données
    return jsonify({"status": "success"})
```

## 📊 Tableau de bord

L'application inclut un tableau de bord avec :
- Nombre total de déploiements
- Déploiements en cours
- Répartition par plateforme (graphique)
- Historique complet

## 🔒 Sécurité

- Validation des entrées utilisateur
- Token secret pour les webhooks
- Pas de stockage de données sensibles

## 🤝 Contribution

Les contributions sont bienvenues ! Pour contribuer :

1. Fork le projet
2. Créez votre branche (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 📞 Support

Pour toute question ou problème :
- Email : support@randstad.fr
- Documentation : [Wiki du projet](https://github.com/votre-username/deployment-management/wiki)

## 📄 License

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

---

Développé avec ❤️ par l'équipe IT Randstad
