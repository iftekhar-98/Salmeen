#  سالمين (Salmeen) - Saudi Smart Traffic Safety Platform

## نظرة عامة | Overview

**سالمين** هي منصة ذكية للسلامة المرورية في المملكة العربية السعودية، متكاملة مع منصة أبشر. تستخدم الذكاء الاصطناعي لحساب "درجة السلامة" (0-100) للسائقين بناءً على سلوكهم في القيادة، وتتنبأ بمستويات الخطر.

**Salmeen** is a Saudi smart traffic safety platform integrated with "Absher". It calculates a "Safety Score" (0-100) for drivers based on their behavior and uses AI to predict risk levels.

---

## ✨ المميزات | Features

### 1. واجهة المواطن (Citizen View)
- **درجة السلامة**: عرض مرئي تفاعلي لدرجة السلامة الحالية (0-100)
- **التاريخ**: رسم بياني يوضح تطور درجة السلامة خلال آخر 30 يوم
- **المدرب الذكي**: توصيات مخصصة بناءً على سلوك القيادة
- **النشاط الأخير**: جدول بآخر الرحلات والمخالفات

### 2. لوحة التحكم الوزارية (Ministry Dashboard)
- **المؤشرات الرئيسية**: إحصائيات شاملة عن المخالفات والسلامة
- **خريطة حرارية**: عرض المناطق عالية الخطورة في الرياض
- **تحليل المناطق**: أكثر 10 مناطق خطورة
- **توزيع المخالفات**: تحليل أنواع المخالفات
- **التحليل الزمني**: متابعة المخالفات عبر الزمن

### 3. الذكاء الاصطناعي
- **حساب درجة السلامة**: خوارزمية متقدمة تأخذ في الاعتبار:
  - تجاوز السرعة
  - الفرملة المفاجئة
  - استخدام الجوال أثناء القيادة
  - المخالفات المرورية
- **التنبؤ بالخطر**: نموذج Random Forest للتنبؤ بمستوى خطورة السائق
- **التوصيات الذكية**: نصائح مخصصة لتحسين سلوك القيادة

### 4. دعم اللغة العربية
- واجهة كاملة باللغة العربية
- دعم RTL (Right-to-Left)
- بيانات واقعية من سياق الرياض

---

##  التقنيات المستخدمة | Tech Stack

- **Framework**: Streamlit
- **Language**: Python 3.11
- **ML**: scikit-learn (Random Forest Classifier)
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly, PyDeck
- **Maps**: PyDeck with Heatmap Layer

---

## هيكل المشروع | Project Structure

```
salmeen/
├── app.py                  # Main Streamlit application
├── utils.py                # Data generation utilities
├── model.py                # ML models and scoring logic
├── driving_data.csv        # Generated dummy data (500 records)
└── README.md               # This file
```

---

## التشغيل | Installation & Running

### المتطلبات | Requirements

```bash
pip install streamlit scikit-learn pydeck plotly pandas numpy
```

### تشغيل التطبيق | Run the Application

