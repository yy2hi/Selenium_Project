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
        write_to_sheet("CheckCart", "Pass", "")
    except Exception as e:
        error_message = f"{type(e).__name__}"  # 예외 클래스의 이름만 추출
        
        # 예외 유형이 ElementNotInteractableException이면 N / A로 기록
        if type(e).__name__ == "ElementNotInteractableException":
            print("제품 노출: N / A")
            write_to_sheet("CheckCart", "N / A", error_message)
        else:
            print("제품 노출: Fail")
            write_to_sheet("CheckCart", "Fail", error_message)
 
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
            write_to_sheet("CheckCart", "Pass", random_item)

            # 선택된 제품 selected_items에 추가
            selected_items.append(random_item)
        except Exception as e:
            error_message = f"{type(e).__name__}"  # 예외 클래스의 이름만 추출
            print(f"{i+1}번째 제품 설명 페이지 이동: Fail")
            write_to_sheet("CheckCart", "Fail", error_message)

    # TC16, 20, 24, 28. Add to cart 버튼 노출 확인
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tbodyid"]/div[2]/div/a')))
        print(f"{i+1}번째 제품 Add to cart 버튼 노출: Pass")
        write_to_sheet("CheckCart", "Pass", "")
    except Exception as e:
        error_message = f"{type(e).__name__}"  # 예외 클래스의 이름만 추출
        
        # 예외 유형이 ElementNotInteractableException이면 N / A로 기록
        if type(e).__name__ == "ElementNotInteractableException":
            print(f"{i+1}번째 제품 Add to cart 버튼 노출: N / A")
            write_to_sheet("CheckCart", "N / A", error_message)
        else:
            print(f"{i+1}번째 제품 Add to cart 버튼 노출: Fail")
            write_to_sheet("CheckCart", "Fail", error_message)

    # TC17, 21, 25, 29. Add to cart 버튼 클릭 확인
    try:
        addcart_btn = driver.find_element(By.XPATH, '//*[@id="tbodyid"]/div[2]/div/a')
        driver.execute_script("arguments[0].click();", addcart_btn)
        print(f"{i+1}번째 제품 Add to cart 버튼 클릭: Pass")
        write_to_sheet("CheckCart", "Pass", "")
    except Exception as e:
        error_message = f"{type(e).__name__}"  # 예외 클래스의 이름만 추출
        
        # 예외 유형이 ElementNotInteractableException이면 N / A로 기록
        if type(e).__name__ == "ElementNotInteractableException":
            print(f"{i+1}번째 제품 Add to cart 버튼 클릭: N / A")
            write_to_sheet("CheckCart", "N / A", error_message)
        else:
            print(f"{i+1}번째 제품 Add to cart 버튼 클릭: Fail")
            write_to_sheet("CheckCart", "Fail", error_message)

    # 장바구니 담기 시 alert 노출 확인
    WebDriverWait(driver, 10).until(EC.alert_is_present())

    # alert로 화면 전환
    alert = driver.switch_to.alert

    # alert 확인 버튼 클릭
    alert.accept()

    # 홈으로 이동
    home_btn = driver.find_element(By.XPATH, '//*[@id="nava"]')
    driver.execute_script("arguments[0].click();", home_btn)

