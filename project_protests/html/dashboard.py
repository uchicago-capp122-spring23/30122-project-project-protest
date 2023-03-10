####Task: Create HTML file using dash
###Author: JP Martinez & Monica Nimmagadda
###Last Modification: 03.05.2023

import dash
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from project_protests.html.text_inputs import HTML_TEXT , DATA_TEXT
from project_protests.visualizations.protest_viz import protest_by_city
from project_protests.visualizations.pairwise_viz import visualize_similarity
from project_protests.visualizations.news_viz import news_counts, month_corr
from project_protests.visualizations.sentiment_viz import visualize_sentiment_scores
from project_protests.visualizations.budget_viz import budget_viz
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.PULSE],suppress_callback_exceptions=True)

fig_protest = protest_by_city()
fig_similarity = visualize_similarity()
fig_news = news_counts()
fig_month_corr = month_corr()
fig_budget = budget_viz()
background_color = "background-color : rgb(255, 251, 250)"
style_h1 = {"padding":"25px", "text-align":"center", "border-width": "1px", "border-style": "solid"} 
style_p = {"padding":"10px","text-align":"left",
"margin-left":"5cm","margin-right":"5cm"}
style_h3 = {"text-align":"left","font":r"150% Arial", "text-decoration": "underline",
"font-weight":"bold","margin-left":"5cm","margin-right":"5cm"}  
style_h2 = {"text-align":"left","font-family":r"Arial", "text-decoration": "underline",
"font-weight":"bold","margin-left":"5cm","margin-right":"5cm"}
style_t = {"text-center":"center","font-family":r"Arial",
"font-weight":"bold","margin-left":"8cm","margin-right":"5cm"}


title_container = dbc.Container(
    fluid = True,
    style={
            "height": "60vh",
            "background-color": "rgb(40,40,43)",
            "color": "rgb(255, 251, 250)",
            "display": "flex",
            "flex-direction": "column",
            "justify-content": "center",
            "align-items": "center",
            "background": "url(https://static01.nyt.com/images/2020/06/10/us/10unrest-briefing-black-lives-matter/merlin_173249754_19a2cf59-a4a7-4bb9-8aaa-f910d7442ca3-superJumbo.jpg?quality=75&auto=webp)",
            "background-size": "cover",
        },
    children=[html.H1(HTML_TEXT["Title"],style = style_h1)]
)  

select_bar = dbc.Nav(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/", active="exact")),
        dbc.NavItem(dbc.NavLink("Data Collection and Analysis", href="/data", active="exact"))
    ],
    pills=True,
    fill=True,
)

content = html.Div(id="page-content",style={"margin":"50px"}, children = [])

app.layout = html.Div(style={'background-color': "rgb(255, 251, 250)",
    "color":"rgb(40,40,43)", "right-margin":"5cm","left-margin":"5cm"},
    children=[
    dcc.Location(id="url"),
    select_bar,
    title_container,
    content
])

@app.callback(
    [Output(component_id="sentiment_score_graph",component_property="figure")],
    [Input(component_id="select_section",component_property="value")]
)

def update_sentiment_graph(section):
    """
    Updated sentiment analysis graph according to the selective options
    Input:
    - section (str): Possible values of the dropdown for the graph
    Retur: Graph figure.
    """
    fig = visualize_sentiment_scores(section)
    return [fig]

