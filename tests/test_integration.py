import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

@pytest.fixture
def browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Jalankan tanpa UI
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_valid_login(browser):
    browser.get("http://localhost/login")
    username_input = browser.find_element(By.NAME, "username")
    password_input = browser.find_element(By.NAME, "password")
    login_button = browser.find_element(By.NAME, "submit")

    username_input.send_keys("admin")
    password_input.send_keys("nimda666!")
    login_button.click()

    assert "Dashboard" in browser.title
