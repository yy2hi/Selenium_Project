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
    # 스프레드시트의 I열에 결과 기록
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

# 테스트 할 페이지 오픈 및 최대화
def open_url(driver):
    try:
        test_url = "https://www.demoblaze.com/index.html"
        driver.get(test_url)
        driver.maximize_window()
        write_to_sheet("Pass")  # 페이지 열기 성공
    except Exception as e:
        write_to_sheet("Fail")  # 페이지 열기 실패
        pytest.fail(f"Open_url Failed with exception: {e}")

# 회원가입 테스트
def register(driver, username, password):
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="signin2"]')))
        signup_btn = driver.find_element(By.XPATH, '//*[@id="signin2"]')
        driver.execute_script("arguments[0].click();", signup_btn)
        write_to_sheet("Pass")  # Sign up 버튼 클릭 성공
    except Exception as e:
        write_to_sheet("Fail")
        pytest.fail(f"Sign up button click failed: {e}")

    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="signInModal"]/div/div/div[2]')))
        username_field = driver.find_element(By.XPATH, '//*[@id="sign-username"]')
        username_field.send_keys(username)
        write_to_sheet("Pass")  # Username 입력 성공
    except Exception as e:
        write_to_sheet("Fail")
        pytest.fail(f"Username input failed: {e}")

    try:
        password_field = driver.find_element(By.XPATH, '//*[@id="sign-password"]')
        password_field.send_keys(password)
        write_to_sheet("Pass")  # Password 입력 성공
    except Exception as e:
        write_to_sheet("Fail")
        pytest.fail(f"Password input failed: {e}")

    try:
        signup_btn = driver.find_element(By.XPATH, '//*[@id="signin2"]')
        ActionChains(driver).click(signup_btn).perform()
        write_to_sheet("Pass")  # 회원가입 완료 성공
    except Exception as e:
        write_to_sheet("Fail")
        pytest.fail(f"Sign up process failed: {e}")

# 로그인 테스트
def login(driver, username, password):
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="login2"]')))
        login_btn = driver.find_element(By.XPATH, '//*[@id="login2"]')
        driver.execute_script("arguments[0].click();", login_btn)
        write_to_sheet("Pass")  # Login 버튼 클릭 성공
    except Exception as e:
        write_to_sheet("Fail")  # Login 버튼 클릭 실패
        pytest.fail(f"Login button click failed: {e}")

    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="logInModal"]/div/div/div[2]')))
        username_field = driver.find_element(By.XPATH, '//*[@id="loginusername"]')
        username_field.send_keys(username)
        write_to_sheet("Pass")  # Username 입력 성공
    except Exception as e:
        write_to_sheet("Fail")  # Username 입력 실패
        pytest.fail(f"Username input failed: {e}")

    try:
        password_field = driver.find_element(By.XPATH, '//*[@id="loginpassword"]')
        password_field.send_keys(password)
        write_to_sheet("Pass")  # Password 입력 성공
    except Exception as e:
        write_to_sheet("Fail")  # Password 입력 실패
        pytest.fail(f"Password input failed: {e}")

    try:
        login_btn = driver.find_element(By.XPATH, '//*[@id="logInModal"]/div/div/div[3]/button[2]')
        driver.execute_script("arguments[0].click();", login_btn)
        write_to_sheet("Pass")  # Log in 버튼 클릭 성공
    except Exception as e:
        write_to_sheet("Fail")  # Log in 버튼 클릭 실패
        pytest.fail(f"Log in button click failed: {e}")

# 장바구니 추가 테스트
def add_cart(driver):
    global count
    count = 0  # 카운트를 초기화

    try:
        for i in range(4):
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="tbodyid"]')))
            tbody = driver.find_element(By.XPATH, '//*[@id="tbodyid"]')
            images = tbody.find_elements(By.TAG_NAME, 'img')

            if images:
                random_image = random.choice(images)
                driver.execute_script("arguments[0].scrollIntoView(true);", random_image)
                driver.execute_script("arguments[0].click();", random_image)
                write_to_sheet(f"상품 선택 {i+1}번째 Pass")
            else:
                write_to_sheet(f"상품 선택 {i+1}번째 Fail")
                pytest.fail(f"Product selection {i+1} failed: No images found")

            # Add to cart 클릭
            try:
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tbodyid"]/div[2]/div/a')))
                addcart_btn = driver.find_element(By.XPATH, '//*[@id="tbodyid"]/div[2]/div/a')
                driver.execute_script("arguments[0].click();", addcart_btn)
                write_to_sheet(f"Add to cart {i+1}번째 Pass")
                count += 1  # 성공적으로 카트에 추가될 때마다 카운트 증가
            except Exception as e:
                write_to_sheet(f"Add to cart {i+1}번째 Fail")
                pytest.fail(f"Add to cart button click failed: {e}")

        # 4번 수행이 완료되면 성공 메시지
        write_to_sheet("4번 장바구니 추가 수행 Pass")

    except Exception as e:
        write_to_sheet("Fail")
        pytest.fail(f"Add_cart Failed with exception: {e}")

# 장바구니 검증 테스트 (count와 i 비교)
def check_cart(i):
    global count
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="login2"]')))
        cart_btn = driver.find_element(By.XPATH, '//*[@id="navbarExample"]/ul/li[4]/a')
        driver.execute_script("arguments[0].click();", cart_btn)

        # i와 count가 같은지 비교
        if i == count:
            write_to_sheet(f"Cart 확인 Pass - count와 i 값이 같습니다. (count: {count}, i: {i})")
        else:
            write_to_sheet(f"Cart 확인 Fail - count({count})와 i({i})가 다릅니다.")
            pytest.fail(f"Cart count mismatch: i({i}) vs count({count})")
    except Exception as e:
        write_to_sheet("Fail")
        pytest.fail(f"Check_cart Failed with exception: {e}")

# 장바구니 아이템 삭제 테스트
def delete_item(driver):
    try:
        # 모든 "Delete" 텍스트가 포함된 요소를 찾습니다.
        delete_buttons = driver.find_elements(By.XPATH, "//*[text()='Delete']")
        
        if delete_buttons:
            # 무작위로 하나의 삭제 버튼 선택
            random_delete = random.choice(delete_buttons)
            driver.execute_script("arguments[0].click();", random_delete)
            write_to_sheet("Delete 아이템 Pass")  # 삭제 성공
        else:
            write_to_sheet("Delete 아이템 Fail")  # 삭제 버튼이 없음
            pytest.fail("No delete buttons found")
    except Exception as e:
        write_to_sheet("Delete 아이템 Fail")
        pytest.fail(f"Delete_item Failed with exception: {e}")

# 테스트 실행
if __name__ == "__main__":
    username = input("Enter the username: ")
    password = input("Enter the password: ")

    # WebDriver 준비
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # 테스트 단계 순차 실행
    open_url(driver)
    register(driver, username, password)
    login(driver, username, password)
    add_cart(driver)

    # 4번 추가 후 count와 i 값 비교
    check_cart(4)

    # 아이템 삭제 테스트
    delete_item(driver)

    print("테스트 완료 및 결과 기록됨.")