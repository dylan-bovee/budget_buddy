from cryptography.fernet import Fernet

# Générer une clé et la sauvegarder dans key.key
key = Fernet.generate_key()
with open("key.key", "wb") as key_file:
    key_file.write(key)

print("Clé de chiffrement générée avec succès !")
