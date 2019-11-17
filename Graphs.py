import dash 
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import pandas as pd 


df = pd.read_csv('health_insurance.csv')
table = df.values

def DataTable(dataframe, max_rows=10):
    header = []
    for col in dataframe.columns:
        header.append(html.Th(col))
    header = html.Tr(header)

    rows = []
    for i in range(min(len(dataframe), max_rows)):
        row = []
        for col in dataframe.columns:
            row.append(html.Td(dataframe.iloc[i][col]))
        rows.append(html.Tr(row))
    
    return html.Table([
        html.Thead(header),
        html.Tbody(rows)
    ])

def DataScatterPlot(dataframe, xi, yi):
    return px.scatter(dataframe, x=xi, y=yi, height=500, width=500)
  
#def DataDensityPlot():
def TableWithEverything(max_rows=10):
    header = []
    for col in df.columns:
        header.append(html.Th(col))
    header = html.Tr(header)

    rows = []
    for i in range(min(len(df), max_rows)):
        row = []
        for col in df.columns:
            row.append(html.Td(df.iloc[i][col]))
        rows.append(html.Tr(row))
    
    return html.Table([
        html.Thead(header),
        html.Tbody(rows)
    ], className='table')


def ScatterAgeCharges():
    return px.scatter(df, x='age', y='charges', height=500, width=500)

def ScatterBmiCharges():
    return px.scatter(df, x='bmi', y='charges', height=500, width=500)

def ScatterSmokerCharges():
    return px.scatter(df, x='smoker', y='charges', height=500, width=500)

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H4(children='Health costs'),
    DataTable(df),
    html.Div('chares by age graph'),
    dcc.Graph(id='scatterAgeCharges', figure= DataScatterPlot(df,'age', 'charges')),
    html.Div('charges by bmi graph'),
    dcc.Graph(id='scatterBmiCharges', figure= DataScatterPlot(df,'bmi', 'charges')),
    html.Div('charges by smoker graph'),
    dcc.Graph(id='scatterSmokerCharges', figure= DataScatterPlot(df, 'smoker', 'charges'))
])

if __name__ == '__main__':
    app.run_server(debug=True)