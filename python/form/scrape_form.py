#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
フォーム要素のスクレイピング練習
このスクリプトはフォームページから様々なフォーム要素を抽出します。

学習ポイント:
- input要素の種類別取得
- select要素とoption要素の取得
"""

import requests
from bs4 import BeautifulSoup

# スクレイピング対象のURL
URL = "https://scraping-practice-six.vercel.app/form"

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

def scrape_form_basic_info(soup):
    """フォーム要素の基本情報を取得"""
    print("1. フォーム要素の基本情報")
    print("-" * 30)
    
    forms = soup.find_all('form')
    print(f"ページ内のフォーム数: {len(forms)}個")
    
    for i, form in enumerate(forms, 1):
        form_id = form.get('id', 'なし')
        
        print(f"\nフォーム{i}:")
        print(f"  id: {form_id}")
    print()

def scrape_input_elements(soup):
    """input要素を種類別に分類して取得"""
    print("2. input要素の詳細情報")
    print("-" * 30)
    
    inputs = soup.find_all('input')
    print(f"input要素の総数: {len(inputs)}個")
    
    # input要素を種類別に分類
    input_types = {}
    for input_elem in inputs:
        input_type = input_elem.get('type', 'text')
        if input_type not in input_types:
            input_types[input_type] = []
        input_types[input_type].append(input_elem)
    
    # 種類別に表示
    for input_type, elements in input_types.items():
        print(f"\n{input_type}タイプ: {len(elements)}個")
        for i, elem in enumerate(elements, 1):
            name = elem.get('name', 'なし')
            placeholder = elem.get('placeholder', 'なし')
            required = 'あり' if elem.get('required') else 'なし'
            
            print(f"  {i}. name: {name}")
            print(f"     placeholder: {placeholder}")
            print(f"     required: {required}")
    print()

def scrape_select_elements(soup):
    """select要素とoption要素を取得"""
    print("3. select要素とoption要素")
    print("-" * 30)
    
    selects = soup.find_all('select')
    print(f"select要素数: {len(selects)}個")
    
    for i, select in enumerate(selects, 1):
        name = select.get('name', 'なし')
        select_id = select.get('id', 'なし')
        multiple = 'あり' if select.get('multiple') else 'なし'
        
        print(f"\nセレクトボックス{i}:")
        print(f"  name: {name}")
        print(f"  id: {select_id}")
        print(f"  multiple: {multiple}")
        
        # option要素を取得
        options = select.find_all('option')
        print(f"  option数: {len(options)}個")
        for j, option in enumerate(options, 1):
            value = option.get('value', 'なし')
            text = option.get_text(strip=True)
            selected = 'あり' if option.get('selected') else 'なし'
            
            print(f"    {j}. value: {value}, text: {text}, selected: {selected}")
    print()

def scrape_textarea_elements(soup):
    """textarea要素を取得"""
    print("4. textarea要素")
    print("-" * 30)
    
    textareas = soup.find_all('textarea')
    print(f"textarea要素数: {len(textareas)}個")
    
    for i, textarea in enumerate(textareas, 1):
        name = textarea.get('name', 'なし')
        placeholder = textarea.get('placeholder', 'なし')
        rows = textarea.get('rows', 'なし')
        cols = textarea.get('cols', 'なし')
        content = textarea.get_text(strip=True)
        
        print(f"\nテキストエリア{i}:")
        print(f"  name: {name}")
        print(f"  placeholder: {placeholder}")
        print(f"  rows: {rows}")
        print(f"  cols: {cols}")
        print(f"  内容: {content[:50]}..." if len(content) > 50 else f"  内容: {content}")
    print()

def scrape_label_elements(soup):
    """label要素とfor属性を取得"""
    print("5. label要素とfor属性")
    print("-" * 30)
    
    labels = soup.find_all('label')
    print(f"label要素数: {len(labels)}個")
    
    for i, label in enumerate(labels, 1):
        for_attr = label.get('for', 'なし')
        text = label.get_text(strip=True)
        
        print(f"ラベル{i}:")
        print(f"  for: {for_attr}")
        print(f"  テキスト: {text}")
        
        # for属性が指定されている場合、対応する要素を探す
        if for_attr != 'なし':
            target = soup.find(id=for_attr)
            if target:
                print(f"  対応要素: {target.name}タグ (id={for_attr})")
            else:
                print(f"  対応要素: 見つかりません")
        print()

def scrape_button_elements(soup):
    """button要素を取得"""
    print("6. button要素")
    print("-" * 30)
    
    buttons = soup.find_all('button')
    print(f"button要素数: {len(buttons)}個")
    
    for i, button in enumerate(buttons, 1):
        button_type = button.get('type', 'button')
        name = button.get('name', 'なし')
        value = button.get('value', 'なし')
        text = button.get_text(strip=True)
        
        print(f"ボタン{i}:")
        print(f"  type: {button_type}")
        print(f"  name: {name}")
        print(f"  value: {value}")
        print(f"  テキスト: {text}")
        print()

def scrape_form_validation_attributes(soup):
    """フォームのバリデーション属性を取得"""
    print("7. フォームのバリデーション属性")
    print("-" * 30)
    
    # バリデーション属性を持つ要素を検索
    validation_attrs = ['required', 'pattern', 'min', 'max', 'minlength', 'maxlength']
    
    for attr in validation_attrs:
        elements = soup.find_all(attrs={attr: True})
        if elements:
            print(f"\n{attr}属性を持つ要素: {len(elements)}個")
            for i, elem in enumerate(elements, 1):
                tag = elem.name
                name = elem.get('name', 'なし')
                attr_value = elem.get(attr, 'なし')
                
                print(f"  {i}. {tag}タグ (name: {name})")
                print(f"     {attr}: {attr_value}")
    print()

def main():
    """メイン関数 - メニュー形式で実行する機能を選択"""
    menu = [
        ("フォーム要素の基本情報", scrape_form_basic_info),
        ("input要素の詳細情報", scrape_input_elements),
        ("select要素とoption要素", scrape_select_elements),
        ("textarea要素", scrape_textarea_elements),
        ("label要素とfor属性", scrape_label_elements),
        ("button要素", scrape_button_elements),
        ("フォームのバリデーション属性", scrape_form_validation_attributes),
    ]
    
    print("📝 フォーム要素スクレイピング練習")
    print("対象: フォームページ (/form)")
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
