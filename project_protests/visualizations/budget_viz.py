"""
Lisette Solis 
"""
import pandas as pd 
import plotly.express as px 
import plotly.graph_objects as go
import pathlib
from project_protests.visualizations.protest_viz import protest_data
from project_protests.police_budget.budget_analysis import load_budget_data

def budget_viz():
    """
    Visualization of per capita police spending year over year 

    Return: Plotly figure
    """
    # create traces for figure 
    traces = []
    dropdowns = []
    buttons = []

    df = load_budget_data()
    df.drop(df.index[(df["Type"] == "Total") | (df["Type"] == "Population")], 
            inplace=True)
    df.drop(columns=["Type"], inplace=True)
    df = df.melt(id_vars="City", value_name="Total")

    # add traces for cities
    cities = list(df["City"].unique())
    for city in cities:
        sub_df = df.loc[df['City'] == city]
        trace = go.Scatter( 
                x=sub_df['variable'],
                y=sub_df['Total'], 
                name=city,
                mode='lines')
        traces.append(trace)
        dropdowns.append({'label': city, 'value':trace})
    # add dropdown options     
    for i, dropdown in enumerate(dropdowns):
        visible = [False] * len(dropdowns)
        visible[i] = True
        buttons.append({'args': [{'visible': visible}],
                        'label': dropdowns[i]['label'], \
                        'method': 'restyle'
                        })
    # define layout 
    initial_layout = go.Layout(
        updatemenus=[{'buttons': buttons,
            'direction': 'down',
            'showactive': True,
            'x': 0.1,
            'y': 1.2
                }
            ],
        xaxis=dict(title='Year'),
        yaxis=dict(title='Count'),
        title="Per Capita Police Budget", title_x=0.5,
        template="simple_white", 
            )
    # Create the figure with the traces and layout
    fig = go.Figure(data=traces, layout=initial_layout)
    # Change colors
    colors = ['#98A4D7', '#7BAE82', '#1e4477', '#F0CF56', '#9B5B41', '#3F367A', '#4D797D', \
        '#98A4D7', '#7BAE82', '#1e4477', '#F0CF56', '#9B5B41', '#3F367A', '#4D797D']
    for i,_ in enumerate(fig.data):
        fig.data[i].marker.color = colors[i]
    return fig
