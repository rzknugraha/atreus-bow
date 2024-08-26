import cx_Oracle
import os
from dotenv import load_dotenv
from openpyxl import load_workbook
import pandas as pd
import datetime
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
import time

load_dotenv()

def get_data():
    # Set up your Oracle connection string
    dsn = cx_Oracle.makedsn(os.getenv("ORA_HOST"), os.getenv("ORA_PORT"), service_name=os.getenv("ORA_SERVICE"))
    print(dsn)
    connection = cx_Oracle.connect(os.getenv("ORA_USER"), os.getenv("ORA_PWD"), dsn)
    print(connection)

    # Create a cursor
    cursor = connection.cursor()

    # Execute a query
    cursor.execute("SELECT TENANT_ID, HOLIDAY_DESC FROM NRT_ADMIN.IPF_PUBLIC_HOLIDAY")

    row = cursor.fetchone()

    # Close the connection
    cursor.close()
    connection.close()

    return row

def insert_excel(data):
    df = pd.read_excel('example.xlsx', engine='openpyxl')

    print(data)

    print("Before adding new row:")
    print(df)

    # Get the current date and time
    now = datetime.datetime.now()

    # Format the date and time
    formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")

    # Data for the new row
    new_data = pd.DataFrame({
    'Name': [data[0]],
    'Value': [data[1]],
    'SentMail': [0],
    'Date': [formatted_now]

    })

    print(new_data)

    # Append the new row to the DataFrame
    # Method 1: Using loc
    df = pd.concat([df, new_data], ignore_index=True)

    print("After adding new row:")
    print(df)

    # Save back to Excel
    try:
        df.to_excel('example1.xlsx', index=False, engine='openpyxl')
        print("Data written to Excel successfully.")
    except Exception as e:
        print(f"Failed to write to Excel: {e}")


def crawlWeb():
    
    # Set the path to the Edge WebDriver
    driver_path = './msedgedriver.exe'
    service = Service(executable_path=driver_path)

    # Initialize the WebDriver for Edge
    driver = webdriver.Edge(service=service)

    # Open the form URL
    form_url = 'https://forms.office.com/r/rqjQEyVTjt'
    driver.get(form_url)

    # Wait for the form to load
    time.sleep(3)
# Locate the form fields using CSS selectors
    try:
        name_field = driver.find_element(By.CSS_SELECTOR, 'input[aria-labelledby="QuestionId_r44fc908293d74bd8be5fc90f448b933d QuestionInfo_r44fc908293d74bd8be5fc90f448b933d"]')
        email_field = driver.find_element(By.CSS_SELECTOR, 'input[aria-labelledby="QuestionId_rc0d238fa0ccf40be8f7e81a2208e3d0b QuestionInfo_rc0d238fa0ccf40be8f7e81a2208e3d0b"]')
        type_field = driver.find_element(By.CSS_SELECTOR, 'input[aria-labelledby="QuestionId_r33727028427a4f44974b03640bb45b5b QuestionInfo_r33727028427a4f44974b03640bb45b5b"]')
        body_field = driver.find_element(By.CSS_SELECTOR, 'textarea[aria-labelledby="QuestionId_rf0b351b0731d41feb48825eddd65cd28 QuestionInfo_rf0b351b0731d41feb48825eddd65cd28"]')  # Assuming 'Body' might be a textarea

        # Fill in the form fields
        name_field.send_keys('John Doe')
        email_field.send_keys('john.doe@example.com')
        type_field.send_keys('Inquiry')
        body_field.send_keys('This is a test message.')

        # Submit the form (if there is a submit button, usually a button element)
        submit_button = driver.find_element(By.CSS_SELECTOR, 'button[data-automation-id="submitButton"]')
        submit_button.click()

        print("Form submitted successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Close the WebDriver
    time.sleep(5)
    driver.quit()


 


if __name__ == "__main__":
    # Fetch data from the database
    # result_data = get_data()
    
    # print(result_data)
    # Send the data via email

    # insert_excel(result_data)

    crawlWeb()