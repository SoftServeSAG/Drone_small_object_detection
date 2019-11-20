import os

# os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"   # see issue #152
# os.environ["CUDA_VISIBLE_DEVICES"] = ""

import cv2
from time import time
import segmentation_models as sm
import keras
import numpy as np
import tensorflow as tf
from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, TensorBoard
import dataGeneratorUnet


config = tf.ConfigProto()
config.gpu_options.allow_growth = True
sess = tf.Session(config=config)

model = sm.Unet('mobilenetv2', classes=1, activation='sigmoid')

model.compile(
    'Adam',
    # loss=sm.losses.bce_jaccard_loss,
    loss="binary_crossentropy", metrics=["accuracy"]
    # metrics=[sm.metrics.iou_score, "accuracy"]
)

model.load_weights("./weights/backup/backup-25.hdf5")
model.save("./weights/final_0.hdf5")
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)



while True:
    _, frame = cap.read()
    now = time()
    inp = np.expand_dims(frame, axis=0)
    prediction = model.predict(inp)
    print(1 / (time() - now))
    cv2.imshow("orig", inp[0])
    rr = prediction[0]

    print(inp.shape, prediction.shape)
    cv2.imshow("orig2", rr)

    cv2.waitKey(1)


