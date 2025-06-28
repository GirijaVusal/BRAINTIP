from bot.available_tools import small_talks, calculate, get_weather_for_city

# How to create tool registry keys tools,tool_functions,prompt should be included
# In prompt part include the the name you include in config file if not just put general_context_info
required_keys = ["tools", "tool_functions", "prompt"]


tool_directory = {
    "test_tool": {
        "tools": [
            small_talks,
            calculate,
            get_weather_for_city,
        ],
        "tool_functions": {
            "small_talks": small_talks,
            "calculate": calculate,
            "get_weather_for_city": get_weather_for_city,
        },
        "prompt": "general_context_info",
    }
}
