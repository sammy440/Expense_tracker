import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def create_category_pie_chart(parent, category_data):
    """
    Embed a pie chart of category distribution into a Tkinter/CustomTkinter widget.
    parent: The widget to contain the chart.
    category_data: Dictionary {category: amount}
    """
    if not category_data:
        return None

    labels = list(category_data.keys())
    sizes = list(category_data.values())

    # Create figure
    fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    # Set figure background to match modern dark/light themes if needed, 
    # but for now standard white/transparent is okay.
    # fig.patch.set_facecolor('#2b2b2b') # Example for dark mode
    
    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    return canvas.get_tk_widget()

def create_monthly_trend_chart(parent, monthly_data):
    """
    Embed a line chart of monthly spending.
    parent: The widget to contain the chart.
    monthly_data: Dictionary {YYYY-MM: amount}
    """
    if not monthly_data:
        return None

    # Sort by date
    sorted_months = sorted(monthly_data.keys())
    amounts = [monthly_data[m] for m in sorted_months]

    fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
    ax.plot(sorted_months, amounts, marker='o', linestyle='-')
    ax.set_title("Monthly Spending Trend")
    ax.set_xlabel("Month")
    ax.set_ylabel("Amount")
    plt.xticks(rotation=45)
    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    return canvas.get_tk_widget()
