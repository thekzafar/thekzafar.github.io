import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np
from sklearn import metrics
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

# read data

data = pd.read_csv('Advertising.csv', index_col=0)
TV = data.TV
Radio = data.Radio
Newspaper = data.Newspaper
Sales = data.Sales
print(data.head())

# check the shape(rows, columns)
print(data.shape)

plt.scatter(TV, Sales, c='r', marker='*', label='TV')
plt.scatter(Radio, Sales, c='b', marker='.', label='Radio')
plt.scatter(Newspaper, Sales, c='g', marker='3', label='Newspaper')
plt.legend()
plt.ylabel("Sales")
plt.xlabel("Advertising Spend")
plt.grid(linestyle='-.')
plt.show()


col = ['TV', 'Radio', 'Newspaper']

# 2、Standardization of data processing
min_max_scalar = MinMaxScaler()
data_new = min_max_scalar.fit_transform(X=data)

# use the list to select a subset of the original df
x = data[col]

print(type(x))
print(x.shape)

y = data.Sales
print(y.head())

x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1)
print(x_train.shape)
print(y_train.shape)
print(x_test.shape)
print(y_test.shape)

# instantiate
linreg = LinearRegression()

# find the coefficients
linreg.fit(x_train, y_train)
# print the intercept and coefficients
print(linreg.intercept_)
print(linreg.coef_)

list(zip(col, linreg.coef_))

# predictions
y_pred = linreg.predict(np.array(x_test))
print(np.sqrt(metrics.mean_squared_error(y_test, y_pred)))

# accuracy
score = linreg.score(x_test, y_test)
print("Accuracy :{:.2%}".format(score))

# plot
t = np.arange(len(x_test))
plt.plot(t, y_test, 'r-', linewidth=2, label='Test')
plt.plot(t, y_pred, 'b-', linewidth=2, label='Predict')
plt.legend()
plt.show()



