#!/usr/bin/env python3
"""
Model Validation and Testing System
Comprehensive validation for exported models
"""

import json
import pickle
import os
import hashlib
from typing import Any, Dict, List, Tuple
import numpy as np

class ModelValidator:
    """Comprehensive model validation system"""
    
    def __init__(self, models_dir: str = "./enhanced_models"):
        self.models_dir = models_dir
    
    def validate_json_integrity(self, filepath: str) -> Dict[str, Any]:
        """Validate JSON file structure and content"""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            validation_result = {
                'valid': True,
                'file_size': os.path.getsize(filepath),
                'content_type': type(data).__name__,
                'keys_count': len(data) if isinstance(data, dict) else 0,
                'structure_check': self._check_model_structure(data),
                'checksum': self._calculate_checksum(filepath)
            }
            return validation_result
        except Exception as e:
            return {'valid': False, 'error': str(e)}
    
    def validate_pickle_integrity(self, filepath: str) -> Dict[str, Any]:
        """Validate Pickle file integrity"""
        try:
            with open(filepath, 'rb') as f:
                data = pickle.load(f)
            
            validation_result = {
                'valid': True,
                'file_size': os.path.getsize(filepath),
                'content_type': type(data).__name__,
                'structure_check': self._check_model_structure(data),
                'checksum': self._calculate_checksum(filepath)
            }
            return validation_result
        except Exception as e:
            return {'valid': False, 'error': str(e)}
    
    def _check_model_structure(self, model: Any) -> Dict[str, bool]:
        """Check common model structure elements"""
        checks = {}
        
        if isinstance(model, dict):
            # Common model keys
            checks['has_model_type'] = 'model_type' in model
            checks['has_weights'] = any(key in model for key in ['weights', 'coefficients', 'parameters'])
            checks['has_features'] = 'features' in model
            checks['has_algorithm'] = 'algorithm' in model
            checks['has_performance'] = any(key in model for key in ['accuracy', 'performance', 'rmse'])
        
        return checks
    
    def _calculate_checksum(self, filepath: str) -> str:
        """Calculate MD5 checksum of file"""
        hash_md5 = hashlib.md5()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def compare_model_versions(self, model1_path: str, model2_path: str) -> Dict[str, Any]:
        """Compare two model versions"""
        try:
            # Load both models
            with open(model1_path, 'r') as f:
                model1 = json.load(f)
            with open(model2_path, 'r') as f:
                model2 = json.load(f)
            
            comparison = {
                'same_type': model1.get('model_type') == model2.get('model_type'),
                'same_features': model1.get('features') == model2.get('features'),
                'performance_improved': self._compare_performance(model1, model2),
                'size_difference': os.path.getsize(model2_path) - os.path.getsize(model1_path)
            }
            return comparison
        except Exception as e:
            return {'error': str(e)}
    
    def _compare_performance(self, model1: Dict, model2: Dict) -> bool:
        """Compare performance metrics between models"""
        perf1 = model1.get('performance', {})
        perf2 = model2.get('performance', {})
        
        if 'accuracy' in perf1 and 'accuracy' in perf2:
            return perf2['accuracy'] > perf1['accuracy']
        elif 'rmse' in perf1 and 'rmse' in perf2:
            return perf2['rmse'] < perf1['rmse']
        
        return False
    
    def run_validation_suite(self) -> Dict[str, Any]:
        """Run complete validation suite on all models"""
        results = {
            'json_models': [],
            'pickle_models': [],
            'summary': {}
        }
        
        # Find all model files
        json_files = [f for f in os.listdir(self.models_dir) if f.endswith('.json')]
        pkl_files = [f for f in os.listdir(self.models_dir) if f.endswith('.pkl')]
        
        # Validate JSON files
        for file in json_files:
            filepath = os.path.join(self.models_dir, file)
            validation = self.validate_json_integrity(filepath)
            validation['filename'] = file
            results['json_models'].append(validation)
        
        # Validate Pickle files
        for file in pkl_files:
            filepath = os.path.join(self.models_dir, file)
            validation = self.validate_pickle_integrity(filepath)
            validation['filename'] = file
            results['pickle_models'].append(validation)
        
        # Summary
        valid_json = sum(1 for v in results['json_models'] if v['valid'])
        valid_pkl = sum(1 for v in results['pickle_models'] if v['valid'])
        
        results['summary'] = {
            'total_models': len(json_files) + len(pkl_files),
            'valid_models': valid_json + valid_pkl,
            'invalid_models': (len(json_files) + len(pkl_files)) - (valid_json + valid_pkl),
            'validation_rate': (valid_json + valid_pkl) / max(1, len(json_files) + len(pkl_files))
        }
        
        return results

