# google_sheets_writer.py
import os
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

# Google Sheets API에 접근하기 위한 클래스
class GoogleSheetsWriter:
    def __init__(self, spreadsheet_id, service_account_file, scopes=None, base_row=7):
        if scopes is None:
            scopes = ['https://www.googleapis.com/auth/spreadsheets']
        
        # 서비스 계정 파일로 인증
        creds = Credentials.from_service_account_file(service_account_file, scopes=scopes)
        self.service = build('sheets', 'v4', credentials=creds)
        self.spreadsheet_id = spreadsheet_id
        self.sheet = self.service.spreadsheets()
        self.result_row = base_row  # 결과를 기록할 시작 행 번호
    
    # 결과를 Google Sheets에 기록하는 함수
    def write_to_sheet(self, result):
        body = {
            'values': [[result]]  # 기록할 값 (Pass 또는 Fail)
        }
        # I열에 결과 기록 (행 번호는 result_row에서 시작)
        self.sheet.values().update(
            spreadsheetId=self.spreadsheet_id, 
            range=f'I{self.result_row}:I{self.result_row}',
            valueInputOption='RAW',
            body=body
        ).execute()
        self.result_row += 1  # 다음 결과는 다음 행에 기록
