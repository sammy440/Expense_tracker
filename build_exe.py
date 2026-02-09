"""
Build script for creating executable using PyInstaller
Run this script to build the Expense Tracker executable
"""
import os
import sys
import subprocess
import shutil

def clean_build_folders():
    """Remove old build artifacts"""
    folders_to_remove = ['build', 'dist', '__pycache__']
    for folder in folders_to_remove:
        if os.path.exists(folder):
            print(f"Removing {folder}...")
            shutil.rmtree(folder)
    
    # Remove spec file if exists
    if os.path.exists('ExpenseTracker.spec'):
        os.remove('ExpenseTracker.spec')

def build_executable():
    """Build the executable using PyInstaller"""
    print("Building Expense Tracker executable...")
    
    # PyInstaller command
    cmd = [
        'pyinstaller',
        '--name=ExpenseTracker',
        '--windowed',  # No console window
        '--onefile',   # Single executable file
        '--icon=NONE',  # Add your icon path here if you have one
        '--add-data=utils;utils',  # Include utils folder
        '--hidden-import=PIL._tkinter_finder',
        '--hidden-import=babel.numbers',
        '--collect-all=customtkinter',
        '--collect-all=tkcalendar',
        'main.py'
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("\n✅ Build successful!")
        print(f"📦 Executable location: {os.path.join(os.getcwd(), 'dist', 'ExpenseTracker.exe')}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Build failed: {e}")
        return False
    except FileNotFoundError:
        print("\n❌ PyInstaller not found. Please install it using:")
        print("   pip install pyinstaller")
        return False

def main():
    print("=" * 60)
    print("Expense Tracker - Build Script")
    print("=" * 60)
    
    # Ask user if they want to clean old builds
    clean = input("\nClean old build files? (y/n): ").lower().strip()
    if clean == 'y':
        clean_build_folders()
    
    # Build
    if build_executable():
        print("\n" + "=" * 60)
        print("Next steps:")
        print("1. Test the executable in the 'dist' folder")
        print("2. Distribute the .exe file to users")
        print("3. Users can run it without Python installed!")
        print("=" * 60)

if __name__ == "__main__":
    main()
