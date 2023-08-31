import time

import pandas as pd
from modules.navigation import *
from modules.scraper import *
from modules.output import *
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains


from config.settings import *

stock_list = ["AAPL",
"ABNB",
"AMD",
"AMZN",
"APO",
"crwd",
"csco",
"ctra",
              ]
classification_terms = ['buy', 'sell', 'hold']

rating_list = []
price_target_list = []
driver, success = make_request('https://www.cnbc.com/quotes/AAPL?qsearchterm=apple')
if success:
    driver.maximize_window()
    time.sleep(1)
    load_and_click(driver, '//*[@id="QuotePage-ICBanner"]/div/div/div[1]')


    # login and password
    username = 'rameshsingh360@gmail.com'
    password = '-lioN2o88'
    insert_text(driver, '//*[@id="sign-in"]/div[1]/div/div/input', username)
    insert_text(driver, '//*[@id="sign-in"]/div[2]/div/div/input', password)
    load_and_click(driver, '//*[@id="sign-in"]/button[1]')
    time.sleep(1)

    # search the stock list
    for s in stock_list:
        print(s)
        driver.get(f'https://www.cnbc.com/quotes/{s}')
        time.sleep(3)
        soup = get_source(driver)
        rating_block = find_all(soup, 'div', 'class', 'ICBanner-firstRow')
        if len(rating_block)>0:
            rating = rating_block[1].text
            rating_list.append(rating)
        else:
            rating_list.append('N/A')
        price_target_block = find_all(soup, 'div', 'class', 'ICBanner-rowValue')
        if len(price_target_block)>0:
            price_target = price_target_block[0].text
            price_target_list.append(price_target)
        else:
            price_target_list.append('N/A')
driver.quit()

if len(rating_list)>0 and len(price_target_list)>0:
    data = {
        "Name": stock_list,
        "Rating": rating_list,
        "Price Target": price_target_list
    }
    df = pd.DataFrame(data)
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # Save the DataFrame to an Excel file
    script_dir = os.path.dirname(sys.argv[0])
    print(script_dir)
    excel_filename = f'tipranks_{timestamp}.xlsx'
    df.to_excel(os.path.join(script_dir, excel_filename), index=False)






