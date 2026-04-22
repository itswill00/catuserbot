import os
import sys

def interactive_setup():
    """Interactive terminal setup for first-time users."""
    if os.environ.get("STRING_SESSION") or os.path.exists(".env") or os.path.exists("config.py"):
        return

    print("====================================================")
    print("      CATUSERBOT INTERACTIVE SETUP (2026)")
    print("====================================================")
    print("It seems you haven't configured your bot yet.")
    
    choice = input("Would you like to setup now? (y/n): ").lower()
    if choice != 'y':
        print("Setup skipped. Bot might fail to start if vars are missing.")
        return

    api_id = input("Enter your API_ID: ")
    api_hash = input("Enter your API_HASH: ")
    string_session = input("Enter your STRING_SESSION: ")
    bot_token = input("Enter your TG_BOT_TOKEN (optional, press enter to skip): ")

    with open(".env", "w") as f:
        f.write(f"APP_ID={api_id}\n")
        f.write(f"API_HASH={api_hash}\n")
        f.write(f"STRING_SESSION={string_session}\n")
        if bot_token:
            f.write(f"TG_BOT_TOKEN={bot_token}\n")
        f.write("ENV=True\n")
    
    print("\n[!] .env file created successfully!")
    print("[!] Restarting the bot to apply changes...\n")
    os.execv(sys.executable, ['python3'] + sys.argv)
