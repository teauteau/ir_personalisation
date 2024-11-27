from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd


def create_browser(profile_path):
    """
    Creates a browser with a specific profile for cookie simulation.
    :param profile_path: Path to the browser profile directory.
    """
    options = Options() 
    options.add_extension("accept_cookies.crx")
    options.add_argument(f"user-data-dir={profile_path}")  # Load the specific profile
    service = Service(r"C:\Users\thoma\Documents\Studie\M1\Information_Retrieval\project\chromedriver-win64\chromedriver-win64\chromedriver.exe")  # Update with the path to chromedriver
    driver = webdriver.Chrome(service=service, options=options)
    
    return driver


def simulate_browsing(driver, urls, visit_time=2):
    """
    Simulates browsing by visiting a list of URLs.
    :param driver: Selenium WebDriver instance.
    :param urls: List of URLs to visit.
    :param visit_time: Time in seconds to stay on each page.
    """
    for url in urls:
        print(f"Visiting: {url}")
        driver.get(url)
        time.sleep(visit_time)  # Stay on the page for a while

def perform_google_search(driver, query):
    """
    Performs a Google search and retrieves the search result URLs.
    :param driver: Selenium WebDriver instance.
    :param query: Search query string.
    :return: List of search result URLs.
    """
    driver.get("https://www.google.com")
    time.sleep(3)
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)  # Wait for results to load

    # Extract search result URLs
    results = driver.find_elements(By.XPATH, '//div[@class="g"]//a')
    urls = [result.get_attribute("href") for result in results if result.get_attribute("href")]
    return urls


def main():
    # Paths to profiles for different virtual users
    far_right_profile = "/right"
    far_left_profile = "/left"

    # Websites to simulate browsing
    far_right_websites = ["https://geenstijl.nl", "https://ongehoordnederland.tv/", "https://www.blckbx.tv/"]
    far_left_websites = ["https://www.bnnvara.nl/joop", "https://www.volkskrant.nl/"]

    # Search query
    search_query = "covid-19"

    # Simulate far-right user
    driver_right = create_browser(far_right_profile)
    simulate_browsing(driver_right, far_right_websites)
    far_right_results = perform_google_search(driver_right, search_query)
    driver_right.quit()

    # Simulate far-left user
    driver_left = create_browser(far_left_profile)
    simulate_browsing(driver_left, far_left_websites)
    far_left_results = perform_google_search(driver_left, search_query)
    driver_left.quit()

    # Analyze results
    df = pd.DataFrame({
        "Far Right Results": far_right_results,
        "Far Left Results": far_left_results
    })
    df.to_csv("google_search_results.csv", index=False)
    print("Results saved to google_search_results.csv")


if __name__ == "__main__":
    main()