# Distribution Guide for Expense Tracker

## 📦 How to Create an Executable for Users

This guide will help you package your Python Expense Tracker app into a standalone `.exe` file that users can download and run **without installing Python**.

---

## Prerequisites

1. **Install PyInstaller** (if not already installed):
   ```bash
   pip install pyinstaller
   ```

2. **Install all dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## Method 1: Using the Build Script (Recommended)

The easiest way to build your executable:

1. **Run the build script**:
   ```bash
   python build_exe.py
   ```

2. **Follow the prompts** - it will ask if you want to clean old builds

3. **Find your executable** in the `dist` folder:
   ```
   dist/ExpenseTracker.exe
   ```

---

## Method 2: Manual PyInstaller Command

If you prefer to run PyInstaller directly:

### Option A: Single File Executable (Recommended)
```bash
pyinstaller --name=ExpenseTracker --windowed --onefile --add-data="utils;utils" --collect-all=customtkinter --collect-all=tkcalendar --hidden-import=PIL._tkinter_finder --hidden-import=babel.numbers main.py
```

### Option B: Folder Distribution (Faster startup)
```bash
pyinstaller --name=ExpenseTracker --windowed --add-data="utils;utils" --collect-all=customtkinter --collect-all=tkcalendar --hidden-import=PIL._tkinter_finder --hidden-import=babel.numbers main.py
```

---

## 🎯 PyInstaller Options Explained

| Option | Description |
|--------|-------------|
| `--name=ExpenseTracker` | Name of the executable |
| `--windowed` | No console window (GUI only) |
| `--onefile` | Bundle everything into a single .exe |
| `--add-data="utils;utils"` | Include the utils folder |
| `--collect-all=customtkinter` | Include all CustomTkinter files |
| `--collect-all=tkcalendar` | Include all tkcalendar files |
| `--hidden-import=...` | Import modules that PyInstaller might miss |
| `--icon=icon.ico` | Add custom icon (optional) |

---

## 📤 Distributing to Users via GitHub

### Step 1: Create a GitHub Release

1. **Go to your GitHub repository**
2. **Click on "Releases"** (right sidebar)
3. **Click "Create a new release"**
4. **Fill in the details**:
   - **Tag version**: `v1.0.0` (or your version)
   - **Release title**: `Expense Tracker v1.0.0`
   - **Description**: Add features, screenshots, etc.

### Step 2: Upload the Executable

1. **Drag and drop** your `ExpenseTracker.exe` from the `dist` folder
2. **Optionally**, create a ZIP file with:
   - `ExpenseTracker.exe`
   - `README.md` (user guide)
   - `LICENSE` (if applicable)

### Step 3: Publish Release

1. Click **"Publish release"**
2. Users can now download the `.exe` from the releases page!

---

## 📥 How Users Download and Run

### For Users (No Python Required):

1. **Go to the GitHub Releases page**:
   ```
   https://github.com/YOUR_USERNAME/YOUR_REPO/releases
   ```

2. **Download** the latest `ExpenseTracker.exe`

3. **Run the executable**:
   - Double-click `ExpenseTracker.exe`
   - Windows might show a security warning (click "More info" → "Run anyway")

4. **That's it!** The app will create an `expenses.json` file in the same folder to store data.

---

## 🛡️ Windows Security Warning

When users first run the `.exe`, Windows Defender might show a warning because the app isn't signed. Users can:

1. Click **"More info"**
2. Click **"Run anyway"**

To avoid this (advanced):
- Sign your executable with a code signing certificate (costs money)
- Build reputation over time as more users download

---

## 🐛 Troubleshooting

### Build Issues

**Problem**: `ModuleNotFoundError` when running the .exe
- **Solution**: Add the missing module with `--hidden-import=module_name`

**Problem**: CustomTkinter theme not loading
- **Solution**: Use `--collect-all=customtkinter` flag

**Problem**: .exe is too large (>100MB)
- **Solution**: Use folder distribution instead of `--onefile`
- Or use UPX compression: `pip install pyinstaller[encryption]`

### Runtime Issues

**Problem**: App crashes on startup
- **Solution**: Run without `--windowed` to see error messages:
  ```bash
  pyinstaller --onefile --add-data="utils;utils" --collect-all=customtkinter main.py
  ```

**Problem**: Data not saving
- **Solution**: Ensure `expenses.json` has write permissions in the app directory

---

## 📊 File Size Optimization

Your executable will be around **50-100MB** due to CustomTkinter and matplotlib. To reduce size:

1. **Use folder distribution** instead of `--onefile`
2. **Remove unused imports** from your code
3. **Use UPX compression**:
   ```bash
   pip install pyinstaller[encryption]
   pyinstaller --onefile --upx-dir=/path/to/upx ...
   ```

---

## 🎨 Adding a Custom Icon (Optional)

1. **Create or download** a `.ico` file (256x256 recommended)
2. **Save it** as `icon.ico` in your project folder
3. **Add to PyInstaller command**:
   ```bash
   --icon=icon.ico
   ```

---

## 📝 Example GitHub Release Description

```markdown
# Expense Tracker v1.0.0

A beautiful, modern desktop expense tracker built with Python and CustomTkinter.

## ✨ Features
- 📊 Visual dashboard with charts
- 💰 Track expenses by category
- 📅 Date-based filtering
- 📈 Monthly spending trends
- 💾 Export to CSV
- 🌓 Dark/Light mode

## 📥 Download
Download `ExpenseTracker.exe` below and run it - no installation required!

## 🖥️ System Requirements
- Windows 10/11
- No Python installation needed

## 🚀 Quick Start
1. Download the .exe file
2. Double-click to run
3. Start tracking your expenses!

## 📸 Screenshots
[Add screenshots here]
```

---

## 🔄 Updating Your App

When you make changes:

1. **Update version** in your code
2. **Rebuild** the executable
3. **Create a new GitHub release** with the new version
4. Users download the latest version

---

## ✅ Checklist Before Release

- [ ] Test the .exe on a clean Windows machine
- [ ] Verify all features work
- [ ] Check file size is reasonable
- [ ] Create README for users
- [ ] Add screenshots to GitHub
- [ ] Write clear release notes
- [ ] Test on Windows 10 and 11
- [ ] Verify data persistence works

---

## 📚 Additional Resources

- [PyInstaller Documentation](https://pyinstaller.org/en/stable/)
- [GitHub Releases Guide](https://docs.github.com/en/repositories/releasing-projects-on-github)
- [Code Signing Info](https://learn.microsoft.com/en-us/windows/win32/seccrypto/cryptography-tools)

---

## 🆘 Need Help?

If you encounter issues:
1. Check the PyInstaller logs in the `build` folder
2. Run without `--windowed` to see console errors
3. Search PyInstaller issues on GitHub
4. Ask in Python communities (r/Python, Stack Overflow)
