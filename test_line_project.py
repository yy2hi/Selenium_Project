import random
import pytest
import os
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
current_dir = os.getcwd()
SERVICE_ACCOUNT_FILE = os.path.join(current_dir, 'dsstudy-375712-bafa8d5af4f8.json')

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

# webdriver 생성
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

count = -1

# 테스트 할 페이지 오픈 및 최대화
def test_open_url():
    try:
        test_url = "https://www.demoblaze.com/index.html"
        driver.get(test_url)
        driver.maximize_window()
        write_to_sheet("Pass")
    except Exception as e:
        write_to_sheet("Fail")
        pytest.fail(f"Failed with exception: {e}")


def test_register(username, password):
    try:
        # Sign up 버튼 대기
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="signin2"]'))) 
        write_to_sheet("Pass")
    except Exception as e:
        write_to_sheet("Fail")
        pytest.fail(f"Failed with exception: {e}")

    # Sign up 버튼 클릭
    try:
        signup_btn = driver.find_element(By.XPATH, '//*[@id="signin2"]')
        ActionChains(driver).click(signup_btn).perform()
        write_to_sheet("Pass")
    except Exception as e:
        write_to_sheet("Fail")
        pytest.fail(f"Failed with exception: {e}")

    # Sign up 모달창 대기
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="signInModal"]/div/div/div[2]')))

    try:
        # 회원가입 모달창 내 Username 입력
        username_field = driver.find_element(By.XPATH, '//*[@id="sign-username"]')
        username_field.send_keys(username)
        write_to_sheet("Pass")
    except Exception as e:
        write_to_sheet("Fail")
        pytest.fail(f"Failed with exception: {e}")
        
    try:
        # 회원가입 모달창 내 Password 입력 
        password_field = driver.find_element(By.XPATH, '//*[@id="sign-password"]')
        password_field.send_keys(password)
        write_to_sheet("Pass")
    except Exception as e:
        write_to_sheet("Fail")
        pytest.fail(f"Failed with exception: {e}")

    try:
        # 회원가입 모달창 내 Sign up 버튼 클릭
        signup_btn = driver.find_element(By.XPATH, '//*[@id="signin2"]')
        ActionChains(driver).click(signup_btn).perform()
    except Exception as e:
        write_to_sheet("Fail")
        pytest.fail(f"Failed with exception: {e}")

def test_login(username, password):
    # Login 버튼 노출 대기
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="login2"]')))

    try:
        # Login 버튼 클릭
        login_btn = driver.find_element(By.XPATH, '//*[@id="login2"]')
        driver.execute_script("arguments[0].click();", login_btn)
        write_to_sheet("Pass")
    except Exception as e:
        write_to_sheet("Fail")
        pytest.fail(f"Failed with exception: {e}")

    # Login 모달창 대기
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="logInModal"]/div/div/div[2]')))

    try:
        # 로그인 모달창 내 Username 입력
        username_field = driver.find_element(By.XPATH, '//*[@id="loginusername"]')
        username_field.send_keys(username)
        write_to_sheet("Pass")
    except Exception as e:
        write_to_sheet("Fail")
        pytest.fail(f"Failed with exception: {e}")

    try:
        # 로그인 모달창 내 Password 입력 
        password_field = driver.find_element(By.XPATH, '//*[@id="loginpassword"]')
        password_field.send_keys(password)
        write_to_sheet("Pass")
    except Exception as e:
        write_to_sheet("Fail")
        pytest.fail(f"Failed with exception: {e}")

    try:
        # 로그인 모달창 내 Log in 버튼 클릭
        signup_btn = driver.find_element(By.XPATH, '//*[@id="signin2"]')
        ActionChains(driver).click(signup_btn).perform()
        write_to_sheet("Pass")
    except Exception as e:
        write_to_sheet("Fail")
        pytest.fail(f"Failed with exception: {e}")
