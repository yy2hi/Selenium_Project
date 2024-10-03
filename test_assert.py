import random
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

# Google Sheets API 인증 및 스프레드시트 접근 설정
SPREADSHEET_ID = '1I97oWxnWm3V7b3F1M-oc-SntYrbt_PvVeWe7kIEaNDU'  # 구글 스프레드시트 ID
BASE_ROW = 7  # I열에 기록을 시작할 행 번호
result_row = BASE_ROW  # 테스트 결과를 기록할 행 번호

# 서비스 계정 키 파일 경로 (Google Cloud Console에서 받은 JSON 파일)
SERVICE_ACCOUNT_FILE = 'C:\\Project\\Python\\LINE_Project\\dsstudy-375712-bafa8d5af4f8.json'

# 구글 스프레드시트 API에 접근하기 위한 인증 설정
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

# Google 스프레드시트에 결과를 기록하는 함수
def write_to_sheet(result):
    global result_row
    body = {
        'values': [[result]]  # 결과 값 (Pass 또는 Fail) 기록
    }
    # 스프레드시트의 I열에 결과 기록 (행 번호는 result_row에서 시작)
    sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=f'I{result_row}:I{result_row}', valueInputOption='RAW', body=body).execute()
    result_row += 1  # 다음 결과는 다음 행에 기록

@pytest.fixture(scope="session")
def driver():
    # ChromeDriver 생성
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    yield driver
    driver.quit()

# Open_url을 사전 조건으로 사용하는 fixture
@pytest.fixture(scope="function", autouse=True)
def open_url(driver):
    # 테스트 할 페이지 오픈 및 최대화
    test_url = "https://www.demoblaze.com/index.html"
    driver.get(test_url)
    driver.maximize_window()

# 로그인 작업을 미리 처리하는 함수
def test_login(driver):
    try:
        username = "testuser"
        password = "password123"
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="login2"]')))
        login_btn = driver.find_element(By.XPATH, '//*[@id="login2"]')
        driver.execute_script("arguments[0].click();", login_btn)
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="logInModal"]/div/div/div[2]')))
        username_field = driver.find_element(By.XPATH, '//*[@id="loginusername"]')
        username_field.send_keys(username)
        password_field = driver.find_element(By.XPATH, '//*[@id="loginpassword"]')
        password_field.send_keys(password)
        login_btn = driver.find_element(By.XPATH, '//*[@id="signin2"]')
        ActionChains(driver).click(login_btn).perform()
        write_to_sheet("Pass")
    except Exception as e:
        write_to_sheet("Fail")
        pytest.fail(f"Failed with exception: {e}")

# test_add_cart는 open_url과 test_login이 먼저 실행되어야 함
def test_add_cart(driver):
    test_login(driver)  # 먼저 로그인 실행

    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="tbodyid"]')))
        tbody = driver.find_element(By.XPATH, '//*[@id="tbodyid"]')
        images = tbody.find_elements(By.TAG_NAME, 'img')
        if images:
            random_image = random.choice(images)
            driver.execute_script("arguments[0].scrollIntoView(true);", random_image)
            driver.execute_script("arguments[0].click();", random_image)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tbodyid"]/div[2]/div/a')))
            addcart_btn = driver.find_element(By.XPATH, '//*[@id="tbodyid"]/div[2]/div/a')
            driver.execute_script("arguments[0].click();", addcart_btn)
            WebDriverWait(driver, 10).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert.accept()
            write_to_sheet("Pass")
        else:
            write_to_sheet("Fail")
            pytest.fail("No images found")
    except Exception as e:
        write_to_sheet("Fail")
        pytest.fail(f"Failed with exception: {e}")

# test_delete_item은 open_url, test_login, test_add_cart가 먼저 실행되어야 함
def test_delete_item(driver):
    test_login(driver)  # 로그인 먼저 실행
    test_add_cart(driver)  # 장바구니에 아이템 추가 먼저 실행

    try:
        delete_buttons = driver.find_elements(By.XPATH, "//*[text()='Delete']")
        if delete_buttons:
            random_delete = random.choice(delete_buttons)
            driver.execute_script("arguments[0].click();", random_delete)
            write_to_sheet("Pass")
        else:
            write_to_sheet("Fail")
            pytest.fail("No delete buttons found")
    except Exception as e:
        write_to_sheet("Fail")
        pytest.fail(f"Failed with exception: {e}")
