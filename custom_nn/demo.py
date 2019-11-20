import cv2
import tensorflow as tf
import numpy as np
from time import time
from custom_nn.model import model
#
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
sess = tf.Session(config=config)
# import os
# os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"   # see issue #152
# os.environ["CUDA_VISIBLE_DEVICES"] = ""

myModel = model((720, 1280, 3))
myModel.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
myModel.load_weights("weights/backup-13-0.94.hdf5")
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
while True:
    _, frame = cap.read()
    now = time()
    prediction = myModel.predict(np.expand_dims(cv2.resize(frame, dsize=(1280, 720)), axis=0))[0]
    print(1 / (time() - now))
    chan_a = prediction[..., 0]
    chan_b = prediction[..., 1]
    cv2.imshow("orig", frame)
    # cv2.imshow("a", cv2.threshold(chan_a, 0.2, 1.0, cv2.THRESH_BINARY)[1])
    cv2.imshow("a", chan_a)
    cv2.imshow("b", chan_b)
    cv2.waitKey(1)
