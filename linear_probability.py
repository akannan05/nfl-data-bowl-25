import pandas as pd
import numpy as np

from sklearn.linear_model import LogisticRegression

model = LogisticRegression()

data = pd.read_csv("C:/Users/anime/Downloads/yac data.csv")

data = data.fillna(0)

from sklearn.model_selection import train_test_split

X = data.drop('Outcome', axis = 1)
y = data['Outcome']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

model.fit(X_train, y_train)

predictions = model.predict_proba(X_test)

binary_predictions = []

for x in predictions:

    if x[1] >= 0.5:

        binary_predictions.append(1)

    else:

        binary_predictions.append(0)

import matplotlib.pyplot as plt

plt.hist(binary_predictions)

plt.show()
#print(classification_report(y_test, binary_predictions))