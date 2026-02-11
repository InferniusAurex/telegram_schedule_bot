import requests

CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR_2xTOPVGwrQI9celR0ZLSEXsT8JK6IowezaBK3UU1NxUB4mM6f5C3gLHmtaFmDiVwQFzkHZAdlxdX/pub?gid=0&single=true&output=csv"

def get_holiday(date_str):
    """
    date_str format: YYYY-MM-DD
    returns reason or None
    """
    try:
        r = requests.get(CSV_URL, timeout=10)
        lines = r.text.splitlines()

        # skip header
        for line in lines[1:]:
            parts = line.split(",")
            if len(parts) >= 2:
                if parts[0].strip() == date_str:
                    return parts[1].strip()

    except Exception as e:
        print("Holiday fetch error:", e)

    return None
