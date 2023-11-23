"""
Business logic writing the reviews
"""
from typing import Any, Dict, Optional
from datetime import datetime, timedelta
import json
import re

from slack_sdk import WebClient

from app.slack_ops import fetch_channel_messages, filter_non_membership_and_join
from app.openai_ops import make_synchronous_openai_call

# DEFAULT_SYSTEM_TEXT = """
#     You are combining multiple summaries across slack. Prioritize including content for all three categories. Consolidate bullet points as needed. Include hyperlinks using the format:

#     Categories:
#     :handshake: *Collaboration:*
#     • Spotlight standout collaborative efforts or mentorship examples from Slack. If there's nothing in this category, mention "There's nothing I could find :confused:"

#     :computer: *Technical Quality:*
#     • Highlight key instances that the user has mentioned something related to technical quality like best practices, catching bugs or things that someone might have missed, or improving a technical RFC. If there's nothing in this category, mention "There's nothing I could find :confused:"

#     :rocket: *Execution:*
#     • Spotlight successful launches, significant contributions, or major changes. If there's nothing in this category, mention "There's nothing we could find :confused:"

#     Example (do not reuse)

#     :rocket: *Execution:*
#     • [Added you to lemonsqueezy](https://thinksy.slack.com/archives/C050R8QKY1Z/p1693793077294329): Taking steps to improve the payment process by switching to lemonsqueezy for better suitability.

#     :handshake: *Collaboration:*
#     • [Added someone to a different workspace](https://thinksy.slack.com/archives/C050R8QKY1Z/p1693792268521079?thread_ts=1693792268.521079&cid=C050R8QKY1Z): Expanding the team and involving friends to test the product.
# """

DEFAULT_SYSTEM_TEXT = """

Assess the individual's performance by reviewing their Slack conversations. Prioritize content for all three categories: Collaboration, Technical Quality, and Execution. Consolidate bullet points as needed for clarity and brevity. Please include hyperlinks in this format.

Please ensure to double-check your work for accuracy and completeness.

:handshake: Collaboration:
• Highlight exceptional collaborative efforts or mentorship moments with specific Slack conversation links. If there's nothing in this category, mention "No relevant content found :confused:"

:computer: Technical Quality:
• Identify instances where the user discussed technical quality aspects (e.g., best practices, bug identification, RFC improvements) and provide hyperlinks to relevant discussions. If there's nothing in this category, mention "No relevant content found :confused:"

:rocket: Execution:
• Showcase successful launches, significant contributions, or major changes discussed in Slack with specific conversation links. If there's nothing in this category, mention "No relevant content found :confused:"
"""

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
                "content": DEFAULT_SYSTEM_TEXT
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
