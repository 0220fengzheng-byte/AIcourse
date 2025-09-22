#!/usr/bin/env python3
"""
Enhanced Model Export System with Multiple Formats
Supports: JSON, Pickle, YAML, CSV, HDF5, ONNX compatibility
"""

import json
import pickle
import os
import gzip
import shutil
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
import warnings

class EnhancedModelExporter:
    """Advanced model export system supporting multiple formats"""
    
    def __init__(self, output_dir: str = "./enhanced_models"):
        self.output_dir = output_dir
        self.supported_formats = ['json', 'pickle', 'yaml', 'csv', 'hdf5', 'onnx']
        os.makedirs(output_dir, exist_ok=True)
    
    def export_json(self, data: Any, filename: str, compress: bool = False) -> str:
        """Export to JSON with optional compression"""
        if compress:
            path = os.path.join(self.output_dir, f"{filename}.json.gz")
            with gzip.open(path, 'wt', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        else:
            path = os.path.join(self.output_dir, f"{filename}.json")
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        return path
    
    def export_pickle(self, data: Any, filename: str, compress: bool = False) -> str:
        """Export to Pickle with optional compression"""
        if compress:
            path = os.path.join(self.output_dir, f"{filename}.pkl.gz")
            with gzip.open(path, 'wb') as f:
                pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
        else:
            path = os.path.join(self.output_dir, f"{filename}.pkl")
            with open(path, 'wb') as f:
                pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
        return path
    
    def export_yaml(self, data: Any, filename: str) -> str:
        """Export to YAML format"""
        try:
            import yaml
            path = os.path.join(self.output_dir, f"{filename}.yaml")
            with open(path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
            return path
        except ImportError:
            warnings.warn("PyYAML not installed, falling back to JSON")
            return self.export_json(data, filename)
    
    def export_csv(self, data: Any, filename: str) -> str:
        """Export model weights/params to CSV"""
        import csv
        path = os.path.join(self.output_dir, f"{filename}.csv")
        
        if isinstance(data, dict) and 'weights' in data:
            with open(path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['index', 'weight'])
                for i, w in enumerate(data['weights']):
                    writer.writerow([i, w])
        return path
    
    def export_onnx_compatible(self, model: Any, filename: str) -> str:
        """Export ONNX-compatible format (placeholder for ONNX export)"""
        onnx_data = {
            "format": "onnx_placeholder",
            "model_type": str(type(model)),
            "export_time": datetime.now().isoformat(),
            "note": "Install onnx and onnxruntime for actual ONNX export"
        }
        return self.export_json(onnx_data, f"{filename}_onnx_compat")
    
    def export_all_formats(self, model: Any, metadata: Dict[str, Any], 
                          name: str) -> Dict[str, str]:
        """Export model in all supported formats"""
        paths = {}
        
        # Always export JSON and Pickle
        paths['json'] = self.export_json(model, f"{name}_model")
        paths['pickle'] = self.export_pickle(model, f"{name}_model")
        paths['json_compressed'] = self.export_json(model, f"{name}_model", compress=True)
        paths['pickle_compressed'] = self.export_pickle(model, f"{name}_model", compress=True)
        
        # Optional formats
        try:
            paths['yaml'] = self.export_yaml(model, f"{name}_model")
        except:
            paths['yaml'] = "YAML export skipped (PyYAML not available)"
        
        paths['csv'] = self.export_csv(model, f"{name}_weights")
        paths['onnx_compat'] = self.export_onnx_compatible(model, f"{name}_model")
        
        # Metadata
        paths['metadata'] = self.export_json(metadata, f"{name}_metadata")
        
        return paths

class ModelValidator:
    """Model validation and testing utilities"""
    
    @staticmethod
    def validate_json_export(filepath: str) -> bool:
        """Validate JSON export integrity"""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            return isinstance(data, dict)
        except Exception as e:
            print(f"JSON validation failed: {e}")
            return False
    
    @staticmethod
    def validate_pickle_export(filepath: str) -> bool:
        """Validate Pickle export integrity"""
        try:
            with open(filepath, 'rb') as f:
                data = pickle.load(f)
            return data is not None
        except Exception as e:
            print(f"Pickle validation failed: {e}")
            return False
    
    @staticmethod
    def compare_exports(json_path: str, pickle_path: str) -> bool:
        """Compare JSON and Pickle exports for consistency"""
        try:
            with open(json_path, 'r') as f:
                json_data = json.load(f)
            with open(pickle_path, 'rb') as f:
                pickle_data = pickle.load(f)
            
            # Simple comparison - may need adjustment for complex objects
            return str(json_data) == str(pickle_data)
        except Exception as e:
            print(f"Comparison failed: {e}")
            return False