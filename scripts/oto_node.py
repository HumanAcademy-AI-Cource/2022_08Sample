#!/usr/bin/env python3

# 必要なライブラリをインポート
import rospy
from std_msgs.msg import Float64
import pyaudio
import audioop
import numpy as np
import math


class OtoNode():
    def __init__(self):
        # パブリッシャーを定義
        self.sound_pub = rospy.Publisher("/sound", Float64, queue_size=1)

        # データ保存用の変数
        self.sound_val = None
        self.decibel = 0

        # チャンク:音源から1回読み込むときのデータサイズ
        self.chunk = 512
        # サンプリングレート
        sampling_rate = 44100

        self.p = pyaudio.PyAudio()
        self.p.stream = self.p.open(format=self.p.get_format_from_width(2), channels=1, rate=sampling_rate, frames_per_buffer=self.chunk, input=True, output=False)
        self.stream = self.p.stream

    def get_sound_val(self):
        """
        音センサ（マイク）からの音を処理する関数
        """

        # 音声データを取得
        # CHANKの長さ分のデータを読み込む（データの中身は、音センサから取得した音の強さを表すデジタルの数値）
        input = self.stream.read(self.chunk, exception_on_overflow=False)
        # 音センサの値をint16のNumpy形式に変換
        self.sound_val = np.frombuffer(input, dtype='int16')
        # デシベルに変換
        rms = audioop.rms(self.sound_val[0], 2)
        self.decibel = 20 * math.log10(rms) if rms > 0 else 0
        # 変換したデシベルの値をパブリッシュする
        print("音センサの値[db]: {}".format(self.decibel))
        self.sound_pub.publish(self.decibel)

    def stop(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

if __name__ == '__main__':
    # ノードを宣言
    rospy.init_node("mic")
    # クラスのインスタンスを作成
    oto = OtoNode()
    # ループ処理開始
    while not rospy.is_shutdown():
        # 処理を実行
        oto.get_sound_val()
    oto.stop()
    

