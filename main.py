import customtkinter as ctk
from tkinter import messagebox, filedialog
from tkcalendar import DateEntry
from datetime import datetime
import sys
import os

# Add utils to path
sys.path.append(os.path.dirname(__file__))

from utils.file_handler import load_expenses, add_expense, export_to_csv
from utils.stats import (
    get_total_spending, 
    get_expense_count, 
    get_category_breakdown,
    get_highest_spending_category,
    get_monthly_spending
)
from utils.chart_utils import create_category_pie_chart, create_monthly_trend_chart

# --- Theme Configuration ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# Colors
COLOR_BG_MAIN = "#1a1a1a"
COLOR_SIDEBAR = "#242424"
COLOR_CARD = "#2b2b2b"
COLOR_PRIMARY = "#1f6aa5"
COLOR_TEXT_MAIN = "#ffffff"
COLOR_TEXT_SUB = "#aaaaaa"
FONT_FAMILY = "Segoe UI" # Windows standard, falls back gracefully

class ExpenseTrackerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("ExpenseTracker | Pro")
        self.geometry("1400x850")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Fonts
        self.font_header = ctk.CTkFont(family=FONT_FAMILY, size=28, weight="bold")
        self.font_subheader = ctk.CTkFont(family=FONT_FAMILY, size=20, weight="bold")
        self.font_normal = ctk.CTkFont(family=FONT_FAMILY, size=14)
        self.font_small = ctk.CTkFont(family=FONT_FAMILY, size=12)
        self.font_stat_val = ctk.CTkFont(family=FONT_FAMILY, size=32, weight="bold")
        self.font_stat_label = ctk.CTkFont(family=FONT_FAMILY, size=14)

        # Create Sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=240, corner_radius=0, fg_color=COLOR_SIDEBAR)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(8, weight=1)

        self.buttons = {}
        self._create_sidebar()

        # Create Main Content Area
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=COLOR_BG_MAIN)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        # Initialize
        self.current_view = None

        self.show_dashboard()

    def _create_sidebar(self):
        # Logo
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="💰 ExpenseTracker", 
            font=ctk.CTkFont(family=FONT_FAMILY, size=22, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(40, 30), sticky="ew")

        # Navigation
        self._add_nav_button("Dashboard", "📊", self.show_dashboard, 1)
        self._add_nav_button("New Expense", "➕", self.show_add_expense, 2)
        self._add_nav_button("Transactions", "📝", self.show_view_expenses, 3)
        self._add_nav_button("Export Data", "📤", self.export_data, 4)

        # Appearance Mode
        self.appearance_mode_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="Theme:", 
            anchor="w",
            font=self.font_small,
            text_color=COLOR_TEXT_SUB
        )
        self.appearance_mode_label.grid(row=9, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.appearance_mode_menu = ctk.CTkOptionMenu(
            self.sidebar_frame, 
            values=["Dark", "Light", "System"],
            command=self.change_appearance_mode_event,
            font=self.font_small,
            fg_color=COLOR_CARD
        )
        self.appearance_mode_menu.grid(row=10, column=0, padx=20, pady=(5, 30), sticky="ew")
        self.appearance_mode_menu.set("Dark")

    def _add_nav_button(self, text, icon, command, row):
        btn = ctk.CTkButton(
            self.sidebar_frame,
            corner_radius=8,
            height=45,
            border_spacing=10,
            text=f"{icon}  {text}",
            fg_color="transparent",
            text_color=COLOR_TEXT_SUB,
            hover_color=("gray70", "gray30"),
            anchor="w",
            command=lambda: self._handle_nav(command, text),
            font=ctk.CTkFont(family=FONT_FAMILY, size=15, weight="bold")
        )
        btn.grid(row=row, column=0, sticky="ew", padx=15, pady=5)
        self.buttons[text] = btn

    def _handle_nav(self, command, name):
        # Reset all buttons
        for btn_name, btn in self.buttons.items():
            btn.configure(fg_color="transparent", text_color=COLOR_TEXT_SUB)
        
        # Highlight active
        self.buttons[name].configure(fg_color=COLOR_PRIMARY, text_color="white")
        command()

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    # --- VIEWS ---

    def show_dashboard(self):
        if self.current_view == "dashboard": return
        self.current_view = "dashboard"
        self.clear_main_frame()
        self.buttons["Dashboard"].configure(fg_color=COLOR_PRIMARY, text_color="white") # Ensure highlight on init

        # Container
        content = ctk.CTkScrollableFrame(self.main_frame, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Header
        ctk.CTkLabel(content, text="Dashboard Overview", font=self.font_header).pack(anchor="w", pady=(0, 20))

        expenses = load_expenses()

        # Stats Row
        stats_container = ctk.CTkFrame(content, fg_color="transparent")
        stats_container.pack(fill="x", pady=(0, 30))
        stats_container.grid_columnconfigure((0, 1, 2), weight=1)

        self._create_stat_card(stats_container, 0, "Total Spending", f"${get_total_spending(expenses):.2f}", "💵")
        self._create_stat_card(stats_container, 1, "Total Transactions", str(get_expense_count(expenses)), "🧾")
        self._create_stat_card(stats_container, 2, "Top Category", get_highest_spending_category(expenses), "🔥")

        # Charts Section
        charts_container = ctk.CTkFrame(content, fg_color="transparent")
        charts_container.pack(fill="both", expand=True)
        charts_container.grid_columnconfigure((0, 1), weight=1)
        charts_container.grid_rowconfigure(0, weight=1)

        # Pie Chart
        pie_card = ctk.CTkFrame(charts_container, fg_color=COLOR_CARD, corner_radius=15)
        pie_card.grid(row=0, column=0, sticky="nsew", padx=(0, 15), pady=10)
        ctk.CTkLabel(pie_card, text="Distribution by Category", font=self.font_subheader).pack(pady=15)
        
        category_data = get_category_breakdown(expenses)
        if category_data:
            chart = create_category_pie_chart(pie_card, category_data)
            chart.pack(fill="both", expand=True, padx=10, pady=10)
        else:
            ctk.CTkLabel(pie_card, text="No data available", font=self.font_normal, text_color="gray").pack(expand=True)

        # Line Chart
        line_card = ctk.CTkFrame(charts_container, fg_color=COLOR_CARD, corner_radius=15)
        line_card.grid(row=0, column=1, sticky="nsew", padx=(15, 0), pady=10)
        ctk.CTkLabel(line_card, text="Spending Trend", font=self.font_subheader).pack(pady=15)

        monthly_data = get_monthly_spending(expenses)
        if monthly_data:
            chart = create_monthly_trend_chart(line_card, monthly_data)
            chart.pack(fill="both", expand=True, padx=10, pady=10)
        else:
            ctk.CTkLabel(line_card, text="No data available", font=self.font_normal, text_color="gray").pack(expand=True)

    def _create_stat_card(self, parent, col, title, value, icon):
        card = ctk.CTkFrame(parent, fg_color=COLOR_CARD, corner_radius=15, height=140)
        card.grid(row=0, column=col, sticky="ew", padx=10 if col==1 else 0)
        
        # Prevent shrinking
        card.grid_propagate(False) 
        
        ctk.CTkLabel(card, text=title, font=self.font_stat_label, text_color=COLOR_TEXT_SUB).pack(pady=(20, 5), padx=20, anchor="w")
        ctk.CTkLabel(card, text=value, font=self.font_stat_val, text_color=COLOR_TEXT_MAIN).pack(pady=(0, 5), padx=20, anchor="w")
        # Icon watermark (optional)
        icon_lbl = ctk.CTkLabel(card, text=icon, font=ctk.CTkFont(size=40))
        icon_lbl.place(relx=0.9, rely=0.5, anchor="e")

    def show_add_expense(self):
        if self.current_view == "add_expense": return
        self.current_view = "add_expense"
        self.clear_main_frame()
        self.buttons["New Expense"].configure(fg_color=COLOR_PRIMARY, text_color="white")

        # Center Container
        center_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        center_frame.pack(expand=True, fill="both", padx=100, pady=50)

        card = ctk.CTkFrame(center_frame, fg_color=COLOR_CARD, corner_radius=20)
        card.pack(fill="both", expand=True, padx=50, pady=20)

        # Form Content
        form_scroll = ctk.CTkScrollableFrame(card, fg_color="transparent")
        form_scroll.pack(fill="both", expand=True, padx=40, pady=40)

        ctk.CTkLabel(form_scroll, text="Add New Expense", font=self.font_header).pack(pady=(0, 30), anchor="w")

        # Fields
        self._create_form_entry(form_scroll, "Amount ($)", "amount_entry", "0.00")
        self._create_form_dropdown(form_scroll, "Category", "category_var", ["Food", "Transport", "Bills", "Entertainment", "Shopping", "Health", "Misc"])
        
        # Date (Special case)
        ctk.CTkLabel(form_scroll, text="Date", font=self.font_normal, text_color=COLOR_TEXT_SUB).pack(pady=(10, 5), anchor="w")
        self.date_entry = DateEntry(
            form_scroll, width=12, background='#2b2b2b', foreground='white', 
            borderwidth=0, date_pattern='yyyy-mm-dd', font=('Arial', 12)
        )
        self.date_entry.pack(fill="x", pady=(0, 20), ipady=5)

        self._create_form_entry(form_scroll, "Description", "description_entry", "What was this for?")

        # Buttons
        btn_frame = ctk.CTkFrame(form_scroll, fg_color="transparent")
        btn_frame.pack(fill="x", pady=20)

        ctk.CTkButton(
            btn_frame, text="Save Expense", height=50, 
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=COLOR_PRIMARY, hover_color="#144870",
            command=self.submit_expense
        ).pack(fill="x")

    def _create_form_entry(self, parent, label, attr_name, placeholder):
        ctk.CTkLabel(parent, text=label, font=self.font_normal, text_color=COLOR_TEXT_SUB).pack(pady=(10, 5), anchor="w")
        entry = ctk.CTkEntry(
            parent, placeholder_text=placeholder, height=45, border_width=0,
            fg_color="#3a3a3a", text_color="white", placeholder_text_color="#666666",
            font=self.font_normal
        )
        entry.pack(fill="x", pady=(0, 15))
        setattr(self, attr_name, entry)

    def _create_form_dropdown(self, parent, label, attr_name, values):
        ctk.CTkLabel(parent, text=label, font=self.font_normal, text_color=COLOR_TEXT_SUB).pack(pady=(10, 5), anchor="w")
        var = ctk.StringVar(value=values[0])
        menu = ctk.CTkOptionMenu(
            parent, variable=var, values=values, height=45,
            fg_color="#3a3a3a", button_color=COLOR_PRIMARY,
            button_hover_color="#144870", text_color="white",
            font=self.font_normal
        )
        menu.pack(fill="x", pady=(0, 15))
        setattr(self, attr_name, var)

    def submit_expense(self):
        try:
            val = self.amount_entry.get()
            if not val: raise ValueError
            amount = float(val)
            if amount <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid positive amount.")
            return

        expense = {
            "amount": amount,
            "category": self.category_var.get(),
            "date": self.date_entry.get_date().strftime("%Y-%m-%d"),
            "description": self.description_entry.get(),
            "timestamp": datetime.now().isoformat()
        }

        if add_expense(expense):
            messagebox.showinfo("Success", "Expense saved successfully!")
            self.amount_entry.delete(0, 'end')
            self.description_entry.delete(0, 'end')
        else:
            messagebox.showerror("Error", "Could not save expense.")

    def show_view_expenses(self):
        if self.current_view == "view_expenses": return
        self.current_view = "view_expenses"
        self.clear_main_frame()
        self.buttons["Transactions"].configure(fg_color=COLOR_PRIMARY, text_color="white")

        container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=30, pady=30)

        # Header with Filter
        header_frame = ctk.CTkFrame(container, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(header_frame, text="Transaction History", font=self.font_header).pack(side="left")
        
        self.filter_var = ctk.StringVar(value="All")
        filter_menu = ctk.CTkOptionMenu(
            header_frame,
            values=["All", "Food", "Transport", "Bills", "Entertainment", "Shopping", "Health", "Misc"],
            variable=self.filter_var,
            width=150,
            command=lambda x: self.refresh_expense_list()
        )
        filter_menu.pack(side="right")
        ctk.CTkLabel(header_frame, text="Filter:", font=self.font_normal, text_color=COLOR_TEXT_SUB).pack(side="right", padx=10)

        # List Area
        self.expenses_scroll_frame = ctk.CTkScrollableFrame(container, fg_color="transparent")
        self.expenses_scroll_frame.pack(fill="both", expand=True)

        self.refresh_expense_list()

    def refresh_expense_list(self):
        for widget in self.expenses_scroll_frame.winfo_children(): widget.destroy()

        expenses = load_expenses()
        filter_cat = self.filter_var.get()
        if filter_cat != "All":
            expenses = [e for e in expenses if e['category'] == filter_cat]
        expenses.sort(key=lambda x: x['date'], reverse=True)

        if not expenses:
            ctk.CTkLabel(self.expenses_scroll_frame, text="No transactions found.", font=self.font_normal, text_color="gray").pack(pady=40)
            return

        for exp in expenses:
            self._create_expense_row(exp)

    def _create_expense_row(self, expense):
        row = ctk.CTkFrame(self.expenses_scroll_frame, fg_color=COLOR_CARD, corner_radius=10)
        row.pack(fill="x", pady=5)
        
        # Icon/Category
        ctk.CTkLabel(row, text="🏷️", font=ctk.CTkFont(size=20)).pack(side="left", padx=(15, 5), pady=15)
        
        info_frame = ctk.CTkFrame(row, fg_color="transparent")
        info_frame.pack(side="left", padx=10)
        
        ctk.CTkLabel(info_frame, text=expense['category'], font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(info_frame, text=expense['date'], font=ctk.CTkFont(size=11), text_color=COLOR_TEXT_SUB).pack(anchor="w")
        
        # Amount/Desc
        amt_frame = ctk.CTkFrame(row, fg_color="transparent")
        amt_frame.pack(side="right", padx=15)
        
        ctk.CTkLabel(amt_frame, text=f"-${expense['amount']:.2f}", font=ctk.CTkFont(size=16, weight="bold"), text_color="#ff6b6b").pack(anchor="e") # Red for expense
        if expense.get('description'):
             ctk.CTkLabel(amt_frame, text=expense['description'], font=ctk.CTkFont(size=12), text_color=COLOR_TEXT_SUB).pack(anchor="e")

    def export_data(self):
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if filename:
            if export_to_csv(filename): messagebox.showinfo("Success", f"Data exported to {filename}")
            else: messagebox.showerror("Error", "Failed to export data")

if __name__ == "__main__":
    app = ExpenseTrackerApp()
    app.mainloop()
