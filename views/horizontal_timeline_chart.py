import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import streamlit as st

# Sample data

data = {
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
        "2025-05-28 00:00:00",
        "2025-05-30 00:00:00",
        "2025-05-30 00:00:00",
        "2025-06-01 00:00:00",
        "2025-06-02 00:00:00",
        "2025-06-03 00:00:00",
        "2025-06-04 00:00:00",
        "2025-06-05 00:00:00",
        "2025-06-06 00:00:00",
        "2025-06-07 00:00:00",
        "2025-06-08 00:00:00",
    ],
}

df = pd.DataFrame(data)
# Function to truncate labels

def truncate_label(label, max_length=20):
    return label if len(label) <= max_length else label[:max_length] + '..'

def create_timeline_chart(df):
    if not df.empty:
        df["Date"] = pd.to_datetime(df["Next Milestone Date"])

        # Setup the figure
        fig, ax = plt.subplots(figsize=(14, 5))
        ax.axhline(0, color='black', linewidth=1)

        # Plot milestones with adjusted vertical positions to avoid overlap
        date_counts = df["Date"].value_counts().to_dict()
        date_offsets = {date: 0 for date in date_counts}

        for i, (idx, row) in enumerate(df.iterrows()):
            y = 1 if i % 2 == 0 else -1
            offset = date_offsets[row["Date"]] * 0.15
            date_offsets[row["Date"]] += 1
            ax.vlines(row["Date"], 0, y * (0.7 + offset), linewidth=2)
            ax.plot(row["Date"], y * (0.7 + offset), "o", markersize=20)

            ax.text(
                row["Date"], y * (0.85 + offset),
                f"{truncate_label(row['concatenate'])}\n{row['Date'].strftime('%d.%m.%Y')}",
                ha='center',
                va='bottom' if y > 0 else 'top',
                fontsize=7,
            )

        # Hide x-axis
        ax.xaxis.set_visible(False)

        # Final touches
        ax.set_yticks([])
        ax.set_ylim(-1.5, 1.5)

        ax.set_title("Milestone Timeline: All Milestones Colored by Last Completed Project Milestone", fontsize=10,
                     weight='bold')

        ax.grid(False)
        plt.tight_layout()
        st.pyplot(fig)
    else:
        print("Please select the filter!!!")

create_timeline_chart(df)