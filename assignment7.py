import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

df = pd.read_csv('Assignment7/FifaSats.csv')

winner_counts = df['Winner'].value_counts().reset_index()
winner_counts.columns = ['Country', 'Wins']



app = Dash(__name__)
server = app.server
app.layout = html.Div([
    html.H1('FIFA World Cup Dashboard'),

    html.H2('World Cup Winners'),
    dcc.Graph(id='map'),

    html.H2('Select a country to See Win Count'),
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': i, 'value': i} for i in sorted(df['Winner'].unique())],
        value='Brazil'
    ),
    html.Div(id='win-count-output', style={'margin':'10px'}),
    
    html.H2('Select a Year to See Final Results'),
    dcc.Slider(
        id='year-slider',
        min=df['Year'].min(),
        max=df['Year'].max(),
        step=None,
        marks={int(year): str(year) for year in df['Year'].sort_values()},
        value=2022
    ),
    html.Div(id='final-result-output', style={'margin':'10px'})
])

@app.callback(
    Output('map', 'figure'),
    Input('country-dropdown', 'value')
)

def update_map(_):
    fig = px.choropleth(
    winner_counts,
    locations='Country',
    locationmode='country names',
    color='Wins',
    hover_name='Country',
    color_continuous_scale='Viridis',
    title='FIFA World Cups Winners by Country'
)
    return fig

@app.callback(
    Output('win-count-output', 'children'),
    Input('country-dropdown', 'value')
)
def update_win(country):
    count = df['Winner'].str.count(country).sum()
    return f'{country} has won the FIFA World Cup {count} times.'

@app.callback(
    Output('final-result-output', 'children'),
    Input('year-slider', 'value')
)
def update_final(year):
    row = df[df['Year'] == year].iloc[0]
    return f'The {year} FIFA World Cup winner was {row["Winner"]} and the runner up was {row["Runner Up"]}'

if __name__ == '__main__':
    app.run(debug=False, port=8051)
