import sys
from datetime import datetime

for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith("subject_id"):
        continue
    
    parts = line.split(",")
    if len(parts) < 4:
        continue

    dob = parts[2].strip()
    dod = parts[3].strip()

    if not dob:
        continue

    try:
        dob_dt = datetime.strptime(dob, "%Y-%m-%d %H:%M:%S")
        death_or_today = datetime.strptime(dod, "%Y-%m-%d %H:%M:%S") if dod else datetime(2010, 1, 1)
        age = (death_or_today - dob_dt).days / 365.25
        if 0 <= age <= 120:
            print(f"age\t{age}")
    except:
        continue