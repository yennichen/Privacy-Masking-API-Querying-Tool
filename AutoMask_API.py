import os
import time
import re
import json
import pyperclip
import keyboard
import winsound
import pyautogui
import threading
from urllib.parse import urlparse
from http.server import BaseHTTPRequestHandler, HTTPServer
from PIL import Image
import requests 

# =======================================================
# 🛑 CONFIGURATION & API KEYS
# =======================================================
# Do NOT share your keys. Use environment variables for production.
MORALIS_API_KEY = "YOUR_MORALIS_API_KEY_HERE"
TRONGRID_API_KEY = "YOUR_TRONGRID_API_KEY_HERE"

# --- Directory & Path Setup (Using Relative Paths) ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUTOMASK_DIR = os.path.join(BASE_DIR, "automask")
JSON_DIR = os.path.join(AUTOMASK_DIR, "json")
AI_BOT_IN_DIR = os.path.join(AUTOMASK_DIR, "screenshots_in")
EXTENSION_DIR = os.path.join(BASE_DIR, "AutoMask_Extension")

ENTITY_JSON_PATH = os.path.join(JSON_DIR, "entity_mapping.json")
SENSITIVE_JSON_PATH = os.path.join(JSON_DIR, "sensitive_data.json")

# Visual setting: percentage of the screen to crop (taskbar)
TASKBAR_HEIGHT_PERCENT = 0.05 

# Application State
state = {"url": "", "token": "", "addr": "", "last_clip": "", "expecting_url": False}
entity_mapping = {}
sensitive_data_list = []
last_hotkey_time = 0  # For debounce logic

# =======================================================
# 🔍 ON-CHAIN RADAR: SMART ROUTER
# =======================================================
def check_history_router(address, token):
    """
    Determines which API/Node to query based on the Token type.
    """
    token_up = token.upper()
    print(f"\n🔍 [Smart Radar Initiated] Target Address: {address} | Token: {token_up}")

    # 1. EVM Compatible Chains (via Moralis)
    evm_tokens = ["ETH", "USDT-ERC20", "USDC-ERC20", "BSC", "BNB", "USDT-BEP20", "POL", "MATIC", "AVAX", "ARB", "OP"]
    if token_up in evm_tokens:
        check_moralis(address, token_up)
    
    # 2. Solana (via Official Public RPC)
    elif token_up in ["SOL", "SOLANA"]:
        check_solana(address)
    
    # 3. TRON Ecosystem (via TronGrid)
    elif token_up in ["TRX", "USDT-TRC20"]:
        check_trongrid(address)
    
    # 4. Bitcoin (via Mempool.space)
    elif token_up in ["BTC", "BITCOIN"]:
        check_utxo(address, "BTC", f"https://mempool.space/api/address/{address}")
    
    # 5. Litecoin (via Litecoinspace)
    elif token_up in ["LTC", "LITECOIN"]:
        check_utxo(address, "LTC", f"https://litecoinspace.org/api/address/{address}")
    
    # 6. TON (via TonAPI)
    elif token_up in ["TON", "TONCOIN"]:
        check_ton(address)
    
    # 7. Privacy Tokens (Tracking blocked by design)
    elif token_up in ["XMR", "ZEC"]:
        print(f"⚠️ [Privacy Coin] {token_up} tracking is impossible via public APIs.")
        print_ready_prompt()
    
    # 8. Unsupported or Manual Check Required
    elif token_up in ["USDT-TRX", "ADA", "DOT", "ATOM", "EOS"]:
        print(f"⚪ [Manual Check Required] Radar not integrated for {token_up}.")
        print_ready_prompt()
    else:
        print(f"⚪ [Manual Check Required] Unrecognized token '{token_up}'.")
        print_ready_prompt()

# --- API Engines ---

