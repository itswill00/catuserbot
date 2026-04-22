import os
import sys

def interactive_setup():
    """Terminal setup for first-time users."""
    if os.environ.get("STRING_SESSION") or os.path.exists(".env") or os.path.exists("config.py"):
        return

    print("====================================================")
    print("      CATUSERBOT INTERACTIVE SETUP")
    print("====================================================")
    print("Configuration not found.")
    
    choice = input("Would you like to configure your bot now? (y/n): ").lower()
    if choice != 'y':
        print("Setup skipped.")
        return

    api_id = input("Enter your API_ID: ")
    api_hash = input("Enter your API_HASH: ")
    string_session = input("Enter your STRING_SESSION: ")
    bot_token = input("Enter your TG_BOT_TOKEN (optional): ")

    with open(".env", "w") as f:
        f.writelines([
            f"APP_ID={api_id}\n",
            f"API_HASH={api_hash}\n",
            f"STRING_SESSION={string_session}\n",
            f"TG_BOT_TOKEN={bot_token}\n" if bot_token else "",
            "ENV=True\n"
        ])
    
    print("\n[!] Configuration saved to .env.")
    print("[!] Restarting...\n")
    os.execv(sys.executable, ['python3'] + sys.argv)
