from pydantic import BaseModel

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

    # api expects a dict mapping from data_source_id to a list of company_ids
    trigger_data: dict[int, list[int]]


class ApiTriggerDataSourcesCreateOut(_ApiTriggerDataSourcesOutBase):
    """Output model for the TriggerDataSources creation endpoint."""

    pass
