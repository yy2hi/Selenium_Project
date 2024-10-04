import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.parametrize("username,password", [("testuser", "testpassword")])
def test_login(driver, username, password):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="login2"]'))).click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="logInModal"]/div/div/div[2]')))
    
    driver.find_element(By.XPATH, '//*[@id="loginusername"]').send_keys(username)
    driver.find_element(By.XPATH, '//*[@id="loginpassword"]').send_keys(password)
    driver.find_element(By.XPATH, '//*[@id="logInModal"]/div/div/div[3]/button[2]').click()

    assert "Welcome" in driver.page_source, "로그인 실패"
