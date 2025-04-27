import requests
from bs4 import BeautifulSoup

def scrape_page(url):
    # 發送 GET 請求
    response = requests.get(url)
    response.raise_for_status()  # 如果請求失敗會拋出錯誤

    # 用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # 抓取主要內容，這裡我們把所有文字都取出
    # 你也可以根據網頁結構細分特定區域
    text = soup.get_text(separator='\n')

    return text
if __name__ == "__main__":
    # 這邊可以自行貼上想要爬的網址
    url = "https://docs.streamlit.io/develop/concepts/architecture/caching"
    scraped_text = scrape_page(url)

    # 把結果存成 txt 檔案
    save_path = "/Users/migu/Desktop/資料庫/gen_ai_try/ai_metadata/streamlit/scraped_page.txt"
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(scraped_text)

    print(f"爬取完成！內容已儲存在 {save_path}")
