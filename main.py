import os
import sys
import json
import time
import requests
from datetime import datetime

try:
    import curses
except ImportError:
    print("Erreur : Le module 'curses' est requis. Installez-le avec : pip install windows-curses")
    sys.exit(1)

# Récupère le dossier absolu dans lequel se trouve ce script Python
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Associe les sous-dossiers au dossier du script
TMP_DIR = os.path.join(SCRIPT_DIR, "tmp_api")
EXPORT_DIR = os.path.join(SCRIPT_DIR, "exports_dox")

# Le reste ne change pas, CONFIG_FILE utilisera automatiquement le bon chemin
CONFIG_FILE = os.path.join(TMP_DIR, "api.json")
BASE_URL = "https://brixhub.net/api/v1"

ASCII_ART = """____________________._______  ______ ___  ____ -------------  --------  --------  ____  ___
\\______    \\______    \\   \\   \\/  /   |   \\|    |   \\______    \\ \\______ \\  \\-----    \\ \\   \\/  /
 |    |  _/|       _/   |\\     /    ~    \\    |   /|    |  _/  |    |  \\  /   |    \\ \\     / 
 |    |   \\|    |   \\   |/     \\    Y    /    |  / |    |   \\  |    `   \\/    |    \\/     \\ 
 |______  /|____|_  /___/___/\\  \\___|_  /|______/  |______  / /-------  /\\-------  /___/\\  \\
        \\/        \\/          \\_/     \\/                  \\/        \\/         \\/       \\_/"""

LISTE_CATEGORIES = [
    "1. IDENTITÉ",
    "2. NAISSANCE",
    "3. CONTACT",
    "4. LOCALISATION",
    "5. FIVEM / GTA RP",
    "6. CHAMPS AVANCÉS"
]

categories = {
    "1. IDENTITÉ": {
        "nom_famille": "", "prenom": "", "nom_naissance": "", "nom_affichage": "", "nom_utilisateur": "", "genre": "", "civilit": ""
    },
    "2. NAISSANCE": {
        "date_naissanc": "", "annee_naissanc": "", "jour_naissance": "", "mois_naissance": "", "ville_naissanc": "", "lieu_naissanc": ""
    },
    "3. CONTACT": {
        "email": "", "telephone": "", "mobile": "", "adresse_ip": ""
    },
    "4. LOCALISATION": {
        "adresse": "", "complement_adress": "", "code_postal": "", "ville": "", "pays": "", "region": "", "departement": ""
    },
    "5. FIVEM / GTA RP": {
        "steam_id": "", "fivem_licensestring": "", "fivem_license2string": "", "fivem_id": "", "xbox_live_id": "", "live_id": "", "discord_id": ""
    },
    "6. CHAMPS AVANCÉS": {
        "nir": "", "iban": "", "bic": "", "siret": "", "siren": "", "vin_plaque": "", "immatriculation": "", "numero_seriestring": "", "marque": "", "modele": "", "societe": "", "profession": "", "fonction": ""
    }
}

resultats_temps_reel = []
statut_recherche = "Aucune recherche effectuee"
dernier_timestamp_recherche = 0.0

def initialiser_dossiers():
    if not os.path.exists(TMP_DIR):
        os.makedirs(TMP_DIR)
    if not os.path.exists(EXPORT_DIR):
        os.makedirs(EXPORT_DIR)

def charger_cle_json():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                cle = json.load(f).get("api_key", "")
                return cle.strip()
        except: pass
    return ""

