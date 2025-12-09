"""
Utility functions for Salmeen - Saudi Traffic Safety Platform
Generates realistic dummy data for Saudi traffic contexts
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random


def generate_dummy_data(num_records=500):
    """
    Generate realistic dummy driving data for Saudi Arabia (Riyadh context)
    
    Returns:
        pd.DataFrame: DataFrame with driving logs
    """
    np.random.seed(42)
    random.seed(42)
    
    # Riyadh coordinates (center: 24.7136, 46.6753)
    riyadh_center_lat = 24.7136
    riyadh_center_lon = 46.6753
    
    # Famous Riyadh locations and roads
    riyadh_locations = [
        {"name": "طريق الملك فهد", "lat": 24.7136, "lon": 46.6753},
        {"name": "طريق الملك عبدالله", "lat": 24.7500, "lon": 46.7200},
        {"name": "طريق الملك خالد", "lat": 24.6900, "lon": 46.6900},
        {"name": "شارع العليا", "lat": 24.7100, "lon": 46.6800},
        {"name": "طريق الدائري الشرقي", "lat": 24.7400, "lon": 46.7500},
        {"name": "حي النخيل", "lat": 24.7700, "lon": 46.7300},
        {"name": "حي الملقا", "lat": 24.7800, "lon": 46.6400},
        {"name": "حي الياسمين", "lat": 24.8100, "lon": 46.6600},
        {"name": "طريق خريص", "lat": 24.6500, "lon": 46.7100},
        {"name": "حي الربوة", "lat": 24.7300, "lon": 46.6500},
    ]
    
    # Violation types in Arabic
    violation_types = [
        "لا يوجد",
        "تجاوز السرعة",
        "قطع الإشارة الحمراء",
        "عدم ربط حزام الأمان",
        "استخدام الجوال أثناء القيادة",
        "تجاوز خاطئ",
        "عدم إعطاء الأولوية",
    ]
    
    # Generate data
    data = []
    start_date = datetime.now() - timedelta(days=90)
    
    # Create different driver profiles
    # 70% safe drivers, 30% risky drivers
    driver_profiles = []
    for i in range(num_records):
        if i < num_records * 0.7:
            driver_profiles.append("safe")
        else:
            driver_profiles.append("risky")
    
    random.shuffle(driver_profiles)
    
    for i in range(num_records):
        profile = driver_profiles[i]
        
        # Generate date (random within last 90 days)
        days_ago = random.randint(0, 90)
        record_date = start_date + timedelta(days=days_ago)
        
        # Select random location
        location = random.choice(riyadh_locations)
        lat = location["lat"] + np.random.normal(0, 0.02)
        lon = location["lon"] + np.random.normal(0, 0.02)
        location_name = location["name"]
        
        if profile == "safe":
            # Safe driver characteristics
            speed_kmh = np.random.normal(100, 15)  # Average speed around 100 km/h
            speed_kmh = max(60, min(140, speed_kmh))  # Clamp between 60-140
            harsh_braking = 1 if random.random() < 0.05 else 0  # 5% chance
            phone_usage = 1 if random.random() < 0.03 else 0  # 3% chance
            violation = "لا يوجد" if random.random() < 0.9 else random.choice(violation_types[1:])
        else:
            # Risky driver characteristics
            speed_kmh = np.random.normal(130, 20)  # Higher average speed
            speed_kmh = max(100, min(180, speed_kmh))  # Clamp between 100-180
            harsh_braking = 1 if random.random() < 0.25 else 0  # 25% chance
            phone_usage = 1 if random.random() < 0.20 else 0  # 20% chance
            violation = "لا يوجد" if random.random() < 0.6 else random.choice(violation_types[1:])
        
        # Speed limit (most roads in Riyadh: 120 km/h)
        speed_limit = 120
        
        data.append({
            "date": record_date.strftime("%Y-%m-%d"),
            "speed_kmh": round(speed_kmh, 1),
            "speed_limit": speed_limit,
            "harsh_braking": harsh_braking,
            "phone_usage": phone_usage,
            "location_lat": round(lat, 6),
            "location_lon": round(lon, 6),
            "location_name": location_name,
            "violation_type": violation,
            "driver_profile": profile,
        })
    
    df = pd.DataFrame(data)
    df = df.sort_values("date").reset_index(drop=True)
    
    return df


def save_dummy_data(filename="driving_data.csv"):
    """
    Generate and save dummy data to CSV file
    
    Args:
        filename (str): Output CSV filename
    """
    df = generate_dummy_data()
    df.to_csv(filename, index=False, encoding="utf-8-sig")
    print(f"✅ Generated {len(df)} records and saved to {filename}")
    return df


if __name__ == "__main__":
    # Generate and save data when run directly
    save_dummy_data()
