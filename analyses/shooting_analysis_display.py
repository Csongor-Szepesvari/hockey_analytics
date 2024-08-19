# Shooting analysis display
'''
We're going to import the data we get from shooting analysis and use this separate file to display them.
We do this because we need to run an instance of matplotlib instead of just grabbing a screengrab which is how it works in the notebook.

Our goals are:
    - Create a search bar, so we can manipulate the data live
    - Have a hover feature that highlights the line of a player when they are being hovered on.
'''
import numpy as np
import pandas as pd
import dash
from dash import dcc, html, Input, Output

import plotly.graph_objs as go
# Create data for the plot

# import all the data from the shooting_analysis document to be able to work with it here
undiscounted = pd.read_csv("simple_analysis_all_positions.csv")

# lets consider what our filters are going to be, our natural filters from the data are:
# games played
# position
# shooting pct
# size of random sample to display within that category

# we need to make a box for all of these 


# then we also need a way to chop the first x games
CHOP = 100

# figure out a way to retrieve per player series to be able to extract labels
mean_undiscounted = undiscounted.groupby("name_position")['cumulative_mean'].apply(lambda x: np.array(list(map(float, x)))).values
#print(mean_undiscounted)
std_undiscounted = undiscounted.groupby("name_position")['cumulative_std'].apply(lambda x: np.array(list(map(float, x)))).values
#print(std_undiscounted)
names_array = undiscounted.groupby('name_position')['name_position'].apply(lambda x: x.iloc[0]).values
#print(names_array)

colors = [
    "#1f77b4",  # Blue
    "#ff7f0e",  # Orange
    "#2ca02c",  # Green
    "#d62728",  # Red
    "#9467bd",  # Purple
    "#8c564b",  # Brown
    "#e377c2",  # Pink
    "#7f7f7f",  # Gray
    "#bcbd22",  # Olive
    "#17becf",  # Teal
    "#393b79",  # Dark Blue
    "#637939",  # Dark Green
    "#8c6d31",  # Dark Brown
    "#843c39",  # Dark Red
    "#7b4173",  # Dark Purple
    "#a55194",  # Magenta
    "#ce6dbd",  # Light Pink
    "#9c9ede",  # Light Blue
    "#c7c7c7",  # Light Gray
    "#dbdb8d"   # Light Olive
]


# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the Dash app
app.layout = html.Div([
    dcc.Input(
        id='name-input-box', type='text', value='',
        placeholder='Enter a player name to display'
    ),
    dcc.Input(
        id='games-played-box', type='number', value=0,
        placeholder='Display starting at this many games played'
    ),
    dcc.Graph(id='interactive-plot')
])

# Callback to update the graph based on input
@app.callback(
    Output('interactive-plot', 'figure'),
    Input('name-input-box', 'value'),
    Input('games-played-box', 'value')
)


def update_graph(search_term, games_played):
    print(search_term)
    print(games_played)
    if games_played:
        CHOP = games_played
    else:
        CHOP = 0
    # Plot each series with its confidence interval
    def display_plot(mean_series, std_dev_series, labels, colors, number_to_display):
        if number_to_display > len(labels):
            _mean_series = mean_series
            _std_dev_series = std_dev_series
            _labels = labels
        else:
            _mean_series = mean_series[:number_to_display]
            _std_dev_series = std_dev_series[:number_to_display]
            _labels = labels[:number_to_display]
        big_colors = colors * ((number_to_display//len(colors))+1) 
        traces = []
        for i, series in enumerate(_mean_series):
            
            label = _labels[i]
            color = big_colors[i]

            #print(label)
            
            if len(search)>3 and search in label.lower() and CHOP < _mean_series[i].size:
                #print(search, label.lower())

                means = np.array(_mean_series[i][CHOP:])
                stds = np.array(_std_dev_series[i][CHOP:])
                x = [CHOP+j for j in range(means.size)]
                #print(label, series, "\n\n\n\n", type(_std_dev_series[i]))
                lower_bound = means - 1.96 * stds
                upper_bound = means + 1.96 * stds
                
                # Line trace
                traces.append(go.Scatter(
                    x=x,
                    y=means,
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
            xaxis_title="Games played",
            yaxis_title="Estimated mean shooting %",
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

        # Return the figure to show
        return fig
    
    search = search_term.lower()

    return display_plot(mean_series=mean_undiscounted, std_dev_series=std_undiscounted, labels=names_array, colors=colors, number_to_display=1500)


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
