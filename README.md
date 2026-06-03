BrixHub CLI Dashboard
Une interface graphique en terminal (TUI) développée en Python avec la bibliothèque curses, conçue pour interagir efficacement avec l'API BrixHub. Ce tableau de bord permet de configurer des critères de recherche avancés, d'exécuter des requêtes à distance et de visualiser les profils de données récupérés de manière structurée.

Fonctionnalités
Interface TUI Bi-Colonne : Navigation fluide au clavier entre le panneau de configuration des filtres (gauche) et le panneau de visualisation des résultats (droite).

Gestion par Catégories : Structuration des données en sections dédiées : Identité, Naissance, Contact, Localisation, Empreinte Gaming/RP (FiveM, Discord, Steam) et Champs Avancés (NIR, IBAN, VIN, Immatriculation).

Affichage Thématique Épuré : Organisation automatique des réponses de l'API dans des blocs visuels alignés et hiérarchisés pour une lecture instantanée.

Système de Défilement (Scroll) : Support du défilement vertical dans le panneau des résultats pour gérer les profils volumineux sans couper l'affichage.

Export Local Automatisé : Génération de rapports textuels structurés à partir d'un profil sélectionné, sauvegardés directement dans un répertoire local.

Sécurité & Limitation : Intégration d'un mécanisme d'anti-spam (cooldown de 15 secondes entre les requêtes) et persistance locale de la clé API chiffrée en JSON.

Prérequis
Python 3.x

Dépendances réseau : requests

Système d'exploitation : Compatible nativement sous Linux/macOS via curses. Pour les utilisateurs Windows, l'installation de la version adaptée est obligatoire :

Bash
pip install windows-curses requests
Structure des Fichiers
Le script gère automatiquement son environnement lors de sa première exécution :

tmp_api/api.json : Stocke de manière persistante la clé API BrixHub après validation du jeton.

exports_dox/ : Répertoire de destination où sont générés les exports textuels des profils.

Utilisation
Lancez l'interface depuis votre terminal :

Bash
python test.py
Saisie de la clé : Au premier démarrage, l'application vous invite à saisir votre jeton API BrixHub.

Navigation : Utilisez les flèches directionnelles HAUT et BAS pour parcourir les options du menu.

Édition : Appuyez sur ENTRÉE sur une catégorie pour renseigner ou modifier vos critères de recherche.

Exécution : Sélectionnez l'option de recherche pour envoyer le payload à l'API.

Visualisation & Export : Appuyez sur la flèche DROITE pour basculer sur le panneau des résultats, naviguez sur le profil souhaité et appuyez sur ENTRÉE pour l'exporter.
