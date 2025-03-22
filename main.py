from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException

import csv
import os

from Pages.HomePage import HomePage


def log2csv(data: dict, log_path: str = 'Logs/log.csv'):
    """ Save data to csv file (new / exiting)"""
    dir_path = os.path.dirname(log_path)
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)

    is_file_exists = os.path.isfile(log_path)
    with open(log_path, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        if not is_file_exists:
            print("new file")
            writer.writeheader()
        writer.writerow(data)
        print(f"data saved to {log_path}")


def run_speedtest():

    # Auto Install Chrome Driver
    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome()

    driver.set_page_load_timeout(15)  # Set max time for page to load

    # Load the page until timeout than start testing
    print("Loading Page...")
    try:
        driver.get("https://www.speedtest.net/")
    except TimeoutException:
        pass

    driver.maximize_window()
    driver.implicitly_wait(10)

    home_page = HomePage(driver)

    # remove privacy popup
    home_page.handle_continue_privacy_popup()
    home_page.click_go_button()

    data = {}
    data['ping'] = home_page.get_ping()
    print(f"Ping: {data['ping']}")

    print("Analyze Download & Upload...")
    while True:
        if "opacity: 0;" in home_page.speed_handle_opacity_style():
            data['Download (mbps)'] = home_page.get_download_Mbps()
            data['Upload (mbps)'] = home_page.get_upload_Mbps()
            print(f"Download Mbps: {data['Download (mbps)']} \nUpload Mbps: {data['Upload (mbps)']}")
            break

    log_path = 'Logs/log.csv'
    log2csv(data, log_path=log_path)

    driver.close()


if __name__ == '__main__':
    run_speedtest()
    