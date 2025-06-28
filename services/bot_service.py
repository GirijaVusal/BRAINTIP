from bot.core import ask_llm
from schemas import BotResponse
from utils import load_config
import requests

config = load_config()
provider = config["tool_calling_agent"]["provider"]
model = config["tool_calling_agent"]["model"]
api_key = config["apis"][provider]


class BotService:
    @staticmethod
    async def async_get_bot_response(user_query: str, use_tool: bool = True) -> dict:
        result, token_usage = await ask_llm(
            user_query, provider, model, api_key=api_key, use_tool=use_tool
        )

        if result:
            response = BotResponse(code="200", response=result, token_usage=token_usage)
        else:
            response = BotResponse(
                code="204",
                response="Currently all our services are busy, we will response you ASAP.",
            )
        return response