def sauvegarder_cle_json(cle):
    initialiser_dossiers()
    # Nettoyage strict pour éviter les retours à la ligne ou espaces parasites
    cle_propre = cle.strip().replace("\n", "").replace("\r", "").replace(" ", "")
    data = {"api_key": cle_propre, "mis_a_jour_le": datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    return cle_propre

def vider_tous_les_champs():
    global resultats_temps_reel, statut_recherche
    for cat in categories.values():
        for k in cat.keys():
            cat[k] = ""
    resultats_temps_reel = []

def afficher_chargement_barre(stdscr, message):
    h, w = stdscr.getmaxyx()
    largeur_barre = 20
    for i in range(largeur_barre + 1):
        stdscr.clear()
        stdscr.attron(curses.color_pair(4))
        stdscr.box()
        stdscr.attroff(curses.color_pair(4))
        
        rempli = "*" * i
        vide = " " * (largeur_barre - i)
        barre_texte = f"[{rempli}{vide}]"
        
        stdscr.addstr(h // 2 - 1, max(2, (w - len(message)) // 2), message, curses.color_pair(1) | curses.A_BOLD)
        stdscr.addstr(h // 2 + 1, max(2, (w - len(barre_texte)) // 2), barre_texte, curses.color_pair(3))
        stdscr.refresh()
        time.sleep(0.04)

def afficher_animation_dox(stdscr):
    h, w = stdscr.getmaxyx()
    etapes = ["DOX MAKING .", "DOX MAKING ..", "DOX MAKING ...", "DOX MAKING ...."]
    
    for idx in range(12):
        stdscr.clear()
        stdscr.attron(curses.color_pair(2))
        stdscr.box()
        stdscr.attroff(curses.color_pair(2))
        
        msg = etapes[idx % len(etapes)]
        barre = f"[{'*' * (idx + 1)}{' ' * (12 - idx - 1)}]"
        
        stdscr.addstr(h // 2 - 1, max(2, (w - len("COMPILATION DES DONNEES")) // 2), "COMPILATION DES DONNEES", curses.color_pair(2) | curses.A_BLINK | curses.A_BOLD)
        stdscr.addstr(h // 2 + 1, max(2, (w - len(msg)) // 2), msg, curses.color_pair(3) | curses.A_BOLD)
        stdscr.addstr(h // 2 + 2, max(2, (w - len(barre)) // 2), barre, curses.color_pair(1))
        
        stdscr.refresh()
        time.sleep(0.08)

def tester_cle_api(cle):
    headers = {"X-API-Key": cle, "Content-Type": "application/json", "User-Agent": "VerificateurCle/4.0"}
    try:
        r = requests.get(f"{BASE_URL}/me", headers=headers, timeout=5)
        if r.status_code == 200:
            return True, "Cle valide"
        return False, f"Refusee ({r.status_code})"
    except:
        return False, "Erreur de connexion"

def executer_recherche(stdscr, cle_api):
    global resultats_temps_reel, statut_recherche, dernier_timestamp_recherche
    
    temps_actuel = time.time()
    temps_ecoule = temps_actuel - dernier_timestamp_recherche
    if temps_ecoule < 15.0:
        temps_restant = int(15.0 - temps_ecoule)
        statut_recherche = f"Anti-Spam : Attendez {temps_restant}s"
        curses.flash()
        return

    payload = {}
    for cat in categories.values():
        for k, v in cat.items():
            if v: payload[k] = v
            
    if not payload:
        statut_recherche = "Erreur : Aucun critere"
        resultats_temps_reel = []
        return

    payload["flexible"] = False
    payload["per_page"] = 10

    dernier_timestamp_recherche = temps_actuel
    afficher_chargement_barre(stdscr, "Recherche BrixHub en cours...")

    try:
        h_req = {"X-API-Key": cle_api, "Content-Type": "application/json", "User-Agent": "InterfaceGraphique/4.0"}
        r = requests.post(f"{BASE_URL}/search", json=payload, headers=h_req, timeout=30)
        if r.status_code == 200:
            resultats_temps_reel = r.json().get("data", {}).get("results", [])
            statut_recherche = f"Trouve : {len(resultats_temps_reel)} profil(s)"
        else:
            statut_recherche = f"Erreur serveur ({r.status_code})"
            resultats_temps_reel = []
    except:
        statut_recherche = "Erreur reseau ou timeout (30s)"
        resultats_temps_reel = []

def generer_fichier_dox(stdscr, profil):
    global statut_recherche
    initialiser_dossiers()
    afficher_animation_dox(stdscr)
    
    nom = str(profil.get("nom_famille", "INCONNU")).upper().strip()
    prenom = str(profil.get("prenom", "INCONNU")).capitalize().strip()
    
    filename = f"dox_{nom}_{prenom}.txt".replace("/", "_").replace("\\", "_")
    filepath = os.path.join(EXPORT_DIR, filename)
    
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(ASCII_ART + "\n")
            f.write("="*90 + "\n")
            f.write(f" EXPORT DOX MAKER - GENERATION : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f" CIBLE : {prenom} {nom}\n")
            f.write("="*90 + "\n\n")
            
            def ecrire_si_existe(label, valeur):
                if valeur and str(valeur).strip() and str(valeur).strip().upper() != "N/A":
                    f.write(f"    - {label} : {valeur}\n")
                    return True
                return False

            f.write("[+] INFORMATIONS D'IDENTITE\n")
            ecrire_si_existe("Prénom", profil.get('prenom'))
            ecrire_si_existe("Nom de famille", profil.get('nom_famille'))
            ecrire_si_existe("Nom de naissance", profil.get('nom_naissance'))
            ecrire_si_existe("Nom d'affichage / Pseudo", profil.get('nom_affichage'))
            ecrire_si_existe("Nom d'utilisateur", profil.get('nom_utilisateur'))
            ecrire_si_existe("Genre", profil.get('genre'))
            ecrire_si_existe("Civilité", profil.get('civilit'))
            f.write("\n")
            
            f.write("[+] NAISSANCE & ORIGINES\n")
            ecrire_si_existe("Date de naissance", profil.get('date_naissanc'))
            ecrire_si_existe("Jour", profil.get('jour_naissance'))
            ecrire_si_existe("Mois", profil.get('mois_naissance'))
            ecrire_si_existe("Année", profil.get('annee_naissanc'))
            ecrire_si_existe("Ville de naissance", profil.get('ville_naissanc'))
            ecrire_si_existe("Lieu de naissance", profil.get('lieu_naissanc'))
            f.write("\n")
            
            f.write("[+] COORDONNEES DE CONTACT\n")
            ecrire_si_existe("Adresse Email", profil.get('email'))
            ecrire_si_existe("Téléphone fixe", profil.get('telephone'))
            ecrire_si_existe("Téléphone Mobile", profil.get('mobile'))
            ecrire_si_existe("Adresse IP connue", profil.get('adresse_ip'))
            f.write("\n")
            
            f.write("[+] EMPLACEMENT GEOGRAPHIQUE\n")
            ecrire_si_existe("Adresse postale", profil.get('adresse'))
            ecrire_si_existe("Complément d'adresse", profil.get('complement_adress'))
            ecrire_si_existe("Code Postal", profil.get('code_postal'))
            ecrire_si_existe("Ville", profil.get('ville'))
            ecrire_si_existe("Département", profil.get('departement'))
            ecrire_si_existe("Région", profil.get('region'))
            ecrire_si_existe("Pays", profil.get('pays'))
            f.write("\n")
            
            f.write("[+] EMPREINTE NUMERIQUE / GAMING / RP\n")
            ecrire_si_existe("Discord ID", profil.get('discord_id'))
            ecrire_si_existe("Steam ID Hex", profil.get('steam_id'))
            ecrire_si_existe("FiveM License", profil.get('fivem_licensestring'))
            ecrire_si_existe("FiveM License 2", profil.get('fivem_license2string'))
            ecrire_si_existe("FiveM ID", profil.get('fivem_id'))
            ecrire_si_existe("Xbox Live ID", profil.get('xbox_live_id'))
            ecrire_si_existe("Live ID", profil.get('live_id'))
            f.write("\n")
            
            f.write("[+] DONNEES SENSIBLES & VEHICULES\n")
            ecrire_si_existe("NIR (Sécurité Sociale)", profil.get('nir'))
            ecrire_si_existe("IBAN", profil.get('iban'))
            ecrire_si_existe("BIC", profil.get('bic'))
            ecrire_si_existe("SIRET", profil.get('siret'))
            ecrire_si_existe("SIREN", profil.get('siren'))
            ecrire_si_existe("Immatriculation", profil.get('immatriculation'))
            ecrire_si_existe("Numéro VIN / Plaque", profil.get('vin_plaque'))
            ecrire_si_existe("Marque véhicule", profil.get('marque'))
            ecrire_si_existe("Modèle véhicule", profil.get('modele'))
            ecrire_si_existe("Numéro de série", profil.get('numero_seriestring'))
            ecrire_si_existe("Société", profil.get('societe'))
            ecrire_si_existe("Profession", profil.get('profession'))
            ecrire_si_existe("Fonction", profil.get('fonction'))
            f.write("\n")
            
            champs_deja_mis = ['prenom', 'nom_famille', 'nom_naissance', 'nom_affichage', 'nom_utilisateur', 'genre', 'civilit',
                               'date_naissanc', 'jour_naissance', 'mois_naissance', 'annee_naissanc', 'ville_naissanc', 'lieu_naissanc',
                               'email', 'telephone', 'mobile', 'adresse_ip', 'adresse', 'complement_adress', 'code_postal', 'ville',
                               'departement', 'region', 'pays', 'discord_id', 'steam_id', 'fivem_licensestring', 'fivem_license2string',
                               'fivem_id', 'xbox_live_id', 'live_id', 'nir', 'iban', 'bic', 'siret', 'siren', 'immatriculation',
                               'vin_plaque', 'marque', 'modele', 'numero_seriestring', 'societe', 'profession', 'fonction', '_confidence', '_sources']
            for k, v in profil.items():
                if k not in champs_deja_mis:
                    ecrire_si_existe(k.upper(), v)
            
            f.write("\n" + "="*90 + "\n")
            f.write(" END OF FILE - GENERATED BY https://github.com/w83467583-sudo/BrixHubApiOSint \n")
            f.write("="*90 + "\n")
            
        statut_recherche = f"Dox cree -> {filename}"
        vider_tous_les_champs()
        
    except:
        statut_recherche = "Erreur lors de la generation du fichier"

def prompt_saisie_interne(stdscr, label):
    h, w = stdscr.getmaxyx()
    y_input = h - 3
    stdscr.move(y_input, 1)
    stdscr.clrtoeol()
    stdscr.attron(curses.color_pair(4))
    stdscr.box()
    stdscr.attroff(curses.color_pair(4))
    
    stdscr.addstr(y_input, 4, f"Entrez {label} : ", curses.color_pair(3))
    stdscr.refresh()
    curses.echo()
    curses.curs_set(1)
    buffer = stdscr.getstr(y_input, 4 + len(f"Entrez {label} : "), 80) # Augmenté à 80 caractères max pour la clé longue
    curses.noecho()
    curses.curs_set(0)
    
    # Encodage propre et nettoyage immédiat des espaces/retours chariots cachés
    resultat = buffer.decode('utf-8', errors='ignore').strip()
    return resultat.replace("\n", "").replace("\r", "").replace(" ", "")

def gerer_sous_menu_champs(stdscr, nom_cat):
    champs = categories[nom_cat]
    cles_champs = list(champs.keys())
    sel_idx = 0
    
    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        m_x = w // 2
        
        stdscr.attron(curses.color_pair(4))
        stdscr.box()
        for y in range(1, h - 4): stdscr.addstr(y, m_x, "|")
        stdscr.attroff(curses.color_pair(4))
        
        stdscr.addstr(1, 3, f" CONFIGURATION : {nom_cat} ", curses.color_pair(3) | curses.A_BOLD)
        
        y_pos = 4
        for idx, k in enumerate(cles_champs):
            if y_pos >= h - 6: break
            v = champs[k]
            aff_v = f"[{v}]" if v else "---"
            txt = f"  {k.ljust(18)} : {aff_v}"
            if idx == sel_idx:
                stdscr.addstr(y_pos, 2, f"> {txt}"[:m_x-3], curses.color_pair(3) | curses.A_BOLD)
            else:
                stdscr.addstr(y_pos, 2, f"  {txt}"[:m_x-3])
            y_pos += 1
            
        if sel_idx == len(cles_champs):
            stdscr.addstr(y_pos + 1, 2, "> [ VALIDER ET RETOURNER ]", curses.color_pair(1) | curses.A_BOLD)
        else:
            stdscr.addstr(y_pos + 1, 2, "  [ VALIDER ET RETOURNER ]", curses.A_DIM)
            
        stdscr.addstr(4, m_x + 3, "--- RESULTATS ---", curses.color_pair(1) | curses.A_BOLD)
        stdscr.refresh()
        
        key = stdscr.getch()
        if key == curses.KEY_UP: sel_idx = (sel_idx - 1) % (len(cles_champs) + 1)
        elif key == curses.KEY_DOWN: sel_idx = (sel_idx + 1) % (len(cles_champs) + 1)
        elif key in [10, 13, curses.KEY_ENTER]:
            if sel_idx == len(cles_champs): break
            else:
                ch_sel = cles_champs[sel_idx]
                categories[nom_cat][ch_sel] = prompt_saisie_interne(stdscr, ch_sel)

def interface_principale(stdscr):
    global resultats_temps_reel, statut_recherche
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_CYAN)   
    curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    
    curses.curs_set(0)
    stdscr.keypad(True)
    
    initialiser_dossiers()
    cle_api = charger_cle_json()
    if cle_api:
        afficher_chargement_barre(stdscr, "Verification de la cle API enregistree...")
        ok, msg = tester_cle_api(cle_api)
        if not ok:
            statut_recherche = f"Alerte cle : {msg}"
    
    while not cle_api:
        stdscr.clear()
        stdscr.box()
        stdscr.addstr(2, 4, "CLE API INITIALE MANQUANTE (BixHub.net/api)", curses.color_pair(2) | curses.A_BOLD)
        val = prompt_saisie_interne(stdscr, "API_KEY")
        if val:
            cle_api = sauvegarder_cle_json(val)

    index_global = 0
    focus_colonne = "GAUCHE"
    
    scroll_offset_y = 0 
    index_element_selectionne = 0

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        m_x = w // 2
        
        stdscr.attron(curses.color_pair(4))
        stdscr.box()
        for y in range(1, h - 4): stdscr.addstr(y, m_x, "|")
        stdscr.attroff(curses.color_pair(4))
        
        stdscr.addstr(1, 3, " BRIXHUB DASHBOARD ", curses.color_pair(3) | curses.A_BOLD)
        aff_key = f"{cle_api[:12]}..." if len(cle_api) > 12 else cle_api
        stdscr.addstr(2, 3, f" API active: {aff_key} |", curses.color_pair(1))

        # ==================== BLOC DE GAUCHE ====================
        y_cat = 5
        for idx, cat_name in enumerate(LISTE_CATEGORIES):
            nb_remplis = sum(1 for v in categories[cat_name].values() if v)
            info = f"({nb_remplis})" if nb_remplis > 0 else "(-)"
            texte_bouton = f" [ {cat_name.ljust(22)} {info} ] "
            
            if index_global == idx and focus_colonne == "GAUCHE":
                stdscr.addstr(y_cat, 3, texte_bouton[:m_x-4], curses.color_pair(3) | curses.A_BOLD)
            else:
                stdscr.addstr(y_cat, 3, texte_bouton[:m_x-4])
            y_cat += 2

        # ==================== BAS GAUCHE : ACTIONS ====================
        y_bas = h - 8
        stdscr.addstr(y_bas, 2, "─" * (m_x - 3), curses.A_DIM)
        
        temps_restant_visuel = 15.0 - (time.time() - dernier_timestamp_recherche)
        if temps_restant_visuel > 0:
            label_recherche = f"   [ RECHERCHE EN COOLDOWN ({int(temps_restant_visuel)}s) ]   "
        else:
            label_recherche = "   [ >>> EXECUTER LA RECHERCHE <<< ]   "

        if index_global == 6 and focus_colonne == "GAUCHE":
            stdscr.attron(curses.color_pair(1) | curses.A_REVERSE | curses.A_BOLD)
            stdscr.addstr(y_bas + 1, 2, label_recherche[:m_x-2])
            stdscr.attroff(curses.color_pair(1) | curses.A_REVERSE | curses.A_BOLD)
        else:
            stdscr.addstr(y_bas + 1, 2, label_recherche[:m_x-2], curses.color_pair(1))

        est_clean = (index_global == 7 and focus_colonne == "GAUCHE")
        est_quit  = (index_global == 8 and focus_colonne == "GAUCHE")
        
        stdscr.addstr(y_bas + 3, 2, "[ CLEAN ]", curses.color_pair(2) if est_clean else curses.A_DIM)
        stdscr.addstr(y_bas + 3, 20, "[ Quitter ]", curses.color_pair(2) if est_quit else curses.A_DIM)

        # ==================== BLOC DE DROITE ====================
        stdscr.addstr(4, m_x + 3, "--- RESULTATS COMPLETS & DETAILLES ---", curses.A_BOLD | curses.color_pair(1))
        stdscr.addstr(5, m_x + 3, f"Statut : {statut_recherche}"[:w-m_x-6], curses.A_DIM)
        
        if focus_colonne == "DROITE":
            stdscr.addstr(5, max(m_x+4, w - 24), "[ DEFILEMENT / SCROLL ACTIVE ]", curses.color_pair(3) | curses.A_BOLD)
        else:
            stdscr.addstr(5, max(m_x+4, w - 24), "", curses.A_DIM)

        lignes_a_afficher = []
        
        if not resultats_temps_reel:
            lignes_a_afficher.append(("TITRE_BRUT", "En attente d'execution..."))
            lignes_a_afficher.append(("TEXTE_SIMPLE", ""))
            for c_n, c_ch in categories.items():
                for k, v in c_ch.items():
                    if v:
                        lignes_a_afficher.append(("PREVIEW_CHAMP", f"  * {k} = {v}"))
                        lignes_a_afficher.append(("TEXTE_SIMPLE", ""))
        else:
            mapping_structure = [
                ("[ IDENTITE & ETAT CIVIL ]", ["prenom", "nom_famille", "nom_naissance", "nom_affichage", "nom_utilisateur", "genre", "civilit"]),
                ("[ INFORMATION NAISSANCE ]", ["date_naissanc", "jour_naissance", "mois_naissance", "annee_naissanc", "ville_naissanc", "lieu_naissanc"]),
                ("[ COORDONNEES DE CONTACT ]", ["email", "telephone", "mobile", "adresse_ip"]),
                ("[ LOCALISATION ET POSTALE ]", ["adresse", "complement_adress", "code_postal", "ville", "departement", "region", "pays"]),
                ("[ EMPREINTE GAMING & RP ]", ["discord_id", "steam_id", "fivem_licensestring", "fivem_license2string", "fivem_id", "xbox_live_id", "live_id"]),
                ("[ DONNEES SENSIBLES / VEHICULES ]", ["nir", "iban", "bic", "siret", "siren", "immatriculation", "vin_plaque", "marque", "modele", "numero_seriestring", "societe", "profession", "fonction"])
            ]

            for p_idx, profil in enumerate(resultats_temps_reel):
                lignes_a_afficher.append(("TEXTE_SIMPLE", "┌" + "─" * (w - m_x - 8) + "┐"))
                titre_profil = f" PROFIL #{p_idx + 1} ── Fiabilité : {profil.get('_confidence', 0)}% "
                lignes_a_afficher.append(("ENTETE_PROFIL", titre_profil, profil))
                lignes_a_afficher.append(("TEXTE_SIMPLE", "└" + "─" * (w - m_x - 8) + "┘"))
                lignes_a_afficher.append(("TEXTE_SIMPLE", ""))
                
                for nom_bloc, cles_bloc in mapping_structure:
                    bloc_a_ajouter = []
                    for cle in cles_bloc:
                        valeur = profil.get(cle)
                        if valeur:
                            bloc_a_ajouter.append(("INFO_LIGNE", f"    → {cle.upper().ljust(18)} : {valeur}"))
                            bloc_a_ajouter.append(("TEXTE_SIMPLE", ""))
                    
                    if bloc_a_ajouter:
                        lignes_a_afficher.append(("SECTION_BLOC", f"  {nom_bloc}"))
                        lignes_a_afficher.append(("TEXTE_SIMPLE", ""))
                        lignes_a_afficher.extend(bloc_a_ajouter)
                
                cles_deja_traitees = sum([c for n, c in mapping_structure], []) + ['_confidence', '_sources']
                bloc_extra = []
                for k, v in profil.items():
                    if k not in cles_deja_traitees and v:
                        bloc_extra.append(("INFO_LIGNE", f"    → {k.upper().ljust(18)} : {v}"))
                        bloc_extra.append(("TEXTE_SIMPLE", ""))
                
                if bloc_extra:
                    lignes_a_afficher.append(("SECTION_BLOC", "  [ DONNEES COMPLEMENTAIRES BRUTES ]"))
                    lignes_a_afficher.append(("TEXTE_SIMPLE", ""))
                    lignes_a_afficher.extend(bloc_extra)

                lignes_a_afficher.append(("TEXTE_SIMPLE", "═" * (w - m_x - 6)))
                lignes_a_afficher.append(("TEXTE_SIMPLE", ""))

        y_debut_affichage = 7
        hauteur_disponible_affichage = h - 9 
        
        max_elements = len(lignes_a_afficher)
        if index_element_selectionne >= max_elements:
            index_element_selectionne = max(0, max_elements - 1)
            
        if index_element_selectionne < scroll_offset_y:
            scroll_offset_y = index_element_selectionne
        elif index_element_selectionne >= scroll_offset_y + hauteur_disponible_affichage:
            scroll_offset_y = index_element_selectionne - hauteur_disponible_affichage + 1

        for visible_idx in range(hauteur_disponible_affichage):
            contexte_idx = scroll_offset_y + visible_idx
            if contexte_idx >= len(lignes_a_afficher):
                break
                
            element = lignes_a_afficher[contexte_idx]
            y_ecran = y_debut_affichage + visible_idx
            est_element_selectionne = (focus_colonne == "DROITE" and contexte_idx == index_element_selectionne)
            
            type_ligne = element[0]
            
            if type_ligne == "ENTETE_PROFIL":
                txt = element[1]
                if est_element_selectionne:
                    stdscr.addstr(y_ecran, m_x + 3, f"  > CLIQUEZ ICI POUR GENERER LE DOX <  ", curses.color_pair(3) | curses.A_BOLD)
                else:
                    stdscr.addstr(y_ecran, m_x + 3, txt[:w-m_x-4], curses.color_pair(1) | curses.A_BOLD)
            elif type_ligne == "SECTION_BLOC":
                stdscr.addstr(y_ecran, m_x + 3, element[1][:w-m_x-4], curses.color_pair(4) | curses.A_BOLD)
            elif type_ligne == "INFO_LIGNE":
                txt = element[1]
                if est_element_selectionne:
                    stdscr.addstr(y_ecran, m_x + 3, txt[:w-m_x-5], curses.color_pair(3) | curses.A_BOLD)
                else:
                    stdscr.addstr(y_ecran, m_x + 3, txt[:w-m_x-5], curses.A_BOLD)
            elif type_ligne == "PREVIEW_CHAMP":
                stdscr.addstr(y_ecran, m_x + 4, element[1][:w-m_x-6], curses.color_pair(1) | curses.A_BOLD)
            elif type_ligne == "TITRE_BRUT":
                stdscr.addstr(y_ecran, m_x + 3, element[1], curses.color_pair(2) | curses.A_BOLD)
            else:
                stdscr.addstr(y_ecran, m_x + 3, element[1][:w-m_x-5], curses.A_BOLD)

        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_RIGHT and resultats_temps_reel:
            focus_colonne = "DROITE"
            index_element_selectionne = 1
            scroll_offset_y = 0
        elif key == curses.KEY_LEFT:
            focus_colonne = "GAUCHE"

        # ==================== NAVIGATION COLONNE GAUCHE ====================
        if focus_colonne == "GAUCHE":
            if key == curses.KEY_UP:
                index_global = (index_global - 1) % 9
            elif key == curses.KEY_DOWN:
                index_global = (index_global + 1) % 9
            elif key in [10, 13, curses.KEY_ENTER]:
                if index_global < 6:
                    gerer_sous_menu_champs(stdscr, LISTE_CATEGORIES[index_global])
                elif index_global == 6:
                    executer_recherche(stdscr, cle_api)
                elif index_global == 7:
                    vider_tous_les_champs()
                    statut_recherche = "Toutes les selections ont ete nettoyees"
                elif index_global == 8:
                    break
                    
        # ==================== NAVIGATION COLONNE DROITE ====================
        elif focus_colonne == "DROITE" and max_elements > 0:
            if key == curses.KEY_UP:
                index_element_selectionne = (index_element_selectionne - 1) % max_elements
            elif key == curses.KEY_DOWN:
                index_element_selectionne = (index_element_selectionne + 1) % max_elements
            elif key in [10, 13, curses.KEY_ENTER]:
                scan_idx = index_element_selectionne
                while scan_idx >= 0:
                    if lignes_a_afficher[scan_idx][0] == "ENTETE_PROFIL":
                        target_profil = lignes_a_afficher[scan_idx][2]
                        generer_fichier_dox(stdscr, target_profil)
                        break
                    scan_idx -= 1
                    
                focus_colonne = "GAUCHE"
                index_global = 0
BRIXHUB DASHBOARD
if __name__ == "__main__":
    curses.wrapper(interface_principale)
