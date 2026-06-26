const {
  default: makeWASocket,
  useMultiFileAuthState,
  DisconnectReason,
  delay,
  fetchLatestBaileysVersion,
  downloadMediaMessage
} = require("@whiskeysockets/baileys");
const { Boom } = require("@hapi/boom");
const axios = require("axios");
const readline = require("readline");
const fs = require("fs");
const path = require("path");
const pino = require("pino");
const qrcode = require("qrcode-terminal");
const http = require('http');
let pendingPairResolve = null;
let lastPairingCode = null;
let lastPairingNumber = null;
let botOnline = false;
const pairServer = http.createServer(async (req, res) => {
  const url = new URL(req.url, 'http://' + req.headers.host);
  if (req.method === 'GET' && url.pathname === '/pair') {
    res.writeHead(200, {'Content-Type': 'text/html'});
    res.end('<!DOCTYPE html><html><head><title>Shark Bot Pair</title><meta name=viewport content=width=device-width,initial-scale=1><style>*{box-sizing:border-box;margin:0;padding:0}body{background:#0f172a;color:#e2e8f0;font-family:Arial,sans-serif;display:flex;align-items:center;justify-content:center;min-height:100vh;padding:20px}.card{background:#1e293b;border-radius:16px;padding:32px;max-width:420px;width:100%;border:1px solid #334155}h1{color:#38bdf8;font-size:24px;margin-bottom:8px}p{color:#94a3b8;margin-bottom:24px;font-size:14px}input{width:100%;padding:14px;border-radius:10px;border:1px solid #475569;background:#0f172a;color:#e2e8f0;font-size:16px;margin-bottom:16px}button{width:100%;padding:14px;border-radius:10px;background:#0ea5e9;color:white;font-size:16px;font-weight:bold;border:none;cursor:pointer}.code{background:#0f172a;border:2px solid #38bdf8;border-radius:12px;padding:20px;text-align:center;margin-top:20px;font-size:32px;font-weight:bold;letter-spacing:8px;color:#38bdf8}.steps{margin-top:16px;background:#0f172a;border-radius:10px;padding:16px;font-size:13px;color:#94a3b8;line-height:1.8}</style></head><body><div class=card><h1>🦈 Shark Bot</h1><p>Enter your WhatsApp number to get a pairing code</p>' + (lastPairingCode ? '<div class=code>' + lastPairingCode + '</div><p style=margin-top:12px;color:#93c5fd>For: +' + lastPairingNumber + '</p>' : '') + '<form method=POST action=/pair style=margin-top:20px><input type=tel name=number placeholder="e.g. 254712345678" required><button type=submit>Get Pairing Code</button></form><div class=steps><b>How to link:</b><br>1. Enter your number<br>2. Copy the code<br>3. WhatsApp → Linked Devices<br>4. Link with phone number<br>5. Enter the code</div></div></body></html>');
    return;
  }
  if (req.method === 'POST' && url.pathname === '/pair') {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => {
      const params = new URLSearchParams(body);
      const number = (params.get('number') || '').replace(/[s-+]/g, '');
      if (number && pendingPairResolve) { lastPairingNumber = number; pendingPairResolve(number); pendingPairResolve = null; }
      res.writeHead(302, {Location: '/pair'}); res.end();
    });
    return;
  }
  res.writeHead(200, {'Content-Type': 'application/json'});
  res.end(JSON.stringify({status:'ok',online:botOnline}));
});
pairServer.listen(process.env.WEB_PORT || 3000, () => console.log('🌐 Pair UI: http://localhost:' + (process.env.WEB_PORT || 3000) + '/pair'));

