import uuid
import json
import os
from datetime import datetime
import base64
import plotly.express as px
import numpy as np
import pandas as pd
import streamlit as st
import requests
try:
    from dotenv import load_dotenv
    load_dotenv()
except: pass

# --- Page Config ---
st.set_page_config(
    page_title="RxTrace | Aetheris Pharma",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Function to get base64
def get_base64_image(image_path):
    if os.path.exists(image_path):
        try:
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
        except: return ""
    return ""

logo_base64 = get_base64_image("logo.png")

# --- UI Theme CSS ---
css_code = """
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
<style>
    html, body, [class*="css"] { 
        font-family: 'Inter', sans-serif !important; 
    }
    .stApp { 
        background: radial-gradient(circle at 50% 50%, #111827 0%, #030712 100%); 
        color: #f3f4f6; 
    }
    [data-testid="stSidebar"] { 
        background: linear-gradient(180deg, #111827 0%, #0f172a 100%); 
        border-right: 1px solid rgba(255, 255, 255, 0.05); 
    }
    [data-testid="stHeader"] { 
        background: rgba(0,0,0,0) !important; 
        color: transparent !important;
    }
    header { visibility: hidden !important; }
    
    /* Bottom Nav Pill - Elegant & Minimal */
    div.stRadio > div {
        background: rgba(15, 23, 42, 0.4) !important;
        backdrop-filter: blur(25px) !important;
        display: flex !important;
        flex-direction: row !important;
        justify-content: center !important;
        align-items: center !important;
        position: fixed !important;
        bottom: 25px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        z-index: 1000000 !important;
        width: auto !important;
        min-width: 950px !important;
        white-space: nowrap !important;
        padding: 5px 20px !important;
        border-radius: 50px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5) !important;
    }
    
    div.stRadio > div label {
        color: rgba(255, 255, 255, 0.5) !important;
        padding: 8px 12px !important;
        margin: 0 5px !important;
        border-radius: 30px !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
    }

    div.stRadio > div label:hover {
        color: rgba(255, 255, 255, 0.9) !important;
        background: rgba(255, 255, 255, 0.05) !important;
    }

    div.stRadio > div label[data-selected="true"] {
        background: rgba(255, 255, 255, 0.1) !important;
        color: #10b981 !important;
        box-shadow: none !important;
    }

    /* Hide standard radio circles */
    div.stRadio > div label > div:first-child {
        display: none !important;
    }

    /* Elegant SVG Icons via CSS Masking */
    div.stRadio > div label p::before {
        content: '';
        display: inline-block;
        width: 14px;
        height: 14px;
        margin-right: 6px;
        vertical-align: middle;
        background-color: currentColor;
        mask-size: contain;
        mask-repeat: no-repeat;
        mask-position: center;
        -webkit-mask-size: contain;
        -webkit-mask-repeat: no-repeat;
        -webkit-mask-position: center;
        margin-top: -2px;
    }

    /* Focus Today: Target */
    div.stRadio > div label:nth-child(1) p::before {
        -webkit-mask-image: url('data:image/svg+xml;utf8,<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="10"/><path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/></svg>');
    }
    /* My Results: Activity Line */
    div.stRadio > div label:nth-child(2) p::before {
        -webkit-mask-image: url('data:image/svg+xml;utf8,<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>');
    }
    /* Intelligence: Bell/Signal */
    div.stRadio > div label:nth-child(3) p::before {
        -webkit-mask-image: url('data:image/svg+xml;utf8,<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>');
    }
    /* Territory: Map */
    div.stRadio > div label:nth-child(4) p::before {
        -webkit-mask-image: url('data:image/svg+xml;utf8,<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg"><polygon points="3 6 9 3 15 6 21 3 21 18 15 21 9 18 3 21"/><line x1="9" y1="3" x2="9" y2="21"/><line x1="15" y1="3" x2="15" y2="21"/></svg>');
    }

    /* Action Card Module */
    .action-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 20px;
        transition: transform 0.3s ease;
    }
    .action-card:hover { transform: translateY(-5px); border-color: rgba(16, 185, 129, 0.4); }
    
    .status-badge {
        padding: 5px 12px;
        border-radius: 50px;
        font-size: 11px;
        font-weight: bold;
        text-transform: uppercase;
        margin-left: 10px;
    }
    .badge-urgent { background: rgba(239, 68, 68, 0.2); color: #ef4444; border: 1px solid #ef4444; }
    .badge-overdue { background: rgba(245, 158, 11, 0.2); color: #f59e0b; border: 1px solid #f59e0b; }
    .badge-potential { background: rgba(16, 185, 129, 0.2); color: #10b981; border: 1px solid #10b981; }

    .block-container { padding-bottom: 140px !important; }

    /* Custom Header Info */
    .identity-card {
        background: rgba(16, 185, 129, 0.05);
        border: 1px solid rgba(16, 185, 129, 0.1);
        padding: 12px 20px;
        border-radius: 12px;
        display: inline-block;
    }

    /* XAI Intelligence Pulse Card */
    .xai-pulse {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.05) 100%);
        border: 1px dashed rgba(16, 185, 129, 0.3);
        border-radius: 12px;
        padding: 15px;
        margin-top: 15px;
    }
    .xai-label {
        font-size: 0.75rem;
        font-weight: bold;
        color: #10b981;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 5px;
    }
</style>
"""
st.markdown(css_code, unsafe_allow_html=True)

# --- Data Loading ---
@st.cache_data
def load_chemist_data():
    # Synthetic Chemist Mapping
    chem_data = []
    for i in range(1, 21):
        chem_data.append({
            "chemist_id": f"CHM{i:03}",
            "name": f"Reliance Pharma {i}",
            "area": ["Thane", "Mulund", "Bandra", "Chembur", "Andheri"][i % 5],
            "top_doctor_map": f"DOC{(i%5)+1:03}"
        })
    chemists = pd.DataFrame(chem_data)
    
    # Audit Inspection Data
    audit_rows = []
    for c in range(1, 21):
        for m in ["MOL01", "MOL02", "MOL03"]:
            aetheris_sold = np.random.randint(5, 50)
            comp_sold = np.random.randint(10, 80)
            audit_rows.append({
                "chemist_id": f"CHM{c:03}",
                "molecule_id": m,
                "aetheris_vol": aetheris_sold,
                "competitor_vol": comp_sold,
                "leakage_pct": round((comp_sold / (aetheris_sold + comp_sold + 1)) * 100, 1)
            })
    audits = pd.DataFrame(audit_rows)
    return chemists, audits

pres, alts, intel, roi, recs, docs, mols = load_rep_data_v3()
chemists, audits = load_chemist_data()

# --- Persistence Layer (Strategic Config) ---
CONFIG_FILE = "config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"competitor_list": [], "hero_product": "MOL01", "target_share": 0.5}

def save_config(cfg):
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=2)

