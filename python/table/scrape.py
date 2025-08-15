import requests
from bs4 import BeautifulSoup
import csv

URL = "https://scraping-practice-six.vercel.app/table"

def get_soup():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    response = requests.get(URL, headers=headers)
    response.raise_for_status()
    return BeautifulSoup(response.content, 'html.parser')

def scrape_product_table(soup):
    print("■ 商品テーブル")
    table = soup.find('table', id='product-table')
    rows = table.find_all('tr')[1:]  # ヘッダー除く
    for row in rows:
        cells = row.find_all('td')
        data = [cell.get_text(strip=True) for cell in cells]
        print(data)

def scrape_sales_table(soup):
    print("\n■ 売上テーブル")
    table = soup.find('table', id='sales-table')
    rows = table.find_all('tr')[1:]  # ヘッダー除く
    for row in rows:
        cells = row.find_all('td')
        data = [cell.get_text(strip=True) for cell in cells]
        print(data)

def scrape_employee_table(soup):
    print("\n■ 従業員テーブル")
    table = soup.find('table', id='employee-table')
    rows = table.find_all('tr')[1:]  # ヘッダー除く
    for row in rows:
        cells = row.find_all(['td', 'th'])
        data = [cell.get_text(strip=True) for cell in cells]
        print(data)

def scrape_price_comparison(soup):
    print("\n■ 価格比較（divテーブル形式）")
    table = soup.find('div', class_='price-comparison-table')
    rows = table.find_all('div', class_='table-row')
    for row in rows:
        cols = row.find_all('div')
        data = [col.get_text(strip=True) for col in cols]
        print(data)

def scrape_product_name_price_to_csv(soup, filename="product_name_price.csv"):
    """商品テーブルから商品名と価格を抽出してCSVに保存する"""
    table = soup.find('table', id='product-table')
    if not table:
        print("商品テーブルが見つかりません")
        return
    rows = table.find_all('tr')[1:]  # ヘッダー除く
    data_list = []
    for row in rows:
        name_cell = row.find('td', class_='product-name')
        price_cell = row.find('td', class_='price')
        if name_cell and price_cell:
            name = name_cell.get_text(strip=True)
            price = price_cell.get_text(strip=True)
            data_list.append([name, price])
    if not data_list:
        print("商品名と価格のデータが見つかりませんでした")
        return
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["商品名", "価格"])
            writer.writerows(data_list)
        print(f"商品名と価格をCSVに保存しました: {filename}")
    except Exception as e:
        print(f"CSV保存に失敗しました: {e}")

def main():
    soup = get_soup()
    scrape_product_table(soup)
    scrape_sales_table(soup)
    scrape_employee_table(soup)
    scrape_price_comparison(soup)
    scrape_product_name_price_to_csv(soup)

if __name__ == "__main__":
    main()

