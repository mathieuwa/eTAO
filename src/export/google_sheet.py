import json
import pygsheets
from datetime import datetime

from google.oauth2 import service_account
from gsheetsdb import connect

from parameters.parameters import Parameters

# Documentation : https://understandingdata.com/posts/the-comprehensive-guide-to-google-sheets-with-python/

def get_first_empty_id(wks):

    first_column = wks.get_col(1)
    idx_ = first_column.index("")
    return idx_



def send_data(data):


    #with open('.streamlit/etao-383821-902fcf809fd4.json') as source:
    #    info = json.load(source)
    #credentials = service_account.Credentials.from_service_account_info(info)

    client = pygsheets.authorize(service_account_file='data/google_sheet_secret.json')

    #spreadsheet_url = "https://docs.google.com/spreadsheets/d/1jBr5QFWVQa6JmI7YkNUioDjRc4ytI272IYP-ePuB9zo/edit#gid=0"
    #sheet_data = client.sheet.get('1jBr5QFWVQa6JmI7YkNUioDjRc4ytI272IYP-ePuB9zo')
    sheet = client.open_by_key('1jBr5QFWVQa6JmI7YkNUioDjRc4ytI272IYP-ePuB9zo')

    wks = sheet.worksheet_by_title('Sheet1')


    first_empty_id = get_first_empty_id(wks)


    if data["etao"] == None:
        etao_displayed = None
    else:
        etao_displayed = data["etao"]*10./3


    current_date = datetime.now()


    values = [
        first_empty_id, 
        current_date.strftime("%d/%m/%Y - %H:%M:%S"),
        practitioner[0], practitioner[1],
        Parameters.LANGUAGE,
        data["first_name"], 
        data["last_name"],
        data["date"].strftime("%d/%m/%Y"),
        data["eye_right_colors"][0], data["eye_right_colors"][1], data["eye_right_colors"][2], data["eye_right_colors"][3],
        data["eye_left_colors"][0], data["eye_left_colors"][1], data["eye_left_colors"][2], data["eye_left_colors"][3],
        data["etao"], etao_displayed
    ]

    wks.insert_rows(first_empty_id, number=1, values=values, inherit=False)