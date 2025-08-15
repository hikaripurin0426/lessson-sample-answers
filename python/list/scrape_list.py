#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
【初心者向け】リスト要素のスクレイピング練習
このスクリプトはリストページから様々なリスト要素を抽出します。

学習ポイント:
- ul (順序なしリスト) の取得
- ol (順序ありリスト) の取得
- li (リスト項目) の取得
- ネストしたリストの処理
"""

import requests
from bs4 import BeautifulSoup

# スクレイピング対象のURL
URL = "https://scraping-practice-six.vercel.app/list"

def get_soup():
    """Webページを取得してBeautifulSoupオブジェクトを返す"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    print("📡 Webページを取得中...")
    response = requests.get(URL, headers=headers)
    response.raise_for_status()
    print("✓ ページ取得成功")
    return BeautifulSoup(response.content, 'html.parser')

def scrape_unordered_lists(soup):
    """順序なしリスト (ul) を取得"""
    print("1. 順序なしリスト (ul) の取得")
    print("-" * 30)
    
    ul_lists = soup.find_all('ul')
    print(f"ul要素数: {len(ul_lists)}個")
    
    for i, ul in enumerate(ul_lists, 1):
        ul_id = ul.get('id', 'なし')
        ul_class = ' '.join(ul.get('class', []))
        
        print(f"\nリスト{i}:")
        print(f"  id: {ul_id}")
        print(f"  class: {ul_class if ul_class else 'なし'}")
        
        # 直下のli要素のみを取得（ネストしたリストの項目は除外）
        direct_items = ul.find_all('li', recursive=False)
        print(f"  項目数: {len(direct_items)}個")
        
        for j, li in enumerate(direct_items, 1):
            text = li.get_text(strip=True)
            # ネストしたリストがある場合は最初の文だけ取得
            if li.find(['ul', 'ol']):
                # 子要素のテキストを除外して、直接のテキストのみ取得
                direct_text = ''.join(li.find_all(text=True, recursive=False)).strip()
                text = direct_text if direct_text else text.split('\n')[0]
            
            print(f"    {j}. {text}")
    print()

def scrape_ordered_lists(soup):
    """順序ありリスト (ol) を取得"""
    print("2. 順序ありリスト (ol) の取得")
    print("-" * 30)
    
    ol_lists = soup.find_all('ol')
    print(f"ol要素数: {len(ol_lists)}個")
    
    for i, ol in enumerate(ol_lists, 1):
        ol_id = ol.get('id', 'なし')
        ol_class = ' '.join(ol.get('class', []))
        start = ol.get('start', '1')
        list_type = ol.get('type', 'なし')
        
        print(f"\nリスト{i}:")
        print(f"  id: {ol_id}")
        print(f"  class: {ol_class if ol_class else 'なし'}")
        print(f"  start: {start}")
        print(f"  type: {list_type}")
        
        # 直下のli要素のみを取得
        direct_items = ol.find_all('li', recursive=False)
        print(f"  項目数: {len(direct_items)}個")
        
        for j, li in enumerate(direct_items, 1):
            text = li.get_text(strip=True)
            # ネストしたリストがある場合は最初の文だけ取得
            if li.find(['ul', 'ol']):
                direct_text = ''.join(li.find_all(text=True, recursive=False)).strip()
                text = direct_text if direct_text else text.split('\n')[0]
            
            print(f"    {j}. {text}")
    print()

