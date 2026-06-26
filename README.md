# 🦈 Shark Bot — Henry Tech Automation V5.0

A powerful WhatsApp bot built with Baileys (Node.js) + Quart (Python), featuring AI chat, media downloading, auto reactions, anti-ban, and much more.

---

## 📋 Requirements

- Node.js v18+
- Python 3.10+
- A WhatsApp account
- Groq API key (free at [console.groq.com](https://console.groq.com))

---

## 📁 File Structure

```
shark-bot/
├── app.py               # Python backend (AI, database, commands)
├── client_bridge.js     # WhatsApp bridge (Baileys)
├── start.sh             # Startup script (starts Python first, then Node)
├── requirements.txt     # Python dependencies
├── package.json         # Node.js dependencies
├── Dockerfile           # Docker build file
├── railway.json         # Railway deploy config
├── render.yaml          # Render deploy config
├── .env.example         # Copy to .env and fill in your keys
└── README.md            # This file
```

---

## ⚙️ Setup (Local / Termux)

### Step 1 — Copy environment file
```bash
cp .env.example .env
# Edit .env and paste your GROQ_API_KEY
nano .env
```

### Step 2 — Install Python dependencies (in a virtual environment)

Modern Termux/Python blocks plain `pip install` with an `externally-managed-environment`
error. A virtual environment sidesteps that cleanly — no special flags needed:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

`start.sh` (below) automatically detects and uses this `.venv` if it exists, so once
it's created you don't need to `source .venv/bin/activate` again before running the bot.

### Step 3 — Install Node.js dependencies
```bash
npm install
```

---

## 📱 Running on Termux (Android)

```bash
# Install system packages
pkg update && pkg upgrade -y
pkg install python nodejs git build-essential ffmpeg curl -y

# Clone or copy the bot folder
cd ~
# (paste or extract your bot files here)

# Create a virtual environment & install Python dependencies
# (avoids Termux's "externally-managed-environment" pip error)
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt --prefer-binary
deactivate

# Install Node dependencies
npm install

# Set your Groq API key
echo "GROQ_API_KEY=your_key_here" > .env

# Run the bot — start.sh auto-detects .venv and uses it
bash start.sh
```

> **Tip:** Use `tmux` or `screen` to keep the bot running when you close Termux:
> ```bash
> pkg install tmux
> tmux new -s sharkbot
> bash start.sh
> # Press Ctrl+B then D to detach
> ```

> **⚡ Wake-Lock — stop Android from killing the bot:** Android suspends background processes to save battery. Tell Termux to stay awake before running the bot — no extra app needed, it's built into Termux:
> ```bash
> termux-wake-lock
> bash start.sh
> ```
> To release the lock later: `termux-wake-unlock`
>
> For a permanent fix: Android **Settings → Battery → Termux → Unrestricted** (wording varies by phone brand — look for "Unrestricted" or "No restrictions" under battery optimisation).

---

## 🔗 Linking WhatsApp

When you run `node client_bridge.js` you'll be asked for:

1. **Session name** — enter anything (e.g. `mybot`)
2. **Linking method** — choose:

### Method 1 — QR Code
- Choose `1` when prompted
- Open WhatsApp → Linked Devices → Link a Device → Scan QR

### Method 2 — Pairing Code
- Choose `2` when prompted
- Enter your number with country code (e.g. `2547XXXXXXXX`)
- Open WhatsApp → Linked Devices → Link a Device → "Link with phone number instead"
- Enter the code shown

---

## 🚀 Running the Bot

### Option A — Run both together (recommended for Termux)
```bash
bash start.sh
```

### Option B — Run separately (two terminals)
```bash
# Terminal 1 — Python backend
# (activate the venv first if you created one in Setup)
source .venv/bin/activate   # skip this line if you didn't use a venv
python app.py

# Terminal 2 — WhatsApp bridge
node client_bridge.js
```

---

## 💬 Commands

| Command | Description |
|---------|-------------|
| `/ask [query]` | Chat with Llama-3 AI via Groq |
| `/paint [text]` | Generate a styled text image |
| `/download_video [URL]` | Download video (YT, IG, FB, TikTok, 1000+ sites) |
| `/download_song [URL]` | Extract audio stream from any video |
| `/recover [number]` | Recover last 5 cached messages from a contact |

---

## 🛡️ Auto Features

| Feature | Status |
|---------|--------|
| Auto Save Contacts | ✅ On |
| Auto Welcome Message | ✅ On |
| Auto Read Messages | ✅ On |
| Auto React to Messages | ✅ On |
| Auto View & Like Status | ✅ On |
| Auto Bio Update (60s) | ✅ On |
| Save View Once Media | ✅ On |
| Anti-Call | ✅ On |
| Always Online | ✅ On |
| Anti-Ban Mode (random delays) | ✅ On |
| Fake Typing/Recording Simulation | ✅ On |
| Auto Reconnect | ✅ On |
| Multi-Session Support | ✅ On |

---

## 🚂 Deploying to Railway

1. Push your code to a GitHub repo
2. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub
3. Select your repo
4. Go to **Variables** → Add: `GROQ_API_KEY=your_key`, and either `SESSION_ID=mybot` plus `PAIRING_NUMBER=2547XXXXXXXX` (pairing code shown in the deploy logs), or just `SESSION_ID=mybot` to get a QR code printed in the logs instead
5. Railway auto-builds using `railway.json` + `Dockerfile`
6. ⚠️ **Note:** Without `SESSION_ID`/`PAIRING_NUMBER` set, the bot has no terminal to ask you for them and will fall back to defaults (session `default`, QR code in the logs). Either way, attach a persistent volume mounted at `sessions/` (and ideally the working dir, for the SQLite DB) — without one, every redeploy/restart wipes your WhatsApp session and you'll have to relink.

---

## 🗄️ Database

SQLite file `henry_tech_v5.db` stores:
- `contacts` — all saved WhatsApp contacts
- `messages` — all incoming messages (for /recover)
- `blacklist` — blocked users

---

## ⚠️ Important Notes

- Keep your `sessions/` folder safe — it contains your WhatsApp auth
- Never share your `sessions/` folder publicly
- Bot auto-reconnects on disconnection with a 3-second backoff
- GROQ_API_KEY is required for `/ask` command only

---

Built by **Henry Tech** 🦈
