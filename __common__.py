import random
import json
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

def create_driver():
    ## webdriver 생성
    chrome_options = webdriver.ChromeOptions() 
    chrome_options.add_experimental_option("detach", True) # 브라우저 자동 종료 방지
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options) # ChromeDriver 자동 설치, detach 모드로 ChromeDriver 실행
    return driver

# 설정 파일 read
def load_config(config_path='config.json'):
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# 설정 로드
config = load_config()

## Google Sheets API 인증 및 스프레드시트 접근 설정
SPREADSHEET_ID = config["SPREADSHEET_ID"]  # 구글 스프레드시트 ID (config 설정 파일)
result_row = config["START_ROW"]  # 테스트 결과 기록 시작 행 번호 (config 설정 파일)

## 구글 서비스 계정 키 파일 경로
current_dir = os.getcwd() # 현재 경로
SERVICE_ACCOUNT_FILE = os.path.join(current_dir, config["SERVICE_ACCOUNT_FILE"])

## 구글 스프레드시트 API 사용 인증 설정
SCOPES = config["SCOPES"] # 읽기 및 쓰기 권한 (config 설정 파일)
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES) # Google Cloud 서비스 계정 인증
service = build('sheets', 'v4', credentials=creds) # Google Sheets API 클라이언트 생성
sheet = service.spreadsheets() 

## 스프레드시트에 테스트 결과 기록 함수
def write_to_sheet(sheet_name, result, note=None):
    global result_row
    body = {
        'values': [[result, note]]  # 테스트 결과 (Pass or Fail or N / A) 및 메시지 기록
    }
    # 스프레드시트의 I열에 테스트 결과, J열에 메시지 기록
    sheet.values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=f'{sheet_name}!H{result_row}:I{result_row}',
        valueInputOption='RAW',
        body=body
    ).execute()
    result_row += 1  # 다음 결과는 다음 행에 기록