import pandas as pd
import time
import os
import sys
from datetime import datetime


def clean_lists(*lists):
    for lst in lists:
        lst.clear()


def save_to_xlsx(list1, list2, input_list):
    if len(list1) > 0 and len(list2) > 0:
        data = {
            "Name": input_list,
            "Rating": list1,
            "Price Target": list2
        }
        df = pd.DataFrame(data)
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

        # Save the DataFrame to an Excel file
        script_dir = os.path.dirname(sys.argv[0])
        excel_filename = f'CNBC_{timestamp}.xlsx'
        df.to_excel(os.path.join(script_dir, excel_filename), index=False)
