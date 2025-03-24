from tkinter import *
import tkinter as tk
from tkinter import messagebox
import mysql.connector
import bcrypt
import re


# Connexion à la base de données MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="bank"
)
cursor = conn.cursor()

# Création des tables si elles n'existent pas
cursor.execute('''CREATE TABLE IF NOT EXISTS user (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    solde FLOAT DEFAULT 0.0)''')
conn.commit()

cursor.execute('''CREATE TABLE IF NOT EXISTS transaction (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    type_transaction VARCHAR(50),
                    amount FLOAT,
                    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES user(id))''')
conn.commit()

cursor.execute('''CREATE TABLE IF NOT EXISTS transaction_history (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    transaction_type VARCHAR(50),
                    amount FLOAT,
                    balance_after FLOAT,
                    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES user(id))''')
conn.commit()

#Fonction pour valider le mot de passe selon les critères
def valider_mot_de_passe(mot_de_passe):
    # Vérification des critères
    if len(mot_de_passe) < 10:
        return False, "Le mot de passe doit contenir au moins 10 caractères."
    if not re.search("[a-z]", mot_de_passe):  # Au moins une minuscule
        return False, "Le mot de passe doit contenir au moins une minuscule."
    if not re.search("[A-Z]", mot_de_passe):  # Au moins une majuscule
        return False, "Le mot de passe doit contenir au moins une majuscule."
    if not re.search("[0-9]", mot_de_passe):  # Au moins un chiffre
        return False, "Le mot de passe doit contenir au moins un chiffre."
    if not re.search("[@#$%^&+=]", mot_de_passe):  # Au moins un caractère spécial
        return False, "Le mot de passe doit contenir au moins un caractère spécial (@#$%^&+=)."
    return True, ""

# Fonction de hachage du mot de passe avec bcrypt
def hacher_mot_de_passe(mot_de_passe):
    # Générer un salt
    salt = bcrypt.gensalt()
    # Hacher le mot de passe
    mot_de_passe_hache = bcrypt.hashpw(mot_de_passe.encode('utf-8'), salt)
    return mot_de_passe_hache

# Fonction pour enregistrer un nouvel utilisateur (ajout des champs surname et name)
def enregistrer_utilisateur(name, surname, email, mot_de_passe):
    # Vérification de la validité du mot de passe
    valid, message = valider_mot_de_passe(mot_de_passe)
    if not valid:
        messagebox.showerror("Erreur", message)
        return
    
    # Hachage du mot de passe
    mot_de_passe_hache = hacher_mot_de_passe(mot_de_passe)
    
    try:
        cursor.execute("INSERT INTO user (name, surname, email, password) VALUES (%s, %s, %s, %s)", (name, surname, email, mot_de_passe_hache))
        conn.commit()
        messagebox.showinfo("Succès", "Inscription réussie !")
    except mysql.connector.IntegrityError:
        messagebox.showerror("Erreur", "Cet email est déjà utilisé.")

# Fonction de connexion
def connecter_utilisateur(email, mot_de_passe):
    cursor.execute("SELECT id, password, solde FROM user WHERE email = %s", (email,))
    utilisateur = cursor.fetchone()

    if utilisateur:
        mot_de_passe_stocke = utilisateur[1]
        # Vérification du mot de passe en comparant le mot de passe fourni avec le mot de passe haché
        if bcrypt.checkpw(mot_de_passe.encode('utf-8'), mot_de_passe_stocke.encode('utf-8')):
            return utilisateur  # Retourner id, password, solde
    return None

