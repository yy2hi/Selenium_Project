from __common__ import *


## 테스트 할 페이지 오픈 및 최대화
def open_url(sheet_name):
    driver = create_driver()
    # TC1. 테스트 페이지 접근 확인
    try:
        test_url = "https://www.demoblaze.com/index.html"
        driver.get(test_url)
        driver.maximize_window()
        print("테스트 페이지 오픈: Pass")
        write_to_sheet(sheet_name, "Pass", "")
    except Exception as e:
        error_message = f"{type(e).__name__}"  # 예외 클래스의 이름만 추출

        # 예외 유형이 ElementNotInteractableException이면 N / A
        if type(e).__name__ == "ElementNotInteractableException":
            print("테스트 페이지 오픈: N / A")
            write_to_sheet(sheet_name, "N / A", error_message)
        else:
            print("테스트 페이지 오픈: Fail")
            write_to_sheet(sheet_name, "Fail", error_message)

    return driver

if __name__ == '__main__':
    open_url("Login")