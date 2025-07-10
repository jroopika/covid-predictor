import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import pickle

df = pd.read_csv("model/data.csv", encoding='latin1')
df = df.dropna()

X = df[['Fever', 'Tiredness', 'Dry-Cough', 'Difficulty-in-Breathing', 'Sore-Throat', 'Age']]
y = df['COVID-19']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = DecisionTreeClassifier()
model.fit(X_train, y_train)

with open("model/covid_model.pkl", "wb") as file:
    pickle.dump(model, file)
