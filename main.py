import streamlit as st
import streamlit.components.v1 as components
import base64, os

# ── CONFIG ────────────────────────────────────────────────────────────────────
FRIEND_NAME = "Cyliatun"
PHOTO_PATH  = "imagee.jpeg"   # ← doit être dans le même dossier que ce script
# ─────────────────────────────────────────────────────────────────────────────

st.set_page_config(page_title=f"Happy Birthday {FRIEND_NAME}! 🎂", layout="wide")

# Full-screen, no scroll, no Streamlit chrome
st.markdown("""
<style>
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding-top: 1rem !important; }
  iframe { display: block; border: none; }
</style>
""", unsafe_allow_html=True)


def photo_b64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            ext  = path.rsplit(".", 1)[-1].lower()
            mime = {"jpg": "jpeg", "jpeg": "jpeg", "png": "png", "gif": "gif"}.get(ext, "jpeg")
            return f"data:image/{mime};base64,{base64.b64encode(f.read()).decode()}"
    svg = """
<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300' viewBox='0 0 300 300'>
  <rect width='300' height='300' fill='#ffe0ec' rx='20'/>
  <text x='150' y='130' font-size='80' text-anchor='middle'>&#128248;</text>
  <text x='150' y='200' font-size='18' text-anchor='middle' fill='#c06080'>Add imagee.jpeg next to</text>
  <text x='150' y='225' font-size='18' text-anchor='middle' fill='#c06080'>this script!</text>
</svg>"""
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode("utf-8")).decode()


photo_src = photo_b64(PHOTO_PATH)

html_code = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

  html, body {{
    width: 100%;
    font-family: 'Segoe UI', sans-serif;
    background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 40%, #ffecd2 100%);
    overflow-y: auto;
  }}

  /* ── QUESTION SCREEN ── */
  #q-screen {{
    width: 100%;
    padding: 80px 20px 60px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    animation: fadeIn .6s ease;
  }}

  #q-screen h1 {{
    font-size: 2.8rem;
    color: #b0203a;
    margin-bottom: 12px;
    text-shadow: 2px 2px 0px rgba(255,255,255,.6);
  }}

  #q-screen p {{
    color: #c03050;
    margin-bottom: 48px;
    font-size: 1.3rem;
    font-weight: 600;
  }}

  .btn-row {{
    display: flex;
    gap: 32px;
    justify-content: center;
  }}

  .btn {{
    padding: 18px 52px;
    font-size: 1.5rem;
    border: none;
    border-radius: 50px;
    cursor: pointer;
    font-weight: bold;
    box-shadow: 0 6px 20px rgba(0,0,0,.18);
  }}

  #yes-btn {{
    background: linear-gradient(135deg, #ff6b9d, #ff4d6d);
    color: white;
    transition: transform .1s, box-shadow .1s;
  }}
  #yes-btn:hover {{ transform: scale(1.09); box-shadow: 0 8px 26px rgba(255,77,109,.5); }}
  #yes-btn:active {{ transform: scale(.97); }}

  #no-btn {{
    background: #eeeeee;
    color: #999;
    position: fixed;
    visibility: hidden;
    transition: left .12s ease, top .12s ease;
  }}

  /* ── PARTY SCREEN ── */
  #party-screen {{
    display: none;
    width: 100%;
    padding: 40px 20px 40px;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    animation: popIn .5s cubic-bezier(.17,.67,.35,1.4);
  }}

  #party-screen h1 {{
    font-size: 3.2rem;
    background: linear-gradient(90deg, #ff4d6d, #ff9a3c, #ffcd3c, #4dffb4, #4db8ff, #b44dff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 10px;
    text-align: center;
  }}

  #party-screen .sub {{
    color: #b0203a;
    font-size: 1.4rem;
    font-weight: 600;
    margin-bottom: 28px;
  }}

  #party-screen img {{
    width: min(380px, 85vw);
    height: auto;
    border-radius: 24px;
    border: 6px solid white;
    box-shadow: 0 12px 40px rgba(255,77,109,.4);
    margin-bottom: 24px;
  }}

  #party-screen .heart-row {{
    font-size: 2.5rem;
    letter-spacing: 8px;
    animation: pulse 1s infinite alternate;
  }}

  /* ── CONFETTI ── */
  .confetto {{
    position: fixed;
    top: -14px;
    border-radius: 2px;
    animation: fall linear forwards;
  }}

  @keyframes fadeIn {{ from {{ opacity:0; transform:translateY(24px) }} to {{ opacity:1; transform:none }} }}
  @keyframes popIn  {{ from {{ opacity:0; transform:scale(.5) }}        to {{ opacity:1; transform:scale(1) }} }}
  @keyframes pulse  {{ from {{ transform:scale(1) }}                     to {{ transform:scale(1.12) }} }}
  @keyframes fall {{
    0%   {{ opacity:1; transform:translateY(0) rotate(0deg); }}
    100% {{ opacity:0; transform:translateY(110vh) rotate(720deg); }}
  }}
