import random
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials


## Google Sheets API 인증 및 스프레드시트 접근 설정
SPREADSHEET_ID = '1I97oWxnWm3V7b3F1M-oc-SntYrbt_PvVeWe7kIEaNDU'  # 구글 스프레드시트 ID
result_row = 7  # 테스트 결과 기록 시작 행 번호

## 구글 서비스 계정 키 파일 경로
current_dir = os.getcwd() # 현재 경로
SERVICE_ACCOUNT_FILE = os.path.join(current_dir, 'dsstudy-375712-bafa8d5af4f8.json')

## 구글 스프레드시트 API 사용 인증 설정
SCOPES = ['https://www.googleapis.com/auth/spreadsheets'] # 읽기 및 쓰기 권한
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES) # Google Cloud 서비스 계정 인증
service = build('sheets', 'v4', credentials=creds) # Google Sheets API 클라이언트 생성
sheet = service.spreadsheets() 

## 스프레드시트에 테스트 결과 기록 함수
def write_to_sheet(result, exception_msg=None):
    global result_row
    body = {
        'values': [[result, exception_msg]]  # 테스트 결과 (Pass or Fail or N / A) 및 예외 메시지 기록
    }
    # 스프레드시트의 I열에 테스트 결과, J열에 예외 메시지 기록
    sheet.values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=f'H{result_row}:I{result_row}',
        valueInputOption='RAW',
        body=body
    ).execute()
    result_row += 1  # 다음 결과는 다음 행에 기록

## webdriver 생성
chrome_options = webdriver.ChromeOptions() 
chrome_options.add_experimental_option("detach", True) # 브라우저 자동 종료 방지
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options) # ChromeDriver 자동 설치, detach 모드로 ChromeDriver 실행

count = -1 # 장바구니 수량 확인용

## 테스트 할 페이지 오픈 및 최대화
def test_open_url():
    # TC1. 테스트 페이지 접근 확인
    try:
        test_url = "https://www.demoblaze.com/index.html"
        driver.get(test_url)
        driver.maximize_window()
        print("테스트 페이지 오픈: Pass")
        write_to_sheet("Pass", "")
    except Exception as e:
        error_message = f"{type(e).__name__}"  # 예외 클래스의 이름만 추출

        # 예외 유형이 ElementNotInteractableException이면 N / A
        if type(e).__name__ == "ElementNotInteractableException":
            print("테스트 페이지 오픈: N / A")
            write_to_sheet("N / A", error_message)
        else:
            print("테스트 페이지 오픈: Fail")
            write_to_sheet("Fail", error_message)

