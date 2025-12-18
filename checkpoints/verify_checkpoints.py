import os
from pathlib import Path

def verify_sam3d_checkpoints(checkpoints_dir="checkpoints"):
    """Verify all required SAM3D model files are present"""
    
    checkpoints_path = Path(checkpoints_dir)
    required_files = []
    missing_files = []
    
    print("=== SAM3D Checkpoint Verification ===")
    print(f"Checkpoints directory: {checkpoints_path.absolute()}")
    print(f"Directory exists: {checkpoints_path.exists()}")
    
    if not checkpoints_path.exists():
        print(f"❌ Checkpoints directory does not exist!")
        return False
    
    # Check for HuggingFace format
    hf_dir = checkpoints_path / "hf"
    if hf_dir.exists():
        print(f"\n📁 Found HuggingFace directory: {hf_dir}")
        required_hf_files = [
            "pipeline.yaml",
            "config.json",
            "model.safetensors"  # or .bin, .pth
        ]
        
        for file in required_hf_files:
            file_path = hf_dir / file
            if file_path.exists():
                required_files.append(str(file_path))
                size = file_path.stat().st_size / (1024*1024)
                print(f"  ✅ {file} ({size:.1f} MB)")
            else:
                missing_files.append(str(file_path))
                print(f"  ❌ {file} (missing)")
    
    # Check for PyTorch format
    pth_files = list(checkpoints_path.glob("*.pth"))
    if pth_files:
        print(f"\n📁 Found PyTorch files:")
        for pth_file in pth_files:
            required_files.append(str(pth_file))
            size = pth_file.stat().st_size / (1024*1024)
            print(f"  ✅ {pth_file.name} ({size:.1f} MB)")
    
    # Check total size
    total_size = 0
    for file in checkpoints_path.rglob("*"):
        if file.is_file():
            total_size += file.stat().st_size
    
    print(f"\n📊 Total checkpoints size: {total_size/(1024*1024):.1f} MB")
    
    if missing_files:
        print(f"\n❌ Missing {len(missing_files)} required files:")
        for file in missing_files:
            print(f"  - {file}")
        return False
    elif required_files:
        print(f"\n🎉 Found {len(required_files)} required files!")
        return True
    else:
        print(f"\n⚠️  No model files found in {checkpoints_dir}")
        return False

if __name__ == "__main__":
    success = verify_sam3d_checkpoints()
    if not success:
        print("\nPlease download the SAM3D model files first!")
        exit(1)