def check_cart():
    global selected_items

    # TC30. Cart 버튼 노출 확인
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="login2"]')))
        print("Cart 버튼 노출: Pass")
        write_to_sheet("CheckCart", "Pass", "")
    except Exception as e:
        error_message = f"{type(e).__name__}"  # 예외 클래스의 이름만 추출
        
        # 예외 유형이 ElementNotInteractableException이면 N / A로 기록
        if type(e).__name__ == "ElementNotInteractableException":
            print("Cart 버튼 노출: N / A")
            write_to_sheet("CheckCart", "N / A", error_message)
        else:
            print("Cart 버튼 노출: Fail")
            write_to_sheet("CheckCart", "Fail", error_message)

    # TC31. Cart 버튼 클릭 확인
    try:
        cart_btn = driver.find_element(By.XPATH, '//*[@id="navbarExample"]/ul/li[4]/a')
        driver.execute_script("arguments[0].click();", cart_btn)
        print("Cart 버튼 클릭: Pass")
        write_to_sheet("CheckCart", "Pass", "")
    except Exception as e:
        error_message = f"{type(e).__name__}"  # 예외 클래스의 이름만 추출
        
        # 예외 유형이 ElementNotInteractableException이면 N / A로 기록
        if type(e).__name__ == "ElementNotInteractableException":
            print("Cart 버튼 클릭: N / A")
            write_to_sheet("CheckCart", "N / A", error_message)
        else:
            print("Cart 버튼 클릭: Fail")
            write_to_sheet("CheckCart", "Fail", error_message)

    # TC32. Cart 페이지에 정상적으로 제품 저장 확인
    try:
        # 페이지 끝 높이
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        # 추출한 제품명을 저장할 리스트
        cart_item_names = []

        while True:
            # 페이지 끝까지 스크롤
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            time.sleep(1)  # 스크롤 후 대기
            
            # 새로운 페이지 높이 가져오기
            new_height = driver.execute_script("return document.body.scrollHeight")
            
            # 더 이상 스크롤이 없을 경우 종료
            if new_height == last_height:
                time.sleep(1)
                new_height = driver.execute_script("return document.body.scrollHeight")
                            
                # 현재까지 로드된 제품 추출
                cart_items = driver.find_elements(By.XPATH, '//*[@id="tbodyid"]/tr/td[2]')       

                # 현재까지 로드된 제품 이름 저장
                for item in cart_items:
                    item_name = item.text
                    cart_item_names.append(item_name)

                if new_height == last_height:
                    break
            last_height = new_height

        # 제품 추출 후 selected_items와 비교해 제품 없는경우 missing_items에 추가
        missing_items = []
        for item in selected_items:
            if item not in cart_item_names:
                missing_items.append(item)

        if not missing_items:
            # 모든 제품이 정상적으로 장바구니에 담겨있는 경우
            print("Cart 페이지에 정상적으로 모든 제품 저장: Pass")
            write_to_sheet("CheckCart", "Pass", f"이번 장바구니에 담은 제품: {selected_items}")
        else:
            # selected_items 중 장바구니에 누락된 제품이 있는 경우
            print(f"Cart 내 누락된 제품 {missing_items}: Fail")
            write_to_sheet("CheckCart", "Fail", f"누락된 제품: {missing_items}")

    except Exception as e:
        error_message = f"{type(e).__name__}"  # 예외 클래스의 이름만 추출
        if type(e).__name__ == "ElementNotInteractableException":
            print("Cart 페이지에 정상적으로 제품 저장: N / A")
            write_to_sheet("CheckCart", "N / A", error_message)
        else:
            print("Cart 페이지에 정상적으로 제품 저장: Fail")
            write_to_sheet("CheckCart", "Fail", error_message)

def delete_item():
    # TC33. 장바구니 내 제품 삭제 버튼 노출 확인
    try:
        delete_buttons = driver.find_elements(By.XPATH, "//*[@id='tbodyid']//a")
        print("Delete 버튼 노출: Pass")
        write_to_sheet("CheckCart", "Pass", "")
    except Exception as e:
        error_message = f"{type(e).__name__}"  # 예외 클래스의 이름만 추출
        # 예외 유형이 ElementNotInteractableException이면 N / A로 기록
        if type(e).__name__ == "ElementNotInteractableException":
            print("Delete 버튼 노출: N / A")
            write_to_sheet("CheckCart", "N / A", error_message)
        else:
            print("Delete 버튼 노출: Fail")
            write_to_sheet("CheckCart", "Fail", error_message)

    if delete_buttons:
        # delete_buttons 중 하나 랜덤 선택
        random_delete = random.choice(delete_buttons)

        try:
            # 상위 요소로부터 제품 이름이 들어있는 <td> 찾기
            item_name_xpath = "./ancestor::tr/td[2]"
            delete_item = random_delete.find_element(By.XPATH, item_name_xpath).text  # random_delete 할 제품 이름 추출

            # TC34. 장바구니 내 제품 삭제 가능 확인
            try:
                driver.execute_script("arguments[0].click();", random_delete)
                print(f"삭제된 제품 {delete_item}: Pass ")
                write_to_sheet("CheckCart", "Pass", delete_item)
            except Exception as e:
                error_message = f"{type(e).__name__}"
                if type(e).__name__ == "ElementNotInteractableException":
                    print("장바구니 내 제품 삭제: N / A")
                    write_to_sheet("CheckCart", "N / A", error_message)
                else:
                    print("장바구니 내 제품 삭제: Fail")
                    write_to_sheet("CheckCart", "Fail", error_message)
        except Exception as e:
            print("장바구니 내 제품 이름 미노출:", str(e))

if __name__ == "__main__":
    driver = open_url("CheckCart")
    for i in range(4):
        add_cart(i)
        print(f"선택된 아이템: {selected_items}")
    check_cart()
    delete_item()
    input("Press Enter to quit the script and close the browser")
    print("******************************CheckCart test completed.******************************")