# Fonction pour ouvrir la fenêtre du compte
def ouvrir_compte(utilisateur):
    fenetre_solde = Toplevel(fenetre)
    fenetre_solde.title("Mon Compte")
    fenetre_solde.minsize(400, 250)

    cadre_compte = Frame(fenetre_solde, padx=20, pady=20)
    cadre_compte.pack(fill="both", expand=True)

    Label(cadre_compte, text="Bienvenue sur votre compte", font=("Arial", 14, "bold")).pack(pady=10)
    Label(cadre_compte, text="Votre solde actuel est :", font=("Arial", 12)).pack(pady=5)
    
    solde = utilisateur[2]
    Label(cadre_compte, text=f"{solde} €", font=("Arial", 16, "bold"), fg="green").pack(pady=10)

    # Boutons pour les opérations
    Button(cadre_compte, text="Déposer", width=20, command=lambda: deposer_fenetre(utilisateur[0])).pack(pady=5)
    Button(cadre_compte, text="Retirer", width=20, command=lambda: retirer_fenetre(utilisateur[0])).pack(pady=5)
    Button(cadre_compte, text="Transférer", width=20, command=lambda: transferer_fenetre(utilisateur[0])).pack(pady=5)
    Button(cadre_compte, text="Historique", width=20, command=lambda: afficher_historique(utilisateur[0])).pack(pady=5)

# Fonction de vérification de connexion
def verifier_connexion():
    email = expression1.get()
    mot_de_passe = expression2.get()
    
    utilisateur = connecter_utilisateur(email, mot_de_passe)
    if utilisateur:
        ouvrir_compte(utilisateur)
    else:
        label_erreur.config(text="Identifiants incorrects", fg="red")

# Fonction d'inscription utilisateur avec ajout des champs name et surname
def afficher_formulaire_inscription():
    def inscrire():
        name = entry_name.get()
        surname = entry_surname.get()
        email = entry_email.get()
        mot_de_passe = entry_motdepasse.get()
        mot_de_passe_confirmation = entry_motdepasse_confirmation.get()

        if mot_de_passe != mot_de_passe_confirmation:
            messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas.")
            return

        enregistrer_utilisateur(name, surname, email, mot_de_passe)

    fenetre_inscription = Toplevel(fenetre)
    fenetre_inscription.title("Inscription")
    fenetre_inscription.minsize(400, 300)

    Label(fenetre_inscription, text="Prénom:").pack(pady=10)
    entry_name = Entry(fenetre_inscription, width=30)
    entry_name.pack(pady=5)

    Label(fenetre_inscription, text="Nom de famille:").pack(pady=10)
    entry_surname = Entry(fenetre_inscription, width=30)
    entry_surname.pack(pady=5)

    Label(fenetre_inscription, text="Email:").pack(pady=10)
    entry_email = Entry(fenetre_inscription, width=30)
    entry_email.pack(pady=5)

    Label(fenetre_inscription, text="Mot de passe:").pack(pady=10)
    entry_motdepasse = Entry(fenetre_inscription, width=30, show="*")
    entry_motdepasse.pack(pady=5)

    Label(fenetre_inscription, text="Confirmer le mot de passe:").pack(pady=10)
    entry_motdepasse_confirmation = Entry(fenetre_inscription, width=30, show="*")
    entry_motdepasse_confirmation.pack(pady=5)

    Button(fenetre_inscription, text="S'inscrire", command=inscrire).pack(pady=20)

# Fonction de dépôt
def deposer_fenetre(user_id):
    def deposer():
        try:
            amount = float(entry_amount.get())
            description = entry_description.get().strip()

            if not description:
                messagebox.showerror("Erreur", "Veuillez entrer une description pour le dépôt.")
                return

            # Insérer dans la base de données
            cursor.execute("INSERT INTO transaction (user_id, type_transaction, type, amount, description) VALUES (%s, %s, %s, %s, %s)", (user_id, "Dépôt", "Dépôt", amount, description))
            cursor.execute("UPDATE user SET solde = solde + %s WHERE id = %s", (amount, user_id))
            conn.commit()

            messagebox.showinfo("Succès", "Dépôt effectué avec succès !")

        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un montant valide.")
        except mysql.connector.Error as err:
            messagebox.showerror("Erreur SQL", f"Erreur : {err}")

    # Interface Tkinter
    root = tk.Tk()
    root.title("Dépôt d'argent")

    tk.Label(root, text="Montant:").pack()
    entry_amount = tk.Entry(root)
    entry_amount.pack()

    tk.Label(root, text="Description:").pack()
    entry_description = tk.Entry(root)
    entry_description.pack()

    btn_deposer = tk.Button(root, text="Déposer", command=deposer)
    btn_deposer.pack()

