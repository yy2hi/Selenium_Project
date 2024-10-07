from __common__ import *
from __openurl__ import open_url

def register(username, password):
    # TC2. Sign up GNB 노출 확인
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="signin2"]')))
        print("Sign up 버튼 노출: Pass")
        write_to_sheet("Register", "Pass", "")
    except Exception as e:
        error_message = f"{type(e).__name__}"  # 예외 클래스의 이름만 추출
        
        # 예외 유형이 ElementNotInteractableException이면 N / A로 기록
        if type(e).__name__ == "ElementNotInteractableException":
            print("Sign up 버튼 노출: N / A")
            write_to_sheet("Register", "N / A", error_message)
        else:
            print("Sign up 버튼 노출: Fail")
            write_to_sheet("Register", "Fail", error_message)

    # TC3. Sign up GNB 클릭 확인
    signup_btn = driver.find_element(By.XPATH, '//*[@id="signin2"]')
    try:
        
        ActionChains(driver).click(signup_btn).perform()
        print("Sign up GNB 클릭: Pass")
        write_to_sheet("Register", "Pass", "")
    except Exception as e:
        error_message = f"{type(e).__name__}"  # 예외 클래스의 이름만 추출
        
        # 예외 유형이 ElementNotInteractableException이면 N / A로 기록
        if type(e).__name__ == "ElementNotInteractableException":
            print("Sign up GNB 클릭: N / A")
            write_to_sheet("Register", "N / A", error_message)
        else:
            print("Sign up GNB 클릭: Fail")
            write_to_sheet("Register", "Fail", error_message)

    # TC4. Sign up 모달창 노출 확인
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="signInModal"]/div/div/div[2]')))
        print("Sign up 모달창 노출: Pass")
        write_to_sheet("Register", "Pass", "")
    except Exception as e:
        error_message = f"{type(e).__name__}"  # 예외 클래스의 이름만 추출
        
        # 예외 유형이 ElementNotInteractableException이면 N / A로 기록
        if type(e).__name__ == "ElementNotInteractableException":
            print("Sign up 모달창 노출: N / A")
            write_to_sheet("Register", "N / A", error_message)
        else:
            print("Sign up 모달창 노출: Fail")
            write_to_sheet("Register", "Fail", error_message)

    # TC5. 회원가입 모달창 내 Username 입력 확인
    try:
        username_field = driver.find_element(By.XPATH, '//*[@id="sign-username"]')
        username_field.send_keys(username)
        print("회원가입 모달창 내 Username 입력: Pass")
        write_to_sheet("Register", "Pass", username)
    except Exception as e:
        error_message = f"{type(e).__name__}"  # 예외 클래스의 이름만 추출
        
        # 예외 유형이 ElementNotInteractableException이면 N / A로 기록
        if type(e).__name__ == "ElementNotInteractableException":
            print("회원가입 모달창 내 Username 입력: N / A")
            write_to_sheet("Register", "N / A", error_message)
        else:
            print("회원가입 모달창 내 Username 입력: Fail")
            write_to_sheet("Register", "Fail", error_message)
        
    # TC6. 회원가입 모달창 내 Password 입력 확인    
    try:
        password_field = driver.find_element(By.XPATH, '//*[@id="sign-password"]')
        password_field.send_keys(password)
        print("회원가입 모달창 내 Password 입력: Pass")
        write_to_sheet("Register", "Pass", password)
    except Exception as e:
        error_message = f"{type(e).__name__}"  # 예외 클래스의 이름만 추출
        
        # 예외 유형이 ElementNotInteractableException이면 N / A로 기록
        if type(e).__name__ == "ElementNotInteractableException":
            print("회원가입 모달창 내 Password 입력: N / A")
            write_to_sheet("Register", "N / A", error_message)
        else:
            print("회원가입 모달창 내 Password 입력: Fail")
            write_to_sheet("Register", "Fail", error_message)

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
            write_to_sheet("Register", "Fail", alert_text)
            close_btn = driver.find_element(By.XPATH, '//*[@id="signInModal"]/div/div/div[3]/button[1]')
            ActionChains(driver).click(close_btn).perform()
        elif alert_text == "Please fill out Username and Password.":
            print("회원가입 모달창 내 Sign up 버튼 클릭: Fail")
            write_to_sheet("Register", "Fail", alert_text)
            close_btn = driver.find_element(By.XPATH, '//*[@id="signInModal"]/div/div/div[3]/button[1]')
            ActionChains(driver).click(close_btn).perform()
        else:
            print("회원가입 모달창 내 Sign up 버튼 클릭: Pass")
            write_to_sheet("Register", "Pass", alert_text)

    except Exception as e:
        error_message = f"{type(e).__name__}"  # 예외 클래스의 이름만 추출
        
        # 예외 유형이 ElementNotInteractableException이면 N / A로 기록
        if type(e).__name__ == "ElementNotInteractableException":
            print("회원가입 모달창 내 Sign up 버튼 클릭: N / A")
            write_to_sheet("Register", "N / A", error_message)
        else:
            print("회원가입 모달창 내 Sign up 버튼 클릭: Fail")
            write_to_sheet("Register", "Fail", error_message)


if __name__ == "__main__":
    username = input("Enter the username: ")
    password = input("Enter the password: ")
    driver = open_url("Register")
    register(username, password)
    input("Press Enter to quit the script and close the browser")
    print("******************************Register test completed.******************************")