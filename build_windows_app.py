import os
import sys
import shutil
import argparse
from pathlib import Path
import PyInstaller.__main__

def build_windows_app(checkpoints_dir="checkpoints"):
    """Build Windows executable with embedded checkpoints"""
    
    app_name = "SAM3D_Objects"
    
    print(f"Building {app_name} for Windows...")
    
    # Clean previous build
    build_dir = Path("build")
    if build_dir.exists():
        shutil.rmtree(build_dir)
    
    # Build with PyInstaller
    PyInstaller.__main__.run([
        'demo.py',
        '--name=' + app_name,
        '--windowed',
        f'--add-data={checkpoints_dir};checkpoints',
        '--add-data=requirements.txt;.',
        '--onefile',
        '--distpath=build',
        '--workpath=build/temp',
        '--specpath=build'
    ])
    
    # Check if executable was created
    exe_path = Path(f"build/{app_name}.exe")
    if exe_path.exists():
        size = exe_path.stat().st_size / (1024*1024)
        print(f"✅ Windows app built successfully!")
        print(f"   Executable: {exe_path}")
        print(f"   Size: {size:.1f} MB")
        return exe_path
    else:
        print("❌ Windows build failed - executable not found")
        return None

def main():
    parser = argparse.ArgumentParser(description='Build Windows app for SAM3D Objects')
    parser.add_argument('--checkpoints-dir', type=str, default='checkpoints',
                        help='Path to SAM3D checkpoints directory')
    args = parser.parse_args()
    
    try:
        build_windows_app(args.checkpoints_dir)
        print("\n🎉 Build completed successfully!")
    except Exception as e:
        print(f"\n❌ Build failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
