BrixHub CLI Dashboard
BrixHub CLI Dashboard est une interface utilisateur en terminal (TUI) conçue pour interagir avec l'API BrixHub, filtrer des requêtes et exporter des données.

Permet une navigation fluide au clavier.

Gère l'affichage dynamique et le défilement des données.

Fonctionne sous Python 3.

Installation
With PyPI
Bash
pip install windows-curses requests
With GitHub
Bash
git clone https://github.com/votre-profil/brixhub-dashboard.git
cd brixhub-dashboard
python test.py
Quick Start
L'application sépare les filtres de recherche et l'affichage des profils trouvés dans deux colonnes distinctes.

Navigation Controles
Plaintext
* [FLECHE HAUT / BAS]   : Déplacer la sélection dans les menus
* [FLECHE DROITE]       : Basculer vers le panneau des résultats
* [FLECHE GAUCHE]       : Revenir au panneau des filtres
* [ENTREE]              : Modifier un champ ou exporter un profil
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
│ [ CLEAN ] [ Config API ] [ Quitter ] │
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
