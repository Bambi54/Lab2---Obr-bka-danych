import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score
import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials
import json

# generowanie prostego zbioru danych
def generate_data():

    # generowanie ilości punktów dla chmur
    num_points1 = np.random.randint(50, 101)
    num_points2 = np.random.randint(50, 101)
    
    # środek chmury
    cluster1_center = [0, 0]
    cluster2_center = [10,10]

    # odchylenie standardowe punktów
    std_dev1 = 1.5
    std_dev2 = 1.5

    # generowanie punktów
    cluster1 = np.random.normal(loc=cluster1_center, scale=std_dev1, size=(num_points1, 2))
    cluster2 = np.random.normal(loc=cluster2_center, scale=std_dev2, size=(num_points2, 2))

    # tworzenie etykiet dla klas
    labels1 = np.zeros(num_points1)
    labels2 = np.zeros(num_points2)
    
    return np.vstack((cluster1, cluster2)), np.concatenate((labels1, labels2))


def get_data_from_google_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials_info = json.loads(os.getenv("GOOGLE_SHEETS_CREDENTIALS_JSON"))
    creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_info, scope)
    client = gspread.authorize(creds)

    pass

# trenowanie prostego modelu regresji logistycznej
def train_model():
    # Podział na zbiór treningowy i testowy
    data, labels = generate_data()

    x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.3)

    # Trenowanie modelu
    log_reg = LinearRegression().fit(x_train, y_train)
    
    # Predykcja na zbiorze testowym
    y_pred = log_reg.predict(x_test)
    
    # Wyliczenie dokładności
    accuracy = accuracy_score(y_test, y_pred)

    # Zapis wyniku
    print(f"Model trained with accuracy: {accuracy * 100:.2f}%")
    with open('accuracy.txt', 'w') as file:
        file.write(f'{accuracy * 100:.2f}')


if __name__ == "__main__":
    get_data_from_google_sheet()