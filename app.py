"""
Salmeen - Saudi Smart Traffic Safety Platform
Streamlit MVP Application
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pydeck as pdk

from utils import generate_dummy_data
from model import SafetyScoreCalculator, RiskPredictor, AICoach


# Page configuration
st.set_page_config(
    page_title="سلمين - منصة السلامة المرورية",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for RTL and Arabic styling
st.markdown("""
<style>
    /* RTL Support */
    .main .block-container {
        direction: rtl;
        text-align: right;
    }
    
    /* Sidebar RTL */
    [data-testid="stSidebar"] {
        direction: rtl;
        text-align: right;
    }
    
    [data-testid="stSidebar"] .css-1d391kg {
        text-align: right;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        direction: rtl;
        text-align: right;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        direction: ltr;
        text-align: center;
    }
    
    [data-testid="stMetricLabel"] {
        direction: rtl;
        text-align: right;
    }
    
    /* Buttons */
    .stButton > button {
        direction: rtl;
        width: 100%;
    }
    
    /* Radio buttons */
    .stRadio > label {
        direction: rtl;
        text-align: right;
    }
    
    /* Custom styling */
    .big-font {
        font-size: 24px !important;
        font-weight: bold;
        direction: rtl;
        text-align: right;
    }
    
    .success-box {
        padding: 20px;
        border-radius: 10px;
        background-color: #d4edda;
        border: 2px solid #28a745;
        direction: rtl;
        text-align: right;
        margin: 10px 0;
    }
    
    .warning-box {
        padding: 20px;
        border-radius: 10px;
        background-color: #fff3cd;
        border: 2px solid #ffc107;
        direction: rtl;
        text-align: right;
        margin: 10px 0;
    }
    
    .danger-box {
        padding: 20px;
        border-radius: 10px;
        background-color: #f8d7da;
        border: 2px solid #dc3545;
        direction: rtl;
        text-align: right;
        margin: 10px 0;
    }
    
    .info-box {
        padding: 20px;
        border-radius: 10px;
        background-color: #d1ecf1;
        border: 2px solid #17a2b8;
        direction: rtl;
        text-align: right;
        margin: 10px 0;
    }
    
    /* Tables */
    .dataframe {
        direction: rtl;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    """Load and cache the driving data"""
    try:
        df = pd.read_csv("driving_data.csv", encoding="utf-8-sig")
    except FileNotFoundError:
        df = generate_dummy_data(500)
        df.to_csv("driving_data.csv", index=False, encoding="utf-8-sig")
    return df


@st.cache_resource
def load_models(df):
    """Load and train ML models"""
    calculator = SafetyScoreCalculator()
    predictor = RiskPredictor()
    predictor.train(df)
    coach = AICoach()
    return calculator, predictor, coach


def create_gauge_chart(score, title="درجة السلامة"):
    """Create a gauge chart for safety score"""
    calculator = SafetyScoreCalculator()
    color = calculator.get_score_color(score)
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 24}},
        delta={'reference': 85, 'increasing': {'color': "green"}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 50], 'color': '#ffcccc'},
                {'range': [50, 70], 'color': '#fff4cc'},
                {'range': [70, 85], 'color': '#ffffcc'},
                {'range': [85, 100], 'color': '#ccffcc'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        height=400,
        font={'size': 16},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    
    return fig


def create_score_history_chart(df, days=30):
    """Create line chart showing score history"""
    # Calculate daily scores
    df['date'] = pd.to_datetime(df['date'])
    end_date = df['date'].max()
    start_date = end_date - timedelta(days=days)
    
    recent_data = df[df['date'] >= start_date].copy()
    
    # Group by date and calculate score
    calculator = SafetyScoreCalculator()
    daily_scores = []
    
    for date in pd.date_range(start_date, end_date):
        day_data = recent_data[recent_data['date'] == date]
        if len(day_data) > 0:
            score = calculator.calculate_score(day_data)
            daily_scores.append({'date': date, 'score': score})
    
    if len(daily_scores) == 0:
        return None
    
    score_df = pd.DataFrame(daily_scores)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=score_df['date'],
        y=score_df['score'],
        mode='lines+markers',
        name='درجة السلامة',
        line=dict(color='#00C851', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title="تاريخ درجة السلامة - آخر 30 يوم",
        xaxis_title="التاريخ",
        yaxis_title="درجة السلامة",
        height=400,
        hovermode='x unified',
        font={'size': 14},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.9)"
    )
    
    return fig


