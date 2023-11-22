"""
Business logic writing the reviews
"""
from typing import Any, Dict, Optional
from datetime import datetime, timedelta
from slack_sdk import WebClient


def generate_review(user: str, body, web_client: WebClient, selected_conversations, start_date, end_date):
    """
    Generates the review based on the user's criteria

    Parameters:
        user (str): The user ID from Slack
        slack_enc_team_id (str): The team ID from Slack

    Returns:
        dict: The payload for setting up review criteria
    """

    # start_date_num = datetime.strptime(start_date, "%Y-%m-%d")
    # end_date_num = datetime.strptime(end_date, "%Y-%m-%d")

    # fetch_channel_messages(web_client, user, selected_conversations, start_date_num, end_date_num)


    # combined_summary = generate_combined_summary(user, asana_data + github_data + slack_data)

    # return combined_summary