const http = require('http');
let pendingPairResolve = null;
let lastPairingCode = null;
let lastPairingNumber = null;
let botOnline = false;
const pairServer = http.createServer(async (req, res) => {
  const url = new URL(req.url, 'http://' + req.headers.host);
  if (req.method === 'GET' && url.pathname === '/pair') {
    res.writeHead(200, {'Content-Type': 'text/html'});
    res.end('<!DOCTYPE html><html><head><title>Shark Bot Pair</title><meta name=viewport content=width=device-width,initial-scale=1><style>*{box-sizing:border-box;margin:0;padding:0}body{background:#0f172a;color:#e2e8f0;font-family:Arial,sans-serif;display:flex;align-items:center;justify-content:center;min-height:100vh;padding:20px}.card{background:#1e293b;border-radius:16px;padding:32px;max-width:420px;width:100%;border:1px solid #334155}h1{color:#38bdf8;font-size:24px;margin-bottom:8px}p{color:#94a3b8;margin-bottom:24px;font-size:14px}input{width:100%;padding:14px;border-radius:10px;border:1px solid #475569;background:#0f172a;color:#e2e8f0;font-size:16px;margin-bottom:16px}button{width:100%;padding:14px;border-radius:10px;background:#0ea5e9;color:white;font-size:16px;font-weight:bold;border:none;cursor:pointer}.code{background:#0f172a;border:2px solid #38bdf8;border-radius:12px;padding:20px;text-align:center;margin-top:20px;font-size:32px;font-weight:bold;letter-spacing:8px;color:#38bdf8}.steps{margin-top:16px;background:#0f172a;border-radius:10px;padding:16px;font-size:13px;color:#94a3b8;line-height:1.8}</style></head><body><div class=card><h1>🦈 Shark Bot</h1><p>Enter your WhatsApp number to get a pairing code</p>' + (lastPairingCode ? '<div class=code>' + lastPairingCode + '</div><p style=margin-top:12px;color:#93c5fd>For: +' + lastPairingNumber + '</p>' : '') + '<form method=POST action=/pair style=margin-top:20px><input type=tel name=number placeholder="e.g. 254712345678" required><button type=submit>Get Pairing Code</button></form><div class=steps><b>How to link:</b><br>1. Enter your number<br>2. Copy the code<br>3. WhatsApp → Linked Devices<br>4. Link with phone number<br>5. Enter the code</div></div></body></html>');
    return;
  }
  if (req.method === 'POST' && url.pathname === '/pair') {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => {
      const params = new URLSearchParams(body);
      const number = (params.get('number') || '').replace(/[s-+]/g, '');
      if (number && pendingPairResolve) { lastPairingNumber = number; pendingPairResolve(number); pendingPairResolve = null; }
      res.writeHead(302, {Location: '/pair'}); res.end();
    });
    return;
  }
  res.writeHead(200, {'Content-Type': 'application/json'});
  res.end(JSON.stringify({status:'ok',online:botOnline}));
});
pairServer.listen(process.env.WEB_PORT || 3000, () => console.log('🌐 Pair UI: http://localhost:' + (process.env.WEB_PORT || 3000) + '/pair'));


const logger = pino({ level: "silent" });
const BACKEND_URL = "http://127.0.0.1:5000";

// Env vars let the bot start unattended on Railway/Render, where there is no
// interactive terminal to answer the session-name / linking-method prompts.
const SESSION_ID_ENV = (process.env.SESSION_ID || "").trim();
const PAIRING_NUMBER_ENV = (process.env.PAIRING_NUMBER || "").replace(/[\s\-\+]/g, "");
const IS_INTERACTIVE = Boolean(process.stdin.isTTY);

const apiClient = axios.create({
  baseURL: BACKEND_URL,
  timeout: 45000,
  maxContentLength: Infinity,
  maxBodyLength: Infinity
});

// Sessions directory
const SESSIONS_DIR = "./sessions";
if (!fs.existsSync(SESSIONS_DIR)) fs.mkdirSync(SESSIONS_DIR, { recursive: true });

function prompt(question) {
  return new Promise((resolve) => {
    const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
    rl.question(question, (answer) => {
      rl.close();
      resolve(answer.trim());
    });
  });
}

function printBanner() {
  console.log("\n╔══════════════════════════════════════╗");
  console.log("   🦈 SHARK BOT — HENRY BOTS© V5.0 🦈   ");
  console.log("╚══════════════════════════════════════╝\n");
}

async function askLinkingMethod() {
  console.log("1️⃣  QR Code  - Scan with WhatsApp camera");
  console.log("2️⃣  Pairing Code - Enter code in WhatsApp\n");
  const answer = await prompt("Choose method (1 or 2): ");
  return answer;
}

async function askPhoneNumber() {
  const num = await prompt("Enter phone number with country code (e.g. 2547XXXXXXXX): ");
  // Strip spaces, dashes, plus sign
  return num.replace(/[\s\-\+]/g, "");
}

async function askSessionId() {
  if (SESSION_ID_ENV) return SESSION_ID_ENV;
  if (!IS_INTERACTIVE) {
    console.log("ℹ️  No TTY detected and no SESSION_ID env var set — using 'default'.");
    return "default";
  }
  const existing = fs.readdirSync(SESSIONS_DIR).filter(f =>
    fs.statSync(path.join(SESSIONS_DIR, f)).isDirectory()
  );
  if (existing.length > 0) {
    console.log("\n📂 Existing sessions:");
    existing.forEach((s, i) => console.log(`   ${i + 1}. ${s}`));
  }
  const answer = await prompt("\nEnter session name (e.g. mybot or your name): ");
  return answer || "default";
}

