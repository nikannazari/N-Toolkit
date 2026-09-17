"""
commands.py - Central registry for framework commands, tools, and constants.
"""

# Framework Metadata
FRAMEWORK_NAME = "N-Toolkit"
FRAMEWORK_VERSION = "1.0.0"
PROMPT_TEXT = f"{FRAMEWORK_NAME} ❯ "

# Built-in shell commands
BUILTIN_COMMANDS = {
    "help": "Show this help menu and available options",
    "tools": "List all available integrated tools",
    "run <tool>": "Launch the Streamlit Web UI for a specific tool",
    "clear": "Clear the terminal screen",
    "history": "Show command history",
    "exit": "Exit the framework safely"
}

# Available tools
AVAILABLE_TOOLS = [
    "calculator++",
    "mpv++"
    # "ffmpeg",
    # "autogit",
    # "sysinfo",
    # "nettools",
    # "filemanager"
]

# Tool execution prefix
TOOL_RUN_PREFIX = "run"