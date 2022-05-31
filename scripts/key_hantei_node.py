#!/usr/bin/env python3

# 必要なライブラリをインポート
import sys
import select
import tty
import termios
import rospy
from std_msgs.msg import *

class KeyHanteiNode(object):
    def __init__(self):
        # ROSの設定
        self.pub = rospy.Publisher("/satuei", Bool, queue_size=1)

        # キー入力の設定
        old_console_setting = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())

    def main(self):
        # 一定周期でループを実行するための変数を定義
        rate = rospy.Rate(10)

        print("--------------------------------------------------")
        print(" スペースキー を押すと撮影します。")
        print("終了するには Ctrl-C を押してください。")
        print("--------------------------------------------------")
        # Whileでキー入力を待ち続ける
        while not rospy.is_shutdown():
            # キー入力があるか確認
            if select.select([sys.stdin], [], [], 0)[0] == [sys.stdin]:
                # 入力されたキーを調べる
                key = sys.stdin.read(1)
                # もしスペースが入力されていたら撮影コマンドを送信
                if key == " ":
                    self.pub.publish(True)
            rate.sleep()
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_console_setting)


if __name__ == '__main__':
    # ノードを宣言
    rospy.init_node("key_hantei")
    # クラスのインスタンスを作成し、メイン関数を実行
    KeyHanteiNode().main()
