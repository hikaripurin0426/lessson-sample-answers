#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
【動的サイト対応】Seleniumを使用した動的コンテンツのスクレイピング
このスクリプトは以下のことを行います：
1. Seleniumを使用してブラウザを自動操作
2. JavaScriptで生成される動的コンテンツを取得
3. リアルタイムで更新される要素を監視
4. ユーザーインタラクションをシミュレート
5. 取得したデータをCSVとJSONで保存
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import json
import csv
import os
from datetime import datetime

def setup_driver():
    """Chrome WebDriverを設定して返す"""
    print("🔧 WebDriverを設定中...")
    
    # Chromeのオプション設定
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    try:
        # WebDriverを初期化
        driver = webdriver.Chrome(options=chrome_options)
        print("✓ WebDriver初期化成功")
        return driver
    except Exception as e:
        print(f"✗ WebDriver初期化失敗: {e}")
        print("ChromeDriverが正しくインストールされているか確認してください")
        return None

def scrape_realtime_content(driver):
    """リアルタイムで更新される時刻情報を取得"""
    print("\n📅 リアルタイム時刻情報を取得中...")
    
    try:
        # 時刻表示要素が読み込まれるまで待機（最大10秒）
        time_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "current-time"))
        )
        
        # 複数回時刻を取得して変化を確認
        time_data = []
        for i in range(3):
            current_time = driver.find_element(By.ID, "current-time").text
            current_date = driver.find_element(By.ID, "current-date").text
            timestamp_element = driver.find_element(By.ID, "timestamp")
            timestamp = timestamp_element.get_attribute("data-timestamp")
            
            time_info = {
                "取得回数": i + 1,
                "現在時刻": current_time,
                "現在日付": current_date,
                "タイムスタンプ": timestamp,
                "取得時刻": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            time_data.append(time_info)
            print(f"  取得{i+1}: {current_time}")
            
            if i < 2:  # 最後の取得でない場合は待機
                time.sleep(2)
        
        return time_data
        
    except TimeoutException:
        print("✗ 時刻要素の読み込みがタイムアウトしました")
        return []
    except Exception as e:
        print(f"✗ 時刻取得エラー: {e}")
        return []

def interact_with_counter(driver):
    """カウンターを操作して、動的な変化を観察"""
    print("\n🔢 カウンター操作中...")
    
    try:
        counter_data = []
        
        # 初期値を取得
        counter_element = driver.find_element(By.ID, "counter-value")
        initial_value = int(counter_element.get_attribute("data-count"))
        status_element = driver.find_element(By.CLASS_NAME, "counter-status")
        initial_status = status_element.get_attribute("data-status")
        
        counter_data.append({
            "操作": "初期値",
            "値": initial_value,
            "ステータス": initial_status,
            "表示テキスト": counter_element.text
        })
        print(f"  初期値: {initial_value} (ステータス: {initial_status})")
        
        # インクリメントボタンを3回クリック
        increment_btn = driver.find_element(By.CLASS_NAME, "increment-btn")
        for i in range(3):
            increment_btn.click()
            time.sleep(0.5)  # 少し待機
            
            value = int(counter_element.get_attribute("data-count"))
            status = status_element.get_attribute("data-status")
            
            counter_data.append({
                "操作": f"インクリメント_{i+1}",
                "値": value,
                "ステータス": status,
                "表示テキスト": counter_element.text
            })
            print(f"  インクリメント{i+1}: {value} (ステータス: {status})")
        
        # デクリメントボタンを5回クリック
        decrement_btn = driver.find_element(By.CLASS_NAME, "decrement-btn")
        for i in range(5):
            decrement_btn.click()
            time.sleep(0.5)
            
            value = int(counter_element.get_attribute("data-count"))
            status = status_element.get_attribute("data-status")
            
            counter_data.append({
                "操作": f"デクリメント_{i+1}",
                "値": value,
                "ステータス": status,
                "表示テキスト": counter_element.text
            })
            print(f"  デクリメント{i+1}: {value} (ステータス: {status})")
        
        # リセットボタンをクリック
        reset_btn = driver.find_element(By.CLASS_NAME, "reset-btn")
        reset_btn.click()
        time.sleep(0.5)
        
        final_value = int(counter_element.get_attribute("data-count"))
        final_status = status_element.get_attribute("data-status")
        
        counter_data.append({
            "操作": "リセット",
            "値": final_value,
            "ステータス": final_status,
            "表示テキスト": counter_element.text
        })
        print(f"  リセット: {final_value} (ステータス: {final_status})")
        
        return counter_data
        
    except Exception as e:
        print(f"✗ カウンター操作エラー: {e}")
        return []

def manipulate_dynamic_list(driver):
    """動的リストの操作と監視"""
    print("\n📝 動的リスト操作中...")
    
    try:
        list_data = []
        
        # 初期アイテム数を取得
        item_count_element = driver.find_element(By.CLASS_NAME, "item-count")
        initial_count = int(item_count_element.get_attribute("data-count"))
        print(f"  初期アイテム数: {initial_count}")
        
        # 初期リストアイテムを取得
        initial_items = driver.find_elements(By.CLASS_NAME, "dynamic-item")
        for i, item in enumerate(initial_items):
            item_text = item.find_element(By.CLASS_NAME, "item-text").text
            item_id = item.get_attribute("data-item-id")
            list_data.append({
                "操作": "初期アイテム",
                "インデックス": i,
                "アイテムID": item_id,
                "テキスト": item_text,
                "総アイテム数": initial_count
            })
        
        # 新しいアイテムを3つ追加
        add_btn = driver.find_element(By.CLASS_NAME, "add-item-btn")
        for i in range(3):
            add_btn.click()
            time.sleep(0.5)
            
            # 更新されたアイテム数を取得
            current_count = int(item_count_element.get_attribute("data-count"))
            # 最後に追加されたアイテムを取得
            items = driver.find_elements(By.CLASS_NAME, "dynamic-item")
            if items:
                last_item = items[-1]
                item_text = last_item.find_element(By.CLASS_NAME, "item-text").text
                item_id = last_item.get_attribute("data-item-id")
                
                list_data.append({
                    "操作": f"アイテム追加_{i+1}",
                    "インデックス": len(items) - 1,
                    "アイテムID": item_id,
                    "テキスト": item_text,
                    "総アイテム数": current_count
                })
                print(f"  追加{i+1}: {item_text} (総数: {current_count})")
        
        # 最初のアイテムを削除
        items = driver.find_elements(By.CLASS_NAME, "dynamic-item")
        if items:
            first_item = items[0]
            item_text = first_item.find_element(By.CLASS_NAME, "item-text").text
            remove_btn = first_item.find_element(By.CLASS_NAME, "remove-btn")
            remove_btn.click()
            time.sleep(0.5)
            
            current_count = int(item_count_element.get_attribute("data-count"))
            list_data.append({
                "操作": "アイテム削除",
                "インデックス": 0,
                "アイテムID": "削除済み",
                "テキスト": f"削除: {item_text}",
                "総アイテム数": current_count
            })
            print(f"  削除: {item_text} (総数: {current_count})")
        
        return list_data
        
    except Exception as e:
        print(f"✗ 動的リスト操作エラー: {e}")
        return []

def scrape_async_news(driver):
    """非同期ニュース読み込みの監視"""
    print("\n📰 非同期ニュース読み込み中...")
    
    try:
        news_data = []
        
        # 初期ニュースアイテムを取得
        initial_news = driver.find_elements(By.CLASS_NAME, "news-item")
        print(f"  初期ニュース数: {len(initial_news)}")
        
        for news in initial_news:
            title = news.find_element(By.CLASS_NAME, "news-title").text
            date = news.get_attribute("data-date")
            category = news.get_attribute("data-category")
            news_id = news.get_attribute("data-news-id")
            
            news_data.append({
                "タイプ": "初期ニュース",
                "ニュースID": news_id,
                "タイトル": title,
                "日付": date,
                "カテゴリ": category
            })
        
        # さらに読み込むボタンをクリック
        load_more_btn = driver.find_element(By.CLASS_NAME, "load-more-btn")
        
        # ローディング状態を確認
        print("  ニュースを追加読み込み中...")
        load_more_btn.click()
        
        # ローディングインジケーターが表示されることを確認
        try:
            loading_indicator = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "loading-spinner"))
            )
            print("  ✓ ローディングインジケーター確認")
        except TimeoutException:
            print("  ⚠ ローディングインジケーターが見つかりませんでした")
        
        # 新しいニュースが読み込まれるまで待機
        time.sleep(2)
        
        # 更新されたニュースアイテムを取得
        updated_news = driver.find_elements(By.CLASS_NAME, "news-item")
        print(f"  更新後ニュース数: {len(updated_news)}")
        
        # 新しく追加されたニュースを特定
        # 例：初期ニュースが3個、追加後が5個の場合
        # initial_news = [news1, news2, news3]  # len=3
        # updated_news = [news1, news2, news3, news4, news5]  # len=5
        # updated_news[3:] = [news4, news5]  （新しいニュースのみ
        for news in updated_news[len(initial_news):]:
            title = news.find_element(By.CLASS_NAME, "news-title").text
            date = news.get_attribute("data-date")
            category = news.get_attribute("data-category")
            news_id = news.get_attribute("data-news-id")
            
            news_data.append({
                "タイプ": "追加ニュース",
                "ニュースID": news_id,
                "タイトル": title,
                "日付": date,
                "カテゴリ": category
            })
            print(f"  新規: {title}")
        
        return news_data
        
    except Exception as e:
        print(f"✗ ニュース読み込みエラー: {e}")
        return []

