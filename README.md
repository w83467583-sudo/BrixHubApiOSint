# BrixHub CLI Dashboard

BrixHub CLI Dashboard est une interface utilisateur en terminal (TUI) conçue pour interagir avec l'API BrixHub, filtrer des requêtes et exporter des données.

* Permet une navigation fluide au clavier.
* Gère l'affichage dynamique et le défilement des données.
* Fonctionne sous Python 3.

## Installation

### With PyPI
```bash
pip install windows-curses requests
With GitHub
Bash
git clone https://github.com/w83467583-sudo/BrixHubApiOSint.git
cd BrixHubApiOSint
python main.py
Quick Start

attender 10 15 sec avant la première recherche pour éviter le rate limites
Pour changer l api il faut aller dans le dossier tmp_api puis api.json pour la changer (en cas d erreur 401 récurente)

L'application sépare les filtres de recherche et l'affichage des profils trouvés dans deux colonnes distinctes.

Navigation Controles
[FLECHE HAUT / BAS] : Déplacer la sélection dans les menus

[FLECHE DROITE] : Basculer vers le panneau des résultats

[FLECHE GAUCHE] : Revenir au panneau des filtres

[ENTREE] : Modifier un champ ou exporter un profil

CLI Example
Bash
python test.py
Menu Principal (Panneau Gauche)
Plaintext
┌──────────────────────────────────────┐
│ * 1. IDENTITÉ                        │ --> Appuyez sur [ENTRÉE] pour éditer
│ * 2. NAISSANCE                       │
│ * 3. CONTACT                         │
│ * 4. LOCALISATION                    │
│ * 5. FIVEM / GTA RP                  │
│ * 6. CHAMPS AVANCÉS                  │
├──────────────────────────────────────┤
│ [ >>> EXECUTER LA RECHERCHE <<< ]    │ --> Envoie la requête à l'API
├──────────────────────────────────────┤
│ [ CLEAN ]                [ Quitter ] │ --> clean supprime les donners rempli 
└──────────────────────────────────────┘
Module Output
Les données reçues sont nettoyées, puis triées par catégories dans le panneau de droite.

Panneau Droite (Résultats)
Plaintext
┌────────────────────────────────────────────────────────┐
│ PROFIL #1 ── Fiabilité : 95%                           │
├────────────────────────────────────────────────────────┤
│ [ IDENTITE & ETAT CIVIL ]                              │
│     * PRENOM             : John                        │
│     * NOM_FAMILLE        : Doe                         │
│                                                        │
│ [ COORDONNEES DE CONTACT ]                             │
│     * EMAIL              : john.doe@email.com          │
│     * ADRESSE_IP         : 127.0.0.1                   │
│                                                        │
│ [ EMPREINTE GAMING & RP ]                              │
│     * DISCORD_ID         : 123456789012345678          │
│     * FIVEM_ID           : fivem:123456                │
└────────────────────────────────────────────────────────┘
pour éviter les erreurs de requètes potentionnels éviter de spammers

┌──────────────────────────────────────────────────────────────────────────────────┐
│ STATUS CODE | ERROR TYPE       | VISUAL DESCRIPTION                              │
├──────────────────────────────────────────────────────────────────────────────────┤
│ * 400       | bad_request      | Err 400 (Parametres invalides)                  │
│ * 401       | unauthorized     | Err 401 (Cle manquante / invalide)              │
│ * 401       | expired          | Err 401 (Cle expiree)                           │
│ * 403       | plan_limited     | Err 403 (Fonctionnalite non disponible)         │
│ * 429       | quota_exceeded   | Err 429 (Quota journalier depasse)              │
│ * 429       | rate_limited     | Err 429 (Trop de requetes par minute)           │
│ * 500       | internal         | Err 500 (Erreur serveur)                        │
│ * 503       | service_not_avail| Err 503 (Base inaccessible)                     │
└──────────────────────────────────────────────────────────────────────────────────┘
