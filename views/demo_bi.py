import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import random
import colorsys

# Sample dataset

dataset = {
    "concatenate": [
        "MC-OGG1-1L, NCE, Ex,MC-OGG1-1L, NCE, Ex",
        "MC-WWP1-1L, NCE, Ex",
        "MC-APR2-1L, NCE, Ex",
        "MC-UCP3-1L, NCE, Ex",
        "MC-UCP3-2L, NCE, Ex",
        "MC-UCP3-2L, NCE, Ex",
        "MC-UCP3-3L, NCE, Ex",
        "MC-UCP3-4L, NCE, Ex",
        "MC-UCP3-5L, NCE, Ex",
        "MC-UCP3-4L, NCE, Ex",
        "MC-UCP3-5L, NCE, Ex"
    ],

    "Next Milestone Date": [
        "28/05/2025", "30/05/2025", "30/05/2025", "01/06/2025", "02/06/2025",
        "03/06/2025", "04/06/2025", "05/06/2025", "06/06/2025", "07/06/2025", "08/06/2025"
    ],
}

df = pd.DataFrame(dataset)

# Generate medium-brightness random colors
def generate_medium_color():
    h = random.random()
    s = 0.5 + random.random() * 0.3  # Saturation between 0.5 and 0.8
    v = 0.6 + random.random() * 0.3  # Brightness between 0.6 and 0.9

    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return '#{:02x}{:02x}{:02x}'.format(int(r * 255), int(g * 255), int(b * 255))

# Quarter formatter

def quarter_with_months_old(x, pos=None):
    date = mdates.num2date(x)
    year = date.year
    month = date.month
    if 1 <= month <= 3:
        return f"Q1 {year}\n(Jan–Mar)"

    elif 4 <= month <= 6:
        return f"Q2 {year}\n(Apr–Jun)"

    elif 7 <= month <= 9:
        return f"Q3 {year}\n(Jul–Sep)"

    else:
        return f"Q4 {year}\n(Oct–Dec)"

# Fiscal quarter formatter (Q1 starts in April)

def quarter_with_months(x, pos=None):
    date = mdates.num2date(x)
    year = date.year
    month = date.month

    if 4 <= month <= 6:
        return f"Q1 {year}\n(Apr–Jun)"

    elif 7 <= month <= 9:
        return f"Q2 {year}\n(Jul–Sep)"

    elif 10 <= month <= 12:
        return f"Q3 {year}\n(Oct–Dec)"

    else:  # Jan–Mar belongs to Q4 of previous fiscal year
        return f"Q4 {year - 1}\n(Jan–Mar)"

def create_timeline_chart(df):
    # To print the dataset values in Power BI

    # plt.figure(figsize=(10, 6))
    # plt.axis('off')
    # table = plt.table(cellText=df.values, colLabels=df.columns, loc='center')
    # plt.show()
    # exit()

    if not df.empty:
        # Assign random colors if 'field1' is missing

        # color_list = df['field1'].tolist() if 'field1' in df.columns else [f"#{random.randint(0, 0xFFFFFF):06x}" for _ in range(len(df))]

        color_list = df['field1'].tolist() if 'field1' in df.columns else [generate_medium_color() for _ in
                                                                           range(len(df))]
        # Convert to datetime and drop invalid dates
        df['Next Milestone Date'] = pd.to_datetime(df['Next Milestone Date'], format='%d/%m/%Y', errors='coerce')

        df = df.dropna(subset=['Next Milestone Date'])

        # Truncate long labels
        def truncate_label(label, max_length=20):
            return label if len(label) <= max_length else label[:max_length] + '..'

        dates = df['Next Milestone Date'].tolist()

        labels = [truncate_label(label) for label in df['concatenate'].tolist()]

        # colors = [color if color else f"#{random.randint(0, 0xFFFFFF):06x}" for color in color_list[:len(df)]]

        colors = [color if color else generate_medium_color() for color in color_list[:len(df)]]

        # Plot setup
        fig, ax = plt.subplots(figsize=(14, 10))

        for i, (label, date, color) in enumerate(zip(labels, dates, colors)):
            ax.plot([date, date], [i - 0.4, i + 0.4], color='black', linewidth=1)

            ax.text(date, i, f"{label}\n{date.strftime('%d.%m.%Y')}",
                    va='center', ha='center', fontsize=7,
                    bbox=dict(facecolor=color, edgecolor='black', boxstyle='round,pad=0.4'), color='white')

        # Set x-axis range and format
        min_date = df['Next Milestone Date'].min()
        max_date = df['Next Milestone Date'].max()

        start_date = min_date - relativedelta(months=6)
        end_date = max_date + relativedelta(months=6)

        ax.set_xlim(start_date, end_date)
        ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 4, 7, 10]))
        ax.xaxis.set_major_formatter(plt.FuncFormatter(quarter_with_months))

        ax.tick_params(axis='x', labelsize=7)

        ax.set_yticks([])

        ax.grid(axis='x', linestyle='--', alpha=0.4)

        # Title
        ax.set_title("Milestone Timeline: All Milestones Colored by Last Completed Project Milestone", fontsize=10)

        plt.tight_layout()
        plt.show()
    else:
        print("Please select the filter!!!")
create_timeline_chart(df)