def test_conditional_visibility(driver):
    """条件付き表示要素のテスト"""
    print("\n👁 条件付き表示要素のテスト中...")
    
    try:
        visibility_data = []
        
        # 条件付きメッセージ要素を取得
        conditional_element = driver.find_element(By.ID, "conditional-message")
        
        # 初期状態（非表示）を確認
        initial_visible = conditional_element.is_displayed()
        initial_data_visible = conditional_element.get_attribute("data-visible")
        
        visibility_data.append({
            "状態": "初期",
            "表示": initial_visible,
            "data-visible": initial_data_visible
        })
        print(f"  初期状態: 表示={initial_visible}, data-visible={initial_data_visible}")
        
        # チェックボックスを見つけてクリック
        checkbox = driver.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
        checkbox.click()
        time.sleep(0.5)
        
        # 表示状態を確認
        after_click_visible = conditional_element.is_displayed()
        after_click_data_visible = conditional_element.get_attribute("data-visible")
        
        visibility_data.append({
            "状態": "チェック後",
            "表示": after_click_visible,
            "data-visible": after_click_data_visible
        })
        print(f"  チェック後: 表示={after_click_visible}, data-visible={after_click_data_visible}")
        
        # もう一度クリックして非表示に
        checkbox.click()
        time.sleep(0.5)
        
        final_visible = conditional_element.is_displayed()
        final_data_visible = conditional_element.get_attribute("data-visible")
        
        visibility_data.append({
            "状態": "チェック解除後",
            "表示": final_visible,
            "data-visible": final_data_visible
        })
        print(f"  チェック解除後: 表示={final_visible}, data-visible={final_data_visible}")
        
        return visibility_data
        
    except Exception as e:
        print(f"✗ 条件付き表示テストエラー: {e}")
        return []

