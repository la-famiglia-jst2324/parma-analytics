import json
import os
from pickle import NONE
import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin.exceptions import FirebaseError
from typing import List, Dict, Any


class FirestoreService:
    def __init__(self) -> None:
        try:
            firebase_admin_cert = os.environ.get("FIREBASE_ADMINSDK_CERTIFICATE")
            if firebase_admin_cert is None:
                raise ValueError("Firebase admin certificate not found")
            firebase_admin_cert_json = json.loads(firebase_admin_cert)
            self.cred = credentials.Certificate(firebase_admin_cert_json)
            firebase_admin.initialize_app(self.cred)
            self.db = firestore.client()
        except FirebaseError as e:
            print(f"Error initializing Firebase: {e}")
            # Depending on the use case, you might want to re-raise the exception or handle it differently

    def add_new_data_source_and_company(
        self, data_source: str, company: str, page_id: Dict[str, Any]
    ) -> None:
        try:
            doc_ref = self.db.collection(data_source).document(company)
            doc_ref.set(page_id)
        except FirebaseError as e:
            print(f"Error creating new data source: {e}")

    def get_all_data_sources(self) -> List[str]:
        try:
            collections = self.db.collections()
            data_sources = [collection.id for collection in collections]
            return data_sources
        except FirebaseError as e:
            print(f"Error getting all data sources: {e}")
            return []

    def get_all_companies(self, data_source: str) -> List[str]:
        companies = []
        try:
            companies_ref = self.db.collection(data_source)
            docs = companies_ref.stream()
            for doc in docs:
                companies.append(doc.id)
        except FirebaseError as e:
            print(f"Error getting all companies: {e}")
        return companies

    def check_company_exists(self, data_source: str, company: str) -> bool:
        try:
            doc_ref = self.db.collection(data_source).document(company)
            doc = doc_ref.get()
            return doc.exists
        except FirebaseError as e:
            print(f"Error checking if company exists: {e}")
            return False

    def add_new_raw_data(
        self,
        data_source: str,
        company: str,
        page_id: str,
        raw_data_content: Dict[str, Any],
    ) -> None:
        try:
            doc_ref = (
                self.db.collection(data_source)
                .document(company)
                .collection(page_id)
                .document("raw_data")
            )
            doc_ref.set(raw_data_content)
        except FirebaseError as e:
            print(f"Error adding new raw data: {e}")
