import csv
import hashlib

def read_users():
    with open('db/users.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            email = row['mail'].strip()
            password = hash_password(row['haslo'].strip())
            users[email] = {"password": password, "role": "operator"}
    return users

def authenticate(email, password, users_db):
    user = users_db.get(email)
    if not user:
        return None
    if user["password"] == hash_password(password):
        return user["role"]
    return None