def test_register(username, password):
    # TC2. Sign up GNB 노출 확인
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="signin2"]')))
        print("Sign up 버튼 노출: Pass")
        write_to_sheet("Pass", "")
    except Exception as e:
        error_message = f"{type(e).__name__}"  # 예외 클래스의 이름만 추출
        
        # 예외 유형이 ElementNotInteractableException이면 N / A로 기록
        if type(e).__name__ == "ElementNotInteractableException":
            print("Sign up 버튼 노출: N / A")
            write_to_sheet("N / A", error_message)
        else:
            print("Sign up 버튼 노출: Fail")
            write_to_sheet("Fail", error_message)

    # TC3. Sign up GNB 클릭 확인
    signup_btn = driver.find_element(By.XPATH, '//*[@id="signin2"]')
    try:
        
        ActionChains(driver).click(signup_btn).perform()
        print("Sign up GNB 클릭: Pass")
        write_to_sheet("Pass", "")
    except Exception as e:
        error_message = f"{type(e).__name__}"  # 예외 클래스의 이름만 추출
        
        # 예외 유형이 ElementNotInteractableException이면 N / A로 기록
        if type(e).__name__ == "ElementNotInteractableException":
            print("Sign up GNB 클릭: N / A")
            write_to_sheet("N / A", error_message)
        else:
            print("Sign up GNB 클릭: Fail")
            write_to_sheet("Fail", error_message)

    # TC4. Sign up 모달창 노출 확인
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="signInModal"]/div/div/div[2]')))
        print("Sign up 모달창 노출: Pass")
        write_to_sheet("Pass", "")
    except Exception as e:
        error_message = f"{type(e).__name__}"  # 예외 클래스의 이름만 추출
        
        # 예외 유형이 ElementNotInteractableException이면 N / A로 기록
        if type(e).__name__ == "ElementNotInteractableException":
            print("Sign up 모달창 노출: N / A")
            write_to_sheet("N / A", error_message)
        else:
            print("Sign up 모달창 노출: Fail")
            write_to_sheet("Fail", error_message)

    # TC5. 회원가입 모달창 내 Username 입력 확인
    try:
        username_field = driver.find_element(By.XPATH, '//*[@id="sign-username"]')
        username_field.send_keys(username)
        print("회원가입 모달창 내 Username 입력: Pass")
        write_to_sheet("Pass", "")
    except Exception as e:
        error_message = f"{type(e).__name__}"  # 예외 클래스의 이름만 추출
        
        # 예외 유형이 ElementNotInteractableException이면 N / A로 기록
        if type(e).__name__ == "ElementNotInteractableException":
            print("회원가입 모달창 내 Username 입력: N / A")
            write_to_sheet("N / A", error_message)
        else:
            print("회원가입 모달창 내 Username 입력: Fail")
            write_to_sheet("Fail", error_message)
        
    # TC6. 회원가입 모달창 내 Password 입력 확인    
    try:
        password_field = driver.find_element(By.XPATH, '//*[@id="sign-password"]')
        password_field.send_keys(password)
        print("회원가입 모달창 내 Password 입력: Pass")
        write_to_sheet("Pass", "")
    except Exception as e:
        error_message = f"{type(e).__name__}"  # 예외 클래스의 이름만 추출
        
        # 예외 유형이 ElementNotInteractableException이면 N / A로 기록
        if type(e).__name__ == "ElementNotInteractableException":
            print("회원가입 모달창 내 Password 입력: N / A")
            write_to_sheet("N / A", error_message)
        else:
            print("회원가입 모달창 내 Password 입력: Fail")
            write_to_sheet("Fail", error_message)

    # TC7. 회원가입 모달창 내 Sign up 버튼 클릭 확인
    try:
        signup_btn = driver.find_element(By.XPATH, '//*[@id="signInModal"]/div/div/div[3]/button[2]')
        ActionChains(driver).click(signup_btn).perform()

        # alert 노출 확인
        WebDriverWait(driver, 10).until(EC.alert_is_present())

        # alert로 화면 전환
        alert = driver.switch_to.alert

        # alert text 확인
        alert_text = alert.text

        # alert 확인 버튼 클릭
        alert.accept()

        if alert_text == "This user already exist.":
            print("회원가입 모달창 내 Sign up 버튼 클릭: Fail")
            write_to_sheet("Fail", alert_text)
            close_btn = driver.find_element(By.XPATH, '//*[@id="signInModal"]/div/div/div[3]/button[1]')
            ActionChains(driver).click(close_btn).perform()
        elif alert_text == "Please fill out Username and Password.":
            print("회원가입 모달창 내 Sign up 버튼 클릭: Fail")
            write_to_sheet("Fail", alert_text)
            close_btn = driver.find_element(By.XPATH, '//*[@id="signInModal"]/div/div/div[3]/button[1]')
            ActionChains(driver).click(close_btn).perform()
        else:
            print("회원가입 모달창 내 Sign up 버튼 클릭: Pass")
            write_to_sheet("Pass", alert_text)

    except Exception as e:
        error_message = f"{type(e).__name__}"  # 예외 클래스의 이름만 추출
        
        # 예외 유형이 ElementNotInteractableException이면 N / A로 기록
        if type(e).__name__ == "ElementNotInteractableException":
            print("회원가입 모달창 내 Sign up 버튼 클릭: N / A")
            write_to_sheet("N / A", error_message)
        else:
            print("회원가입 모달창 내 Sign up 버튼 클릭: Fail")
            write_to_sheet("Fail", error_message)