def save_data_to_files(time_data, counter_data, list_data, news_data, visibility_data):
    """収集したデータをファイルに保存"""
    print("\n💾 データを保存中...")
    
    # output フォルダを作成
    output_folder = "output"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"✓ フォルダ作成: {output_folder}")
    
    # JSONファイルとして保存
    all_data = {
        "スクレイピング情報": {
            "実行日時": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "対象URL": "https://scraping-practice-six.vercel.app/dynamic",
            "使用ツール": "Selenium WebDriver"
        },
        "リアルタイム時刻データ": time_data,
        "カウンター操作データ": counter_data,
        "動的リストデータ": list_data,
        "非同期ニュースデータ": news_data,
        "条件付き表示データ": visibility_data
    }
    
    json_filename = os.path.join(output_folder, "dynamic_scraping_data.json")
    try:
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2)
        print(f"✓ JSONファイル保存: {json_filename}")
    except Exception as e:
        print(f"✗ JSON保存エラー: {e}")
    
    # CSVファイルとして保存（カウンターデータを例として）
    csv_filename = os.path.join(output_folder, "counter_operations.csv")
    try:
        with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
            if counter_data:
                writer = csv.DictWriter(f, fieldnames=counter_data[0].keys())
                writer.writeheader()
                writer.writerows(counter_data)
        print(f"✓ CSVファイル保存: {csv_filename}")
    except Exception as e:
        print(f"✗ CSV保存エラー: {e}")
    
    # ニュースデータもCSVで保存
    news_csv_filename = os.path.join(output_folder, "news_data.csv")
    try:
        with open(news_csv_filename, 'w', newline='', encoding='utf-8') as f:
            if news_data:
                writer = csv.DictWriter(f, fieldnames=news_data[0].keys())
                writer.writeheader()
                writer.writerows(news_data)
        print(f"✓ ニュースCSVファイル保存: {news_csv_filename}")
    except Exception as e:
        print(f"✗ ニュースCSV保存エラー: {e}")

def main():
    """メイン実行関数"""
    print("🚀 動的コンテンツスクレイピング開始")
    print("=" * 60)
    
    # WebDriverを設定
    driver = setup_driver()
    if not driver:
        return
    
    try:
        # 対象ページにアクセス
        url = "https://scraping-practice-six.vercel.app/dynamic"
        print(f"🌐 ページにアクセス中: {url}")
        driver.get(url)
        
        # ページが完全に読み込まれるまで待機
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        print("✓ ページ読み込み完了")
        
        # 各種スクレイピング実行
        time_data = scrape_realtime_content(driver)
        counter_data = interact_with_counter(driver)
        list_data = manipulate_dynamic_list(driver)
        news_data = scrape_async_news(driver)
        visibility_data = test_conditional_visibility(driver)
        
        # データを保存
        save_data_to_files(time_data, counter_data, list_data, news_data, visibility_data)
        
        # 結果表示
        print("\n" + "=" * 60)
        print("🎉 動的コンテンツスクレイピング完了")
        print("=" * 60)
        print(f"時刻データ: {len(time_data)}件")
        print(f"カウンター操作: {len(counter_data)}件")
        print(f"リスト操作: {len(list_data)}件")
        print(f"ニュースデータ: {len(news_data)}件")
        print(f"表示制御テスト: {len(visibility_data)}件")
        print("=" * 60)
        
    except Exception as e:
        print(f"✗ メイン処理エラー: {e}")
    
    finally:
        # ブラウザを閉じる
        print("🔄 ブラウザを閉じています...")
        driver.quit()
        print("✓ クリーンアップ完了")

if __name__ == "__main__":
    main()
