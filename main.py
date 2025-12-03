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

# Set appearance mode and default color theme
ctk.set_appearance_mode("dark")  # Modes: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

class ExpenseTrackerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("Personal Expense Tracker")
        self.geometry("1200x700")
        
        # Configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create sidebar frame with widgets
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)

        # Sidebar - Logo/Title
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="💰 Expense Tracker", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Sidebar - Navigation Buttons
        self.dashboard_button = ctk.CTkButton(
            self.sidebar_frame, 
            text="Dashboard",
            command=self.show_dashboard
        )
        self.dashboard_button.grid(row=1, column=0, padx=20, pady=10)

        self.add_expense_button = ctk.CTkButton(
            self.sidebar_frame, 
            text="Add Expense",
            command=self.show_add_expense
        )
        self.add_expense_button.grid(row=2, column=0, padx=20, pady=10)

        self.view_expenses_button = ctk.CTkButton(
            self.sidebar_frame, 
            text="View Expenses",
            command=self.show_view_expenses
        )
        self.view_expenses_button.grid(row=3, column=0, padx=20, pady=10)

        self.export_button = ctk.CTkButton(
            self.sidebar_frame, 
            text="Export Data",
            command=self.export_data
        )
        self.export_button.grid(row=4, column=0, padx=20, pady=10)

        # Sidebar - Theme Toggle
        self.appearance_mode_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="Appearance Mode:", 
            anchor="w"
        )
        self.appearance_mode_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(
            self.sidebar_frame, 
            values=["Dark", "Light", "System"],
            command=self.change_appearance_mode_event
        )
        self.appearance_mode_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # Create main content frame
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        # Initialize with dashboard
        self.current_view = None
        self.show_dashboard()

    def clear_main_frame(self):
        """Clear all widgets from main frame"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        """Change the appearance mode"""
        ctk.set_appearance_mode(new_appearance_mode)

    def show_dashboard(self):
        """Display the dashboard with statistics and charts"""
        if self.current_view == "dashboard":
            return
        
        self.current_view = "dashboard"
        self.clear_main_frame()

        # Title
        title = ctk.CTkLabel(
            self.main_frame, 
            text="Dashboard", 
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=3, padx=20, pady=(0, 20), sticky="w")

        # Load expenses
        expenses = load_expenses()

        # Statistics Cards Frame
        stats_frame = ctk.CTkFrame(self.main_frame)
        stats_frame.grid(row=1, column=0, columnspan=3, padx=20, pady=10, sticky="ew")
        stats_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # Card 1: Total Spending
        total_spending = get_total_spending(expenses)
        card1 = ctk.CTkFrame(stats_frame, corner_radius=10)
        card1.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        ctk.CTkLabel(
            card1, 
            text="Total Spending", 
            font=ctk.CTkFont(size=14)
        ).pack(pady=(15, 5))
        
        ctk.CTkLabel(
            card1, 
            text=f"${total_spending:.2f}", 
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=(0, 15))

        # Card 2: Number of Expenses
        expense_count = get_expense_count(expenses)
        card2 = ctk.CTkFrame(stats_frame, corner_radius=10)
        card2.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        ctk.CTkLabel(
            card2, 
            text="Total Expenses", 
            font=ctk.CTkFont(size=14)
        ).pack(pady=(15, 5))
        
        ctk.CTkLabel(
            card2, 
            text=str(expense_count), 
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=(0, 15))

        # Card 3: Highest Category
        highest_category = get_highest_spending_category(expenses)
        card3 = ctk.CTkFrame(stats_frame, corner_radius=10)
        card3.grid(row=0, column=2, padx=10, pady=10, sticky="ew")
        
        ctk.CTkLabel(
            card3, 
            text="Top Category", 
            font=ctk.CTkFont(size=14)
        ).pack(pady=(15, 5))
        
        ctk.CTkLabel(
            card3, 
            text=highest_category, 
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=(0, 15))

        # Charts Frame
        charts_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        charts_frame.grid(row=2, column=0, columnspan=3, padx=20, pady=10, sticky="nsew")
        charts_frame.grid_columnconfigure((0, 1), weight=1)
        charts_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)

        # Pie Chart
        pie_frame = ctk.CTkFrame(charts_frame, corner_radius=10)
        pie_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        ctk.CTkLabel(
            pie_frame, 
            text="Category Distribution", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)

        category_data = get_category_breakdown(expenses)
        if category_data:
            pie_widget = create_category_pie_chart(pie_frame, category_data)
            if pie_widget:
                pie_widget.pack(fill="both", expand=True, padx=10, pady=10)
        else:
            ctk.CTkLabel(pie_frame, text="No data available").pack(pady=20)

        # Line Chart
        line_frame = ctk.CTkFrame(charts_frame, corner_radius=10)
        line_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        ctk.CTkLabel(
            line_frame, 
            text="Monthly Trend", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)

        monthly_data = get_monthly_spending(expenses)
        if monthly_data:
            line_widget = create_monthly_trend_chart(line_frame, monthly_data)
            if line_widget:
                line_widget.pack(fill="both", expand=True, padx=10, pady=10)
        else:
            ctk.CTkLabel(line_frame, text="No data available").pack(pady=20)

    def show_add_expense(self):
        """Display the add expense form"""
        if self.current_view == "add_expense":
            return
        
        self.current_view = "add_expense"
        self.clear_main_frame()

        # Title
        title = ctk.CTkLabel(
            self.main_frame, 
            text="Add New Expense", 
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(pady=(0, 30))

        # Form Frame
        form_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        form_frame.pack(padx=100, pady=20, fill="both", expand=True)

        # Amount
        ctk.CTkLabel(
            form_frame, 
            text="Amount ($):", 
            font=ctk.CTkFont(size=14)
        ).pack(pady=(20, 5), anchor="w", padx=40)
        
        self.amount_entry = ctk.CTkEntry(
            form_frame, 
            placeholder_text="0.00",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.amount_entry.pack(pady=(0, 15), padx=40, fill="x")

        # Category
        ctk.CTkLabel(
            form_frame, 
            text="Category:", 
            font=ctk.CTkFont(size=14)
        ).pack(pady=(10, 5), anchor="w", padx=40)
        
        self.category_var = ctk.StringVar(value="Food")
        self.category_menu = ctk.CTkOptionMenu(
            form_frame,
            values=["Food", "Transport", "Bills", "Entertainment", "Shopping", "Health", "Misc"],
            variable=self.category_var,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.category_menu.pack(pady=(0, 15), padx=40, fill="x")

        # Date
        ctk.CTkLabel(
            form_frame, 
            text="Date:", 
            font=ctk.CTkFont(size=14)
        ).pack(pady=(10, 5), anchor="w", padx=40)
        
        self.date_entry = DateEntry(
            form_frame,
            width=12,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern='yyyy-mm-dd'
        )
        self.date_entry.pack(pady=(0, 15), padx=40, fill="x")

        # Description
        ctk.CTkLabel(
            form_frame, 
            text="Description:", 
            font=ctk.CTkFont(size=14)
        ).pack(pady=(10, 5), anchor="w", padx=40)
        
        self.description_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Optional description",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.description_entry.pack(pady=(0, 20), padx=40, fill="x")

        # Submit Button
        submit_button = ctk.CTkButton(
            form_frame,
            text="Add Expense",
            command=self.submit_expense,
            height=45,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        submit_button.pack(pady=(10, 30), padx=40, fill="x")

    def submit_expense(self):
        """Handle expense submission"""
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                raise ValueError("Amount must be positive")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive amount")
            return

        category = self.category_var.get()
        date = self.date_entry.get_date().strftime("%Y-%m-%d")
        description = self.description_entry.get()

        expense = {
            "amount": amount,
            "category": category,
            "date": date,
            "description": description,
            "timestamp": datetime.now().isoformat()
        }

        if add_expense(expense):
            messagebox.showinfo("Success", "Expense added successfully!")
            # Clear form
            self.amount_entry.delete(0, 'end')
            self.description_entry.delete(0, 'end')
            self.date_entry.set_date(datetime.now())
        else:
            messagebox.showerror("Error", "Failed to save expense")

    def show_view_expenses(self):
        """Display all expenses in a scrollable view"""
        if self.current_view == "view_expenses":
            return
        
        self.current_view = "view_expenses"
        self.clear_main_frame()

        # Title
        title = ctk.CTkLabel(
            self.main_frame, 
            text="View Expenses", 
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(pady=(0, 20))

        # Filter Frame
        filter_frame = ctk.CTkFrame(self.main_frame)
        filter_frame.pack(padx=20, pady=10, fill="x")

        ctk.CTkLabel(filter_frame, text="Filter by Category:").pack(side="left", padx=10)
        
        self.filter_var = ctk.StringVar(value="All")
        filter_menu = ctk.CTkOptionMenu(
            filter_frame,
            values=["All", "Food", "Transport", "Bills", "Entertainment", "Shopping", "Health", "Misc"],
            variable=self.filter_var,
            command=lambda x: self.refresh_expense_list()
        )
        filter_menu.pack(side="left", padx=10)

        # Scrollable Frame for expenses
        self.expenses_scroll_frame = ctk.CTkScrollableFrame(self.main_frame)
        self.expenses_scroll_frame.pack(padx=20, pady=10, fill="both", expand=True)

        self.refresh_expense_list()

    def refresh_expense_list(self):
        """Refresh the expense list based on current filter"""
        # Clear existing items
        for widget in self.expenses_scroll_frame.winfo_children():
            widget.destroy()

        expenses = load_expenses()
        filter_category = self.filter_var.get()

        # Filter expenses
        if filter_category != "All":
            expenses = [e for e in expenses if e['category'] == filter_category]

        # Sort by date (newest first)
        expenses.sort(key=lambda x: x['date'], reverse=True)

        if not expenses:
            ctk.CTkLabel(
                self.expenses_scroll_frame, 
                text="No expenses found",
                font=ctk.CTkFont(size=16)
            ).pack(pady=20)
            return

        # Display expenses
        for expense in expenses:
            expense_frame = ctk.CTkFrame(self.expenses_scroll_frame, corner_radius=10)
            expense_frame.pack(padx=10, pady=5, fill="x")

            # Left side - Category and Description
            left_frame = ctk.CTkFrame(expense_frame, fg_color="transparent")
            left_frame.pack(side="left", fill="both", expand=True, padx=15, pady=10)

            ctk.CTkLabel(
                left_frame,
                text=f"🏷️ {expense['category']}",
                font=ctk.CTkFont(size=14, weight="bold")
            ).pack(anchor="w")

            if expense.get('description'):
                ctk.CTkLabel(
                    left_frame,
                    text=expense['description'],
                    font=ctk.CTkFont(size=12),
                    text_color="gray"
                ).pack(anchor="w")

            # Right side - Amount and Date
            right_frame = ctk.CTkFrame(expense_frame, fg_color="transparent")
            right_frame.pack(side="right", padx=15, pady=10)

            ctk.CTkLabel(
                right_frame,
                text=f"${expense['amount']:.2f}",
                font=ctk.CTkFont(size=16, weight="bold")
            ).pack(anchor="e")

            ctk.CTkLabel(
                right_frame,
                text=expense['date'],
                font=ctk.CTkFont(size=12),
                text_color="gray"
            ).pack(anchor="e")

    def export_data(self):
        """Export expenses to CSV"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if filename:
            if export_to_csv(filename):
                messagebox.showinfo("Success", f"Data exported to {filename}")
            else:
                messagebox.showerror("Error", "Failed to export data")

if __name__ == "__main__":
    app = ExpenseTrackerApp()
    app.mainloop()
