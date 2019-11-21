import dash
import dash_html_components as html 
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from ML import costPredictor
#Graph contains the functions to display the Graphs
from Graphs import DataTable, ScatterAgeCharges, ScatterBmiCharges, ScatterSmokerCharges

app = dash.Dash(__name__)

server=app.server #needed to heroku deployment

#lists of options need to for the radio buttons and Dropdowns
sex_options = ['Male', 'Female']
dependents_options = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

#layout of the app starts here
app.layout = html.Div([
   
#Header
    html.Div([
        html.Div('HealthLR', className='title')], 
        className='Header'),
    html.Div([

    html.Div([   
        #Div Component that constains:
        #1. Sex radio buttons
        #2. Birthyear textbox
        #3. Height textbox
        #4. Weight textbox
        #5. Children Dropdown
        #6. Smoker radio buttons
#Sex radio button
    html.Div([
    html.Label('SEX'),
    dcc.RadioItems(
        id='sex',
        options=[{'label': i, 'value': i} for i in sex_options]
    )], className = 'sex-radio'),
#Birthyear textbox
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
        options = [{'label':i, 'value' : i} for i in dependents_options], #Uses the list of options dependents_options
    )], className = 'children-number-dropdown'),

#Smoker radio buttons
#Value of 0 or 1 for ease of use when using linear regression
    html.Div([
    html.Label('SMOKER'),
    dcc.Dropdown(
        id='smoker',
        options=[
            {'label': 'Non-Smoker', 'value': '0'}, #value of non-smoker is 0
            {'label': 'Smoker', 'value': '1'}], #value of smoker is 1
    )], className = 'smoker-dropdown')],

    className='bigbox'),

#Area where the health care costs appear
#Initalially will stay blank
#The cost appears after all the fields are entered
    html.Div( 
        html.Div(className = 'cost', id='predicted_charge'),
        className='cost-box'),

#Section where the graphs are tables are 
    html.Div('Data Exploration', className='graph-intro-title'),
    html.Div('Variables that affect health care charges to the insurer', className='graph-intro-text'),

#Dropdown to display selected graph
#A callback we will be ran depending on the value of the Dropdown
#to display the corresponding graph
    dcc.Dropdown(
        id="graphs",
        className='drop-graphs',
        options=[
            {'label': 'Age', 'value':'age'},
            {'label': 'Bmi', 'value':'bmi'},
            {'label': 'Smoke', 'value': 'smoke'}
        ], value = 'age'
    ),
#Location where the graphs will be displayed.
#Default graph is 'age', because the Dropdown default value is 'age'.
#Callback gives this Graph component a figure property 
# correspoding to the same value from Dropdown.
    dcc.Graph(id="graph-output", className='graphs'),

#Heatmap image    
    html.Div('Heatmap', className='heatmap-title'),
    html.Img(src=app.get_asset_url ('heatmap.jpg'), className = "heatmap"),

#Table
#The function that builds the table is located in Graphs.py.
#The DataTable is contained in a Div Component, 
#so it is easier to size and position using CSS
    html.Div('Dataset Sample', className='table-title'),
    html.Div([DataTable()], className='table-box')],
    
    className='bigbigbox'),

    html.Div(className='Footer'),
])

#callback that takes as input birthyear, height, weight, children, smoker
# and outputs a string to 'predicted_charge', where the predicted health care charges
# is calculated using the equation obtained from the multiple linear regression in the ML.py file
@app.callback(
    Output('predicted_charge', 'children'),
    [Input('birthyear', 'value'),
    Input('height', 'value'),
    Input('weight', 'value'),
    Input('children', 'value'),
    Input('smoker', 'value')])
def save_info(birthyear, height, weight, children, smoker):
#An empty string is returned as long as there is 1 field that is empty.
    if (birthyear == None or height == None or weight == None or children == None or smoker == None):
        return ""
    else:
#The equation takes the age, bmi, #children and smoker.
#The age is calculated using the inputed birthyear.
#The bmi is calculated using the inputed weight and height. weight(kg)/(height(m)^2)
        c = costPredictor(2019-int(birthyear), int(weight)/((int(height)/100)*(int(height)/100)), int(children), int(smoker))
#Decimals for the predicted cost is reduced to 2
        d = '{0:.2f}'.format(c[0])
        return ('Predicted medical costs {}'.format(d))

#callback that takes input from the graph dropdown, 
# and outputs the corresponding graph figure to the graph component
@app.callback(
    Output('graph-output', 'figure'),
    [Input('graphs', 'value')])
#The figures are imported from the Graphs.py file
def update_graph(name_graph):
      if (name_graph == 'age'):
          return ScatterAgeCharges()
      elif (name_graph == 'bmi'):
          return ScatterBmiCharges()
      elif (name_graph == 'smoke'):
          return ScatterSmokerCharges()

if __name__ == '__main__':
    app.run_server(debug=True)