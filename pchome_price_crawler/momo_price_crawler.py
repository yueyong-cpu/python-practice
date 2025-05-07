# momo_price_crawler.py
import requests
from bs4 import BeautifulSoup
import pandas as pd

def crawl_momo(keyword, max_results=10):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }

    url = f"https://www.momoshop.com.tw/search/searchShop.jsp?keyword={keyword}"
    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')

    titles = [tag.text.strip() for tag in soup.select('.prdName')][:max_results]
    prices = [tag.text.strip().replace(',', '') for tag in soup.select('.price')][:max_results]
    links = ["https://www.momoshop.com.tw" + tag['href'] for tag in soup.select('.prdName > a')][:max_results]

    data = pd.DataFrame({
        '商品名稱': titles,
        '價格': prices,
        '連結': links
    })
    return data

if __name__ == "__main__":
    keyword = input("請輸入搜尋商品關鍵字：")
    result = crawl_momo(keyword)
    print("\n🔍 搜尋結果：")
    print(result)
    result.to_excel(f"{keyword}_比價結果.xlsx", index=False)
    print(f"\n✅ 已輸出報表：{keyword}_比價結果.xlsx")
