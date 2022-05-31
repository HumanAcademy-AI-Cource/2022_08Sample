#!/usr/bin/env python3

# 必要なライブラリをインポート
import rospy
from std_msgs.msg import *

class OtoHanteiNode(object):
    def __init__(self):
        # ROSの設定
        rospy.Subscriber("/sound", Float64, self.sound_callback)
        self.pub = rospy.Publisher("/satuei", Bool, queue_size=1)
        self.sound_data = 0

    def sound_callback(self, msg):
        self.sound_data = msg.data

    def main(self):
        # 一定周期でループを実行するための変数を定義
        rate = rospy.Rate(10)
        # ループを実行
        while not rospy.is_shutdown():
            # 70dB以上だったら撮影コマンドを送信
            if self.sound_data >= 70:
                self.pub.publish(True)
            rate.sleep()


if __name__ == '__main__':
    # ノードを宣言
    rospy.init_node("oto_hantei")
    # クラスのインスタンスを作成し、メイン関数を実行
    OtoHanteiNode().main()
