import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

# Default color to use if color code is missing
default_color = "#1f77b4"

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
print(df)

# Display column names
print("Columns in dataset:", df.columns.tolist())

if not df.empty:
    # Extract columns into separate lists

    next_milestone_date_list = df['Next Milestone Date'].tolist()
    concatenate_list = df['concatenate'].tolist()
    # program_name_list = df['Program Name'].tolist()

    # Use default color if 'field1' is missing
    color_list = df['field1'].tolist() if 'field1' in df.columns else [default_color] * len(df)

    # # Convert 'Next Milestone Date' to datetime
    # df['Next Milestone Date'] = pd.to_datetime(df['Next Milestone Date'])

    # Convert to datetime, coercing errors
    df['Next Milestone Date'] = pd.to_datetime(df['Next Milestone Date'], format='%d/%m/%Y', errors='coerce')

    # Calculate min and max dates
    min_date = df['Next Milestone Date'].min()
    max_date = df['Next Milestone Date'].max()

    # Function to truncate labels
    def truncate_label(label, max_length=20):
        return label if len(label) <= max_length else label[:max_length] + '..'

    # dates = [datetime.strptime(date_str, "%m/%d/%Y") for date_str in next_milestone_date_list ]
    dates = [datetime.strptime(date_str, "%d/%m/%Y") for date_str in next_milestone_date_list if
             isinstance(date_str, str)]

    labels = [truncate_label(label) for label in concatenate_list]

    colors = [color if color else default_color for color in color_list]

    y_positions = list(range(len(df)))

    # Plot setup

    fig, ax = plt.subplots(figsize=(14, 10))

    # Plot milestone markers and labels
    for i, (label, date, color) in enumerate(zip(labels, dates, colors)):
        y = 1 if i % 2 == 0 else -1  # alternate positions

        ax.plot([date, date], [i - 0.4, i + 0.4], color='black', linewidth=1)

        ax.text(date, i, f"{label}\n{date.strftime('%d.%m.%Y')}",
                va='center', ha='center', fontsize=7,
                bbox=dict(facecolor=color, edgecolor='black', boxstyle='round,pad=0.4'), color='white')

    # Calculate start and end dates
    start_date = min_date - relativedelta(months=6)
    end_date = max_date + relativedelta(months=6)

    # Timeline range and x-axis format
    ax.set_xlim(start_date, end_date)

    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b\n%Y"))

    ax.tick_params(axis='x', labelsize=8)
    # Clean up y-axis

    ax.set_yticks([])
    ax.grid(axis='x', linestyle='--', alpha=0.4)

    # Title
    ax.set_title("Milestone Timeline: All Milestones Colored by Last Completed Project Milestone", fontsize=10)

    # Add legend
    unique_milestones = list(set((truncate_label(label), color if color else default_color) for label, color in
                                 zip(concatenate_list, color_list)))

    for label, color in unique_milestones:
        ax.plot([], [], color=color, label=label, linewidth=10)

    ax.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=7)

    # Adjust layout to avoid tight_layout warning

    plt.tight_layout()

    plt.show()

else:
    print("Please select the filter!!!")