from typing import List, Dict, Union

import openai
from openai.openai_object import OpenAIObject
from app.openai_constants import (
    MAX_TOKENS,
)


def make_synchronous_openai_call(
    *,
    openai_api_key: str,
    model: str,
    temperature: float,
    messages,
    openai_api_type: str,
    openai_api_base: str,
    openai_api_version: str,
    openai_deployment_id: str,
    timeout_seconds: int,
) -> OpenAIObject:
    return openai.ChatCompletion.create(
        api_key=openai_api_key,
        model=model,
        messages=messages,
        top_p=1,
        n=1,
        max_tokens=MAX_TOKENS,
        temperature=temperature,
        presence_penalty=0,
        frequency_penalty=0,
        logit_bias={},
        stream=False,
        api_type=openai_api_type,
        api_base=openai_api_base,
        api_version=openai_api_version,
        deployment_id=openai_deployment_id,
        request_timeout=timeout_seconds,
    )
