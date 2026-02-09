# 🚀 Quick Reference: Building & Distributing Your Expense Tracker

## Step-by-Step Guide

### 1️⃣ Install PyInstaller
```bash
pip install pyinstaller
```

### 2️⃣ Build the Executable
```bash
python build_exe.py
```
OR manually:
```bash
pyinstaller --name=ExpenseTracker --windowed --onefile --add-data="utils;utils" --collect-all=customtkinter --collect-all=tkcalendar main.py
```

### 3️⃣ Test the Executable
```bash
cd dist
./ExpenseTracker.exe
```

### 4️⃣ Create GitHub Release

1. Go to your repo → **Releases** → **Create a new release**
2. Tag: `v1.0.0`
3. Title: `Expense Tracker v1.0.0`
4. Upload `dist/ExpenseTracker.exe`
5. Click **Publish release**

### 5️⃣ Share with Users

Share this link:
```
https://github.com/YOUR_USERNAME/YOUR_REPO/releases
```

---

## 📋 Common Commands

| Task | Command |
|------|---------|
| Install dependencies | `pip install -r requirements.txt` |
| Run app (dev) | `python main.py` |
| Build executable | `python build_exe.py` |
| Clean build files | Remove `build`, `dist`, `*.spec` folders |
| Test executable | `dist/ExpenseTracker.exe` |

---

## 🐛 Troubleshooting Quick Fixes

| Problem | Solution |
|---------|----------|
| PyInstaller not found | `pip install pyinstaller` |
| Module not found in .exe | Add `--hidden-import=module_name` |
| CustomTkinter theme broken | Use `--collect-all=customtkinter` |
| .exe too large | Remove `--onefile` flag |
| See error messages | Remove `--windowed` flag |

---

## 📦 What Gets Distributed?

**Users download**: `ExpenseTracker.exe` (50-100MB)

**Users DON'T need**:
- Python installation
- pip packages
- Your source code
- Any dependencies

**The .exe includes everything!**

---

## ✅ Pre-Release Checklist

- [ ] Test the .exe on your machine
- [ ] Test on another Windows machine (if possible)
- [ ] Verify all features work
- [ ] Check data saves correctly
- [ ] Update version number
- [ ] Write release notes
- [ ] Add screenshots to README
- [ ] Push code to GitHub
- [ ] Create GitHub release
- [ ] Upload .exe file
- [ ] Test download link

---

## 🎯 File Sizes

- **Source code**: ~20 KB
- **With dependencies**: ~50 MB
- **Built .exe (onefile)**: ~80-100 MB
- **Built .exe (folder)**: ~70 MB (but multiple files)

---

## 💡 Pro Tips

1. **Always test the .exe** before releasing
2. **Use semantic versioning**: v1.0.0, v1.1.0, v2.0.0
3. **Write clear release notes** for users
4. **Keep old releases** available for download
5. **Respond to user issues** on GitHub
6. **Update regularly** with bug fixes

---

## 🔗 Useful Links

- Full guide: [DISTRIBUTION.md](DISTRIBUTION.md)
- PyInstaller docs: https://pyinstaller.org
- GitHub releases: https://docs.github.com/en/repositories/releasing-projects-on-github

---

**Need help?** Check DISTRIBUTION.md for detailed instructions!
