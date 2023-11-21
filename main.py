import logging
import os

from slack_bolt import App, BoltContext
from slack_sdk.web import WebClient
from slack_sdk.http_retry.builtin_handlers import RateLimitErrorRetryHandler

#from app.bolt_listeners import before_authorize, register_listeners
from app.env import (
    USE_SLACK_LANGUAGE,
    SLACK_APP_LOG_LEVEL,
    OPENAI_MODEL,
    OPENAI_TEMPERATURE,
    OPENAI_API_TYPE,
    OPENAI_API_BASE,
    OPENAI_API_VERSION,
    OPENAI_DEPLOYMENT_ID,
    OPENAI_FUNCTION_CALL_MODULE_NAME,
)
#from app.slack_ops import build_home_tab

if __name__ == "__main__":
    from slack_bolt.adapter.socket_mode import SocketModeHandler

    logging.basicConfig(level=SLACK_APP_LOG_LEVEL)

    #
    # Initiates the SlackBolt app based on provided App credentials
    #
    app = App(
        token=os.environ.get("SLACK_BOT_TOKEN"),
    )
    app.client.retry_handlers.append(RateLimitErrorRetryHandler(max_retry_count=2))

    #register_listeners(app)

    ##
    # START: SLACK APP ROUTES
    ##

    @app.event("app_home_opened")
    def update_home_tab(client, event, logger):
        try:
            # views.publish is the method that your app uses to push a view to the Home tab
            client.views_publish(
            # the user that opened your app's app home
            user_id=event["user"],
            # the view object that appears in the app home
            view={
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
                            "action_id": "users_select-action"
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
                            "action_id": "multi_conversations_select-action"
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
                            "initial_date": "1990-04-28",
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
                            "initial_date": "1990-04-28",
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
                                "value": "click_me_123",
                                "action_id": "actionId-0"
                            }
                        ]
                    }
                ]

            }
            )

        except Exception as e:
            logger.error(f"Error publishing home tab: {e}")

    @app.middleware
    def set_openai_api_key(context: BoltContext, next_):
        context["OPENAI_API_KEY"] = os.environ["OPENAI_API_KEY"]
        context["OPENAI_MODEL"] = OPENAI_MODEL
        context["OPENAI_TEMPERATURE"] = OPENAI_TEMPERATURE
        context["OPENAI_API_TYPE"] = OPENAI_API_TYPE
        context["OPENAI_API_BASE"] = OPENAI_API_BASE
        context["OPENAI_API_VERSION"] = OPENAI_API_VERSION
        context["OPENAI_DEPLOYMENT_ID"] = OPENAI_DEPLOYMENT_ID
        context["OPENAI_FUNCTION_CALL_MODULE_NAME"] = OPENAI_FUNCTION_CALL_MODULE_NAME
        next_()


    ##
    # END: SLACK APP ROUTES
    ##

    print("socket starting")
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
