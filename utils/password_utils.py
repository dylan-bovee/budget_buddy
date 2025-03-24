import bcrypt
import re

def validate_password(password):
    if len(password) < 10:
        return False, "Le mot de passe doit contenir au moins 10 caractères."
    if not re.search("[a-z]", password):
        return False, "Au moins une minuscule requise."
    if not re.search("[A-Z]", password):
        return False, "Au moins une majuscule requise."
    if not re.search("[0-9]", password):
        return False, "Au moins un chiffre requis."
    if not re.search("[@#$%^&+=]", password):
        return False, "Au moins un caractère spécial requis."
    return True, ""

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
