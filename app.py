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

# Custom CSS (Global Styles + Dashboard Design)
st.markdown("""
    <style>
        /* Import Arabic Font */
        @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;800&display=swap');
        
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
            --danger-red: #D32F2F;
        }
        
        h1, h2, h3, h4, h5 { color: var(--primary-green) !important; }
        
        /* Buttons Style */
        div.stButton > button {
            width: 100%; border-radius: 15px; height: 3em;
            background-color: var(--primary-green); color: white; border: none;
            font-weight: bold; font-size: 18px; transition: 0.3s;
        }
        div.stButton > button:hover { background-color: var(--secondary-orange); color: var(--primary-green); }
        
        /* --- Landing Page Cards --- */
        .landing-card {
            background-color: white;
            border: 2px solid var(--primary-green);
            border-radius: 25px;
            padding: 30px;
            text-align: center;
            height: 260px;
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
            border-color: var(--secondary-orange);
        }
        .card-icon { font-size: 70px; margin-bottom: 15px; color: var(--primary-green); }
        .card-title { font-size: 26px; font-weight: bold; color: var(--primary-green); }
        .card-desc { font-size: 15px; color: var(--text-taupe); margin-top: 10px; }

        /* --- Dashboard/Profile Cards --- */
        .dashboard-card {
            background-color: white;
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            border: 1px solid #eee;
            margin-bottom: 20px;
            height: 100%; /* For full height in columns */
            transition: 0.3s;
        }
        .dashboard-card:hover {
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
            transform: translateY(-2px);
        }

        .card-header {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 15px;
            color: var(--primary-green);
            border-bottom: 2px solid #f0f0f0;
            padding-bottom: 10px;
        }

        /* --- Score Circle --- */
        .score-container {
            text-align: center;
            padding: 20px;
            background: linear-gradient(135deg, #f0fdf4 0%, #ffffff 100%);
            border-radius: 25px;
            border: 2px solid var(--primary-green);
            margin-bottom: 30px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        }
        .score-number {
            font-size: 80px;
            font-weight: 800;
            color: var(--primary-green);
            line-height: 1;
        }
        .score-label {
            color: var(--text-taupe);
            font-size: 18px;
            margin-top: 10px;
        }

        /* --- Control Panel (Simulator) --- */
        .control-panel {
            background-color: #F8F9FA;
            border-radius: 15px;
            padding: 20px;
            border: 1px dashed var(--primary-green);
            margin-bottom: 30px;
        }

        /* Remove Sidebar */
        [data-testid="stSidebar"] { display: none; }
    </style>
""", unsafe_allow_html=True)

# --- 2. REAL AI MODEL (TRAINING) ---
@st.cache_resource
def train_model():
    # Generate Synthetic Training Data (1000 records)
    np.random.seed(42)
    n_samples = 1000
    
    speed = np.random.normal(90, 20, n_samples)
    braking = np.random.randint(0, 10, n_samples)
    peak_hour = np.random.randint(0, 2, n_samples)
    
    X = pd.DataFrame({'speed': speed, 'braking': braking, 'peak_hour': peak_hour})
    y = []
    for i in range(n_samples):
        risk = 0 # Safe
        if speed[i] > 120 or braking[i] > 5: risk = 2 # High
        elif speed[i] > 100 or braking[i] > 3: risk = 1 # Medium
        y.append(risk)
        
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    model = RandomForestClassifier(n_estimators=50)
    model.fit(X_train, y_train)
    
    acc = accuracy_score(y_test, model.predict(X_test))
    return model, acc

# Load Model
model, accuracy = train_model()

# --- 3. HELPER FUNCTIONS ---
def get_risk_label(risk_code):
    if risk_code == 2: return "عالي الخطورة 🔴", "خفف السرعة فوراً!"
    if risk_code == 1: return "متوسط 🟠", "انتبه لمسافة الأمان."
    return "آمن 🟢", "استمر على هذا الأداء."

def simulate_action_plans(risk_code):
    if risk_code == 2:
        return [
            {"type": "تحذير عاجل", "text": "سرعتك تضعك في دائرة الخطر بنسبة 90%."},
            {"type": "هدف أسبوعي", "text": "تجنب القيادة في المسار الأيسر."}
        ]
    elif risk_code == 1:
        return [
            {"type": "نصيحة يومية", "text": "لاحظنا كثرة الفرملة."},
            {"type": "هدف أسبوعي", "text": "حافظ على سرعة ثابتة."}
        ]
    else:
        return [
            {"type": "مكافأة", "text": "أداؤك ممتاز! استمر."},
            {"type": "نصيحة", "text": "حافظ على هذا المستوى لخصم التأمين."}
        ]

# --- 4. NAVIGATION LOGIC ---
if 'page' not in st.session_state: st.session_state['page'] = 'home'
def navigate_to(page): st.session_state['page'] = page; st.rerun()

# ==========================================
# PAGE 1: LANDING PAGE (HOME)
# ==========================================
if st.session_state['page'] == 'home':
    # Logo Area
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if os.path.exists("assets/logosalmeen.png"):
            st.image("assets/logosalmeen.png", use_container_width=True)
        else:
            st.title("سالمين")
            
    st.markdown("<h3 style='text-align: center; color: #8A827E;'>نقاطك اليوم.. سلامتك بكرة</h3>", unsafe_allow_html=True)
    st.write("")
    st.write("")

    # Cards Area
    c1, c_space, c2 = st.columns([1, 0.1, 1])
    
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

