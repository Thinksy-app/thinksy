"""
Business logic writing the reviews
"""
from typing import Any, Dict, Optional
from datetime import datetime, timedelta
from slack_sdk import WebClient

from app.slack_ops import fetch_channel_messages
from app.openai_ops import make_synchronous_openai_call


def generate_review(context, user: str, web_client: WebClient, selected_conversations, start_date, end_date):
    """
    Generates the review based on the user's criteria

    Parameters:
        user (str): The user ID from Slack
        slack_enc_team_id (str): The team ID from Slack

    Returns:
        dict: The payload for setting up review criteria
    """

    start_date_num = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_num = datetime.strptime(end_date, "%Y-%m-%d")

    slack_messages = fetch_channel_messages(web_client, user, selected_conversations, start_date_num, end_date_num)

    print(slack_messages)

    # openai_response = make_synchronous_openai_call(
    #     openai_api_key = context.get("OPENAI_API_KEY"),
    #     model=context["OPENAI_MODEL"],
    #     temperature=context["OPENAI_TEMPERATURE"],
    #     messages=slack_messages,
    #     openai_api_type=context["OPENAI_API_TYPE"],
    #     openai_api_base=context["OPENAI_API_BASE"],
    #     openai_api_version=context["OPENAI_API_VERSION"],
    #     openai_deployment_id=context["OPENAI_DEPLOYMENT_ID"],
    #     timeout_seconds=30,
    # )

    # print(openai_response)


    # combined_summary = generate_combined_summary(user, asana_data + github_data + slack_data)

    # return combined_summary
