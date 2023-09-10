import time
import pandas as pd
from modules.navigation import *
from modules.scraper import *
from modules.output import *
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains
from config.settings import *
from flask import Flask, render_template, request


app = Flask(__name__)
first_column_values_definitive = []

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/process_form', methods=['POST'])
def process_form():
    try:
        # Retrieve data from the submitted form
        name = request.form['name']
        email = request.form['email']

        # Process the form data (replace with your logic)
        # For example, you can print the values:
        print(f"Name: {name}")
        print(f"Email: {email}")

        return "Form submitted successfully."

    except Exception as e:
        print(f"Error processing form: {e}")
        return "An error occurred."


@app.route('/start_processing', methods=['POST'])
def start_processing():
    try:
        # Add the code that should run when the "Start" button is pressed
        # For example, you can add your existing code here

        # Example: Start processing the XLSX file
        # set current file directory (main)
        script_path = sys.argv[0]
        script_directory = os.path.abspath(os.path.dirname(script_path))

        first_column_values = get_first_column_values_from_xlsx(script_directory)

        if first_column_values is not None:
            print('## List Successfully found ##')
            filtered_list = [item for item in first_column_values if item is not None]
            for i in filtered_list:
                first_column_values_definitive.append(i.upper())
        else:
            print("No XLSX file found in the specified directory.")
            sys.exit()

        return "Processing started."

    except Exception as e:
        print(f"Error processing XLSX file: {e}")
        return "An error occurred during processing."


if __name__ == '__main__':
    app.run(debug=True)















