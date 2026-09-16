"""
prompt_validator.py - Validates the syntax of user input.
"""

from src.commands import TOOL_RUN_PREFIX

def validate_prompt_syntax(user_input: str) -> tuple[bool, tuple, str]:
    """
    Validates the syntax of the input.
    Returns: (is_valid, parsed_data, error_message)
    """
    parts = user_input.strip().split()
    
    if not parts:
        return False, (), "Empty input."

    main_cmd = parts[0].lower()

    # If it's a tool execution command: run <tool> [args...]
    if main_cmd == TOOL_RUN_PREFIX:
        if len(parts) < 2:
            return False, (), f"Missing tool name. Usage: '{TOOL_RUN_PREFIX} <tool> [args]'"
        
        tool_name = parts[1]
        args = parts[2:]  # Everything after the tool name is an argument
        return True, (tool_name, args), "OK"

    # If it's a direct command (e.g., user typed 'calculator++' instead of 'run calculator++')
    # We'll allow direct execution if the word matches a tool name later.
    tool_name = parts[0]
    args = parts[1:]
    return True, (tool_name, args), "OK"