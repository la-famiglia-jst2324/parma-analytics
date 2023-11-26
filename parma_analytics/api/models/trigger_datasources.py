from pydantic import BaseModel
from typing import Dict, List

# ------------------------------------------------------------------------------------ #
#                                       Internal                                       #
# ------------------------------------------------------------------------------------ #


class _ApiTriggerDataSourcesBase(BaseModel):
    """Internal base model for the trigger datasources endpoints."""

    pass


class _ApiTriggerDataSourcesOutBase(_ApiTriggerDataSourcesBase):
    """Output base model for the several endpoint."""

    return_message: str


# ------------------------------------------------------------------------------------ #
#                                     Create Models                                    #
# ------------------------------------------------------------------------------------ #


class ApiTriggerDataSourcesCreateIn(_ApiTriggerDataSourcesBase):
    """Input model for the TriggerDataSources creation endpoint."""

    # the api accepts a dictionary of data_source_id as key and list of company ids as values.
    trigger_data: Dict[int, List[int]]


class ApiTriggerDataSourcesCreateOut(_ApiTriggerDataSourcesOutBase):
    """Output model for the TriggerDataSources creation endpoint."""

    pass
