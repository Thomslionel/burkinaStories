# Patch sqlite3 before any other import
import sys
import importlib
import re

import pysqlite3

sys.modules["sqlite3"] = pysqlite3
sys.modules["sqlite3.dbapi2"] = pysqlite3.dbapi2

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Re-import sqlite3 just in case
importlib.import_module("sqlite3")




import streamlit as st
# import os
import html
# from dotenv import load_dotenv
import chromadb
from chromadb.utils import embedding_functions
from mistralai import Mistral

# Configuration de la page
st.set_page_config(
    page_title="Contes Burkinabè - CITADEL",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Chargement des variables d'environnement
# load_dotenv()
MISTRAL_API_KEY = st.secrets["MISTRAL_API_KEY"]




# Initialisation des modèles et bases
@st.cache_resource
def load_resources():
    # embed_model = embedding_functions.SentenceTransformerEmbeddingFunction(
    #     model_name="all-MiniLM-L6-v2"
    # )
    chroma_client = chromadb.PersistentClient(path="chromadb_storage")
    collection = chroma_client.get_collection(
        name="stories", 
        # embedding_function=embed_model
    )
    client = Mistral(api_key=MISTRAL_API_KEY)
    return collection, client

collection, client = load_resources()


# Fonction de sauvegarde dans Google Sheets
def save_to_google_sheets(titre, histoire):
    

    titre = re.sub(r"[#*]", "", titre).strip()
    histoire = re.sub(r"[#*]", "", histoire).strip()

    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["GOOGLE_CREDANTIALS"], scope)

    client = gspread.authorize(creds)

    try:
        sheet = client.open("Recueil de Contes").sheet1
    except gspread.exceptions.SpreadsheetNotFound:
        sheet = client.create("Recueil de Contes").sheet1

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    sheet.append_row([titre, histoire, now])

# Style personnalisé
st.markdown("""
    <style>
    .main-title {
        color: #2c5f2d;
        font-size: 2.8em;
        text-align: center;
        font-family: 'Georgia', serif;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        margin-bottom: 0.5em;
    }
    .story-container {
        background: #f8f5f0;
        border-radius: 15px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border-left: 4px solid #2c5f2d;
    }
    .input-box {
        background: #fff;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .footer {
        text-align: center;
        padding: 1.5rem;
        color: #666;
        margin-top: 2rem;
    }
    .logo-img {
        max-width: 120px;
        margin: 1rem auto;
    }
    .vertical-spacer {
        height: 27px;
        visibility: hidden;
    }
    </style>
""", unsafe_allow_html=True)

# Entête
st.markdown("<h1 class='main-title'>📜 Conteur Numérique du Burkina</h1>", unsafe_allow_html=True)

# Section principale
with st.container():
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <p style='font-size: 1.1em; color: #555;'>
            "La sagesse ancestrale rencontre l'intelligence artificielle"<br>
            Créez des histoires uniques inspirées de notre riche patrimoine culturel
        </p>
    </div>
    """, unsafe_allow_html=True)

# Formulaire de génération
with st.form(key="generation_form"):
    with st.container():
        col1, col2 = st.columns([3, 1])
        with col1:
            titre = st.text_input(
                "✍️ Donnez un titre à votre histoire",
                placeholder="Ex: Le lièvre rusé et le baobab magique",
                help="Soyez créatif ! Plus le titre est descriptif, mieux c'est"
            )
        with col2:
            st.markdown('<div class="vertical-spacer"></div>', unsafe_allow_html=True)
            submit_button = st.form_submit_button("🌟 Générer", use_container_width=True)

# Logique de génération
if submit_button:
    if not titre.strip():
        st.error("❌ Veuillez saisir un titre avant de générer")
    else:
        with st.spinner("🔎 Exploration des archives traditionnelles..."):
            results = collection.query(query_texts=titre, n_results=2)
            relevant_chunks = [doc for sublist in results["documents"] for doc in sublist]

        if not relevant_chunks:
            st.warning("Aucune référence culturelle trouvée pour ce thème")
            st.stop()

        with st.spinner("🖋️ Le griot numérique écrit votre histoire..."):
            try:
                response = client.chat.complete(
                    model="mistral-large-latest",
                    messages=[{
                        "role": "system",
                        "content": f"""Créez un conte burkinabè court et captivant. Style: humoristique, rythmé avec morale finale.
                            Titre: {titre}
                            Contexte: {relevant_chunks}
                            Inclure: Proverbes locaux, noms de lieux réels, éléments culturels"""
                    }]
                )
                histoire = response.choices[0].message.content

                st.write("Response type:", type(histoire))
                st.write("Response content:", histoire)

                

                # 📝 Sauvegarde automatique dans Google Sheets
                save_to_google_sheets(titre, histoire)
                
                # Conversion et sécurisation du contenu
                histoire_safe = html.escape(histoire)
                histoire_html = histoire_safe.replace("\n", "<br>")
                
                # Affichage stylisé
                with st.container():
                    st.markdown(f"""
    <style>
        .story-container {{
            background-color: #ffffff !important;
            color: #000000 !important;
            padding: 1rem;
            border-radius: 0.5rem;
            box-shadow: 0 0 10px rgba(0,0,0,0.05);
        }}
        .story-container h3 {{
            color: #2c5f2d !important;
        }}
    </style>

    <div class="story-container">
        <h3>{titre}</h3>
        <div style='line-height: 1.6; font-size: 1.1em;'>
            {histoire_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

                    
                    # Actions utilisateur
                    col1, col2, col3 = st.columns([2, 3, 2])
                    with col2:
                        st.download_button(
                            label="📥 Télécharger l'histoire",
                            data=histoire,
                            file_name=f"Conte_{titre.replace(' ', '_')}.txt",
                            mime="text/plain",
                            use_container_width=True
                        )

            except Exception as e:
                st.error(f"Erreur de génération : {str(e)}")

# Section d'information
with st.expander("ℹ️ À propos de cette application"):
    st.markdown("""
    **Fonctionnalités clés :**
    - Génération d'histoires culturellement ancrées
    - Base de connaissances de contes traditionnels
    - Technologie RAG (Retrieval-Augmented Generation)
    - Modèle linguistique Mistral AI

    **Conseils d'utilisation :**
    1. Utilisez des titres évocateurs
    2. Incorporez des éléments locaux dans vos suggestions
    3. Personnalisez les résultats avec des détails spécifiques
    """)

# Pied de page
st.markdown("""
<div class="footer">
    <div>
        <img src="https://i0.wp.com/citadel.bf/wp-content/uploads/2021/09/cropped-logo-citadel-250x250-1.png?fit=3472%2C826&ssl=1" 
             class="logo-img" 
             alt="CITADEL">
    </div>
    <div style='margin-top: 1rem;'>
        Projet développé par <strong>CITADEL</strong><br>
        <em>Préservons notre patrimoine culturel par la technologie</em>
    </div>
</div>
""", unsafe_allow_html=True)