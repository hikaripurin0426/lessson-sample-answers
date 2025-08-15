#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
【初心者向け】画像スクレイピングの基本
このスクリプトは以下のことを行います：
1. Webページから全ての画像URLを取得
2. 画像URLをCSVファイルに保存
3. 画像をローカルフォルダにダウンロード
"""

import requests
from bs4 import BeautifulSoup
import csv
import os
from urllib.parse import urljoin, urlparse

def scrape_images():
    """画像を取得してCSVに保存、ローカルにダウンロードする"""
    
    # スクレイピング対象のURL
    url = "https://scraping-practice-six.vercel.app/basic"
    
    print("=" * 50)
    print("画像スクレイピング開始")
    print(f"対象URL: {url}")
    print("=" * 50)
    
    # 1. Webページを取得
    print("1. Webページを取得中...")
    try:
        response = requests.get(url)
        response.raise_for_status()  # エラーがあれば例外を発生
        print("✓ ページ取得成功")
    except Exception as e:
        print(f"✗ ページ取得失敗: {e}")
        return
    
    # 2. BeautifulSoupでHTMLを解析
    print("2. HTMLを解析中...")
    soup = BeautifulSoup(response.content, 'html.parser')
    print("✓ HTML解析完了")
    
    # 3. 全ての画像タグを検索
    print("3. 画像を検索中...")
    images = soup.find_all('img')
    print(f"✓ {len(images)}個の画像を発見")
    
    # 4. 画像情報をリストに保存
    image_list = []
    for i, img in enumerate(images, 1):
        # src属性（画像のURL）を取得
        src = img.get('src')
        if src:
            # 相対URLを絶対URLに変換
            full_url = urljoin(url, src)
            
            # alt属性（画像の説明文）を取得
            alt = img.get('alt', '説明なし')
            
            # 画像のファイル名を生成
            filename = f"image_{i}.jpg"
            
            # リストに追加
            image_data = {
                '番号': i,
                '画像URL': full_url,
                'alt属性': alt,
                'ファイル名': filename
            }
            image_list.append(image_data)
            
            print(f"  画像{i}: {alt} -> {full_url}")
    
    # 5. CSVファイルに保存
    print("\n4. CSVファイルに保存中...")
    csv_filename = "images.csv"
    try:
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            # CSVの列名を定義
            fieldnames = ['番号', '画像URL', 'alt属性', 'ファイル名']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # ヘッダー行を書き込み
            writer.writeheader()
            
            # データ行を書き込み
            for image_data in image_list:
                writer.writerow(image_data)
        
        print(f"✓ CSVファイル保存完了: {csv_filename}")
    except Exception as e:
        print(f"✗ CSV保存失敗: {e}")
        return
    
    # 6. 画像ダウンロード用フォルダを作成
    print("\n5. 画像をダウンロード中...")
    download_folder = "downloaded_images"
    
    # フォルダが存在しない場合は作成
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
        print(f"✓ フォルダ作成: {download_folder}")
    
    # 7. 各画像をダウンロード
    success_count = 0
    for image_data in image_list:
        try:
            # 画像URLからデータを取得
            img_response = requests.get(image_data['画像URL'])
            img_response.raise_for_status()
            
            # ファイルパスを作成
            file_path = os.path.join(download_folder, image_data['ファイル名'])
            
            # 画像ファイルを保存
            with open(file_path, 'wb') as f:
                f.write(img_response.content)
            
            print(f"  ✓ ダウンロード成功: {image_data['ファイル名']}")
            success_count += 1
            
        except Exception as e:
            print(f"  ✗ ダウンロード失敗: {image_data['ファイル名']} - {e}")
    
    # 8. 結果を表示
    print("\n" + "=" * 50)
    print("画像スクレイピング完了")
    print("=" * 50)
    print(f"発見した画像数: {len(image_list)}個")
    print(f"ダウンロード成功: {success_count}個")
    print(f"CSVファイル: {csv_filename}")
    print(f"画像フォルダ: {download_folder}")
    print("=" * 50)

if __name__ == "__main__":
    # プログラム実行時にscrape_images関数を呼び出し
    scrape_images()