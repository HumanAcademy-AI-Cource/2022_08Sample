#!/usr/bin/env python3

# 必要なライブラリをインポート
import rospy
import cv2
import os
import roslib.packages

from cv_bridge import CvBridge
import numpy as np
from std_msgs.msg import *
from sensor_msgs.msg import Image
from sensor_msgs.msg import CompressedImage


class SatueiNode(object):
    def __init__(self):
        # ROSの設定
        rospy.Subscriber("/usb_cam/image_raw", Image, self.image_callback)
        rospy.Subscriber("/satuei", Bool, self.satuei_callback)
        self.pub = rospy.Publisher("/shot_image", CompressedImage, queue_size=1)
        self.image = None
        # 画像の保存先ディレクトリのパスを定義
        self.image_dir = roslib.packages.get_pkg_dir("ros_satuei") + "/scripts/images/"
        # フォルダがない場合は新しく作成
        if not os.path.isdir(self.image_dir):
            os.mkdir(self.image_dir)
        rospy.spin()

    def image_callback(self, msg):
        self.image = CvBridge().imgmsg_to_cv2(msg, "bgr8")
        
    def satuei_callback(self, msg):
        if self.image is not None:
            cv2.imwrite(self.image_dir + "camera.jpg", self.image)
            cv_image = cv2.imread(self.image_dir + "camera.jpg")

            pub_image = CompressedImage()
            pub_image.header.stamp = rospy.Time.now()
            pub_image.format = "jpeg"
            pub_image.data = np.array(cv2.imencode(".jpg", cv_image)[1]).tostring()

            self.pub.publish(pub_image)
            rospy.loginfo("撮影が完了しました。")
            rospy.sleep(1)

if __name__ == '__main__':
    # ノードを宣言
    rospy.init_node("satuei")
    # クラスのインスタンスを作成し、メイン関数を実行
    SatueiNode()
