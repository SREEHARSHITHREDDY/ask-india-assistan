"""
============================================================
   Project : India-Only AI Assistant
   API Used: Groq (FREE)
   Author  : Sreeharshith Reddy
   Run     : python "Ask India Assistant.py"
   Then    : Open http://localhost:5000 in your browser
============================================================
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json, urllib.request, urllib.error, webbrowser, threading, os

# ── API Key (hidden from UI) ──────────────────────────────
API_KEY  = "YOUR_GROQ_API_KEY_HERE"   # <-- paste your gsk_... key here
MODEL    = "llama-3.3-70b-versatile"
PORT     = 5000

SYSTEM_PROMPT = """You are an expert AI assistant on everything related to India.
Your ONLY job is to answer questions about India and Indian topics.
This includes: Indian states, cities, tourist places, temples, monuments, national parks,
history, culture, traditions, festivals, religions, food, geography, rivers, mountains,
climate, politics, government, economy, sports, cricket, cinema, famous people, languages.
IMPORTANT: The user does NOT need to say the word "India" in the question.
Questions about Goa beaches, Kerala backwaters, Hampi temples, Hyderabad biryani,
Rajasthan forts, Kaziranga Park, Varanasi ghats, Sachin Tendulkar etc. are India-related — answer them fully.
STRICT RULE: If the question is completely unrelated to India, respond with EXACTLY:
"I am sorry, I can only talk about India."
Do NOT add extra words. Just that exact sentence."""

# ── HTML UI (embedded) ───────────────────────────────────
HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>BharatAI — India Only Assistant</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet"/>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--saffron:#FF6B00;--saffron-l:#FF8C33;--saffron-p:#FFF3E8;--green:#0A6E3F;--green-l:#E8F5EE;--navy:#0D1B2A;--white:#FDFCF8;--gray:#6B7280;--gray-l:#F5F4F0;--border:#E8E4DC}
body{font-family:'DM Sans',sans-serif;background:var(--white);color:var(--navy);min-height:100vh;display:flex;flex-direction:column}
header{display:flex;align-items:center;justify-content:space-between;padding:1rem 2rem;border-bottom:1px solid var(--border);background:var(--white);position:sticky;top:0;z-index:10}
.logo{display:flex;align-items:center;gap:12px}
.flag-strip{display:flex;flex-direction:column;width:28px;height:20px;border-radius:3px;overflow:hidden;border:1px solid #ddd}
.fs1{flex:1;background:#FF9933}.fs2{flex:1;background:white;display:flex;align-items:center;justify-content:center}.fs3{flex:1;background:#138808}
.chakra-sm{width:7px;height:7px;border:1.5px solid #000080;border-radius:50%}
.logo-text{font-family:'Playfair Display',serif;font-size:20px;font-weight:700;color:var(--navy)}
.logo-text span{color:var(--saffron)}
.header-right{display:flex;align-items:center;gap:10px}
.status-pill{display:flex;align-items:center;gap:6px;font-size:12px;padding:4px 12px;border-radius:20px;background:var(--green-l);color:var(--green);font-weight:500;border:1px solid #C6E8D6}
.sdot{width:7px;height:7px;border-radius:50%;background:#22c55e}
.app-layout{display:flex;flex:1;height:calc(100vh - 61px)}
.sidebar{width:260px;border-right:1px solid var(--border);display:flex;flex-direction:column;padding:1.5rem 1rem;gap:1.5rem;background:var(--gray-l);flex-shrink:0;overflow-y:auto}
.sec-title{font-size:11px;font-weight:500;letter-spacing:.08em;text-transform:uppercase;color:var(--gray);margin-bottom:8px}
.stats-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.stat-card{background:var(--white);border:1px solid var(--border);border-radius:8px;padding:10px;text-align:center}
.stat-num{font-size:20px;font-weight:700;color:var(--saffron);font-family:'Playfair Display',serif}
.stat-label{font-size:11px;color:var(--gray);margin-top:2px}
.qbtn{display:block;width:100%;text-align:left;padding:8px 12px;border-radius:8px;border:1px solid var(--border);background:var(--white);font-size:13px;color:var(--navy);cursor:pointer;transition:all .15s;margin-bottom:6px;font-family:'DM Sans',sans-serif;line-height:1.4}
.qbtn:hover{border-color:var(--saffron);background:var(--saffron-p);color:var(--saffron)}
.chat-area{flex:1;display:flex;flex-direction:column;overflow:hidden}
.chat-msgs{flex:1;overflow-y:auto;padding:1.5rem 2rem;display:flex;flex-direction:column;gap:1.25rem}
.welcome{display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;text-align:center;padding:2rem;animation:fadeIn .5s ease}
.wflag{display:flex;flex-direction:column;width:64px;height:44px;border-radius:5px;overflow:hidden;margin-bottom:1.5rem;border:1.5px solid #ddd}
.wf1{flex:1;background:#FF9933}.wf2{flex:1;background:white;display:flex;align-items:center;justify-content:center}.wf3{flex:1;background:#138808}
.chakra-lg{width:16px;height:16px;border:2.5px solid #000080;border-radius:50%}
.welcome h2{font-family:'Playfair Display',serif;font-size:28px;font-weight:700;color:var(--navy);margin-bottom:8px}
.welcome p{font-size:15px;color:var(--gray);max-width:420px;line-height:1.6}
.chips{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin-top:1.5rem;max-width:500px}
.chip{padding:6px 14px;border-radius:20px;border:1px solid var(--border);font-size:13px;cursor:pointer;background:var(--white);color:var(--navy);transition:all .15s}
.chip:hover{background:var(--saffron-p);border-color:var(--saffron);color:var(--saffron)}
.msg-row{display:flex;gap:10px;align-items:flex-start;animation:slideUp .25s ease}
.msg-row.user{flex-direction:row-reverse}
.av-you{width:32px;height:32px;border-radius:50%;background:var(--navy);color:white;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:600;flex-shrink:0;margin-top:2px}
.av-flag{display:flex;flex-direction:column;width:32px;height:32px;border-radius:50%;overflow:hidden;border:1.5px solid #FFD4A8;flex-shrink:0;margin-top:2px}
.af1{flex:1;background:#FF9933}.af2{flex:1;background:white}.af3{flex:1;background:#138808}
.bwrap{max-width:72%}
.bubble{padding:10px 14px;border-radius:14px;font-size:14px;line-height:1.65;color:var(--navy)}
.bubble.bot{background:var(--white);border:1px solid var(--border);border-top-left-radius:4px}
.bubble.user{background:var(--saffron);color:white;border-top-right-radius:4px}
.bubble.blocked{background:#FEF2F2;border:1px solid #FECACA;color:#991B1B;border-top-left-radius:4px}
.mtag{display:inline-flex;align-items:center;gap:4px;font-size:11px;margin-top:5px;padding:2px 8px;border-radius:10px}
.t-india{background:var(--green-l);color:var(--green)}.t-block{background:#FEF2F2;color:#DC2626}
.tdot{width:5px;height:5px;border-radius:50%}.t-india .tdot{background:var(--green)}.t-block .tdot{background:#DC2626}
.input-bar{border-top:1px solid var(--border);padding:1rem 2rem;background:var(--white)}
.input-row{display:flex;gap:10px;align-items:center;background:var(--gray-l);border:1.5px solid var(--border);border-radius:14px;padding:6px 6px 6px 16px;transition:border-color .2s}
.input-row:focus-within{border-color:var(--saffron)}
#qi{flex:1;border:none;background:transparent;font-size:14px;color:var(--navy);outline:none;font-family:'DM Sans',sans-serif;padding:6px 0}
#qi::placeholder{color:#B0A99A}
#sb{width:38px;height:38px;border-radius:10px;background:var(--saffron);border:none;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:all .15s;flex-shrink:0}
#sb:hover{background:var(--saffron-l)}#sb:disabled{opacity:.4;cursor:not-allowed}
#sb svg{width:16px;height:16px;fill:white}
.hint{font-size:11px;color:#B0A99A;text-align:center;margin-top:6px}
.tdots{display:flex;gap:4px;align-items:center;padding:4px 0}
.tdots span{width:6px;height:6px;background:var(--gray);border-radius:50%;animation:bounce 1.2s infinite}
.tdots span:nth-child(2){animation-delay:.2s}.tdots span:nth-child(3){animation-delay:.4s}
@keyframes fadeIn{from{opacity:0}to{opacity:1}}
@keyframes slideUp{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
@keyframes bounce{0%,60%,100%{transform:translateY(0)}30%{transform:translateY(-5px)}}
</style>
</head>
<body>
<header>
  <div class="logo">
    <div class="flag-strip"><div class="fs1"></div><div class="fs2"><div class="chakra-sm"></div></div><div class="fs3"></div></div>
    <div class="logo-text">Bharat<span>AI</span></div>
  </div>
  <div class="header-right">
    <div class="status-pill"><div class="sdot"></div>India-Only Assistant · Live</div>
  </div>
</header>

<div class="app-layout">
  <aside class="sidebar">
    <div>
      <div class="sec-title">Session Stats</div>
      <div class="stats-grid">
        <div class="stat-card"><div class="stat-num" id="tc">0</div><div class="stat-label">Questions</div></div>
        <div class="stat-card"><div class="stat-num" id="ic">0</div><div class="stat-label">India topics</div></div>
        <div class="stat-card"><div class="stat-num" id="bc">0</div><div class="stat-label">Blocked</div></div>
        <div class="stat-card"><div class="stat-num" id="ac">—</div><div class="stat-label">Accuracy</div></div>
      </div>
    </div>
    <div>
      <div class="sec-title">Quick Questions</div>
      <button class="qbtn" onclick="qa('What is the capital of India?')">🏛 Capital of India?</button>
      <button class="qbtn" onclick="qa('Who was Akbar?')">👑 Who was Akbar?</button>
      <button class="qbtn" onclick="qa('Tell me about Goa beaches')">🏖 Goa beaches</button>
      <button class="qbtn" onclick="qa('Best temples in Tirupati')">🛕 Tirupati temples</button>
      <button class="qbtn" onclick="qa('Tell me about Kerala backwaters')">🌿 Kerala backwaters</button>
      <button class="qbtn" onclick="qa('History of Taj Mahal')">🕌 Taj Mahal history</button>
      <button class="qbtn" onclick="qa('Tell me about the history of London')">🚫 London (block test)</button>
    </div>
  </aside>

  <div class="chat-area">
    <div class="chat-msgs" id="cm">
      <div class="welcome" id="ws">
        <div class="wflag"><div class="wf1"></div><div class="wf2"><div class="chakra-lg"></div></div><div class="wf3"></div></div>
        <h2>Namaste! Ask me about India</h2>
        <p>I can answer anything about Indian history, culture, tourism, food, geography, politics, temples, national parks and more.</p>
        <div class="chips">
          <div class="chip" onclick="qa('Best hill stations in India')">Hill stations</div>
          <div class="chip" onclick="qa('Famous national parks in India')">National parks</div>
          <div class="chip" onclick="qa('History of Hyderabad')">Hyderabad history</div>
          <div class="chip" onclick="qa('Indian classical dance forms')">Dance forms</div>
          <div class="chip" onclick="qa('What is the significance of Diwali?')">Diwali</div>
          <div class="chip" onclick="qa('Tell me about Rajasthan forts')">Rajasthan forts</div>
        </div>
      </div>
    </div>
    <div class="input-bar">
      <div class="input-row">
        <input type="text" id="qi" placeholder="Ask anything about India — temples, food, history, tourism..." onkeydown="if(event.key==='Enter')send()"/>
        <button id="sb" onclick="send()"><svg viewBox="0 0 24 24"><path d="M2 21l21-9L2 3v7l15 2-15 2z"/></svg></button>
      </div>
      <div class="hint">BharatAI · India-only mode active</div>
    </div>
  </div>
</div>

<script>
let t=0,ic=0,bc=0;
function us(bl){t++;if(bl)bc++;else ic++;document.getElementById('tc').textContent=t;document.getElementById('ic').textContent=ic;document.getElementById('bc').textContent=bc;document.getElementById('ac').textContent=t>0?Math.round(ic/t*100)+'%':'—';}
function qa(q){document.getElementById('qi').value=q;send();}
function hw(){const w=document.getElementById('ws');if(w)w.remove();}
function addU(txt){hw();const c=document.getElementById('cm'),d=document.createElement('div');d.className='msg-row user';d.innerHTML=`<div class="av-you">You</div><div class="bwrap"><div class="bubble user">${txt}</div></div>`;c.appendChild(d);c.scrollTop=c.scrollHeight;}
function addB(txt){const c=document.getElementById('cm'),bl=txt.trim()==='I am sorry, I can only talk about India.',d=document.createElement('div');d.className='msg-row';d.innerHTML=`<div class="av-flag"><div class="af1"></div><div class="af2"></div><div class="af3"></div></div><div class="bwrap"><div class="bubble ${bl?'blocked':'bot'}">${txt}</div><div class="mtag ${bl?'t-block':'t-india'}"><div class="tdot"></div>${bl?'Off-topic — blocked':'India topic — answered'}</div></div>`;c.appendChild(d);c.scrollTop=c.scrollHeight;us(bl);}
function addT(){hw();const c=document.getElementById('cm'),d=document.createElement('div');d.className='msg-row';d.id='tm';d.innerHTML=`<div class="av-flag"><div class="af1"></div><div class="af2"></div><div class="af3"></div></div><div class="bwrap"><div class="bubble bot"><div class="tdots"><span></span><span></span><span></span></div></div></div>`;c.appendChild(d);c.scrollTop=c.scrollHeight;}
function rmT(){const e=document.getElementById('tm');if(e)e.remove();}
async function send(){
  const i=document.getElementById('qi'),b=document.getElementById('sb'),q=i.value.trim();
  if(!q)return;
  i.value='';b.disabled=true;addU(q);addT();
  try{
    const r=await fetch('/ask',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question:q})});
    const d=await r.json();rmT();addB(d.answer);
  }catch(e){rmT();addB('Error: '+e.message);}
  b.disabled=false;i.focus();
}
</script>
</body>
</html>"""