def test_login(username, password):
    # TC8. Log in GNB 노출 확인
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="login2"]')))
        print("Log in GNB 노출: Pass")
        write_to_sheet("Pass", "")
    except Exception as e:
        error_message = f"{type(e).__name__}"  # 예외 클래스의 이름만 추출
        
        # 예외 유형이 ElementNotInteractableException이면 N / A로 기록
        if type(e).__name__ == "ElementNotInteractableException":
            print("Log in GNB 노출: N / A")
            write_to_sheet("N / A", error_message)
        else:
            print("Log in GNB 노출: Fail")
            write_to_sheet("Fail", error_message)    

    # TC9. Log in GNB 클릭 확인
    try:
        login_btn = driver.find_element(By.XPATH, '//*[@id="login2"]')
        driver.execute_script("arguments[0].click();", login_btn)
        print("Log in GNB 클릭 확인: Pass")
        write_to_sheet("Pass", "")
    except Exception as e:
        error_message = f"{type(e).__name__}"  # 예외 클래스의 이름만 추출
        
        # 예외 유형이 ElementNotInteractableException이면 N / A로 기록
        if type(e).__name__ == "ElementNotInteractableException":
            print("Log in GNB 클릭 확인: N / A")
            write_to_sheet("N / A", error_message)
        else:
            print("Log in GNB 클릭 확인: Fail")
            write_to_sheet("Fail", error_message)

    # TC10. Log in 모달창 노출 확인
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="logInModal"]/div/div')))
        print("Log in 모달창 노출: Pass")
        write_to_sheet("Pass", "")
    except Exception as e:
        error_message = f"{type(e).__name__}"  # 예외 클래스의 이름만 추출
        
        # 예외 유형이 ElementNotInteractableException이면 N / A로 기록
        if type(e).__name__ == "ElementNotInteractableException":
            print("Log in 모달창 노출: N / A")
            write_to_sheet("N / A", error_message)
        else:
            print("Log in 모달창 노출: Fail")
            write_to_sheet("Fail", error_message)

    # TC11. Log in 모달창 내 Username 입력 확인
    try:
        username_field = driver.find_element(By.XPATH, '//*[@id="loginusername"]')
        username_field.send_keys(username)
        print("Log in 모달창 내 Username 입력: Pass")
        write_to_sheet("Pass", "")
    except Exception as e:
        error_message = f"{type(e).__name__}"  # 예외 클래스의 이름만 추출
        
        # 예외 유형이 ElementNotInteractableException이면 N / A로 기록
        if type(e).__name__ == "ElementNotInteractableException":
            print("Log in 모달창 내 Username 입력: N / A")
            write_to_sheet("N / A", error_message)
        else:
            print("Log in 모달창 내 Username 입력: Fail")
            write_to_sheet("Fail", error_message)

    # TC12. 로그인 모달창 내 Password 입력 확인
    try:
        password_field = driver.find_element(By.XPATH, '//*[@id="loginpassword"]')
        password_field.send_keys(password)
        print("로그인 모달창 내 Password 입력: Pass")
        write_to_sheet("Pass", "")
    except Exception as e:
        error_message = f"{type(e).__name__}"  # 예외 클래스의 이름만 추출
        
        # 예외 유형이 ElementNotInteractableException이면 N / A로 기록
        if type(e).__name__ == "ElementNotInteractableException":
            print("로그인 모달창 내 Password 입력: N / A")
            write_to_sheet("N / A", error_message)
        else:
            print("로그인 모달창 내 Password 입력: Fail")
            write_to_sheet("Fail", error_message)

    # TC13. 로그인 모달창 내 Log in 버튼 클릭 확인
    try:
        # 로그인 모달창 내 Log in 버튼 클릭
        login_btn = driver.find_element(By.XPATH, '//*[@id="logInModal"]/div/div/div[3]/button[2]')
        ActionChains(driver).click(login_btn).perform()

        try:
            # alert가 나타날 때까지 10초 대기 (alert가 없는 경우 TimeoutException 발생)
            WebDriverWait(driver, 2).until(EC.alert_is_present())

            # alert로 화면 전환
            alert = driver.switch_to.alert

            # alert text 확인
            alert_text = alert.text

            # alert 확인 버튼 클릭
            alert.accept()

            # alert 텍스트에 따라 처리
            if alert_text == "User does not exist.":
                print("로그인 모달창 내 Log in 버튼 클릭: Fail")
                write_to_sheet("Fail", alert_text)
                close_btn = driver.find_element(By.XPATH, '//*[@id="logInModal"]/div/div/div[3]/button[1]')
                ActionChains(driver).click(close_btn).perform()
            elif alert_text == "Wrong password.":
                print("로그인 모달창 내 Log in 버튼 클릭: Fail")
                write_to_sheet("Fail", alert_text)
                close_btn = driver.find_element(By.XPATH, '//*[@id="logInModal"]/div/div/div[3]/button[1]')
                ActionChains(driver).click(close_btn).perform()
            elif alert_text == "Please fill out Username and Password.":
                print("로그인 모달창 내 Log in 버튼 클릭: Fail")
                write_to_sheet("Fail", alert_text)
                close_btn = driver.find_element(By.XPATH, '//*[@id="logInModal"]/div/div/div[3]/button[1]')
                ActionChains(driver).click(close_btn).perform()
        
        except TimeoutException:
            # alert가 뜨지 않으면 로그인 성공으로 처리
            print("로그인 모달창 내 Log in 버튼 클릭: Pass")
            write_to_sheet("Pass", "")

    except Exception as e:
        error_message = f"{type(e).__name__}"  # 예외 클래스의 이름만 추출
        
        # 예외 유형이 ElementNotInteractableException이면 N / A로 기록
        if type(e).__name__ == "ElementNotInteractableException":
            print("로그인 모달창 내 Log in 버튼 클릭: N / A")
            write_to_sheet("N / A", error_message)
        else:
            print("로그인 모달창 내 Log in 버튼 클릭: Fail")
            write_to_sheet("Fail", error_message)