async function startSession(sessionId) {
  const sessionPath = path.join(SESSIONS_DIR, sessionId);
  const { state, saveCreds } = await useMultiFileAuthState(sessionPath);

  // Fetch latest Baileys version for best compatibility
  const { version } = await fetchLatestBaileysVersion();
  console.log(`\n📦 Using Baileys WA version: ${version.join(".")}`);

  let usePairingCode = false;
  let phoneNumber = "";

  if (!state.creds.registered) {
    if (PAIRING_NUMBER_ENV) {
      usePairingCode = true;
      phoneNumber = PAIRING_NUMBER_ENV;
      console.log(`🔢 Using pairing code linking for ${phoneNumber} (from PAIRING_NUMBER env var).`);
    } else if (IS_INTERACTIVE) {
      const method = await askLinkingMethod();
      if (method === "2") {
        usePairingCode = true;
        phoneNumber = await askPhoneNumber();
      }
    } else {
      console.log("ℹ️  No TTY and no PAIRING_NUMBER env var — falling back to QR code.");
      console.log("📷 Watch this process's logs for the QR code and scan it before it expires.");
    }
  }

  const socket = makeWASocket({
    version,
    auth: state,
    printQRInTerminal: false,
    logger,
    markOnlineOnConnect: true,
    generateHighQualityLinkPreview: true,
    // Helps avoid bans — don't look like web browser
    browser: ["Ubuntu", "Chrome", "20.0.04"]
  });

  // Pairing code generation
  if (usePairingCode && !state.creds.registered) {
    await delay(3000); // Wait for socket to initialize
    try {
      const code = await socket.requestPairingCode(phoneNumber);
      console.log("\n╔══════════════════════════════════════╗");
      console.log(`   🔑 PAIRING CODE: ${code.match(/.{1,4}/g).join("-")}  `);
      console.log("╚══════════════════════════════════════╝");
      console.log("\n📱 Steps:");
      console.log("1. Open WhatsApp");
      console.log("2. Go to Linked Devices");
      console.log("3. Tap Link a Device");
      console.log("4. Tap 'Link with phone number instead'");
      console.log("5. Enter the code above\n");
    } catch (e) {
      console.error("❌ Pairing code error:", e.message);
      console.log("💡 Try method 1 (QR Code) instead, or check your phone number.");
    }
  }

  socket.ev.on("creds.update", saveCreds);

  // Feature: Anti-Call
  socket.ev.on("call", async (inboundCall) => {
    for (const call of inboundCall) {
      if (call.status === "offer") {
        try {
          await socket.rejectCall(call.id, call.from);
          console.log(`🚫 [${sessionId}] AntiCall: rejected call from ${call.from}`);
        } catch (e) {
          console.error("❌ AntiCall error:", e.message);
        }
      }
    }
  });

  socket.ev.on("messages.upsert", async (chatUpdate) => {
    try {
      const msg = chatUpdate.messages[0];
      if (!msg || !msg.message) return;

      const sender = msg.key.remoteJid;
      if (!sender) return;

      const isStatus = sender === "status@broadcast";
      const name = msg.pushName || "User";
      const msgId = msg.key.id;

      // Extract message body from all common message types
      const body =
        msg.message?.conversation ||
        msg.message?.extendedTextMessage?.text ||
        msg.message?.imageMessage?.caption ||
        msg.message?.videoMessage?.caption ||
        msg.message?.buttonsResponseMessage?.selectedButtonId ||
        msg.message?.listResponseMessage?.singleSelectReply?.selectedRowId ||
        "";

      // Feature: Auto View & Like Status
      if (isStatus) {
        try {
          await socket.readMessages([msg.key]);
          // Send status reaction properly
          await socket.sendMessage(
            sender,
            { react: { text: "❤️", key: msg.key } },
            { statusJidList: [msg.key.participant || sender] }
          );
        } catch (e) {
          // Status reactions can fail silently — it's fine
        }
        return;
      }

      if (msg.key.fromMe) return;

      // Feature: Auto Read Messages
      try {
        await socket.readMessages([msg.key]);
      } catch (e) {}

      // Log message to DB for /recover
      if (body) {
        apiClient.post("/log-message", { msg_id: msgId, sender, name, body }).catch(() => {});
      }

      // Feature: Save View Once Media
      const viewOnceMsg =
        msg.message?.viewOnceMessage?.message ||
        msg.message?.viewOnceMessageV2?.message ||
        msg.message?.viewOnceMessageV2Extension?.message;

      if (viewOnceMsg) {
        try {
          const mediaType = Object.keys(viewOnceMsg)[0]; // imageMessage | videoMessage | audioMessage
          const inner = viewOnceMsg[mediaType] || {};
          const caption = inner.caption ? `\n${inner.caption}` : "";

          // downloadMediaMessage needs a {key, message} shaped object pointing
          // at the *inner* media message, not the viewOnceMessage wrapper.
          const fakeMsg = { key: msg.key, message: viewOnceMsg };
          const buffer = await downloadMediaMessage(
            fakeMsg,
            "buffer",
            {},
            { logger, reuploadRequest: socket.updateMediaMessage }
          );

          await socket.sendMessage(selfJid, {
            text: `📸 *View Once received from ${name} (${sender})*`
          });

          if (mediaType === "imageMessage") {
            await socket.sendMessage(selfJid, { image: buffer, caption: `Saved view-once image${caption}` });
          } else if (mediaType === "videoMessage") {
            await socket.sendMessage(selfJid, { video: buffer, caption: `Saved view-once video${caption}` });
          } else if (mediaType === "audioMessage") {
            await socket.sendMessage(selfJid, {
              audio: buffer,
              mimetype: inner.mimetype || "audio/ogg; codecs=opus",
              ptt: true
            });
          }
        } catch (e) {
          console.error(`❌ [${sessionId}] View-once save failed:`, e.message);
        }
      }

      // Feature: Auto Save Contacts & Welcome Message
      try {
        const registry = await apiClient.post("/auto-save", { sender, name });
        if (registry?.data?.status === "new_user_registered") {
          await socket.sendMessage(sender, { text: registry.data.welcome_message });
          return; // Don't react/process commands on first message
        }
      } catch (e) {}

      // Feature: Auto React to messages
      if (body) {
        try {
          const sentiment = await apiClient.post("/react", { body });
          if (sentiment?.data?.emoji) {
            await socket.sendMessage(sender, {
              react: { text: sentiment.data.emoji, key: msg.key }
            });
          }
        } catch (e) {}
      }

      // Core Command Handler (slash commands only)
      if (body.startsWith("/")) {
        const humanDelay = Math.floor(Math.random() * 1500) + 800;
        await delay(humanDelay);

        const presenceType = body.startsWith("/download_song") ? "recording" : "composing";
        try { await socket.sendPresenceUpdate(presenceType, sender); } catch (e) {}

        try {
          const response = await apiClient.post("/webhook", { body, sender });
          const data = response.data;

          try { await socket.sendPresenceUpdate("paused", sender); } catch (e) {}

          if (data.type === "image" && data.url) {
            await socket.sendMessage(sender, { image: { url: data.url }, caption: data.caption || "" });
          } else if (data.type === "video" && data.url) {
            await socket.sendMessage(sender, { video: { url: data.url }, caption: data.caption || "", mimetype: "video/mp4" });
          } else if (data.type === "audio" && data.url) {
            await socket.sendMessage(sender, { audio: { url: data.url }, mimetype: "audio/mpeg", ptt: false });
          } else if (data.reply) {
            await socket.sendMessage(sender, { text: data.reply });
          }
        } catch (e) {
          await socket.sendMessage(sender, { text: `❌ Bot error: ${e.message}` });
        }
      }
    } catch (error) {
      console.error(`❌ [${sessionId}] Message handler error:`, error.message);
    }
  });

  // Feature: Auto Bio Update every 60 seconds
  setInterval(async () => {
    try {
      const bioResponse = await apiClient.get("/get-bio");
      if (bioResponse?.data?.bio) {
        await socket.updateProfileStatus(bioResponse.data.bio);
      }
    } catch (e) {}
  }, 60000);

  // Feature: Always Online — re-announce presence every 10 minutes
  setInterval(async () => {
    try {
      await socket.sendPresenceUpdate("available");
    } catch (e) {}
  }, 10 * 60 * 1000);

  // Connection state handler with null-safety fix
  socket.ev.on("connection.update", (update) => {
    const { connection, lastDisconnect, qr } = update;

    if (qr) {
      console.log("\n📷 QR code ready — scan it with WhatsApp now!\n");
      qrcode.generate(qr, { small: true });
    }

    if (connection === "connecting") {
      console.log(`🔗 [${sessionId}] Connecting to WhatsApp...`);
    }

    if (connection === "open") {
      console.log(`\n✅ [${sessionId}] SHARK BOT IS ONLINE AND READY! 🦈\n`); botOnline = true; botOnline = true;
    }

    if (connection === "close") {
      // FIX: lastDisconnect can be null/undefined — always guard it
      const statusCode = lastDisconnect?.error instanceof Boom
        ? lastDisconnect.error.output?.statusCode
        : null;

      const loggedOut = statusCode === DisconnectReason.loggedOut;

      if (loggedOut) {
        console.log(`🚪 [${sessionId}] Logged out. Delete session folder and restart to relink.`);
      } else {
        const reason = statusCode ? `(code: ${statusCode})` : "(unknown reason)";
        console.log(`🔄 [${sessionId}] Reconnecting... ${reason}`);
        // Exponential backoff — wait 3s before reconnecting
        setTimeout(() => startSession(sessionId), 3000);
      }
    }
  });
}

async function main() {
  printBanner();
  const sessionId = await askSessionId();
  console.log(`\n🚀 Starting session: "${sessionId}"...`);
  await startSession(sessionId);
}

main().catch((err) => {
  console.error("❌ Fatal error:", err.message);
  process.exit(1);
});
