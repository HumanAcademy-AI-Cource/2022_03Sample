#!/usr/bin/env python

# ライブラリのインポート
import boto3
import subprocess
import wave


def onsei_gousei(text):
    """
    AWSを使った音声合成の関数
    """
    
    polly = boto3.client(service_name="polly")
    return polly.synthesize_speech(
        Text=text,
        OutputFormat='pcm',
        VoiceId='Mizuki'
    )['AudioStream']

def onsei_hozon(data, filename):
    """
    音声データを保存する関数
    """

    wave_data = wave.open(filename, 'wb')
    wave_data.setnchannels(1)
    wave_data.setsampwidth(2)
    wave_data.setframerate(16000)
    wave_data.writeframes(data.read())
    # ファイルを閉じる
    wave_data.close()

def onsei_saisei(filename):
    """
    音声データを再生する関数
    """

    subprocess.check_call('aplay -D plughw:Headphones {}'.format("speech.wav"), shell=True)

def speech_message(message):
    """
    テキストを音声合成して再生する関数
    """

    print("発話させる文章: {}".format(message))
    # テキストを音声合成
    speech_data = onsei_gousei(message)
    # 音声データを保存
    onsei_hozon(speech_data, "speech.wav")
    # 音声データを再生
    onsei_saisei("speech.wav")

if __name__ == '__main__':
    speech_message("バナナ")
    speech_message("ナス")