</style>
</head>
<body>

<!-- ── QUESTION ── -->
<div id="q-screen">
  <h1>💕 Am I your best friend? 💕</h1>
  <p>Choose wisely… 👀</p>
  <div class="btn-row">
    <button id="yes-btn" class="btn" onclick="sayYes()">YES 🥰</button>
    <button id="no-btn"  class="btn"
      onmouseover="runAway(this)"
      ontouchstart="runAway(this); event.preventDefault()">NO 😤</button>
  </div>
</div>

<!-- ── PARTY ── -->
<div id="party-screen">
  <h1>🎂 Happy Birthday {FRIEND_NAME}! 🎂</h1>
  <p class="sub">Obviously I'm your best friend 💅✨</p>
  <img src="{photo_src}" alt="us"/>
  <div class="heart-row">💖💖💖</div>
</div>

<script>
  const noBtn = document.getElementById('no-btn');
  let noBtnX = 0, noBtnY = 0;

  function placeNoBtn() {{
    const rect = document.getElementById('q-screen').getBoundingClientRect();
    noBtnX = rect.left + rect.width / 2 + 48;
    noBtnY = rect.top  + rect.height / 2 + 30;
    noBtn.style.left = noBtnX + 'px';
    noBtn.style.top  = noBtnY + 'px';
    noBtn.style.visibility = 'visible';
  }}
  window.addEventListener('load', placeNoBtn);

  function runAway(btn) {{
    // Stay within visible area: cap Y to 500px so button never hides below the fold
    const maxX = window.innerWidth  - 130;
    const maxY = 500;
    const minX = 10;
    const minY = 10;
    let nx, ny, tries = 0;
    do {{
      nx = minX + Math.random() * (maxX - minX);
      ny = minY + Math.random() * (maxY - minY);
      tries++;
    }} while (tries < 30 && Math.abs(nx - noBtnX) < 150 && Math.abs(ny - noBtnY) < 100);
    noBtnX = nx;
    noBtnY = ny;
    btn.style.left = nx + 'px';
    btn.style.top  = ny + 'px';
  }}

  function sayYes() {{
    document.getElementById('q-screen').style.display = 'none';
    noBtn.style.display = 'none';
    const party = document.getElementById('party-screen');
    party.style.display = 'flex';
    launchConfetti();
  }}

  const COLORS = ['#ff4d6d','#ff9a3c','#ffcd3c','#4dffb4','#4db8ff','#b44dff','#ff6b9d','#fff'];

  function launchConfetti() {{
    for (let i = 0; i < 100; i++) setTimeout(() => spawnPiece(), i * 35);
  }}

  function spawnPiece() {{
    const el = document.createElement('div');
    el.className = 'confetto';
    el.style.left              = Math.random() * 100 + 'vw';
    el.style.background        = COLORS[Math.floor(Math.random() * COLORS.length)];
    el.style.width             = (7 + Math.random() * 9)  + 'px';
    el.style.height            = (10 + Math.random() * 12) + 'px';
    el.style.animationDuration = (1.6 + Math.random() * 2.2) + 's';
    el.style.animationDelay    = '0s';
    document.body.appendChild(el);
    setTimeout(() => el.remove(), 4000);
  }}
</script>
</body>
</html>
"""

components.html(html_code, height=1400, scrolling=True)