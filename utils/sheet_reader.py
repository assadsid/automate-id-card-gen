import gspread
from oauth2client.service_account import ServiceAccountCredentials

def fetch_employee_data(sheet_name, worksheet_name):
    try:
        # Recommended modern scope list
        scope = [
            "https://www.googleapis.com/auth/spreadsheets.readonly",
            "https://www.googleapis.com/auth/drive.readonly"
        ]

        creds = ServiceAccountCredentials.from_json_keyfile_name(
            "creds/google_service_account.json", scope
        )
        client = gspread.authorize(creds)

        # 🔍 Check available spreadsheet titles
        spreadsheets = [s.title for s in client.openall()]
        if sheet_name not in spreadsheets:
            raise ValueError(f"❌ Spreadsheet '{sheet_name}' not found. Available: {spreadsheets}")

        sheet = client.open(sheet_name)
        worksheet = sheet.worksheet(worksheet_name)

        data = worksheet.get_all_records()
        return data

    except Exception as e:
        print(f"🚨 Error fetching data from Google Sheet: {e}")
        return []
