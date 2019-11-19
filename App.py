import dash
import dash_html_components as html 
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from ML import costPredictor
from Graphs import TableWithEverything, ScatterAgeCharges, ScatterBmiCharges, ScatterSmokerCharges

app = dash.Dash(__name__)

sexe_options = ['Male', 'Female']

height_options = ['cm', 'ft']

weight_options = ['lbs', 'kg']

dependents_options = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

graph_options = [
    {'age': ScatterAgeCharges(),
    'bmi': ScatterBmiCharges(),
    'smoke': ScatterSmokerCharges()}
]

app.layout = html.Div([
   
#Title
    html.Div([
        html.Div('HealthLR', className='title')], 
        className='Header'),

    html.Div([
    html.Div([   
#Sexe radio button
    html.Div([
    html.Label('SEX'),
    dcc.RadioItems(
        id='sex',
        options=[{'label': i, 'value': i} for i in sexe_options]
    )], className = 'sex-radio'),
#Birthday textbox, calender
    html.Div([   
    html.Label('BIRTHYEAR'),
    dcc.Input(id='birthyear', value='', type='text')], className = 'birth-text'),
    
#Height textbox
    html.Div([ 
    html.Label('HEIGHT(cm)'),
    dcc.Input(id='height', value='', type='text')], className = 'height-text'),

#Weight textbox 
    html.Div([
    html.Label('WEIGHT(kg)'),
    dcc.Input(id='weight', value='', type='text')], className = 'weight-text'),

#Children dropdown
   html.Div([
   html.Label ('# OF CHILDREN'),
    dcc.Dropdown(
        id='children',
        options = [{'label':i, 'value' : i} for i in dependents_options],
    )], className = 'children-number-dropdown'),

#smoker
    html.Div([
    html.Label('SMOKER'),
    dcc.Dropdown(
        id='smoker',
        options=[
            {'label': 'Non-Smoker', 'value': '0'},
            {'label': 'Smoker', 'value': '1'}],
    )], className = 'smoker-dropdown')],

    className='bigbox'),

    html.Div( 
        html.Div(className = 'cost', id='predicted_charge'),
        className='cost-box'),

    html.Div('Data Exploration', className='graph-intro-title'),
    html.Div('Variables that affect health care charges to the insurer', className='graph-intro-text'),

    dcc.Dropdown(
        id="graphs",
        className='drop-graphs',
        options=[
            {'label': 'Age', 'value':'age'},
            {'label': 'Bmi', 'value':'bmi'},
            {'label': 'Smoke', 'value': 'smoke'}
        ], value = 'age'
    ),

    dcc.Graph(id="graph-output", className='graphs'),
    
    html.Div('Heatmap', className='heatmap-title'),
    html.Img(src=app.get_asset_url ('heatmap.jpg'), className = "heatmap"),

    html.Div('Dataset Sample', className='table-title'),
    html.Div([TableWithEverything()], className='table-box')],
    
    className='bigbigbox'),
])


@app.callback(
    Output('predicted_charge', 'children'),
    [Input('birthyear', 'value'),
    Input('height', 'value'),
    Input('weight', 'value'),
    Input('children', 'value'),
    Input('smoker', 'value')])
def save_info(birthyear, height, weight, children, smoker):
    if (birthyear == None or height == None or weight == None or children == None or smoker == None):
        return ""
    else:
        c = costPredictor(2019-int(birthyear), int(weight)/((int(height)/100)*(int(height)/100)), int(children), int(smoker))
        d = '{0:.2f}'.format(c[0])
        #c = costPredictor(35, 26.125, 0, 0)
        #print(c)
        return ('Predicted medical costs {}'.format(d))
        #return ('You have selected {} date, {} cm, {} kg, {} children, {}'.format(birthyear, height, weight, children, smoker) )

@app.callback(
    Output('graph-output', 'figure'),
    [Input('graphs', 'value')])
def update_graph(name_graph):
      if (name_graph == 'age'):
          return ScatterAgeCharges()
      elif (name_graph == 'bmi'):
          return ScatterBmiCharges()
      elif (name_graph == 'smoke'):
          return ScatterSmokerCharges()


if __name__ == '__main__':
    app.run_server(debug=True)