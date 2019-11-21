import dash 
import dash_table
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import pandas as pd 

#reading the dataset
df = pd.read_csv('health_insurance.csv')
#edits to the table to be displayed
#cutting charges to 2 decimals
df['charges'] = df['charges'].map(lambda x: '{0:.2f}'.format(x))
#cutting bmi to 1 decimal
df['bmi'] = df['bmi'].map(lambda x: '{0:.1f}'.format(x))
table = df.values

def DataScatterPlot(dataframe, xi, yi):
    return px.scatter(dataframe, x=xi, y=yi, height=500, width=500)

def DataTable():
    return dash_table.DataTable(
                id='table',
                columns=[{'name': i, 'id': i} for i in df.columns],
                data=df.to_dict('records'),
                fixed_rows={'headers': True, 'data': 0},
                style_cell={
                    'whiteSpace': 'normal',
                    'textAlign': 'left'
                },
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                },
                style_data_conditional=[
                    {'if': {'column_id': 'age'}, 'width': '50px'},
                    {'if': {'column_id': 'sex'}, 'width': '50px'},
                    {'if': {'column_id': 'bmi'}, 'width': '50px'},
                    {'if': {'column_id': 'children'}, 'width': '50px'},
                    {'if': {'column_id': 'smoker'}, 'width': '50px'},
                    {'if': {'column_id': 'region'}, 'width': '50px'},
                    {'if': {'column_id': 'charges'}, 'width': '50px'},
                ],
                virtualization=True
            )

def ScatterAgeCharges():
    return px.scatter(df, x='age', y='charges', height=500, width=500)

def ScatterBmiCharges():
    return px.scatter(df, x='bmi', y='charges', height=500, width=500)

def ScatterSmokerCharges():
    return px.scatter(df, x='smoker', y='charges', height=500, width=500)

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H4(children='Health costs'),
    html.Div('chares by age graph'),
    dcc.Graph(id='scatterAgeCharges', figure= DataScatterPlot(df,'age', 'charges')),
    html.Div('charges by bmi graph'),
    dcc.Graph(id='scatterBmiCharges', figure= DataScatterPlot(df,'bmi', 'charges')),
    html.Div('charges by smoker graph'),
    dcc.Graph(id='scatterSmokerCharges', figure= DataScatterPlot(df, 'smoker', 'charges')),
    DataTable()
])

if __name__ == '__main__':
    app.run_server(debug=True)