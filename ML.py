import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
import statsmodels.api as sm


data = pd.read_csv("health_insurance.csv")



x = data.iloc [:, :-1]
y = data.iloc [:,-1]

x = x.drop ('sex', axis = 1)

smoker = pd.get_dummies(x['smoker'], drop_first = True)
x = x.drop('smoker', axis = 1)
x = pd.concat([x, smoker], axis = 1)

x = x.drop ('region', axis = 1)



x_train, x_test, y_train, y_test = train_test_split (x, y, test_size=0.2, random_state=1)

from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(x_train, y_train)

X2 = sm.add_constant(x_train)
est = sm.OLS(y_train, X2)
est2 = est.fit()
#print(est2.summary())

#print(x_test)
#print(y_test)

yPredict = regressor.predict(x_test)

from sklearn.metrics import r2_score
score=r2_score(y_test,yPredict)

def costPredictor(age, bmi, children, smoke):
    data = np.array([[age, bmi, children, smoke]])
    #frame = pd.DataFrame({'age': data[:, 0], 'bmi': data[:,1], 'children': data[:,2], 'yes': data[:,3]})
    return regressor.predict(data)

#print(score)

#print(costPredictor(22, 30, 0, 0))