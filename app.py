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
        
        /* Buttons Style */
        div.stButton > button {
            width: 100%; border-radius: 15px; height: 3em;
            background-color: #124641; color: white; border: none;
            font-weight: bold; font-size: 18px; transition: 0.3s;
        }
        div.stButton > button:hover { background-color: #FD9E19; color: #124641; }
        
        /* Landing Page Cards */
        .landing-card {
            background-color: white;
            border: 2px solid #124641;
            border-radius: 25px;
            padding: 40px;
            text-align: center;
            height: 280px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            margin-bottom: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        .landing-card:hover {
            transform: translateY(-5px);
            border-color: #FD9E19;
        }
        .card-icon { font-size: 80px; margin-bottom: 20px; color: #124641; }
        .card-title { font-size: 28px; font-weight: bold; color: #124641; }
        .card-desc { font-size: 16px; color: #8A827E; margin-top: 10px; }

        /* AI Cards */
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
    np.random.seed(42)
    n_samples = 1000
    speed = np.random.normal(90, 20, n_samples)
    braking = np.random.randint(0, 10, n_samples)
    peak_hour = np.random.randint(0, 2, n_samples)
    
    X = pd.DataFrame({'speed': speed, 'braking': braking, 'peak_hour': peak_hour})
    y = []
    for i in range(n_samples):
        risk = 0 
        if speed[i] > 120 or braking[i] > 5: risk = 2
        elif speed[i] > 100 or braking[i] > 3: risk = 1
        y.append(risk)
        
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    model = RandomForestClassifier(n_estimators=50)
    model.fit(X_train, y_train)
    acc = accuracy_score(y_test, model.predict(X_test))
    return model, acc

model, accuracy = train_model()

# --- 3. HELPER FUNCTIONS ---
def get_risk_label(risk_code):
    if risk_code == 2: return "عالي الخطورة 🔴", "خفف السرعة فوراً!"
    if risk_code == 1: return "متوسط 🟠", "انتبه لمسافة الأمان."
    return "آمن 🟢", "استمر على هذا الأداء."

def simulate_action_plans(risk_code):
    if risk_code == 2:
        return [{"type": "تحذير عاجل", "text": "سرعتك الحالية تضعك في دائرة الخطر بنسبة 90%."}, {"type": "هدف أسبوعي", "text": "تجنب القيادة في المسار الأيسر."}]
    elif risk_code == 1:
        return [{"type": "نصيحة يومية", "text": "لاحظنا كثرة الفرملة."}, {"type": "هدف أسبوعي", "text": "حافظ على سرعة ثابتة."}]
    else:
        return [{"type": "مكافأة", "text": "أداؤك ممتاز!"}, {"type": "نصيحة", "text": "حافظ على هذا المستوى."}]

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
            
    st.markdown("<h3 style='text-align: center; color: #8A827E;'>نقاطك اليوم.. سلامتك بكرة</h3>", unsafe_allow_html=True)
    st.write("")
    st.write("")

    c1, c_space, c2 = st.columns([1, 0.2, 1])
    
    with c1:
        st.markdown("""
            <div class="landing-card">
                <div class="card-icon">👤</div>
                <div class="card-title">للأفراد</div>
                <div class="card-desc">ملفك الشخصي، مؤشر التزامك، وخطط التحسين</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("دخول المواطن", use_container_width=True):
            navigate_to('citizen')
            
    with c2:
        st.markdown("""
            <div class="landing-card">
                <div class="card-icon">🏛️</div>
                <div class="card-title">للجهات الحكومية</div>
                <div class="card-desc">لوحة التحكم، الخرائط الحرارية، والتحليلات</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("دخول الوزارة", use_container_width=True):
            navigate_to('ministry')

# --- PAGE: CITIZEN PROFILE ---
elif st.session_state['page'] == 'citizen':
    c1, c2 = st.columns([1, 5])
    with c1:
        if st.button("🏠 الرئيسية"): navigate_to('home')
    with c2:
        st.header("الملف الشخصي")
        st.caption(f"تم تدريب نموذج الذكاء الاصطناعي بنجاح (الدقة: {accuracy*100:.1f}%)")

    st.markdown("### 🎛️ جرب الذكاء الاصطناعي بنفسك!")
    col_input1, col_input2 = st.columns(2)
    with col_input1: user_speed = st.slider("متوسط السرعة (كم/س)", 60, 160, 110)
    with col_input2: user_braking = st.slider("عدد مرات الفرملة المفاجئة", 0, 10, 2)
    
    user_input = [[user_speed, user_braking, 1]]
    prediction_code = model.predict(user_input)[0]
    risk_label, risk_advice = get_risk_label(prediction_code)
    
    current_score = int(max(0, min(100, 100 - (user_speed/2) - (user_braking * 2))))

    st.markdown(f"""
        <div style="text-align: center; padding: 20px; background-color: #f0f2f6; border-radius: 10px; margin-top: 20px;">
            <h1 style="font-size: 60px; color: #124641; margin: 0;">{current_score}</h1>
            <p style="color: #8A827E;">مؤشر الالتزام (AI Predicted)</p>
        </div>
    """, unsafe_allow_html=True)
    st.divider()
    
    st.subheader("المدرب الذكي (Smart Coach)")
    border_color = "#FD9E19" if prediction_code > 0 else "#124641"
    st.markdown(f"""
        <div class="ai-card" style="border-right: 5px solid {border_color};">
            <h3 style="color: {border_color};">2. توقع المخاطر (AI Prediction)</h3>
            <p>تصنيف النموذج لحالتك: <strong>{risk_label}</strong></p>
            <p>السبب المحتمل: {risk_advice}</p>
        </div>
    """, unsafe_allow_html=True)
    
    plans = simulate_action_plans(prediction_code)
    cols = st.columns(len(plans))
    for i, plan in enumerate(plans):
        with cols[i]: st.info(f"**{plan['type']}**\n\n{plan['text']}")

# --- PAGE: MINISTRY DASHBOARD ---
elif st.session_state['page'] == 'ministry':
    if st.button("🏠 الرئيسية"): navigate_to('home')
    st.header("لوحة التحكم الاستراتيجية")
    k1, k2, k3 = st.columns(3)
    k1.metric("دقة نموذج AI", f"{accuracy*100:.1f}%")
    k2.metric("متوسط السرعة", "94 كم/س")
    k3.metric("تنبؤات الحوادث", "143")
    st.map(pd.DataFrame(np.random.randn(100, 2) / [50, 50] + [24.7136, 46.6753], columns=['lat', 'lon']))