class ModelTester:
    """Test model predictions and functionality"""
    
    def __init__(self):
        self.test_cases = self._generate_test_cases()
    
    def _generate_test_cases(self) -> List[Dict[str, Any]]:
        """Generate test cases for model prediction"""
        return [
            {
                'name': 'high_performer',
                'features': {'study_hours': 30, 'attendance': 95, 'sleep_hours': 8},
                'expected_range': (85, 100)
            },
            {
                'name': 'average_performer',
                'features': {'study_hours': 15, 'attendance': 75, 'sleep_hours': 7},
                'expected_range': (60, 80)
            },
            {
                'name': 'low_performer',
                'features': {'study_hours': 5, 'attendance': 50, 'sleep_hours': 5},
                'expected_range': (30, 50)
            }
        ]
    
    def test_model_predictions(self, model: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Test model predictions with test cases"""
        results = []
        
        for test_case in self.test_cases:
            try:
                prediction = self._predict_with_model(model, test_case['features'])
                result = {
                    'test_case': test_case['name'],
                    'prediction': prediction,
                    'expected_range': test_case['expected_range'],
                    'within_range': test_case['expected_range'][0] <= prediction <= test_case['expected_range'][1],
                    'status': 'success'
                }
            except Exception as e:
                result = {
                    'test_case': test_case['name'],
                    'status': 'failed',
                    'error': str(e)
                }
            
            results.append(result)
        
        return results
    
    def _predict_with_model(self, model: Dict[str, Any], features: Dict[str, float]) -> float:
        """Make prediction using model"""
        if model.get('model_type') == 'linear_regression':
            coefficients = model.get('coefficients', [1, 1, 1])
            intercept = model.get('intercept', 0)
            
            feature_values = [features.get(f, 0) for f in model.get('features', ['study_hours', 'attendance', 'sleep_hours'])]
            
            prediction = intercept + sum(c * v for c, v in zip(coefficients, feature_values))
            return max(0, min(100, prediction))  # Clamp between 0-100
        
        return 75  # Default fallback

def main():
    """Run validation and testing suite"""
    print("🔍 Model Validation and Testing System")
    print("=" * 50)
    
    # Initialize validator
    validator = ModelValidator()
    tester = ModelTester()
    
    # Run validation
    validation_results = validator.run_validation_suite()
    
    print(f"📊 Validation Results:")
    print(f"   Total models: {validation_results['summary']['total_models']}")
    print(f"   Valid models: {validation_results['summary']['valid_models']}")
    print(f"   Validation rate: {validation_results['summary']['validation_rate']:.2%}")
    
    # Test specific model
    test_model = {
        'model_type': 'linear_regression',
        'coefficients': [2.5, 0.8, 1.2],
        'intercept': 10,
        'features': ['study_hours', 'attendance', 'sleep_hours']
    }
    
    test_results = tester.test_model_predictions(test_model)
    
    print(f"\n🧪 Model Testing Results:")
    for result in test_results:
        if result['status'] == 'success':
            print(f"   {result['test_case']}: {result['prediction']:.1f} ")
            print(f"      Expected: {result['expected_range']}")
            print(f"      Status: {'✅ PASS' if result['within_range'] else '❌ FAIL'}")
        else:
            print(f"   {result['test_case']}: {result['status']} - {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    main()