def get_strategic_analytics(df, cfg):
    """Calculates alignment scores based on strategy config."""
    if df.empty: return pd.DataFrame()
    hero_id = cfg.get("hero_product")
    target = cfg.get("target_share", 0.5)
    
    # Group by Doctor and Molecule
    doctor_shares = df.groupby(["doctor_id", "molecule_id"])["hybrid_score"].sum().reset_index()
    doctor_totals = df.groupby("doctor_id")["hybrid_score"].sum().reset_index().rename(columns={"hybrid_score": "total_rx"})
    
    shares = doctor_shares.merge(doctor_totals, on="doctor_id")
    shares["share_pct"] = shares["hybrid_score"] / shares["total_rx"]
    
    # Filter for hero product
    hero_shares = shares[shares["molecule_id"] == hero_id].copy()
    
    # Compliance = 100 - absolute distance from target
    hero_shares["alignment_score"] = hero_shares["share_pct"].apply(lambda x: max(0, 100 - abs((target - x) * 100)))
    
    return hero_shares

def get_market_news(cfg):
    """Fetches pharma news using API or curated fallback."""
    news_key = os.getenv("NEWS_API_KEY")
    query = " ".join(cfg.get("competitor_list", [])) or "pharmaceutical market trends 2024"
    
    if news_key and news_key != "your_news_api_key_here":
        try:
            url = f"https://newsapi.org/v2/everything?q={query}&language=en&sortBy=relevancy&pageSize=5&apiKey={news_key}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                articles = response.json().get("articles", [])
                return [{"title": a["title"], "source": a["source"]["name"], "date": a["publishedAt"][:10]} for a in articles]
        except: pass
    
    # High-value Curated Fallback
    return [
        {"title": "Madrigal Pharma NASH drug approval shifts Liver market", "source": "Aetheris Intel", "date": "2026-04-18"},
        {"title": "Rising demand for Thyroid precision monitoring", "source": "Global Trends", "date": "2026-04-17"},
        {"title": "Competitor Expansion in CNS/Neuro segments", "source": "Pharma Weekly", "date": "2026-04-18"}
    ]

def generate_ai_strategy(cfg, news_list):
    """Synthesizes news and strategy into a playbook using Gemini."""
    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key or gemini_key == "your_gemini_api_key_here":
        return "Please provide a valid GEMINI_API_KEY in .env to unlock live strategic synthesis."
    
    hero_id = cfg.get("hero_product")
    comps = ", ".join(cfg.get("competitor_list", [])) or "Global Leaders"
    news_titles = "\n".join([f"- {n['title']}" for n in news_list])
    
    prompt = f"""
    You are an Elite Pharma Growth Alchemist. Your mission is to give Aetheris Pharma a 'Strategic Cheatcode' to dominate the market.
    Current Focus: {hero_id} | Competitors: {comps}
    Market Intel: {news_titles}

    Synthesize an AGGRESSIVE, VISIONARY strategy. Use powerful language like 'Surgical Strike', 'Market Dominance', 'Empire Building', and 'Unfair Advantage'. 
    Make the leadership feel like this insight is a game-changer. Return only the 3 'Aetheris Power Plays' as bold bullet points.
    """
    
    try:
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={gemini_key}"
        headers = {'Content-Type': 'application/json'}
        data = {"contents": [{"parts": [{"text": prompt}]}]}
        response = requests.post(url, headers=headers, json=data, timeout=10)
        if response.status_code == 200:
            text = response.json()['candidates'][0]['content']['parts'][0]['text']
            # Split and clean
            points = [p.strip().strip('*').strip('-').strip() for p in text.split('\n') if p.strip()]
            return points[:3]
        else:
            return [
                f"Surgical Market Capture: Launch a strike on the '{hero_id}' segment by identifying high-volume accounts with low alignment.",
                f"Competitor Neutralization: Position Aetheris as the bedrock of reliability during the current {news_list[0]['title'][:20] if news_list else 'market'} disruption.",
                "Empire Expansion: Dominate high-ROI territories where competitor vacancy is currently peaking."
            ]
    except:
        return [
            f"Surgical Market Capture: Priority strike on '{hero_id}' across alignment-gap accounts.",
            "Competitor Pivot: Neutralize rival momentum by leveraging our superior pricing unit economics.",
            "Territory Colonization: Capture new clinic share in high-growth regional hubs."
        ]

# --- Activity Log Engine (Cross-Role Message Bus) ---
ACTIVITY_LOG_FILE = "activity_log.json"

def load_activity_log():
    if os.path.exists(ACTIVITY_LOG_FILE):
        try:
            with open(ACTIVITY_LOG_FILE, "r") as f:
                entries = json.load(f)
            # Migration v3.0: Formal Batch Handshake
            for e in entries:
                e.setdefault("total_requested", e.get("details", {}).get("qty", 0) if isinstance(e.get("details"), dict) else 0)
                e.setdefault("confirmed_received", e.get("delivered_qty", 0)) # Legacy delivered becomes confirmed
                e.setdefault("in_transit_qty", 0)
                e.setdefault("acknowledged", False)
            return entries
        except:
            return []
    return []

def save_activity_log(entries):
    with open(ACTIVITY_LOG_FILE, "w") as f:
        json.dump(entries, f, indent=2, default=str)

def add_activity(source_role, source_id, action_type, details, assigned_to=None):
    log = load_activity_log()
    total_req = details.get("qty", 0) if isinstance(details, dict) else 0
    
    entry = {
        "id": f"ACT-{str(uuid.uuid4())[:8].upper()}",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source_role": source_role,
        "source_id": source_id,
        "action_type": action_type,
        "details": details,
        "total_requested": total_req,
        "confirmed_received": 0,
        "in_transit_qty": 0,
        "status": "Assigned" if assigned_to else "Pending",
        "assigned_to": assigned_to,
        "completed_at": None,
        "acknowledged": False
    }
    log.append(entry)
    save_activity_log(log)
    return entry["id"]

def update_activity(act_id, **kwargs):
    log = load_activity_log()
    for entry in log:
        if entry["id"] == act_id:
            entry.update(kwargs)
            
            # Status Automation v3.0
            conf = entry.get("confirmed_received", 0)
            transit = entry.get("in_transit_qty", 0)
            goal = entry.get("total_requested", 0)
            
            if goal > 0:
                if conf >= goal:
                    entry["status"] = "Completed"
                elif transit > 0:
                    entry["status"] = "Shipment in Transit"
                elif conf > 0:
                    entry["status"] = "Partially Fulfilled"
                else:
                    entry["status"] = "Assigned"
            break
    save_activity_log(log)

