#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
【失敗例】BeautifulSoupで動的コンテンツを取得しようとする
このスクリプトは意図的に失敗します：
- JavaScriptで生成される要素は取得できません
- リアルタイム更新される要素は古い値しか取得できません
- ユーザーインタラクションが必要な要素は取得できません

Seleniumとの違いを理解するための教材として使用してください。
"""

import requests
from bs4 import BeautifulSoup

def scrape_dynamic_page_with_soup():
    """BeautifulSoupで動的ページをスクレイピング（失敗例）"""
    print("🌐 BeautifulSoupで動的ページにアクセス中...")
    
    url = "https://scraping-practice-six.vercel.app/dynamic"
    
    try:
        # 通常のHTTPリクエスト
        response = requests.get(url)
        response.raise_for_status()
        print("✓ ページ取得成功")
        
        # BeautifulSoupで解析
        soup = BeautifulSoup(response.content, 'html.parser')
        print("✓ HTML解析完了")
        
    except Exception as e:
        print(f"✗ ページ取得失敗: {e}")
        return

    print("\n" + "=" * 60)
    print("BeautifulSoupでの取得結果（失敗例）")
    print("=" * 60)

    # 1. リアルタイム時刻の取得を試行
    print("\n1. リアルタイム時刻取得を試行...")
    try:
        time_element = soup.find('div', id='current-time')
        if time_element:
            print(f"  取得した時刻: {time_element.get_text(strip=True)}")
            print("  ⚠️  この時刻は静的なHTMLの初期値です")
            print("  ⚠️  実際の現在時刻ではありません")
        else:
            print("  ✗ 時刻要素が見つかりません")
            print("  → JavaScriptで動的に生成されている可能性があります")
    except Exception as e:
        print(f"  ✗ エラー: {e}")

    # 2. カウンター値の取得を試行
    print("\n2. カウンター値取得を試行...")
    try:
        counter_element = soup.find('div', id='counter-value')
        if counter_element:
            counter_value = counter_element.get_text(strip=True)
            data_count = counter_element.get('data-count', 'なし')
            print(f"  取得したカウンター値: {counter_value}")
            print(f"  data-count属性: {data_count}")
            print("  ⚠️  これは初期値（0）のみです")
            print("  ⚠️  ユーザーがボタンを押した後の値は取得できません")
        else:
            print("  ✗ カウンター要素が見つかりません")
    except Exception as e:
        print(f"  ✗ エラー: {e}")

    # 3. 動的リストの取得を試行
    print("\n3. 動的リスト取得を試行...")
    try:
        list_items = soup.find_all('li', class_='dynamic-item')
        print(f"  取得したリストアイテム数: {len(list_items)}個")
        
        if list_items:
            for i, item in enumerate(list_items):
                item_text_elem = item.find('span', class_='item-text')
                if item_text_elem:
                    print(f"    アイテム{i+1}: {item_text_elem.get_text(strip=True)}")
            print("  ⚠️  これは初期アイテムのみです")
            print("  ⚠️  「アイテムを追加」ボタンで追加されたアイテムは見えません")
        else:
            print("  ⚠️  動的リストアイテムが見つかりません")
            print("  → JavaScriptで動的に生成されている可能性があります")
    except Exception as e:
        print(f"  ✗ エラー: {e}")

    # 4. 非同期ニュースの取得を試行
    print("\n4. 非同期ニュース取得を試行...")
    try:
        news_items = soup.find_all('article', class_='news-item')
        print(f"  取得したニュース数: {len(news_items)}個")
        
        if len(news_items) > 0:
            for i, news in enumerate(news_items):
                title_elem = news.find('h3', class_='news-title')
                if title_elem:
                    print(f"    ニュース{i+1}: {title_elem.get_text(strip=True)}")
            print("  ⚠️  初期ニュースは見つかりませんでした")
            print("  → ページ読み込み時にJavaScriptで非同期ロードされます")
        else:
            print("  ✗ ニュースアイテムが見つかりません")
            print("  → 2秒の非同期読み込み待機が必要です")
    except Exception as e:
        print(f"  ✗ エラー: {e}")

    # 5. 条件付き表示要素の取得を試行
    print("\n5. 条件付き表示要素取得を試行...")
    try:
        conditional_element = soup.find('div', id='conditional-message')
        if conditional_element:
            style = conditional_element.get('style', '')
            data_visible = conditional_element.get('data-visible', 'なし')
            print(f"  要素の存在: 確認")
            print(f"  style属性: {style}")
            print(f"  data-visible属性: {data_visible}")
            print("  ⚠️  初期状態（非表示）の情報のみ取得可能")
            print("  ⚠️  チェックボックス操作後の状態変化は追跡できません")
        else:
            print("  ✗ 条件付き表示要素が見つかりません")
    except Exception as e:
        print(f"  ✗ エラー: {e}")


    print("\n" + "=" * 60)
    print("結論: BeautifulSoupの限界")
    print("=" * 60)
    print("❌ JavaScript生成コンテンツ → 取得不可")
    print("❌ リアルタイム更新 → 取得不可") 
    print("❌ ユーザーインタラクション → 実行不可")
    print("❌ 非同期データ読み込み → 待機不可")
    print("❌ 動的な状態変化 → 追跡不可")
    print()
    print("✅ 解決策: Seleniumを使用")
    print("  → ブラウザエンジンでJavaScript実行")
    print("  → 実際のユーザー操作をシミュレート")
    print("  → 動的な変化を待機・監視")
    print("=" * 60)

if __name__ == "__main__":
    print("🚫 動的コンテンツの静的スクレイピング（失敗例）")
    print("=" * 60)
    scrape_dynamic_page_with_soup()
