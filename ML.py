import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
import statsmodels.api as sm

#pandas dataframe
data = pd.read_csv("health_insurance.csv")

#columns order: age, sex, bmi, children, smoker, region, charges
#slicing the dataframe
#for the x(independant variables) we want all the rows, all columns except charges(last column)
x = data.iloc [:, 0:-1]
#for the y(dependant variable) we want all the rows, and only the charges column(last column)
y = data.iloc [:,-1]

#based on the heatmap, the sex and the region columns have no correlation to health care charges.
#sex and region columns are dropped from the dataframe
x = x.drop ('sex', axis = 1)
x = x.drop ('region', axis = 1)

#the smoker column is filled with yes and no, so it needs to be converted to 1 and 0
#get_dummies splits the smoker column into two new colums: "yes" and "no" and drops the first column.
#smoker status is then represented by 1s and 0s where 1 == smoker and 0 == non-smoker under a new column "yes"
#The column smoker is then dropped from the dataframe and the new column: "yes", is concatenated to the dataframe.
smoker = pd.get_dummies(x['smoker'], drop_first = True)
x = x.drop('smoker', axis = 1)
x = pd.concat([x, smoker], axis = 1)

#the dataframe is split into train and test. 80% of the dataframe is in train and 20% is in test
#We include a random state so the same sequence of random splitting is performed to allow for reproducible results
x_train, x_test, y_train, y_test = train_test_split (x, y, test_size=0.2, random_state=1)

#Multiple linear regression
from sklearn.linear_model import LinearRegression
regressor = LinearRegression()

#trains the algorithm
regressor.fit(x_train, y_train)

X2 = sm.add_constant(x_train)
est = sm.OLS(y_train, X2)
est2 = est.fit()

#information on the linear regression:
#print(est2.summary())

#testing the linear regression
yPredict = regressor.predict(x_test)
from sklearn.metrics import r2_score
#Calculating the r^2 coefficient of determination.
#based on observed values (y_test) and predicted values based on our multiple regression model(yPredict)
score=r2_score(y_test,yPredict)
print(score) #r^2 : 0.76

#function to predict the health care charges.
#to be exported to App.py
def costPredictor(age, bmi, children, smoke):
    data = np.array([[age, bmi, children, smoke]])
    return regressor.predict(data)

#testing the prediction
#print(costPredictor(22, 30, 0, 0))