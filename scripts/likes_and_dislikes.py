#!/usr/bin/env python3

# ライブラリのインポート
import rospy
import roslib.packages
import cv2
import time
import os
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist

import boto3
import json
import sys
import pydub
import subprocess
import contextlib

# 自作のライブラリをインポート
import detect_banana_and_nasu
import speech

# バナナとナスを識別するクラス
class BananaAndNasu():
    def __init__(self):
        # サブスクライバーを定義
        rospy.Subscriber("/usb_cam/image_raw", Image, self.callback_img)
        # 画像を保持する変数
        self.image = None
        # 画像の保存先
        self.image_path = roslib.packages.get_pkg_dir("banana_and_nasu") + "/scripts/images/camera.jpg"
    
    def callback_img(self, data):
        """
        受け取った画像を保存する関数
        """

        # 画像をROSのデータ形式からOpenCV形式に変換して変数に保存
        self.image = CvBridge().imgmsg_to_cv2(data, "bgr8")

    def save_image(self):
        """
        画像をファイルとして保存する関数
        """
        
        rospy.loginfo("カメラ画像を保存（{}）".format(self.image_path))
        cv2.imwrite(self.image_path, self.image)

    def detect_label(self):
        """
        バナナとナスを検出して発話させる関数
        """

        rospy.loginfo("AWSを使った画像認識を開始")
        transrate = rospy.get_param('likes_and_dislikes/transrate')
        result_data = detect_banana_and_nasu.banana_nasu_sagasu(self.image_path, transrate=transrate)
        detect_flag = False
        for d in result_data:
            if d == "ナス":
                speech.speech_message("ナスきらい!!!")
                detect_flag = True
            if d == "バナナ":
                speech.speech_message("ばなな大好き!!!")
                detect_flag = True
        if not detect_flag:
            rospy.loginfo("バナナとナスが見つかりませんでした。")

    def run(self):
        """
        一連の処理を行う関数
        """

        if self.image is not None:
            self.save_image()
            self.detect_label()
        else:
            rospy.loginfo("画像がありません。")

if __name__ == '__main__':
    # ノードを宣言
    rospy.init_node('banana_and_nasu')
    # クラスのインスタンスを作成
    ban = BananaAndNasu()
    # 一定周期で処理を実行するための準備
    rate = rospy.Rate(1)
    # ループ処理開始
    while not rospy.is_shutdown():
        # 処理を実行
        ban.run()
        rate.sleep()