@app.callback(
    [Output(component_id="page-content",component_property="children")],
    [Input(component_id="url",component_property="pathname")]
)
def render_page_content(pathname):
    """
    Function to determine the content of the different pages.
    Input:
    -pathname (str): Page to update.
    Output:
    List of HTML components that are included in the page to update.
    """
    if pathname == "/":
        return [[html.Br(),
                html.H2("Introduction",style = style_h2),
                html.P(HTML_TEXT["paragraphs"]["introduction"],style = style_p),
                html.P(HTML_TEXT["paragraphs"]["team"],style = style_p),
                html.H2(HTML_TEXT["subtitles"]["Number of protest"],style = style_h2),
                html.P(HTML_TEXT["graph_info"]["protest"], style=style_p),
                dcc.Graph(id="protest_number",figure=fig_protest),
                html.H2(HTML_TEXT["subtitles"]["News"], style=style_h2),
                html.P(HTML_TEXT["graph_info"]["news"], style=style_p),
                dcc.Graph(id="news_counts",figure=fig_news),
                html.P("To complement the analysis, we graphed the correlation matrix "
                "between the different variables, where it is posible to observe that " 
                "there is a positive correlation between the number of protests and " 
                "the number of news stories. This relationship was not as strong as we expected "
                "but again may be due to the upward spike in the protest data after 2020.", style = style_p),
                dcc.Graph(id="month_corr",figure=fig_month_corr),
                html.H2(HTML_TEXT["subtitles"]["Sentiment_Score"], style=style_h3),
                html.P(HTML_TEXT["graph_info"]["sentiment"], style=style_p),
                html.P(HTML_TEXT["graph_info"]["sentiment_2"], style=style_p),
                html.P(HTML_TEXT["graph_info"]["sentiment_3"], style=style_p),
                dcc.Dropdown(id="select_section",
                            options=[
                                {"label": "Headline", "value": "headline"},
                                {"label": "Lead Paragrah", "value": "lead_paragraph"},
                                ],
                            multi=False,
                            value="lead_paragraph",
                            style={'width': "40%","font":"Arial"}
                            ),
                dcc.Graph(id="sentiment_score_graph",figure={}),
                html.H2(HTML_TEXT["subtitles"]["Pairwise"], style=style_h3),
                html.P(HTML_TEXT["graph_info"]["pairwise"], style=style_p),
                dcc.Graph(id="News_pairwise",figure=fig_similarity),
                html.Br(),
                html.H2(HTML_TEXT["subtitles"]["Police"],style = style_h2),
                html.P(HTML_TEXT["graph_info"]["budget"], style=style_p),
                dcc.Graph(id="budget",figure=fig_budget),
                html.Br(),
                html.Br(),
                html.H2(HTML_TEXT["subtitles"]["Conclusion"],style = style_h2),
                html.P(DATA_TEXT["paragraphs"]["p11"],style = style_p), 
                html.P(DATA_TEXT["paragraphs"]["p12"],style = style_p), 
                            ]]
    elif pathname == "/data":
        return [[
                html.H1("Data description",
                        style=style_h1),
                html.H2("Protest Data",style = style_h2),
                html.P(DATA_TEXT["paragraphs"]["p1"],style = style_p),
                html.P(DATA_TEXT["paragraphs"]["tags_protest"],style = style_t),
                html.H2("Newspaper Data",style = style_h2),
                html.P(DATA_TEXT["paragraphs"]["p2"],style = style_p),
                html.P(DATA_TEXT["paragraphs"]["tags_news"],style = style_t),
                html.H2("Budget Data",style = style_h2),
                html.P(DATA_TEXT["paragraphs"]["p3"],style = style_t),
                html.H2("Sentiment Analysis",style = style_h2),
                html.P(DATA_TEXT["paragraphs"]["p4"],style = style_p),
                html.P(DATA_TEXT["paragraphs"]["p5"],style = style_p),
                html.P(DATA_TEXT["paragraphs"]["p6"],style = style_p),
                html.P(DATA_TEXT["paragraphs"]["p7"],style = style_p),
                html.H2("Pairwise correlation",style = style_h2),
                html.H3("Process", style=style_h3),
                html.P(DATA_TEXT["paragraphs"]["p8"],style = style_p),
                html.H3("Visualization", style=style_h3),
                html.P(DATA_TEXT["paragraphs"]["p9"],style = style_p),
                html.H3("Next Steps", style=style_h3),
                html.P(DATA_TEXT["paragraphs"]["p10"],style = style_p),
                ]]
    elif pathname == "/methods":
        return [[
                html.H1('Methodology description',
                        style={'textAlign':'center'}),
                
                ]]

if __name__ == "__main__":
    app.run_server(port=8059,debug = True)