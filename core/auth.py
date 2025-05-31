import csv
import hashlib

def hash_password(raw_password):
    return hashlib.sha1(raw_password.encode()).hexdigest()

def load_users_from_csv(path="db/users.csv"):
    users = {}
    with open(path, newline='', encoding='UTF-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
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
