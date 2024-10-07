from __common__ import *
from __openurl__ import open_url

def add_cart(i):
    global selected_items
    global available_items
    available_items = []

    driver.implicitly_wait(3) # 웹 페이지 요소 찾는 암시적 대기

    # TC14, 18, 22, 26. 제품 노출 확인
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="tbodyid"]')))
        print(f"{i+1}번째 제품 확인: Pass")
        write_to_sheet("AddCart", "Pass", "")
    except Exception as e:
        error_message = f"{type(e).__name__}"  # 예외 클래스의 이름만 추출
        
        # 예외 유형이 ElementNotInteractableException이면 N / A로 기록
        if type(e).__name__ == "ElementNotInteractableException":
            print("제품 노출: N / A")
            write_to_sheet("AddCart", "N / A", error_message)
        else:
            print("제품 노출: Fail")
            write_to_sheet("AddCart", "Fail", error_message)
 
    # tbodyid 중 하위 a 요소들 (ex.//*[@id="tbodyid"]/div[6]/div/div/h4/a)
    item_links = driver.find_elements(By.XPATH, '//*[@id="tbodyid"]//h4/a')

   # 선택된 제품 제외
    for item in item_links:
        item_name = item.text # a 태그 텍스트

        if item_name not in selected_items:
            available_items.append(item_name)
 
    if available_items:
        # 제품들 중 하나 랜덤 선택
        random_item = random.choice(available_items)

        # random_item의 WebElement 찾기
        item_element = driver.find_element(By.XPATH, f"//h4/a[contains(text(), '{random_item}')]")

        # 선택한 random_item으로 스크롤 이동
        driver.execute_script("arguments[0].scrollIntoView(true);", item_element)

        # TC15, 19, 23, 27. 해당 제품 설명 페이지 이동 확인
        try:
            driver.execute_script("arguments[0].click();", item_element)
            print(f"{i+1}번째 제품 설명 페이지 이동: Pass")
            write_to_sheet("AddCart", "Pass", random_item)

            # 선택된 제품 selected_items에 추가
            selected_items.append(random_item)
        except Exception as e:
            error_message = f"{type(e).__name__}"  # 예외 클래스의 이름만 추출
            print(f"{i+1}번째 제품 설명 페이지 이동: Fail")
            write_to_sheet("AddCart", "Fail", error_message)

    # TC16, 20, 24, 28. Add to cart 버튼 노출 확인
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tbodyid"]/div[2]/div/a')))
        print(f"{i+1}번째 제품 Add to cart 버튼 노출: Pass")
        write_to_sheet("AddCart", "Pass", "")
    except Exception as e:
        error_message = f"{type(e).__name__}"  # 예외 클래스의 이름만 추출
        
        # 예외 유형이 ElementNotInteractableException이면 N / A로 기록
        if type(e).__name__ == "ElementNotInteractableException":
            print(f"{i+1}번째 제품 Add to cart 버튼 노출: N / A")
            write_to_sheet("AddCart", "N / A", error_message)
        else:
            print(f"{i+1}번째 제품 Add to cart 버튼 노출: Fail")
            write_to_sheet("AddCart", "Fail", error_message)

    # TC17, 21, 25, 29. Add to cart 버튼 클릭 확인
    try:
        addcart_btn = driver.find_element(By.XPATH, '//*[@id="tbodyid"]/div[2]/div/a')
        driver.execute_script("arguments[0].click();", addcart_btn)
        print(f"{i+1}번째 제품 Add to cart 버튼 클릭: Pass")
        write_to_sheet("AddCart", "Pass", "")
    except Exception as e:
        error_message = f"{type(e).__name__}"  # 예외 클래스의 이름만 추출
        
        # 예외 유형이 ElementNotInteractableException이면 N / A로 기록
        if type(e).__name__ == "ElementNotInteractableException":
            print(f"{i+1}번째 제품 Add to cart 버튼 클릭: N / A")
            write_to_sheet("AddCart", "N / A", error_message)
        else:
            print(f"{i+1}번째 제품 Add to cart 버튼 클릭: Fail")
            write_to_sheet("AddCart", "Fail", error_message)

    # 장바구니 담기 시 alert 노출 확인
    WebDriverWait(driver, 10).until(EC.alert_is_present())

    # alert로 화면 전환
    alert = driver.switch_to.alert

    # alert 확인 버튼 클릭
    alert.accept()

    # 홈으로 이동
    home_btn = driver.find_element(By.XPATH, '//*[@id="nava"]')
    driver.execute_script("arguments[0].click();", home_btn)


if __name__ == '__main__':
    driver = open_url("AddCart")
    for i in range(4):
        add_cart(i)
        print(f"선택된 아이템: {selected_items}")

    input("Press Enter to quit the script and close the browser")
    print("******************************AddCart test completed.******************************")
