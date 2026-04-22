# 🐾 CatUserbot (Modern 2026 Edition)

**CatUserbot** is a Telegram Userbot based on [Telethon](https://github.com/LonamiWebs/Telethon) that has been modernized for high efficiency, maximum stability, and easy setup. This version is fully optimized to run without external database dependencies.

![catuserbot logo](https://graph.org/file/4860c8e1a5a56d0616b79.png)

---

## 🚀 Key Features (Modern & Efficient)

- 📦 **100% Local JSON DB:** No need for PostgreSQL, Redis, or other SQL databases. All data (GBAN, Filters, Sudo, etc.) is safely stored locally in a lightweight JSON format.
- ⚡ **Parallel Plugin Loading:** The bot starts significantly faster thanks to concurrent plugin loading using `asyncio.gather`.
- 🛠️ **Interactive Terminal Setup:** Running the bot for the first time? It will guide you through configuration directly in the terminal (Auto-generates `.env`).
- 🐳 **Docker Optimized:** Lightweight Docker image based on Python 3.11-slim, ready to deploy anywhere.
- 🧠 **AI Ready:** Core architecture is prepared for native AI integration (OpenAI/Gemini).
- 🛡️ **Smart Error Handling:** Smarter error reporting with automatic tracebacks sent to your private log group.

---

## 🛠️ Installation & Setup

### ⚡ Run Locally (Fastest Way)

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
   *If you don't have a configuration file yet, the bot will automatically enter **Interactive Setup Mode** in your terminal.*

---

### 🐳 Using Docker

1. **Build the Image:**
   ```bash
   docker build -t catuserbot .
   ```

2. **Run the Container:**
   ```bash
   docker run -it --env-file .env catuserbot
   ```

---

## 📂 Data Structure (Local DB)

Since we are using **Local JSON DB**, all your data is stored in:
`userbot/cache/*.json`

*Make sure to backup the `userbot/cache/` folder if you want to move the bot to another server so your filters, blacklists, and sudo data are not lost.*

---

## 🤝 Support & Community

If you find a bug or need help, please contact us at:
- 📢 **Channel:** [@catuserbot17](https://t.me/catuserbot17)
- 👥 **Group Support:** [@catuserbot_support](https://t.me/catuserbot_support)

---

## ⚠️ Disclaimer

```text
              IMPORTANT: BANNED RISK
Your Telegram account may get banned if you misuse this bot (Spamming/Flooding).
We (the developers) are not responsible for any risks to your account.
Use this bot wisely for productivity and fun purposes.
```

---

## ❤️ Credits & Inspiration

- [Telethon](https://github.com/LonamiWebs/Telethon/) by LonamiWebs.
- [CatUserBot Original Team](https://github.com/TgCatUB/catuserbot) for the original foundation.
- All contributors and the Telegram Userbot community.

---
**Made with ❤️ and high-performance code.**
