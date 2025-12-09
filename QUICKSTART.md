# 🚀 Quick Start Guide - Salmeen Platform

## Installation (3 Steps)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Generate Data (Optional - already included)
```bash
python utils.py
```
This will generate `driving_data.csv` with 500 realistic driving records.

### Step 3: Run the Application
```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`

---

## 📱 Navigation

### User Profile (Citizen View)
1. Click **"👤 الملف الشخصي"** in the sidebar
2. View your safety score (0-100)
3. Check score history chart
4. Read AI coach recommendations
5. Review recent driving activity

### Ministry Dashboard (Government View)
1. Click **"🏛️ لوحة التحكم الوزارية"** in the sidebar
2. View key metrics and statistics
3. Explore the risk heatmap of Riyadh
4. Analyze top risky locations
5. Review violation distributions

---

## 🎯 Key Features to Test

### 1. Safety Score Gauge
- Interactive gauge showing score 0-100
- Color-coded: Green (85+), Amber (70-84), Orange (50-69), Red (0-49)

### 2. Score History Chart
- Line chart showing 30-day trend
- Hover to see daily scores

### 3. AI Coach Recommendations
- Personalized advice based on driving behavior
- Specific location-based warnings

### 4. Risk Heatmap
- Interactive map of Riyadh
- Shows high-risk zones in red

### 5. Analytics Dashboard
- Total violations count
- Average city safety score
- High-risk driver percentage
- Phone usage statistics

---

## 🧪 Testing Scenarios

### Scenario 1: Safe Driver Profile
The default view shows a "safe" driver with:
- Score: ~70-85
- Few violations
- Positive recommendations

### Scenario 2: Risky Driver Pattern
Data includes ~30% risky drivers with:
- Lower scores (50-70)
- More speeding violations
- Harsh braking incidents
- Phone usage violations

### Scenario 3: Location Analysis
Check the heatmap to see:
- King Fahd Road (طريق الملك فهد)
- King Abdullah Road (طريق الملك عبدالله)
- Other Riyadh locations

---

## 🔧 Customization

### Change Number of Records
Edit `utils.py`:
```python
df = generate_dummy_data(1000)  # Change from 500 to 1000
```

### Adjust Safety Score Algorithm
Edit `model.py` in the `SafetyScoreCalculator` class:
```python
speeding_penalty = min(30, ...)  # Adjust penalty weights
```

### Add New Locations
Edit `utils.py` in the `riyadh_locations` list:
```python
{"name": "حي جديد", "lat": 24.7000, "lon": 46.7000}
```

---

## 📊 Understanding the Data

### Data File: `driving_data.csv`
- **500 rows** of driving logs
- **10 columns** of features
- **90 days** of historical data
- **10 locations** in Riyadh

### Key Metrics
- Speed range: 60-180 km/h
- Speed limit: 120 km/h (most roads)
- Violation types: 7 different types
- Driver profiles: Safe (70%) vs Risky (30%)

---

## 🐛 Troubleshooting

### Issue: Port Already in Use
```bash
streamlit run app.py --server.port 8502
```

### Issue: Missing Dependencies
```bash
pip install --upgrade streamlit scikit-learn pydeck plotly
```

### Issue: Data Not Loading
```bash
python utils.py  # Regenerate data
```

### Issue: Arabic Text Not Displaying
- Ensure your browser supports Arabic fonts
- Try Chrome or Firefox for best results

---

## 💡 Tips

1. **RTL Support**: The entire UI is right-to-left for Arabic
2. **Responsive**: Works on desktop and tablet (mobile view limited)
3. **Interactive**: All charts are interactive - hover, zoom, pan
4. **Real-time**: Data updates when you switch between pages
5. **Cached**: ML models are cached for fast performance

---

## 📈 Next Steps

After exploring the MVP:

1. **Customize the data** to match your specific use case
2. **Adjust the scoring algorithm** based on your requirements
3. **Add new features** like user authentication
4. **Integrate with real APIs** (Absher, traffic cameras, etc.)
5. **Deploy to production** using Streamlit Cloud or Docker

---

## 🎓 Learning Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [Plotly Charts](https://plotly.com/python/)
- [PyDeck Maps](https://deckgl.readthedocs.io)
- [scikit-learn ML](https://scikit-learn.org)

---

**Happy Hacking! 🚗💨**