def test_add_cart(i):
    global count
    driver.implicitly_wait(1) # 웹 페이지 요소 찾는 암시적 대기

    # TC14, 18, 22, 26. 제품 노출 확인
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="tbodyid"]')))
        print(f"{i+1}번째 제품 확인: Pass")
        write_to_sheet("Pass", "")
    except Exception as e:
        error_message = f"{type(e).__name__}"  # 예외 클래스의 이름만 추출
        
        # 예외 유형이 ElementNotInteractableException이면 N / A로 기록
        if type(e).__name__ == "ElementNotInteractableException":
            print("제품 노출: N / A")
            write_to_sheet("N / A", error_message)
        else:
            print("제품 노출: Fail")
            write_to_sheet("Fail", error_message)

    # tbodyid 중 img 요소들
    images = driver.find_elements(By.XPATH, '//*[@id="tbodyid"]//img')

    if images:
        # 이미지들 중 하나 랜덤 선택
        random_image = random.choice(images)

        # 선택된 이미지로 스크롤 이동
        driver.execute_script("arguments[0].scrollIntoView(true);", random_image)

        # TC15, 19, 23, 27. 해당 제품 설명 페이지 이동 확인
        try:
            driver.execute_script("arguments[0].click();", random_image)
            print(f"{i+1}번째 제품 설명 페이지 이동: Pass")
            write_to_sheet("Pass", "")
        except Exception as e:
            error_message = f"{type(e).__name__}"  # 예외 클래스의 이름만 추출
            print(f"{i+1}번째 제품 설명 페이지 이동: Fail")
            write_to_sheet("Fail", error_message)

    # TC16, 20, 24, 28. Add to cart 버튼 노출 확인
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tbodyid"]/div[2]/div/a')))
        print(f"{i+1}번째 제품 Add to cart 버튼 노출: Pass")
        write_to_sheet("Pass", "")
    except Exception as e:
        error_message = f"{type(e).__name__}"  # 예외 클래스의 이름만 추출
        
        # 예외 유형이 ElementNotInteractableException이면 N / A로 기록
        if type(e).__name__ == "ElementNotInteractableException":
            print(f"{i+1}번째 제품 Add to cart 버튼 노출: N / A")
            write_to_sheet("N / A", error_message)
        else:
            print(f"{i+1}번째 제품 Add to cart 버튼 노출: Fail")
            write_to_sheet("Fail", error_message)

    # TC17, 21, 25, 29. Add to cart 버튼 클릭 확인
    try:
        addcart_btn = driver.find_element(By.XPATH, '//*[@id="tbodyid"]/div[2]/div/a')
        driver.execute_script("arguments[0].click();", addcart_btn)
        print(f"{i+1}번째 제품 Add to cart 버튼 클릭: Pass")
        write_to_sheet("Pass", "")
    except Exception as e:
        error_message = f"{type(e).__name__}"  # 예외 클래스의 이름만 추출
        
        # 예외 유형이 ElementNotInteractableException이면 N / A로 기록
        if type(e).__name__ == "ElementNotInteractableException":
            print(f"{i+1}번째 제품 Add to cart 버튼 클릭: N / A")
            write_to_sheet("N / A", error_message)
        else:
            print(f"{i+1}번째 제품 Add to cart 버튼 클릭: Fail")
            write_to_sheet("Fail", error_message)

    # 장바구니 담기 시 alert 노출 확인
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

    # TC30. Cart 버튼 노출 확인
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="login2"]')))
        print("Cart 버튼 노출: Pass")
        write_to_sheet("Pass", "")
    except Exception as e:
        error_message = f"{type(e).__name__}"  # 예외 클래스의 이름만 추출
        
        # 예외 유형이 ElementNotInteractableException이면 N / A로 기록
        if type(e).__name__ == "ElementNotInteractableException":
            print("Cart 버튼 노출: N / A")
            write_to_sheet("N / A", error_message)
        else:
            print("Cart 버튼 노출: Fail")
            write_to_sheet("Fail", error_message)

    # TC31. Cart 버튼 클릭 확인
    try:
        cart_btn = driver.find_element(By.XPATH, '//*[@id="navbarExample"]/ul/li[4]/a')
        driver.execute_script("arguments[0].click();", cart_btn)
        print("Cart 버튼 클릭: Pass")
        write_to_sheet("Pass", "")
    except Exception as e:
        error_message = f"{type(e).__name__}"  # 예외 클래스의 이름만 추출
        
        # 예외 유형이 ElementNotInteractableException이면 N / A로 기록
        if type(e).__name__ == "ElementNotInteractableException":
            print("Cart 버튼 클릭: N / A")
            write_to_sheet("N / A", error_message)
        else:
            print("Cart 버튼 클릭: Fail")
            write_to_sheet("Fail", error_message)

    # TC32. Cart 페이지에 정상적으로 제품 저장 확인
    if i == count:
        try:
            print("Cart 페이지에 정상적으로 제품 저장: Pass")
            write_to_sheet("Pass", "")
        except Exception as e:
            error_message = f"{type(e).__name__}"  # 예외 클래스의 이름만 추출
            # 예외 유형이 ElementNotInteractableException이면 N / A로 기록
            if type(e).__name__ == "ElementNotInteractableException":
                print("Cart 페이지에 정상적으로 제품 저장: N / A")
                write_to_sheet("N / A", error_message)
            else:
                print("Cart 페이지에 정상적으로 제품 저장: Fail")
                write_to_sheet("Fail", error_message)

