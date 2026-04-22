# 🐾 CatUserbot (Modern 2026 Edition)

**CatUserbot** adalah Telegram Userbot berbasis [Telethon](https://github.com/LonamiWebs/Telethon) yang telah dimodernisasi untuk efisiensi tinggi, stabilitas maksimal, dan kemudahan setup. Versi ini telah dioptimalkan sepenuhnya untuk berjalan tanpa ketergantungan database eksternal.

![catuserbot logo](https://graph.org/file/4860c8e1a5a56d0616b79.png)

---

## 🚀 Fitur Unggulan (Modern & Efficient)

- 📦 **100% Local JSON DB:** Tidak butuh PostgreSQL, Redis, atau SQL lainnya. Semua data (GBAN, Filter, Sudo, dll) tersimpan aman di lokal dalam format JSON yang ringan.
- ⚡ **Parallel Plugin Loading:** Bot menyala jauh lebih cepat berkat sistem pemuatan plugin secara konkuren menggunakan `asyncio.gather`.
- 🛠️ **Interactive Terminal Setup:** Pertama kali menjalankan bot? Bot akan memandu Anda melakukan konfigurasi langsung di terminal (Auto-generate `.env`).
- 🐳 **Docker Optimized:** Image Docker yang lebih ringan berbasis Python 3.11-slim, siap dideploy di mana saja.
- 🧠 **AI Ready:** Arsitektur core telah disiapkan untuk integrasi AI (OpenAI/Gemini) secara native.
- 🛡️ **Smart Error Handling:** Pelaporan error yang lebih cerdas dengan traceback otomatis yang dikirim ke grup log pribadi Anda.

---

## 🛠️ Cara Install & Setup

### ⚡ Jalankan Secara Lokal (Cara Tercepat)

1. **Clone Repositori:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/catuserbot.git
   cd catuserbot
   ```

2. **Instal Dependensi:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Jalankan Bot:**
   ```bash
   python3 -m userbot
   ```
   *Jika Anda belum memiliki file konfigurasi, bot akan otomatis masuk ke **Mode Setup Interaktif** di terminal Anda.*

---

### 🐳 Menggunakan Docker

1. **Build Image:**
   ```bash
   docker build -t catuserbot .
   ```

2. **Jalankan Container:**
   ```bash
   docker run -it --env-file .env catuserbot
   ```

---

## 📂 Struktur Data (Local DB)

Karena kita menggunakan **Local JSON DB**, seluruh data Anda tersimpan di direktori:
`userbot/cache/*.json`

*Pastikan Anda melakukan backup folder `userbot/cache/` jika ingin memindahkan bot ke server lain agar data filter, blacklist, dan sudo Anda tidak hilang.*

---

## 🤝 Dukungan & Komunitas

Jika Anda menemukan bug atau membutuhkan bantuan, silakan hubungi kami di:
- 📢 **Channel:** [@catuserbot17](https://t.me/catuserbot17)
- 👥 **Group Support:** [@catuserbot_support](https://t.me/catuserbot_support)

---

## ⚠️ Disclaimer

```text
              PENTING: RISIKO BANNED
Akun Telegram Anda mungkin terkena banned jika menyalahgunakan bot ini (Spamming/Flooding).
Kami (Pengembang) tidak bertanggung jawab atas segala risiko pada akun Anda.
Gunakan bot ini dengan bijak untuk tujuan produktivitas dan kesenangan.
```

---

## ❤️ Credits & Inspiration

- [Telethon](https://github.com/LonamiWebs/Telethon/) oleh LonamiWebs.
- [CatUserBot Original Team](https://github.com/TgCatUB/catuserbot) untuk fondasi awalnya.
- Seluruh kontributor dan komunitas Userbot Telegram.

---
**Made with ❤️ and high-performance code.**
