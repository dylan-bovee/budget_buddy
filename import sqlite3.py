from tkinter import *
import sqlite3
import bcrypt

# Connexion à la base de données SQLite
conn = sqlite3.connect("utilisateurs.db")
cursor = conn.cursor()

# Fonction de vérification du mot de passe
def verifier_mot_de_passe_hache(mot_de_passe, hash_stocke):
    return bcrypt.checkpw(mot_de_passe.encode(), hash_stocke)

# Fonction de connexion
def connecter_utilisateur(email, mot_de_passe):
    cursor.execute("SELECT mot_de_passe FROM utilisateurs WHERE email = ?", (email,))
    utilisateur = cursor.fetchone()

    if utilisateur:
        hash_stocke = utilisateur[0]  # Le mot de passe est déjà sous forme de bytes
        if verifier_mot_de_passe_hache(mot_de_passe, hash_stocke):
            return True
    return False

# Fonction appelée par le bouton Login
def verifier_connexion():
    email = expression1.get()
    mot_de_passe = expression2.get()
    
    if connecter_utilisateur(email, mot_de_passe):
        ouvrir_compte()  # Ouvre la fenêtre du compte si la connexion est réussie
    else:
        label_erreur.config(text="Identifiants incorrects", fg="red")

# Fonction pour afficher la page de compte après connexion
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

# Création de la fenêtre principale
fenetre = Tk()
fenetre.title("La Banque")
fenetre.minsize(400, 200)

cadre = Frame(fenetre, padx=20, pady=20)
cadre.pack()

titre = Label(cadre, text="Entre les codes", font=("Arial", 14, "bold"))
titre.grid(row=0, column=0, columnspan=2, pady=10)

Label(cadre, text="Email:").grid(row=1, column=0, sticky=E, padx=5, pady=5)
expression1 = StringVar()
entree1 = Entry(cadre, textvariable=expression1, width=30)
entree1.grid(row=1, column=1, padx=5, pady=5)

Label(cadre, text="Mot de passe:").grid(row=2, column=0, sticky=E, padx=5, pady=5)
expression2 = StringVar()
entree2 = Entry(cadre, textvariable=expression2, width=30, show="*")
entree2.grid(row=2, column=1, padx=5, pady=5)

label_erreur = Label(cadre, text="", font=("Arial", 10), fg="red")
label_erreur.grid(row=3, column=0, columnspan=2, pady=5)

bouton = Button(cadre, text="Login", width=15, command=verifier_connexion)
bouton.grid(row=4, column=0, columnspan=2, pady=10)

fenetre.mainloop()
