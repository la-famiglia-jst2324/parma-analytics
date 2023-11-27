from pydantic import BaseModel

# ------------------------------------------------------------------------------------ #
#                                       Internal                                       #
# ------------------------------------------------------------------------------------ #


class _ApiNewCompanyBase(BaseModel):
    """Internal base model for the new company endpoints."""

    id: int
    company_name: str


class _ApiNewCompanyOutBase(_ApiNewCompanyBase):
    """Output base model for the several endpoint."""

    return_message: str


# ------------------------------------------------------------------------------------ #
#                                     Create Models                                    #
# ------------------------------------------------------------------------------------ #


class ApiNewCompanyCreateIn(_ApiNewCompanyBase):
    """Input model for the NewCompany creation endpoint."""

    description: str
    added_by: str


class ApiNewCompanyCreateOut(_ApiNewCompanyOutBase):
    """Output model for the NewCompany creation endpoint."""

    pass
