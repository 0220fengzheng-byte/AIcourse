import json
import pickle
import os

class ModelExport:
    def __init__(self, output_dir="models"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def export_model(self, model, name):
        """Export model to pickle file"""
        path = os.path.join(self.output_dir, f"{name}.pkl")
        with open(path, 'wb') as f:
            pickle.dump(model, f)
        return path
    
    def export_config(self, config, name):
        """Export configuration to JSON"""
        path = os.path.join(self.output_dir, f"{name}.json")
        with open(path, 'w') as f:
            json.dump(config, f, indent=2)
        return path

# Example usage
if __name__ == "__main__":
    # Sample model
    sample_model = {
        'type': 'regression',
        'weights': [0.1, 0.2, 0.3],
        'bias': 0.5
    }
    
    # Sample config
    config = {
        'model_name': 'student_predictor',
        'version': '1.0',
        'accuracy': 0.85
    }
    
    # Export
    exporter = ModelExport()
    model_path = exporter.export_model(sample_model, 'my_model')
    config_path = exporter.export_config(config, 'my_model_config')
    
    print(f"Model exported to: {model_path}")
    print(f"Config exported to: {config_path}")