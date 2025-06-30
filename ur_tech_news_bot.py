# ur_tech_news_bot.py

import os
import sys
import requests
import json
import random
import tweepy
from datetime import datetime, timedelta
import re # Ajouté pour les expressions régulières

# --- 1. Variables d'environnement (NE PAS METTRE LES CLÉS ICI DIRECTEMENT) ---
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Vérification des clés
if not all([MISTRAL_API_KEY, TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET, NEWS_API_KEY]):
    print("❌ ERREUR : Toutes les clés d'API nécessaires ne sont pas définies en tant que variables d'environnement.")
    sys.exit(1)

# --- 2. Configuration des APIs ---
MISTRAL_API_BASE_URL = "https://api.mistral.ai/v1/chat/completions"
MISTRAL_MODEL_NAME = "mistral-tiny" # ou "mistral-small", "mistral-medium" pour plus de qualité/coût

NEWS_API_BASE_URL = "https://newsapi.org/v2/top-headlines"

# --- 3. Fonctions du Bot ---

def get_tech_news():
    """
    Récupère une actualité tech récente et pertinente depuis NewsAPI.org.
    """
    print("🔎 Récupération d'une actualité tech...")
    from_date = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')
    params = {
        'qInTitle': 'tech OR technology OR AI OR artificial intelligence OR startup OR innovation OR software OR hardware OR cybersecurity OR gadgets', # Mots-clés plus précis
        'language': 'en',
        'sortBy': 'relevancy',
        'apiKey': NEWS_API_KEY,
        'pageSize': 20,
        'from': from_date,
        'category': 'technology' # Filtrage par catégorie "technology"
        # 'excludeDomains': 'espn.com, cnn.com, bbc.com, sportsillustrated.com' # Exemple : décommentez et ajoutez si besoin
    }
    
    try:
        response = requests.get(NEWS_API_BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data['status'] == 'ok' and data['articles']:
            relevant_articles = [
                a for a in data['articles']
                if a['title'] and a['description'] and not (a['title'].lower() == '[removed]' or a['description'].lower() == '[removed]')
            ]
            
            if relevant_articles:
                selected_article = random.choice(relevant_articles)
                print(f"✅ Actualité trouvée : {selected_article['title']}")
                return {
                    'title': selected_article['title'],
                    'description': selected_article['description'],
                    'url': selected_article['url']
                }
            else:
                print("⚠️ Aucune actualité pertinente trouvée avec des titres/descriptions valides.")
                return None
        else:
            print(f"⚠️ NewsAPI : Aucun article trouvé. Statut: {data['status']}, TotalResults: {data.get('totalResults', 0)}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ ERREUR réseau lors de la récupération des actualités : {e}")
        return None
    except Exception as e:
        print(f"❌ ERREUR inattendue lors de la récupération des actualités : {e}")
        return None

def generate_tweet_with_mistral(news_item):
    """
    Utilise Mistral AI pour générer un tweet concis et engageant basé sur une actualité.
    """
    print("🧠 Demande à Mistral AI de générer un tweet...")
    prompt = (
        f"You are a Twitter bot named 'UrTechNews'. Your goal is to tweet concise, engaging, "
        f"and informative updates about the latest tech news. "
        f"Based on the following news article, write a tweet (max 270 characters including hashtags and link). "
        f"The tweet MUST include 2-4 **highly relevant tech hashtags** (e.g., #TechNews, #AI, #Innovation, #Software, #Hardware, #Cybersecurity, #Gadgets, #FutureTech, #DeepTech). "
        f"It MUST end with the article's URL and NOT include 'Read more' or similar phrases before the link, nor any placeholder like '[Link]'. "
        f"Focus on the most interesting aspect of the news. Do NOT use bullet points or lists. Ensure the tweet sounds professional and engaging.\n\n"
        f"Article Title: {news_item['title']}\n"
        f"Article Description: {news_item['description']}\n"
        f"Article URL: {news_item['url']}\n\n"
        f"Your Tweet:"
    )

    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MISTRAL_MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 150 # Limite les tokens de l'IA pour rester concis
    }

    try:
        response = requests.post(MISTRAL_API_BASE_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        
        if 'choices' in data and data['choices']:
            tweet_content = data['choices'][0]['message']['content'].strip()

            # --- Nouvelle logique de nettoyage et d'ajout du lien ---
            # Nettoyer toute mention de "Link", "[Link]", "Read more", etc.
            tweet_content = tweet_content.replace('[Link]', '').replace('Link', '').replace('Read more', '').strip()
            # Supprimer toute URL partielle que l'IA aurait pu commencer à générer
            tweet_content = re.sub(r'https?:\/\/\S*$', '', tweet_content).strip()
            tweet_content = re.sub(r'\[.*?\]', '', tweet_content).strip() # Enlève tout ce qui est entre crochets

            # Calculer la longueur maximale disponible pour le texte du tweet
            # Un lien Twitter est "shortened" à 23 caractères quel que soit sa longueur réelle
            remaining_chars_for_text = 280 - 23 - 1 # 280 total - 23 pour le lien - 1 pour l'espace avant le lien

            # Tronquer le tweet si nécessaire AVANT d'ajouter le lien
            if len(tweet_content) > remaining_chars_for_text:
                tweet_content = tweet_content[:remaining_chars_for_text - 3] + "..." # Tronquer et ajouter "..."

            # Ajouter le lien final
            final_tweet = f"{tweet_content} {news_item['url']}"

            print(f"✅ Tweet généré : {final_tweet}")
            return final_tweet
        else:
            print(f"❌ Mistral AI : Aucune réponse valide. Réponse complète: {data}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ ERREUR réseau lors de la génération du tweet par Mistral AI : {e}")
        return None
    except Exception as e:
        print(f"❌ ERREUR inattendue lors de la génération du tweet : {e}")
        return None

def tweet_status(tweet_text):
    """
    Publie le tweet sur Twitter via l'API Tweepy (v2 Client).
    """
    print(f"🚀 Publication du tweet : {tweet_text}")
    try:
        client = tweepy.Client(
            consumer_key=TWITTER_API_KEY,
            consumer_secret=TWITTER_API_SECRET,
            access_token=TWITTER_ACCESS_TOKEN,
            access_token_secret=TWITTER_ACCESS_TOKEN_SECRET
        )

        response = client.create_tweet(text=tweet_text)
        
        print(f"✅ Tweet publié avec succès ! ID du tweet : {response.data['id']}")
        return True
    except tweepy.TweepyException as e:
        print(f"❌ ERREUR Tweepy lors de la publication du tweet : {e}")
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_json = e.response.json()
                print(f"Détails de l'erreur Twitter : {json.dumps(error_json, indent=2)}")
            except json.JSONDecodeError:
                print(f"Réponse d'erreur non-JSON : {e.response.text}")
        return False
    except Exception as e:
        print(f"❌ ERREUR inattendue lors de la publication du tweet : {e}")
        return False

# --- 4. Fonction Principale ---
def main():
    print("🤖 Démarrage du bot Twitter UrTechNews...")
    news_item = get_tech_news()

    if news_item:
        tweet_content = generate_tweet_with_mistral(news_item)
        if tweet_content:
            if tweet_status(tweet_content):
                print("🎉 Processus complet réussi !")
            else:
                print("⚠️ Le tweet n'a pas pu être publié.")
        else:
            print("⚠️ La génération du tweet a échoué.")
    else:
        print("⚠️ Aucune actualité à tweeter pour le moment.")
    
    print("🤖 Bot UrTechNews terminé.")

if __name__ == "__main__":
    main()