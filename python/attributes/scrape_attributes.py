#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
【初心者向け】HTML属性のスクレイピング練習
このスクリプトは属性ページから様々なHTML属性を抽出します。

学習ポイント:
- get()メソッドで属性値を取得
- data属性の抽出
- 複数の属性を持つ要素の処理
"""

import requests
from bs4 import BeautifulSoup

# スクレイピング対象のURL
URL = "https://scraping-practice-six.vercel.app/attributes"

def get_soup():
    """Webページを取得してBeautifulSoupオブジェクトを返す"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    print("📡 Webページを取得中...")
    response = requests.get(URL, headers=headers)
    response.raise_for_status()  # エラーがあれば例外を発生
    print("✓ ページ取得成功")
    return BeautifulSoup(response.content, 'html.parser')

def scrape_basic_attributes(soup):
    """基本的なHTML属性を抽出する"""
    print("1. 基本的なHTML属性")
    print("-" * 30)
    
    # id属性を持つ要素を検索
    elements_with_id = soup.find_all(attrs={'id': True})
    print(f"id属性を持つ要素: {len(elements_with_id)}個")
    for element in elements_with_id[:5]:  # 最初の5個だけ表示
        print(f"  - {element.name}タグ: id='{element.get('id')}'")
    
    # class属性を持つ要素を検索
    elements_with_class = soup.find_all(attrs={'class': True})
    print(f"\nclass属性を持つ要素: {len(elements_with_class)}個")
    for element in elements_with_class[:5]:  # 最初の5個だけ表示
        classes = element.get('class', [])
        print(f"  - {element.name}タグ: class='{' '.join(classes)}'")
    print()

def scrape_link_attributes(soup):
    """リンク要素の属性を詳しく抽出する"""
    print("2. リンク要素の属性")
    print("-" * 30)
    
    links = soup.find_all('a')
    for i, link in enumerate(links, 1):
        href = link.get('href', 'なし')
        target = link.get('target', 'なし')
        title = link.get('title', 'なし')
        text = link.get_text(strip=True)
        
        print(f"リンク{i}:")
        print(f"  テキスト: {text}")
        print(f"  href: {href}")
        print(f"  target: {target}")
        print(f"  title: {title}")
        print()

def scrape_image_attributes(soup):
    """画像要素の属性を詳しく抽出する"""
    print("3. 画像要素の属性")
    print("-" * 30)
    
    images = soup.find_all('img')
    for i, img in enumerate(images, 1):
        src = img.get('src', 'なし')
        alt = img.get('alt', 'なし')
        width = img.get('width', 'なし')
        height = img.get('height', 'なし')
        class_names = img.get('class', [])
        
        print(f"画像{i}:")
        print(f"  src: {src}")
        print(f"  alt: {alt}")
        print(f"  width: {width}")
        print(f"  height: {height}")
        print(f"  class: {' '.join(class_names) if class_names else 'なし'}")
        print()

def scrape_data_attributes(soup):
    """data属性を抽出する"""
    print("4. data属性の抽出")
    print("-" * 30)
    
    # data属性を持つ要素を検索
    all_elements = soup.find_all()
    data_elements = []
    
    for element in all_elements:
        # 全ての属性をチェックしてdata-で始まるものを探す
        data_attrs = {k: v for k, v in element.attrs.items() if k.startswith('data-')}
        if data_attrs:
            data_elements.append((element, data_attrs))
    
    print(f"data属性を持つ要素: {len(data_elements)}個")
    for element, data_attrs in data_elements[:10]:  # 最初の10個だけ表示
        print(f"  {element.name}タグ:")
        for attr_name, attr_value in data_attrs.items():
            print(f"    {attr_name}: {attr_value}")
        print()

def scrape_form_attributes(soup):
    """フォーム要素の属性を抽出する"""
    print("5. フォーム要素の属性")
    print("-" * 30)
    
    # input要素の属性を取得
    inputs = soup.find_all('input')
    for i, input_elem in enumerate(inputs, 1):
        input_type = input_elem.get('type', 'なし')
        name = input_elem.get('name', 'なし')
        placeholder = input_elem.get('placeholder', 'なし')
        required = input_elem.get('required', 'なし')
        
        print(f"入力フィールド{i}:")
        print(f"  type: {input_type}")
        print(f"  name: {name}")
        print(f"  placeholder: {placeholder}")
        print(f"  required: {required}")
        print()

def scrape_style_attributes(soup):
    """style属性とその他の装飾属性を抽出する"""
    print("6. style属性とその他の装飾属性")
    print("-" * 30)
    
    # style属性を持つ要素を検索
    styled_elements = soup.find_all(attrs={'style': True})
    print(f"style属性を持つ要素: {len(styled_elements)}個")
    
    for i, element in enumerate(styled_elements[:5], 1):
        style = element.get('style', '')
        print(f"要素{i} ({element.name}タグ):")
        print(f"  style: {style}")
        print()

def main():
    """メイン関数 - メニュー形式で実行する機能を選択"""
    menu = [
        ("基本的なHTML属性", scrape_basic_attributes),
        ("リンク要素の属性", scrape_link_attributes),
        ("画像要素の属性", scrape_image_attributes),
        ("data属性の抽出", scrape_data_attributes),
        ("フォーム要素の属性", scrape_form_attributes),
        ("style属性とその他の装飾属性", scrape_style_attributes),
    ]
    
    print("🔍 HTML属性スクレイピング練習")
    print("対象: 属性ページ (/attributes)")
    print("=" * 50)
    
    for i, (name, _) in enumerate(menu, 1):
        print(f"{i}. {name}")
    print("0. 終了")
    print("=" * 50)
    
    # 一度だけWebページを取得
    soup = get_soup()
    
    while True:
        try:
            choice = int(input("\n実行したい番号を選んでください: "))
        except ValueError:
            print("❌ 数字を入力してください")
            continue
        except Exception as e:
            print(f"❌ 予期しないエラーが発生しました: {e}")
            continue
        
        if choice == 0:
            print("👋 プログラムを終了します。")
            break
        elif 1 <= choice <= len(menu):
            print("\n" + "=" * 50)
            menu[choice - 1][1](soup)
        else:
            print("❌ 有効な番号を選んでください")

if __name__ == "__main__":
    main()
