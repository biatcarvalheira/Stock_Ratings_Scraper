import time
import pandas as pd
from modules.navigation import *
from modules.scraper import *
from modules.output import *
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains
from config.settings import *

# set current file directory (main)
script_path = sys.argv[0]
script_directory = os.path.abspath(os.path.dirname(script_path))

first_column_values = get_first_column_values_from_xlsx(script_directory)
first_column_values_definitive = []

if first_column_values is not None:
    print('## List Successfully found ##')
    filtered_list = [item for item in first_column_values if item is not None]
    for i in filtered_list:
        first_column_values_definitive.append(i.upper())

else:
    print("No XLSX file found in the specified directory.")

print(first_column_values_definitive)






stock_list = ["AAPL",
"ABNB",
"AMD",
"AMZN",
"APO",
"crwd",
"csco",
"ctra",
              ]