def render_activity_details(details):
    if not isinstance(details, dict):
        return str(details)
    
    friendly_parts = []
    if "compound" in details:
        friendly_parts.append(f"📦 <b>Brand</b>: {details['compound']}")
    if "qty" in details:
        friendly_parts.append(f"🔢 <b>Goal</b>: {details['qty']} Units")
    if "instructions" in details or "info" in details:
        note = details.get("instructions") or details.get("info")
        friendly_parts.append(f"📝 <b>Note</b>: {note}")
    if "nature" in details:
        friendly_parts.append(f"❓ <b>Kind</b>: {details['nature']}")
    
    return " | ".join(friendly_parts) if friendly_parts else str(details)

def get_xai_insight(row):
    score = row['hybrid_score']
    days = row['days_since_last_visit']
    align = row.get('alignment_score', 0)
    cfg = load_config()
    hero = next((m['brand_name'] for m in mols.to_dict('records') if m['molecule_id'] == cfg['hero_product']), "Hero Brand")
    
    base_insight = ""
    if score < 10: base_insight = f"CRITICAL RISK: Relationship has eroded due to {days} days of field inactivity."
    elif score < 30: base_insight = f"MODERATE RISK: {days} days since last visit is causing brand slippage."
    elif score > 80: base_insight = "OPTIMAL ALIGNMENT: High compliance and recent activity."
    else: base_insight = "STABLE: Relationship is healthy but requires routine touchpoints."
    
    # Strategic Layer
    strategy_hook = ""
    if align < (cfg['target_share'] * 100):
        strategy_hook = f" 💡 <b>Strategic Push:</b> Doctor is below target share for <b>{hero}</b>. Competitor moves detected in area—highlight our specific unit pricing today."
    else:
        strategy_hook = f" ✅ <b>Strategy Success:</b> Doctor is properly aligned with <b>{hero}</b> targets. Focus on delivery reliability."
        
    return f"{base_insight}{strategy_hook}"

# --- Auth ---
if 'authenticated' not in st.session_state: st.session_state.authenticated = False
if 'active_modal' not in st.session_state: st.session_state.active_modal = None
if 'modal_data' not in st.session_state: st.session_state.modal_data = ""

