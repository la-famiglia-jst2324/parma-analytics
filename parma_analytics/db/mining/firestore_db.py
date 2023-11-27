import firebase_admin
import os
from firebase_admin import credentials
from firebase_admin import firestore
import json

# dotenv loads all the variables found as environment variables. Imp while debugging.
from dotenv import load_dotenv

load_dotenv()


def get_firebase_config():
    private_key = os.environ.get("FIREBASE_PRIVATE_KEY")
    if private_key:
        private_key = private_key.replace("\\n", "\n")
    firebase_config = {
        "type": os.environ.get("FIREBASE_TYPE"),
        "project_id": os.environ.get("FIREBASE_PROJECT_ID"),
        "private_key_id": os.environ.get("FIREBASE_PRIVATE_KEY_ID"),
        "private_key": private_key,
        "client_email": os.environ.get("FIREBASE_CLIENT_EMAIL"),
        "client_id": os.environ.get("FIREBASE_CLIENT_ID"),
        "auth_uri": os.environ.get("FIREBASE_AUTH_URI"),
        "token_uri": os.environ.get("FIREBASE_TOKEN_URI"),
        "auth_provider_x509_cert_url": os.environ.get(
            "FIREBASE_AUTH_PROVIDER_X509_CERT_URL"
        ),
        "client_x509_cert_url": os.environ.get("FIREBASE_CLIENT_X509_CERT_URL"),
        "universe_domain": os.environ.get("FIREBASE_UNIVERSE_DOMAIN"),
    }
    return firebase_config


firebase_config_json = json.dumps(get_firebase_config())

service_account_info = json.loads(firebase_config_json)

cred = credentials.Certificate(service_account_info)

firebase_admin.initialize_app(cred)

db = firestore.client()

# write data to the db
doc_ref = db.collection("users").document("parma")
doc_ref.set({"first": "parma", "last": "analytics", "born": 2023})

doc_ref = db.collection("users").document("parma-")
doc_ref.set({"first": "parma", "middle": "", "last": "web", "born": 2023})

# read data from the db
users_ref = db.collection("users")
docs = users_ref.stream()

for doc in docs:
    print(f"{doc.id} => {doc.to_dict()}")
