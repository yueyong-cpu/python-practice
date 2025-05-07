# pchome_price_crawler.py
import requests
import urllib.parse
import pandas as pd

def crawl_pchome(keyword, max_results=20):
    encoded_keyword = urllib.parse.quote(keyword)
    url = f"https://ecshweb.pchome.com.tw/search/v3.3/all/results?q={encoded_keyword}&page=1&sort=rnk/dc"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }

    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        print("❌ 無法連線到 PChome")
        return pd.DataFrame()

    data = res.json()
    if 'prods' not in data:
        print("❗ 找不到商品資料，可能關鍵字太模糊或被擋爬")
        return pd.DataFrame()

    titles = []
    prices = []
    urls = []

    for item in data['prods'][:max_results]:
        titles.append(item['name'])
        prices.append(item['price'])
        urls.append(f"https://24h.pchome.com.tw/prod/{item['Id']}")

    df = pd.DataFrame({
        "商品名稱": titles,
        "價格": prices,
        "連結": urls
    })
    return df

if __name__ == "__main__":
    keyword = input("請輸入搜尋商品關鍵字（例如 羅技 鍵盤）：")
    result = crawl_pchome(keyword)
    if not result.empty:
        print("\n🔍 搜尋結果：")
        print(result)
        result.to_excel(f"{keyword}_pchome比價.xlsx", index=False)
        print(f"\n✅ 已輸出報表：{keyword}_pchome比價.xlsx")