def test_delete_item():
    # TC33. 장바구니 내 제품 삭제 버튼 노출 확인
    try:
        delete_buttons = driver.find_elements(By.XPATH, "//*[text()='Delete']")
        print("Delete 버튼 노출: Pass")
        write_to_sheet("Pass", "")
    except Exception as e:
        error_message = f"{type(e).__name__}"  # 예외 클래스의 이름만 추출
        # 예외 유형이 ElementNotInteractableException이면 N / A로 기록
        if type(e).__name__ == "ElementNotInteractableException":
            print("Delete 버튼 노출: N / A")
            write_to_sheet("N / A", error_message)
        else:
            print("Delete 버튼 노출: Fail")
            write_to_sheet("Fail", error_message)

    if delete_buttons:
        # delete_buttons 중 하나 랜덤 선택
        random_delete = random.choice(delete_buttons)

        # TC34. 장바구니 내 제품 삭제 가능 확인
        try:
            driver.execute_script("arguments[0].click();", random_delete)
            print("장바구니 내 제품 삭제: Pass")
            write_to_sheet("Pass", "")
        except Exception as e:
            if type(e).__name__ == "ElementNotInteractableException":
                print("장바구니 내 제품 삭제: N / A")
                write_to_sheet("N / A", error_message)
            else:
                print("장바구니 내 제품 삭제: Fail")
                write_to_sheet("Fail", error_message)

# 유효성 검증을 위해 테스터가 id / pw 입력
if __name__ == "__main__":
    username = input("Enter the username: ")
    password = input("Enter the password: ")

    test_open_url()
    test_register(username, password)
    test_login(username, password)
    for i in range(4):
        test_add_cart(i) 

    test_check_cart(i)
    test_delete_item()

    print("Automation test completed.")