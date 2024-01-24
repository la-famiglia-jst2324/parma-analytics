r"""The SlackService provides functionality to send messages and reports to Slack.

Available methods:
- send_report(user_id: int, content: str): Sends a weekly report to a user.
- send_notification(user_id: int, content: str): Sends a notification to a user.

This class also encapsulates private helper methods for tasks such as sending messages,
retrieving channel IDs, creating message blocks,
and obtaining user destination information.

Example usage:
slack_service = SlackService()
slack_service.send_report(user_id=1,
    content="Here's your weekly report:\n- Point A\n- Point B\n- Point C")
"""


import logging
from typing import Any

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from parma_analytics.reporting.notification_service_manager import (
    NotificationServiceManager,
)
from parma_analytics.vendor.secret_manager import get_client, retrieve_secret

logger = logging.getLogger(__name__)


class SlackService:
    """A class that provides functionality to send messages and reports to Slack users.

    Methods:
        send_report(user_id: int, content: str):
            Sends a weekly report to a user.
        send_notification(user_id: int, content: str):
            Sends a notification to a user.
    """

    def _get_channel_id(self, channel_name: str, client: WebClient):
        try:
            for result in client.conversations_list():
                for channel in result["channels"]:
                    if channel["name"] == channel_name:
                        return channel["id"]
            raise ValueError(f"Channel with name '{channel_name}' not found.")
        except Exception as e:
            logger.error(f"An error occurred while fetching the channel ID: {e}")

    def _send_message(
        self,
        channel_name: str,
        content: str,
        slack_api_token: str,
        blocks: list[Any] | None = None,
    ):
        """Sends a message to a Slack channel.

        Args:
            channel_name (str): The name of the Slack channel to send the message to.
            content (str): The content of the message.
            slack_api_token (str): The API token for accessing the Slack API.
            blocks (List[Any], optional): The blocks to include in the message.
        """
        try:
            slack_client = WebClient(token=slack_api_token)
            channel_id = self._get_channel_id(
                channel_name=channel_name, client=slack_client
            )
            slack_client.chat_postMessage(
                channel=channel_id, text=content, blocks=blocks
            )
        except SlackApiError as e:
            logger.error(f"Error sending report: {e.response['error']}")

    def _create_message_blocks(
        self,
        content: str,
        title: str,
    ):
        """Create message blocks for sending Slack messages.

        Args:
        content (str): The main content of the message.
        title (str): The title of the message.

        Returns:
        list: A list of message blocks.
        """
        blocks = [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": title, "emoji": True},
            },
            {
                "type": "section",  # Use a section block for the main content
                "text": {"type": "mrkdwn", "text": content},
            },
        ]
        return blocks

    def _get_user_destinations(self, user_id: int):
        """Get all user slack channels for notification or report."""
        channel_manager = NotificationServiceManager(
            service_type="slack", user_id=user_id
        )
        return channel_manager.get_slack_key_and_destinations()

    def _send_message_to_user(self, user_id: int, content: str, title: str):
        """General function to send a message to a user.

        Args:
            user_id: The ID of the user.
            content: The content of the message.
            title: The title for the message blocks.
        """
        channels_and_keys = self._get_user_destinations(user_id)
        for channel, secret_id in channels_and_keys:
            try:
                slack_api_token = retrieve_secret(get_client(), secret_id=secret_id)
            except Exception as e:
                logger.error(
                    f"Failed to retrieve secret key for secret_id {secret_id}: {e}"
                )
                continue  # Skip to the next channel
            blocks = self._create_message_blocks(content=content, title=title)
            try:
                self._send_message(
                    channel_name=channel,
                    content=content,
                    slack_api_token=slack_api_token,
                    blocks=blocks,
                )
            except Exception as e:
                logger.error(f"Failed to send message to channel {channel}: {e}")

    def send_report(self, user_id: int, content: str):
        """Send a weekly report to a user."""
        self._send_message_to_user(
            user_id=user_id, content=content, title="Your Weekly Report by Parma AI"
        )

    def send_notification(self, user_id: int, content: str):
        """Send a notification to a user."""
        self._send_message_to_user(
            user_id=user_id, content=content, title="Important Update!"
        )
