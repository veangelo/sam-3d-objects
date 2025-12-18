import os
import sys
import argparse
from pathlib import Path

def find_model_files(checkpoints_dir="checkpoints"):
    """Find available model files in checkpoints directory"""
    
    checkpoints_path = Path(checkpoints_dir)
    
    # Check for HuggingFace format
    hf_dir = checkpoints_path / "hf"
    if hf_dir.exists():
        pipeline_file = hf_dir / "pipeline.yaml"
        model_files = list(hf_dir.glob("*.safetensors")) + list(hf_dir.glob("*.bin")) + list(hf_dir.glob("*.pth"))
        
        if pipeline_file.exists() and model_files:
            return {
                "format": "hf",
                "pipeline": str(pipeline_file),
                "model": str(model_files[0]),
                "config": str(hf_dir / "config.json") if (hf_dir / "config.json").exists() else None
            }
    
    # Check for PyTorch format
    pth_files = list(checkpoints_path.glob("*.pth"))
    if pth_files:
        return {
            "format": "pytorch",
            "model": str(pth_files[0])
        }
    
    return None

def load_sam3d_model(model_info):
    """Load SAM3D model based on available files"""
    
    if model_info["format"] == "hf":
        print(f"Loading SAM3D model from HuggingFace format...")
        print(f"  Pipeline: {model_info['pipeline']}")
        print(f"  Model: {model_info['model']}")
        
        # Your HuggingFace model loading code here
        try:
            from transformers import pipeline
            model = pipeline("image-segmentation", model=model_info['model'])
            return model
        except Exception as e:
            print(f"Error loading HuggingFace model: {e}")
            return None
    
    elif model_info["format"] == "pytorch":
        print(f"Loading SAM3D model from PyTorch format...")
        print(f"  Model: {model_info['model']}")
        
        # Your PyTorch model loading code here
        try:
            import torch
            model = torch.load(model_info['model'], map_location='cpu')
            return model
        except Exception as e:
            print(f"Error loading PyTorch model: {e}")
            return None
    
    return None

def main():
    parser = argparse.ArgumentParser(description='SAM3D Demo')
    parser.add_argument('--checkpoints-dir', type=str, default='checkpoints',
                        help='Path to SAM3D checkpoints directory')
    args = parser.parse_args()
    
    # Find model files
    model_info = find_model_files(args.checkpoints_dir)
    
    if not model_info:
        print(f"❌ No valid model files found in {args.checkpoints_dir}")
        print("Please ensure you have downloaded the SAM3D checkpoints.")
        sys.exit(1)
    
    # Load model
    model = load_sam3d_model(model_info)
    
    if model is None:
        print("❌ Failed to load SAM3D model")
        sys.exit(1)
    
    print("✅ SAM3D model loaded successfully!")
    
    # Your demo code here
    print("🚀 Running SAM3D demo...")
    
    # Example usage
    # results = model.process_image("example.jpg")
    # print(f"Found {len(results)} objects")

if __name__ == "__main__":
    main()