# ==========================================
# PAGE 2: CITIZEN PROFILE (THE DASHBOARD)
# ==========================================
elif st.session_state['page'] == 'citizen':
    
    # Header Area
    c1, c2, c3 = st.columns([1, 4, 1])
    with c1:
        if st.button("🏠 الرئيسية", use_container_width=True):
            navigate_to('home')
    with c2:
        st.markdown(f"""
            <div style="text-align: center;">
                <h2 style="margin:0; padding:0;">مرحباً، محمد عبدالله 👋</h2>
                <p style="color: #8A827E; margin:0;">آخر تحديث: الآن (AI Active)</p>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
            <div style="text-align: left; background: #e0f2f1; padding: 5px 15px; border-radius: 20px; color: #124641; font-weight: bold; font-size: 14px; display: inline-block;">
                عضو مميز ⭐
            </div>
        """, unsafe_allow_html=True)

    st.write("") 

    # Control Panel (Simulator)
    st.markdown("##### 🎛️ محاكي الذكاء الاصطناعي (تحكم في بياناتك)")
    with st.container():
        st.markdown('<div class="control-panel">', unsafe_allow_html=True)
        col_input1, col_input2 = st.columns(2)
        with col_input1:
            user_speed = st.slider("معدل السرعة (كم/س)", 60, 160, 110)
        with col_input2:
            user_braking = st.slider("عدد مرات الفرملة المفاجئة", 0, 10, 2)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # AI Processing
    user_input = [[user_speed, user_braking, 1]]
    prediction_code = model.predict(user_input)[0]
    risk_label, risk_advice = get_risk_label(prediction_code)
    
    # Calculate Score
    current_score = int(max(0, min(100, 100 - (user_speed/2.2) - (user_braking * 3))))
    
    # Dynamic Colors
    score_color = "#124641" if current_score > 70 else "#FD9E19"
    if current_score < 50: score_color = "#D32F2F"

    # Big Score Circle
    st.markdown(f"""
        <div class="score-container" style="border-color: {score_color};">
            <div class="score-number" style="color: {score_color};">{current_score}</div>
            <div class="score-label">مؤشر التزامك الحالي (AI Predicted)</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Smart Coach Columns
    st.subheader("المدرب الذكي (تحليل شامل)")
    row1_1, row1_2, row1_3 = st.columns(3)
    
    # Card 1: Behavioral
    with row1_1:
        st.markdown(f"""
            <div class="dashboard-card">
                <div class="card-header">1. التحليل السلوكي</div>
                <div style="font-size: 40px; text-align: center; margin-bottom: 10px;">📊</div>
                <p><strong>نمط القيادة:</strong> {( "متزن" if current_score > 75 else "متهور" )}</p>
                <p><strong>نقاط القوة:</strong> <br><span style="color:#124641;">• الالتزام بالمسار</span></p>
                <p><strong>نقاط التحسن:</strong> <br><span style="color:#FD9E19;">• {("السرعة الزائدة" if user_speed > 100 else "الفرملة المتكررة")}</span></p>
            </div>
        """, unsafe_allow_html=True)

    # Card 2: Predictive
    with row1_2:
        risk_border = "#124641" if prediction_code == 0 else "#FD9E19"
        if prediction_code == 2: risk_border = "#D32F2F"
        
        st.markdown(f"""
            <div class="dashboard-card" style="border: 2px solid {risk_border};">
                <div class="card-header" style="color: {risk_border};">2. توقع المخاطر</div>
                <div style="font-size: 40px; text-align: center; margin-bottom: 10px;">🔮</div>
                <p style="text-align:center; font-weight:bold; font-size:18px; color: {risk_border};">
                    {risk_label}
                </p>
                <hr style="margin: 10px 0;">
                <p style="font-size: 14px;"><strong>السبب المحتمل:</strong><br>{risk_advice}</p>
            </div>
        """, unsafe_allow_html=True)

    # Card 3: Action Plan
    with row1_3:
        plans = simulate_action_plans(prediction_code)
        plans_html = ""
        for p in plans:
            plans_html += f"""
            <div style="background:#f9f9f9; padding:10px; border-radius:10px; margin-bottom:10px; border-right: 3px solid #124641;">
                <strong style="color:#124641;">{p['type']}</strong><br>
                <span style="font-size:13px; color:#555;">{p['text']}</span>
            </div>
            """ 
        st.markdown(f"""
            <div class="dashboard-card">
                <div class="card-header">3. الخطة المقترحة</div>
                {plans_html}
            </div>
        """, unsafe_allow_html=True)

# ==========================================
# PAGE 3: MINISTRY DASHBOARD
# ==========================================
elif st.session_state['page'] == 'ministry':
    if st.button("🏠 الرئيسية"): navigate_to('home')
    st.header("لوحة التحكم الاستراتيجية")
    
    k1, k2, k3 = st.columns(3)
    k1.metric("دقة نموذج AI", f"{accuracy*100:.1f}%")
    k2.metric("متوسط السرعة", "94 كم/س")
    k3.metric("تنبؤات الحوادث", "143")
    
    st.subheader("الخريطة الحرارية للمخاطر المتوقعة")
    # Generate random points around Riyadh
    map_data = pd.DataFrame(
        np.random.randn(100, 2) / [50, 50] + [24.7136, 46.6753],
        columns=['lat', 'lon']
    )
    st.map(map_data)
