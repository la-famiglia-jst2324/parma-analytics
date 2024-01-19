from pydantic import BaseModel


# ------------------------------------------------------------------------------------ #
#                                       Internal                                       #
# ------------------------------------------------------------------------------------ #

class _NotificationOut(BaseModel):
    id: int
    message: str
    company_id: int
    data_source_id: int
    

# ------------------------------------------------------------------------------------ #
#                                     Create Models                                    #
# ------------------------------------------------------------------------------------ #

class NotificationOut(_NotificationOut):
    """Output model for the Notification creation endpoint."""

    pass