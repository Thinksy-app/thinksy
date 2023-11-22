import os
from typing import Optional

DEFAULT_SYSTEM_TEXT = """
    You are combining multiple summaries across slack. Prioritize including content for all three categories. Consolidate bullet points as needed. Include hyperlinks using the format:

    Categories:
    :handshake: *Collaboration:*
    • Spotlight standout collaborative efforts or mentorship examples from Slack. If there's nothing in this category, mention "There's nothing I could find :confused:"

    :computer: *Technical Quality:*
    • Highlight key instances that the user has mentioned something related to technical quality like best practices, catching bugs or things that someone might have missed, or improving a technical RFC. If there's nothing in this category, mention "There's nothing I could find :confused:"

    :rocket: *Execution:*
    • Spotlight successful launches, significant contributions, or major changes. If there's nothing in this category, mention "There's nothing we could find :confused:"

    Example (do not reuse)

    :rocket: *Execution:*
    • [Added you to lemonsqueezy](https://thinksy.slack.com/archives/C050R8QKY1Z/p1693793077294329): Taking steps to improve the payment process by switching to lemonsqueezy for better suitability.

    :handshake: *Collaboration:*
    • [Added someone to a different workspace](https://thinksy.slack.com/archives/C050R8QKY1Z/p1693792268521079?thread_ts=1693792268.521079&cid=C050R8QKY1Z): Expanding the team and involving friends to test the product.
"""
SYSTEM_TEXT = os.environ.get("OPENAI_SYSTEM_TEXT", DEFAULT_SYSTEM_TEXT)

DEFAULT_OPENAI_TIMEOUT_SECONDS = 30
OPENAI_TIMEOUT_SECONDS = int(
    os.environ.get("OPENAI_TIMEOUT_SECONDS", DEFAULT_OPENAI_TIMEOUT_SECONDS)
)

DEFAULT_OPENAI_MODEL = "gpt-3.5-turbo"
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", DEFAULT_OPENAI_MODEL)

DEFAULT_OPENAI_TEMPERATURE = 1
OPENAI_TEMPERATURE = float(
    os.environ.get("OPENAI_TEMPERATURE", DEFAULT_OPENAI_TEMPERATURE)
)

DEFAULT_OPENAI_API_TYPE: Optional[str]  = None
OPENAI_API_TYPE = os.environ.get("OPENAI_API_TYPE", DEFAULT_OPENAI_API_TYPE)

DEFAULT_OPENAI_API_BASE = "https://api.openai.com/v1"
OPENAI_API_BASE = os.environ.get("OPENAI_API_BASE", DEFAULT_OPENAI_API_BASE)

DEFAULT_OPENAI_API_VERSION: Optional[str]  = None
OPENAI_API_VERSION = os.environ.get("OPENAI_API_VERSION", DEFAULT_OPENAI_API_VERSION)

DEFAULT_OPENAI_DEPLOYMENT_ID: Optional[str]  = None
OPENAI_DEPLOYMENT_ID = os.environ.get(
    "OPENAI_DEPLOYMENT_ID", DEFAULT_OPENAI_DEPLOYMENT_ID
)

DEFAULT_OPENAI_FUNCTION_CALL_MODULE_NAME: Optional[str] = None
OPENAI_FUNCTION_CALL_MODULE_NAME = os.environ.get(
    "OPENAI_FUNCTION_CALL_MODULE_NAME", DEFAULT_OPENAI_FUNCTION_CALL_MODULE_NAME
)

USE_SLACK_LANGUAGE = os.environ.get("USE_SLACK_LANGUAGE", "true") == "true"

SLACK_APP_LOG_LEVEL = os.environ.get("SLACK_APP_LOG_LEVEL", "DEBUG")

TRANSLATE_MARKDOWN = os.environ.get("TRANSLATE_MARKDOWN", "false") == "true"

REDACTION_ENABLED = os.environ.get("REDACTION_ENABLED", "false") == "true"

# Redaction patterns
#
REDACT_EMAIL_PATTERN = os.environ.get(
    "REDACT_EMAIL_PATTERN", r"\b[A-Za-z0-9.*%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)
REDACT_PHONE_PATTERN = os.environ.get(
    "REDACT_PHONE_PATTERN", r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
)
REDACT_CREDIT_CARD_PATTERN = os.environ.get(
    "REDACT_CREDIT_CARD_PATTERN", r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b"
)
REDACT_SSN_PATTERN = os.environ.get(
    "REDACT_SSN_PATTERN", r"\b\d{3}[- ]?\d{2}[- ]?\d{4}\b"
)
# For REDACT_USER_DEFINED_PATTERN, the default will never match anything
REDACT_USER_DEFINED_PATTERN = os.environ.get("REDACT_USER_DEFINED_PATTERN", r"(?!)")