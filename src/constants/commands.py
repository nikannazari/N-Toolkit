"""
commands.py - Central registry for framework commands, tools, and constants.
"""

# Framework Metadata
FRAMEWORK_NAME = "N-Toolkit"
FRAMEWORK_VERSION = "1.0.0"
PROMPT_TEXT = f"{FRAMEWORK_NAME} ❯ "

# Built-in shell commands (handled directly by prompt.py)
# In src/commands.py, update the BUILTIN_COMMANDS dictionary:
BUILTIN_COMMANDS = {
    "help": "Show this help menu and available options",
    "tools": "List all available integrated tools",
    "run <tool> ui": "Launch the Streamlit Web UI for a tool",
    "run <tool> <args>": "Run the tool in CLI mode with arguments",
    "clear": "Clear the terminal screen",
    "history": "Show command history",
    "exit": "Exit the framework safely"
}

# Available tools (will eventually be dynamically loaded from core/tools)
AVAILABLE_TOOLS = [
    "calculator++",
    "ffmpeg",
    "autogit",
    "sysinfo",
    "nettools",
    "filemanager"
]

# Tool execution prefix
TOOL_RUN_PREFIX = "run"