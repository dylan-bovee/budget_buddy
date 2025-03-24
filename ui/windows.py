from tkinter import *
from tkinter import ttk 
from tkinter import Tk
from services.auth_service import login_user, register_user
from services.transaction_service import deposit, withdraw, transfer
from db import cursor
from models.transaction import Transaction
from tkinter import messagebox
from services.transaction_service import search_transactions
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime

def create_main_window():
    window = Tk()
    window.title("Budget Buddy")
    window.minsize(400, 250)

    frame = Frame(window, padx=20, pady=20)
    frame.pack()

    Label(frame, text="Email").grid(row=0, column=0)
    email_entry = Entry(frame, width=25)
    email_entry.grid(row=0, column=1)

    Label(frame, text="Mot de passe").grid(row=1, column=0)
    password_entry = Entry(frame, show="*", width=25)
    password_entry.grid(row=1, column=1)

    msg_label = Label(frame, text="", fg="red")
    msg_label.grid(row=2, columnspan=2)

    def try_login():
        user = login_user(email_entry.get(), password_entry.get())
        if user:
            open_account_window(user)
        else:
            msg_label.config(text="Identifiants incorrects.")

    Button(frame, text="Se connecter", command=try_login).grid(row=3, columnspan=2, pady=10)
    Button(frame, text="S'inscrire", command=lambda: open_register_window()).grid(row=4, columnspan=2)

    window.mainloop()

def open_register_window():
    win = Toplevel()
    win.title("Inscription")

    entries = {}

    for i, label in enumerate(["Nom", "Prénom", "Email", "Mot de passe", "Confirmation"]):
        Label(win, text=label).pack()
        entry = Entry(win, show="*" if "Mot" in label else None)
        entry.pack()
        entries[label] = entry

    def submit():
        if entries["Mot de passe"].get() != entries["Confirmation"].get():
            messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas.")
            return
        register_user(entries["Prénom"].get(), entries["Nom"].get(), entries["Email"].get(), entries["Mot de passe"].get())

    Button(win, text="S'inscrire", command=submit).pack(pady=10)

def open_account_window(user):
    win = Toplevel()
    win.title("Mon Compte")

    Label(win, text=f"Bienvenue {user.name} {user.surname}").pack(pady=5)
    Label(win, text=f"Solde : {user.solde} €").pack(pady=5)

    Button(win, text="Déposer", command=lambda: open_amount_window(user.id, "deposit")).pack(pady=2)
    Button(win, text="Retirer", command=lambda: open_amount_window(user.id, "withdraw")).pack(pady=2)
    Button(win, text="Transférer", command=lambda: open_transfer_window(user.id)).pack(pady=2)
    Button(win, text="Historique", command=lambda: show_history(user.id)).pack(pady=2)
    Button(win, text="Rechercher Transactions", command=lambda: open_search_window(user.id)).pack(pady=2)
    Button(win, text="📊 Tableau de Bord", command=lambda: open_dashboard(user.id)).pack(pady=2)



def open_amount_window(user_id, action):
    win = Toplevel()
    win.title("Montant")

    Label(win, text="Montant :").pack()
    entry = Entry(win)
    entry.pack()

    Label(win, text="Description :").pack()
    desc_entry = Entry(win)
    desc_entry.pack()

    def process():
        try:
            amt = float(entry.get())
            if action == "deposit":
                deposit(user_id, amt, desc_entry.get())
            else:
                withdraw(user_id, amt, desc_entry.get())
            win.destroy()
        except:
            messagebox.showerror("Erreur", "Montant invalide.")

    Button(win, text="Valider", command=process).pack()

def open_transfer_window(user_id):
    win = Toplevel()
    win.title("Transfert")

    Label(win, text="Email du destinataire :").pack()
    email_entry = Entry(win)
    email_entry.pack()

    Label(win, text="Montant :").pack()
    amount_entry = Entry(win)
    amount_entry.pack()

    Label(win, text="Description :").pack()
    desc_entry = Entry(win)
    desc_entry.pack()

    def send():
        try:
            amt = float(amount_entry.get())
            transfer(user_id, amt, email_entry.get(), desc_entry.get())
            win.destroy()
        except:
            messagebox.showerror("Erreur", "Montant invalide.")

    Button(win, text="Envoyer", command=send).pack()

def show_history(user_id):
    win = Toplevel()
    win.title("Historique")

    cursor.execute("SELECT type_transaction, amount, description, date FROM transaction WHERE user_id = %s ORDER BY date DESC", (user_id,))
    rows = cursor.fetchall()

    for t in rows:
        Label(win, text=f"{t[0]}: {t[1]} € | {t[2]} | {t[3]}").pack()
