# CatUserbot

**CatUserbot** is a Telegram Userbot based on [Telethon](https://github.com/LonamiWebs/Telethon). This version is optimized to run with a local JSON database and simplified setup process.

![catuserbot logo](https://graph.org/file/4860c8e1a5a56d0616b79.png)

---

## Features

- **Local JSON DB:** Uses a lightweight JSON database for all storage (GBAN, Filters, Sudo, etc.), eliminating the need for external SQL databases.
- **Improved Performance:** Faster plugin loading using concurrent execution.
- **Interactive Setup:** Guided configuration directly in the terminal for first-time users.
- **Docker Support:** Optimized Dockerfile using Python 3.11-slim.

---

## Installation & Setup

### Local Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/itswill00/catuserbot.git
   cd catuserbot
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Bot:**
   ```bash
   python3 -m userbot
   ```
   *Follow the interactive prompts in the terminal to configure your bot.*

---

### Docker Setup

1. **Build the Image:**
   ```bash
   docker build -t catuserbot .
   ```

2. **Run the Container:**
   ```bash
   docker run -it --env-file .env catuserbot
   ```

---

## Data Management

All persistent data is stored in the following directory:
`userbot/cache/*.json`

---

## Support

- **Channel:** [@catuserbot17](https://t.me/catuserbot17)
- **Group:** [@catuserbot_support](https://t.me/catuserbot_support)

---

## Disclaimer

```text
Your Telegram account may get banned if you misuse this bot.
Developers are not responsible for any risks to your account.
Use this bot wisely.
```

---

## Credits

- [Telethon](https://github.com/LonamiWebs/Telethon/) by LonamiWebs.
- [CatUserBot Original Team](https://github.com/TgCatUB/catuserbot).
