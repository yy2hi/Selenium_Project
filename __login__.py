from __common__ import *
from __openurl__ import open_url

def login(username, password):
    # TC8. Log in GNB 노출 확인
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="login2"]')))
        print("Log in GNB 노출: Pass")
        write_to_sheet("Login", "Pass", "")
    except Exception as e:
        error_message = f"{type(e).__name__}"  # 예외 클래스의 이름만 추출
        
        # 예외 유형이 ElementNotInteractableException이면 N / A로 기록
        if type(e).__name__ == "ElementNotInteractableException":
            print("Log in GNB 노출: N / A")
            write_to_sheet("Login", "N / A", error_message)
        else:
            print("Log in GNB 노출: Fail")
            write_to_sheet("Login", "Fail", error_message)    

    # TC9. Log in GNB 클릭 확인
    try:
        login_btn = driver.find_element(By.XPATH, '//*[@id="login2"]')
        driver.execute_script("arguments[0].click();", login_btn)
        print("Log in GNB 클릭 확인: Pass")
        write_to_sheet("Login", "Pass", "")
    except Exception as e:
        error_message = f"{type(e).__name__}"  # 예외 클래스의 이름만 추출
        
        # 예외 유형이 ElementNotInteractableException이면 N / A로 기록
        if type(e).__name__ == "ElementNotInteractableException":
            print("Log in GNB 클릭 확인: N / A")
            write_to_sheet("Login", "N / A", error_message)
        else:
            print("Log in GNB 클릭 확인: Fail")
            write_to_sheet("Login", "Fail", error_message)

    # TC10. Log in 모달창 노출 확인
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="logInModal"]/div/div')))
        print("Log in 모달창 노출: Pass")
        write_to_sheet("Login", "Pass", "")
    except Exception as e:
        error_message = f"{type(e).__name__}"  # 예외 클래스의 이름만 추출
        
        # 예외 유형이 ElementNotInteractableException이면 N / A로 기록
        if type(e).__name__ == "ElementNotInteractableException":
            print("Log in 모달창 노출: N / A")
            write_to_sheet("Login", "N / A", error_message)
        else:
            print("Log in 모달창 노출: Fail")
            write_to_sheet("Login", "Fail", error_message)

    # TC11. Log in 모달창 내 Username 입력 확인
    try:
        username_field = driver.find_element(By.XPATH, '//*[@id="loginusername"]')
        username_field.send_keys(username)
        print("Log in 모달창 내 Username 입력: Pass")
        write_to_sheet("Login", "Pass", username)
    except Exception as e:
        error_message = f"{type(e).__name__}"  # 예외 클래스의 이름만 추출
        
        # 예외 유형이 ElementNotInteractableException이면 N / A로 기록
        if type(e).__name__ == "ElementNotInteractableException":
            print("Log in 모달창 내 Username 입력: N / A")
            write_to_sheet("Login", "N / A", error_message)
        else:
            print("Log in 모달창 내 Username 입력: Fail")
            write_to_sheet("Login", "Fail", error_message)

    # TC12. 로그인 모달창 내 Password 입력 확인
    try:
        password_field = driver.find_element(By.XPATH, '//*[@id="loginpassword"]')
        password_field.send_keys(password)
        print("로그인 모달창 내 Password 입력: Pass")
        write_to_sheet("Login", "Pass", password)
    except Exception as e:
        error_message = f"{type(e).__name__}"  # 예외 클래스의 이름만 추출
        
        # 예외 유형이 ElementNotInteractableException이면 N / A로 기록
        if type(e).__name__ == "ElementNotInteractableException":
            print("로그인 모달창 내 Password 입력: N / A")
            write_to_sheet("Login", "N / A", error_message)
        else:
            print("로그인 모달창 내 Password 입력: Fail")
            write_to_sheet("Login", "Fail", error_message)

    # TC13. 로그인 성공 여부 확인
    try:
        # 로그인 성공 여부
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
                print("로그인 성공 여부: Fail")
                write_to_sheet("Login", "Fail", alert_text)
                close_btn = driver.find_element(By.XPATH, '//*[@id="logInModal"]/div/div/div[3]/button[1]')
                ActionChains(driver).click(close_btn).perform()
            elif alert_text == "Wrong password.":
                print("로그인 성공 여부: Fail")
                write_to_sheet("Login", "Fail", alert_text)
                close_btn = driver.find_element(By.XPATH, '//*[@id="logInModal"]/div/div/div[3]/button[1]')
                ActionChains(driver).click(close_btn).perform()
            elif alert_text == "Please fill out Username and Password.":
                print("로그인 성공 여부: Fail")
                write_to_sheet("Login", "Fail", alert_text)
                close_btn = driver.find_element(By.XPATH, '//*[@id="logInModal"]/div/div/div[3]/button[1]')
                ActionChains(driver).click(close_btn).perform()
        
        except TimeoutException:
            # alert가 뜨지 않으면 로그인 성공으로 처리
            print("로그인 성공 여부: Pass")
            write_to_sheet("Login", "Pass", "")

    except Exception as e:
        error_message = f"{type(e).__name__}"  # 예외 클래스의 이름만 추출
        
        # 예외 유형이 ElementNotInteractableException이면 N / A로 기록
        if type(e).__name__ == "ElementNotInteractableException":
            print("로그인 성공 여부: N / A")
            write_to_sheet("Login", "N / A", error_message)
        else:
            print("로그인 성공 여부: Fail")
            write_to_sheet("Login", "Fail", error_message)

if __name__ == '__main__':
    username = input("Enter the username: ")
    password = input("Enter the password: ")
    driver = open_url("Login")
    login(username, password)
    input("Press Enter to quit the script and close the browser")
    print("******************************Login test completed.******************************")