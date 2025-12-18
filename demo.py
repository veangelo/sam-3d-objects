import os
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description='SAM3D Demo')
    parser.add_argument('--model-path', type=str, default='checkpoints/hf/',
                        help='Path to SAM3D model files')
    args = parser.parse_args()
    
    model_path = Path(args.model_path)
    
    # Verify model files exist
    pipeline_file = model_path / "pipeline.yaml"
    model_file = model_path / "sam3d_large.safetensors"  # Adjust filename
    
    if not pipeline_file.exists():
        raise FileNotFoundError(f"Pipeline file not found at {pipeline_file}")
    
    if not model_file.exists():
        raise FileNotFoundError(f"Model file not found at {model_file}")
    
    # Load and run SAM3D model
    print(f"Loading SAM3D model from {model_path}")
    # Your SAM3D loading code here
    
    print("SAM3D demo running successfully!")

if __name__ == "__main__":
    main()
