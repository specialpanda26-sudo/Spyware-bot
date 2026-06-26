import os
import time
import asyncio
import logging
import json
from urllib.parse import quote_plus
from pathlib import Path
from quart import Quart, request, jsonify, Response
import httpx
import aiosqlite

# Load .env file if present (for local/Termux dev)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Setup logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("HenryTechCore")

def print_banner():
    banner = """
\033[1;36m
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   ██╗  ██╗███████╗███╗   ██╗██████╗ ██╗   ██╗              ║
║   ██║  ██║██╔════╝████╗  ██║██╔══██╗╚██╗ ██╔╝              ║
║   ███████║█████╗  ██╔██╗ ██║██████╔╝ ╚████╔╝               ║
║   ██╔══██║██╔══╝  ██║╚██╗██║██╔══██╗  ╚██╔╝                ║
║   ██║  ██║███████╗██║ ╚████║██║  ██║   ██║                  ║
║   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝   ╚═╝                 ║
║                                                              ║
║   \033[1;35m██████╗  ██████╗ ████████╗███████╗\033[1;36m                    ║
║   \033[1;35m██╔══██╗██╔═══██╗╚══██╔══╝██╔════╝\033[1;36m                    ║
║   \033[1;35m██████╔╝██║   ██║   ██║   ███████╗\033[1;36m                    ║
║   \033[1;35m██╔══██╗██║   ██║   ██║   ╚════██║\033[1;36m                    ║
║   \033[1;35m██████╔╝╚██████╔╝   ██║   ███████║\033[1;36m                    ║
║   \033[1;35m╚═════╝  ╚═════╝    ╚═╝   ╚══════╝\033[1;36m                   ║
║                                                              ║
║      \033[1;33m✦ Henry Bots© — created by Henry ✦\033[1;36m              ║
║      \033[1;32m🦈 AUTOMATION V5.0  |  PYTHON BACKEND\033[1;36m              ║
║      \033[1;33m⚡ AI  |  DATABASE  |  COMMANDS  |  API\033[1;36m            ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
\033[0m"""
    print(banner)

print_banner()

app = Quart(__name__)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
if not GROQ_API_KEY:
    logger.warning("⚠️  GROQ_API_KEY not set! /ask command will fail.")

async def call_groq_ai(prompt: str) -> str:
    """Call Groq API directly via httpx — no groq package needed."""
    if not GROQ_API_KEY:
        return "❌ AI not configured. Set GROQ_API_KEY in your .env file."
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    # NOTE: "llama3-8b-8192" was decommissioned by Groq (May 2025).
                    # openai/gpt-oss-20b is a current production model — fast & cheap.
                    # If Groq deprecates this too, check https://console.groq.com/docs/models
                    "model": "openai/gpt-oss-20b",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 1024
                }
            )
            try:
                data = response.json()
            except ValueError:
                return f"❌ AI Error: Groq returned a non-JSON response (HTTP {response.status_code})"
            if response.status_code == 200:
                try:
                    return data["choices"][0]["message"]["content"]
                except (KeyError, IndexError):
                    return "❌ AI Error: Unexpected response shape from Groq."
            else:
                return f"❌ AI Error: {data.get('error', {}).get('message', 'Unknown error')}"
    except Exception as e:
        return f"❌ AI Error: {str(e)}"
DB_FILE = "henry_tech_v5.db"
SESSION_REGISTRY = {}


