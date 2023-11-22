import logging
import os
import json

from typing import Any, Dict, List
from slack_bolt import App, Ack, BoltContext
from slack_sdk.web import WebClient
from slack_sdk.http_retry.builtin_handlers import RateLimitErrorRetryHandler
from slack_sdk.errors import SlackApiError

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
from app.slack_ops import build_home_tab, build_channel_warning
from app.review_ops import generate_review

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


    ##
    # START: SLACK APP ROUTES
    ##

    @app.event("app_home_opened")
    def update_home_tab(client, event, logger):
        """
        Publishes view when a user opens the home tab

        Args:
            ack (Ack): A function to acknowledge the action.
            body (dict): The payload of the action request.

        Returns:
            None
        """
        try:
            client.views_publish(
                user_id=event["user"],
                view=json.dumps(build_home_tab(event["user"]))
            )
        except Exception as e:
            logger.error(f"Error publishing home tab: {e}")

    @app.action("generate-review-action")
    def handle_generate_review(client, ack: Ack, body: Dict[str, Any], context: BoltContext, logger: logging.Logger) -> None:
        """
        Handles when a user clicks the "Generate Review" button.

        Args:
            ack (Ack): A function to acknowledge the action.
            body (dict): The payload of the action request.

        Returns:
            None
        """

        ack()

        user = body['user']['id']

        try:
            client.chat_postEphemeral(
                channel=user,
                text=":saluting_face: *On it, boss! Give me a minute or two to generate your report* :hourglass_flowing_sand:",
                user=user,
            )
        except SlackApiError as e:
            logger.error(f"Error sending ephemeral message: {e}")

        selected_conversations = body["view"]["state"]["values"]["selected_conversations"]["multi_conversations_select-action"]["selected_conversations"]
        selected_user = body["view"]["state"]["values"]["selected_user"]["users_select-action"]["selected_user"]
        start_date = body["view"]["state"]["values"]["selected_start_date"]["datepicker-action"]["selected_date"]
        end_date = body["view"]["state"]["values"]["selected_end_date"]["datepicker-action"]["selected_date"]

        if not selected_conversations:
            try:
                client.chat_postEphemeral(
                    channel=user,
                    text="Please select at least 1 channel before generating a report, please :)",
                    user=user,
                )
            except SlackApiError as e:
                logger.error(f"Error sending ephemeral message: {e}")


        try:
            client.chat_postMessage(
                channel=user,
                text=json.dumps(generate_review(context, selected_user, client, selected_conversations, start_date, end_date)),
                user=user,
                unfurl_links=False
            )
        except SlackApiError as e:
            logger.error(f"Error sending review: {e}")



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

    @app.action("users_select-action")
    @app.action("multi_conversations_select-action")
    def handle_no_op_actions(ack: Ack, body: Dict[str, Any], logger: logging.Logger):
        """
        Acknowledges and logs the actions that don't need any further processing.

        Args:
            ack (Ack): A function to acknowledge the action.
            body (Dict[str, Any]): The payload of the action request.
            logger (logging.Logger): The logger object for logging.

        Returns:
            None
        """

        ack()

    ##
    # END: SLACK APP ROUTES
    ##

    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