def scrape_nested_lists(soup):
    """ネストしたリストを詳細に取得"""
    print("3. ネストしたリストの詳細取得")
    print("-" * 30)
    
    def process_list(list_element, level=0):
        """リストを再帰的に処理する関数"""
        indent = "  " * level
        list_type = list_element.name  # 'ul' または 'ol'
        
        items = list_element.find_all('li', recursive=False)
        print(f"{indent}{list_type}リスト ({len(items)}項目):")
        
        for i, li in enumerate(items, 1):
            # 直接のテキストコンテンツを取得
            direct_text = ''.join(li.find_all(text=True, recursive=False)).strip()
            print(f"{indent}  {i}. {direct_text}")
            
            # 子リストがあるかチェック
            child_lists = li.find_all(['ul', 'ol'], recursive=False)
            for child_list in child_lists:
                process_list(child_list, level + 2)
    
    # トップレベルのリストを検索
    top_lists = soup.find_all(['ul', 'ol'])
    nested_lists = []
    
    for lst in top_lists:
        # 子リストを含むかチェック
        if lst.find(['ul', 'ol']):
            nested_lists.append(lst)
    
    print(f"ネストしたリスト: {len(nested_lists)}個")
    
    for i, lst in enumerate(nested_lists, 1):
        print(f"\nネストリスト{i}:")
        process_list(lst)
    print()

def scrape_definition_lists(soup):
    """定義リスト (dl, dt, dd) を取得"""
    print("4. 定義リスト (dl, dt, dd) の取得")
    print("-" * 30)
    
    dl_lists = soup.find_all('dl')
    print(f"dl要素数: {len(dl_lists)}個")
    
    for i, dl in enumerate(dl_lists, 1):
        dl_id = dl.get('id', 'なし')
        dl_class = ' '.join(dl.get('class', []))
        
        print(f"\n定義リスト{i}:")
        print(f"  id: {dl_id}")
        print(f"  class: {dl_class if dl_class else 'なし'}")
        
        # dt (定義語) と dd (定義内容) を取得
        dts = dl.find_all('dt')
        dds = dl.find_all('dd')
        
        print(f"  定義語数: {len(dts)}個")
        print(f"  定義内容数: {len(dds)}個")
        
        # dt と dd をペアで表示
        for j, (dt, dd) in enumerate(zip(dts, dds), 1):
            dt_text = dt.get_text(strip=True)
            dd_text = dd.get_text(strip=True)
            
            print(f"    {j}. {dt_text}: {dd_text}")
    print()



def scrape_lists_by_class(soup):
    """特定のクラスを持つリストを取得"""
    print("6. 特定のクラスを持つリストの取得")
    print("-" * 30)
    
    # クラス名でリストを検索
    classes = ['programming-languages', 'tech-categories']
    
    for class_name in classes:
        # 全てのul, ol要素を取得
        all_lists = soup.find_all(['ul', 'ol'])
        elements = []
        
        # 各リスト要素のクラスをチェック
        for lst in all_lists:
            class_attr = lst.get('class')
            if class_attr:  # クラス属性が存在する場合
                class_string = ' '.join(class_attr)  # リストを文字列に変換
                if class_name in class_string:  # 指定したクラス名が含まれるかチェック
                    elements.append(lst)
        
        if elements:
            print(f"\n'{class_name}'を含むクラスのリスト: {len(elements)}個")
            for i, element in enumerate(elements, 1):
                element_class = ' '.join(element.get('class', []))
                items = element.find_all('li', recursive=False)
                
                print(f"  {i}. class='{element_class}' ({len(items)}項目)")
                for j, item in enumerate(items[:3], 1):  # 最初の3項目のみ表示
                    text = item.get_text(strip=True)[:30]
                    print(f"     {j}. {text}...")
    print()

def main():
    """メイン関数 - メニュー形式で実行する機能を選択"""
    menu = [
        ("順序なしリスト (ul) の取得", scrape_unordered_lists),
        ("順序ありリスト (ol) の取得", scrape_ordered_lists),
        ("ネストしたリストの詳細取得", scrape_nested_lists),
        ("定義リスト (dl, dt, dd) の取得", scrape_definition_lists),
        ("特定のクラスを持つリストの取得", scrape_lists_by_class),
    ]
    
    print("📋 リスト要素スクレイピング練習")
    print("対象: リストページ (/list)")
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
