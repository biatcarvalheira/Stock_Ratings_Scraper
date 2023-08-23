import pandas as pd
from modules.navigation import *
from modules.scraper import *
from modules.output import *
from datetime import datetime

from config.settings import *
import requests
from bs4 import BeautifulSoup
stock_list = ["aapl",
"abnb",
"ael-a",
"all-i",
"amd",
"amzn",
"apo"]
classification_terms = ['buy', 'sell', 'hold']

status_list = []
price_list = []

for s in stock_list:
    driver, success = make_request(f'https://www.tipranks.com/stocks/{s}/forecast')
    status = 'N/A'
    print(s)
    if success:
        driver.maximize_window()
        scroll_script = "window.scrollBy(0, 300);"
        driver.execute_script(scroll_script)
        time.sleep(0.5)
        soup = get_source(driver)

        classification = find(soup, 'span', 'class', 'colorpale fonth4_bold aligncenter mobile_mb0 mobile_fontSize3small w12')
        if classification:
            classification_formatted = (classification.text).lower()

            for c in classification_terms:
                if c in classification_formatted:
                    status = c
                    break
                else:
                    status = 'N/A'
            status_list.append(status)
            content_div = soup.find('span', class_='fontWeightsemibold colorgray-1')
            if content_div:
                price = content_div.get_text()
            else:
                price = 'N/A'
            price_list.append(price)
        else:
            status_list.append('N/A')
            price_list.append('N/A')
            continue
    driver.quit()

if len(status_list)>0 and len(price_list)>0:
    script_dir = os.path.dirname(sys.argv[0])

    print(script_dir)
    data = {
        "Name": stock_list,
        "Rating": status_list,
        "Average price": price_list
    }
    df = pd.DataFrame(data)
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # Save the DataFrame to an Excel file
    excel_filename = os.path.join(script_dir, f'tipranks_{timestamp}.xlsx')
    df.to_excel(excel_filename, index=False)





