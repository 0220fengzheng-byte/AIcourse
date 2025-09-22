#!/usr/bin/env python3
import json
import pickle
import os

def export_model(model_data, filename):
    """Export model to JSON file"""
    with open(f"{filename}.json", 'w') as f:
        json.dump(model_data, f, indent=2)
    return f"{filename}.json"

def export_binary(model, filename):
    """Export model to pickle file"""
    with open(f"{filename}.pkl", 'wb') as f:
        pickle.dump(model, f)
    return f"{filename}.pkl"

# Demo
if __name__ == "__main__":
    # Sample AI model for student performance prediction
    student_model = {
        "model_type": "linear_regression",
        "coefficients": [0.8, 0.6, -0.3],
        "intercept": 0.2,
        "features": ["study_hours", "attendance", "sleep_hours"],
        "accuracy": 0.85,
        "created": "2024-09-03"
    }
    
    # Export both formats
    json_path = export_model(student_model, "student_model")
    pkl_path = export_binary(student_model, "student_model")
    
    print(f"✅ Model exported successfully!")
    print(f"JSON format: {json_path}")
    print(f"Binary format: {pkl_path}")
    
    # Verify files exist
    if os.path.exists(json_path):
        print(f"✅ JSON file size: {os.path.getsize(json_path)} bytes")
    if os.path.exists(pkl_path):
        print(f"✅ Binary file size: {os.path.getsize(pkl_path)} bytes")