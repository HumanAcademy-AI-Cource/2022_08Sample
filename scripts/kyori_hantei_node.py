#!/usr/bin/env python3

# 必要なライブラリをインポート
import rospy
from std_msgs.msg import *

class KyoriHanteiNode(object):
    def __init__(self):
        # ROSの設定
        rospy.Subscriber("/sensor", UInt16, self.sensor_callback)
        self.pub = rospy.Publisher("/satuei", Bool, queue_size=1)
        self.sensor_data = 0

    def sensor_callback(self, msg):
        self.sensor_data = msg.data

    def main(self):
        # 一定周期でループを実行するための変数を定義
        rate = rospy.Rate(10)
        # ループを実行
        while not rospy.is_shutdown():
            # 距離センサの値が600以上だったら撮影コマンドを送信
            if self.sensor_data >= 600:
                self.pub.publish(True)
            rate.sleep()


if __name__ == '__main__':
    # ノードを宣言
    rospy.init_node("kyori_hantei")
    # クラスのインスタンスを作成し、メイン関数を実行
    KyoriHanteiNode().main()
