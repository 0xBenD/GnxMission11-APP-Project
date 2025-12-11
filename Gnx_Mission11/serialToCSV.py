import serial
import csv
import sys
import time
import os

# --- CONFIGURATION ---
PORT = "/dev/cu.usbmodem0E22C84F1"
BAUDRATE = 9600
TRIGGER_START = "Fin de la salve"
NB_MESURES_MAX = 10000
NOM_BASE_FICHIER = "mesures_sonores.csv"

# Ton chemin vers le dossier synchronisé Teams
# os.path.expanduser permet de remplacer le "~" par "/Users/ton_nom" automatiquement
CHEMIN_DOSSIER_TEAMS = os.path.expanduser("~/Documents/ISEP/APP G7C - APP Signal Processing Missions/csv")

def generer_chemin_fichier_unique(dossier, nom_fichier):
    """
    Génère un chemin complet unique (ex: mesures_sonores_1.csv)
    pour ne pas écraser les fichiers précédents.
    """
    base, extension = os.path.splitext(nom_fichier)
    compteur = 1
    
    # Construction du chemin initial
    chemin_final = os.path.join(dossier, nom_fichier)
    
    # Tant que le fichier existe, on incrémente le numéro
    while os.path.exists(chemin_final):
        nouveau_nom = f"{base}_{compteur}{extension}"
        chemin_final = os.path.join(dossier, nouveau_nom)
        compteur += 1
    
    return chemin_final

def lire_port_serie():
    ser = None
    try:
        # 1. Vérification que le dossier de destination existe
        if not os.path.exists(CHEMIN_DOSSIER_TEAMS):
            print(f"❌ Erreur : Le dossier n'existe pas :")
            print(f"👉 {CHEMIN_DOSSIER_TEAMS}")
            print("Vérifie que tu as bien créé le dossier 'csv' dans ton dossier APP G7C.")
            return

        # 2. Génération du nom de fichier unique
        fichier_sortie = generer_chemin_fichier_unique(CHEMIN_DOSSIER_TEAMS, NOM_BASE_FICHIER)
        
        # 3. Connexion Série
        ser = serial.Serial(PORT, BAUDRATE, timeout=3)
        print(f"✅ Connecté à l'Arduino sur {PORT}")
        print(f"📂 Destination : {fichier_sortie}")
        print(f"⏳ En attente du déclencheur : '{TRIGGER_START}'...")

        # 4. Ouverture et écriture
        with open(fichier_sortie, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Pas d'en-tête pour compatibilité MATLAB directe
            
            enregistrement_actif = False
            compteur_valeurs = 0
            
            while True:
                try:
                    ligne_bytes = ser.readline()
                    ligne = ligne_bytes.decode('utf-8', errors='ignore').strip()

                    # Gestion Timeout
                    if enregistrement_actif and not ligne:
                        print("\n\n⚠️ Timeout (Arduino silencieux). Arrêt.")
                        break

                    if not ligne:
                        continue

                    # Détection du démarrage
                    if TRIGGER_START in ligne:
                        enregistrement_actif = True
                        print(f"\n🚀 DÉCLENCHEUR REÇU ! Enregistrement en cours...")
                        continue

                    # Enregistrement des données
                    if enregistrement_actif:
                        # Vérification stricte (nombre entier)
                        if ligne.isdigit() or (ligne.startswith('-') and ligne[1:].isdigit()):
                            try:
                                valeur = int(ligne)
                                # Filtre 0 - 4096
                                if 0 <= valeur <= 4096:
                                    writer.writerow([valeur])
                                    compteur_valeurs += 1
                                    
                                    # Barre de progression
                                    pourcentage = (compteur_valeurs / NB_MESURES_MAX) * 100
                                    sys.stdout.write(f"\r☁️ Sync Teams : {compteur_valeurs}/{NB_MESURES_MAX} ({pourcentage:.1f}%)")
                                    sys.stdout.flush()

                                    # Arrêt automatique
                                    if compteur_valeurs >= NB_MESURES_MAX:
                                        print("\n\n✅ Terminé ! 10 000 valeurs enregistrées sur Teams.")
                                        break
                            except ValueError:
                                pass 

                except KeyboardInterrupt:
                    print("\n\n🛑 Arrêt manuel.")
                    break

    except serial.SerialException as e:
        print(f"\n❌ Erreur Port Série : {e}")
        if "Resource busy" in str(e):
            print("👉 Ferme le moniteur d'Energia !")
    except PermissionError:
        print(f"\n❌ Erreur de Permission : Impossible d'écrire dans {CHEMIN_DOSSIER_TEAMS}")
        print("👉 Vérifie que ton terminal a l'accès aux fichiers (Réglages Système > Confidentialité > Fichiers et dossiers)")
    finally:
        if ser and ser.is_open:
            ser.close()

if __name__ == "__main__":
    lire_port_serie()
