from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from secret import EMAIL, PASSWORD
import time
from datetime import datetime
import argparse


def get_options() -> Options:
    options = Options()
    if args.headless:
        options.add_argument("--headless")
    options.add_argument("--mute-audio")
    options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 2})
    return options


def login_to_facebook() -> None:
    print("Loading facebook...")
    driver.get("https://facebook.com/pokes")

    email_box = driver.find_element(By.ID, "email")
    password_box = driver.find_element(By.ID, "pass")
    login_btn = driver.find_element(By.ID, "loginbutton")

    print("Logging in...")

    email_box.send_keys(EMAIL)
    password_box.send_keys(PASSWORD)
    login_btn.click()


def make_pokes() -> None:
    poke_xpath = "//*[contains(text(), 'Poke Back')]"

    name_xpath = "//a[contains(@href, 'https://www.facebook.com')]"

    print("Searching for pokes...")
    while True:
        if not args.norefresh:
            driver.refresh()
        assert "pokes" in driver.current_url

        # check if you're blocked xd
        if close_btn := driver.find_elements(By.CSS_SELECTOR, "[aria-label=Close]"):
            close_btn[0].click()

        poke_btns = driver.find_elements(By.XPATH, poke_xpath)
        names = driver.find_elements(By.XPATH, name_xpath)[-len(poke_btns):]

        cur_time = datetime.now().strftime("[%I:%M:%S]")
        for btn, name in zip(poke_btns, names):
            streak_txt = name.find_element(By.XPATH, "..").text.split(" ")
            count = next((el for el in streak_txt if el.isdigit()), 0)
            print(f"{cur_time} poked {name.text}! ({count})")
            btn.click()
        time.sleep(args.time)
 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--time", type=int, default=60, help="delay betweeen pokes, defaults to 60 sec.")
    parser.add_argument("-H", "--headless", action="store_true", help="run browser in headless modes")
    parser.add_argument("-v", "--verbose", action="store_true", help="enable verbose output")
    parser.add_argument("-nr", "--norefresh", action="store_true", help="no refresh of page between pokes")
    args = parser.parse_args()
    options = get_options()
    driver: Chrome = Chrome(options=options)
    login_to_facebook()
    make_pokes()
