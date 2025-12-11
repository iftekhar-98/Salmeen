import streamlit as st
import pandas as pd
import numpy as np
import os

# --- 1. CONFIGURATION & STYLING ---
st.set_page_config(
    page_title="سالمين | Salmeen",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"  # Hide sidebar
)

# Custom CSS for Colors, RTL, and Card Design
st.markdown("""
    <style>
        /* Import Google Font for Arabic */
        @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Tajawal', sans-serif;
            direction: rtl;
            text-align: right;
        }
        
        /* Color Palette */
        :root {
            --primary-green: #124641;
            --secondary-orange: #FD9E19;
            --text-taupe: #8A827E;
            --bg-white: #FFFFFF;
        }
        
        /* Primary Headers */
        h1, h2, h3 {
            color: #124641 !important;
        }
        
        /* Orange Highlights */
        .highlight {
            color: #FD9E19;
            font-weight: bold;
        }
        
        /* Card Design */
        div.stButton > button {
            width: 100%;
            border-radius: 15px;
            height: 3em;
            background-color: #124641;
            color: white;
            border: none;
            font-weight: bold;
            font-size: 18px;
            transition: 0.3s;
        }
        div.stButton > button:hover {
            background-color: #FD9E19;
            color: #124641;
        }
        
        /* Custom Cards for AI Layers */
        .ai-card {
            background-color: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 20px;
            border-right: 5px solid #124641;
        }
        .ai-card-orange {
            border-right: 5px solid #FD9E19;
        }
        
        /* Remove Sidebar completely */
        [data-testid="stSidebar"] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

# --- 2. DATA GENERATION (MOCK) ---
# Generate dummy data if not exists
if 'data' not in st.session_state:
    data = pd.DataFrame({
        'date': pd.date_range(start='2025-01-01', periods=30),
        'score': np.random.randint(70, 100, 30),
        'risk_level': np.random.choice(['منخفض', 'متوسط', 'عالي'], 30)
    })
    st.session_state['data'] = data

# --- 3. HELPER FUNCTIONS (AI SIMULATION) ---
def simulate_behavioral_ai():
    return {
        "style": "متوازن",
        "strengths": ["الالتزام بالمسار", "تجديد الوثائق مبكراً"],
        "weaknesses": ["السرعة في أوقات الذروة"]
    }

def simulate_predictive_safety():
    return {
        "risk_prob": 45,
        "next_risk_hour": "17:00",
        "reason": "ازدحام متوقع على طريق الملك فهد"
    }

def simulate_action_plans():
    return [
        {"type": "نصيحة يومية", "text": "تجنب طريق الملك فهد اليوم الساعة 5 مساءً واستخدم طريق الخدمة."},
        {"type": "هدف أسبوعي", "text": "حاول تقليل الفرملة المفاجئة بنسبة 10% لرفع نقاطك."},
        {"type": "تنبيه استباقي", "text": "توقعات بأمطار غداً، ننصحك بالخروج قبل موعدك بـ 15 دقيقة."}
    ]

# --- 4. PAGE LOGIC ---

# Initialize Session State for Navigation
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'

def navigate_to(page):
    st.session_state['page'] = page
    st.rerun()

# --- PAGE: LANDING PAGE ---
if st.session_state['page'] == 'home':
    # Display Logo
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Check if logo exists
        if os.path.exists("assets/logosalmeen.png"):
            st.image("assets/logosalmeen.png", use_container_width=True)
        else:
            st.title("سالمين") # Fallback text
    
    st.markdown("<h3 style='text-align: center;'>نقاطك اليوم.. سلامتك بكرة</h3>", unsafe_allow_html=True)
    st.write("")
    st.write("")
    
    # Navigation Buttons (Cards)
    c1, c2 = st.columns(2)
    with c1:
        st.info("للأفراد")
        if st.button("الملف الشخصي للمواطن"):
            navigate_to('citizen')
            
    with c2:
        st.warning("للجهات الحكومية")
        if st.button("لوحة التحكم الوزارية"):
            navigate_to('ministry')

# --- PAGE: CITIZEN PROFILE ---
elif st.session_state['page'] == 'citizen':
    # Header with Back Button
    c1, c2 = st.columns([1, 5])
    with c1:
        if st.button("🏠 الرئيسية"):
            navigate_to('home')
    with c2:
        st.header("الملف الشخصي | محمد عبدالله")

    # Hero Section: Score
    score = st.session_state['data']['score'].iloc[-1]
    st.markdown(f"""
        <div style="text-align: center; padding: 20px; background-color: #f0f2f6; border-radius: 10px;">
            <h1 style="font-size: 60px; color: #124641; margin: 0;">{score}</h1>
            <p style="color: #8A827E;">مؤشر الالتزام الحالي</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # --- SMART COACH SECTION (3 LAYERS) ---
    st.subheader("المدرب الذكي (Smart Coach)")
    
    # Layer 1: Behavioral
    beh_data = simulate_behavioral_ai()
    st.markdown(f"""
        <div class="ai-card">
            <h3 style="color: #124641;">1. الذكاء السلوكي (Behavioral AI)</h3>
            <p><strong>نمط القيادة:</strong> {beh_data['style']}</p>
            <p><strong>نقاط القوة:</strong> {', '.join(beh_data['strengths'])}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Layer 2: Predictive
    pred_data = simulate_predictive_safety()
    st.markdown(f"""
        <div class="ai-card ai-card-orange">
            <h3 style="color: #FD9E19;">2. توقع المخاطر (Predictive Safety)</h3>
            <p>احتمالية الخطر خلال 24 ساعة: <strong>{pred_data['risk_prob']}%</strong></p>
            <p>السبب الرئيسي: {pred_data['reason']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Layer 3: Action Plan
    plans = simulate_action_plans()
    st.markdown("""<div class="ai-card"><h3 style="color: #124641;">3. الخطة الذكية (Action Plan)</h3>""", unsafe_allow_html=True)
    cols = st.columns(3)
    for i, plan in enumerate(plans):
        with cols[i]:
            st.info(f"**{plan['type']}**\n\n{plan['text']}")
    st.markdown("</div>", unsafe_allow_html=True)

# --- PAGE: MINISTRY DASHBOARD ---
elif st.session_state['page'] == 'ministry':
    # Header with Back Button
    c1, c2 = st.columns([1, 5])
    with c1:
        if st.button("🏠 الرئيسية"):
            navigate_to('home')
    with c2:
        st.header("لوحة التحكم الاستراتيجية | وزارة الداخلية")
        
    # KPIs
    k1, k2, k3 = st.columns(3)
    k1.metric("إجمالي المخالفات (اليوم)", "1,240", "-5%")
    k2.metric("متوسط مؤشر السلامة", "78/100", "+2%")
    k3.metric("الأحياء عالية الخطورة", "3 أحياء", "حي الملقا")
    
    st.subheader("الخريطة الحرارية للمخاطر (Heatmap)")
    # Generate Map Data (Riyadh)
    map_data = pd.DataFrame(
        np.random.randn(100, 2) / [50, 50] + [24.7136, 46.6753],
        columns=['lat', 'lon']
    )
    st.map(map_data)
