# 🐱 CatUserbot

<p align="center">
    <img src="https://graph.org/file/4860c8e1a5a56d0616b79.png" width="200" alt="CatUserbot Logo">
</p>

<p align="center">
    <a href="https://github.com/itswill00/catuserbot/stargazers"><img src="https://img.shields.io/github/stars/itswill00/catuserbot?style=for-the-badge&color=blue" alt="Stars"></a>
    <a href="https://github.com/itswill00/catuserbot/network/members"><img src="https://img.shields.io/github/forks/itswill00/catuserbot?style=for-the-badge&color=red" alt="Forks"></a>
    <a href="https://github.com/itswill00/catuserbot/blob/master/LICENSE"><img src="https://img.shields.io/github/license/itswill00/catuserbot?style=for-the-badge&color=green" alt="License"></a>
    <a href="https://t.me/catuserbot_support"><img src="https://img.shields.io/badge/Telegram-Support-blue?style=for-the-badge&logo=telegram" alt="Support"></a>
</p>

---

**CatUserbot** is a powerful, highly customizable, and optimized Telegram Userbot based on [Telethon](https://github.com/LonamiWebs/Telethon). Designed for stability, speed, and ease of use.

## 🚀 Key Features

- ⚡ **Lightning Fast:** Optimized plugin loading and concurrent execution.
- 📂 **Local JSON Database:** No more complex SQL setups. Lightweight and portable.
- 🛠️ **100+ Plugins:** From admin tools to fun games and media converters.
- 🛡️ **Stable & Secure:** Built-in error handling and security checks.
- 🐳 **Docker Ready:** Deploy anywhere with ease.
- 🤖 **Assistant Bot:** Includes a helper bot for PM management and more.

## 🛠️ Recent Stability Fixes (v3.3.1+)

We've recently overhauled the core for maximum reliability:
- ✅ **Async Initialization:** Fixed core event loop and startup conflicts.
- ✅ **Data Safety:** Prevented accidental plugin deletion on import errors.
- ✅ **Robust Config:** Added intelligent validation for environment variables.
- ✅ **Improved Logging:** More descriptive error reports for easier debugging.

## 📦 Quick Installation

### 🖥️ Local Deployment

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/itswill00/catuserbot.git
   cd catuserbot
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure:**
   - Copy `sample_config.py` to `config.py` and fill in your details.
   - Or simply run the bot and follow the interactive setup.

4. **Run:**
   ```bash
   python3 -m userbot
   ```

### 🐳 Docker Deployment

```bash
docker build -t catuserbot .
docker run -it --env-file .env catuserbot
```

## ⚙️ Configuration Variables

| Variable | Description |
|----------|-------------|
| `APP_ID` | Your API ID from my.telegram.org |
| `API_HASH` | Your API Hash from my.telegram.org |
| `STRING_SESSION` | Telethon Session String |
| `TG_BOT_TOKEN` | Token from @BotFather for the Assistant Bot |
| `PRIVATE_GROUP_BOT_API_ID` | Group ID for Bot Logs |

> For a full list of variables, check [docs/installation/variables/](docs/installation/variables/).

## 🤝 Support & Community

- 📢 **Channel:** [@catuserbot17](https://t.me/catuserbot17)
- 💬 **Support Group:** [@catuserbot_support](https://t.me/catuserbot_support)

## 📜 Disclaimer

> **Your Telegram account may get banned if you misuse this bot.**
> The developers are not responsible for any risks to your account.
> Use this bot wisely and at your own risk.

## ❤️ Credits

- [Telethon](https://github.com/LonamiWebs/Telethon/) by LonamiWebs.
- [CatUserBot Original Team](https://github.com/TgCatUB/catuserbot).
- Improved and Maintained by [itswill00](https://github.com/itswill00).
