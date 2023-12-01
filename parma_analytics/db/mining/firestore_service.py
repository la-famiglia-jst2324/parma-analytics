import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class FirestoreService:
    def __init__(self):
        self.cred = credentials.Certificate(
            "../../../.secrets/la-famiglia-parma-ai.json"
        )
        firebase_admin.initialize_app(self.cred)
        self.db = firestore.client()

    def create_new_data_source(self, data_source, company, page_id):
        doc_ref = self.db.collection(data_source).document(company)
        doc_ref.set(page_id)

    def get_all_companies(self, data_source):
        companies = []
        # Query the collection
        companies_ref = self.db.collection(data_source)
        docs = companies_ref.stream()

        for doc in docs:
            company = doc.to_dict()
            company["id"] = doc.id  # might want to include the page ID as well
            companies.append(company)

        return companies

    def add_new_raw_data(self, data_source, company, page_id, raw_data_content):
        doc_ref = (
            self.db.collection(data_source)
            .document(company)
            .collection(page_id)
            .document("raw_data")
        )
        doc_ref.set(raw_data_content)

    def add_new_normalized_data(
        self, data_source, company, page_id, normalized_data_content
    ):
        doc_ref = (
            self.db.collection(data_source)
            .document(company)
            .collection(page_id)
            .document("normalized_data")
        )
        doc_ref.set(normalized_data_content)
