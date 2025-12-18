import os
from pathlib import Path

def verify_sam3d_checkpoints(checkpoints_dir="checkpoints"):
    """Verify all required SAM3D model files are present"""
    
    checkpoints_path = Path(checkpoints_dir)
    required_files = []
    missing_files = []
    
    # Check for HuggingFace format
    hf_dir = checkpoints_path / "hf"
    if hf_dir.exists():
        required_hf_files = [
            "pipeline.yaml",
            "config.json",
            "model.safetensors"  # or .bin, .pth
        ]
        
        for file in required_hf_files:
            file_path = hf_dir / file
            if file_path.exists():
                required_files.append(str(file_path))
            else:
                missing_files.append(str(file_path))
    
    # Check for PyTorch format
    pth_files = list(checkpoints_path.glob("*.pth"))
    if pth_files:
        required_files.extend([str(f) for f in pth_files])
    
    # Print results
    print("=== SAM3D Checkpoint Verification ===")
    print(f"Checkpoints directory: {checkpoints_path.absolute()}")
    print(f"Directory exists: {checkpoints_path.exists()}")
    
    if required_files:
        print(f"\n✅ Found {len(required_files)} required files:")
        for file in required_files:
            size = os.path.getsize(file) / (1024*1024)  # MB
            print(f"  - {file} ({size:.1f} MB)")
    
    if missing_files:
        print(f"\n❌ Missing {len(missing_files)} required files:")
        for file in missing_files:
            print(f"  - {file}")
    
    # Check total size
    total_size = 0
    for file in checkpoints_path.rglob("*"):
        if file.is_file():
            total_size += file.stat().st_size
    
    print(f"\n📊 Total checkpoints size: {total_size/(1024*1024):.1f} MB")
    
    return len(missing_files) == 0

if __name__ == "__main__":
    success = verify_sam3d_checkpoints()
    if success:
        print("\n🎉 All required files are present!")
    else:
        print("\n⚠️  Some files are missing. Please download them first.")