def do_login():
    bg_img = "file:///C:/Users/Lenovo/.gemini/antigravity/brain/152012bb-1465-4fd1-8055-2ea9dada866a/aetheris_login_bg_1776421091543.png"
    st.markdown(f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background: linear-gradient(rgba(2, 6, 23, 0.85), rgba(2, 6, 23, 0.85)), url("{bg_img}");
            background-size: cover;
            background-position: center;
        }}
        [data-testid="stHeader"] {{
            background: rgba(0,0,0,0);
        }}
        .login-box {{
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
            margin-top: 50px;
        }}
        .stTextInput input {{
            background-color: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            color: white !important;
            border-radius: 10px !important;
            padding: 12px !important;
        }}
        .stButton button {{
            background: linear-gradient(135deg, #10b981 0%, #3b82f6 100%) !important;
            border: none !important;
            color: white !important;
            font-weight: bold !important;
            padding: 15px !important;
            border-radius: 10px !important;
            transition: all 0.3s ease !important;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .stButton button:hover {{
            transform: translateY(-2px) !important;
            box-shadow: 0 5px 15px rgba(16, 185, 129, 0.4) !important;
        }}
        </style>
        
        <div style="text-align: center; padding-top: 80px;">
            <div style="font-size: 4.5rem; font-weight: 900; background: linear-gradient(to right, #10b981, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0;">RxTrace</div>
            <p style="color: #9ca3af; letter-spacing: 4px; font-size: 0.8rem; font-weight: 300; margin-top: -10px; margin-bottom: 40px;">AETHERIS PHARMA ENTERPRISE</p>
        </div>
    """, unsafe_allow_html=True)
    
    _, c2, _ = st.columns([1, 1.2, 1])
    with c2:
        st.markdown("<div class='login-box'>", unsafe_allow_html=True)
        u = st.text_input("User ID", placeholder="Enter your ID")
        p = st.text_input("Password", type="password", placeholder="Enter your password")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("LOGIN", use_container_width=True):
            # Admin Case
            if u == "admin" and p == "admin123":
                st.session_state.authenticated = True
                st.session_state.user_role = "Admin"
                st.session_state.user_id = "ADM01"
                st.rerun()
            
            # Sales Rep Cases (rep01 to rep10)
            elif u.startswith("rep") and p == f"{u}123":
                try:
                    num = int(u[3:])
                    if 1 <= num <= 10:
                        st.session_state.authenticated = True
                        st.session_state.user_role = "Sales Rep"
                        st.session_state.user_id = f"REP{num:03}"
                        st.rerun()
                except: pass
            
            # Doctor Cases (doc01 to doc05)
            elif u.startswith("doc") and p == f"{u}123":
                try:
                    num = int(u[3:])
                    if 1 <= num <= 5:
                        st.session_state.authenticated = True
                        st.session_state.user_role = "Doctor"
                        st.session_state.user_id = f"DOC{num:03}"
                        st.rerun()
                except: pass
            
            st.error("Invalid Credentials or User ID range limit exceeded.")
        st.markdown("</div>", unsafe_allow_html=True)


if not st.session_state.authenticated:
    do_login()
    st.stop()

# --- PM-LED SIDEBAR REDESIGN ---
with st.sidebar:
    # 1. Branding Header
    st.markdown("<div style='text-align: center; margin-bottom: 20px;'>", unsafe_allow_html=True)
    if os.path.exists("logo.png"):
        st.image("logo.png", width=220)
    st.markdown("<h3 style='color: #10b981; margin-top: -10px;'>RxTrace v2.5</h3></div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 2. Proactive Status Badge
    st.markdown(f"""
        <div style='background: rgba(16, 185, 129, 0.05); padding: 15px; border-radius: 12px; border: 1px solid rgba(16, 185, 129, 0.1); margin-bottom: 20px;'>
            <p style='margin:0; font-size: 0.75rem; color: #10b981; font-weight: bold;'>● SYSTEM STATUS: ONLINE</p>
            <p style='margin:0; font-size: 0.85rem; color: #9ca3af;'>User ID: <b>{st.session_state.user_id}</b></p>
            <p style='margin:0; font-size: 0.85rem; color: #9ca3af;'>Last Node Sync: <b>Just Now</b></p>
        </div>
    """, unsafe_allow_html=True)
    
    # 3. Persistent KPI (PM Strategy: Visual Nudge based on role)
    if st.session_state.user_role == "Sales Rep":
        st.markdown("<p style='font-size: 0.8rem; margin-bottom: 5px; color: #9ca3af; font-weight: bold;'>MONTHLY QUOTA PROGRESS</p>", unsafe_allow_html=True)
        st.progress(0.72)
        st.markdown("<p style='font-size: 0.7rem; text-align: right; color: #10b981; font-weight: bold;'>72% COMPLETED</p>", unsafe_allow_html=True)
        st.markdown("---")
    elif st.session_state.user_role == "Admin":
        st.markdown("<p style='font-size: 0.8rem; margin-bottom: 5px; color: #9ca3af; font-weight: bold;'>NETWORK UPTIME</p>", unsafe_allow_html=True)
        st.progress(0.99)
        st.markdown("<p style='font-size: 0.7rem; text-align: right; color: #10b981; font-weight: bold;'>99.9% LIVE</p>", unsafe_allow_html=True)
        st.markdown("---")
    
    # 4. Role-Specific Utility Section
    st.markdown("### Quick Tools")

    if st.session_state.user_role == "Admin":
        if st.button("🖥️ System Health", use_container_width=True): 
            st.session_state.active_modal = "sys_health"
            st.rerun()
        if st.button("📂 Data Overrides", use_container_width=True): 
            st.session_state.active_modal = "data_override"
            st.rerun()
    elif st.session_state.user_role == "Doctor":
        if st.button("📦 Request Samples", use_container_width=True): 
            st.session_state.active_modal = "restock"
            st.rerun()
        if st.button("📞 Rep Priority Line", use_container_width=True): 
            st.session_state.active_modal = "priority_dispatch"
            st.rerun()
    else: # Sales Rep
        if st.button("📝 Offline Visit Log", use_container_width=True): 
            st.session_state.active_modal = "offline_log"
            st.rerun()
        if st.button("💬 Contact Operations", use_container_width=True): 
            st.session_state.active_modal = "contact_ops"
            st.rerun()
    
    st.markdown("<div style='height: 60px;'></div>", unsafe_allow_html=True)
    
    # 5. The "Floating" Logout
    if st.button("🚪 Terminate Session", use_container_width=True, type="primary"):
        st.session_state.authenticated = False
        st.rerun()

# --- Responsive Header ---
hr = datetime.now().hour
greeting = "Good Morning" if 5 <= hr < 12 else "Good Afternoon" if 12 <= hr < 17 else "Good Evening"

if st.session_state.user_role == "Sales Rep":
    user_name = "Alex"
    subtitle = f"Ready to hit your targets today? Let's make {datetime.now().strftime('%B %d')} a successful day in the field."
else:
    user_name = st.session_state.user_role
    subtitle = f"Here is your territory summary for {datetime.now().strftime('%B %d')}."

st.markdown(f"""
    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 40px;'>
        <div>
            <h1 style='margin-bottom: 0;'>{greeting}, {user_name}!</h1>
            <p style='color: #9ca3af;'>{subtitle}</p>
        </div>
        <div class='identity-card'>
            <p style='margin:0; font-size:11px; color:#10b981; font-weight:bold;'>SYNC SECURE</p>
            <p style='margin:0; font-weight:bold;'>{st.session_state.user_id}</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- Interactive Modals Render Block ---
if st.session_state.active_modal:
    st.markdown("---")
    st.markdown("<div style='background: rgba(16, 185, 129, 0.05); padding: 25px; border-radius: 12px; border: 1px solid rgba(16, 185, 129, 0.4); margin-bottom: 25px;'>", unsafe_allow_html=True)
    
    if st.session_state.active_modal == "offline_log":
        with st.form("offline_form"):
            st.subheader("📝 Log Offline Visit")
            c_a, c_b = st.columns(2)
            with c_a: st.selectbox("Assign Doctor", ["Dr. Pooja Desai", "Dr. Simran Nair", "Other Focus Targets"])
            with c_b: st.date_input("Visit Date")
            st.text_area("Field Notes / Commitments")
            sub1, sub2, _ = st.columns([2, 2, 8])
            with sub1:
                if st.form_submit_button("Save Log", type="primary"):
                    add_activity("Sales Rep", st.session_state.user_id, "Offline Visit", {"info": "Logged via sidebar"})
                    st.session_state.active_modal = None
                    st.rerun()
            with sub2:
                if st.form_submit_button("Cancel"):
                    st.session_state.active_modal = None
                    st.rerun()

    elif st.session_state.active_modal == "contact_ops":
        with st.form("contact_form"):
            st.subheader("💬 Contact Enterprise Operations")
            st.selectbox("Issue Routing", ["Territory Data Reassignment", "Sample Inventory Request", "System Bug/Error"])
            st.text_area("Request Specifics")
            sub1, sub2, _ = st.columns([2, 2, 8])
            with sub1:
                if st.form_submit_button("Send Notice", type="primary"):
                    add_activity("Sales Rep", st.session_state.user_id, "Ops Request", {"type": "Operations Inquiry"})
                    st.session_state.active_modal = None
                    st.rerun()
            with sub2:
                if st.form_submit_button("Cancel"):
                    st.session_state.active_modal = None
                    st.rerun()
                    
    elif st.session_state.active_modal == "log_visit":
        doc_name = st.session_state.modal_data
        with st.form("log_visit_form"):
            st.subheader(f"✅ Fast Log: {doc_name}")
            st.radio("Outcome", ["Dropped Samples", "Detailed Pitch Completed", "Follow Up Requested"])
            st.text_input("Quick Memo")
            sub1, sub2, _ = st.columns([2, 2, 8])
            with sub1:
                if st.form_submit_button("Submit Data", type="primary"):
                    add_activity("Sales Rep", st.session_state.user_id, "Fast Log Visit", {"doctor": doc_name})
                    st.session_state.active_modal = None
                    st.rerun()
            with sub2:
                if st.form_submit_button("Cancel"):
                    st.session_state.active_modal = None
                    st.rerun()

    elif st.session_state.active_modal == "call":
        doc_name = st.session_state.modal_data
        st.info(f"Initiating secure VOIP routing to: **{doc_name}**...")
        st.markdown("<h2 style='text-align: center; color: #10b981; margin: 30px 0;'>📞 Calling...</h2>", unsafe_allow_html=True)
        if st.button("Hang Up", type="primary"):
            st.session_state.active_modal = None
            st.rerun()

    elif st.session_state.active_modal == "sys_health":
        st.subheader("🖥️ Core System Health Checks")
        col1, col2 = st.columns(2)
        col1.metric("API Gateway Sync", "99.98% Uptime", "Optimal")
        col2.metric("Database Latency", "12ms", "-1ms")
        st.progress(1.0)
        st.caption("All data pipelines operating normally.")
        if st.button("Close Diagnostics"):
            st.session_state.active_modal = None
            st.rerun()

    elif st.session_state.active_modal == "data_override":
        with st.form("override_form"):
            st.subheader("📂 Manual Data Override")
            st.text_input("Enter Document / HCP ID to adjust")
            st.selectbox("Adjustment Type", ["Priority Score Modification", "Coverage Re-assignment", "Suppress Alert"])
            st.text_area("Justification / Auth Number")
            sub1, sub2, _ = st.columns([2, 2, 8])
            with sub1:
                if st.form_submit_button("Submit Override", type="primary"):
                    st.session_state.active_modal = None
                    st.rerun()
            with sub2:
                if st.form_submit_button("Cancel"):
                    st.session_state.active_modal = None
                    st.rerun()

    elif st.session_state.active_modal == "restock":
        with st.form("restock_form"):
            st.subheader("📦 Urgent Sample Restock Requisition")
            compound = st.selectbox("Compound Needed", ["MOL01", "MOL02", "MOL03"])
            qty = st.number_input("Quantity Required (Units)", min_value=10, max_value=500, value=50)
            instr = st.text_input("Delivery Instructions")
            sub1, sub2, _ = st.columns([2, 2, 8])
            with sub1:
                if st.form_submit_button("Submit Requisition", type="primary"):
                    add_activity("Doctor", st.session_state.user_id, "Sample Requisition", {"compound": compound, "qty": qty, "instructions": instr})
                    st.session_state.active_modal = None
                    st.rerun()
            with sub2:
                if st.form_submit_button("Cancel"):
                    st.session_state.active_modal = None
                    st.rerun()

    elif st.session_state.active_modal == "priority_dispatch":
        st.info("Pinging your assigned Aetheris field agent...")
        st.markdown("<h2 style='text-align: center; color: #10b981; margin: 30px 0;'>📞 Dispatching Priority Notification...</h2>", unsafe_allow_html=True)
        if st.button("Confirm & Send Dispatch", type="primary"):
            add_activity("Doctor", st.session_state.user_id, "Priority Dispatch", {"urgent": True})
            st.session_state.active_modal = None
            st.rerun()
        if st.button("Cancel Dispatch"):
            st.session_state.active_modal = None
            st.rerun()
            
    st.markdown("</div>", unsafe_allow_html=True)

# --- Navigation Options per Role ---
if st.session_state.user_role == "Admin":
    nav_opts = ["Overview", "Strategy & Intel", "Field Force", "Chemist Audit", "Activity Queue", "National Map"]
elif st.session_state.user_role == "Doctor":
    nav_opts = ["Monthly Targets", "Rx History", "Deliveries", "Support"]
else: # Sales Rep
    nav_opts = ["Focus Today", "My Results", "Intelligence", "Territory"]

# Render the dynamic Navigation Pill
nav = st.radio("M", nav_opts, horizontal=True, label_visibility="collapsed")

# ==========================================
# 🏢 ADMIN DASHBOARD (Pharma HQ)
# ==========================================
if st.session_state.user_role == "Admin":
    st.sidebar.markdown("### 📅 Analytical Period")
    date_range = st.sidebar.date_input("Analysis Window", [datetime(2025,1,1), datetime(2025,12,31)])
    
    if nav == nav_opts[0]: # Overview
        st.title("Headquarters Overview")
        st.caption(f"Analysis spanning {date_range[0]} to {date_range[1] if len(date_range)>1 else ''}")
        c1, c2, c3 = st.columns(3)
        c1.metric("Active Field Reps", "142", "+3 this month")
        c2.metric("Total Prescriptions", f"{intel['hybrid_score'].sum():,.0f}", "+12%")
        c3.metric("Critical Market Alerts", str(len(alts[alts['priority'] == 'High'])), "-5")
        st.plotly_chart(px.bar(pres.head(20), x='name', y='hybrid_score', 
                           title="Top Performing Doctors Across Network",
                           labels={'hybrid_score': 'Rx Performance Index', 'name': 'HCP Name'}))
        
    elif nav == nav_opts[1]: # Strategy & Intel
        st.title("Corporate Strategy & Market Intelligence")
        st.caption("Define global posture, monitor competition, and set alignment targets.")
        
        cfg = load_config()
        
        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown("<div class='action-card'>", unsafe_allow_html=True)
            st.subheader("🎯 Strategy Configuration")
            with st.form("strategy_config"):
                hero = st.selectbox("Strategic Hero Product", mols['brand_name'].tolist(), index=mols['brand_name'].tolist().index(next((m['brand_name'] for m in mols.to_dict('records') if m['molecule_id'] == cfg['hero_product']), mols['brand_name'].iloc[0])))
                target = st.slider("Target Prescribing Share (%)", 0, 100, int(cfg['target_share'] * 100))
                
                hero_id = mols[mols['brand_name'] == hero]['molecule_id'].iloc[0]
                
                if st.form_submit_button("Deploy Global Strategy"):
                    cfg['hero_product'] = hero_id
                    cfg['target_share'] = target / 100
                    cfg['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    save_config(cfg)
                    st.success(f"Strategy deployed: Focused on {hero}")
            st.markdown("</div>", unsafe_allow_html=True)
            
        with c2:
            st.markdown("<div class='action-card'>", unsafe_allow_html=True)
            st.subheader("🕵️ Competitor Intelligence")
            new_comp = st.text_input("Add Competitor Company", placeholder="e.g. AbbVie, Pfizer")
            if st.button("Register Competitor"):
                if new_comp and new_comp not in cfg['competitor_list']:
                    cfg['competitor_list'].append(new_comp)
                    save_config(cfg)
                    st.rerun()
            
            if cfg['competitor_list']:
                st.write("Tracking Coverage:")
                for comp in cfg['competitor_list']:
                    st.markdown(f"● **{comp}** <span style='font-size:0.7rem; color:#ef4444; cursor:pointer;' onclick=''>[Remove]</span>", unsafe_allow_html=True)
                if st.button("Reset to Global Pharma Trends"):
                    cfg['competitor_list'] = []
                    save_config(cfg)
                    st.rerun()
            else:
                st.info("Current Mode: **Global Pharma Genius Trends** (Broad Market monitoring)")
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("🌍 Market Pulse & Insights")
        st.caption("Synthesizing current affairs and competitor moves.")
        
        news = get_market_news(cfg)
        for item in news:
            st.markdown(f"""
<div style='background:rgba(255,255,255,0.03); padding:15px; border-radius:10px; margin-bottom:10px; border:1px solid rgba(255,255,255,0.05);'>
    <div style='font-size:0.8rem; color:#10b981;'>{item['date']} • {item['source']}</div>
    <div style='font-weight:bold;'>{item['title']}</div>
</div>
""", unsafe_allow_html=True)
        
        if st.button("Synthesize Corporate Strategy Playbook", type="primary"):
            with st.spinner("Aetheris AI is synthesizing market data..."):
                playbook_points = generate_ai_strategy(cfg, news)
                st.session_state.current_playbook = playbook_points
        
        if 'current_playbook' in st.session_state:
            st.markdown("<h4 style='color: #10b981; margin-top:25px;'>✦ Aetheris Strategic Directives</h4>", unsafe_allow_html=True)
            for idx, insight in enumerate(st.session_state.current_playbook):
                c1, c2 = st.columns([4, 1])
                with c1:
                    st.markdown(f"""
<div style='background: rgba(255,255,255,0.03); padding: 15px; border-radius: 10px; border: 1px solid rgba(16, 185, 129, 0.2); margin-bottom: 10px;'>
    <div style='font-size: 0.9rem;'>{insight}</div>
</div>
""", unsafe_allow_html=True)
                with c2:
                    if st.button("🚀 Deploy", key=f"deploy_{idx}"):
                        reps = intel['rep_id'].unique()
                        for rep in reps:
                            add_activity("Admin", "HQ", "Strategic Directive", {
                                "plan_of_action": insight,
                                "instructions": "Transparent HQ Directive: Implement this marketing strategy immediately in your territory accounts."
                            }, assigned_to=rep)
                            # Find activities assigned to this rep and leave a note
                            acts = load_activity_log()
                            for a in acts:
                                if a.get("assigned_to") == rep and a["status"] != "Completed":
                                    a["admin_note"] = f"STRATEGIC UPDATE: {insight}"
                            save_activity_log(acts)
                        st.success(f"Directive Broadcasted to {len(reps)} Reps!")
        
    elif nav == nav_opts[2]: # Field Force
        st.title("Field Force Monitoring")
        st.caption("Live tracking of personnel interventions and account coverage.")
        
        cfg = load_config()
        align_df = get_strategic_analytics(pres, cfg)
        
        field_intel = intel.merge(align_df[['doctor_id', 'alignment_score']], on='doctor_id', how='left').fillna(0)
        
        field_rename = {
            "doctor_id": "HCP Account", "rep_id": "Field Personnel ID",
            "hybrid_score": "Rx Performance Index", "alignment_score": "Strategy Compliance (%)",
            "days_since_last_visit": "Market Coverage (Days)",
            "urgent_intervention": "Immediate Priority", "overdue_high_value": "Key Account Risk",
            "doctor_name": "Doctor Name", "specialty": "Speciality", "area": "Territory"
        }
        st.dataframe(field_intel.head(15).rename(columns={k:v for k,v in field_rename.items() if k in field_intel.columns}), use_container_width=True, hide_index=True)
        
    elif nav == nav_opts[3]: # Chemist Audit
        st.title("Doctor:Chemist Audit Inspection")
        st.caption("Verifying medical prescription volume against chemist retail data.")
        
        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown("### 🧪 Molecule Leakage Analysis")
            # Join audits with chemists for rich view
            rich_audit = audits.merge(chemists, on='chemist_id')
            # Mapping Dr to Chemist for display
            rich_audit['HCP_Account'] = rich_audit['top_doctor_map']
            
            display_audit = rich_audit[['HCP_Account', 'name', 'molecule_id', 'aetheris_vol', 'competitor_vol', 'leakage_pct']].copy()
            display_audit.columns = ["Linked HCP", "Chemist Outlet", "Molecule", "Aetheris Sales", "Competitor Sales", "Leakage (%)"]
            st.dataframe(display_audit, use_container_width=True, hide_index=True)
            
        with c2:
            st.markdown("<div class='action-card'>", unsafe_allow_html=True)
            st.subheader("⚠️ High Substitution Alert")
            critical_leaks = audits[audits['leakage_pct'] > 70].head(5)
            for _, row in critical_leaks.iterrows():
                st.error(f"**{row['chemist_id']}** - {row['molecule_id']}: **{row['leakage_pct']}%** Competitor Dominance. Field Rep intervention required.")
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.info("Proximal chemists are automatically mapped to Doctors based on regional hub proximity.")

    elif nav == nav_opts[4]: # Activity Queue
        st.title("Strategic Activity Queue")
        st.caption("Live command center for cross-role task processing.")
        
        acts = load_activity_log()
        if not acts:
            st.info("No active signals in the queue.")
        else:
            for act in reversed(acts):
                with st.container():
                    st.markdown(f"""
<div class='action-card' style='border-left: 5px solid {"#10b981" if act["status"] in ["Completed", "Acknowledged/Closed"] else "#f59e0b" if act["status"]=="Assigned" else "#3b82f6" if "Delivered" in act["status"] else "#ef4444"};'>
<div style='display: flex; justify-content: space-between;'>
<div>
<h4 style='margin:0;'>{act["action_type"]} <span style='font-size: 0.8rem; color:#9ca3af;'>({act["id"]})</span></h4>
<p style='margin:0; font-size:0.9rem; color:#9ca3af;'>Source: {act["source_role"]} ({act["source_id"]}) • {act["timestamp"]}</p>
<p style='margin-top:10px; color:#f3f4f6;'>{render_activity_details(act["details"])}</p>
{f"<p style='color:#f59e0b; font-size:0.85rem;'><b>Admin Alert:</b> {act['admin_note']}</p>" if act.get('admin_note') else ""}
<p style='margin-top:5px; font-weight:bold;'>Status: {act["status"]} ({act["confirmed_received"]} / {act["total_requested"]} Units confirmed)</p>
{f"<p style='color:#3b82f6; font-size:0.85rem;'>📦 <b>In Transit:</b> {act['in_transit_qty']} units</p>" if act.get('in_transit_qty') else ""}
</div>
<div style='text-align: right;'>
<p style='margin:0; color:#10b981;'>Assigned to: {act["assigned_to"] or "Unassigned"}</p>
</div>
</div>
</div>
""", unsafe_allow_html=True)
                    
                    if act["total_requested"] > 0:
                        prg = min(act["confirmed_received"] / act["total_requested"], 1.0)
                        st.progress(prg)
                        st.caption(f"Fulfillment Progress: {act['confirmed_received']} / {act['total_requested']} Units Confirmed")
                        if act.get("in_transit_qty", 0) > 0:
                            st.caption(f"🚀 Shipment in Transit: **{act['in_transit_qty']}** units")
                    
                    if act["status"] == "Pending":
                        c1, c2, _ = st.columns([2, 3, 5])
                        with c1:
                            target_rep = st.selectbox("Assign To", [f"REP{i:03}" for i in range(1, 11)], key=f"sel_{act['id']}")
                        with c2:
                            st.markdown("<div style='height:28px;'></div>", unsafe_allow_html=True) # Spacer
                            if st.button(f"Confirm Assignment", key=f"assign_{act['id']}"):
                                update_activity(act["id"], status="Assigned", assigned_to=target_rep)
                                st.rerun()
                    st.markdown("<br>", unsafe_allow_html=True)
        
    elif nav == nav_opts[4]: # National Map
        st.title("National Territory Intelligence")
        st.caption("Enterprise-grade density analysis across all clinical hubs.")
        
        c1, c2 = st.columns([2, 1])
        with c1:
            fig = px.treemap(docs, path=['area', 'specialty'], values='avg_patients_per_day',
                           color='avg_patients_per_day', color_continuous_scale='Viridis',
                           title="Market Load Density: Patient Volume by Hub & Speciality")
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.markdown("<div class='action-card'>", unsafe_allow_html=True)
            st.subheader("📍 Regional Pulse")
            area_stats = docs.groupby('area')['avg_patients_per_day'].sum().sort_values(ascending=False)
            for area, vol in area_stats.items():
                st.write(f"**{area}:** {vol:,.0f} Patients/Day")
            st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 🩺 DOCTOR DASHBOARD (Partner Portal)
# ==========================================
elif st.session_state.user_role == "Doctor":
    doc_id = st.session_state.user_id
    
    if nav == nav_opts[0]: # Target Requirements
        st.title("Molecular Target Requirements")
        st.caption("Prescription milestones discussed with your assigned Aetheris Rep.")
        
        st.markdown("<div class='action-card'>", unsafe_allow_html=True)
        st.markdown("### Monthly Alignment Protocol")
        st.write("Your account is synchronized with Aetheris's strategic pipeline. Maintaining the prescribed molecular targets ensures uninterrupted sample inventory and consistent supply chain support for your clinic's patient load.")
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        col1.metric("Current Monthly Compliance", "84%", "+4% vs Last Month")
        col2.metric("Accumulated Clinic Credits", "1,250", "-150 used offline")
        
        st.progress(0.84)
        st.markdown("</div>", unsafe_allow_html=True)
        
    elif nav == nav_opts[1]: # Rx History
        st.title("Your Rx Fulfillment Log")
        
        doc_col_map = {
            "doctor_id": "Doctor ID",
            "molecule_id": "Molecular Compound",
            "month": "Reporting Period",
            "hybrid_score": "Compliance Score",
            "rank": "Market Rank",
            "mom_delta_pct": "Monthly Growth %",
            "consecutive_decline": "Trend: Consecutive Drop",
            "rank_drop_alert": "Alert: Market Slide",
            "new_prescriber_flag": "Inaugural Prescription",
            "high_leakage_doctor": "Switching Pattern Alert",
            "name": "Doctor Name"
        }

        try:
            my_pres = pres[pres['doctor_id'] == doc_id]
            if len(my_pres) == 0:
                st.info("No external Rx data logged for your ID yet. Showing sample structure below:")
                display_df = pres.head(5).rename(columns={k: v for k, v in doc_col_map.items() if k in pres.columns})
                st.dataframe(display_df, use_container_width=True, hide_index=True)
            else:
                display_df = my_pres.rename(columns={k: v for k, v in doc_col_map.items() if k in my_pres.columns})
                st.dataframe(display_df, use_container_width=True, hide_index=True)
        except:
            display_df = pres.head(5).rename(columns={k: v for k, v in doc_col_map.items() if k in pres.columns})
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
    elif nav == nav_opts[2]: # Deliveries
        st.title("Incoming Shipments & Registries")
        
        acts = load_activity_log()
        my_deliveries = [a for a in acts if a["source_id"] == doc_id and a["total_requested"] > 0]
        
        if my_deliveries:
            st.subheader("Your Sample Requisitions")
            for act in reversed(my_deliveries):
                with st.container():
                    st.markdown(f"""
<div class='action-card' style='border-left: 5px solid {"#10b981" if act["acknowledged"] and act["confirmed_received"] >= act["total_requested"] else "#3b82f6"};'>
<h4>{act["action_type"]} - {act["timestamp"]}</h4>
<p>{render_activity_details(act["details"])}</p>
{f"<p style='color: #60a5fa;'><b>Update:</b> {act['doctor_note']}</p>" if act.get('doctor_note') and not act["acknowledged"] else ""}
<p><b>Status:</b> {act["status"]} ({act["confirmed_received"]}/{act["total_requested"]} Confirmed)</p>
{f"<p style='background:rgba(59,130,246,0.1); padding:10px; border-radius:5px; border: 1px solid rgba(59,130,246,0.2);'>📦 <b>Shipment Arrived:</b> Please acknowledge receipt of <b>{act['in_transit_qty']}</b> units.</p>" if act.get('in_transit_qty') > 0 else ""}
</div>
""", unsafe_allow_html=True)
                    
                    if act["in_transit_qty"] > 0:
                        if st.button(f"Confirm Receipt of Batch ({act['in_transit_qty']} units)", key=f"ack_{act['id']}"):
                            new_confirmed = act["confirmed_received"] + act["in_transit_qty"]
                            new_status = "Acknowledged/Closed" if new_confirmed >= act["total_requested"] else "Partially Fulfilled"
                            update_activity(act["id"], confirmed_received=new_confirmed, in_transit_qty=0, status=new_status, acknowledged=True)
                            st.rerun()
                    st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("---")
        st.subheader("Approved Molecules Registry")
        mol_col_map = {
            "molecule_id": "Compound Code",
            "brand_name": "Proprietary Name",
            "therapy_area": "Therapeutic Classification",
            "MRP_per_unit": "Unit Pricing (MRP)",
            "margin_percent": "Clinic Margin (%)"
        }
        display_mols = mols.rename(columns={k: v for k, v in mol_col_map.items() if k in mols.columns})
        st.dataframe(display_mols, use_container_width=True, hide_index=True)
        
    elif nav == nav_opts[3]: # Support
        st.title("Partner Support")
        st.markdown("<div class='action-card'>", unsafe_allow_html=True)
        st.subheader("Request Specific Inventory/Samples")
        with st.form("doc_support"):
            nature = st.selectbox("Inquiry Nature", ["Request Priority Visit from Rep", "Sample Restock", "Clinical Efficacy Query"])
            details = st.text_area("Details")
            if st.form_submit_button("Send to Representative", type="primary"):
                add_activity("Doctor", st.session_state.user_id, "Support Inquiry", {"nature": nature, "details": details})
                st.success("Your assigned Sales Rep has been notified on their dashboard.")
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 💼 SALES REP DASHBOARD (Daily Companion)
# ==========================================
elif st.session_state.user_role == "Sales Rep":
    
    # NEW: Global Strategy Directive Section
    acts = load_activity_log()
    directives = [a for a in acts if a["action_type"] == "Strategic Directive" and a["assigned_to"] == st.session_state.user_id]
    
    if directives:
        with st.expander("📡 [HIGH PRIORITY] LIVE HQ STRATEGIC DIRECTIVES", expanded=True):
            for d in reversed(directives[-3:]): # Show last 3
                st.markdown(f"""
<div style='background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(59, 130, 246, 0.2) 100%); padding: 15px; border-radius: 12px; border: 1px solid rgba(16, 185, 129, 0.4); margin-bottom: 15px;'>
    <div style='font-size: 0.75rem; color: #10b981; font-weight: bold; margin-bottom: 5px;'>✦ HQ DIRECTIVE RECEIVED • {d['timestamp']}</div>
    <div style='font-weight: bold; font-size: 1.1rem; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 5px;'>{d['details']['plan_of_action']}</div>
    <div style='font-size: 0.85rem; color: #e5e7eb; margin-top: 8px;'><b>Plan of Action:</b> {d['details']['instructions']}</div>
</div>
""", unsafe_allow_html=True)

    if nav == nav_opts[0]: # Focus Today
        st.subheader("📍 Critical Daily Agenda")
        my_docs = intel[intel['rep_id'] == st.session_state.user_id].merge(docs[['doctor_id', 'name', 'specialty', 'area']], on='doctor_id')
        top_focus = my_docs.sort_values(['urgent_intervention', 'overdue_high_value'], ascending=False).head(3)
        
        # Strategy Alignment Enrichment
        cfg = load_config()
        align_df = get_strategic_analytics(pres, cfg)
        my_docs = my_docs.merge(align_df[['doctor_id', 'alignment_score']], on='doctor_id', how='left').fillna(0)
        
        for idx, row in top_focus.iterrows():
            # Get alignment for this specific row
            matching_align = align_df[align_df['doctor_id'] == row['doctor_id']]
            curr_align = matching_align['alignment_score'].iloc[0] if not matching_align.empty else 0
            
            badge = "badge-urgent" if row['urgent_intervention'] == 1 else "badge-overdue"
            label = "CRITICAL: Urgent Action Required" if row['urgent_intervention'] == 1 else "Action: Long Overdue Visit"
            
            with st.container():
                st.markdown(f"""
<div class='action-card'>
<div style='display: flex; justify-content: space-between; align-items: flex-start;'>
<div>
<h3 style='margin:0;'>{row['name']} <span class='status-badge {badge}'>{label}</span></h3>
<p style='margin-top:5px; color:#9ca3af;'>{row['specialty']} • {row['area']}</p>
</div>
<div style='text-align: right;'>
<p style='margin:0; color:#10b981; font-size:1.2rem; font-weight:bold;'>Health: {row['hybrid_score']:.0f}/100</p>
<p style='margin:0; font-size:0.8rem; color:#9ca3af;'>Strategy Alignment: <b>{curr_align:.0f}%</b></p>
</div>
</div>
</div>
""", unsafe_allow_html=True)
                
                # XAI Layer Pulse Check insertion
                insight = get_xai_insight(row)
                st.markdown(f"""
<div class='xai-pulse'>
<div class='xai-label'>✦ Aetheris AI Insight Pulse</div>
<div style='font-size: 0.9rem;'>{insight}</div>
</div>
<br>
""", unsafe_allow_html=True)
                
                c1, c2, c3 = st.columns([1,1,2])
                with c1: 
                    if st.button(f"Log Visit: {row['name']}", key=f"v_{idx}"):
                        st.session_state.active_modal = "log_visit"
                        st.session_state.modal_data = row['name']
                        st.rerun()
                with c2: 
                    if st.button(f"Call {row['name']}", key=f"c_{idx}"):
                        st.session_state.active_modal = "call"
                        st.session_state.modal_data = row['name']
                        st.rerun()

        st.markdown("---")
        st.subheader("📋 My Assignments")
        st.caption("Tasks assigned by Enterprise Operations or Partner HCPs.")
        
        acts = load_activity_log()
        my_acts = [a for a in acts if a["assigned_to"] == st.session_state.user_id and a["status"] in ["Assigned", "Partially Delivered"]]
        
        if not my_acts:
            st.info("No active assignments for today. Great job!")
        else:
            for act in my_acts:
                with st.container():
                    st.markdown(f"""
<div class='action-card' style='border-left: 5px solid #f59e0b;'>
<h4 style='margin:0;'>{act["action_type"]}</h4>
<p style='margin:0; font-size: 0.9rem; color: #9ca3af;'>From: {act["source_role"]} ({act["source_id"]}) • {act["timestamp"]}</p>
<p style='margin-top: 10px;'>{render_activity_details(act["details"])}</p>
</div>
""", unsafe_allow_html=True)
                    
                    if act["total_requested"] > 0:
                        st.caption(f"Progress: <b>{act['confirmed_received']} / {act['total_requested']}</b> confirmed", unsafe_allow_html=True)
                        if act["in_transit_qty"] > 0:
                            st.info(f"Currently in Transit: {act['in_transit_qty']} units (Awaiting HCP Receipt)")
                        
                        with st.form(f"batch_{act['id']}"):
                            remaining = act["total_requested"] - act["confirmed_received"] - act["in_transit_qty"]
                            if remaining > 0:
                                delivery_amt = st.number_input("Dispatch Shipment Batch (Quantity)", min_value=1, max_value=remaining, value=min(remaining, 50))
                                if st.form_submit_button("Dispatch to HCP"):
                                    new_transit = act["in_transit_qty"] + delivery_amt
                                    status = "Shipment in Transit"
                                    
                                    admin_note = f"Dispatch logged: {delivery_amt} units. Total in transit: {new_transit}"
                                    doctor_note = f"A batch of {delivery_amt} units has been dispatched to your clinic. Please confirm on arrival."
                                    
                                    update_activity(act["id"], 
                                                    in_transit_qty=new_transit, 
                                                    status=status, 
                                                    acknowledged=False,
                                                    admin_note=admin_note,
                                                    doctor_note=doctor_note)
                                    st.success(f"Batch of {delivery_amt} dispatched!")
                                    st.rerun()
                            else:
                                st.success("All units for this goal are either confirmed or in transit.")
                    else:
                        if st.button(f"Mark Task Completed", key=f"comp_{act['id']}"):
                            update_activity(act["id"], status="Completed", completed_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            st.rerun()
                    st.markdown("<br>", unsafe_allow_html=True)
                        
    elif nav == nav_opts[1]: # My Results
        st.title("Performance Hub")
        fig = px.bar(pres.head(10), x='name', y='hybrid_score', 
                     labels={'name': 'Doctor Name', 'hybrid_score': 'Performance Score'},
                     title="Your Top-Yielding Accounts")
        st.plotly_chart(fig, use_container_width=True)
    
    elif nav == nav_opts[2]: # Intelligence
        st.title("Your Action Recommendations")
        st.caption("These are personalised tips generated from the latest market signals in your territory.")
    
        col_rename_map = {
            "doctor_id": "Doctor ID", "rep_id": "Your ID", "molecule_id": "Product Target",
            "month": "Reporting Period", "alert_type": "Signal Type", "priority": "Priority Level",
            "days_since_last_visit": "Days Since Last Visit", "days_since_last_gift": "Days Since Last Sample Drop",
            "negative_count": "Negative Trend Count", "recommended_action": "Suggested Strategy",
            "intervention_type": "Action Category", "action_description": "What To Do",
            "urgency": "Urgency Level", "doctor_name": "Doctor Name",
            "brand_name": "Product / Brand", "area": "Territory", "specialty": "Speciality",
        }
    
        # Only rename columns that actually exist in the dataframe
        present_renames = {k: v for k, v in col_rename_map.items() if k in recs.columns}
        display_df = recs.head(15).rename(columns=present_renames)
    
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    elif nav == nav_opts[3]: # Territory
        st.title("Territory Analysis")
        fig = px.treemap(docs, path=['area', 'specialty'], values='avg_patients_per_day',
                       title="Market Density: Patient Load by Specialty and Area")
        st.plotly_chart(fig, use_container_width=True)
