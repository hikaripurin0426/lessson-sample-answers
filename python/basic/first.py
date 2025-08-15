import requests
from bs4 import BeautifulSoup

URL = "https://scraping-practice-six.vercel.app/basic"

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
response = requests.get(URL, headers=headers)

# BeautifulSoupオブジェクトを作成してsoup変数に格納
soup = BeautifulSoup(response.content, 'html.parser')
# メインタイトルを抽出
# 今回はタグ＋IDで取得
main_title = soup.find('h1', id='main-title')
# main_titleの中身を確認
print(main_title)
# メインタイトルのテキストのみ取得
main_title_text = main_title.get_text(strip=True)
# メインタイトルのテキストを表示
print(f"メインタイトル: {main_title_text}")