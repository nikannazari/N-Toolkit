# main.py
from src.services.welcome import welcome
from src.services.prompt import start_prompt, show_options

def main():
    # 1. Show the spectacular welcome screen
    welcome()
    
    # 2. Show the available commands immediately after welcome
    show_options()
    
    # 3. Start the interactive prompt loop
    start_prompt()

if __name__ == "__main__":
    main()