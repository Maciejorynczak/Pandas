import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

# Wczytanie danych
data_xlsx = pd.read_excel('default_of_credit_card_clients.xlsx', header=1)

# Podział danych: cechy (X) i zmienna docelowa (y)
X = data_xlsx.drop(['ID', 'default payment next month'], axis=1)
y = data_xlsx['default payment next month']

# Podział na dane treningowe i testowe (80% treningowe, 20% testowe)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Definicja modelu Drzewa Decyzyjnego
dt = DecisionTreeClassifier(random_state=42)

# Hiperparametry dla GridSearch
param_grid_dt = {
    'max_depth': [5, 10, 15],
    'min_samples_split': [10, 20, 50]
}

# Użycie GridSearch do optymalizacji hiperparametrów
grid_search_dt = GridSearchCV(dt, param_grid_dt, cv=5, scoring='accuracy', n_jobs=-1, verbose=1)
grid_search_dt.fit(X_train, y_train)

# Wyświetlenie najlepszych parametrów
print(f"Najlepsze hiperparametry dla Drzewa Decyzyjnego: {grid_search_dt.best_params_}")

# Predykcja na zbiorze testowym
y_pred_dt = grid_search_dt.predict(X_test)

# Raport klasyfikacyjny
print("Raport klasyfikacyjny dla Drzewa Decyzyjnego:")
print(classification_report(y_test, y_pred_dt))

# Definicja modelu Lasu Losowego
rf = RandomForestClassifier(random_state=42)

# Hiperparametry dla GridSearch dla Lasu Losowego
param_grid_rf = {
    'n_estimators': [100, 200],
    'max_depth': [5, 10, 15],
    'min_samples_split': [10, 20]
}

# Optymalizacja hiperparametrów dla Lasu Losowego
grid_search_rf = GridSearchCV(rf, param_grid_rf, cv=5, scoring='accuracy', n_jobs=-1, verbose=1)
grid_search_rf.fit(X_train, y_train)

# Najlepsze hiperparametry dla Lasu Losowego
print(f"Najlepsze hiperparametry dla Lasu Losowego: {grid_search_rf.best_params_}")

# Predykcja na zbiorze testowym dla Lasu Losowego
y_pred_rf = grid_search_rf.predict(X_test)

# Raport klasyfikacyjny dla Lasu Losowego
print("Raport klasyfikacyjny dla Lasu Losowego:")
print(classification_report(y_test, y_pred_rf))

# Zapisanie najlepszego modelu
joblib.dump(grid_search_rf.best_estimator_, 'best_random_forest_model.pkl')
print("Model został zapisany jako 'best_random_forest_model.pkl'")
