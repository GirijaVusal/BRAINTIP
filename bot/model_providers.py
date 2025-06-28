from typing import Callable, Dict
from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI


# Allowed models per provider
ALLOWED_MODELS: Dict[str, list[str]] = {
    "groq": [
        "llama-3.3-70b-versatile",
        "mixtral-8x7b",
        "llama3-8b-8192",
        "gemma2-9b-it",
    ],
    "openai": ["gpt-4o", "gpt-4-turbo"],
    "ollama": ["llama3-groq-tool-use:8b", "llama3.2:3b", "gemma3:12b"],
    "local": ["llama3-groq-tool-use:8b", "llama3.2:3b", "gemma3:12b"],
}


# Factory functions
def groq_factory(model: str, temperature: int, api_key: str):
    return ChatGroq(model=model, temperature=temperature, api_key=api_key)


def openai_factory(model: str, temperature: int, api_key: str):
    return ChatOpenAI(model=model, temperature=temperature, api_key=api_key)


# def anthropic_factory(model: str, temperature=0):
#     return ChatAnthropic(model=model, temperature=temperature)


def ollama_factory(model: str, temperature: int, api_key: str = None):
    return ChatOllama(model=model, temperature=temperature)


# Mapping from provider name to factory function
FACTORY_MAP: Dict[str, Callable[[str], object]] = {
    "groq": groq_factory,
    "openai": openai_factory,
    "ollama": ollama_factory,
    "local": ollama_factory,
}


async def acall_llm(model_provider: str, model: str, temperature: int, api_key: str):
    if model_provider not in FACTORY_MAP:
        raise ValueError(f"Unsupported model provider: {model_provider}")

    if model not in ALLOWED_MODELS.get(model_provider, []):
        raise ValueError(
            f"Model '{model}' is not valid for provider '{model_provider}'"
        )
    if api_key is None and model_provider not in ["ollama", "local"]:
        raise ValueError(
            f"""Please prove api key in call_llm functon  like call_llm(...,api_key="Your api key") to access {model_provider}"""
        )
    factory_func = FACTORY_MAP[model_provider]
    return factory_func(model, temperature, api_key)


def call_llm(model_provider: str, model: str, temperature: int, api_key: str):
    if model_provider not in FACTORY_MAP:
        raise ValueError(f"Unsupported model provider: {model_provider}")

    if model not in ALLOWED_MODELS.get(model_provider, []):
        raise ValueError(
            f"Model '{model}' is not valid for provider '{model_provider}'"
        )
    if api_key is None and model_provider not in ["ollama", "local"]:
        raise ValueError(
            f"""Please prove api key in call_llm functon  like call_llm(...,api_key="Your api key") to access {model_provider}"""
        )
    factory_func = FACTORY_MAP[model_provider]
    return factory_func(model, temperature, api_key)
