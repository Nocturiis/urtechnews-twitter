# 🤖 UrTechNews Twitter Bot

Bienvenue dans le dépôt du bot Twitter automatisé **UrTechNews** \! Ce projet vise à maintenir les passionnés de technologie informés en publiant automatiquement des tweets quotidiens sur les dernières actualités et innovations du monde de la tech.

Le bot fonctionne grâce à une combinaison d'APIs :

  * **NewsAPI.org** pour la récupération des actualités.
  * **Mistral AI** pour la génération intelligente et concise des tweets.
  * **API Twitter (X API)** pour la publication des messages.

Le tout est orchestré et automatisé via **GitHub Actions**, assurant une diffusion régulière sans intervention manuelle.

-----

## ✨ Fonctionnalités

  * **📰 Récupération d'actualités Tech :** Recherche et sélection d'articles pertinents et récents dans le domaine de la technologie via NewsAPI.org.
  * **🧠 Génération de Tweets Intelligente :** Utilisation de Mistral AI pour transformer les résumés d'articles en tweets engageants, formatés pour Twitter, avec des hashtags pertinents.
  * **🐦 Publication Automatisée :** Publication directe des tweets sur le compte @UrTechNews via l'API Twitter.
  * **⏰ Ordonnancement Quotidien :** Exécution programmée plusieurs fois par jour grâce à GitHub Actions.
  * **🔒 Sécurité des Clés :** Toutes les clés d'API sont stockées en toute sécurité via les Secrets GitHub.

-----

## 🚀 Comment ça marche ?

Le workflow est le suivant :

1.  **Déclenchement :** GitHub Actions lance le script Python selon un **calendrier prédéfini** (par exemple, 3 fois par jour) ou manuellement.
2.  **Collecte d'actualités :** Le script interroge NewsAPI.org pour obtenir les derniers articles technologiques. Un filtrage strict est appliqué pour garantir la pertinence.
3.  **Rédaction du tweet :** Le titre, la description et l'URL de l'article sélectionné sont envoyés à Mistral AI. L'IA génère un tweet court et percutant, incluant des hashtags et le lien de l'article.
4.  **Publication :** Le tweet généré est envoyé à l'API Twitter (X API v2) pour être publié sur le compte @UrTechNews.
5.  **Fin d'exécution :** La tâche GitHub Actions se termine, en attendant la prochaine exécution programmée.

-----

## 🛠️ Configuration et Installation

Pour faire fonctionner ce bot, vous devrez obtenir plusieurs clés d'API et les configurer correctement.

### 1\. Clés d'API requises

  * **API Twitter (X API) :**
      * Créez un compte développeur sur [developer.twitter.com](https://developer.twitter.com/en/portal/dashboard).
      * Créez une nouvelle application avec des **permissions d'écriture (Read and Write)**.
      * Notez vos : `API Key`, `API Key Secret`, `Access Token`, `Access Token Secret`.
  * **Mistral AI API :**
      * Inscrivez-vous sur [console.mistral.ai](https://console.mistral.ai/).
      * Générez une `API Key`.
  * **NewsAPI.org API :**
      * Inscrivez-vous sur [newsapi.org](https://newsapi.org/).
      * Obtenez votre `API Key`.

### 2\. Configuration des Secrets GitHub

Pour des raisons de sécurité, **ne jamais inclure vos clés API directement dans le code**. Utilisez les Secrets GitHub.

1.  Sur votre dépôt GitHub, allez dans **`Settings`** (Paramètres).
2.  Dans le menu latéral, cliquez sur **`Security`** (Sécurité) \> **`Secrets and variables`** (Secrets et variables) \> **`Actions`**.
3.  Cliquez sur **`New repository secret`** (Nouveau secret de dépôt) pour ajouter chacun des secrets suivants avec leurs valeurs respectives :
      * `MISTRAL_API_KEY`
      * `TWITTER_API_KEY`
      * `TWITTER_API_SECRET`
      * `TWITTER_ACCESS_TOKEN`
      * `TWITTER_ACCESS_TOKEN_SECRET`
      * `NEWS_API_KEY`

### 3\. Fichiers du Dépôt

Assurez-vous que votre dépôt contient les fichiers suivants :

```
UrTechNews-Twitter-Bot/
├── .github/
│   └── workflows/
│       └── tweet.yml  # Configuration du workflow GitHub Actions
├── ur_tech_news_bot.py   # Le script Python du bot
└── README.md             # Ce fichier
```

  * **`ur_tech_news_bot.py` :** Contient le code Python principal du bot.
  * **`.github/workflows/tweet.yml` :** Configure le workflow GitHub Actions pour exécuter le bot.

-----

## 🏃 Lancement du Bot

1.  **Poussez vos modifications :** Une fois tous les fichiers (`ur_tech_news_bot.py`, `tweet.yml`, et ce `README.md`) ajoutés et les Secrets GitHub configurés, poussez-les vers votre dépôt GitHub.
    ```bash
    git add .
    git commit -m "Initial commit for UrTechNews Twitter Bot"
    git push origin main # ou master, selon votre branche principale
    ```
2.  **Vérifiez le workflow :**
      * Allez dans l'onglet **`Actions`** de votre dépôt GitHub.
      * Vous devriez voir le workflow "Daily Tech News Tweet".
      * Il se déclenchera automatiquement aux heures programmées (voir le fichier `tweet.yml`).
      * Vous pouvez également le déclencher manuellement en cliquant sur "Run workflow" dans le menu latéral du workflow.

Consultez les logs d'exécution du workflow pour vérifier le bon fonctionnement ou déboguer d'éventuels problèmes.

-----

## 🤝 Contribution

Les contributions sont les bienvenues \! Si vous avez des idées d'amélioration, des corrections de bugs ou de nouvelles fonctionnalités, n'hésitez pas à ouvrir une issue ou à soumettre une pull request.

-----

## 📜 Licence

Ce projet est sous licence [MIT](https://opensource.org/licenses/MIT).

-----

N'hésitez pas à me dire si vous souhaitez des ajustements ou des ajouts \!