async def init_db():
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                sender TEXT PRIMARY KEY, name TEXT, timestamp REAL
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS blacklist (sender TEXT PRIMARY KEY)
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                msg_id TEXT PRIMARY KEY, sender TEXT, name TEXT, body TEXT, timestamp REAL
            )
        """)
        await db.commit()
        logger.info("\033[1;32m⚡ V5.0 Master Database Synchronized — All tables ready.\033[0m")


@app.before_serving
async def startup_configuration_lifecycle():
    await init_db()
    logger.info("\033[1;36m🦈 Henry Tech V5.0 Backend LIVE on port %s\033[0m", os.environ.get("PORT", 5000))
    logger.info("\033[1;33m📡 Waiting for Shark Bot (Node.js) to connect...\033[0m")


WELCOME_TEXT = (
    "╔═══════════════════════════════════════╗\n"
    "  █░█ █▀▀ █▄░█ █▀█ █▄█   ▀█▀ █▀▀ █▀▀ █░█\n"
    "  █▀█ ██▄ █░▀█ █▀▄ ░█░   ░█░ ██▄ █▄▄ █▀█\n"
    "╚═══════════════════════════════════════╝\n\n"
    "✨ 𝖧𝖤𝖭𝖱𝖸 𝖳𝖤𝖢𝖧 𝖠𝖴𝖳𝖮𝖬𝖠𝖳𝖨𝖮𝖭 𝖵𝖤𝖱𝖲𝖨𝖮𝖭 5.0 ✨\n\n"
    "Your profile node is securely authenticated. All 19 Automation Core Modules are currently online. 🌐\n\n"
    "⚡ ENGINE COMMAND MATRIX ⚡\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "🧠 /ask [query] ➔ Chat with Llama-3 AI\n"
    "🎨 /paint [text] ➔ Generate text image\n"
    "📥 /download_video [URL] ➔ Download Videos (YT, IG, FB, TikTok)\n"
    "🎧 /download_song [URL] ➔ Extract MP3 audio\n"
    "🗑️ /recover [number] ➔ Recover deleted messages\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    "🛡️ Anti-Ban, Fake Typing, Auto Status & Auto React running in background."
)


async def check_db_blacklist(sender: str) -> bool:
    if not sender:
        return False
    async with aiosqlite.connect(DB_FILE) as db:
        async with db.execute("SELECT 1 FROM blacklist WHERE sender = ?", (sender,)) as c:
            return (await c.fetchone()) is not None


async def get_video_url(url: str) -> dict:
    """Use yt-dlp to get direct video download link (dump-json only, no download)"""
    try:
        proc = await asyncio.create_subprocess_exec(
            "yt-dlp",
            "--dump-json",
            "--no-playlist",
            "-f", "best[ext=mp4]/best",
            "--no-warnings",
            url,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=45)
        if proc.returncode == 0:
            data = json.loads(stdout.decode())
            return {
                "success": True,
                "url": data.get("url", ""),
                "title": data.get("title", "Video"),
                "duration": data.get("duration_string", "")
            }
        return {"success": False, "error": stderr.decode()[:300]}
    except asyncio.TimeoutError:
        return {"success": False, "error": "Timed out. Try a shorter video."}
    except Exception as e:
        return {"success": False, "error": str(e)}


async def get_audio_url(url: str) -> dict:
    """
    Use yt-dlp to get best audio stream URL.
    NOTE: --dump-json with --extract-audio is incompatible (extract-audio requires actual download).
    We fetch the best audio format URL directly instead.
    """
    try:
        proc = await asyncio.create_subprocess_exec(
            "yt-dlp",
            "--dump-json",
            "--no-playlist",
            "-f", "bestaudio/best",
            "--no-warnings",
            url,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=45)
        if proc.returncode == 0:
            data = json.loads(stdout.decode())
            return {
                "success": True,
                "url": data.get("url", ""),
                "title": data.get("title", "Audio"),
                "ext": data.get("ext", "mp3")
            }
        return {"success": False, "error": stderr.decode()[:300]}
    except asyncio.TimeoutError:
        return {"success": False, "error": "Timed out. Try again."}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.route("/")
async def landing_page():
    index_path = Path(__file__).parent / "index.html"
    if index_path.exists():
        return Response(index_path.read_text(encoding="utf-8"), mimetype="text/html")
    return jsonify({"status": "ok", "service": "Henry Tech Shark Bot V5 backend"})


@app.route("/auto-save", methods=["POST"])
async def register_profile():
    data = await request.get_json() or {}
    sender = data.get("sender", "").strip()
    name = data.get("name", "User").strip()
    if not sender:
        return jsonify({"status": "error", "message": "Missing sender"}), 400
    if await check_db_blacklist(sender):
        return jsonify({"status": "blacklisted"})
    async with aiosqlite.connect(DB_FILE) as db:
        try:
            await db.execute("INSERT INTO contacts VALUES (?, ?, ?)", (sender, name, time.time()))
            await db.commit()
            return jsonify({"status": "new_user_registered", "welcome_message": WELCOME_TEXT})
        except aiosqlite.IntegrityError:
            return jsonify({"status": "already_indexed"})


@app.route("/log-message", methods=["POST"])
async def log_message():
    data = await request.get_json() or {}
    msg_id = data.get("msg_id")
    sender = data.get("sender")
    name = data.get("name", "User")
    body = data.get("body", "")
    if not msg_id or not sender:
        return jsonify({"status": "ignored"}), 400
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute(
            "INSERT OR REPLACE INTO messages VALUES (?, ?, ?, ?, ?)",
            (msg_id, sender, name, body, time.time())
        )
        await db.commit()
    return jsonify({"status": "logged"})


@app.route("/react", methods=["POST"])
async def process_sentiment():
    import random
    data = await request.get_json() or {}
    p = data.get("body", "").lower().strip()
    if random.random() > 0.6:
        return jsonify({"emoji": None})
    if any(w in p for w in ["love", "heart", "perfect", "amazing", "beautiful", "cute", "sweet"]):
        return jsonify({"emoji": random.choice(["❤️", "😍", "🥰", "💕"])})
    if any(w in p for w in ["lol", "haha", "lmao", "funny", "joke", "hilarious"]):
        return jsonify({"emoji": random.choice(["😂", "🤣", "💀", "😭"])})
    if any(w in p for w in ["sad", "cry", "miss", "alone", "depressed", "pain", "hurt"]):
        return jsonify({"emoji": random.choice(["🥺", "😢", "💔", "🫂"])})
    if any(w in p for w in ["fire", "lit", "banger", "hard", "crazy", "insane"]):
        return jsonify({"emoji": random.choice(["🔥", "💯", "🫡", "👏"])})
    if any(w in p for w in ["wow", "omg", "seriously", "really", "no way", "what"]):
        return jsonify({"emoji": random.choice(["😮", "😱", "🤯", "👀"])})
    if any(w in p for w in ["good", "nice", "cool", "great", "okay", "ok", "yes"]):
        return jsonify({"emoji": random.choice(["👍", "✅", "💪", "🙌"])})
    if any(w in p for w in ["money", "paid", "cash", "rich", "hustle", "business"]):
        return jsonify({"emoji": random.choice(["💰", "🤑", "💵", "📈"])})
    if any(w in p for w in ["fuck", "shit", "damn", "bro", "fam", "aye"]):
        return jsonify({"emoji": random.choice(["💀", "😭", "🤣", "👀"])})
    return jsonify({"emoji": random.choice(["👍", "🙏", "💯", "😊", "🫡", None, None])})



@app.route("/get-bio", methods=["GET"])
async def generate_auto_bio():
    t_str = time.strftime("%H:%M:%S")
    return jsonify({"bio": f"🤖 Henry Tech V5.0 Active | Sync: {t_str} | Operating Always 🌐"})


@app.route("/webhook", methods=["POST"])
async def process_command_pipeline():
    data = await request.get_json() or {}
    incoming_text = data.get("body", "").strip()
    sender = data.get("sender", "").strip()

    if await check_db_blacklist(sender):
        return jsonify({"reply": "❌ Access Denied. Your profile node remains blacklisted."})

    # 1. AI Command
    if incoming_text.startswith("/ask "):
        prompt = incoming_text[5:].strip()
        if not prompt:
            return jsonify({"reply": "⚠️ Please provide a query after /ask"})
        reply = await call_groq_ai(prompt)
        return jsonify({"reply": reply})

    # 2. Paint Command
    elif incoming_text.startswith("/paint "):
        prompt = incoming_text[7:].strip()
        if not prompt:
            return jsonify({"reply": "⚠️ Please provide text after /paint"})
        # quote_plus percent-encodes &, #, %, ?, /, emoji, etc. — a plain
        # .replace(' ', '+') let those characters break or truncate the URL.
        encoded = quote_plus(prompt)
        url = f"https://placehold.co/1200x630/0f172a/38bdf8?text={encoded}"
        return jsonify({"reply": f"🎨 *Text Image Generated*\n\n🖼️ Link:\n{url}"})

    # 3. Video Download Command
    elif incoming_text.startswith("/download_video "):
        url = incoming_text[16:].strip()
        if not url:
            return jsonify({"reply": "⚠️ Please provide a URL after /download_video"})
        result = await get_video_url(url)
        if result["success"] and result["url"]:
            title = result.get("title", "Video")
            duration = result.get("duration", "")
            return jsonify({"reply": f"⬇️ *Video Ready*\n\n🎬 {title}\n⏱️ {duration}\n\n📦 Download Link:\n{result['url']}"})
        return jsonify({"reply": f"❌ Could not download video.\n{result.get('error', 'Unknown error')}"})

    # 4. Song/MP3 Download Command
    elif incoming_text.startswith("/download_song "):
        url = incoming_text[15:].strip()
        if not url:
            return jsonify({"reply": "⚠️ Please provide a URL after /download_song"})
        result = await get_audio_url(url)
        if result["success"] and result["url"]:
            title = result.get("title", "Audio")
            ext = result.get("ext", "audio")
            return jsonify({"reply": f"🎧 *Audio Ready*\n\n🎵 {title}\n🎼 Format: {ext.upper()}\n\n📦 Download Link:\n{result['url']}"})
        return jsonify({"reply": f"❌ Could not extract audio.\n{result.get('error', 'Unknown error')}"})

    # 5. Recover Command
    elif incoming_text.startswith("/recover "):
        target_jid = incoming_text[9:].strip()
        if not target_jid:
            return jsonify({"reply": "⚠️ Please provide a contact number after /recover"})
        async with aiosqlite.connect(DB_FILE) as db:
            async with db.execute(
                "SELECT name, body FROM messages WHERE sender LIKE ? ORDER BY timestamp DESC LIMIT 5",
                (f"%{target_jid}%",)
            ) as cursor:
                rows = await cursor.fetchall()
                if not rows:
                    return jsonify({"reply": f"❌ No cached messages found for {target_jid}"})
                reply_text = f"🗑️ *Recovered Messages for {target_jid}:*\n\n" + \
                             "\n".join([f"👤 *{row[0]}*: {row[1]}" for row in rows])
                return jsonify({"reply": reply_text})

    return jsonify({"reply": "ℹ️ Unknown command. Use /ask, /paint, /download_video, /download_song or /recover"})




@app.route("/admin")
async def admin_panel():
    admin_path = Path(__file__).parent / "admin.html"
    if admin_path.exists():
        return Response(admin_path.read_text(encoding="utf-8"), mimetype="text/html")
    return jsonify({"error": "Not found"}), 404

@app.route("/admin/stats", methods=["GET"])
async def admin_stats():
    async with aiosqlite.connect(DB_FILE) as db:
        async with db.execute("SELECT COUNT(*) FROM contacts") as c:
            contacts = (await c.fetchone())[0]
        async with db.execute("SELECT COUNT(*) FROM messages") as c:
            messages = (await c.fetchone())[0]
        async with db.execute("SELECT COUNT(*) FROM viewonce_media") as c:
            viewonce = (await c.fetchone())[0]
        async with db.execute("SELECT name, sender, timestamp FROM contacts ORDER BY timestamp DESC LIMIT 20") as c:
            rows = await c.fetchall()
            recent_contacts = [{"name": r[0], "sender": r[1], "time": time.strftime("%d/%m %H:%M", time.localtime(r[2]))} for r in rows]
    session_list = [{"name": n, "number": i.get("number",""), "online": i.get("online",False), "msg_count": i.get("msg_count",0), "since": i.get("since","")} for n, i in SESSION_REGISTRY.items()]
    return jsonify({"sessions": len([s for s in session_list if s["online"]]), "contacts": contacts, "messages": messages, "viewonce": viewonce, "session_list": session_list, "recent_contacts": recent_contacts})

@app.route("/admin/terminate", methods=["POST"])
async def admin_terminate():
    data = await request.get_json() or {}
    name = data.get("session","")
    if name in SESSION_REGISTRY:
        SESSION_REGISTRY[name]["online"] = False
        SESSION_REGISTRY[name]["terminate"] = True
    return jsonify({"status": "terminated"})

@app.route("/admin/register-session", methods=["POST"])
async def register_session():
    data = await request.get_json() or {}
    name = data.get("name","unknown")
    SESSION_REGISTRY[name] = {"number": data.get("number",""), "online": data.get("online",False), "msg_count": 0, "since": time.strftime("%d/%m %H:%M")}
    return jsonify({"status": "registered"})

@app.route("/admin/update-session", methods=["POST"])
async def update_session():
    data = await request.get_json() or {}
    name = data.get("name","")
    if name in SESSION_REGISTRY:
        SESSION_REGISTRY[name].update({"online": data.get("online", True), "msg_count": data.get("msg_count", 0), "number": data.get("number", SESSION_REGISTRY[name].get("number",""))})
    return jsonify({"status": "updated"})

@app.route("/admin/check-terminate", methods=["POST"])
async def check_terminate():
    data = await request.get_json() or {}
    name = data.get("name","")
    return jsonify({"terminate": SESSION_REGISTRY.get(name, {}).get("terminate", False)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
