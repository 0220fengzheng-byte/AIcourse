import json
import pickle
import os
from typing import Any, Dict, List, Optional


class ModelExporter:
    """A utility class for exporting machine learning models in various formats."""
    
    def __init__(self, model_dir: str = "./models"):
        self.model_dir = model_dir
        os.makedirs(model_dir, exist_ok=True)
    
    def export_json(self, model_data: Dict[str, Any], filename: str) -> str:
        """Export model data as JSON file."""
        filepath = os.path.join(self.model_dir, f"{filename}.json")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(model_data, f, indent=2, ensure_ascii=False)
        return filepath
    
    def export_pickle(self, model: Any, filename: str) -> str:
        """Export model as pickle file."""
        filepath = os.path.join(self.model_dir, f"{filename}.pkl")
        with open(filepath, 'wb') as f:
            pickle.dump(model, f)
        return filepath
    
    def export_metadata(self, metadata: Dict[str, Any], filename: str) -> str:
        """Export model metadata as JSON."""
        filepath = os.path.join(self.model_dir, f"{filename}_metadata.json")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        return filepath
    
    def export_complete_model(self, model: Any, metadata: Dict[str, Any], 
                            base_filename: str) -> Dict[str, str]:
        """Export both model and metadata in multiple formats."""
        results = {}
        
        # Export model as pickle
        model_path = self.export_pickle(model, base_filename)
        results['model_path'] = model_path
        
        # Export metadata as JSON
        metadata_path = self.export_metadata(metadata, base_filename)
        results['metadata_path'] = metadata_path
        
        # Export combined data
        combined = {
            'model': str(type(model)),
            'metadata': metadata
        }
        combined_path = self.export_json(combined, f"{base_filename}_combined")
        results['combined_path'] = combined_path
        
        return results
    
    def list_models(self) -> List[str]:
        """List all exported models."""
        files = os.listdir(self.model_dir)
        return [f for f in files if f.endswith('.pkl') or f.endswith('.json')]
    
    def load_model(self, filename: str) -> Any:
        """Load a model from pickle file."""
        filepath = os.path.join(self.model_dir, filename)
        with open(filepath, 'rb') as f:
            return pickle.load(f)
    
    def load_metadata(self, filename: str) -> Dict[str, Any]:
        """Load metadata from JSON file."""
        filepath = os.path.join(self.model_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)


# Example usage and demo
if __name__ == "__main__":
    # Create a simple example model
    example_model = {
        'type': 'linear_regression',
        'weights': [0.5, 0.3, -0.2],
        'bias': 0.1,
        'features': ['age', 'income', 'education']
    }
    
    # Create exporter instance
    exporter = ModelExporter()
    
    # Export the model
    results = exporter.export_complete_model(
        model=example_model,
        metadata={
            'name': 'Student Performance Predictor',
            'version': '1.0',
            'accuracy': 0.85,
            'created_at': '2024-09-03',
            'description': 'Predicts student academic performance based on demographics'
        },
        base_filename='student_performance_model'
    )
    
    print("Model exported successfully!")
    print("Files created:")
    for key, path in results.items():
        print(f"  {key}: {path}")
    
    # List all models
    print("\nAvailable models:")
    for model in exporter.list_models():
        print(f"  - {model}")