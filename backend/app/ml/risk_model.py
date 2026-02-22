import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import os
from app.utils.logger import get_logger
from typing import List, Dict, Any
import json

logger = get_logger(__name__)

class RiskPredictionModel:
    def __init__(self, model_path: str = None):
        """Initialize risk prediction model"""
        self.model = None
        self.vectorizer = None
        self.model_path = model_path or "models/risk_model.pkl"
        self.vectorizer_path = "models/vectorizer.pkl"
        
        # Try to load existing model
        self.load_model()
    
    def load_model(self):
        """Load pre-trained model if exists"""
        try:
            if os.path.exists(self.model_path):
                self.model = joblib.load(self.model_path)
                self.vectorizer = joblib.load(self.vectorizer_path)
                logger.info("Loaded pre-trained risk model")
            else:
                # Initialize with default model
                self._init_default_model()
                logger.info("Initialized default risk model")
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            self._init_default_model()
    
    def _init_default_model(self):
        """Initialize default model"""
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.vectorizer = TfidfVectorizer(max_features=1000)
        
        # Train with some default data
        self._train_default()
    
    def _train_default(self):
        """Train with default data"""
        # Sample training data
        sample_texts = [
            "simple crud application with basic features",
            "complex microservices architecture with high scalability",
            "machine learning system with real-time predictions",
            "e-commerce platform with payment integration",
            "mobile app with offline sync",
            "real-time chat application with websockets",
            "data pipeline processing millions of events",
            "blockchain based smart contract system",
            "IoT device management platform",
            "video streaming service with transcoding"
        ]
        
        # Sample risk labels (0=low, 1=medium, 2=high)
        sample_risks = [0, 2, 2, 1, 1, 1, 2, 2, 1, 2]
        
        # Vectorize text
        X = self.vectorizer.fit_transform(sample_texts)
        
        # Train model
        self.model.fit(X, sample_risks)
        
        # Save model
        self.save_model()
    
    def predict_risks(self, text: str) -> List[Dict[str, Any]]:
        """Predict risks from text"""
        try:
            # Vectorize input
            X = self.vectorizer.transform([text])
            
            # Get prediction
            risk_level = self.model.predict(X)[0]
            probabilities = self.model.predict_proba(X)[0]
            
            # Generate risk details based on prediction
            risks = self._generate_risk_details(risk_level, probabilities, text)
            
            return risks
            
        except Exception as e:
            logger.error(f"Risk prediction failed: {str(e)}")
            return self._get_default_risks()
    
    def _generate_risk_details(
        self, 
        risk_level: int, 
        probabilities: np.ndarray,
        text: str
    ) -> List[Dict[str, Any]]:
        """Generate detailed risk information"""
        risks = []
        
        # Map risk level to description
        risk_descriptions = {
            0: {
                "category": "technical",
                "description": "Low technical complexity",
                "probability": 0.2,
                "impact": "low",
                "mitigation": "Standard development practices"
            },
            1: {
                "category": "technical",
                "description": "Moderate technical complexity",
                "probability": 0.5,
                "impact": "medium",
                "mitigation": "Conduct technical design review"
            },
            2: {
                "category": "technical",
                "description": "High technical complexity",
                "probability": 0.8,
                "impact": "high",
                "mitigation": "Break down into smaller components, prototype key features"
            }
        }
        
        # Add main risk
        main_risk = risk_descriptions.get(risk_level, risk_descriptions[1])
        main_risk["probability"] = float(probabilities[risk_level])
        risks.append(main_risk)
        
        # Add specific risks based on text analysis
        if "payment" in text.lower() or "stripe" in text.lower():
            risks.append({
                "category": "security",
                "description": "Payment processing security",
                "probability": 0.7,
                "impact": "critical",
                "mitigation": "PCI compliance, security audit, penetration testing"
            })
        
        if "real-time" in text.lower() or "websocket" in text.lower():
            risks.append({
                "category": "technical",
                "description": "Real-time communication complexity",
                "probability": 0.6,
                "impact": "high",
                "mitigation": "Use established WebSocket libraries, load testing"
            })
        
        if "machine learning" in text.lower() or "ai" in text.lower():
            risks.append({
                "category": "technical",
                "description": "ML model accuracy and performance",
                "probability": 0.7,
                "impact": "high",
                "mitigation": "Start with simple models, iterate based on data"
            })
        
        if "scalable" in text.lower() or "high traffic" in text.lower():
            risks.append({
                "category": "infrastructure",
                "description": "Scalability under load",
                "probability": 0.6,
                "impact": "high",
                "mitigation": "Design for horizontal scaling, load testing"
            })
        
        return risks
    
    def _get_default_risks(self) -> List[Dict[str, Any]]:
        """Get default risks if prediction fails"""
        return [
            {
                "category": "technical",
                "description": "Technical complexity risk",
                "probability": 0.5,
                "impact": "medium",
                "mitigation": "Regular technical reviews and prototyping"
            },
            {
                "category": "timeline",
                "description": "Timeline estimation risk",
                "probability": 0.6,
                "impact": "high",
                "mitigation": "Add buffer time, use agile methodology"
            }
        ]
    
    def save_model(self):
        """Save trained model"""
        try:
            os.makedirs("models", exist_ok=True)
            joblib.dump(self.model, self.model_path)
            joblib.dump(self.vectorizer, self.vectorizer_path)
            logger.info("Model saved successfully")
        except Exception as e:
            logger.error(f"Failed to save model: {str(e)}")
    
    def retrain(self, texts: List[str], labels: List[int]):
        """Retrain model with new data"""
        try:
            X = self.vectorizer.fit_transform(texts)
            self.model.fit(X, labels)
            self.save_model()
            logger.info("Model retrained successfully")
        except Exception as e:
            logger.error(f"Retraining failed: {str(e)}")