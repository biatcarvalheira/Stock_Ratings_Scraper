import time

import requests
from bs4 import BeautifulSoup
import re
import json


def get_source(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def find(soup, section, attribute, att_identifier):
    find_result = soup.find(section, {attribute: att_identifier})
    return find_result


def find_all(soup, section, attribute, att_identifier):
    result_find_all = soup.find_all(section, {attribute: att_identifier})
    return result_find_all


def append_simple(source_list, target_list):
    for f in source_list:
        target_list.append(f)
    return target_list


def get_xlsx(directory_path):
    try:
        # Get a list of all files in the directory
        files = os.listdir(directory_path)
        # Check if any of the files has a .xlsx extension
        for file in files:
            if file.lower().endswith('.xlsx') and not file.startswith('~$'):
                file_path = os.path.join(directory_path, file)
                try:
                    wb = openpyxl.load_workbook(file_path)
                    sheet_names = wb.sheetnames
                    if sheet_names:
                        first_sheet_name = sheet_names[0]
                        sheet = wb[first_sheet_name]

                        # Get the letters of all active columns
                        active_columns_letters = [openpyxl.utils.get_column_letter(col) for col in
                                                  range(1, sheet.max_column + 1)]

                        # Get the last active row
                        last_active_row = sheet.max_row

                        return first_sheet_name, file_path, active_columns_letters, last_active_row
                except Exception as e:
                    print(f"Error while processing file '{file}': {e}")
        # If no XLSX file with a sheet is found
        return None
    except Exception as e:
        print(f"Error while listing directory '{directory_path}': {e}")
