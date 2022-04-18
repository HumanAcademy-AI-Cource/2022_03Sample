#!/usr/bin/env python

# ライブラリのインポート
import boto3

def honyaku(text, source, target):
    """
    AWSを使って簡単に翻訳できるようにした関数
    """
    
    # AWSを使った翻訳の準備
    translate = boto3.client(service_name="translate")

    # 翻訳開始
    result = translate.translate_text(
        Text=text,
        SourceLanguageCode=source,
        TargetLanguageCode=target
    )["TranslatedText"]
    return result

if __name__ == '__main__':
    # 翻訳する文章の配列
    texts = ["banana", "nasu"]
    # 翻訳の設定
    source = "en"
    target = "ja"
    # 配列を展開して翻訳
    for text in texts:
        kekka = honyaku(text, source, target)
        print("元の文章({}): {}, 翻訳後({}): {}".format(source, text, target, kekka))
