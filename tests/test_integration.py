import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture
def browser():
    """Setup WebDriver dengan Chrome Headless Mode."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Jalankan tanpa UI
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    yield driver
    driver.quit()

def test_valid_login(browser):
    """Test login dengan kredensial valid (admin/nimda666!)."""
    browser.get("http://localhost/login")
    
    username_input = browser.find_element(By.NAME, "username")
    password_input = browser.find_element(By.NAME, "password")
    login_button = browser.find_element(By.NAME, "submit")

    username_input.send_keys("admin")
    password_input.send_keys("nimda666!")
    login_button.click()

    assert "Dashboard" in browser.title

def test_invalid_login(browser):
    """Test login dengan kredensial salah."""
    browser.get("http://localhost/login")
    
    username_input = browser.find_element(By.NAME, "username")
    password_input = browser.find_element(By.NAME, "password")
    login_button = browser.find_element(By.NAME, "submit")

    username_input.send_keys("wrong_user")
    password_input.send_keys("wrong_pass")
    login_button.click()

    error_message = browser.find_element(By.ID, "error-message").text
    assert "Invalid username or password" in error_message

def test_access_without_login(browser):
    """Test akses halaman profil tanpa login."""
    browser.get("http://localhost/profile")
    
    # Pastikan pengguna dialihkan ke halaman login
    assert "Login" in browser.title
    assert browser.current_url.endswith("/login")

def test_create_new_data(browser):
    """Test menambahkan data baru setelah login sebagai admin."""
    browser.get("http://localhost/login")
    
    # Login dengan user admin
    username_input = browser.find_element(By.NAME, "username")
    password_input = browser.find_element(By.NAME, "password")
    login_button = browser.find_element(By.NAME, "submit")

    username_input.send_keys("admin")
    password_input.send_keys("nimda666!")
    login_button.click()

    browser.get("http://localhost/create")
    
    name_input = browser.find_element(By.NAME, "name")
    email_input = browser.find_element(By.NAME, "email")
    submit_button = browser.find_element(By.NAME, "submit")

    name_input.send_keys("Test User")
    email_input.send_keys("testuser@example.com")
    submit_button.click()

    # Cek apakah data muncul di daftar
    browser.get("http://localhost/index")
    assert "Test User" in browser.page_source
    assert "testuser@example.com" in browser.page_source

def test_logout(browser):
    """Test logout dari sistem setelah login sebagai admin."""
    browser.get("http://localhost/login")
    
    # Login terlebih dahulu
    username_input = browser.find_element(By.NAME, "username")
    password_input = browser.find_element(By.NAME, "password")
    login_button = browser.find_element(By.NAME, "submit")

    username_input.send_keys("admin")
    password_input.send_keys("nimda666!")
    login_button.click()

    browser.get("http://localhost/logout")
    
    # Pastikan pengguna kembali ke halaman login
    assert "Login" in browser.title
    assert browser.current_url.endswith("/login")
