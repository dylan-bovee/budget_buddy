import sqlite3
import bcrypt
import re
from tkinter import *
from tkinter import messagebox

# Connexion à la base de données SQLite
conn = sqlite3.connect("utilisateurs.db")
cursor = conn.cursor()

# Création de la table utilisateurs si elle n'existe pas
cursor.execute('''CREATE TABLE IF NOT EXISTS utilisateurs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT,
                    prenom TEXT,
                    email TEXT UNIQUE,
                    mot_de_passe BLOB)''')  # Stockage en BLOB car c'est un hash
conn.commit()

# Vérification de la robustesse du mot de passe
def verifier_mot_de_passe(mot_de_passe):
    if len(mot_de_passe) < 10:
        return False, "Le mot de passe doit contenir au moins 10 caractères."
    if not re.search(r'[A-Z]', mot_de_passe):
        return False, "Le mot de passe doit contenir au moins une majuscule."
    if not re.search(r'[a-z]', mot_de_passe):
        return False, "Le mot de passe doit contenir au moins une minuscule."
    if not re.search(r'[0-9]', mot_de_passe):
        return False, "Le mot de passe doit contenir au moins un chiffre."
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', mot_de_passe):
        return False, "Le mot de passe doit contenir au moins un caractère spécial."
    return True, "Mot de passe valide."

# Hachage du mot de passe avec bcrypt
def hacher_mot_de_passe(mot_de_passe):
    sel = bcrypt.gensalt()
    hash_mdp = bcrypt.hashpw(mot_de_passe.encode(), sel)
    return hash_mdp

# Enregistrement d'un utilisateur
def inscrire_utilisateur(nom, prenom, email, mot_de_passe):
    valide, message = verifier_mot_de_passe(mot_de_passe)
    if not valide:
        messagebox.showerror("Erreur", message)
        return

    mot_de_passe_hache = hacher_mot_de_passe(mot_de_passe)
    
    try:
        cursor.execute("INSERT INTO utilisateurs (nom, prenom, email, mot_de_passe) VALUES (?, ?, ?, ?)",
                       (nom, prenom, email, mot_de_passe_hache))
        conn.commit()
        messagebox.showinfo("Succès", "Inscription réussie !")
    except sqlite3.IntegrityError:
        messagebox.showerror("Erreur", "Cet email est déjà utilisé.")

# Vérification du mot de passe lors de la connexion
def verifier_mot_de_passe_hache(mot_de_passe, hash_stocke):
    return bcrypt.checkpw(mot_de_passe.encode(), hash_stocke)

# Connexion d'un utilisateur
def verifier_login():
    email = expression1.get()
    mot_de_passe = expression2.get()
    
    cursor.execute("SELECT mot_de_passe FROM utilisateurs WHERE email = ?", (email,))
    utilisateur = cursor.fetchone()

    if utilisateur:
        hash_stocke = utilisateur[0]  # Mot de passe hashé stocké en base
        if verifier_mot_de_passe_hache(mot_de_passe, hash_stocke):
            messagebox.showinfo("Succès", "Connexion réussie !")
            ouvrir_compte()
        else:
            messagebox.showerror("Erreur", "Mot de passe incorrect.")
    else:
        messagebox.showerror("Erreur", "Utilisateur non trouvé.")

# Interface graphique avec Tkinter
def ouvrir_compte():
    """Ouvre une nouvelle fenêtre affichant le solde."""
    fenetre_solde = Toplevel(fenetre)
    fenetre_solde.title("Mon Compte")
    fenetre_solde.minsize(400, 250)

    cadre_compte = Frame(fenetre_solde, padx=20, pady=20)
    cadre_compte.pack(fill="both", expand=True)

    Label(cadre_compte, text="Bienvenue sur votre compte", font=("Arial", 14, "bold")).pack(pady=10)
    Label(cadre_compte, text="Votre solde actuel est :", font=("Arial", 12)).pack(pady=5)

    solde = 1500.00 
    Label(cadre_compte, text=f"{solde} €", font=("Arial", 16, "bold"), fg="green").pack(pady=10)

    def afficher_virement():
        label_virement.config(text="Virement effectué avec succès !")

    label_virement = Label(cadre_compte, text="", font=("Arial", 12), fg="blue")
    label_virement.pack(pady=5)

    cadre_bas = Frame(fenetre_solde)
    cadre_bas.pack(side="bottom", fill="x", padx=10, pady=10)

    bouton_virement = Button(cadre_bas, text="Effectuer un virement", font=("Arial", 12), command=afficher_virement)
    bouton_virement.pack(side="left")

# Fenêtre principale (Login / Inscription)
fenetre = Tk()
fenetre.title("La Banque")
fenetre.minsize(400, 250)

cadre = Frame(fenetre, padx=20, pady=20)
cadre.pack()

titre = Label(cadre, text="Connexion à votre compte", font=("Arial", 14, "bold"))
titre.grid(row=0, column=0, columnspan=2, pady=10)

Label(cadre, text="Identifiant (Email):").grid(row=1, column=0, sticky=E, padx=5, pady=5)
expression1 = StringVar()
entree1 = Entry(cadre, textvariable=expression1, width=30)
entree1.grid(row=1, column=1, padx=5, pady=5)

Label(cadre, text="Mot de passe:").grid(row=2, column=0, sticky=E, padx=5, pady=5)
expression2 = StringVar()
entree2 = Entry(cadre, textvariable=expression2, width=30, show="*")
entree2.grid(row=2, column=1, padx=5, pady=5)

bouton_login = Button(cadre, text="Login", width=15, command=verifier_login)
bouton_login.grid(row=3, column=0, columnspan=2, pady=5)

Label(cadre, text="Vous n'avez pas de compte ?").grid(row=4, column=0, columnspan=2, pady=5)

bouton_inscription = Button(cadre, text="S'inscrire", width=15, command=lambda: inscrire_utilisateur("Jean", "Dupont", "jean.dupont@email.com", "Ex@mple123"))
bouton_inscription.grid(row=5, column=0, columnspan=2, pady=5)

fenetre.mainloop()
