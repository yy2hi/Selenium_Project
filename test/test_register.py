import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.parametrize("username,password", [("testuser", "testpassword")])
def test_register(driver, username, password):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="signin2"]'))).click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="signInModal"]/div/div/div[2]')))
    
    driver.find_element(By.XPATH, '//*[@id="sign-username"]').send_keys(username)
    driver.find_element(By.XPATH, '//*[@id="sign-password"]').send_keys(password)
    driver.find_element(By.XPATH, '//*[@id="signInModal"]/div/div/div[3]/button[2]').click()

    assert "Sign up successful" in driver.page_source, "회원가입 실패"
