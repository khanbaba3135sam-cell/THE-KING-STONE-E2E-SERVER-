# streamlit_app.py
import streamlit as st
import time
import threading
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import database as db
import requests
import os
import hashlib
import socket
import json
import random

# -------------------------
# Config & Admin Credentials
# -------------------------
ADMIN_USERNAME = "KINGSAM"
ADMIN_PASSWORD = "samking123"

GITHUB_RAW_URL = "https://raw.githubusercontent.com/deepakdhurve6588-debug/OPX/main/app.txt"
APPROVALS_FILE = "approvals.json"

CONTACT_LINKS = {
    "whatsapp": "https://wa.me/919876543210",
    "telegram": "https://t.me/waleedlegend",
    "facebook": "https://m.facebook.com/waleed.legend"
}

# -------------------------
# Streamlit Page Config + CSS
# -------------------------
st.set_page_config(
    page_title="STONE LEGEND E2E",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    * { font-family: 'Poppins', sans-serif; }
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    .main .block-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 32px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        transition: 0.3s;
    }
    .main .block-container:hover { box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15); }
    .main-header { 
        background: rgba(255, 255, 255, 0.15); 
        background-image: url("https://i.postimg.cc/Zq4ZMNyz/546c121c192e6a7a8e88bec385d375d5.jpg"); 
        background-size: cover; 
        background-position: center; 
        background-repeat: no-repeat; 
        backdrop-filter: blur(12px) brightness(0.9); 
        -webkit-backdrop-filter: blur(12px) brightness(0.9); 
        padding: 2rem; 
        border-radius: 18px; 
        text-align: center; 
        margin-bottom: 2rem; 
        border: 1px solid rgba(255, 255, 255, 0.2); 
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2); 
        position: relative; 
        overflow: hidden; 
    }
    .main-header::before { 
        content: ""; 
        position: absolute; 
        inset: 0; 
        background: rgba(0, 0, 0, 0.25); 
        border-radius: 18px; 
        z-index: 0; 
    }
    .main-header h1, .main-header p { 
        position: relative; 
        z-index: 1; 
        color: #fff; 
    }
    .main-header h1 { 
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4); 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent; 
        background-clip: text; 
        font-size: 2.5rem; 
        font-weight: 700; 
        margin: 0; 
    }
    .main-header p { 
        color: rgba(255, 255, 255, 0.9); 
        font-size: 1.1rem; 
        margin-top: 0.5rem; 
    }
    .legend-logo { 
        width: 80px; 
        height: 80px; 
        border-radius: 15px; 
        margin-bottom: 15px; 
        border: 2px solid #4ecdc4; 
        box-shadow: 0 4px 10px rgba(78, 205, 196, 0.4); 
        transition: transform 0.3s ease, box-shadow 0.3s ease; 
    }
    .legend-logo:hover { 
        transform: scale(1.08); 
        box-shadow: 0 6px 14px rgba(78, 205, 196, 0.6); 
    }
    .stButton>button { 
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4); 
        color: white; 
        border: none; 
        border-radius: 10px; 
        padding: 0.75rem 2rem; 
        font-weight: 600; 
        font-size: 1rem; 
        transition: all 0.3s ease; 
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4); 
        width: 100%; 
    }
    .stButton>button:hover { 
        opacity: 0.9; 
        transform: translateY(-2px); 
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6); 
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stNumberInput>div>div>input { 
        background: rgba(255, 255, 255, 0.15); 
        border: 1px solid rgba(255, 255, 255, 0.25); 
        border-radius: 8px; 
        color: white; 
        padding: 0.75rem; 
        transition: all 0.3s ease; 
    }
    .stTextInput>div>div>input::placeholder, .stTextArea>div>div>textarea::placeholder { 
        color: rgba(255, 255, 255, 0.6); 
    }
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus { 
        background: rgba(255, 255, 255, 0.2); 
        border-color: #4ecdc4; 
        box-shadow: 0 0 0 2px rgba(78, 205, 196, 0.2); 
        color: white; 
    }
    label { 
        color: white !important; 
        font-weight: 500 !important; 
        font-size: 14px !important; 
    }
    .stTabs [data-baseweb="tab-list"] { 
        gap: 8px; 
        background: rgba(255, 255, 255, 0.06); 
        padding: 10px; 
        border-radius: 10px; 
    }
    .stTabs [data-baseweb="tab"] { 
        background: rgba(255, 255, 255, 0.1); 
        border-radius: 8px; 
        color: white; 
        padding: 10px 20px; 
    }
    .stTabs [aria-selected="true"] { 
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4); 
    }
    [data-testid="stMetricValue"] { 
        color: #4ecdc4; 
        font-weight: 700; 
        font-size: 1.8rem; 
    }
    [data-testid="stMetricLabel"] { 
        color: rgba(255, 255, 255, 0.9); 
        font-weight: 500; 
    }
    .console-section { 
        margin-top: 20px; 
        padding: 15px; 
        background: rgba(255, 255, 255, 0.06); 
        border-radius: 10px; 
        border: 1px solid rgba(78, 205, 196, 0.3); 
    }
    .console-header { 
        color: #4ecdc4; 
        text-shadow: 0 0 10px rgba(78, 205, 196, 0.5); 
        margin-bottom: 20px; 
        font-weight: 600; 
    }
    .console-output { 
        background: rgba(0, 0, 0, 0.5); 
        border: 1px solid rgba(78, 205, 196, 0.4); 
        border-radius: 10px; 
        padding: 12px; 
        font-family: 'Courier New', 'Consolas', 'Monaco', monospace; 
        font-size: 12px; 
        color: #00ff88; 
        line-height: 1.6; 
        max-height: 400px; 
        overflow-y: auto; 
        scrollbar-width: thin; 
        scrollbar-color: rgba(78, 205, 196, 0.5) rgba(0, 0, 0, 0.2); 
    }
    .console-output::-webkit-scrollbar { 
        width: 8px; 
    }
    .console-output::-webkit-scrollbar-track { 
        background: rgba(0, 0, 0, 0.2); 
    }
    .console-output::-webkit-scrollbar-thumb { 
        background: rgba(78, 205, 196, 0.5); 
        border-radius: 4px; 
    }
    .console-output::-webkit-scrollbar-thumb:hover { 
        background: rgba(78, 205, 196, 0.7); 
    }
    .console-line { 
        margin-bottom: 3px; 
        word-wrap: break-word; 
        padding: 6px 10px; 
        padding-left: 28px; 
        color: #00ff88; 
        background: rgba(78, 205, 196, 0.08); 
        border-left: 2px solid rgba(78, 205, 196, 0.4); 
        position: relative; 
    }
    .console-line::before { 
        content: ''; 
        position: absolute; 
        left: 10px; 
        opacity: 0.6; 
        color: #4ecdc4; 
    }
    .success-box { 
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%); 
        padding: 1rem; 
        border-radius: 10px; 
        color: white; 
        text-align: center; 
        margin: 1rem 0; 
    }
    .error-box { 
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); 
        padding: 1rem; 
        border-radius: 10px; 
        color: white; 
        text-align: center; 
        margin: 1rem 0; 
    }
    .info-card { 
        background: rgba(255, 255, 255, 0.1); 
        backdrop-filter: blur(10px); 
        padding: 1.5rem; 
        border-radius: 15px; 
        margin: 1rem 0; 
        border: 1px solid rgba(255, 255, 255, 0.15); 
    }
    .footer { 
        text-align: center; 
        padding: 2rem; 
        color: rgba(255, 255, 255, 0.7); 
        font-weight: 600; 
        margin-top: 3rem; 
        background: rgba(255, 255, 255, 0.05); 
        border-radius: 10px; 
        border-top: 1px solid rgba(255, 255, 255, 0.15); 
    }
    [data-testid="stSidebar"] { 
        background: rgba(0, 0, 0, 0.3); 
        backdrop-filter: blur(10px); 
    }
    [data-testid="stSidebar"] .element-container { 
        color: white; 
    }
    .approval-box {
        background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 2rem 0;
        color: white;
    }
    .approval-key {
        background: rgba(0, 0, 0, 0.2);
        padding: 1rem;
        border-radius: 10px;
        font-family: 'Courier New', monospace;
        font-size: 1.2rem;
        margin: 1rem 0;
        border: 2px dashed white;
    }
    .admin-panel { 
        padding: 12px; 
        background: rgba(255,255,255,0.05); 
        border-radius: 10px; 
    }
    .status-running {
        color: #00ff88;
        font-weight: bold;
    }
    .status-stopped {
        color: #ff6b6b;
        font-weight: bold;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# -------------------------
# Session State defaults
# -------------------------
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'automation_running' not in st.session_state:
    st.session_state.automation_running = False
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'message_count' not in st.session_state:
    st.session_state.message_count = 0
if 'approval_key' not in st.session_state:
    st.session_state.approval_key = None
if 'approved' not in st.session_state:
    st.session_state.approved = False
if 'approval_checked' not in st.session_state:
    st.session_state.approval_checked = False

class AutomationState:
    def __init__(self):
        self.running = False
        self.message_count = 0
        self.logs = []
        self.message_rotation_index = 0

if 'automation_state' not in st.session_state:
    st.session_state.automation_state = AutomationState()
if 'auto_start_checked' not in st.session_state:
    st.session_state.auto_start_checked = False

# -------------------------
# Database initialization
# -------------------------
try:
    db.init_db()
except Exception as e:
    st.error(f"Database initialization error: {e}")

# -------------------------
# Approval storage helpers
# -------------------------
def load_local_approvals():
    if not os.path.exists(APPROVALS_FILE):
        return []
    try:
        with open(APPROVALS_FILE, 'r') as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except Exception:
        return []

def save_local_approvals(keys_list):
    try:
        with open(APPROVALS_FILE, 'w') as f:
            json.dump(keys_list, f, indent=2)
        return True
    except Exception:
        return False

def is_key_locally_approved(key):
    local = load_local_approvals()
    return key in local

def approve_key_locally(key):
    keys = load_local_approvals()
    if key not in keys:
        keys.append(key)
        save_local_approvals(keys)

def revoke_key_locally(key):
    keys = load_local_approvals()
    if key in keys:
        keys.remove(key)
        save_local_approvals(keys)

# -------------------------
# Approval check functions
# -------------------------
def generate_approval_key(username, user_id):
    try:
        hostname = socket.gethostname()
    except:
        hostname = "unknown"
    fingerprint = f"{username}_{user_id}_{hostname}"
    key_hash = hashlib.md5(fingerprint.encode()).hexdigest()[:12].upper()
    return f"WL-{key_hash}"

def check_github_approval(key):
    """Check if key exists in GitHub approval file"""
    try:
        response = requests.get(GITHUB_RAW_URL, timeout=8)
        if response.status_code == 200:
            approved_keys = [k.strip() for k in response.text.split('\n') if k.strip()]
            if key in approved_keys:
                return True
    except Exception:
        pass
    # fallback to local approvals
    return is_key_locally_approved(key)

# -------------------------
# Utility logging
# -------------------------
def log_message(msg, automation_state=None):
    timestamp = time.strftime("%H:%M:%S")
    formatted_msg = f"[{timestamp}] {msg}"
    if automation_state:
        automation_state.logs.append(formatted_msg)
    else:
        if 'logs' in st.session_state:
            st.session_state.logs.append(formatted_msg)

# -------------------------
# Browser Automation Functions
# -------------------------
def setup_browser(automation_state=None):
    log_message('Setting up Chrome browser...', automation_state)
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-setuid-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
    
    # Set Chrome binary location
    chrome_options.binary_location = "/usr/bin/chromium-browser"
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        log_message('Chrome browser setup completed successfully!', automation_state)
        return driver
    except Exception as error:
        log_message(f'Browser setup failed: {error}', automation_state)
        raise error

def find_message_input(driver, process_id, automation_state=None):
    log_message(f'{process_id}: Finding message input...', automation_state)
    time.sleep(5)
    
    # Scroll to ensure page is loaded
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
    except Exception:
        pass
    
    message_input_selectors = [
        'div[contenteditable="true"][role="textbox"]',
        'div[contenteditable="true"][data-lexical-editor="true"]',
        'div[aria-label*="message" i][contenteditable="true"]',
        'div[contenteditable="true"][spellcheck="true"]',
        '[role="textbox"][contenteditable="true"]',
        'textarea[placeholder*="message" i]',
        'div[aria-placeholder*="message" i]',
        '[contenteditable="true"]',
        'textarea',
        'input[type="text"]'
    ]
    
    for idx, selector in enumerate(message_input_selectors):
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            for element in elements:
                try:
                    if element.is_displayed() and element.is_enabled():
                        element.click()
                        time.sleep(1)
                        log_message(f'{process_id}:  Found message input with selector #{idx+1}', automation_state)
                        return element
                except Exception:
                    continue
        except Exception:
            continue
    
    log_message(f'{process_id}:  Message input not found with standard selectors', automation_state)
    return None

def get_next_message(messages, automation_state=None):
    if not messages or len(messages) == 0:
        return 'Hello from STONE LEGEND E2E!'
    if automation_state:
        message = messages[automation_state.message_rotation_index % len(messages)]
        automation_state.message_rotation_index += 1
    else:
        message = messages[0]
    return message

def send_messages(config, automation_state, user_id, process_id='AUTO-1'):
    driver = None
    try:
        log_message(f'{process_id}: Starting STONE LEGEND E2E automation...', automation_state)
        driver = setup_browser(automation_state)
        
        # Navigate to Facebook
        log_message(f'{process_id}: Navigating to Facebook...', automation_state)
        driver.get('https://www.facebook.com/')
        time.sleep(8)
        
        # Add cookies if provided
        if config.get('cookies') and config['cookies'].strip():
            log_message(f'{process_id}: Adding cookies...', automation_state)
            try:
                cookies = json.loads(config['cookies'])
                for cookie in cookies:
                    driver.add_cookie(cookie)
                driver.refresh()
                time.sleep(5)
            except Exception as e:
                log_message(f'{process_id}: Cookie error: {e}', automation_state)
        
        # Navigate to messages
        chat_id = config.get('chat_id', '').strip()
        if chat_id:
            log_message(f'{process_id}: Opening conversation {chat_id}...', automation_state)
            driver.get(f'https://www.facebook.com/messages/t/{chat_id}')
        else:
            log_message(f'{process_id}: Opening messages page...', automation_state)
            driver.get('https://www.facebook.com/messages')
        
        time.sleep(10)
        
        # Find message input
        message_input = find_message_input(driver, process_id, automation_state)
        if not message_input:
            log_message(f'{process_id}:  Message input not found!', automation_state)
            automation_state.running = False
            db.set_automation_running(user_id, False)
            return 0
        
        delay = int(config.get('delay', 10))
        messages_sent = 0
        messages_list = [msg.strip() for msg in config.get('messages', 'Hello!').split('\n') if msg.strip()]
        
        if not messages_list:
            messages_list = ['Hello from STONE LEGEND E2E!']
        
        # Main messaging loop
        while automation_state.running and messages_sent < 100:  # Safety limit
            message_text = get_next_message(messages_list, automation_state)
            
            # Add name prefix if configured
            if config.get('name_prefix'):
                message_text = f"{config['name_prefix']} {message_text}"
            
            try:
                # Clear and send message
                message_input.clear()
                message_input.send_keys(message_text)
                time.sleep(1)
                message_input.send_keys(Keys.RETURN)
                
                messages_sent += 1
                automation_state.message_count = messages_sent
                log_message(f'{process_id}:  Message {messages_sent} sent: {message_text[:50]}...', automation_state)
                
                time.sleep(delay)
                
            except Exception as e:
                log_message(f'{process_id}:  Error sending message: {e}', automation_state)
                break
        
        log_message(f'{process_id}:  Automation completed! Total messages: {messages_sent}', automation_state)
        return messages_sent
        
    except Exception as e:
        log_message(f'{process_id}:  Fatal error: {str(e)}', automation_state)
        return 0
    finally:
        if driver:
            try:
                driver.quit()
                log_message(f'{process_id}: Browser closed', automation_state)
            except:
                pass
        automation_state.running = False
        db.set_automation_running(user_id, False)

def send_telegram_notification(username, message_count, automation_state=None):
    try:
        # Telegram bot configuration (replace with actual tokens)
        telegram_bot_token = "YOUR_BOT_TOKEN"
        telegram_admin_chat_id = "YOUR_CHAT_ID"
        
        if not telegram_bot_token or telegram_bot_token == "YOUR_BOT_TOKEN":
            return False
            
        from datetime import datetime
        import pytz
        
        kolkata_tz = pytz.timezone('Asia/Kolkata')
        current_time = datetime.now(kolkata_tz).strftime("%Y-%m-%d %H:%M:%S")
        
        notification_message = f""" *STONE LEGEND E2E - Automation Report*
 *User:* {username}
 *Time:* {current_time}
 *Messages Sent:* {message_count}
 Automation completed successfully!"""
        
        url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
        data = {
            "chat_id": telegram_admin_chat_id,
            "text": notification_message,
            "parse_mode": "Markdown"
        }
        
        response = requests.post(url, data=data, timeout=10)
        return response.status_code == 200
        
    except Exception:
        return False

def run_automation_with_notification(user_config, username, automation_state, user_id):
    message_count = send_messages(user_config, automation_state, user_id)
    
    # Send notification if messages were sent
    if message_count > 0:
        send_telegram_notification(username, message_count, automation_state)

def start_automation(user_config, user_id):
    automation_state = st.session_state.automation_state
    if automation_state.running:
        log_message("Automation already running!", automation_state)
        return
        
    automation_state.running = True
    automation_state.message_count = 0
    automation_state.logs = []
    automation_state.message_rotation_index = 0
    
    db.set_automation_running(user_id, True)
    username = db.get_username(user_id)
    
    # Start automation in background thread
    thread = threading.Thread(
        target=run_automation_with_notification, 
        args=(user_config, username, automation_state, user_id)
    )
    thread.daemon = True
    thread.start()
    
    log_message(" STONE LEGEND E2E automation started!", automation_state)

def stop_automation(user_id):
    st.session_state.automation_state.running = False
    db.set_automation_running(user_id, False)
    log_message(" Automation stopped by user", st.session_state.automation_state)

# -------------------------
# UI: Header
# -------------------------
st.markdown("""
<div class="main-header">
    <img src="https://i.postimg.cc/9fpZqGjn/17adef215d4766a8620c99e8a17227b5.jpg" class="legend-logo">
    <h1>STONE LEGEND E2E<br>AUTOMATION SYSTEM</h1>
    <p>End-to-End Facebook Message Automation</p>
</div>
""", unsafe_allow_html=True)

# -------------------------
# LOGIN / SIGNUP / ADMIN TAB
# -------------------------
if not st.session_state.logged_in and not st.session_state.is_admin:
    tab1, tab2, tab3 = st.tabs([" Login", " Sign Up", " Admin"])
    
    # User Login
    with tab1:
        st.markdown("### Welcome to STONE LEGEND E2E!")
        username = st.text_input("Username", key="login_username", placeholder="Enter your username")
        password = st.text_input("Password", key="login_password", type="password", placeholder="Enter your password")
        
        if st.button("Login", key="login_btn", use_container_width=True):
            if username and password:
                # Admin login check
                if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                    st.session_state.is_admin = True
                    st.session_state.username = ADMIN_USERNAME
                    st.success(" Admin logged in successfully!")
                    st.rerun()
                else:
                    # User login
                    user_id = db.verify_user(username, password)
                    if user_id:
                        st.session_state.logged_in = True
                        st.session_state.user_id = user_id
                        st.session_state.username = username
                        st.session_state.approval_key = generate_approval_key(username, user_id)
                        st.session_state.approved = check_github_approval(st.session_state.approval_key)
                        st.session_state.approval_checked = True
                        
                        if st.session_state.approved:
                            st.success(f" Welcome {username}! Access granted.")
                        else:
                            st.success(f" Logged in as {username} - Approval pending.")
                        st.rerun()
                    else:
                        st.error(" Invalid username or password!")
            else:
                st.warning(" Please enter both username and password")
    
    # Sign Up
    with tab2:
        st.markdown("### Create New Account")
        new_username = st.text_input("Choose Username", key="signup_username", placeholder="Choose a unique username")
        new_password = st.text_input("Choose Password", key="signup_password", type="password", placeholder="Create a strong password")
        confirm_password = st.text_input("Confirm Password", key="confirm_password", type="password", placeholder="Re-enter your password")
        
        if st.button("Create Account", key="signup_btn", use_container_width=True):
            if new_username and new_password and confirm_password:
                if new_password == confirm_password:
                    success, message = db.create_user(new_username, new_password)
                    if success:
                        st.success(f" {message}")
                    else:
                        st.error(f" {message}")
                else:
                    st.error(" Passwords do not match!")
            else:
                st.warning(" Please fill all fields")
    
    # Admin Login
    with tab3:
        st.markdown("### Admin Access")
        admin_user = st.text_input("Admin Username", key="admin_username")
        admin_pass = st.text_input("Admin Password", key="admin_password", type="password")
        
        if st.button("Admin Login", key="admin_login_btn", use_container_width=True):
            if admin_user == ADMIN_USERNAME and admin_pass == ADMIN_PASSWORD:
                st.session_state.is_admin = True
                st.session_state.username = ADMIN_USERNAME
                st.success(" Admin logged in successfully!")
                st.rerun()
            else:
                st.error(" Invalid admin credentials!")

# -------------------------
# ADMIN PANEL
# -------------------------
if st.session_state.is_admin:
    st.sidebar.markdown(f"###  Admin Panel")
    st.sidebar.markdown(f"**User:** {st.session_state.username}")
    
    if st.sidebar.button(" Logout", use_container_width=True):
        st.session_state.is_admin = False
        st.session_state.username = None
        st.rerun()
    
    st.markdown("<div class='admin-panel'><h3> STONE LEGEND E2E - Admin Control Center</h3></div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### User Management & Approvals")
        
        # Local approvals management
        local_keys = load_local_approvals()
        if local_keys:
            st.markdown("**Approved Keys:**")
            for key in local_keys:
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.code(key)
                with col_b:
                    if st.button(f"Revoke", key=f"revoke_{key}"):
                        revoke_key_locally(key)
                        st.success(f"Revoked {key}")
                        st.rerun()
        else:
            st.info("No local approvals found.")
        
        st.markdown("---")
        st.markdown("#### Manual Key Approval")
        manual_key = st.text_input("Enter approval key:", placeholder="WL-XXXXXXXXXXXX")
        col_x, col_y = st.columns(2)
        with col_x:
            if st.button(" Approve Key", use_container_width=True):
                if manual_key and manual_key.startswith("WL-"):
                    approve_key_locally(manual_key)
                    st.success(f"Key {manual_key} approved!")
                    st.rerun()
                else:
                    st.error("Invalid key format!")
        with col_y:
            if st.button(" Revoke Key", use_container_width=True):
                if manual_key:
                    revoke_key_locally(manual_key)
                    st.success(f"Key {manual_key} revoked!")
                    st.rerun()
    
    with col2:
        st.markdown("#### Admin Tools")
        if st.button("View All Users", use_container_width=True):
            try:
                users = db.get_all_users()
                if users:
                    st.markdown("**Registered Users:**")
                    for user in users:
                        st.text(f" {user.get('username', 'N/A')} (ID: {user.get('id', 'N/A')})")
                else:
                    st.info("No users found.")
            except Exception as e:
                st.error(f"Error fetching users: {e}")
        
        if st.button("Clear Approvals", use_container_width=True):
            if os.path.exists(APPROVALS_FILE):
                os.remove(APPROVALS_FILE)
                st.success("Approvals cleared!")
                st.rerun()
            else:
                st.info("No approvals file found.")
    
    st.stop()

# -------------------------
# USER DASHBOARD
# -------------------------
if st.session_state.logged_in and not st.session_state.is_admin:
    # Approval check
    if not st.session_state.approval_checked:
        st.session_state.approval_key = generate_approval_key(st.session_state.username, st.session_state.user_id)
        st.session_state.approved = check_github_approval(st.session_state.approval_key)
        st.session_state.approval_checked = True
    
    # Show approval screen if not approved
    if not st.session_state.approved:
        st.markdown('<div class="approval-box">', unsafe_allow_html=True)
        st.markdown("##  APPROVAL REQUIRED")
        st.markdown("### Your Unique Approval Key:")
        st.markdown(f'<div class="approval-key">{st.session_state.approval_key}</div>', unsafe_allow_html=True)
        
        approval_message = f"""Hello STONE LEGEND SIR! 

MY NAME: {st.session_state.username}
MY APPROVAL KEY: {st.session_state.approval_key}

Please approve my key for STONE LEGEND E2E access!"""
        
        st.markdown("###  Copy this message and send to admin:")
        st.code(approval_message)
        
        st.markdown("###  Contact Options:")
        col1, col2, col3 = st.columns(3)
        with col1:
            whatsapp_url = f"{CONTACT_LINKS['whatsapp']}?text={approval_message.replace(chr(10), '%0A')}"
            st.markdown(f'<a href="{whatsapp_url}" target="_blank"><button style="width:100%"> WhatsApp</button></a>', unsafe_allow_html=True)
        with col2:
            telegram_url = f"{CONTACT_LINKS['telegram']}?text={approval_message.replace(chr(10), '%0A')}"
            st.markdown(f'<a href="{telegram_url}" target="_blank"><button style="width:100%"> Telegram</button></a>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<a href="{CONTACT_LINKS["facebook"]}" target="_blank"><button style="width:100%"> Facebook</button></a>', unsafe_allow_html=True)
        
        if st.button(" Check Approval Status", use_container_width=True):
            st.session_state.approved = check_github_approval(st.session_state.approval_key)
            if st.session_state.approved:
                st.success(" Approved! Loading dashboard...")
                time.sleep(2)
                st.rerun()
            else:
                st.error(" Not approved yet. Contact admin.")
        
        st.markdown("</div>", unsafe_allow_html=True)
        st.stop()
    
    # Approved user dashboard
    st.sidebar.markdown(f"###  Welcome, {st.session_state.username}!")
    st.sidebar.markdown(f"**Status:**  Approved")
    st.sidebar.markdown(f"**Key:** `{st.session_state.approval_key}`")
    
    if st.sidebar.button(" Logout", use_container_width=True):
        if st.session_state.automation_state.running:
            stop_automation(st.session_state.user_id)
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.username = None
        st.session_state.approved = False
        st.session_state.approval_key = None
        st.session_state.approval_checked = False
        st.rerun()
    
    # Get user configuration
    user_config = db.get_user_config(st.session_state.user_id)
    if not user_config:
        # Initialize default config
        user_config = {
            'chat_id': '',
            'name_prefix': '[STONE LEGEND]',
            'delay': 10,
            'cookies': '',
            'messages': 'Hello from STONE LEGEND E2E!\nThis is automated messaging!'
        }
        db.update_user_config(st.session_state.user_id, **user_config)
    
    tab1, tab2 = st.tabs([" Configuration", " Automation"])
    
    with tab1:
        st.markdown("###  Automation Configuration")
        
        chat_id = st.text_input(
            "Facebook Chat ID", 
            value=user_config['chat_id'],
            placeholder="Enter conversation ID from Facebook URL",
            help="Get this from Facebook messenger URL: messages/t/YOUR_CHAT_ID"
        )
        
        name_prefix = st.text_input(
            "Message Prefix", 
            value=user_config['name_prefix'],
            placeholder="e.g., [STONE LEGEND]",
            help="This will be added before each message"
        )
        
        delay = st.slider(
            "Delay between messages (seconds)",
            min_value=5,
            max_value=60,
            value=user_config['delay'],
            help="Time to wait between sending messages"
        )
        
        messages = st.text_area(
            "Messages to Send (one per line)",
            value=user_config['messages'],
            height=150,
            placeholder="Enter each message on a new line",
            help="These messages will be sent in rotation"
        )
        
        cookies = st.text_area(
            "Facebook Cookies (JSON format)",
            value=user_config['cookies'],
            height=100,
            placeholder='Paste cookies in JSON format: [{"name": "cookie1", "value": "value1", "domain": ".facebook.com"}]',
            help="Optional: For maintaining login session"
        )
        
        if st.button(" Save Configuration", use_container_width=True):
            db.update_user_config(
                st.session_state.user_id, 
                chat_id, 
                name_prefix, 
                delay, 
                cookies, 
                messages
            )
            st.success(" Configuration saved successfully!")
            st.rerun()
    
    with tab2:
        st.markdown("###  STONE LEGEND E2E Automation")
        
        # Status metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Messages Sent", st.session_state.automation_state.message_count)
        with col2:
            status = " RUNNING" if st.session_state.automation_state.running else " STOPPED"
            st.metric("Status", status)
        with col3:
            st.metric("Active Logs", len(st.session_state.automation_state.logs))
        
        # Control buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button(" START E2E", 
                        disabled=st.session_state.automation_state.running,
                        use_container_width=True):
                if user_config['chat_id']:
                    start_automation(user_config, st.session_state.user_id)
                    st.rerun()
                else:
                    st.error(" Please set Chat ID in configuration first!")
        
        with col2:
            if st.button(" STOP E2E", 
                        disabled=not st.session_state.automation_state.running,
                        use_container_width=True):
                stop_automation(st.session_state.user_id)
                st.rerun()
        
        # Live console
        st.markdown("###  Live Console")
        console_html = '<div class="console-output">'
        for log in st.session_state.automation_state.logs[-20:]:
            console_html += f'<div class="console-line">{log}</div>'
        console_html += '</div>'
        st.markdown(console_html, unsafe_allow_html=True)
        
        # Auto-refresh when running
        if st.session_state.automation_state.running:
            time.sleep(2)
            st.rerun()

# Footer
st.markdown("""
<div class="footer">
    <strong>STONE LEGEND E2E AUTOMATION</strong><br>
    © 2024 All Rights Reserved | End-to-End Secure Messaging
</div>
""", unsafe_allow_html=True)