```bash
cd salmeen
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

---

## البيانات | Data

### مصدر البيانات | Data Source
نظرًا لعدم توفر API حقيقي، تم إنشاء بيانات واقعية تحاكي سياق المرور في الرياض:

Since we don't have access to a real API, realistic dummy data simulating Saudi traffic contexts (Riyadh) was generated:

- **500 سجل قيادة** | 500 driving records
- **مواقع حقيقية في الرياض** | Real Riyadh locations (King Fahd Road, King Abdullah Road, etc.)
- **أنواع مخالفات واقعية** | Realistic violation types
- **نمطان للسائقين** | Two driver profiles:
  - 70% سائقون آمنون | Safe drivers
  - 30% سائقون عاليو الخطورة | Risky drivers

### الأعمدة | Data Columns

| Column | Description (AR) | Description (EN) |
|--------|------------------|------------------|
| `date` | التاريخ | Date of driving log |
| `speed_kmh` | السرعة (كم/س) | Speed in km/h |
| `speed_limit` | الحد الأقصى للسرعة | Speed limit |
| `harsh_braking` | فرملة مفاجئة | Harsh braking (0/1) |
| `phone_usage` | استخدام الجوال | Phone usage (0/1) |
| `location_lat` | خط العرض | Latitude |
| `location_lon` | خط الطول | Longitude |
| `location_name` | اسم الموقع | Location name (Arabic) |
| `violation_type` | نوع المخالفة | Violation type (Arabic) |
| `driver_profile` | نمط السائق | Driver profile (safe/risky) |

---

##  خوارزمية درجة السلامة | Safety Score Algorithm

تبدأ الدرجة من 100 ويتم خصم نقاط بناءً على:

The score starts at 100 and deducts points based on:

1. **تجاوز السرعة** | Speeding (up to -30 points)
2. **الفرملة المفاجئة** | Harsh braking (up to -20 points)
3. **استخدام الجوال** | Phone usage (up to -25 points)
4. **المخالفات المرورية** | Traffic violations (up to -25 points)

### التصنيفات | Categories

| Score Range | Category (AR) | Category (EN) | Color |
|-------------|---------------|---------------|-------|
| 85-100 | ممتاز | Excellent | Green |
| 70-84 | جيد | Good | Amber |
| 50-69 | متوسط | Average | Orange |
| 0-49 | ضعيف | Poor | Red |

---

##  نموذج التعلم الآلي | ML Model

### النموذج | Model Type
**Random Forest Classifier** with:
- 100 estimators
- Max depth: 10
- Random state: 42

### المميزات | Features
1. متوسط السرعة | Average speed
2. أقصى سرعة | Maximum speed
3. معدل تجاوز السرعة | Speed violations rate
4. معدل الفرملة المفاجئة | Harsh braking rate
5. معدل استخدام الجوال | Phone usage rate
6. معدل المخالفات | Violation rate
7. متوسط تجاوز الحد الأقصى | Average over speed limit

### الأداء | Performance
- تم التدريب على 26 عينة | Trained on 26 samples
- دقة التنبؤ: ~76% | Prediction confidence: ~76%

---

##  لقطات الشاشة | Screenshots

### 1. الملف الشخصي | User Profile
- عرض درجة السلامة بمقياس تفاعلي
- رسم بياني لتاريخ الدرجة
- توصيات المدرب الذكي
- جدول النشاط الأخير

### 2. لوحة التحكم الوزارية | Ministry Dashboard
- المؤشرات الرئيسية
- خريطة حرارية للمناطق الخطرة
- تحليل المناطق الأكثر خطورة
- توزيع المخالفات
- التحليل الزمني

---

##  حالات الاستخدام | Use Cases

### للمواطنين | For Citizens
1. **متابعة درجة السلامة**: معرفة مستوى أمان القيادة
2. **تحسين السلوك**: الحصول على توصيات لتحسين القيادة
3. **تجنب المخالفات**: التنبيه للسلوكيات الخطرة
4. **مكافآت محتملة**: درجة عالية قد تؤدي لخصومات تأمين

### للجهات الحكومية | For Government
1. **تحديد المناطق الخطرة**: معرفة أين تحدث معظم المخالفات
2. **تخطيط الحملات**: استهداف المناطق والسلوكيات الأكثر خطورة
3. **قياس الأداء**: متابعة تحسن السلامة المرورية
4. **اتخاذ القرارات**: بيانات لدعم سياسات المرور

---

##  التطوير المستقبلي | Future Enhancements

### المرحلة الثانية | Phase 2
- [ ] تكامل حقيقي مع API أبشر
- [ ] نظام إشعارات فورية
- [ ] تطبيق جوال (iOS/Android)
- [ ] نظام مكافآت وخصومات

### المرحلة الثالثة | Phase 3
- [ ] تحليلات متقدمة بالذكاء الاصطناعي
- [ ] تنبؤ بالحوادث قبل وقوعها
- [ ] تكامل مع أنظمة السيارات الذكية
- [ ] لوحة تحكم للشركات (أساطيل المركبات)

---

##  المطور | Developer

Built as a hackathon MVP by a Senior Python Full-Stack Engineer.

**Technologies Demonstrated:**
- ✅ Streamlit for rapid prototyping
- ✅ Machine Learning with scikit-learn
- ✅ Data visualization with Plotly
- ✅ Geospatial analysis with PyDeck
- ✅ Arabic RTL UI/UX design
- ✅ Clean code architecture

---

##  الترخيص | License

This is a hackathon MVP project for demonstration purposes.

---

##  شكر وتقدير | Acknowledgments

- **وزارة الداخلية السعودية** | Saudi Ministry of Interior
- **منصة أبشر** | Absher Platform
- **Streamlit Community**
- **Plotly & PyDeck Teams**

---

##  التواصل | Contact

For questions or collaboration opportunities, please reach out through the hackathon platform.

---

** قد بسلامة! | Drive Safe!**
