"""
ML Model and Safety Scoring Logic for Salmeen Platform
Calculates safety scores and predicts driver risk levels
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import warnings

warnings.filterwarnings("ignore")


class SafetyScoreCalculator:
    """Calculate driver safety score based on driving behavior"""
    
    def __init__(self):
        self.base_score = 100
        
    def calculate_score(self, driver_data):
        """
        Calculate safety score for a driver based on their driving logs
        
        Args:
            driver_data (pd.DataFrame): DataFrame with driver's driving logs
            
        Returns:
            float: Safety score (0-100)
        """
        score = self.base_score
        
        if len(driver_data) == 0:
            return score
        
        # Penalty for speeding
        speeding_violations = driver_data[driver_data["speed_kmh"] > driver_data["speed_limit"]]
        if len(speeding_violations) > 0:
            avg_over_limit = (speeding_violations["speed_kmh"] - speeding_violations["speed_limit"]).mean()
            speeding_penalty = min(30, (len(speeding_violations) / len(driver_data)) * 40 + avg_over_limit * 0.2)
            score -= speeding_penalty
        
        # Penalty for harsh braking
        harsh_braking_count = driver_data["harsh_braking"].sum()
        harsh_braking_rate = harsh_braking_count / len(driver_data)
        harsh_braking_penalty = min(20, harsh_braking_rate * 50)
        score -= harsh_braking_penalty
        
        # Penalty for phone usage
        phone_usage_count = driver_data["phone_usage"].sum()
        phone_usage_rate = phone_usage_count / len(driver_data)
        phone_usage_penalty = min(25, phone_usage_rate * 60)
        score -= phone_usage_penalty
        
        # Penalty for violations
        violations = driver_data[driver_data["violation_type"] != "لا يوجد"]
        violation_penalty = min(25, (len(violations) / len(driver_data)) * 50)
        score -= violation_penalty
        
        # Ensure score is between 0 and 100
        score = max(0, min(100, score))
        
        return round(score, 1)
    
    def get_score_category(self, score):
        """
        Get category label for a safety score
        
        Args:
            score (float): Safety score
            
        Returns:
            str: Category in Arabic
        """
        if score >= 85:
            return "ممتاز"
        elif score >= 70:
            return "جيد"
        elif score >= 50:
            return "متوسط"
        else:
            return "ضعيف"
    
    def get_score_color(self, score):
        """
        Get color for a safety score
        
        Args:
            score (float): Safety score
            
        Returns:
            str: Color code
        """
        if score >= 85:
            return "#00C851"  # Green
        elif score >= 70:
            return "#ffbb33"  # Amber
        elif score >= 50:
            return "#ff8800"  # Orange
        else:
            return "#ff4444"  # Red


class RiskPredictor:
    """Predict driver risk level using ML"""
    
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
        self.scaler = StandardScaler()
        self.is_trained = False
        
    def prepare_features(self, df):
        """
        Prepare features for ML model
        
        Args:
            df (pd.DataFrame): Raw driving data
            
        Returns:
            dict: Feature dictionary
        """
        features = {
            "avg_speed": df["speed_kmh"].mean(),
            "max_speed": df["speed_kmh"].max(),
            "speed_violations_rate": (df["speed_kmh"] > df["speed_limit"]).sum() / len(df),
            "harsh_braking_rate": df["harsh_braking"].sum() / len(df),
            "phone_usage_rate": df["phone_usage"].sum() / len(df),
            "violation_rate": (df["violation_type"] != "لا يوجد").sum() / len(df),
            "avg_over_limit": (df["speed_kmh"] - df["speed_limit"]).mean()
        }
        
        return features
    
    def train(self, df):
        """
        Train the risk prediction model
        
        Args:
            df (pd.DataFrame): Training data with driver_profile column
        """
        # Group by driver profile and create features
        X_list = []
        y_list = []
        
        # Create synthetic driver groups for training
        for profile in df["driver_profile"].unique():
            profile_data = df[df["driver_profile"] == profile]
            
            # Split into chunks to simulate different drivers
            chunk_size = 20
            for i in range(0, len(profile_data), chunk_size):
                chunk = profile_data.iloc[i:i+chunk_size]
                if len(chunk) >= 10:  # Minimum records
                    features = self.prepare_features(chunk)
                    X_list.append(features)
                    y_list.append(1 if profile == "risky" else 0)
        
        X = pd.DataFrame(X_list)
        y = np.array(y_list)
        
        # Train model
        if len(X) > 10:
            X_scaled = self.scaler.fit_transform(X)
            self.model.fit(X_scaled, y)
            self.is_trained = True
            print(f"✅ Model trained on {len(X)} samples")
        else:
            print("⚠️ Not enough data to train model")
    
    def predict(self, driver_data):
        """
        Predict risk level for a driver
        
        Args:
            driver_data (pd.DataFrame): Driver's driving logs
            
        Returns:
            dict: Prediction result with risk level and confidence
        """
        if not self.is_trained or len(driver_data) < 10:
            return {
                "risk_level": "غير محدد",
                "risk_level_en": "Unknown",
                "confidence": 0.0,
                "is_high_risk": False
            }
        
        features = self.prepare_features(driver_data)
        X = pd.DataFrame([features])
        X_scaled = self.scaler.transform(X)
        
        prediction = self.model.predict(X_scaled)[0]
        probability = self.model.predict_proba(X_scaled)[0]
        
        is_high_risk = bool(prediction == 1)
        confidence = float(probability[prediction])
        
        return {
            "risk_level": "عالي الخطورة" if is_high_risk else "آمن",
            "risk_level_en": "High Risk" if is_high_risk else "Safe",
            "confidence": round(confidence * 100, 1),
            "is_high_risk": is_high_risk
        }


class AICoach:
    """Generate personalized driving recommendations"""
    
    def __init__(self):
        pass
    
    def generate_recommendations(self, driver_data, safety_score):
        """
        Generate personalized recommendations based on driving behavior
        
        Args:
            driver_data (pd.DataFrame): Driver's driving logs
            safety_score (float): Current safety score
            
        Returns:
            list: List of recommendations in Arabic
        """
        recommendations = []
        
        if len(driver_data) == 0:
            return ["لا توجد بيانات كافية لتقديم توصيات"]
        
        # Check speeding
        speeding_violations = driver_data[driver_data["speed_kmh"] > driver_data["speed_limit"]]
        if len(speeding_violations) > 0:
            most_common_location = speeding_violations["location_name"].mode()
            if len(most_common_location) > 0:
                recommendations.append(
                    f"⚠️ لاحظنا تجاوزاً متكرراً للسرعة في {most_common_location.iloc[0]}. "
                    f"يرجى الالتزام بالسرعة المحددة للحفاظ على سلامتك."
                )
        
        # Check harsh braking
        harsh_braking_rate = driver_data["harsh_braking"].sum() / len(driver_data)
        if harsh_braking_rate > 0.15:
            recommendations.append(
                "🚗 معدل الفرملة المفاجئة مرتفع. حاول الحفاظ على مسافة آمنة مع المركبات الأمامية "
                "وتوقع حركة المرور مسبقاً."
            )
        
        # Check phone usage
        phone_usage_rate = driver_data["phone_usage"].sum() / len(driver_data)
        if phone_usage_rate > 0.05:
            recommendations.append(
                "📱 تم رصد استخدام الجوال أثناء القيادة. استخدم نظام البلوتوث أو أوقف السيارة "
                "في مكان آمن للرد على المكالمات."
            )
        
        # Check violations
        violations = driver_data[driver_data["violation_type"] != "لا يوجد"]
        if len(violations) > 0:
            violation_types = violations["violation_type"].value_counts()
            most_common = violation_types.index[0]
            recommendations.append(
                f"⚡ تم رصد مخالفة: {most_common}. يرجى الالتزام بقواعد المرور لتجنب الغرامات "
                f"والحفاظ على سلامتك وسلامة الآخرين."
            )
        
        # Positive reinforcement
        if safety_score >= 85:
            recommendations.append(
                "✅ أداء ممتاز! استمر في القيادة الآمنة والالتزام بقواعد المرور."
            )
        
        # General advice if no specific issues
        if len(recommendations) == 0:
            recommendations.append(
                "✅ قيادتك جيدة بشكل عام. استمر في الالتزام بقواعد المرور والقيادة الآمنة."
            )
        
        return recommendations


if __name__ == "__main__":
    # Test the model
    from utils import generate_dummy_data
    
    print("Testing Safety Score Calculator and Risk Predictor...")
    
    # Generate data
    df = generate_dummy_data(500)
    
    # Test safety score
    calculator = SafetyScoreCalculator()
    sample_driver_data = df.head(50)
    score = calculator.calculate_score(sample_driver_data)
    category = calculator.get_score_category(score)
    print(f"\n📊 Safety Score: {score}/100 ({category})")
    
    # Test risk predictor
    predictor = RiskPredictor()
    predictor.train(df)
    prediction = predictor.predict(sample_driver_data)
    print(f"🎯 Risk Prediction: {prediction['risk_level']} (Confidence: {prediction['confidence']}%)")
    
    # Test AI coach
    coach = AICoach()
    recommendations = coach.generate_recommendations(sample_driver_data, score)
    print(f"\n💡 AI Recommendations:")
    for rec in recommendations:
        print(f"  - {rec}")
