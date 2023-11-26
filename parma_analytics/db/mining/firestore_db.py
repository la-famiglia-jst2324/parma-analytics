import firebase_admin
import os
from firebase_admin import credentials
from firebase_admin import firestore

print(os.getenv("TYPE"))
# path where you store the firestore certificate
# secrets will be fetched via github actions
cred = credentials.Certificate("path/to/serviceAccountKey.json")
firebase_admin.initialize_app(cred)


db = firestore.client()

# write data to the db
doc_ref = db.collection("users").document("alovelace")
doc_ref.set({"first": "Ada", "last": "Lovelace", "born": 1815})

doc_ref = db.collection("users").document("aturing")
doc_ref.set({"first": "Alan", "middle": "Mathison", "last": "Turing", "born": 1912})

# read data from the db
users_ref = db.collection("users")
docs = users_ref.stream()

for doc in docs:
    print(f"{doc.id} => {doc.to_dict()}")
