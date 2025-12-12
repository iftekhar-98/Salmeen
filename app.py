import streamlit as st
import pandas as pd
import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import time

# --- 1. إعدادات الصفحة والتصميم ---
st.set_page_config(
    page_title="سالمين | Salmeen",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
    <style>
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
        
        div.stButton > button {
            width: 100%; border-radius: 15px; height: 3em;
            background-color: var(--primary-green); color: white; border: none;
            font-weight: bold; font-size: 18px; transition: 0.3s;
        }
        div.stButton > button:hover { background-color: var(--secondary-orange); color: var(--primary-green); }
        
        .landing-card {
            background-color: white; border: 2px solid var(--primary-green);
            border-radius: 25px; padding: 30px; text-align: center; height: 260px;
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); transition: transform 0.3s ease;
        }
        .landing-card:hover { transform: translateY(-5px); border-color: var(--secondary-orange); }
        .card-icon { font-size: 70px; margin-bottom: 15px; color: var(--primary-green); }
        .card-title { font-size: 26px; font-weight: bold; color: var(--primary-green); }
        .card-desc { font-size: 15px; color: var(--text-taupe); margin-top: 10px; }

        .dashboard-card {
            background-color: white; border-radius: 20px; padding: 25px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05); border: 1px solid #eee;
            margin-bottom: 20px; height: 100%; transition: 0.3s; text-align: center; font-size: 22px;
        }
        .dashboard-card:hover { box-shadow: 0 8px 20px rgba(0,0,0,0.1); transform: translateY(-2px); }

        .card-header {
            font-size: 24px; font-weight: bold; margin-bottom: 15px; color: var(--primary-green);
            border-bottom: 2px solid #f0f0f0; padding-bottom: 10px; text-align: right !important; width: 100%; display: block;
        }

        .score-container {
            text-align: center; padding: 20px;
            background: linear-gradient(135deg, #f0fdf4 0%, #ffffff 100%);
            border-radius: 25px; border: 2px solid var(--primary-green); margin-bottom: 30px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        }
        .score-number { font-size: 80px; font-weight: 800; color: var(--primary-green); line-height: 1; }
        .score-label { color: var(--text-taupe); font-size: 18px; margin-top: 10px; }

        .control-panel {
            background-color: #F8F9FA; border-radius: 15px; padding: 20px;
            border: 1px dashed var(--primary-green); margin-bottom: 30px; text-align: right;
        }

        .metric-card {
            background: linear-gradient(to bottom left, #ffffff, #f0fdf4);
            border-right: 5px solid var(--primary-green); border-radius: 15px; padding: 20px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05); text-align: center; transition: 0.3s; margin-bottom: 15px;
        }
        .metric-card:hover { transform: translateY(-3px); box-shadow: 0 8px 15px rgba(0,0,0,0.1); }
        .metric-value { font-size: 36px; font-weight: 800; color: var(--primary-green); }
        .metric-label { font-size: 16px; color: var(--text-taupe); margin-bottom: 5px; }
        .metric-delta { font-size: 14px; font-weight: bold; background-color: #e8f5e9; padding: 2px 8px; border-radius: 10px; display: inline-block; }
        .positive { color: #2e7d32; background-color: #e8f5e9; }
        .negative { color: #c62828; background-color: #ffebee; }

        .alert-box {
            background-color: #fff; border: 1px solid #eee; border-radius: 10px; padding: 10px;
            margin-bottom: 10px; border-right: 4px solid var(--secondary-orange); font-size: 14px; text-align: right;
        }

        [data-testid="stSidebar"] { display: none; }
        
        /* City Score Ticker */
        .city-ticker {
            background-color: #e0f2f1; color: #124641; padding: 10px 20px; 
            border-radius: 50px; font-weight: bold; text-align: center;
            margin: 0 auto 20px auto; width: fit-content; border: 1px solid #124641;
        }
    </style>
""", unsafe_allow_html=True)

# --- 2. إدارة الحالة المشتركة (The Bridge) ---
# هنا نربط بين المواطن والوزارة
if 'user_status' not in st.session_state:
    st.session_state['user_status'] = {
        'score': 85,
        'risk_level': 0, # 0:Safe, 1:Medium, 2:High
        'last_updated': 'الآن'
    }

# --- 3. بناء وتدريب نموذج الذكاء الاصطناعي ---
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

# --- 4. دوال مساعدة ---
def get_risk_label(risk_code):
    if risk_code == 2: return "عالي الخطورة 🔴", "خفف السرعة فوراً!"
    if risk_code == 1: return "متوسط 🟠", "انتبه لمسافة الأمان."
    return "آمن 🟢", "استمر على هذا الأداء."

def simulate_action_plans(risk_code):
    if risk_code == 2:
        return [{"type": "تحذير عاجل", "text": "سرعتك تضعك في دائرة الخطر بنسبة 90%."}, {"type": "هدف أسبوعي", "text": "تجنب القيادة في المسار الأيسر."}]
    elif risk_code == 1:
        return [{"type": "نصيحة يومية", "text": "لاحظنا كثرة الفرملة."}, {"type": "هدف أسبوعي", "text": "حافظ على سرعة ثابتة."}]
    else:
        return [{"type": "مكافأة", "text": "أداؤك ممتاز! استمر."}, {"type": "نصيحة", "text": "حافظ على هذا المستوى لخصم التأمين."}]

# --- 5. منطق التنقل ---
if 'page' not in st.session_state: st.session_state['page'] = 'home'
def navigate_to(page): st.session_state['page'] = page; st.rerun()

# ==========================================
# الصفحة 1: الرئيسية (Landing Page)
# ==========================================
if st.session_state['page'] == 'home':
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if os.path.exists("assets/logosalmeen.png"):
            st.image("assets/logosalmeen.png", use_container_width=True)
        else:
            st.title("سالمين")
            
    # --- التعديل 1: ربط الشعار بالواقع ---
    city_score = 94 # Default
    # إذا كان المستخدم متهوراً، نخفض نقاط المدينة قليلاً "بسببك"
    if st.session_state['user_status']['risk_level'] == 2:
        city_score = 91 
        
    st.markdown(f"""
        <div class="city-ticker">
            🏙️ مؤشر سلامة الرياض اليوم: <span style="color: #FD9E19; font-size: 20px;">{city_score} نقطة</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h3 style='text-align: center; color: #8A827E;'>نقاطك اليوم.. سلامتك بكرة</h3>", unsafe_allow_html=True)
    st.write("")

    c1, c_space, c2 = st.columns([1, 0.1, 1])
    
    with c1:
        st.markdown("""
            <div class="landing-card">
                <div class="card-icon">👤</div>
                <div class="card-title">للأفراد</div>
                <div class="card-desc">تحكم في نقاطك، وحسن سلوكك لتحمي مدينتك</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("دخول المواطن", use_container_width=True):
            navigate_to('citizen')
            
    with c2:
        st.markdown("""
            <div class="landing-card">
                <div class="card-icon">🏛️</div>
                <div class="card-title">للجهات الحكومية</div>
                <div class="card-desc">راقب تأثير سلوك الأفراد على سلامة المدينة</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("دخول الوزارة", use_container_width=True):
            navigate_to('ministry')

# ==========================================
# الصفحة 2: الملف الشخصي (المصدر)
# ==========================================
elif st.session_state['page'] == 'citizen':
    
    c1, c2, c3 = st.columns([1, 4, 1])
    with c1:
        if st.button("🏠 الرئيسية", use_container_width=True): navigate_to('home')
    with c2:
        st.markdown(f"""<div style="text-align: center;"><h2 style="margin:0;">مرحباً، محمد عبدالله 👋</h2><p style="color: #8A827E; margin:0;">حالتك تؤثر الآن على مؤشر المدينة</p></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""<div style="text-align: left; background: #e0f2f1; padding: 5px 15px; border-radius: 20px; color: #124641; font-weight: bold; font-size: 14px; display: inline-block;">عضو مميز ⭐</div>""", unsafe_allow_html=True)

    st.write("") 

    st.markdown("##### 🎛️ محاكي الذكاء الاصطناعي (أنت الآن تقود..)")
    with st.container():
        st.markdown('<div class="control-panel">', unsafe_allow_html=True)
        col_input1, col_input2 = st.columns(2)
        with col_input1: user_speed = st.slider("معدل السرعة (كم/س)", 60, 160, 110)
        with col_input2: user_braking = st.slider("عدد مرات الفرملة المفاجئة", 0, 10, 2)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # AI Calculation
    user_input = [[user_speed, user_braking, 1]]
    prediction_code = model.predict(user_input)[0]
    risk_label, risk_advice = get_risk_label(prediction_code)
    current_score = int(max(0, min(100, 100 - (user_speed/2.2) - (user_braking * 3))))
    
    # --- التعديل 2: تحديث الحالة العامة (إرسال البيانات للوزارة) ---
    st.session_state['user_status'] = {
        'score': current_score,
        'risk_level': prediction_code,
        'speed': user_speed
    }
    
    score_color = "#124641" if current_score > 70 else "#FD9E19"
    if current_score < 50: score_color = "#D32F2F"

    st.markdown(f"""
        <div class="score-container" style="border-color: {score_color};">
            <div class="score-number" style="color: {score_color};">{current_score}</div>
            <div class="score-label">مؤشر التزامك الحالي (AI Predicted)</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<h3 style="text-align: right; color: #124641;">المدرب الذكي (تحليل شامل)</h3>', unsafe_allow_html=True)
    
    row1_1, row1_2, row1_3 = st.columns(3)
    
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

    with row1_2:
        risk_border = "#124641" if prediction_code == 0 else "#FD9E19"
        if prediction_code == 2: risk_border = "#D32F2F"
        st.markdown(f"""
            <div class="dashboard-card" style="border: 2px solid {risk_border};">
                <div class="card-header" style="color: {risk_border};">2. توقع المخاطر</div>
                <div style="font-size: 40px; text-align: center; margin-bottom: 10px;">🔮</div>
                <p style="text-align:center; font-weight:bold; font-size:28px; color: {risk_border};">{risk_label}</p>
                <hr style="margin: 10px 0;">
                <p style="font-size: 18px;"><strong>السبب المحتمل:</strong><br>{risk_advice}</p>
            </div>
        """, unsafe_allow_html=True)

    with row1_3:
        plans = simulate_action_plans(prediction_code)
        plans_html = ""
        for p in plans:
            plans_html += f"""
            <div style="background:#f9f9f9; padding:10px; border-radius:10px; margin-bottom:10px; border-right: 3px solid #124641; text-align: right;">
                <strong style="color:#124641; font-size: 18px;">{p['type']}</strong><br>
                <span style="font-size:16px; color:#555;">{p['text']}</span>
            </div>
            """ 
        st.markdown(f"""
            <div class="dashboard-card"><div class="card-header">3. الخطة المقترحة</div>{plans_html}</div>
        """, unsafe_allow_html=True)

# ==========================================
# الصفحة 3: لوحة الوزارة (المستقبل)
# ==========================================
elif st.session_state['page'] == 'ministry':
    
    c1, c2 = st.columns([1, 5])
    with c1:
        if st.button("🏠 الرئيسية", use_container_width=True): navigate_to('home')
    with c2:
        st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h2 style="margin:0;">لوحة القيادة الاستراتيجية | غرفة العمليات</h2>
                <span style="background: #e0f2f1; color: #124641; padding: 5px 15px; border-radius: 15px; font-weight: bold;">🔴 مباشر | Live</span>
            </div>
        """, unsafe_allow_html=True)
    
    st.write("")
    
    # --- التعديل 3: استقبال بيانات المواطن ---
    user_status = st.session_state['user_status']
    
    # إذا كان المواطن (أنت) متهوراً، يظهر تأثير ذلك هنا
    total_violations = 1243
    city_safety = 84
    
    if user_status['risk_level'] == 2:
        city_safety = 81 # انخفض المؤشر العام
        total_violations += 1 # زادت المخالفات
    
    st.markdown("### 📊 المؤشرات العامة للمدينة (Real-Time KPIs)")

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""<div class="metric-card"><div class="metric-label">إجمالي المخالفات (اليوم)</div><div class="metric-value">{total_violations}</div><div class="metric-delta {'negative' if user_status['risk_level']==2 else 'positive'}">{'↑ زيادة' if user_status['risk_level']==2 else '↓ تحسن'}</div></div>""", unsafe_allow_html=True)
        
    with k2:
        st.markdown(f"""<div class="metric-card" style="border-right-color: #FD9E19;"><div class="metric-label">مؤشر السلامة العام</div><div class="metric-value">{city_safety}%</div><div class="metric-delta {'negative' if user_status['risk_level']==2 else 'positive'}">{'↓ انخفاض' if user_status['risk_level']==2 else '↑ ارتفاع'}</div></div>""", unsafe_allow_html=True)

    with k3:
        st.markdown("""<div class="metric-card"><div class="metric-label">دقة تنبؤات AI</div><div class="metric-value">99.2%</div><div class="metric-delta positive">✔ نظام مستقر</div></div>""", unsafe_allow_html=True)

    with k4:
        # عدد المناطق الخطرة يزيد لو المواطن متهور
        risk_zones = 3 + (1 if user_status['risk_level'] == 2 else 0)
        st.markdown(f"""<div class="metric-card" style="border-right-color: #D32F2F;"><div class="metric-label">مناطق عالية الخطورة</div><div class="metric-value">{risk_zones}</div><div class="metric-delta negative">⚠ تتطلب تدخل</div></div>""", unsafe_allow_html=True)

    st.divider()

    col_main, col_side = st.columns([2, 1])

    with col_main:
        st.markdown("##### 🗺️ الخريطة الحرارية للمخاطر وتوزيع المناطق")
        map_data = pd.DataFrame(np.random.randn(200, 2) / [50, 50] + [24.7136, 46.6753], columns=['lat', 'lon'])
        st.map(map_data, zoom=10, use_container_width=True)
        
        st.markdown("##### 📈 تحليل المخالفات حسب الأحياء")
        chart_data = pd.DataFrame({'المخالفات': [120, 95, 80, 45, 30], 'الحي': ['الملقا', 'النرجس', 'الياسمين', 'العليا', 'النخيل']}).set_index('الحي')
        st.bar_chart(chart_data, color="#124641")

    with col_side:
        st.markdown("##### 🚨 سجل التنبيهات الحية (Live Feed)")
        
        # --- التعديل 4: إضافة تنبيه المواطن الحالي ---
        alerts = []
        
        # إذا كان المواطن في وضع خطر، يظهر أول تنبيه
        if user_status['risk_level'] == 2:
            alerts.append({"time": "الآن", "msg": f"⚠️ تم رصد سائق متهور (سرعة {user_status['speed']} كم) - المستخدم الحالي", "type": "danger"})
        elif user_status['risk_level'] == 1:
            alerts.append({"time": "الآن", "msg": "تنبيه سلوك متوسط الخطورة - المستخدم الحالي", "type": "warning"})
            
        # تنبيهات افتراضية
        alerts += [
            {"time": "منذ 2 د", "msg": "تنبؤ بازدحام شديد في طريق الملك فهد", "type": "warning"},
            {"time": "منذ 12 د", "msg": "تم تحسين انسيابية الحركة في المطار", "type": "success"},
            {"time": "منذ 35 د", "msg": "حادث محتمل تم تجنبه (AI Alert)", "type": "success"},
        ]
        
        for alert in alerts:
            border_c = "#FD9E19"
            if alert['type'] == 'danger': border_c = "#D32F2F"
            if alert['type'] == 'success': border_c = "#124641"
            st.markdown(f"""
                <div class="alert-box" style="border-right-color: {border_c};">
                    <strong style="color: {border_c};">{alert['time']}</strong><br>
                    {alert['msg']}
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("##### 📉 توزيع مستويات الخطر")
        dist_data = pd.DataFrame({'النسبة': [70, 20, 10]}, index=['آمن', 'متوسط', 'خطر'])
        st.bar_chart(dist_data, horizontal=True, color=["#124641"])