# Fonction de retrait
def retirer_fenetre(user_id):
    def retirer():
        try:
            amount = float(entry_amount.get())
            description = entry_description.get().strip()

            if not description:
                messagebox.showerror("Erreur", "Veuillez entrer une description pour le retrait.")
                return

            cursor.execute("SELECT solde FROM user WHERE id = %s", (user_id,))
            solde_actuel = cursor.fetchone()[0]

            if amount <= 0:
                messagebox.showerror("Erreur", "Montant invalide.")
            elif amount > solde_actuel:
                messagebox.showerror("Erreur", "Solde insuffisant.")
            else:
                # Mise à jour du solde et insertion du retrait dans la transaction
                cursor.execute("UPDATE user SET solde = solde - %s WHERE id = %s", (amount, user_id))
                cursor.execute("INSERT INTO transaction (user_id, type_transaction, type, amount, description) VALUES (%s, %s, %s, %s, %s)",
                               (user_id, "Retrait", "Retrait", amount, description))
                cursor.execute("INSERT INTO transaction_history (user_id, transaction_type, amount, balance_after) VALUES (%s, %s, %s, (SELECT solde FROM user WHERE id = %s))",
                               (user_id, "Retrait", amount, user_id))
                
                conn.commit()

                messagebox.showinfo("Succès", f"Retrait de {amount} € effectué avec succès.")
                root.destroy()  # Fermer la fenêtre après succès

        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un montant valide.")
        except mysql.connector.Error as err:
            messagebox.showerror("Erreur SQL", f"Erreur : {err}")

    # Interface Tkinter
    root = tk.Tk()
    root.title("Retrait d'argent")

    tk.Label(root, text="Montant:").pack()
    entry_amount = tk.Entry(root)
    entry_amount.pack()

    tk.Label(root, text="Description:").pack()
    entry_description = tk.Entry(root)
    entry_description.pack()

    btn_retirer = tk.Button(root, text="Retirer", command=retirer)
    btn_retirer.pack()
