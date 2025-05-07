# momo_selenium_crawler.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import urllib.parse
import os

# 修改這個路徑成你自己的 chromedriver.exe 路徑
CHROMEDRIVER_PATH = r"D:\\Tools\\chromedriver\\chromedriver-win64\\chromedriver.exe"

def crawl_momo(keyword, max_results=10):
    keyword_encoded = urllib.parse.quote(keyword)
    url = f"https://www.momoshop.com.tw/search/searchShop.jsp?keyword={keyword_encoded}"

    # 建議先開啟瀏覽器畫面觀察效果
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # 預設註解掉
    chrome_options.add_argument("--disable-gpu")

    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)

    # 等待商品元素出現（最多等 10 秒）
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".listArea .goodsUrl"))
    )

    # 捲動頁面觸發資料載入
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    items = driver.find_elements(By.CSS_SELECTOR, ".listArea .goodsUrl")[:max_results]

    titles, prices, links = [], [], []
    for item in items:
        try:
            title = item.find_element(By.CSS_SELECTOR, ".prdName").text
            link = item.get_attribute("data-link")

            price_tag = item.find_element(By.CSS_SELECTOR, ".price")
            price = price_tag.text.replace(",", "")

            titles.append(title)
            prices.append(price)
            links.append(link)
        except Exception as e:
            print("⚠️ 抓取單一商品失敗：", e)
            continue

    driver.quit()

    df = pd.DataFrame({
        "商品名稱": titles,
        "價格": prices,
        "連結": links
    })
    return df

if __name__ == "__main__":
    keyword = input("請輸入 momo 搜尋關鍵字：")
    df = crawl_momo(keyword)
    if not df.empty:
        filename = f"{keyword}_momo比價.xlsx"
        df.to_excel(filename, index=False)
        print(f"✅ 已完成抓取並輸出報表：{filename}")
    else:
        print("❌ 沒有找到任何商品，可能是關鍵字太模糊或網頁結構改變。")