def create_risk_heatmap(df):
    """Create heatmap of high-risk zones"""
    # Filter high-risk areas (speeding + violations)
    risk_data = df[
        ((df['speed_kmh'] > df['speed_limit']) | 
         (df['violation_type'] != 'لا يوجد') |
         (df['harsh_braking'] == 1))
    ].copy()
    
    if len(risk_data) == 0:
        return None
    
    # Aggregate risk by location
    risk_by_location = risk_data.groupby(['location_lat', 'location_lon', 'location_name']).size().reset_index(name='risk_count')
    
    # Create pydeck layer
    layer = pdk.Layer(
        'HeatmapLayer',
        data=risk_data,
        get_position='[location_lon, location_lat]',
        get_weight='harsh_braking + phone_usage + 1',
        radiusPixels=60,
        intensity=1,
        threshold=0.3,
    )
    
    # Set the viewport location
    view_state = pdk.ViewState(
        latitude=24.7136,
        longitude=46.6753,
        zoom=11,
        pitch=0,
    )
    
    # Render
    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style='mapbox://styles/mapbox/light-v9',
    )
    
    return r


def user_profile_page():
    """Citizen/User Profile View"""
    st.title("🚗 سلمين - ملفك الشخصي")
    st.markdown("---")
    
    # Load data
    df = load_data()
    calculator, predictor, coach = load_models(df)
    
    # User info
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown("### 👤 المستخدم")
        st.markdown("**الاسم:** عبدالله محمد")
        st.markdown("**رقم الهوية:** ************1234")
        st.markdown("**نوع الرخصة:** خاصة")
    
    with col2:
        # Calculate current safety score (last 30 days)
        recent_data = df.tail(100)  # Simulate user's recent data
        safety_score = calculator.calculate_score(recent_data)
        category = calculator.get_score_category(safety_score)
        
        # Risk prediction
        risk_prediction = predictor.predict(recent_data)
        
        st.markdown("### 📊 الإحصائيات السريعة")
        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
        
        with metric_col1:
            st.metric("درجة السلامة", f"{safety_score}/100", delta=None)
        
        with metric_col2:
            st.metric("التصنيف", category)
        
        with metric_col3:
            violations = recent_data[recent_data['violation_type'] != 'لا يوجد']
            st.metric("المخالفات (30 يوم)", len(violations))
        
        with metric_col4:
            st.metric("مستوى الخطر", risk_prediction['risk_level'])
    
    st.markdown("---")
    
    # Safety Score Gauge
    st.markdown("### 🎯 درجة السلامة الحالية")
    gauge_fig = create_gauge_chart(safety_score)
    st.plotly_chart(gauge_fig, use_container_width=True)
    
    # Score interpretation
    if safety_score >= 85:
        st.markdown('<div class="success-box">✅ <strong>ممتاز!</strong> أنت سائق آمن. استمر في القيادة الحذرة.</div>', unsafe_allow_html=True)
    elif safety_score >= 70:
        st.markdown('<div class="info-box">ℹ️ <strong>جيد</strong> - قيادتك جيدة، لكن هناك مجال للتحسين.</div>', unsafe_allow_html=True)
    elif safety_score >= 50:
        st.markdown('<div class="warning-box">⚠️ <strong>متوسط</strong> - يرجى الانتباه لسلوك القيادة وتجنب المخالفات.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="danger-box">🚨 <strong>ضعيف</strong> - قيادتك تحتاج لتحسين كبير. يرجى اتباع التوصيات.</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Score History
    st.markdown("### 📈 تاريخ درجة السلامة")
    history_fig = create_score_history_chart(recent_data, days=30)
    if history_fig:
        st.plotly_chart(history_fig, use_container_width=True)
    else:
        st.info("لا توجد بيانات كافية لعرض التاريخ")
    
    st.markdown("---")
    
    # AI Coach Recommendations
    st.markdown("### 🤖 المدرب الذكي - توصيات مخصصة")
    recommendations = coach.generate_recommendations(recent_data, safety_score)
    
    for i, rec in enumerate(recommendations, 1):
        st.markdown(f"**{i}.** {rec}")
    
    st.markdown("---")
    
    # Recent Activity
    st.markdown("### 📋 النشاط الأخير")
    recent_activity = recent_data.tail(10)[['date', 'location_name', 'speed_kmh', 'violation_type']].copy()
    recent_activity.columns = ['التاريخ', 'الموقع', 'السرعة (كم/س)', 'نوع المخالفة']
    st.dataframe(recent_activity, use_container_width=True, hide_index=True)


def ministry_dashboard_page():
    """Ministry/Government Dashboard View"""
    st.title("🏛️ لوحة التحكم - وزارة الداخلية")
    st.markdown("---")
    
    # Load data
    df = load_data()
    calculator, predictor, coach = load_models(df)
    
    # Key Metrics
    st.markdown("### 📊 المؤشرات الرئيسية")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_violations = len(df[df['violation_type'] != 'لا يوجد'])
        st.metric("إجمالي المخالفات", f"{total_violations:,}")
    
    with col2:
        avg_score = calculator.calculate_score(df)
        st.metric("متوسط درجة السلامة", f"{avg_score}/100")
    
    with col3:
        high_risk_count = len(df[df['driver_profile'] == 'risky'])
        risk_percentage = (high_risk_count / len(df)) * 100
        st.metric("السائقون عاليو الخطورة", f"{risk_percentage:.1f}%")
    
    with col4:
        phone_violations = df['phone_usage'].sum()
        st.metric("استخدام الجوال", f"{phone_violations:,}")
    
    st.markdown("---")
    
    # Heatmap
    st.markdown("### 🗺️ خريطة المناطق عالية الخطورة - الرياض")
    
    heatmap = create_risk_heatmap(df)
    if heatmap:
        st.pydeck_chart(heatmap)
    else:
        st.info("لا توجد بيانات كافية لعرض الخريطة")
    
    st.markdown("---")
    
    # Top Risk Locations
    st.markdown("### 📍 أكثر المناطق خطورة")
    
    risk_data = df[
        ((df['speed_kmh'] > df['speed_limit']) | 
         (df['violation_type'] != 'لا يوجد') |
         (df['harsh_braking'] == 1))
    ]
    
    location_risk = risk_data.groupby('location_name').size().reset_index(name='عدد الحوادث')
    location_risk = location_risk.sort_values('عدد الحوادث', ascending=False).head(10)
    location_risk.columns = ['المنطقة', 'عدد الحوادث']
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig = px.bar(
            location_risk,
            x='عدد الحوادث',
            y='المنطقة',
            orientation='h',
            title='أكثر 10 مناطق خطورة',
            color='عدد الحوادث',
            color_continuous_scale='Reds'
        )
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.dataframe(location_risk, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Violation Types Distribution
    st.markdown("### 📊 توزيع أنواع المخالفات")
    
    violations = df[df['violation_type'] != 'لا يوجد']
    violation_counts = violations['violation_type'].value_counts().reset_index()
    violation_counts.columns = ['نوع المخالفة', 'العدد']
    
    fig = px.pie(
        violation_counts,
        values='العدد',
        names='نوع المخالفة',
        title='توزيع المخالفات حسب النوع',
        hole=0.4
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Time Series Analysis
    st.markdown("### 📅 تحليل المخالفات عبر الزمن")
    
    df['date'] = pd.to_datetime(df['date'])
    daily_violations = df[df['violation_type'] != 'لا يوجد'].groupby('date').size().reset_index(name='عدد المخالفات')
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=daily_violations['date'],
        y=daily_violations['عدد المخالفات'],
        mode='lines+markers',
        name='المخالفات اليومية',
        line=dict(color='#ff4444', width=2),
        fill='tozeroy'
    ))
    
    fig.update_layout(
        title="المخالفات اليومية",
        xaxis_title="التاريخ",
        yaxis_title="عدد المخالفات",
        height=400,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)


def main():
    """Main application"""
    
    # Sidebar
    st.sidebar.title("🚗 سلمين")
    st.sidebar.markdown("### منصة السلامة المرورية الذكية")
    st.sidebar.markdown("---")
    
    # Navigation
    page = st.sidebar.radio(
        "اختر الصفحة:",
        ["👤 الملف الشخصي", "🏛️ لوحة التحكم الوزارية"],
        index=0
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ℹ️ عن المنصة")
    st.sidebar.info(
        "سلمين هي منصة ذكية لتعزيز السلامة المرورية في المملكة العربية السعودية. "
        "تستخدم الذكاء الاصطناعي لتقييم سلوك القيادة وتقديم توصيات مخصصة."
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("**النسخة:** 1.0.0")
    st.sidebar.markdown("**تاريخ الإطلاق:** 2025")
    st.sidebar.markdown("**متكامل مع:** أبشر")
    
    # Route to selected page
    if page == "👤 الملف الشخصي":
        user_profile_page()
    else:
        ministry_dashboard_page()


if __name__ == "__main__":
    main()
