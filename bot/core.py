from langchain_core.output_parsers import StrOutputParser
from typing import List
from langchain_core.callbacks import get_usage_metadata_callback
from langchain_core.runnables import RunnableLambda

from bot.model_providers import acall_llm
from bot.tools_registry import tool_directory, required_keys
from utils import load_config

config = load_config()


async def general_chat(query: str, temperature: int):
    content = config["general_chat"]["prompt"].format(query)
    model_provider = config["general_chat"]["provider"]
    model = config["general_chat"]["model"]
    api_key = config["apis"][model_provider]
    with get_usage_metadata_callback() as cb:
        llm = await acall_llm(model_provider, model, temperature, api_key)
        chain = llm | StrOutputParser()
        result = await chain.ainvoke(content)
    token_usage = cb.usage_metadata
    token_usage["model_provider"] = model_provider
    return result, token_usage


async def humanize_tool_response(query, result, conf_key, temperature, api_key):
    content = config[conf_key]["prompt"].format(query, result)
    model_provider = config[conf_key]["provider"]
    model = config[conf_key]["model"]

    with get_usage_metadata_callback() as cb:
        llm = await acall_llm(model_provider, model, temperature, api_key)
        chain = llm | StrOutputParser()
        result = await chain.ainvoke(content)

    token_usage = cb.usage_metadata
    token_usage["model_provider"] = model_provider
    # total_token_used.append(token_usage)
    return result, token_usage


async def chat(
    query: str,
    model_provider: str,
    model: str,
    tools_conf: List = None,
    temperature: int = 0,
    api_key: str = None,
):
    if tools_conf is None:
        result, token_usage = await general_chat(
            query, model_provider, model, temperature, api_key
        )
        return result, [token_usage]

    total_token_used = []
    # getting all requied variable from tool config
    tool_functions = tools_conf["tool_functions"]
    tools = tools_conf["tools"]
    conf_key = tools_conf["prompt"]  # this is the key name in cofig.yml file

    # llm = await acall_llm(model_provider, model, temperature, api_key)
    # llm_with_tools = llm.bind_tools(tools)

    # tool_calling_chain = (
    #     llm_with_tools
    #     | RunnableLambda(lambda output: output.tool_calls[0])
    #     | RunnableLambda(lambda x: tool_functions[x["name"]].invoke(x["args"]))
    # )
    # result = await tool_calling_chain.ainvoke(query)

    with get_usage_metadata_callback() as cb:
        llm = await acall_llm(model_provider, model, temperature, api_key)
        llm_with_tools = llm.bind_tools(tools)
        tool_calling_chain = (
            llm_with_tools
            | RunnableLambda(lambda output: output.tool_calls[0])
            | RunnableLambda(lambda x: tool_functions[x["name"]].invoke(x["args"]))
        )
        result = await tool_calling_chain.ainvoke(query)

    print("tool")
    print(result)
    token_usage = cb.usage_metadata
    token_usage["model_provider"] = model_provider
    total_token_used.append(token_usage)

    if result is None:
        result, token_usage = await general_chat(
            query, model_provider, model, temperature, api_key
        )
        total_token_used.append(token_usage)

    else:
        result, token_usage = await humanize_tool_response(
            query, result, conf_key, temperature, api_key
        )
        total_token_used.append(token_usage)

    return result, total_token_used


async def riddle_chat(
    query: str,
    model_provider: str,
    model: str,
    temperature: int = 0.4,
    api_key: str = None,
):
    print("Solving Riddle")
    content = config["riddle"]["prompt"].format(query)
    model_provider = config["riddle"]["provider"]
    model = config["riddle"]["model"]

    with get_usage_metadata_callback() as cb:
        llm = await acall_llm(model_provider, model, temperature, api_key)
        chain = llm | StrOutputParser()
        result = await chain.ainvoke(content)
    token_usage = cb.usage_metadata
    token_usage["model_provider"] = model_provider
    return eval(result), [token_usage]


async def ask_llm(
    query: str,
    model_provider: str,
    model: str,
    use_tool: bool,
    temperature: int = 0,
    api_key: str = None,
):

    try:
        if use_tool == False:
            result, token_usage = await riddle_chat(
                query,
                model_provider,
                model,
                temperature,
                api_key,
            )
            return result, token_usage

        else:

            tool_conf = tool_directory["test_tool"]
            try:
                config[tool_conf["prompt"]]
            except:
                print(
                    f"\033[91mDefault prompt field was added to tool_directory as it the provided key `{tool_conf['prompt']}` was not present originally in config.yml.\033[0m"
                )
                tool_conf["prompt"] = "general_context_info"

            if all(key in tool_conf.keys() for key in required_keys):

                res, token_usage = await chat(
                    query,
                    model_provider,
                    model,
                    tool_conf,
                    temperature,
                    api_key,
                )
                return res, token_usage
            else:
                raise ValueError(
                    "Missing keys: Please include only [tools, tool_functions, prompt] in your tool_directory"
                )
    except Exception as e:
        print(f"Error occured while : \t {e}")
        return None, None
