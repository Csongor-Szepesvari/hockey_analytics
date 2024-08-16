# Shooting analysis display
'''
We're going to import the data we get from shooting analysis and use this separate file to display them.
We do this because we need to run an instance of matplotlib instead of just grabbing a screengrab which is how it works in the notebook.

Our goals are:
    - Create a search bar, so we can manipulate the data live
    - Have a hover feature that highlights the line of a player when they are being hovered on.
'''
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox
import mplcursors
import pandas as pd

import plotly.graph_objs as go
# Create data for the plot

# import all the data from the shooting_analysis document to be able to work with it here
undiscounted = pd.read_csv("simple_analysis_all_positions.csv")

mean_series = [
    np.sin(np.linspace(0, 10, 100)),
    np.cos(np.linspace(0, 8, 80)),
    0.5 * np.sin(np.linspace(0, 6, 60) + np.pi/4)
]
std_dev_series = [
    0.1 + 0.2 * np.random.rand(100),
    0.1 + 0.2 * np.random.rand(80),
    0.1 + 0.2 * np.random.rand(60)
]
labels = ['Sine Wave', 'Cosine Wave', 'Shifted Sine']

traces = []

colors = ['#1f77b4', '#ff7f0e', '#2ca02c']  # You can use any color palette

# Plot each series with its confidence interval
for i, series in enumerate(mean_series):
    label = labels[i]
    color = colors[i]
    x = np.linspace(0, len(series) - 1, len(series))
    lower_bound = series - 1.96 * std_dev_series[i]
    upper_bound = series + 1.96 * std_dev_series[i]
    
    # Line trace
    traces.append(go.Scatter(
        x=x,
        y=series,
        mode='lines',
        name=label,
        line=dict(width=2, color=color),
        legendgroup=label
    ))

    # Confidence interval (as a filled area)
    traces.append(go.Scatter(
        x=np.concatenate([x, x[::-1]]),
        y=np.concatenate([upper_bound, lower_bound[::-1]]),
        fill='toself',
        fillcolor=color,
        line=dict(color='rgba(255,255,255,0)'),
        showlegend=False,
        hoverinfo="skip",
        legendgroup=label,
        opacity=0.2
    ))

# Create the figure
fig = go.Figure(data=traces)

# Update layout for interactivity
fig.update_layout(
    title="Interactive Plotly Graph with Confidence Intervals",
    xaxis_title="X Values",
    yaxis_title="Mean Values",
    legend=dict(
        yanchor="middle",
        y=0.5,
        xanchor="left",
        x=1.05,
        font=dict(size=15)
    ),
    hovermode="x unified",
    template="plotly_white"
)

# Show the plot
fig.show()
