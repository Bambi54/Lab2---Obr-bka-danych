import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import json, time, logging, gspread, sys


def get_data_from_google_sheet():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('log.txt', mode='w'),
            logging.StreamHandler(sys.stdout)
        ]
    )

    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    logging.info("Pobieranie danych logowania")
    with open('credentials.json', 'r') as f:
        credentials_info = json.load(f)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_info, scope)

    logging.info("Logowanie do API Google")
    client = gspread.authorize(creds)
    sheet = client.open("ASI LAB2").sheet1

    csv_file_path = 'external-repo/data_student_25347.csv'
    logging.info("Wczytywanie danych csv")
    data = pd.read_csv(csv_file_path)

    missing_records = data.isna().sum().sum()
    logging.info("Ilość brakujących rekordów: %s", missing_records)

    logging.info("Usuwanie kolumn z ilością braków > 50%")
    data.dropna(thresh=3.5, inplace=True)


    logging.info("Usunięto: %s", missing_records - data.isna().sum().sum())
    missing_records = data.isna().sum().sum()

    logging.info("Obliczanie średniej zarobków")
    mean_avg_sal = round(data[data['Średnie Zarobki'] > 0]['Średnie Zarobki'].mean(), 2)

    logging.info("Uzupełnianie braków w kolumnie: Średnie Zarobki")
    data['Średnie Zarobki'] = data['Średnie Zarobki'].fillna(mean_avg_sal)

    logging.info("Uzupełniono: %s", missing_records - data.isna().sum().sum())
    missing_records = data.isna().sum().sum()

    logging.info("Obliczanie średniego wieku")
    mean_age = round(data[data['Wiek'] > 0]['Wiek'].mean())

    logging.info("Uzupełnianie braków w kolumnie: Wiek")
    data['Wiek'] = data['Wiek'].fillna(mean_age)

    logging.info("Uzupełniono: %s", missing_records - data.isna().sum().sum())
    missing_records = data.isna().sum().sum()

    logging.info("Obliczanie najczęstszej wartości kolumny: Cel Podróży")
    common_travel = data['Cel Podróży'].mode()[0]

    logging.info("Uzupełnianie braków w kolumnie: Cel Podróży")
    data['Cel Podróży'] = data['Cel Podróży'].fillna(common_travel)

    logging.info("Uzupełniono: %s", missing_records - data.isna().sum().sum())
    missing_records = data.isna().sum().sum()

    logging.info("Usuwanie pozostałych rekordów z brakami")
    data.dropna(inplace=True)

    logging.info("Usunięto: %s", missing_records - data.isna().sum().sum())
    missing_records = data.isna().sum().sum()

    data_list = data.values.tolist()
    sheet.clear()
    sheet.insert_row(data.columns.tolist(), 1)

    logging.info("Uzupełnianie danych w Google Sheet")

    for row in data_list:
        write_to_sheet_with_retry(sheet, row)


def write_to_sheet_with_retry(sheet, row):
    retries = 5
    for i in range(retries):
        try:
            sheet.append_row(row)
            break
        except gspread.exceptions.APIError as e:
            logging.warning("Przekroczono ilość requestów/minutę, ponawianie: %s", i+1)
            time.sleep(60)


if __name__ == "__main__":
    get_data_from_google_sheet()
