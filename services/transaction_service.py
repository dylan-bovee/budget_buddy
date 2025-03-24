from db import cursor, conn
from tkinter import messagebox
from models.transaction import Transaction
from datetime import datetime

def deposit(user_id, amount, description):
    cursor.execute("UPDATE user SET solde = solde + %s WHERE id = %s", (amount, user_id))
    cursor.execute("INSERT INTO transaction (user_id, type_transaction, amount, description) VALUES (%s, %s, %s, %s)",
                   (user_id, "Dépôt", amount, description))
    cursor.execute("INSERT INTO transaction_history (user_id, transaction_type, amount, balance_after, description) VALUES (%s, %s, %s, (SELECT solde FROM user WHERE id = %s), %s)",
                   (user_id, "Dépôt", amount, user_id, description))
    conn.commit()
    messagebox.showinfo("Succès", "Dépôt effectué.")

def withdraw(user_id, amount, description):
    cursor.execute("SELECT solde FROM user WHERE id = %s", (user_id,))
    solde = cursor.fetchone()[0]
    if amount > solde:
        messagebox.showerror("Erreur", "Solde insuffisant.")
        return
    cursor.execute("UPDATE user SET solde = solde - %s WHERE id = %s", (amount, user_id))
    cursor.execute("INSERT INTO transaction (user_id, type_transaction, amount, description) VALUES (%s, %s, %s, %s)",
                   (user_id, "Retrait", amount, description))
    cursor.execute("INSERT INTO transaction_history (user_id, transaction_type, amount, balance_after, description) VALUES (%s, %s, %s, (SELECT solde FROM user WHERE id = %s), %s)",
                   (user_id, "Retrait", amount, user_id, description))
    conn.commit()
    messagebox.showinfo("Succès", "Retrait effectué.")

def transfer(user_id, amount, email_destinataire, description):
    cursor.execute("SELECT solde FROM user WHERE id = %s", (user_id,))
    solde = cursor.fetchone()[0]
    if amount > solde:
        messagebox.showerror("Erreur", "Solde insuffisant.")
        return

    cursor.execute("SELECT id FROM user WHERE email = %s", (email_destinataire,))
    result = cursor.fetchone()
    if not result:
        messagebox.showerror("Erreur", "Destinataire introuvable.")
        return
    destinataire_id = result[0]

    cursor.execute("UPDATE user SET solde = solde - %s WHERE id = %s", (amount, user_id))
    cursor.execute("UPDATE user SET solde = solde + %s WHERE id = %s", (amount, destinataire_id))
    cursor.execute("INSERT INTO transaction (user_id, type_transaction, amount, description) VALUES (%s, %s, %s, %s)",
                   (user_id, f"Transfert vers {email_destinataire}", amount, description))
    cursor.execute("INSERT INTO transaction_history (user_id, transaction_type, amount, balance_after, description) VALUES (%s, 'Transfert', %s, (SELECT solde FROM user WHERE id = %s), %s)",
                   (user_id, amount, user_id, description))
    conn.commit()
    messagebox.showinfo("Succès", f"Transfert de {amount} € à {email_destinataire}.")

def search_transactions(user_id, start_date=None, end_date=None, category=None, 
                        transaction_type=None, sort_by_amount=None):
    query = "SELECT * FROM transaction WHERE user_id = %s"
    params = [user_id]

    if start_date:
        query += " AND date >= %s"
        params.append(start_date)
    if end_date:
        query += " AND date <= %s"
        params.append(end_date)
    if category:
        query += " AND description LIKE %s"
        params.append(f"%{category}%")
    if transaction_type:
        query += " AND type_transaction = %s"
        params.append(transaction_type)

    if sort_by_amount:
        query += " ORDER BY amount " + ("ASC" if sort_by_amount == "asc" else "DESC")

    cursor.execute(query, tuple(params))
    result = cursor.fetchall()
    
    transactions = []
    for row in result:
        transaction = Transaction(
            transaction_type=row[2],
            amount=row[3],
            description=row[4],
            date=row[5]
        )
        transactions.append(transaction)
    
    return transactions