import os
import sys
import shutil
import argparse
from pathlib import Path

def build_mac_app(checkpoints_dir="checkpoints"):
    """Build macOS app bundle with embedded checkpoints"""
    
    app_name = "SAM3D Objects"
    app_dir = Path(f"build/{app_name}.app")
    contents_dir = app_dir / "Contents"
    macos_dir = contents_dir / "MacOS"
    resources_dir = contents_dir / "Resources"
    
    print(f"Building {app_name} for macOS...")
    
    # Clean previous build
    if app_dir.exists():
        shutil.rmtree(app_dir)
        print(f"Cleaned previous build at {app_dir}")
    
    # Create app bundle structure
    os.makedirs(macos_dir, exist_ok=True)
    os.makedirs(resources_dir, exist_ok=True)
    print("Created app bundle structure")
    
    # Create Info.plist
    info_plist = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "https://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDisplayName</key>
    <string>{app_name}</string>
    <key>CFBundleExecutable</key>
    <string>main</string>
    <key>CFBundleIdentifier</key>
    <string>com.yourcompany.sam3dobjects</string>
    <key>CFBundleName</key>
    <string>{app_name}</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>LSMinimumSystemVersion</key>
    <string>10.15</string>
    <key>CFBundleDocumentTypes</key>
    <array>
        <dict>
            <key>CFBundleTypeExtensions</key>
            <array>
                <string>jpg</string>
                <string>jpeg</string>
                <string>png</string>
            </array>
            <key>CFBundleTypeName</key>
            <string>Image</string>
            <key>CFBundleTypeRole</key>
            <string>Viewer</string>
        </dict>
    </array>
</dict>
</plist>"""
    
    with open(contents_dir / "Info.plist", "w") as f:
        f.write(info_plist)
    print("Created Info.plist")
    
    # Copy main script
    shutil.copy("demo.py", macos_dir / "main")
    os.chmod(macos_dir / "main", 0o755)
    print("Copied demo.py to main executable")
    
    # Copy checkpoints
    checkpoints_src = Path(checkpoints_dir)
    checkpoints_dest = resources_dir / "checkpoints"
    if checkpoints_src.exists():
        shutil.copytree(checkpoints_src, checkpoints_dest)
        print(f"Copied checkpoints from {checkpoints_src} to {checkpoints_dest}")
        
        # Calculate checkpoints size
        total_size = sum(f.stat().st_size for f in checkpoints_src.rglob('*') if f.is_file())
        print(f"Checkpoints size: {total_size/(1024*1024):.1f} MB")
    else:
        print(f"Warning: Checkpoints directory {checkpoints_src} not found")
    
    # Copy requirements
    shutil.copy("requirements.txt", resources_dir)
    print("Copied requirements.txt")
    
    # Create a simple launcher script
    launcher_script = f"""#!/bin/bash
# SAM3D Objects Launcher
DIR="$( cd "$( dirname "${{BASH_SOURCE[0]}}" )" &> /dev/null && pwd )"
cd "$DIR/../Resources"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
    venv/bin/pip install -r requirements.txt
fi

# Run the app
venv/bin/python "$DIR/../MacOS/main" "$@"
"""
    
    with open(macos_dir / "launcher.sh", "w") as f:
        f.write(launcher_script)
    os.chmod(macos_dir / "launcher.sh", 0o755)
    print("Created launcher script")
    
    # Create DMG
    dmg_path = Path(f"build/{app_name}.dmg")
    if dmg_path.exists():
        os.remove(dmg_path)
    
    print("Creating DMG...")
    os.system(f"hdiutil create -volname \"{app_name}\" -srcfolder \"{app_dir}\" -ov -format UDZO \"{dmg_path}\"")
    
    # Calculate final app size
    app_size = sum(f.stat().st_size for f in app_dir.rglob('*') if f.is_file())
    dmg_size = dmg_path.stat().st_size if dmg_path.exists() else 0
    
    print(f"✅ macOS app built successfully!")
    print(f"   App bundle: {app_dir}")
    print(f"   App size: {app_size/(1024*1024):.1f} MB")
    print(f"   DMG file: {dmg_path}")
    print(f"   DMG size: {dmg_size/(1024*1024):.1f} MB")
    
    return dmg_path

def main():
    parser = argparse.ArgumentParser(description='Build macOS app for SAM3D Objects')
    parser.add_argument('--checkpoints-dir', type=str, default='checkpoints',
                        help='Path to SAM3D checkpoints directory')
    parser.add_argument('--app-name', type=str, default='SAM3D Objects',
                        help='Name of the macOS app')
    args = parser.parse_args()
    
    # Create build directory
    os.makedirs("build", exist_ok=True)
    
    # Build the app
    try:
        build_mac_app(args.checkpoints_dir)
        print("\n🎉 Build completed successfully!")
    except Exception as e:
        print(f"\n❌ Build failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
