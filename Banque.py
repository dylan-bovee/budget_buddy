from tkinter import *

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
     label_virement.config()

    label_virement = Label(cadre_compte, text="", font=("Arial", 12), fg="blue")
    label_virement.pack(pady=5)

    cadre_bas = Frame(fenetre_solde)
    cadre_bas.pack(side="bottom", fill="x", padx=10, pady=10)

    bouton_virement = Button(cadre_bas, text="Effectuer un virement", font=("Arial", 8), command=afficher_virement)
    bouton_virement.pack(side="left")

    
      
    def afficher_historique():
     label_historique.config()

    label_historique = Label(cadre_compte, text="", font=("Arial", 12), fg="blue")
    label_historique.pack(pady=5)

    cadre_bas = Frame(fenetre_solde)
    cadre_bas.pack(side="bottom", fill="x", padx=10, pady=10)

    bouton_historique = Button(cadre_bas, text="Historique", font=("Arial", 8), command=afficher_virement)
    bouton_historique.pack(side="left")

    def retirer():
     label_retirer.config()
     label_retirer = Label()
     label_retirer.pack(pady=5)
    cadre_bas = Frame(fenetre_solde)
    cadre_bas.pack(side="bottom", fill="x", padx=10, pady=10)

    bouton_deposer = Button(cadre_bas, text="retirer", font=("Arial", 8), command=afficher_virement)
    bouton_deposer.pack(side="left")

    def deposer():
     label_deposer.config()
     label_deposer = Label()
     label_deposer.pack(pady=5)
    cadre_bas = Frame(fenetre_solde)
    cadre_bas.pack(side="bottom", fill="x", padx=10, pady=10)

    bouton_deposer = Button(cadre_bas, text="deposer", font=("Arial", 8), command=afficher_virement)
    bouton_deposer.pack(side="left")

fenetre = Tk()
fenetre.title("La Banque")
fenetre.minsize(400, 200)

cadre = Frame(fenetre, padx=20, pady=20)
cadre.pack()

titre = Label(cadre, text="Entre les codes", font=("Arial", 14, "bold"))
titre.grid(row=0, column=0, columnspan=2, pady=10)

Label(cadre, text="Identifiant:").grid(row=1, column=0, sticky=E, padx=5, pady=5)
expression1 = StringVar()
entree1 = Entry(cadre, textvariable=expression1, width=30)
entree1.grid(row=1, column=1, padx=5, pady=5)

Label(cadre, text="Mot de passe:").grid(row=2, column=0, sticky=E, padx=5, pady=5)
expression2 = StringVar()
entree2 = Entry(cadre, textvariable=expression2, width=30, show="*")
entree2.grid(row=2, column=1, padx=5, pady=5)

bouton = Button(cadre, text="Login", width=15, command=ouvrir_compte)
bouton.grid(row=3, column=0, columnspan=2, pady=10)

fenetre.mainloop()
