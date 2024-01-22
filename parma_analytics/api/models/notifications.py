"""This module contains the models related to notifications.

The models in this module are used to represent notifications and their attributes.
"""

from pydantic import BaseModel

# ------------------------------------------------------------------------------------ #
#                                       Internal                                       #
# ------------------------------------------------------------------------------------ #


class _NotificationOut(BaseModel):
    """Internal model for representing a notification.

    Attributes:
        id (int): The ID of the notification.
        message (str): The message of the notification.
        company_id (int): The ID of the company associated with the notification.
        data_source_id (int): The ID of the data source with the notification.
    """

    id: int
    message: str
    company_id: int
    data_source_id: int


# ------------------------------------------------------------------------------------ #
#                                     Create Models                                    #
# ------------------------------------------------------------------------------------ #


class NotificationOut(_NotificationOut):
    """Output model for the Notification creation endpoint.

    Inherits from _NotificationOut.

    This model represents the data that will be returned in the response when creating a
    notification.
    """

    pass
