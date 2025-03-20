from tkinter import *
import mysql.connector

# Connexion à la base de données MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="bank"
)
cursor = conn.cursor()

# Création de la table si elle n'existe pas
cursor.execute('''CREATE TABLE IF NOT EXISTS user (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL)''')
conn.commit()

# Fonction pour enregistrer un nouvel utilisateur
def enregistrer_utilisateur(email, mot_de_passe):
    try:
        cursor.execute("INSERT INTO user (email, password) VALUES (%s, %s)", (email, mot_de_passe))
        conn.commit()
    except mysql.connector.IntegrityError:
        return False
    return True

# Fonction de connexion
def connecter_utilisateur(email, mot_de_passe):
    cursor.execute("SELECT password FROM user WHERE email = %s", (email,))
    utilisateur = cursor.fetchone()
    
    if utilisateur and utilisateur[0] == mot_de_passe:
        return True
    return False

# Fonction pour ouvrir la fenêtre du compte
def ouvrir_compte():
    fenetre_solde = Toplevel(fenetre)
    fenetre_solde.title("Mon Compte")
    fenetre_solde.minsize(400, 250)

    cadre_compte = Frame(fenetre_solde, padx=20, pady=20)
    cadre_compte.pack(fill="both", expand=True)

    Label(cadre_compte, text="Bienvenue sur votre compte", font=("Arial", 14, "bold")).pack(pady=10)
    Label(cadre_compte, text="Votre solde actuel est :", font=("Arial", 12)).pack(pady=5)
    
    solde = 1500.00
    Label(cadre_compte, text=f"{solde} €", font=("Arial", 16, "bold"), fg="green").pack(pady=10)

# Fonction de vérification de connexion
def verifier_connexion():
    email = expression1.get()
    mot_de_passe = expression2.get()
    
    if connecter_utilisateur(email, mot_de_passe):
        ouvrir_compte()
    else:
        label_erreur.config(text="Identifiants incorrects", fg="red")

# Interface graphique principale
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

conn.close()
