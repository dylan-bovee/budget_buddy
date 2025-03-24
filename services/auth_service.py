from db import cursor, conn
from utils.password_utils import validate_password, hash_password, check_password
from models.user import User
from tkinter import messagebox

def register_user(name, surname, email, password):
    valid, msg = validate_password(password)
    if not valid:
        messagebox.showerror("Erreur", msg)
        return False
    try:
        hashed = hash_password(password)
        cursor.execute(
            "INSERT INTO user (name, surname, email, password) VALUES (%s, %s, %s, %s)",
            (name, surname, email, hashed)
        )
        conn.commit()
        messagebox.showinfo("Succès", "Inscription réussie.")
        return True
    except:
        messagebox.showerror("Erreur", "Cet email est déjà utilisé.")
        return False

def login_user(email, password):
    cursor.execute("SELECT id, email, password, solde, name, surname FROM user WHERE email = %s", (email,))
    result = cursor.fetchone()
    if result and check_password(password, result[2]):
        return User(user_id=result[0], email=result[1], solde=result[3], name=result[4], surname=result[5])
    return None
