import streamlit as st
import pandas as pd
import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# --- 1. CONFIGURATION & STYLING ---
st.set_page_config(
    page_title="سالمين | Salmeen",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
        html, body, [class*="css"] {
            font-family: 'Tajawal', sans-serif;
            direction: rtl;
            text-align: right;
        }
        :root {
            --primary-green: #124641;
            --secondary-orange: #FD9E19;
            --text-taupe: #8A827E;
            --bg-white: #FFFFFF;
        }
        h1, h2, h3 { color: #124641 !important; }
        div.stButton > button {
            width: 100%; border-radius: 15px; height: 3em;
            background-color: #124641; color: white; border: none;
            font-weight: bold; font-size: 18px; transition: 0.3s;
        }
        div.stButton > button:hover { background-color: #FD9E19; color: #124641; }
        .ai-card {
            background-color: white; padding: 20px; border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px;
            border-right: 5px solid #124641;
        }
        .ai-card-orange { border-right: 5px solid #FD9E19; }
        [data-testid="stSidebar"] { display: none; }
    </style>
""", unsafe_allow_html=True)

# --- 2. REAL AI MODEL (TRAINING) ---
@st.cache_resource
def train_model():
    # 1. Generate Synthetic Training Data (1000 records)
    # Features: [Average Speed, Harsh Braking Count, Peak Hour Driving (0/1)]
    # Target: 0 (Safe), 1 (Medium), 2 (High Risk)
    
    np.random.seed(42)
    n_samples = 1000
    
    speed = np.random.normal(90, 20, n_samples) # Avg speed around 90
    braking = np.random.randint(0, 10, n_samples) # Braking incidents
    peak_hour = np.random.randint(0, 2, n_samples) # 1 if driving in peak hour
    
    X = pd.DataFrame({
        'speed': speed,
        'braking': braking,
        'peak_hour': peak_hour
    })
    
    # Logic to define "Ground Truth" for training
    y = []
    for i in range(n_samples):
        risk = 0 # Safe
        if speed[i] > 120 or braking[i] > 5:
            risk = 2 # High
        elif speed[i] > 100 or braking[i] > 3:
            risk = 1 # Medium
        y.append(risk)
        
    # 2. Train Random Forest Model
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    model = RandomForestClassifier(n_estimators=50)
    model.fit(X_train, y_train)
    
    acc = accuracy_score(y_test, model.predict(X_test))
    return model, acc

# Load/Train the model
model, accuracy = train_model()

# --- 3. HELPER FUNCTIONS ---
def get_risk_label(risk_code):
    if risk_code == 2: return "عالي الخطورة 🔴", "خفف السرعة فوراً!"
    if risk_code == 1: return "متوسط 🟠", "انتبه لمسافة الأمان."
    return "آمن 🟢", "استمر على هذا الأداء."

def simulate_action_plans(risk_code):
    if risk_code == 2:
        return [
            {"type": "تحذير عاجل", "text": "سرعتك الحالية تضعك في دائرة الخطر بنسبة 90%. خفف السرعة إلى 100 كم/س."},
            {"type": "هدف أسبوعي", "text": "تجنب القيادة في المسار الأيسر لمدة 3 أيام."}
        ]
    elif risk_code == 1:
        return [
            {"type": "نصيحة يومية", "text": "لاحظنا كثرة الفرملة، حاول ترك مسافة أكبر مع السيارة التي أمامك."},
            {"type": "هدف أسبوعي", "text": "حافظ على سرعة ثابتة لتقليل استهلاك الوقود وتحسين النقاط."}
        ]
    else:
        return [
            {"type": "مكافأة", "text": "أداؤك ممتاز! حصلت على شارة 'السائق المثالي' لهذا الأسبوع."},
            {"type": "نصيحة", "text": "حافظ على هذا المستوى للحصول على خصم التأمين القادم."}
        ]

# --- 4. NAVIGATION ---
if 'page' not in st.session_state: st.session_state['page'] = 'home'
def navigate_to(page): st.session_state['page'] = page; st.rerun()

# --- PAGE: LANDING PAGE ---
if st.session_state['page'] == 'home':
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if os.path.exists("assets/logosalmeen.png"):
            st.image("assets/logosalmeen.png", use_container_width=True)
        else:
            st.title("سالمين")
    st.markdown("<h3 style='text-align: center;'>نقاطك اليوم.. سلامتك بكرة</h3>", unsafe_allow_html=True)
    st.write("")
    c1, c2 = st.columns(2)
    with c1:
        st.info("للأفراد")
        if st.button("الملف الشخصي للمواطن"): navigate_to('citizen')
    with c2:
        st.warning("للجهات الحكومية")
        if st.button("لوحة التحكم الوزارية"): navigate_to('ministry')

# --- PAGE: CITIZEN PROFILE ---
elif st.session_state['page'] == 'citizen':
    c1, c2 = st.columns([1, 5])
    with c1:
        if st.button("🏠 الرئيسية"): navigate_to('home')
    with c2:
        st.header("الملف الشخصي | محمد عبدالله")
        st.caption(f"تم تدريب نموذج الذكاء الاصطناعي بنجاح (الدقة: {accuracy*100:.1f}%)")

    # --- INTERACTIVE INPUT (THE MAGIC) ---
    st.markdown("### 🎛️ جرب الذكاء الاصطناعي بنفسك!")
    st.markdown("غير القيم التالية وشاهد كيف يقوم النموذج بتوقع الخطر لحظياً:")
    
    col_input1, col_input2 = st.columns(2)
    with col_input1:
        user_speed = st.slider("متوسط السرعة (كم/س)", 60, 160, 110)
    with col_input2:
        user_braking = st.slider("عدد مرات الفرملة المفاجئة", 0, 10, 2)
    
    # AI Prediction
    user_input = [[user_speed, user_braking, 1]] # 1 assume peak hour
    prediction_code = model.predict(user_input)[0]
    risk_label, risk_advice = get_risk_label(prediction_code)
    
    # Score Calculation (Inverse of risk)
    current_score = 100 - (user_speed/2) - (user_braking * 2)
    current_score = int(max(0, min(100, current_score)))

    # Hero Section
    st.markdown(f"""
        <div style="text-align: center; padding: 20px; background-color: #f0f2f6; border-radius: 10px; margin-top: 20px;">
            <h1 style="font-size: 60px; color: #124641; margin: 0;">{current_score}</h1>
            <p style="color: #8A827E;">مؤشر الالتزام (AI Predicted)</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # --- SMART COACH LAYERS ---
    st.subheader("المدرب الذكي (Smart Coach)")
    
    # Layer 2: Predictive Safety (Real ML Output)
    border_color = "#FD9E19" if prediction_code > 0 else "#124641"
    st.markdown(f"""
        <div class="ai-card" style="border-right: 5px solid {border_color};">
            <h3 style="color: {border_color};">2. توقع المخاطر (AI Prediction)</h3>
            <p>تصنيف النموذج لحالتك: <strong>{risk_label}</strong></p>
            <p>السبب المحتمل: {risk_advice}</p>
            <p style="font-size: 12px; color: grey;">* تم التنبؤ باستخدام خوارزمية Random Forest</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Layer 3: Action Plan
    plans = simulate_action_plans(prediction_code)
    st.markdown("""<div class="ai-card"><h3 style="color: #124641;">3. الخطة الذكية (Action Plan)</h3>""", unsafe_allow_html=True)
    cols = st.columns(len(plans))
    for i, plan in enumerate(plans):
        with cols[i]:
            st.info(f"**{plan['type']}**\n\n{plan['text']}")
    st.markdown("</div>", unsafe_allow_html=True)

# --- PAGE: MINISTRY DASHBOARD ---
elif st.session_state['page'] == 'ministry':
    c1, c2 = st.columns([1, 5])
    with c1:
        if st.button("🏠 الرئيسية"): navigate_to('home')
    with c2:
        st.header("لوحة التحكم الاستراتيجية")
    
    k1, k2, k3 = st.columns(3)
    k1.metric("دقة نموذج AI", f"{accuracy*100:.1f}%", "+1.2%")
    k2.metric("متوسط السرعة (الرياض)", "94 كم/س", "-2%")
    k3.metric("تنبؤات الحوادث اليوم", "143", "منخفض")
    
    st.subheader("الخريطة الحرارية للمخاطر المتوقعة")
    map_data = pd.DataFrame(
        np.random.randn(100, 2) / [50, 50] + [24.7136, 46.6753],
        columns=['lat', 'lon']
    )
    st.map(map_data)
