# Conteur Numérique du Burkina 📚

Ce projet est une application interactive qui utilise l'intelligence artificielle pour générer des contes burkinabè uniques et captivants, inspirés du riche patrimoine culturel du Burkina Faso. L'application combine des technologies modernes comme **Streamlit**, **Mistral AI**, et **Retrieval-Augmented Generation (RAG)** pour offrir une expérience utilisateur immersive.

---

## Fonctionnalités principales 🌟

- **Génération d'histoires culturelles** : Créez des contes basés sur des titres fournis par l'utilisateur.
- **Base de connaissances** : Recherche dans une base de données de contes traditionnels pour enrichir les histoires générées.
- **Personnalisation** : Intégration de proverbes locaux, noms de lieux réels et éléments culturels.
- **Téléchargement facile** : Téléchargez les histoires générées au format texte.

---

## Installation et configuration ⚙️

### Prérequis

- Python 3.8 ou supérieur
- `pip` pour la gestion des dépendances

### Étapes d'installation

1. Clonez ce dépôt :
   ```bash
   git clone https://github.com/votre-utilisateur/burkina_stories.git
   cd burkina_stories

2. Installez les dépendances :
    ```bash
    pip install -r requirements.txt

3. Configurez les variables d'environnement :

    Créez un fichier .env à la racine du projet.
    Ajoutez votre clé API Mistral :

     ```bash
    MISTRAL_API_KEY=your_api_key_here

4. Assurez-vous que le répertoire chromadb_storage/ est accessible pour le stockage persistant.


Lancement de l'application 🚀
Exécutez la commande suivante pour démarrer l'application Streamlit :
    streamlit run app.py


L'application sera accessible à l'adresse : http://localhost:8501



## Utilisation 🖋️
1. Fournissez un titre pour votre histoire dans le formulaire.
2. Cliquez sur le bouton Générer.
3. L'application recherchera des références culturelles dans la base de données et générera une histoire.
 4. Téléchargez l'histoire générée si vous le souhaitez.


Technologies utilisées 🛠️
    Streamlit : Framework pour créer des applications web interactives.
    Mistral AI : Modèle linguistique pour la génération de texte.
    ChromaDB : Base de données vectorielle pour la recherche augmentée.
    Python : Langage principal du projet.


## À propos de CITADEL 🌍
    Ce projet a été développé par CITADEL dans le but de préserver et promouvoir le patrimoine culturel burkinabè à travers la technologie.

## "Préservons notre patrimoine culturel par la technologie."