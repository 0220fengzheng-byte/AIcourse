#!/usr/bin/env python3
"""
Complete Model Export System
This script provides comprehensive model export functionality
"""

import json
import pickle
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

class ModelExporter:
    """Advanced model export system with multiple format support"""
    
    def __init__(self, output_dir: str = "./exported_models"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def export_json(self, data: Dict[str, Any], filename: str) -> str:
        """Export data as JSON file"""
        path = os.path.join(self.output_dir, f"{filename}.json")
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return path
    
    def export_pickle(self, data: Any, filename: str) -> str:
        """Export data as pickle file"""
        path = os.path.join(self.output_dir, f"{filename}.pkl")
        with open(path, 'wb') as f:
            pickle.dump(data, f)
        return path
    
    def export_metadata(self, metadata: Dict[str, Any], filename: str) -> str:
        """Export metadata as JSON"""
        path = os.path.join(self.output_dir, f"{filename}_metadata.json")
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        return path
    
    def export_model_package(self, model: Any, metadata: Dict[str, Any], 
                           name: str) -> Dict[str, str]:
        """Export complete model package"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = f"{name}_{timestamp}"
        
        paths = {}
        paths['json'] = self.export_json(model, f"{base_name}_model")
        paths['pickle'] = self.export_pickle(model, f"{base_name}_model")
        paths['metadata'] = self.export_metadata(metadata, f"{base_name}_metadata")
        
        return paths
    
    def list_models(self) -> List[str]:
        """List all exported models"""
        files = []
        for ext in ['*.json', '*.pkl']:
            import glob
            files.extend(glob.glob(os.path.join(self.output_dir, ext)))
        return [os.path.basename(f) for f in files]

# Sample models for demonstration
def create_sample_models():
    """Create various sample models"""
    
    models = []
    
    # Model 1: Linear Regression for student performance
    linear_model = {
        "model_type": "linear_regression",
        "algorithm": "scikit-learn LinearRegression",
        "coefficients": [0.75, 0.62, -0.28],
        "intercept": 0.15,
        "features": ["study_hours_per_week", "attendance_rate", "sleep_hours"],
        "performance": {
            "rmse": 3.2,
            "mae": 2.8,
            "r2_score": 0.85
        }
    }
    
    # Model 2: Decision Tree for student classification
    tree_model = {
        "model_type": "decision_tree_classifier",
        "algorithm": "scikit-learn DecisionTreeClassifier",
        "max_depth": 8,
        "min_samples_split": 5,
        "criterion": "gini",
        "class_weights": {"A": 1.0, "B": 1.2, "C": 1.5, "D/F": 2.0},
        "feature_importance": {
            "study_hours": 0.45,
            "attendance": 0.35,
            "previous_grades": 0.20
        }
    }
    
    # Model 3: Neural Network for complex predictions
    nn_model = {
        "model_type": "neural_network",
        "algorithm": "PyTorch Sequential",
        "architecture": [10, 64, 32, 16, 1],
        "activations": ["relu", "relu", "relu", "linear"],
        "dropout_rates": [0.0, 0.3, 0.2, 0.0],
        "loss_function": "mse",
        "optimizer": "adam",
        "learning_rate": 0.001,
        "batch_size": 32,
        "epochs": 100
    }
    
    models.extend([
        ("student_performance_linear", linear_model),
        ("student_grade_classifier", tree_model),
        ("student_performance_nn", nn_model)
    ])
    
    return models

def main():
    """Demonstrate the model export system"""
    print("🚀 Starting Model Export System")
    print("=" * 50)
    
    # Initialize exporter
    exporter = ModelExporter()
    
    # Create sample models
    models = create_sample_models()
    
    exported_paths = []
    
    for name, model in models:
        print(f"\n📊 Processing {name}...")
        
        # Create comprehensive metadata
        metadata = {
            "model_name": name,
            "version": "1.0.0",
            "created_by": "AI Efficiency System",
            "created_date": datetime.now().isoformat(),
            "description": f"{name.replace('_', ' ').title()} model",
            "framework": "scikit-learn",
            "task_type": "regression" if "performance" in name else "classification",
            "target_variable": "student_performance_score",
            "data_size": 1000,
            "features_count": len(model.get("features", [])),
            "training_time_minutes": 15.5,
            "cross_validation_folds": 5,
            "license": "MIT",
            "contact": "ai-system@university.edu"
        }
        
        # Export model package
        paths = exporter.export_model_package(model, metadata, name)
        exported_paths.append(paths)
        
        print(f"   ✅ JSON: {os.path.basename(paths['json'])}")
        print(f"   ✅ Pickle: {os.path.basename(paths['pickle'])}")
        print(f"   ✅ Metadata: {os.path.basename(paths['metadata'])}")
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 Export Summary")
    print("=" * 50)
    print(f"Total models exported: {len(models)}")
    print(f"Total files created: {len(exported_paths) * 3}")
    print(f"Output directory: {exporter.output_dir}")
    
    # List all exported models
    print("\n📁 Exported Files:")
    all_files = exporter.list_models()
    for file in sorted(all_files):
        print(f"   📄 {file}")
    
    print("\n✨ Model export completed successfully!")
    print("\nTo use these models in your application:")
    print("1. Load JSON models: json.load(open('filename.json'))")
    print("2. Load pickle models: pickle.load(open('filename.pkl', 'rb'))")
    print("3. Check metadata files for model information")

if __name__ == "__main__":
    main()