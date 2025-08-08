# build_executable.py - Script to build Windows executable

import os
import sys
import subprocess
import shutil

def build_executable():
    """Build Windows executable using PyInstaller"""
    
    print("Building Telegram Bot Desktop Application...")
    print("=" * 50)
    
    # Check if required files exist
    required_files = [
        "desktop_app.py",
        "bot.py", 
        "config.py",
        "responses.json"
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ Required file missing: {file}")
            return False
    
    print("✅ All required files found")
    
    # Create build directory structure
    os.makedirs("build_files", exist_ok=True)
    os.makedirs("dist", exist_ok=True)
    
    # Copy required files
    files_to_copy = [
        "desktop_app.py",
        "bot.py",
        "config.py", 
        "responses.json"
    ]
    
    for file in files_to_copy:
        shutil.copy2(file, "build_files/")
        print(f"📁 Copied: {file}")
    
    # Create .env template if it doesn't exist
    env_file = "build_files/.env"
    if not os.path.exists(env_file):
        with open(env_file, 'w') as f:
            f.write("""# Telegram API Configuration
API_ID=your_api_id_here
API_HASH=your_api_hash_here
PHONE=your_phone_number_here

# Flask Settings  
SECRET_KEY=your_secret_key_here
DEBUG=False
""")
        print("📄 Created .env template")
    
    # PyInstaller command
    pyinstaller_cmd = [
        "pyinstaller",
        "--onefile",  # Single executable file
        "--windowed",  # Hide console window
        "--name=TelegramBotManager",
        "--icon=icon.ico",  # You can add custom icon
        "--add-data=responses.json;.",
        "--add-data=.env;.",
        "--add-data=media;media",
        "--hidden-import=PIL._tkinter_finder",
        "--hidden-import=pystray",
        "--hidden-import=telethon",
        "--hidden-import=nltk",
        "--hidden-import=sklearn",
        "--distpath=dist",
        "--workpath=build_temp",
        "desktop_app.py"
    ]
    
    try:
        print("\n🔨 Building executable with PyInstaller...")
        result = subprocess.run(pyinstaller_cmd, check=True, capture_output=True, text=True)
        print("✅ Build successful!")
        
        # Create installation package structure
        install_dir = "TelegramBotManager_Portable"
        os.makedirs(install_dir, exist_ok=True)
        
        # Copy executable
        shutil.copy2("dist/TelegramBotManager.exe", install_dir + "/")
        
        # Copy required directories
        os.makedirs(install_dir + "/media", exist_ok=True)
        os.makedirs(install_dir + "/media/images", exist_ok=True) 
        os.makedirs(install_dir + "/media/audio", exist_ok=True)
        
        # Copy configuration files
        shutil.copy2("responses.json", install_dir + "/")
        shutil.copy2("build_files/.env", install_dir + "/")
        
        # Create README
        create_readme(install_dir)
        
        # Create batch file for easy running
        create_run_bat(install_dir)
        
        print(f"\n🎉 Installation package created: {install_dir}/")
        print("📁 Package contents:")
        for root, dirs, files in os.walk(install_dir):
            level = root.replace(install_dir, '').count(os.sep)
            indent = ' ' * 2 * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 2 * (level + 1)
            for file in files:
                print(f"{subindent}{file}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        print("Error output:", e.stderr)
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def create_readme(install_dir):
    """Create README file for the installation"""
    readme_content = """# Telegram Bot Manager - Desktop Application

## Quick Start

1. **Configure API Settings:**
   - Open the `.env` file in a text editor
   - Replace placeholder values with your actual Telegram API credentials:
     - API_ID: Get from https://my.telegram.org
     - API_HASH: Get from https://my.telegram.org  
     - PHONE: Your phone number with country code (e.g., +1234567890)

2. **Run the Application:**
   - Double-click `TelegramBotManager.exe`
   - OR run `start.bat` for easier launching

3. **First Time Setup:**
   - Go to Settings tab and verify your API configuration
   - Start the bot from the Bot Control tab
   - You may need to enter a verification code sent to your phone

## Features

### 🤖 Bot Control
- Start/Stop your Telegram bot
- Real-time status monitoring
- Configuration validation

### 💬 Response Management  
- Add, edit, and delete bot responses
- Support for text, image, and audio responses
- Visual response preview

### 📁 Media Management
- Upload images and audio files
- File size and type information
- Easy media deletion

### 📨 Live Message Monitoring
- Real-time message log
- See incoming and outgoing messages
- Export conversation logs

### ⚙️ Settings & Configuration
- API credentials management
- Auto-start options
- System tray integration

## Troubleshooting

### Bot Won't Start
1. Check API credentials in `.env` file
2. Ensure phone number includes country code
3. Verify internet connection
4. Check firewall settings

### Messages Not Appearing
1. Confirm bot is running (green status)
2. Check that responses.json has valid entries
3. Verify media files exist in media/ folders

### System Tray Issues
- If minimize to tray doesn't work, disable the option in Settings
- Some antivirus software may block system tray access

## File Structure

```
TelegramBotManager/
├── TelegramBotManager.exe    # Main application
├── .env                      # Configuration file
├── responses.json            # Bot responses database
├── start.bat                # Easy launcher
├── media/
│   ├── images/              # Image files for bot
│   └── audio/               # Audio files for bot
└── README.txt               # This file
```

## Support

For issues or questions:
1. Check the Live Messages tab for error details
2. Review the bot.log file for technical errors
3. Ensure all requirements are met

## Security Note

Keep your API credentials secure and never share your .env file.
"""
    
    with open(os.path.join(install_dir, "README.txt"), 'w', encoding='utf-8') as f:
        f.write(readme_content)

def create_run_bat(install_dir):
    """Create batch file for easy running"""
    bat_content = """@echo off
title Telegram Bot Manager
echo Starting Telegram Bot Manager...
echo.

TelegramBotManager.exe

if errorlevel 1 (
    echo.
    echo Error: Application failed to start
    echo Check your configuration and try again
    echo.
    pause
)
"""
    
    with open(os.path.join(install_dir, "start.bat"), 'w') as f:
        f.write(bat_content)

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements_desktop.txt"], check=True)
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

if __name__ == "__main__":
    print("Telegram Bot Manager - Executable Builder")
    print("=" * 50)
    
    # Install requirements first
    if not install_requirements():
        input("Press Enter to exit...")
        sys.exit(1)
    
    # Build executable
    if build_executable():
        print("\n🎉 Build completed successfully!")
        print("\nNext steps:")
        print("1. Configure the .env file in TelegramBotManager_Portable/")
        print("2. Run TelegramBotManager.exe to start the application")
        input("\nPress Enter to exit...")
    else:
        print("\n❌ Build failed. Please check the errors above.")
        input("Press Enter to exit...")