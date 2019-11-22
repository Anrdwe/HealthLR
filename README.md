# HealthLR

## Link to the web app
Access the website [here](https://warm-retreat-63434.herokuapp.com/)

## Made during McGill CodeJam 2019, November 16th 2019
for the Plotly, dash app challenge and Intact Insurance challenge.

## Built with
- Dash by Plotly

## Project folder structure
'/' contains the main files that make up the app: App.py, Graphs.py and ML.py <br>
'/assets' contains the css styling and images

## 3 python files:
1. App.py
2. Graphs.py
3. ML.py

## 1. App.py
Contains the App layout:
1. Sex radio button
2. Birthyear textbox
3. Height textbox
4. Weight textbox
5. Children dropdown
6. Smoker dropdown
7. Graph selection dropdown
8. Graph Component
9. Heatmap image Component
10. DataTable component

## 2. Graphs.py
Contains the functions that make the graphs and tables <br>
Functions exported to App.py:
1. ScatterAgeCharges()
2. ScatterBmiCharges()
3. ScatterSmokerCharges()
4. DataTable()

## 3. ML.py
Contains the Linear Regression to predict health care charges <br>
Function exported to App.py
1. costPredictor(age, bmi, children, smoker)
