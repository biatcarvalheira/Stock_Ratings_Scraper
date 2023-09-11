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
        print(f"Username: {username}")
        print(f"Password: {password}")

        script_path = sys.argv[0]
        script_directory = os.path.abspath(os.path.dirname(script_path))
        first_column_values = get_first_column_values_from_xlsx(script_directory)
        if first_column_values is not None:
            print('## List Successfully found ##')
            filtered_list = [item for item in first_column_values if item is not None]
            for i in filtered_list:
                first_column_values_definitive.append(i.upper())
                print(i)
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