def check_solana(address):
    """Query Solana Mainnet signatures."""
    url = "https://api.mainnet-beta.solana.com"
    payload = {
        "jsonrpc": "2.0", "id": 1, "method": "getSignaturesForAddress",
        "params": [address, {"limit": 1}]
    }
    try:
        res = requests.post(url, json=payload, timeout=10).json()
        if "result" in res:
            tx_list = res["result"]
            print_result("Solana Public RPC", len(tx_list) > 0, "Multiple" if len(tx_list) > 0 else 0)
    except Exception as e: print(f"❌ [Error] {e}")

def check_moralis(address, token_up):
    """Query EVM history via Moralis."""
    if "YOUR_" in MORALIS_API_KEY: return print("⚠️ Moralis Key Missing")
    chain_map = {
        "ETH": "eth", "USDT-ERC20": "eth", "USDC-ERC20": "eth",
        "BSC": "bsc", "USDT-BEP20": "bsc", "BNB": "bsc",
        "POL": "polygon", "MATIC": "polygon", "AVAX": "avalanche", "ARB": "arbitrum", "OP": "optimism"
    }
    target_chain = chain_map.get(token_up, "eth")
    url = f"https://deep-index.moralis.io/api/v2.2/{address}?chain={target_chain}"
    headers = {"X-API-Key": MORALIS_API_KEY}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            tx_list = res.json().get("result", [])
            print_result("Moralis", len(tx_list) > 0, len(tx_list))
    except Exception as e: print(f"❌ [Error] {e}")

def check_trongrid(address):
    """Query TRON account status via TronGrid."""
    if "YOUR_" in TRONGRID_API_KEY: return print("⚠️ TronGrid Key Missing")
    url = f"https://api.trongrid.io/v1/accounts/{address}"
    headers = {"TRON-PRO-API-KEY": TRONGRID_API_KEY}
    try:
        res = requests.get(url, headers=headers, timeout=10).json()
        if res.get("success"):
            data = res.get("data", [])
            print_result("TronGrid", len(data) > 0, "Multiple" if len(data) > 0 else 0)
    except Exception as e: print(f"❌ [Error] {e}")

def check_utxo(address, coin_name, url):
    """Generic UTXO query (BTC/LTC)."""
    try:
        res = requests.get(url, timeout=10)
        if res.status_code == 200:
            tx_count = res.json().get("chain_stats", {}).get("tx_count", 0)
            print_result(coin_name, tx_count > 0, tx_count)
    except Exception as e: print(f"❌ [Error] {e}")

def check_ton(address):
    """Query TON account status."""
    url = f"https://tonapi.io/v2/accounts/{address}"
    try:
        res = requests.get(url, timeout=10).json()
        status = res.get("status", "")
        print_result("TonAPI", status == "active", "Multiple" if status == "active" else 0)
    except Exception as e: print(f"❌ [Error] {e}")

def print_result(engine_name, has_history, tx_count):
    print("\n" + "="*60)
    print(f"📡 Data Source: {engine_name}")
    if has_history:
        print(f"🚨 [ALERT! ACTIVE ADDRESS] History found! (Tx count: {tx_count})")
    else:
        print(f"🟢 [NEW ADDRESS] No transaction history found.")
    print("="*60)
    print_ready_prompt()

def print_ready_prompt():
    print("\n▶️  Ready for next capture. Press [Win + W] or [Alt + W] to start.")