def test_add_cart():
    global count

    driver.implicitly_wait(1)

    # tbody 노출 대기
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="tbodyid"]')))

    # tbody의 ID가 'tbodyid'인 요소를 찾습니다.
    tbody = driver.find_element(By.XPATH, '//*[@id="tbodyid"]')

    # tbody 안의 모든 이미지 요소를 찾습니다.
    images = tbody.find_elements(By.TAG_NAME, 'img')

    # 이미지 목록이 비어있는지 확인합니다.
    if images:
        # 이미지들 중 하나를 랜덤으로 선택합니다.
        random_image = random.choice(images)

        # 선택된 이미지로 스크롤 이동
        driver.execute_script("arguments[0].scrollIntoView(true);", random_image)

        try:
            # 선택된 이미지 강제로 클릭 (JavaScript로 클릭)
            driver.execute_script("arguments[0].click();", random_image)
            write_to_sheet("Pass")
        except Exception as e:
            write_to_sheet("Fail")
            pytest.fail(f"Failed with exception: {e}")
    else:
        print("tbody 안에 이미지가 없습니다.")

    # Add to cart 버튼 노출 대기
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tbodyid"]/div[2]/div/a')))

    try:
        # Add to cart 버튼 클릭
        addcart_btn = driver.find_element(By.XPATH, '//*[@id="tbodyid"]/div[2]/div/a')
        driver.execute_script("arguments[0].click();", addcart_btn)
        write_to_sheet("Pass")
    except Exception as e:
        write_to_sheet("Fail")
        pytest.fail(f"Failed with exception: {e}")

    # alert 노출 대기
    WebDriverWait(driver, 10).until(EC.alert_is_present())

    # alert로 화면 전환
    alert = driver.switch_to.alert

    # alert 확인 버튼 클릭
    alert.accept()

    # 홈으로 이동
    home_btn = driver.find_element(By.XPATH, '//*[@id="nava"]')
    driver.execute_script("arguments[0].click();", home_btn)

    count += 1

def test_check_cart(i):
    global count  # 전역 변수 count 사용

    # Cart 버튼 노출 대기
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="login2"]')))

    try:
        # Cart 버튼 클릭
        cart_btn = driver.find_element(By.XPATH, '//*[@id="navbarExample"]/ul/li[4]/a')
        driver.execute_script("arguments[0].click();", cart_btn)
        write_to_sheet("Pass")
    except Exception as e:
        write_to_sheet("Fail")
        pytest.fail(f"Failed with exception: {e}")

    # i와 count 비교
    if i == count:
        print("Success: i와 count가 같습니다.")
        try:
            write_to_sheet("Pass")
        except Exception as e:
            write_to_sheet("Fail")
            pytest.fail(f"Failed with exception: {e}")

    else:
        print(f"Failure: i({i})와 count({count})가 다릅니다.")

def test_delete_item():
    # 모든 "Delete" 텍스트가 포함된 요소를 찾습니다.
    delete_buttons = driver.find_elements(By.XPATH, "//*[text()='Delete']")

    # Delete 요소들이 존재하는지 확인
    if delete_buttons:
        # 무작위로 하나 선택
        random_delete = random.choice(delete_buttons)

        # 선택된 요소 클릭
        try:
            driver.execute_script("arguments[0].click();", random_delete)
            print("랜덤으로 'Delete' 버튼을 클릭했습니다.")
            write_to_sheet("Pass")
        except Exception as e:
            write_to_sheet("Fail")
            pytest.fail(f"Failed with exception: {e}")
    else:
        print("'Delete' 버튼을 찾을 수 없습니다.")


# 유효성 검증을 위해 테스터가 id / pw 입력
if __name__ == "__main__":
    username = input("Enter the username: ")
    password = input("Enter the password: ")

    test_open_url()
    test_register(username, password)
    test_login(username, password)
    for i in range(4):
        test_add_cart() 

    test_check_cart(i)
    test_delete_item()

    print("automation finish")