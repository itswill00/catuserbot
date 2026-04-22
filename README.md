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

## 🛠️ Recent Modernization (2026)

The bot has been fully modernized for low-friction deployment:
- ✅ **Zero-Config DB:** Fully powered by Local JSON Database.
- ✅ **No Heroku Bloat:** Completely decoupled from Heroku for better VPS performance.
- ✅ **Smart Setup:** Automated environment generation and session setup.

## 📦 Quick Installation (VPS/Local)

The setup is now a simple 3-step process:

### **Step 1: Run Automatic Setup**
```bash
git clone https://github.com/itswill00/catuserbot.git
cd catuserbot
bash setup.sh
```
*This will install dependencies and automatically create your `.env` file.*

### **Step 2: Configure & Generate Session**
1. Open the `.env` file and fill in your `APP_ID`, `API_HASH`, and `TG_BOT_TOKEN`.
2. Run the smart session generator:
   ```bash
   python3 stringsetup.py
   ```
3. Copy the generated string and paste it into the `STRING_SESSION` field in your `.env`.

### **Step 3: Start the Bot**
```bash
python3 -m userbot
```

---

## 🐳 Docker Deployment

```bash
docker-compose up -d
```
*Make sure to fill your `.env` file before running docker.*

## ⚙️ Essential Variables

| Variable | Description |
|----------|-------------|
| `APP_ID` | Your API ID from my.telegram.org |
| `API_HASH` | Your API Hash from my.telegram.org |
| `STRING_SESSION` | Telethon Session String |
| `TG_BOT_TOKEN` | Token from @BotFather for the Assistant Bot |

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
