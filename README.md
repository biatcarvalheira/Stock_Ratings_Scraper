# CNBC Web Scraper

Stock Data Scraper streamlines the process of retrieving stock data from the CNBC Investing Club website. It uses Flask to render a user-friendly HTML interface for securely entering credentials. The Python script, using the libraries Beautiful Soup, Selenium, Openpyxl and Pyinstaller, reads an Excel sheet (.xlsx), extracts a list of stock quotes, fetches detailed data for each stock, and exports the comprehensive dataset into another .xlsx file. The end result is a user-friendly Mac OS executable application.


## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/biatcarvalheira/Stock_Ratings_Scraper.git
    cd Stock_Ratings_Scraper
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the web scraping script:

    ```bash
    python main.py
    ```

2. The script will prompt you to enter the username and password for the CNBC website.

3. The scraped data will be saved to an Excel file (`CNBC_%Y-%m-%d_%H-%M-%S.xlsx`) in the project directory.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

