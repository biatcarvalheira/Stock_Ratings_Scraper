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
from flask import Flask, render_template, request
import random

# Determine the script's directory (where main.py is located)
script_dir = os.path.abspath(os.path.dirname(sys.argv[0]))

# Construct the absolute path to the 'templates' folder
template_dir = os.path.join(script_dir, 'templates')

# Initialize the Flask app with the explicit template folder
app = Flask(__name__, template_folder=template_dir)

print(template_dir)

stop_server = False

first_column_values_definitive = []


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/process_form', methods=['POST'])
def process_form():
    try:
        # Retrieve data from the submitted form
        username = request.form['username']
        password = request.form['password']

        # Call the main_program function to start processing and pass the username and password as arguments
        main_result = main_program(username, password)

        return main_result  # Return the result of main_program

    except Exception as e:
        print(f"Error processing form: {e}")
        return "An error occurred."


def main_program(username, password):  # Accept username and password as arguments
    try:
        script_path = sys.argv[0]
        script_directory = os.path.abspath(os.path.dirname(script_path))
        first_column_values = get_first_column_values_from_xlsx(script_directory)
        if first_column_values is not None:
            print('## List Successfully found ##')
            filtered_list = [item for item in first_column_values if item is not None]
            for i in filtered_list:
                first_column_values_definitive.append(i.upper())
            result = automation_and_scraping(username, password, first_column_values_definitive)
        else:
            print("No XLSX file found in the specified directory.")

        return """
                <html>
                <head>
                    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
                    <title>Processing Started</title>
                </head>
                <body>
                    <h1>Processing Started</h1>
                    <p>The script is currently running. You can stop it by clicking the button below:</p>
                    <form method="POST" action="/stop_processing">
                        <input type="submit" value="Stop Script">
                    </form>
                </body>
                </html>
                """

    except Exception as e:
        print(f"Error processing XLSX file: {e}")
        return "An error occurred during processing."


def automation_and_scraping(username, password, first_column_values_definitive):
    rating_list = []
    price_target_list = []

    # Create a session to maintain the connection
    session = requests.Session()

    driver, success = make_request('https://www.cnbc.com/quotes/AAPL?qsearchterm=apple')

    if success:
        driver.maximize_window()
        time.sleep(1)
        load_and_click(driver, '//*[@id="QuotePage-ICBanner"]/div/div/div[1]')

        # login and password
        insert_text(driver, '//*[@id="sign-in"]/div[1]/div/div/input', username)
        insert_text(driver, '//*[@id="sign-in"]/div[2]/div/div/input', password)
        load_and_click(driver, '//*[@id="sign-in"]/button[1]')
        time.sleep(1)

        for s in first_column_values_definitive:
            print(s)
            driver.get(f'https://www.cnbc.com/quotes/{s}')
            time.sleep(random.uniform(2, 5))  # Introduce random delays between requests

            # Add error handling here if needed
            try:
                soup = get_source(driver)
                rating_block = find_all(soup, 'div', 'class', 'ICBanner-firstRow')
                if len(rating_block) > 0:
                    rating = rating_block[1].text
                    rating_list.append(rating)
                else:
                    rating_list.append('N/A')
                print(rating_list)
                price_target_block = find_all(soup, 'div', 'class', 'ICBanner-rowValue')
                if len(price_target_block) > 0:
                    price_target = price_target_block[0].text
                    price_target_list.append(price_target)
                else:
                    price_target_list.append('N/A')
            except Exception as e:
                print(f"Error scraping {s}: {e}")

    driver.quit()
    print('First Value', first_column_values_definitive)
    print('Rating', rating_list)
    print('Price Target', price_target_list)
    return first_column_values_definitive, rating_list, price_target_list



@app.route('/stop_processing', methods=['POST'])
def stop_processing():
    global stop_server
    stop_server = True  # Set the flag to stop the Flask server
    return """<html> <head><link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <title>Program Stopped</title> </head> <body> <h1>Program Stopped</h1> <p>The script has 
    been stopped. Please close this browser window, and the current terminal window and click the executable file 
    again to run.</p> </body> </html>"""


if __name__ == '__main__':
    url = "http://127.0.0.1:5000"  # Change this URL to match your app's address
    webbrowser.open(url)
    app.run(debug=True)
    # Check if the server should be stopped
    if stop_server:
        sys.exit(0)
