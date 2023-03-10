"""
Lisette Solis 
"""
import pandas as pd 
import plotly.express as px 
import plotly.graph_objects as go
import pathlib

def protest_data():
    """
    Create data frame from the CSV of aggregate protest data
    """
    filepath = pathlib.Path(__file__).parent.parent.parent / "project_protests/protest/police-data.csv"
    df = pd.DataFrame(pd.read_csv(filepath),\
        columns = ['Location', 'Date', 'County', 'StateTerritory','City_Town'])
    df['Date']= pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.month
    df['Year'] = df['Date'].dt.year 
    return df


def protest_by_city():
    """
    Visualization of the number of protests year over year at the national level and 
    for the eight cities with highest per capita spending. 

    Returns: Plotly figure
    """
    df = protest_data()
    # Agregate data at the national level 
    df_national = df.groupby(['Year']).size().to_frame().reset_index()
    df_national.rename(columns={0:'Count'}, inplace=True)

    # pivot data for cities
    cities = ['Baltimore', 'New York', 'Chicago', 'Detroit', 'Atlanta', 'Los Angeles', 'Minneapolis', 'Houston']
    cities.sort()
    df_cities = df.loc[df['City_Town'].isin(cities)]
    df_pivot = df_cities.groupby(['Year', 'City_Town']).size().to_frame().reset_index()
    df_pivot.rename(columns={0:'Count'}, inplace=True)

    # create traces for figure 
    traces = []
    dropdowns = []
    buttons = []
    # Add trace for national data
    trace = (go.Scatter(x=df_national["Year"], 
                    y=df_national['Count'], 
                    name='National', 
                    mode="lines"))
    traces.append(trace)
    dropdowns.append({'label': 'National', 'value':trace})
    # Add trace for each city
    for i, city in enumerate(cities):
        sub_df = df_pivot.loc[df_pivot['City_Town'] == city]
        trace = go.Scatter(x=sub_df["Year"], 
                            y=sub_df['Count'], 
                            name=city, 
                            mode="lines")        
        traces.append(trace)
        dropdowns.append({'label': city, 'value':trace})

    # add dropdown options
    for i, dropdown in enumerate(dropdowns):
        visible = [False] * len(dropdowns)
        visible[i] = True
        buttons.append({'args': [{'visible': visible}],
                        'label': dropdowns[i]['label'], 
                        'method': 'restyle'
                        })
    # define initial layout
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
        title="Protests by Year", title_x=0.5,
        template="simple_white", 
            )
    #create the figure with the traces and initial layout
    fig = go.Figure(data=traces, layout=initial_layout)
    # upodate colors 
    colors = ['#98A4D7', '#7BAE82', '#1e4477', '#F0CF56', '#9B5B41', '#3F367A', '#4D797D', \
        '#98A4D7', '#7BAE82', '#1e4477', '#F0CF56', '#9B5B41', '#3F367A', '#4D797D']
    for i,_ in enumerate(fig.data):
        fig.data[i].marker.color = colors[i]

    return fig
