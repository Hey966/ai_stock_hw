import time
from scan_market import classify_market

while True:
    print("開始掃市場...")
    classify_market()
    print("休息10分鐘...")
    time.sleep(600)  # 10分鐘