# =======================================================
# 🌐 CHROME EXTENSION BUILDER
# =======================================================
def build_chrome_extension():
    if not os.path.exists(EXTENSION_DIR): os.makedirs(EXTENSION_DIR)
    manifest = {
        "manifest_version": 3,
        "name": "Chainlabs AutoMask Shutter",
        "version": "2.6",
        "action": { "default_title": "Click to mask and screenshot" },
        "background": { "service_worker": "background.js" },
        "permissions": ["activeTab", "scripting"],
        "host_permissions": ["http://127.0.0.1/*", "http://localhost/*"]
    }
    bg_js = r"""
    chrome.action.onClicked.addListener((tab) => {
      fetch('http://127.0.0.1:9999/get_secrets')
        .then(res => res.json())
        .then(data => {
          chrome.scripting.executeScript({
            target: { tabId: tab.id },
            func: maskPage,
            args: [data.secrets, data.memo_final]
          });
        })
        .catch(err => alert("⚠️ Connection to Python server failed!"));
    });

    function maskPage(secrets, memo) {
      const styleId = 'chainlabs-mosaic-style';
      if (!document.getElementById(styleId)) {
        const style = document.createElement('style');
        style.id = styleId;
        const pattern = 'url("data:image/svg+xml;utf8,<svg width=\'24\' height=\'24\' viewbox=\'0 0 24 24\' xmlns=\'http://www.w3.org/2000/svg\'><rect x=\'0\' y=\'0\' width=\'6\' height=\'6\' fill=\'%23000000\'/><rect x=\'6\' y=\'0\' width=\'6\' height=\'6\' fill=\'%23111111\'/><rect x=\'12\' y=\'0\' width=\'6\' height=\'6\' fill=\'%23000000\'/><rect x=\'18\' y=\'0\' width=\'6\' height=\'6\' fill=\'%23111111\'/></svg>")';
        style.innerHTML = `.cl-mask-item { background-image: ${pattern} !important; background-size: 10px 10px !important; color: transparent !important; display: inline-block !important; border-radius: 2px !important; }`;
        document.head.appendChild(style);
      }
      let found = [];
      const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
      let n;
      let nodes = [];
      while (n = walker.nextNode()) { nodes.push(n); }
      const sortedSecrets = secrets.filter(x => x && x.trim()).sort((a,b) => b.length - a.length);
      nodes.forEach(node => {
        let parent = node.parentNode;
        if (!parent || ['SCRIPT', 'STYLE', 'TEXTAREA', 'INPUT'].includes(parent.tagName)) return;
        let html = node.nodeValue;
        let matched = false;
        sortedSecrets.forEach(x => {
          const regex = new RegExp(x.replace(/[-[\]{}()*+?.,\\\\^$|#\\s]/g, '\\\\$&'), 'gi');
          if (regex.test(html)) {
            html = html.replace(regex, `<span class="cl-mask-item">$&</span>`);
            if (!found.includes(x)) found.push(x);
            matched = true;
          }
        });
        if (matched) {
          const span = document.createElement('span');
          span.innerHTML = html;
          parent.replaceChild(span, node);
        }
      });
      setTimeout(() => {
        fetch('http://127.0.0.1:9999/take_screenshot', {
          method: 'POST', body: JSON.stringify({ memo: memo, found: found })
        });
      }, 1500); 
    }
    """
    with open(os.path.join(EXTENSION_DIR, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=4, ensure_ascii=False)
    with open(os.path.join(EXTENSION_DIR, "background.js"), "w", encoding="utf-8") as f:
        f.write(bg_js)

# =======================================================
# 📡 SERVER & INITIALIZATION
# =======================================================
def init_env():
    for d in [AI_BOT_IN_DIR, JSON_DIR]:
        if not os.path.exists(d): os.makedirs(d)
    global entity_mapping, sensitive_data_list
    if os.path.exists(ENTITY_JSON_PATH):
        with open(ENTITY_JSON_PATH, "r", encoding="utf-8") as f:
            entity_mapping = {k.lower(): str(v) for k, v in json.load(f).items()}
    if os.path.exists(SENSITIVE_JSON_PATH):
        with open(SENSITIVE_JSON_PATH, "r", encoding="utf-8") as f:
            sensitive_data_list = [s for s in json.load(f) if s]

    print("\n" + "="*60)
    print(" 🛡️  Chainlabs AutoMask & Radar Tracker (V51)")
    print("="*60)
    print(f" ✅ Loaded {len(sensitive_data_list)} sensitive entries.")
    print("\n ⌨️  Hotkeys Configuration:")
    print("   [Win + W] or [Alt + W] : Start sequence")
    print("   [Win + R] or [Alt + R] : Reset state")
    print("="*60)
    print_ready_prompt()
    build_chrome_extension()

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/get_secrets':
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            clip = pyperclip.paste().strip()
            memo = clip if clip and clip not in [state["addr"], state["url"], state["token"]] and not clip.startswith("http") else "NA"
            self.wfile.write(json.dumps({"secrets": sensitive_data_list, "memo_final": memo}).encode())

    def do_POST(self):
        if self.path == '/take_screenshot':
            data = json.loads(self.rfile.read(int(self.headers['Content-Length'])).decode('utf-8'))
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            shot = pyautogui.screenshot()
            final_img = shot.crop((0, 0, shot.width, shot.height - int(shot.height * TASKBAR_HEIGHT_PERCENT)))
            netloc = urlparse(state["url"]).netloc if state["url"] else ""
            domain = netloc.split('.')[-2].lower() if '.' in netloc else "unknown"
            filename = f"{entity_mapping.get(domain, '99999')}_{domain.capitalize()}_{state['token'] or 'UKN'}_{re.sub(r'[^a-zA-Z0-9]', '', state['addr']) if state['addr'] else 'NOADDR'}_{data.get('memo','NA')}.png"
            final_img.save(os.path.join(AI_BOT_IN_DIR, filename))
            winsound.Beep(1000, 400)
            print(f"💾 Screenshot saved: {filename}")
            if state["addr"] and state["token"]:
                threading.Thread(target=check_history_router, args=(state["addr"], state["token"])).start()
            else: print_ready_prompt()
            state.update({"url": "", "token": "", "addr": ""})
            self.wfile.write(b"OK")
    def log_message(self, format, *args): return

def trigger_record():
    global last_hotkey_time
    if time.time() - last_hotkey_time < 0.5: return
    last_hotkey_time = time.time()
    winsound.Beep(500, 200)
    state.update({"expecting_url": True})
    print("\n🔗 Recording started. Please copy URL (Ctrl+C)...")

def trigger_reset():
    global last_hotkey_time
    if time.time() - last_hotkey_time < 0.5: return
    last_hotkey_time = time.time()
    winsound.Beep(400, 500)
    state.update({"url": "", "token": "", "addr": "", "last_clip": "", "expecting_url": False})
    print("\n🔄 State reset! Press [Win + W] to start again.")

def run_v4_engine():
    init_env()
    for key in ['win+w', 'win+W', 'win+shift+w', 'alt+w', 'alt+W']:
        try: keyboard.add_hotkey(key, trigger_record)
        except: pass
    for key in ['win+r', 'win+R', 'win+shift+r', 'alt+r', 'alt+R']:
        try: keyboard.add_hotkey(key, trigger_reset)
        except: pass
    threading.Thread(target=lambda: HTTPServer(('127.0.0.1', 9999), RequestHandler).serve_forever(), daemon=True).start()
    while True:
        try: raw = pyperclip.paste().strip()
        except: time.sleep(0.1); continue
        if raw != state["last_clip"] and raw != "":
            state["last_clip"] = raw
            if state["expecting_url"] and raw.startswith("http"):
                state["url"], state["expecting_url"] = raw, False
                winsound.Beep(600, 150)
                print(f"✅ URL: {raw}")
            elif len(raw) >= 26 and not raw.startswith("http") and state["url"] and not state["addr"]:
                state["addr"] = raw
                winsound.Beep(800, 200)
                print(f"✅ Address: {raw}")
            elif 2 <= len(raw) <= 25 and state["url"] and state["token"] == "":
                state["token"] = raw.upper()
                winsound.Beep(800, 150)
                print(f"✅ Token: {state['token']}")
        time.sleep(0.1)

if __name__ == "__main__":
    run_v4_engine()