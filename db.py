import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="bank"
)

cursor = conn.cursor()

def setup_database():
    cursor.execute('''CREATE TABLE IF NOT EXISTS user (
        id INT AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        name VARCHAR(255),
        surname VARCHAR(255),
        solde FLOAT DEFAULT 0.0
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS transaction (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        type_transaction VARCHAR(50),
        amount FLOAT,
        description TEXT,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES user(id)
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS transaction_history (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        transaction_type VARCHAR(50),
        amount FLOAT,
        balance_after FLOAT,
        description TEXT,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES user(id)
    )''')

    conn.commit()
