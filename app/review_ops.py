"""
Business logic writing the reviews
"""
from datetime import datetime
import json
import re

from slack_sdk import WebClient

from app.env import (
    SYSTEM_TEXT,
)
from app.slack_ops import fetch_channel_messages, filter_non_membership_and_join
from app.openai_ops import make_synchronous_openai_call


def generate_review(context, user: str, web_client: WebClient, selected_conversations, start_date, end_date, logger):
    """
    Generates the review based on the user's criteria

    Parameters:
        user (str): The user ID from Slack
        slack_enc_team_id (str): The team ID from Slack

    Returns:
        dict: The payload for setting up review criteria
    """

    filter_non_membership_and_join(web_client, logger, selected_conversations)

    start_date_num = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_num = datetime.strptime(end_date, "%Y-%m-%d")

    slack_messages = fetch_channel_messages(web_client, user, selected_conversations, start_date_num, end_date_num)

    messages = [
                {
                "role": "system",
                "content": SYSTEM_TEXT
                },
                {
                "role": "user",
                "content": json.dumps(slack_messages),
                },
            ]

    openai_response = make_synchronous_openai_call(
        openai_api_key = context.get("OPENAI_API_KEY"),
        model=context["OPENAI_MODEL"],
        temperature=context["OPENAI_TEMPERATURE"],
        messages=messages,
        openai_api_type=context["OPENAI_API_TYPE"],
        openai_api_base=context["OPENAI_API_BASE"],
        openai_api_version=context["OPENAI_API_VERSION"],
        openai_deployment_id=context["OPENAI_DEPLOYMENT_ID"],
        timeout_seconds=30,
    )

    content = openai_response["choices"][0]["message"]["content"]
    slack_formatted_content = markdown_to_slack(content)

    return slack_formatted_content


def markdown_to_slack(markdown_text: str) -> str:
    """
    Converts markdown text to Slack formatting.

    Args:
        markdown_text (str): The input markdown text.

    Returns:
        str: The Slack formatted text.
    """

    # Bold: **text** to *text*
    slack_text = re.sub(r'\*\*(.*?)\*\*', r'*\1*', markdown_text)

    # Links: [text](url) to <url|text>
    slack_text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<\2|\1>', slack_text)

    return slack_text
