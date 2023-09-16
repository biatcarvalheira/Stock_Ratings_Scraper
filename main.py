import sys
import time
import webbrowser
import pandas as pd
from modules.navigation import *
from modules.scraper import *
from modules.output import *
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains
from config.settings import *
from flask import Flask, request, render_template, jsonify
from threading import Thread  # Import the Thread class
import subprocess


# Rest of your code...


# Determine the script's directory (where main.py is located)
script_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
# Construct the absolute path to the 'templates' folder
template_dir = os.path.join(script_dir, 'templates')
# Initialize the Flask app with the explicit template folder
app = Flask(__name__, template_folder=template_dir)

# Define global variables for scraping status
scraping_thread = None
scraping_in_progress = False
stop_scraping = False

input_data_list = []

status_message = ''  # Initialize status_message as an empty string

@app.route('/')
def index():
    return render_template('login.html')


@app.route('/start_scraping', methods=['POST'])
def start_scraping():
    global scraping_thread, scraping_in_progress, stop_scraping

    if scraping_in_progress:
        return jsonify({'status': 'Scraping is already in progress'})

    username = request.form['username']
    password = request.form['password']

    # Read data from an input XLSX file and save it into a list
    script_path = sys.argv[0]
    script_directory = os.path.abspath(os.path.dirname(script_path))
    input_data = read_xlsx(script_directory)
    if input_data is not None:
        print('XLSX file found')
        filtered_list = [item for item in input_data if item is not None]
        for f in filtered_list:
            input_data_list.append(f.upper())
    scraping_thread = Thread(target=scrape_and_save, args=(username, password, input_data_list))
    scraping_thread.start()
    scraping_in_progress = True
    stop_scraping = False
    return jsonify({'status': 'Scraping started'})

@app.route('/stop_scraping', methods=['POST'])
def stop():
    global scraping_thread, scraping_in_progress, stop_scraping
    stop_scraping = True
    scraping_thread.join()  # Wait for the scraping thread to finish
    scraping_in_progress = False
    return jsonify({'status': 'Scraping stopped'})


def scrape_and_save(username, password, input_data):
    global scraping_in_progress, stop_scraping, status_message
    rating_list = []  # Define rating_list as an empty list
    price_target_list = []  # Define price_target_list as an empty list
    # Process the data with your scraping function
    rating_list, price_target_list, input_data = scraping_function(username, password, input_data, rating_list, price_target_list)

    # Save the scraped content to an output XLSX file
    save_to_xlsx(rating_list, price_target_list, input_data)
    scraping_in_progress = False


def scraping_function(username, password, input_data, rating_list, price_target_list):
    driver, success = make_request('https://www.cnbc.com/quotes/AAPL?qsearchterm=apple')
    if success:
        driver.maximize_window()
        time.sleep(1)
        load_and_click(driver, '//*[@id="QuotePage-ICBanner"]/div/div/div[1]')

        # Perform login using provided username and password
      #  insert_text(driver, '//*[@id="sign-in"]/div[1]/div/div/input', username)
     #   insert_text(driver, '//*[@id="sign-in"]/div[2]/div/div/input', password)
     #   load_and_click(driver, '//*[@id="sign-in"]/button[1]')
        time.sleep(1)

        for s in input_data:
            if stop_scraping:  # Check if scraping should be stopped
                break  # Exit the loop if stop_scraping is True

        # Check if the login was successful
        login_failed_element = None
        try:
            login_failed_element = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "AuthForms-miscellaneousError"))
            )
        except Exception as e:
            pass  # Continue if login was successful or timeout occurred

        if login_failed_element:
            driver.quit()
            try:
                subprocess.call(['osascript', '-e', 'tell application "Google Chrome" to close windows'])
            except Exception as e:
                print("Error closing Chrome:", str(e))
            return jsonify({'status': 'Scraping stopped. Wrong username or password'})

        # Continue with scraping logic
        # search the stock list
        for s in input_data:
            driver.get(f'https://www.cnbc.com/quotes/{s}')
            time.sleep(3)
            soup = get_source(driver)
            rating_block = find_all(soup, 'div', 'class', 'ICBanner-firstRow')
            if len(rating_block) > 0:
                rating = rating_block[1].text
                rating_list.append(rating)
            else:
                rating_list.append('N/A')
            price_target_block = find_all(soup, 'div', 'class', 'ICBanner-rowValue')
            if len(price_target_block) > 0:
                price_target = price_target_block[0].text
                price_target_list.append(price_target)
            else:
                price_target_list.append('N/A')

        driver.quit()  # Close the WebDriver when done
        try:
            subprocess.call(['osascript', '-e', 'tell application "Google Chrome" to close windows'])
        except Exception as e:
            print("Error closing Chrome:", str(e))
        return rating_list, price_target_list, input_data





webbrowser.open('http://127.0.0.1:5000/')
app.run(debug=True, use_reloader=False)