# test_fetch_data.py

from utils.sheet_reader import fetch_employee_data

# 🔄 Yeh dono values aap apni sheet ke mutabiq update karein
sheet_name = "EmployeeData"         # 👈 Google Sheet ka exact title
worksheet_name = "Sheet1"           # 👈 Tab ka name (usually "Sheet1")

data = fetch_employee_data(sheet_name, worksheet_name)

if not data:
    print("⚠️ No data found or sheet access failed.")
else:
    print(f"✅ Total rows fetched: {len(data)}")
    print("🔍 Sample row:")
    print(data[-1])  # Show last employee