def open_search_window(user_id):
    win = Toplevel()
    win.title("Recherche de Transactions")

    # Champs de recherche
    Label(win, text="Date de début (YYYY-MM-DD) :").grid(row=0, column=0)
    start_date_entry = Entry(win)
    start_date_entry.grid(row=0, column=1)

    Label(win, text="Date de fin (YYYY-MM-DD) :").grid(row=1, column=0)
    end_date_entry = Entry(win)
    end_date_entry.grid(row=1, column=1)

    Label(win, text="Catégorie (ex: repas, loisir) :").grid(row=2, column=0)
    category_entry = Entry(win)
    category_entry.grid(row=2, column=1)

    Label(win, text="Type de transaction :").grid(row=3, column=0)
    transaction_type_entry = Entry(win)
    transaction_type_entry.grid(row=3, column=1)

    Label(win, text="Trier par montant :").grid(row=4, column=0)
    sort_by_var = StringVar(value="None")
    sort_by_dropdown = ttk.Combobox(win, textvariable=sort_by_var, values=["None", "asc", "desc"])
    sort_by_dropdown.grid(row=4, column=1)

    # Zone d'affichage des résultats
    result_frame = Frame(win)
    result_frame.grid(row=6, column=0, columnspan=2, pady=10)

    result_tree = ttk.Treeview(result_frame, columns=("Type", "Montant", "Description", "Date"), show="headings")
    result_tree.heading("Type", text="Catégorie")
    result_tree.heading("Montant", text="Montant (€)")
    result_tree.heading("Description", text="Date")
    result_tree.heading("Date", text="Type")
    result_tree.pack()

    def search():
        # Récupérer les valeurs saisies par l'utilisateur
        start_date = start_date_entry.get() or None
        end_date = end_date_entry.get() or None
        category = category_entry.get() or None
        transaction_type = transaction_type_entry.get() or None
        sort_by = sort_by_var.get()
        sort_by = None if sort_by == "None" else sort_by

        # Exécuter la recherche
        transactions = search_transactions(user_id, start_date, end_date, category, transaction_type, sort_by)

        # Effacer les résultats précédents
        for row in result_tree.get_children():
            result_tree.delete(row)

        # Afficher les nouveaux résultats
        for t in transactions:
            result_tree.insert("", "end", values=(t.transaction_type, t.amount, t.description, t.date))

    # Bouton de recherche
    Button(win, text="Rechercher", command=search).grid(row=5, column=0, columnspan=2, pady=5)
def open_dashboard(user_id):
    win = Toplevel()
    win.title("Tableau de Bord")

    # Récupérer le solde actuel
    cursor.execute("SELECT solde FROM user WHERE id = %s", (user_id,))
    solde = cursor.fetchone()[0]

    # Récupérer les transactions du dernier mois
    today = datetime.date.today()
    first_day = today.replace(day=1)
    cursor.execute("""
        SELECT type_transaction, SUM(amount) 
        FROM transaction 
        WHERE user_id = %s AND date >= %s 
        GROUP BY type_transaction
    """, (user_id, first_day))
    
    transactions = cursor.fetchall()
    depenses = {t[0]: t[1] for t in transactions}

    # Affichage des informations
    Label(win, text=f"Solde Actuel : {solde:.2f} €", font=("Arial", 14, "bold")).pack(pady=10)
    
    # Vérifier si découvert
    if solde < 0:
        messagebox.showwarning("Attention !", "Vous êtes en découvert !")

    # Tableau des dépenses
    frame = Frame(win)
    frame.pack(pady=10)
    
    tree = ttk.Treeview(frame, columns=("Type", "Montant"), show="headings")
    tree.heading("Type", text="Type de transaction")
    tree.heading("Montant", text="Montant (€)")
    
    for type_transaction, amount in depenses.items():
        tree.insert("", "end", values=(type_transaction, f"{amount:.2f} €"))
    
    tree.pack()

    #Vérifier si on a des données pour éviter une erreur
    if depenses:
        # Création du graphique
        fig, ax = plt.subplots(figsize=(5, 5))  # Taille du graphique
        ax.pie(depenses.values(), labels=depenses.keys(), autopct='%1.1f%%', startangle=90)
        ax.set_title("Répartition des Dépenses")

        # Intégrer Matplotlib à Tkinter
        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)

    Button(win, text="Fermer", command=win.destroy).pack(pady=10)
