import json
import os
import firebase_admin
from firebase_admin import credentials, firestore, storage
from firebase_admin.exceptions import FirebaseError
from typing import Any


class FirestoreService:
    def __init__(self) -> None:
        try:
            firebase_admin_cert = os.environ.get("FIREBASE_ADMIN_SDK")
            if firebase_admin_cert is None:
                raise ValueError("Firebase admin certificate not found")
            firebase_admin_cert_json = json.loads(firebase_admin_cert)
            self.cred = credentials.Certificate(firebase_admin_cert_json)
            firebase_admin.initialize_app(self.cred)
            self.db = firestore.client()
            self.storage = storage.bucket()
            print("storage: ", self.storage)
        except FirebaseError as e:
            print(f"Error initializing Firebase: {e}")
            # Depending on the use case, you might want to re-raise the exception or handle it differently

    def get_next_page_number(self, data_source: str, company: str) -> int:
        company_ref = self.db.collection(data_source).document(company)

        # Fetch the last modified page number
        company_doc = company_ref.get()
        if company_doc.exists:
            company_data = company_doc.to_dict()
            last_page = company_data.get("last_modified_page")
            if last_page:
                # Extract the number from the string 'pageX' and increment it
                page_number = last_page + 1
            else:
                page_number = 1
        else:
            page_number = 0

        return page_number

    # Add a new data_source along with company without new page
    def add_new_data_source_and_company(self, data_source: str, company: str) -> bool:
        try:
            if self.check_company_exists(data_source, company):
                return True
            else:
                doc_ref = self.db.collection(data_source).document(company)
                page_id = self.get_next_page_number(data_source, company)
                page_fields = {
                    "last_modified": firestore.SERVER_TIMESTAMP,
                    "last_modified_page": page_id,
                }
                doc_ref.set(page_fields)
                return True
        except FirebaseError as e:
            print(f"Error creating new data source: {e}")
            return False

    def get_all_data_sources(self) -> list[str]:
        try:
            collections = self.db.collections()
            data_sources = [collection.id for collection in collections]
            return data_sources
        except FirebaseError as e:
            print(f"Error getting all data sources: {e}")
            return []

    def get_all_companies(self, data_source: str) -> list[str]:
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
        raw_data_content: dict[str, Any],
    ) -> bool:
        try:
            page_id = self.get_next_page_number(data_source, company)
            doc_ref = self.db.collection(data_source).document(company)
            doc_ref.set(
                {
                    "last_modified": firestore.SERVER_TIMESTAMP,
                    "last_modified_page": page_id,
                }
            )
            doc_ref.collection(page_id).document("raw_data").set(raw_data_content)
            return True
        except FirebaseError as e:
            print(f"Error adding new raw data: {e}")
            return False

    def add_normalized_schema(
        self,
        data_source: str,
        normalized_schema_content: dict[str, Any],
    ) -> bool:
        try:
            doc_ref = (
                self.db.collection(data_source)
                .document("normalized_schema")
                .collection("page0")
            )
            doc_ref.set(normalized_schema_content)
            return True
        except FirebaseError as e:
            print(f"Error adding new raw data: {e}")
            return False

    def get_normalized_schema(self, data_source: str) -> dict:
        try:
            doc_ref = self.db.collection(data_source).document("normalized_schema")

            doc = doc_ref.get()
            if doc.exists:
                return doc.to_dict()
            else:
                return {}
        except FirebaseError as e:
            print(f"An error occurred while fetching the normalized schema: {e}")
            return {}


# a:str = os.environ.get("FIREBASE_ADMINSDK_CERTIFICATE")
# #print("JSON String:", a)
# #firebase_config_json = json.dumps(a)
# service_account_info = json.loads(a)
# #print("Parsed JSON:", service_account_info)
# cred = credentials.Certificate(service_account_info)
# firebase_admin.initialize_app(cred)
# db = firestore.client()
firebase_instance = FirestoreService()
print(firebase_instance.get_all_data_sources())
