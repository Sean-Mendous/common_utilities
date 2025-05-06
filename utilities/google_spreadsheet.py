import os
import gspread
from google.oauth2.service_account import Credentials
from utilities.logger import logger

"""
spreadsheet = {
    'file_path': '/Users/shinnosuke/Desktop/業務/Samurai marketing/開発/automatic_FormSendding/tests/0410_FPS様_DODAリスト_営業文あり.xlsx',
    'sheet_name': 'sheet',
    'column_map': {
        'website_url': 'E',
        'contact_url': 'F',
        'sentence': 'J',
        'status': 'K',

        'row_start': 'M2',
        'row_end': 'O2',
    }
}
"""

def certification_google_spreadsheet(sheet_id, worksheet_name, credentials_path):
	scopes = [
		"https://www.googleapis.com/auth/spreadsheets",
		"https://www.googleapis.com/auth/drive"
	]
      
	creds = Credentials.from_service_account_file(credentials_path, scopes=scopes)
	client = gspread.authorize(creds)
	sheet = client.open_by_key(sheet_id).worksheet(worksheet_name)
	return sheet

def duplicate_google_sheet(sheet_id, duplicate_sheet_name, credentials_path, new_sheet_name):
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_file(credentials_path, scopes=scopes)
    client = gspread.authorize(creds)

    spreadsheet = client.open_by_key(sheet_id)

    try:
        duplicate_sheet = spreadsheet.worksheet(duplicate_sheet_name)
    except gspread.exceptions.WorksheetNotFound:
        raise ValueError(f"google_spreadsheet.py_🔴 cannot find'{duplicate_sheet_name}'")

    existing_sheet_names = [ws.title for ws in spreadsheet.worksheets()]
    if new_sheet_name in existing_sheet_names:
        logger.info(f"google_spreadsheet.py_🟡 '{new_sheet_name}' already exists!")
        return spreadsheet.worksheet(new_sheet_name)

    response = spreadsheet.duplicate_sheet(
        source_sheet_id=duplicate_sheet.id,
        insert_sheet_index=0,
        new_sheet_name=new_sheet_name
    )

    logger.info(f"google_spreadsheet.py_🟢 successfully duplicated '{new_sheet_name}'")
    return spreadsheet.worksheet(new_sheet_name)

def input_google_spreadsheet(sheet, column_map, row):
    data = {}
    for key, col in column_map.items():
        try:
            cell_value = sheet.acell(f"{col}{row}").value
        except Exception:
            cell_value = None
        data[key] = cell_value
    return data

def output_google_spreadsheet(sheet, column_map, row, data):
    try:
        for key, col_letter in column_map.items():
            if key in data:
                cell = f"{col_letter}{row}"
                value = data[key] if data[key] else "-"
                sheet.update_acell(cell, value)
                logger.info(f" > google_spreadsheet.py_{key}: {value}")
        return True

    except Exception as e:
        logger.error(f"google_spreadsheet.py_🔴 {e}")
        return False

def input_google_spreadsheet_multi(sheet, column_map, row_start, row_end):
    keys = [k for k in column_map if k != "headder"]
    ranges = [f"{column_map[k]}{row_start}:{column_map[k]}{row_end}" for k in keys]
    
    try:
        results = sheet.batch_get(ranges)
        logger.info(f" > spreadsheet.py_🟢 batch_get success")
    except Exception as e:
        raise RuntimeError(f" > spreadsheet.py_🔴 batch_get failed: {e}")

    row_count = row_end - row_start + 1
    row_dicts = []

    for i in range(row_count):
        row_data = {}
        for idx, key in enumerate(keys):
            col_data = results[idx]
            row_data[key] = col_data[i][0] if i < len(col_data) and col_data[i] else None
        row_dicts.append(row_data)

    return row_dicts

def output_google_spreadsheet_multi(sheet, column_map, row_start, data_list):
    keys = [k for k in column_map if k != "headder"]
    row_end = row_start + len(data_list) - 1

    updates = []
    for key in keys:
        col_letter = column_map[key]
        col_range = f"{col_letter}{row_start}:{col_letter}{row_end}"
        col_values = [[str(row.get(key, ""))] for row in data_list]
        updates.append({"range": col_range, "values": col_values})

    try:
        sheet.batch_update(updates)
        logger.info(f" > spreadsheet.py_🟢 batch_update success")
    except Exception as e:
        raise RuntimeError(f" > spreadsheet.py_🔴 batch_update failed: {e}")

if __name__ == "__main__":
	spreadsheet = {
		"sheet_type": "google_sheets",
		"sheet_id": "1iP2WCeapRUAIaaTAzZGQBhKL1UU08dQUlmXa2zMu0vc",
		"credentials_path": "bionic-tracer-458405-j3-28e3106ce590.json",
		"worksheet_name": "test",
		"column_map": {
			"website_url": "A",
			"contact_url": "B",
			"sentence": "C", 
			"status": "D"
		}
	}

	sheet = certification_google_spreadsheet(spreadsheet["sheet_id"], spreadsheet["worksheet_name"], spreadsheet["credentials_path"])
	# input_data = input_google_spreadsheet_multi(sheet, spreadsheet["column_map"], 2, 10)
	# print(input_data)

	output_data = [
		{
			"website_url": "https://www.google.com",
			"contact_url": "https://www.google.com", 
			"sentence": "test1",
			"status": "done"
		},
		{
			"website_url": "https://www.google.com",
			"contact_url": "https://www.google.com",
			"sentence": "test2", 
			"status": "done"
		},
		{
			"website_url": "https://www.google.com",
			"contact_url": "https://www.google.com",
			"sentence": "test3",
			"status": "done"
		},
		{
			"website_url": "https://www.google.com",
			"contact_url": "https://www.google.com",
			"sentence": "test4",
			"status": "done"
		},
		{
			"website_url": "https://www.google.com",
			"contact_url": "https://www.google.com",
			"sentence": "test5",
			"status": "done"
		}
	]
	output_google_spreadsheet_multi(sheet, spreadsheet["column_map"], 11, output_data)
