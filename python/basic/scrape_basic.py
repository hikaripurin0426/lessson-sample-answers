"""
BeautifulSoupを使ったbasicページのスクレイピング例
このスクリプトは練習用サイトの基本ページから様々な要素を抽出します。
"""

import requests
from bs4 import BeautifulSoup

URL = "https://scraping-practice-six.vercel.app/basic"

def get_soup():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    response = requests.get(URL, headers=headers)
    response.raise_for_status()
    return BeautifulSoup(response.content, 'html.parser')

def scrape_main_title(soup):
    print("1. メインタイトル:")
    main_title = soup.find('h1', id='main-title')
    if main_title:
        print(f"   {main_title.get_text(strip=True)}")
    print()

def scrape_headings(soup):
    print("2. 見出し要素 (h1-h6):")
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    for heading in headings:
        print(f"   {heading.name}: {heading.get_text(strip=True)}")
    print()

def scrape_paragraphs(soup):
    print("3. 段落要素:")
    paragraphs = soup.find_all('p')
    for i, p in enumerate(paragraphs):
        text = p.get_text(strip=True)
        if len(text) > 50:
            text = text[:50] + "..."
        print(f"   段落{i}: {text}")
    print()

def scrape_links(soup):
    print("4. リンク要素:")
    links = soup.find_all('a')
    for i, link in enumerate(links, 1):
        href = link.get('href', 'なし')
        text = link.get_text(strip=True)
        print(f"   リンク{i}: {text} -> {href}")
    print()

def scrape_images(soup):
    print("5. 画像要素:")
    images = soup.find_all('img')
    for i, img in enumerate(images, 1):
        src = img.get('src', 'なし')
        alt = img.get('alt', 'なし')
        print(f"   画像{i}: src={src}, alt={alt}")
    print()

def scrape_sections(soup):
    print("6. セクション別情報:")
    sections = soup.find_all('section')
    for i, section in enumerate(sections, 1):
        section_title = section.find('h2')
        if section_title:
            title_text = section_title.get_text(strip=True)
            print(f"   セクション{i}: {title_text}")
    print()

def scrape_white_sections(soup):
    print("7. 特定のクラス要素:")
    white_sections = soup.find_all(class_='bg-white')
    print(f"   'bg-white'クラスの要素数: {len(white_sections)}")
    print()

def scrape_decorative(soup):
    print("9. テキスト装飾要素:")
    decorative_tags = ['strong', 'em', 'u', 's', 'mark', 'sup', 'sub', 'code']
    for tag in decorative_tags:
        elements = soup.find_all(tag)
        if elements:
            print(f"   {tag}: {len(elements)}個")
            for element in elements:
                print(f"     - {element.get_text(strip=True)}")
    print()


def main():
    
    menu = [
        ("メインタイトル", scrape_main_title),
        ("見出し要素 (h1-h6)", scrape_headings),
        ("段落要素", scrape_paragraphs),
        ("リンク要素", scrape_links),
        ("画像要素", scrape_images),
        ("セクション別情報", scrape_sections),
        ("特定のクラス要素", scrape_white_sections),
        ("テキスト装飾要素", scrape_decorative),
    ]
    print("BeautifulSoupスクレイピング練習")
    print("対象: 基本ページ (/basic)")
    print("=" * 50)
    for i, (name, _) in enumerate(menu, 1):
        print(f"{i}. {name}")
    print("0. 終了")
    print("=" * 50)
    soup = get_soup()
    while True:
        try:
            choice = int(input("実行したい番号を選んでください: "))
        except ValueError:
            print("数字を入力してください")
            continue
        if choice == 0:
            print("終了します。")
            break
        elif 1 <= choice <= len(menu):
            print("=" * 50)
            menu[choice - 1][1](soup)
        else:
            print("有効な番号を選んでください")

if __name__ == "__main__":
    main()
