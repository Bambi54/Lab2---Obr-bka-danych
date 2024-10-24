import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import json, time


def get_data_from_google_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    with open('credentials.json', 'r') as f:
        credentials_info = json.load(f)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_info, scope)
    client = gspread.authorize(creds)
    sheet = client.open("ASI LAB2").sheet1

    csv_file_path = 'external-repo/data_student_25347.csv'
    data = pd.read_csv(csv_file_path)

    #Usunięcie NaN
    data = data.fillna(0.0)

    data_list = data.values.tolist()
    sheet.clear()
    sheet.insert_row(data.columns.tolist(), 1)

    for row in data_list:
        write_to_sheet_with_retry(sheet, row)


def write_to_sheet_with_retry(sheet, row):
    retries = 5
    for i in range(retries):
        try:
            sheet.append_row(row)
            break
        except gspread.exceptions.APIError as e:
            time.sleep(60)


if __name__ == "__main__":
    get_data_from_google_sheet()