# Fonction de transfert
def transferer_fenetre(user_id):
    def transferer():
        try:
            amount = float(entree_amount.get())
            email_destinataire = entree_email_destinataire.get()
            description = entree_description.get().strip()  # Récupérer la description

            # Vérification du solde et de l'existence du destinataire
            cursor.execute("SELECT solde FROM user WHERE id = %s", (user_id,))
            solde_actuel = cursor.fetchone()[0]

            cursor.execute("SELECT id FROM user WHERE email = %s", (email_destinataire,))
            destinataire = cursor.fetchone()

            if amount <= 0:
                label_message.config(text="Montant invalide", fg="red")
            elif amount > solde_actuel:
                label_message.config(text="Solde insuffisant", fg="red")
            elif not destinataire:
                label_message.config(text="Destinataire non trouvé", fg="red")
            elif not description:
                label_message.config(text="Veuillez entrer une description", fg="red")
            else:
                destinataire_id = destinataire[0]
                # Mise à jour des soldes
                cursor.execute("UPDATE user SET solde = solde - %s WHERE id = %s", (amount, user_id))
                cursor.execute("UPDATE user SET solde = solde + %s WHERE id = %s", (amount, destinataire_id))
                
                # Enregistrer la transaction avec la description
                cursor.execute("INSERT INTO transaction (user_id, type_transaction, amount, description) VALUES (%s, CONCAT('Transfert vers ', %s), %s, %s)", 
                               (user_id, email_destinataire, amount, description))
                
                # Insérer dans transaction_history avec la description
                cursor.execute("INSERT INTO transaction_history (user_id, transaction_type, amount, balance_after, description) VALUES (%s, 'Transfert', %s, (SELECT solde FROM user WHERE id = %s), %s)", 
                               (user_id, amount, user_id, description))
                
                conn.commit()

                label_message.config(text=f"Transfert de {amount} € effectué vers {email_destinataire}", fg="green")
                fenetre_transferer.destroy()

        except ValueError:
            label_message.config(text="Veuillez entrer un montant valide.", fg="red")
        except mysql.connector.Error as err:
            label_message.config(text=f"Erreur SQL : {err}", fg="red")

    # Fenêtre de transfert
    fenetre_transferer = Toplevel(fenetre)
    fenetre_transferer.title("Transférer de l'argent")
    fenetre_transferer.minsize(300, 250)  # Ajuster la taille pour accueillir la description

    label_amount = Label(fenetre_transferer, text="Montant à transférer:")
    label_amount.pack(pady=10)

    entree_amount = Entry(fenetre_transferer, width=20)
    entree_amount.pack(pady=10)

    label_email_destinataire = Label(fenetre_transferer, text="Email du destinataire:")
    label_email_destinataire.pack(pady=10)

    entree_email_destinataire = Entry(fenetre_transferer, width=20)
    entree_email_destinataire.pack(pady=10)

    label_description = Label(fenetre_transferer, text="Description (obligatoire):")  # Nouveau champ pour la description
    label_description.pack(pady=10)

    entree_description = Entry(fenetre_transferer, width=20)  # Champ de saisie pour la description
    entree_description.pack(pady=10)

    bouton_transferer = Button(fenetre_transferer, text="Transférer", command=transferer)
    bouton_transferer.pack(pady=10)

    label_message = Label(fenetre_transferer, text="", font=("Arial", 10))
    label_message.pack(pady=5)


# Fonction pour afficher l'historique
def afficher_historique(user_id):
    cursor.execute("SELECT type_transaction, amount, date FROM transaction WHERE user_id = %s ORDER BY date DESC", (user_id,))
    transactions = cursor.fetchall()
    
    fenetre_historique = Toplevel(fenetre)
    fenetre_historique.title("Historique des transactions")
    fenetre_historique.minsize(400, 300)

    cadre_historique = Frame(fenetre_historique, padx=20, pady=20)
    cadre_historique.pack(fill="both", expand=True)

    Label(cadre_historique, text="Historique des transactions", font=("Arial", 14, "bold")).pack(pady=10)

    for transaction in transactions:
        Label(cadre_historique, text=f"{transaction[0]}: {transaction[1]} € le {transaction[2]}", font=("Arial", 12)).pack(pady=5)

# Interface graphique principale
fenetre = Tk()
fenetre.title("La Banque")
fenetre.minsize(400, 250)

cadre = Frame(fenetre, padx=20, pady=20)
cadre.pack()

titre = Label(cadre, text="Connexion", font=("Arial", 16, "bold"))
titre.grid(row=0, columnspan=2, pady=10)

label_email = Label(cadre, text="Email")
label_email.grid(row=1, column=0, pady=10)

expression1 = Entry(cadre, width=20)
expression1.grid(row=1, column=1)

label_motdepasse = Label(cadre, text="Mot de passe")
label_motdepasse.grid(row=2, column=0, pady=10)

expression2 = Entry(cadre, width=20, show="*")
expression2.grid(row=2, column=1)

label_erreur = Label(cadre, text="", fg="red", font=("Arial", 10))
label_erreur.grid(row=3, columnspan=2)

button_connexion = Button(cadre, text="Se connecter", command=verifier_connexion)
button_connexion.grid(row=4, columnspan=2, pady=20)

# Bouton pour ouvrir le formulaire d'inscription
button_inscription = Button(cadre, text="S'inscrire", command=afficher_formulaire_inscription)
button_inscription.grid(row=5, columnspan=2, pady=10)

fenetre.mainloop()