# ── HTTP Handler ─────────────────────────────────────────
class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args): pass  # suppress logs

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(HTML.encode())

    def do_POST(self):
        if self.path != '/ask':
            self.send_response(404); self.end_headers(); return
        length  = int(self.headers['Content-Length'])
        body    = json.loads(self.rfile.read(length))
        question = body.get('question', '')
        answer  = call_groq(question)
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({'answer': answer}).encode())


# ── Groq API Call ────────────────────────────────────────
def call_groq(question: str) -> str:
    payload = json.dumps({
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": question}
        ],
        "temperature": 0.3,
        "max_tokens": 600
    }).encode()

    req = urllib.request.Request(
        "https://api.groq.com/openai/v1/chat/completions",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
    )
    try:
        with urllib.request.urlopen(req) as res:
            data = json.loads(res.read())
            return data["choices"][0]["message"]["content"].strip()
    except urllib.error.HTTPError as e:
        err = json.loads(e.read())
        return f"Error: {err.get('error', {}).get('message', 'Unknown error')}"


# ── Run Demo in Terminal ─────────────────────────────────
def run_terminal_demo():
    demo = [
        "What is the capital of India?",
        "Who was Akbar?",
        "Tell me about the history of London."
    ]
    print("=" * 60)
    print("       India-Only AI Assistant — Demo")
    print("=" * 60)
    for i, q in enumerate(demo, 1):
        print(f"\n[Question {i}]")
        print(f"Input : {q}")
        print(f"Output: {call_groq(q)}")
        print("-" * 60)


# ── Main ─────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("   BharatAI — India Only Assistant")
    print("=" * 60)

    # Start web server
    server = HTTPServer(('localhost', PORT), Handler)
    url = f"http://localhost:{PORT}"
    print(f"\n✓ Web UI running at: {url}")
    print("  Press Ctrl+C to stop\n")

    # Auto-open browser
    threading.Timer(1, lambda: webbrowser.open(url)).start()
    server.serve_forever()