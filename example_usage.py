from model_exporter import ModelExporter
import numpy as np


def create_sample_models():
    """Create various sample models for demonstration."""
    
    # Sample 1: Simple linear regression
    linear_model = {
        'type': 'linear_regression',
        'coefficients': [2.5, -1.3, 0.7],
        'intercept': 3.2,
        'features': ['study_hours', 'attendance_rate', 'previous_grade']
    }
    
    # Sample 2: Decision tree
    tree_model = {
        'type': 'decision_tree',
        'max_depth': 5,
        'min_samples_split': 10,
        'feature_importance': {
            'study_hours': 0.6,
            'attendance_rate': 0.3,
            'previous_grade': 0.1
        }
    }
    
    # Sample 3: Neural network
    nn_model = {
        'type': 'neural_network',
        'architecture': [10, 20, 15, 1],
        'activation': 'relu',
        'optimizer': 'adam',
        'weights': [np.random.randn(10, 20), np.random.randn(20, 15), np.random.randn(15, 1)]
    }
    
    return [
        ('linear_regression', linear_model),
        ('decision_tree', tree_model),
        ('neural_network', nn_model)
    ]


def main():
    """Demonstrate model export functionality."""
    
    # Initialize exporter
    exporter = ModelExporter()
    
    # Create sample models
    models = create_sample_models()
    
    print("Starting model export demonstration...")
    
    for name, model in models:
        print(f"\nExporting {name}...")
        
        # Create metadata
        metadata = {
            'model_name': name,
            'version': '1.0.0',
            'created_date': '2024-09-03',
            'framework': 'custom',
            'accuracy': np.random.uniform(0.7, 0.95),
            'description': f'{name} model for student performance prediction'
        }
        
        # Export model
        results = exporter.export_complete_model(
            model=model,
            metadata=metadata,
            base_filename=f'{name}_model'
        )
        
        print(f"  ✅ Model exported: {results['model_path']}")
        print(f"  ✅ Metadata exported: {results['metadata_path']}")
        print(f"  ✅ Combined info: {results['combined_path']}")
    
    # List all exported models
    print("\n" + "="*50)
    print("All exported models:")
    print("="*50)
    
    for model_file in exporter.list_models():
        print(f"  📁 {model_file}")
    
    # Demonstrate loading
    print("\n" + "="*50)
    print("Loading a saved model...")
    print("="*50)
    
    try:
        loaded_model = exporter.load_model('linear_regression_model.pkl')
        loaded_metadata = exporter.load_metadata('linear_regression_model_metadata.json')
        
        print("✅ Successfully loaded:")
        print(f"  Model type: {loaded_model.get('type', 'Unknown')}")
        print(f"  Features: {loaded_model.get('features', [])}")
        print(f"  Metadata version: {loaded_metadata.get('version', 'Unknown')}")
        
    except Exception as e:
        print(f"❌ Error loading model: {e}")


if __name__ == "__main__":
    main()