"""Business layer logic for fetch crm companies."""

from parma_analytics.db.prod.company_query import company_exists_by_name, create_company
from parma_analytics.db.prod.engine import get_session


def get_new_crm_companies_bll(user_id: int) -> str:
    """BLL for fetching new companies from the CRM."""
    # here get the companies:
    all_crm_companies: list[str] = []
    # Filter for new companies.
    with get_session() as db:
        return_message = "No new companies found in the CRM"
        new_companies = [
            company
            for company in all_crm_companies
            if not company_exists_by_name(db, company)
        ]

        # Add new companies to the DB.
        if new_companies != []:
            created_companies = [
                create_company(db, name=company, description=None, added_by=user_id)
                for company in new_companies
            ]
            # Set the return message to a string of comma separated company names.
            return_message = ", ".join([company.name for company in created_companies])

    return return_message
