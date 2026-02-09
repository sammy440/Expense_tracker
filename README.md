# 💰 Personal Expense Tracker

A beautiful, modern desktop expense tracker built with Python and CustomTkinter. Track your spending, visualize trends, and manage your finances with ease!

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)

## ✨ Features

- 📊 **Visual Dashboard** - Beautiful charts showing spending by category and monthly trends
- 💰 **Expense Tracking** - Add, view, and categorize all your expenses
- 🔍 **Smart Filtering** - Filter expenses by category and date
- 📈 **Analytics** - Track total spending, expense count, and top categories
- 💾 **Export to CSV** - Export your data for further analysis
- 🌓 **Dark/Light Mode** - Choose your preferred theme
- 💻 **Offline First** - All data stored locally in JSON format

## 🚀 Quick Start

### For Users (No Python Required)

1. **Download** the latest release from [Releases](../../releases)
2. **Run** `ExpenseTracker.exe`
3. **Start tracking** your expenses!

### For Developers

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
   cd expense-tracker
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

## 📦 Building an Executable

Want to distribute this app? See the detailed [Distribution Guide](DISTRIBUTION.md).

**Quick build**:
```bash
python build_exe.py
```

The executable will be in the `dist` folder.

## 🛠️ Tech Stack

- **Python 3.10+**
- **CustomTkinter** - Modern UI framework
- **Matplotlib** - Data visualization
- **tkcalendar** - Date picker widget
- **Pillow** - Image processing

## 📁 Project Structure

```
expense-tracker/
├── main.py              # Main application file
├── utils/
│   ├── file_handler.py  # JSON data management
│   ├── stats.py         # Statistics calculations
│   └── chart_utils.py   # Chart generation
├── expenses.json        # Data storage (created on first run)
├── requirements.txt     # Python dependencies
├── build_exe.py         # Build script for PyInstaller
├── DISTRIBUTION.md      # Detailed distribution guide
└── README.md           # This file
```

## 📸 Screenshots

*(Add screenshots of your app here)*

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

If you encounter any issues:
1. Check the [Distribution Guide](DISTRIBUTION.md) for common problems
2. Open an issue on GitHub
3. Contact the developer

## 🎯 Roadmap

- [ ] Add budget limits and alerts
- [ ] Recurring expense support
- [ ] Multi-currency support
- [ ] Cloud backup option
- [ ] Mobile companion app

---

Made with ❤️ using Python and CustomTkinter
