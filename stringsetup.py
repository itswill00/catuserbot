#!/usr/bin/env python3
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Script to generate CatUserbot STRING_SESSION.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import os
import sys

# Try to load .env if python-dotenv is installed
try:
    from dotenv import load_dotenv
    if os.path.exists(".env"):
        load_dotenv(".env")
except ImportError:
    pass

from telethon.sessions import StringSession
from telethon.sync import TelegramClient

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    clear_screen()
    print("="*60)
    print("      C A T U S E R B O T   S T R I N G   S E T U P")
    print("="*60)
    print("\nInstructions:")
    print("1. Go to https://my.telegram.org")
    print("2. Login with your Telegram phone number.")
    print("3. Click on 'API Development Tools'.")
    print("4. Create a new application (if you haven't already).")
    print("5. Copy your 'App api_id' and 'App api_hash'.")
    print("\n" + "-"*60)

    # Try to get credentials from environment variables
    env_app_id = os.environ.get("APP_ID")
    env_api_hash = os.environ.get("API_HASH")

    if env_app_id and env_api_hash:
        print(f"\n[!] Found existing APP_ID in .env: {env_app_id}")
        use_env = input("Use APP_ID & API_HASH from .env? (y/n): ").lower()
        if use_env == 'y':
            APP_ID = int(env_app_id)
            API_HASH = env_api_hash
        else:
            try:
                APP_ID = int(input("\nEnter APP ID: "))
                API_HASH = input("Enter API HASH: ")
            except ValueError:
                print("\n[Error] APP ID must be a number!")
                return
    else:
        try:
            APP_ID = int(input("\nEnter APP ID: "))
            API_HASH = input("Enter API HASH: ")
        except ValueError:
            print("\n[Error] APP ID must be a number!")
            return

    print("\n" + "-"*60)
    print("Connecting to Telegram...")
    
    try:
        with TelegramClient(StringSession(), APP_ID, API_HASH) as client:
            session_string = client.session.save()
            
            print("\n" + "="*60)
            print("SUCCESS! Here is your STRING_SESSION:")
            print("="*60)
            print(f"\n{session_string}\n")
            print("="*60)
            print("IMPORTANT: DO NOT SHARE THIS STRING WITH ANYONE!")
            print("Copy the string above and paste it into STRING_SESSION in your .env file.")
            
            try:
                client.send_message("me", f"**CatUserbot STRING_SESSION:**\n\n`{session_string}`\n\n**Keep this safe and do not share it!**")
                print("\n[Info] A copy of the session string has also been sent to your 'Saved Messages'.")
            except Exception:
                pass
                
    except Exception as e:
        print(f"\n[Error] An error occurred: {e}")

if __name__ == "__main__":
    main()
