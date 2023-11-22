from typing import Any, Dict, Optional
from datetime import datetime, timedelta

from slack_sdk.errors import SlackApiError
from slack_sdk import WebClient

def build_home_tab() -> Dict[str, Any]:

    # Calculate 1 week ago from today
    one_week_ago = datetime.now() - timedelta(days=7)
    start_date = one_week_ago.strftime("%Y-%m-%d")

    # Get today's date
    end_date = datetime.now().strftime("%Y-%m-%d")

    return {
        "type": "home",
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "💡 Run a Review"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "User to review"
                },
                "accessory": {
                    "type": "users_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select a user",
                        "emoji": True
                    },
                    "action_id": "users_select-action",
                    "filter": {
                        "exclude_bot_users": True
                    }
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Channels to review"
                },
                "accessory": {
                    "type": "multi_conversations_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select channels",
                        "emoji": True
                    },
                    "action_id": "multi_conversations_select-action",
                    "filter": {
                        "include": [
                            "public",
                            "private"
                        ]
                    },
                    "confirm": {
                        "title": {
                            "type": "plain_text",
                            "text": "Warning"
                        },
                        "text": {
                            "type": "plain_text",
                            "text": "If I am not in any of these channels already I will add myself once this report is generated."
                        },
                        "confirm": {
                            "type": "plain_text",
                            "text": "Ok"
                        },
                    }
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "📅 *Time Range:*"
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "plain_text",
                        "text": "Default: Last week",
                        "emoji": True
                    }
                ]
            },
            {
                "type": "input",
                "element": {
                    "type": "datepicker",
                    "initial_date": start_date,
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select a date",
                        "emoji": True
                    },
                    "action_id": "datepicker-action"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Start Date",
                    "emoji": True
                }
            },
            {
                "type": "input",
                "element": {
                    "type": "datepicker",
                    "initial_date": end_date,
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select a date",
                        "emoji": True
                    },
                    "action_id": "datepicker-action"
                },
                "label": {
                    "type": "plain_text",
                    "text": "End Date",
                    "emoji": True
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "style": "primary",
                        "text": {
                            "type": "plain_text",
                            "text": "Generate review",
                            "emoji": True
                        },
                        "action_id": "generate-review-action"
                    }
                ]
            }
        ]

    }


def filter_non_membership_and_join(client, logger, selected_conversations: list[str]):
    """
    Joins the channel that Thinksy is not already a member of

    Args:
        client (WebClient): The Slack WebClient instance.
        channel_id (str): The ID of the channel from which to fetch messages.
        limit (int, optional): The maximum number of messages to fetch. Defaults to 100.

    Returns:
        list: A list of message dictionaries.
    """
    conversations_bot_is_not_in: list[str] = []

    for conversation in selected_conversations:
        print(conversation)
        try:
            response = client.conversations_info(channel=conversation)
            print(response)
            if not response["channel"]["is_member"]:
                conversations_bot_is_not_in.append(conversation)
        except SlackApiError as e:
            logger.error(f"Error fetching channel review: {e}")

    for to_join_conversation in conversations_bot_is_not_in:
        try:
            response = client.conversations_join(
                channel=to_join_conversation,
            )
            print(response)
        except SlackApiError as e:
            logger.error(f"Error showing warning: {e}")

def fetch_channel_messages(
    client: WebClient,
    user: WebClient,
    conversations: list[str],
    start_date: datetime,
    end_date: datetime,
    limit: int = 100
):
    """
    Fetches messages from a Slack channel

    Args:
        client (WebClient): The Slack WebClient instance.
        channel_id (str): The ID of the channel from which to fetch messages.
        limit (int, optional): The maximum number of messages to fetch. Defaults to 100.

    Returns:
        list: A list of message dictionaries.
    """

    # result = []
    # for conversation_id in conversations:
    #     try:
    #         response = web_client_user.conversations_history(
    #             channel=channel_id,
    #             limit=limit,
    #             user=user.slack_enc_id,
    #             latest=str(end_date.timestamp()) + "00000",
    #             oldest=str(start_date.timestamp()) + "00000",
    #         )
    #         messages = response["messages"]

    #         for message in messages:
    #             if message.get("user") == user.slack_enc_id:
    #                 text = message.get("text", "")
    #                 link = web_client.chat_getPermalink(
    #                     channel=channel_id,
    #                     message_ts=message.get("ts", "")
    #                 )
    #                 url = link.get("permalink", "")
    #                 result.append({"text": text, "url": url})


    #     except SlackApiError as exception:
    #         print(exception)

    # return result

def build_channel_warning(selected_conversations: list[str]):

    formatted_conversations = '\n'.join(f'<#{x}>' for x in selected_conversations)
    return {
        "type": "modal",
        "title": {
            "type": "plain_text",
            "text": "⚠️ Missing Channel ",
            "emoji": True
        },
        "submit": {
            "type": "plain_text",
            "text": "Go ahead! :grin:",
            "emoji": True
        },
        "close": {
            "type": "plain_text",
            "text": "Cancel",
            "emoji": True
        },
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "In order to read messages from these channels I need to be added."
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Are you okay with me adding myself to the following channels?"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": formatted_conversations
                }
            }
        ]
    }


# def generate_slack_summary(messages: list[str]) -> str:
#     """
#     Generates a summary of a user's Slack messages.

#     Args:
#         messages (list[str]): List of Slack messages.

#     Returns:
#         str: The generated summary.
#     """

#     system_msg = '''
#     You are an app tasked with identifying and highlighting the highest impact contributions from a software engineer's work based on messages they've sent in their company Slack. Prioritize including content for all three categories within token limits.

#     Categories:
#     :handshake: *Collaboration:*
#     • Spotlight standout collaborative efforts or mentorship examples from Slack. If there's nothing in this category, mention "There's nothing I could find :confused:"

#     :computer: *Technical Quality:*
#     • Highlight key instances that the user has mentioned something related to technical quality like best practices, catching bugs or things that someone might have missed, or improving a technical RFC. If there's nothing in this category, mention "There's nothing I could find :confused:"

#     :rocket: *Execution:*
#     • Spotlight successful launches, significant contributions, or major changes. If there's nothing in this category, mention "There's nothing we could find :confused:"

#     Remember to include a link to the slack message for each highlighted contribution (only for items that showcase the categories).

#     Example (Do not reuse):

#     :rocket: *Execution:*
#     • [Launched Thinksy to 5 customers](https://domain.slack.com/archives/C050R8QKY1Z/p1693792268521079)

#     :handshake: *Collaboration:*
#     • [Backend Mentorship](https://domain.slack.com/archives/D059DCQNW2U/p1694817789390089): Supported new hires by mentoring them in Q3 BE mentorship program

#     :computer: *Technical Quality:*
#     • [Example Technical Quality Title](https://domain.slack.com/archives/D059DCQNW2U/p1694817439941899): Technical quality highlight here.
#     '''

#     # return generate_summary(messages, system_msg)
