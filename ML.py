import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
import statsmodels.api as sm

#pandas dataframe
data = pd.read_csv("health_insurance.csv")
#columns order: age, sex, bmi, children, smoker, region, charges
#slicing the dataframe
#for the x we want all the rows, all columns except charges(last column)
x = data.iloc [:, 0:-1]
#for the y we wall all the rows, and only the charges column(last column)
y = data.iloc [:,-1]

#based on the heatmap, the sex and the region columns have no correlation to health care charges.
#sex and region columns are dropped from the dataframe
x = x.drop ('sex', axis = 1)
x = x.drop ('region', axis = 1)

#the smoker column is filled with yes and no, so it needs to be converted to 1 and 0
smoker = pd.get_dummies(x['smoker'], drop_first = True)
#after making the dummy smoker we can drop the current one and concat the new smoker column
x = x.drop('smoker', axis = 1)
x = pd.concat([x, smoker], axis = 1)

#the dataframe is split into train and test. 80% of the dataframe is in train and 20% is in test
x_train, x_test, y_train, y_test = train_test_split (x, y, test_size=0.2, random_state=1)

#Linear regression
from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(x_train, y_train)

X2 = sm.add_constant(x_train)
est = sm.OLS(y_train, X2)
est2 = est.fit()

#information on the linear regression:
#print(est2.summary())

#testing the linear regression
yPredict = regressor.predict(x_test)
from sklearn.metrics import r2_score
#comparing the y from the test set and the predicted y obtained from the x test set
score=r2_score(y_test,yPredict)
print(score) #r^2 : 0.76

#function to predict the health care charges.
#to be exported to App.py
def costPredictor(age, bmi, children, smoke):
    data = np.array([[age, bmi, children, smoke]])
    return regressor.predict(data)

#testing the prediction
#print(costPredictor(22, 30, 0, 0))