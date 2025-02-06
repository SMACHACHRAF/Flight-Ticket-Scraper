import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By

# Configure Chrome options
options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--disable-popup-blocking")
options.add_argument('--disable-blink-features=AutomationControlled')


# Specify ChromeDriver path (adjust if necessary)
driver_path = "C:\Program Files (x86)\chromedriver.exe"

# Initialize Chrome WebDriver
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(10)  # Implicit wait for initial page load

def click_show_more(driver, click_count):
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            show_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.ULvh-button.show-more-button"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", show_more_button)
            show_more_button.click()  # Direct click is often more reliable
            print(f"Clicked 'Show more results' {click_count} times")
            return
        except (TimeoutException, StaleElementReferenceException) as e:
            print(f"Error clicking 'Show more' (Attempt {attempt + 1}/{max_attempts}): {e}")
            if attempt < max_attempts - 1:
                time.sleep(2)
    print("Failed to click 'Show more' after multiple attempts.")

def extract_flight_data(driver):
    try:
        companies = []
        dates = []
        days = []
        timeDeparture = []
        timeArrival = []
        airportDepart = []
        airportDestination = []
        stops = []
        durations = []
        prices = []

        companies_element = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.VY2U > div.c_cgF.c_cgF-mod-variant-default"))
        )

        days_element = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.c9L-i > div.c_cgF.c_cgF-mod-variant-default"))
        )

        timeDeparture_elements = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.VY2U > div.vmXl.vmXl-mod-variant-large > span:nth-child(1)"))
        )

        timeArrival_elements = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.VY2U > div.vmXl.vmXl-mod-variant-large > span:nth-child(3)"))
        )

        airporDepart_elements = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.xdW8 > div.c_cgF.c_cgF-mod-variant-default > div > div:nth-child(1) > span > span"))
        )

        airporDestination_elements = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.xdW8 > div.c_cgF.c_cgF-mod-variant-default > div > div:nth-child(3) > span"))
        )

        price_elements = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.f8F1-price-text"))
        )

        dates_elements = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.c9L-i > div.vmXl.vmXl-mod-variant-default"))
        )

        stops_elements = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.JWEO > div.vmXl.vmXl-mod-variant-default > span"))
        )

        durations_elements = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.xdW8 > div.vmXl.vmXl-mod-variant-default"))
        )

        companies = [element.text.strip() for element in companies_element]
        days = [element.text.strip() for element in days_element]
        dates = [element.text.strip() for element in dates_elements]
        timeDeparture = [element.text.strip() for element in timeDeparture_elements]
        timeArrival = [element.text.strip() for element in timeArrival_elements]
        airportDepart = [element.text.strip() for element in airporDepart_elements]
        airportDestination = [element.text.strip() for element in airporDestination_elements]
        stops = [element.text.strip() for element in stops_elements]
        durations = [element.text.strip() for element in durations_elements]
        prices = [element.text.strip() for element in price_elements]

        print("Airline Extracted:", companies)
        print("Day Extracted", days)
        print("Dates Extracted:", dates)
        print("Departure Time Extracted:", timeDeparture)
        print("Arrival Time Extracted:", timeArrival)
        print("Airport Depart Extracted:", airportDepart)
        print("Airport Destination Extracted:", airportDestination)
        print("Stops Extracted:", stops)
        print("Durations Extracted:", durations)
        print("Prices Extracted:", prices)

        return companies, days, dates, timeDeparture, timeArrival, airportDepart, airportDestination, stops, durations, prices

    except TimeoutException:
        print("Timeout waiting for flight elements.")
        return [], [], [], [], [], [], [], [], [], []
    except Exception as e:
        print(f"Error extracting flight details: {e}")
        return [], [], [], [], [], [], [], [], [], []

try:
    driver.get("https://www.momondo.com/flight-search/TUN-CDG/2025-01-01-flexible-3days?ucs=7z6xa6&sort=bestflight_a")

    for i in range(5):
        click_show_more(driver, i + 1)
        time.sleep(3)

    comapnies, days, dates, timeDeparture, timeArrival, airportDepart, airportDestination, stops, durations, prices = extract_flight_data(driver)

    if comapnies and days and dates and timeDeparture and timeArrival and airportDepart and airportDestination and stops and durations and prices:
        with open("flight_data.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Airline", "Day", "Date", "DepartureTime", "ArrivalTime", "AirportDepart", "AirportDestination", "Stops", "Duration", "Price"])
            writer.writerows(zip(comapnies, days, dates, timeDeparture, timeArrival, airportDepart, airportDestination, stops, durations, prices))
        print("Data saved to flight_data.csv")
    else:
        print("No data could be extracted. Check selectors or website structure.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()