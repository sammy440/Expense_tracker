import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# consistent colors
COLOR_PRIMARY = "#1f6aa5" # distinctive blue
COLOR_BG = "#2b2b2b" # dark grey for card background
COLOR_TEXT = "#ffffff"
COLOR_ACCENT = ["#3B8ED0", "#1F6AA5", "#144870", "#E1E1E1", "#D1D5DB"] # Blue-ish palette

def setup_dark_theme():
    """Configure matplotlib for dark theme"""
    plt.style.use('dark_background')
    plt.rcParams.update({
        'axes.facecolor': COLOR_BG,
        'figure.facecolor': COLOR_BG,
        'text.color': COLOR_TEXT,
        'axes.labelcolor': COLOR_TEXT,
        'xtick.color': COLOR_TEXT,
        'ytick.color': COLOR_TEXT,
        'grid.color': '#404040',
        'font.family': 'sans-serif',
        'font.size': 10
    })

def create_category_pie_chart(parent, category_data):
    """
    Embed a pie chart of category distribution.
    """
    setup_dark_theme()
    
    if not category_data:
        return None

    labels = list(category_data.keys())
    sizes = list(category_data.values())

    # Create figure with transparent background
    fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
    fig.patch.set_facecolor(COLOR_BG)
    
    wedges, texts, autotexts = ax.pie(
        sizes, 
        labels=labels, 
        autopct='%1.1f%%', 
        startangle=90,
        colors=plt.cm.Paired.colors if len(labels) > 5 else COLOR_ACCENT[:len(labels)],
        textprops=dict(color=COLOR_TEXT),
        wedgeprops=dict(width=0.6, edgecolor=COLOR_BG)  # Donut style
    )
    
    # Style text
    plt.setp(texts, size=9)
    plt.setp(autotexts, size=9, weight="bold")
    
    ax.axis('equal')
    
    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    return canvas.get_tk_widget()

def create_monthly_trend_chart(parent, monthly_data):
    """
    Embed a line chart of monthly spending.
    """
    setup_dark_theme()

    if not monthly_data:
        return None

    # Sort by date
    sorted_months = sorted(monthly_data.keys())
    amounts = [monthly_data[m] for m in sorted_months]

    fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
    fig.patch.set_facecolor(COLOR_BG)
    ax.set_facecolor(COLOR_BG)
    
    # Plot with gradient-like effect or simple clean line
    ax.plot(
        sorted_months, 
        amounts, 
        marker='o', 
        linestyle='-', 
        color=COLOR_PRIMARY,
        linewidth=2,
        markersize=6
    )
    
    # Fill area under line for "modern" look
    ax.fill_between(sorted_months, amounts, alpha=0.3, color=COLOR_PRIMARY)
    
    ax.set_title("Monthly Spending Trend", color=COLOR_TEXT, pad=20)
    ax.set_xlabel("Month", color=COLOR_TEXT)
    ax.set_ylabel("Amount ($)", color=COLOR_TEXT)
    
    # Stylize grid
    ax.grid(True, linestyle='--', alpha=0.3)
    
    # Remove top and right spines for cleaner look
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.xticks(rotation=45)
    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    return canvas.get_tk_widget()
