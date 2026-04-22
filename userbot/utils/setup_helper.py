import os
import sys

def interactive_setup():
    """Terminal setup for first-time users."""
    if os.environ.get("STRING_SESSION") or os.path.exists(".env") or os.path.exists("config.py"):
        return

    print("\n" + "="*52)
    print("      🚀 CATUSERBOT MODERN INTERACTIVE SETUP 🚀")
    print("="*52)
    print("\nConfiguration not found. Let's get you set up!\n")
    
    choice = input("Would you like to configure your bot now? (y/n): ").lower()
    if choice != 'y':
        print("\n[!] Setup skipped. You need to create a .env file manually.")
        return

    print("\n--- 1. Telegram API Credentials ---")
    print("Get these from https://my.telegram.org")
    api_id = input("   Enter your API_ID: ").strip()
    api_hash = input("   Enter your API_HASH: ").strip()
    
    print("\n--- 2. User Session ---")
    string_session = input("   Enter your STRING_SESSION: ").strip()

    print("\n--- 3. Assistant Bot (Optional but recommended) ---")
    print("Get a token from @BotFather for Assistant features.")
    bot_token = input("   Enter your TG_BOT_TOKEN: ").strip()

    print("\n--- 4. Management & Logging ---")
    owner_id = input("   Enter your User ID (Owner): ").strip()
    log_id = input("   Enter your Log Group/Channel ID (e.g. -100xxx): ").strip()

    with open(".env", "w") as f:
        f.write("# CatUserbot Configuration\n")
        f.write(f"APP_ID={api_id}\n")
        f.write(f"API_HASH={api_hash}\n")
        f.write(f"STRING_SESSION={string_session}\n")
        if bot_token:
            f.write(f"TG_BOT_TOKEN={bot_token}\n")
        if owner_id:
            f.write(f"OWNER_ID={owner_id}\n")
        if log_id:
            f.write(f"PRIVATE_GROUP_BOT_API_ID={log_id}\n")
            f.write(f"PM_LOGGER_GROUP_ID={log_id}\n")
        f.write("ENV=True\n")
    
    print("\n" + "="*52)
    print("✅ Configuration saved to .env!")
    print("Bot will now restart and start loading plugins.")
    print("="*52 + "\n")
    
    os.execv(sys.executable, [sys.executable, '-m', 'userbot'])
