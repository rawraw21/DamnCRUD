from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# Path ke WebDriver (sesuaikan dengan sistem Anda)
driver = webdriver.Chrome()

# 1. Test Case: Validasi Alur Login
def test_valid_login():
    driver.get("http://localhost/DamnCRUD-main/login.php")

    # Tunggu hingga elemen username muncul
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

    # Masukkan kredensial yang benar
    driver.find_element(By.NAME, "username").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("nimda666!")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)

    # Verifikasi apakah login berhasil (misalnya, dengan mengecek keberadaan dashboard)
    assert "Dashboard" in driver.title  # Sesuaikan dengan judul halaman setelah login

# 2. Test Case: Login dengan Kredensial Salah
def test_invalid_login():
    driver.get("http://localhost/DamnCRUD-main/login.php")
    driver.find_element(By.NAME, "username").send_keys("wronguser")
    driver.find_element(By.NAME, "password").send_keys("wrongpass")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)
    error_message = driver.find_element(By.ID, "error-msg").text
    assert "Login gagal" in error_message

# 3. Test Case: Akses Halaman Tanpa Login
def test_access_without_login():
    driver.get("http://localhost/DamnCRUD-main/profil.php")
    time.sleep(2)
    assert "Login" in driver.title  # Pastikan diarahkan ke halaman login

# 4. Test Case: Menambahkan Data Baru
def test_add_data():
    test_valid_login()  # Pastikan login dulu
    driver.get("http://localhost/DamnCRUD-main/create.php")
    driver.find_element(By.NAME, "name").send_keys("Test User")
    driver.find_element(By.NAME, "email").send_keys("test@example.com")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)
    assert "Data berhasil ditambahkan" in driver.page_source

# 5. Test Case: Menghapus Data
def test_delete_data():
    test_valid_login()  # Pastikan login dulu
    driver.get("http://localhost/DamnCRUD-main/index.php")
    delete_buttons = driver.find_elements(By.CLASS_NAME, "delete-btn")
    if delete_buttons:
        delete_buttons[0].click()
        time.sleep(2)
        assert "Data berhasil dihapus" in driver.page_source

# Jalankan test case
test_valid_login()
test_invalid_login()
test_access_without_login()
test_add_data()
test_delete_data()

# Tutup browser setelah selesai
driver.quit()
