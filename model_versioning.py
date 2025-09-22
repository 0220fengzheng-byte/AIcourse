#!/usr/bin/env python3
"""
Model Versioning System
Complete versioning system with semantic versioning, rollback, and change tracking
"""

import json
import os
import shutil
from datetime import datetime
from typing import Any, Dict, List, Optional
import hashlib

class ModelVersion:
    """Represents a single model version"""
    
    def __init__(self, version: str, model_data: Any, metadata: Dict[str, Any]):
        self.version = version
        self.model_data = model_data
        self.metadata = metadata
        self.created_at = datetime.now().isoformat()
        self.checksum = self._calculate_checksum()
    
    def _calculate_checksum(self) -> str:
        """Calculate checksum for model data"""
        data_str = json.dumps(self.model_data, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()[:16]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage"""
        return {
            'version': self.version,
            'created_at': self.created_at,
            'checksum': self.checksum,
            'metadata': self.metadata,
            'model_type': type(self.model_data).__name__
        }

class ModelVersioningSystem:
    """Complete model versioning system"""
    
    def __init__(self, base_dir: str = "./model_registry"):
        self.base_dir = base_dir
        self.registry_dir = os.path.join(base_dir, "registry")
        self.versions_dir = os.path.join(base_dir, "versions")
        self.current_version_file = os.path.join(base_dir, "current_version.json")
        
        os.makedirs(self.registry_dir, exist_ok=True)
        os.makedirs(self.versions_dir, exist_ok=True)
        
        self._init_registry()
    
    def _init_registry(self):
        """Initialize registry file"""
        registry_path = os.path.join(self.registry_dir, "registry.json")
        if not os.path.exists(registry_path):
            with open(registry_path, 'w') as f:
                json.dump({
                    'models': {},
                    'created_at': datetime.now().isoformat(),
                    'last_updated': datetime.now().isoformat()
                }, f, indent=2)
    
    def save_model(self, model_name: str, model_data: Any, 
                   metadata: Dict[str, Any], version: str = None) -> str:
        """Save a new model version"""
        
        # Auto-generate version if not provided
        if version is None:
            version = self._get_next_version(model_name)
        
        # Create model version
        model_version = ModelVersion(version, model_data, metadata)
        
        # Save model data
        model_path = os.path.join(self.versions_dir, f"{model_name}_{version}.json")
        with open(model_path, 'w') as f:
            json.dump({
                'model_data': model_data,
                'metadata': metadata,
                'version_info': model_version.to_dict()
            }, f, indent=2)
        
        # Update registry
        self._update_registry(model_name, model_version)
        
        # Update current version
        self._set_current_version(model_name, version)
        
        return version
    
    def load_model(self, model_name: str, version: str = None) -> Any:
        """Load model by name and version"""
        if version is None:
            version = self.get_current_version(model_name)
        
        model_path = os.path.join(self.versions_dir, f"{model_name}_{version}.json")
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model {model_name} version {version} not found")
        
        with open(model_path, 'r') as f:
            data = json.load(f)
        
        return data['model_data']
    
    def list_versions(self, model_name: str) -> List[Dict[str, Any]]:
        """List all versions of a model"""
        registry = self._get_registry()
        
        if model_name not in registry['models']:
            return []
        
        return registry['models'][model_name]['versions']
    
    def get_current_version(self, model_name: str) -> str:
        """Get current version of model"""
        try:
            with open(self.current_version_file, 'r') as f:
                current = json.load(f)
                return current.get(model_name, "1.0.0")
        except FileNotFoundError:
            return "1.0.0"
    
    def rollback(self, model_name: str, target_version: str) -> bool:
        """Rollback to a specific version"""
        versions = self.list_versions(model_name)
        
        for version_info in versions:
            if version_info['version'] == target_version:
                self._set_current_version(model_name, target_version)
                return True
        
        return False
    
    def compare_versions(self, model_name: str, version1: str, version2: str) -> Dict[str, Any]:
        """Compare two model versions"""
        model1 = self.load_model(model_name, version1)
        model2 = self.load_model(model_name, version2)
        
        registry = self._get_registry()
        info1 = next(v for v in registry['models'][model_name]['versions'] 
                    if v['version'] == version1)
        info2 = next(v for v in registry['models'][model_name]['versions'] 
                    if v['version'] == version2)
        
        return {
            'version1': version1,
            'version2': version2,
            'same_checksum': info1['checksum'] == info2['checksum'],
            'performance_comparison': self._compare_performance(model1, model2),
            'size_difference': len(str(model2)) - len(str(model1))
        }
    
    def _get_next_version(self, model_name: str) -> str:
        """Get next semantic version"""
        versions = self.list_versions(model_name)
        
        if not versions:
            return "1.0.0"
        
        latest = versions[-1]['version']
        major, minor, patch = map(int, latest.split('.'))
        return f"{major}.{minor}.{patch + 1}"
    
    def _get_registry(self) -> Dict[str, Any]:
        """Get registry data"""
        registry_path = os.path.join(self.registry_dir, "registry.json")
        with open(registry_path, 'r') as f:
            return json.load(f)
    
    def _update_registry(self, model_name: str, model_version: ModelVersion):
        """Update registry with new version"""
        registry = self._get_registry()
        
        if model_name not in registry['models']:
            registry['models'][model_name] = {
                'created_at': datetime.now().isoformat(),
                'versions': []
            }
        
        registry['models'][model_name]['versions'].append(model_version.to_dict())
        registry['last_updated'] = datetime.now().isoformat()
        
        registry_path = os.path.join(self.registry_dir, "registry.json")
        with open(registry_path, 'w') as f:
            json.dump(registry, f, indent=2)
    
    def _set_current_version(self, model_name: str, version: str):
        """Set current version for model"""
        current = {}
        if os.path.exists(self.current_version_file):
            with open(self.current_version_file, 'r') as f:
                current = json.load(f)
        
        current[model_name] = version
        
        with open(self.current_version_file, 'w') as f:
            json.dump(current, f, indent=2)
    
    def _compare_performance(self, model1: Any, model2: Any) -> Dict[str, Any]:
        """Compare model performance metrics"""
        perf1 = model1.get('performance', {}) if isinstance(model1, dict) else {}
        perf2 = model2.get('performance', {}) if isinstance(model2, dict) else {}
        
        return {
            'accuracy_improved': perf2.get('accuracy', 0) > perf1.get('accuracy', 0),
            'rmse_improved': perf2.get('rmse', float('inf')) < perf1.get('rmse', float('inf')),
            'r2_improved': perf2.get('r2_score', 0) > perf1.get('r2_score', 0)
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get registry statistics"""
        registry = self._get_registry()
        
        total_models = len(registry['models'])
        total_versions = sum(len(model['versions']) for model in registry['models'].values())
        
        return {
            'total_models': total_models,
            'total_versions': total_versions,
            'models': list(registry['models'].keys()),
            'created_at': registry['created_at'],
            'last_updated': registry['last_updated']
        }

def main():
    """Demonstrate the versioning system"""
    print("🔄 Model Versioning System")
    print("=" * 50)
    
    # Initialize versioning system
    versioning = ModelVersioningSystem()
    
    # Sample model evolution
    model_name = "student_performance_predictor"
    
    # Version 1.0.0 - Initial model
    model_v1 = {
        "model_type": "linear_regression",
        "coefficients": [0.7, 0.5, 0.3],
        "intercept": 10,
        "features": ["study_hours", "attendance", "sleep_hours"],
        "performance": {"accuracy": 0.75, "rmse": 15.2}
    }
    
    metadata_v1 = {
        "description": "Initial student performance model",
        "training_data": 1000,
        "features_engineered": 3
    }
    
    v1 = versioning.save_model(model_name, model_v1, metadata_v1)
    print(f"✅ Saved version {v1}")
    
    # Version 1.0.1 - Improved model
    model_v2 = model_v1.copy()
    model_v2["coefficients"] = [0.8, 0.6, 0.4]
    model_v2["performance"] = {"accuracy": 0.82, "rmse": 12.1}
    
    metadata_v2 = metadata_v1.copy()
    metadata_v2["description"] = "Improved model with better coefficients"
    
    v2 = versioning.save_model(model_name, model_v2, metadata_v2)
    print(f"✅ Saved version {v2}")
    
    # Version 1.1.0 - New features
    model_v3 = {
        "model_type": "linear_regression",
        "coefficients": [0.7, 0.6, 0.4, 0.3, 0.2],
        "intercept": 8,
        "features": ["study_hours", "attendance", "sleep_hours", "previous_grades", "participation"],
        "performance": {"accuracy": 0.87, "rmse": 10.5}
    }
    
    metadata_v3 = {
        "description": "Enhanced model with additional features",
        "training_data": 1500,
        "features_engineered": 5
    }
    
    v3 = versioning.save_model(model_name, model_v3, metadata_v3)
    print(f"✅ Saved version {v3}")
    
    # Display versions
    versions = versioning.list_versions(model_name)
    print(f"\n📋 All versions for {model_name}:")
    for version in versions:
        print(f"   {version['version']} - {version['created_at']}")
    
    # Statistics
    stats = versioning.get_statistics()
    print(f"\n📊 Registry Statistics:")
    print(f"   Total models: {stats['total_models']}")
    print(f"   Total versions: {stats['total_versions']}")
    print(f"   Last updated: {stats['last_updated']}")
    
    # Test rollback
    print(f"\n🔄 Testing rollback to {v2}...")
    versioning.rollback(model_name, v2)
    current = versioning.get_current_version(model_name)
    print(f"   Current version: {current}")

if __name__ == "__main__":
    main()