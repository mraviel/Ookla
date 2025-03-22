from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class HomePage:

    """ Speedtest home page """

    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def handle_continue_privacy_popup(self):
        """ Remove privacy popup window """
        try:
            self.wait.until(EC.visibility_of_element_located((By.ID, "onetrust-accept-btn-handler")))
            self.driver.find_element(By.ID, 'onetrust-accept-btn-handler').click()
        except:
            pass

    def click_go_button(self):
        """ Click on GO button """
        self.driver.find_element(By.CSS_SELECTOR, "span.start-text").click()

    def get_download_Mbps(self) -> str:
        return self.driver.find_element(By.CSS_SELECTOR, "span.download-speed").text

    def get_upload_Mbps(self) -> str:
        return self.driver.find_element(By.CSS_SELECTOR, "span.upload-speed").text

    def get_ping(self) -> str:
        self.wait_for_ping()
        return self.driver.find_element(By.CSS_SELECTOR, "span.ping-speed").text

    def speed_handle_opacity_style(self) -> str:
        """ Return the style of element: ('opacity: 0;' = Stop computing) """
        return self.driver.find_element(By.CSS_SELECTOR, "div.gauge-speed-needle").get_attribute("style")

    def wait_for_ping(self):
        # Wait for ping to be completed
        self.wait.until(EC.text_to_be_present_in_element_attribute(
            (By.CSS_SELECTOR, "div.gauge-group-ping"), "style", "opacity: 0;"))

    def wait_for_computing_download_upload(self):
        # Wait for download and upload to be completed
        self.wait.until(EC.text_to_be_present_in_element_attribute(
            (By.CSS_SELECTOR, "gauge-group-speed"), "style", "opacity: 0;"))