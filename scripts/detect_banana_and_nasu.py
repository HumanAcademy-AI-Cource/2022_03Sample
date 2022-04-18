#!/usr/bin/env python

# ライブラリのインポート
import boto3
import cv2
import time
import random

# 自作のライブラリをインポート
import translate

def gazou_ninshiki(path):
    """
    AWSを使った画像認識の関数
    """

    # 画像認識の準備
    rekognition = boto3.client("rekognition")
    # 画像を読み込んで物を探す
    with open(path, 'rb') as f:
        try:
            return rekognition.detect_labels(
                Image={'Bytes': f.read()},
            )["Labels"]
        except Exception as e:
            print("AWSが混み合っていますので、しばらくお待ちください。")
            time.sleep(int(random.uniform(0, 5)))
            return []
    return []

def banana_nasu_sagasu(path, transrate=False):
    """
    AWSを使ったバナナとナスを探す関数
    """

    # 画像に映る物を探す
    result_data = result_data = gazou_ninshiki(path)
    # 返り値用の配列を定義
    return_data = []
    print("------------------------------------------")
    for d in result_data:
        if d["Name"] == "Eggplant":
            return_data.append("ナス")
        if d["Name"] == "Banana":
            return_data.append("バナナ")
        if transrate:
            print("ラベル: {}({}) - {:.1f}％".format(d["Name"], translate.honyaku(d["Name"], "en", "ja"), d["Confidence"]))
        else:
            print("ラベル: {} - {:.1f}％".format(d["Name"], d["Confidence"]))
        # 注意（翻訳機能を有効にすると動作が少し遅くなります）
        
    print("------------------------------------------")
    return return_data

if __name__ == '__main__':
    # 画像のパス
    image_path = "./images/nasu.jpg"
    # バナナかナスがあるか調べる
    result_data = banana_nasu_sagasu(image_path)
    # 1個以上ある場合はログを出力する
    if len(result_data) != 0:
        for d in result_data:
            print("{}が見つかりました。".format(d))
    else:
        print("見つかりませんでした。")
