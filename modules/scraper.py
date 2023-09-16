import time
import os
import openpyxl
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


def read_xlsx(directory_path):
    for filename in os.listdir(directory_path):
        if filename.lower().endswith('.xlsx'):
            file_path = os.path.join(directory_path, filename)
            try:
                workbook = openpyxl.load_workbook(file_path)
                sheet = workbook.active  # Get the active sheet (usually the first one)

                # Extract values from the first column
                first_column_values = [cell.value for cell in sheet['A']]  # Assuming the first column is 'A'

                return first_column_values

            except Exception as e:
                print(f"Error processing {filename}: {e}")

    # If no XLSX file is found or if there's an issue, return None
    return None