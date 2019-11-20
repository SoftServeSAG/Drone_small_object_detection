import sys, os, cv2, time
import numpy as np, math

model_xml = "/home/mmatsi/SS/customNN/unet/weights/weights_converted/openvino/frozen_model.xml"
model_bin = os.path.splitext(model_xml)[0] + ".bin"

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)

from openvino.inference_engine import IENetwork, IEPlugin
plugin = IEPlugin(device="CPU")
plugin.add_cpu_extension("/home/mmatsi/SS/ball_detection/demo/lib/libcpu_extension.so")
net = IENetwork(model=model_xml, weights=model_bin)
input_blob = next(iter(net.inputs))
exec_net = plugin.load(network=net)

while cap.isOpened():
    now = time.time()
    ret, image = cap.read()
    prepimg = image[np.newaxis, :, :, :].transpose((0, 3, 1, 2))
    outputs = exec_net.infer(inputs={input_blob: prepimg})
    # prediction = model.predict(prepimg)
    prediction = outputs["sigmoid/Sigmoid"][0][0]
    print((time.time() - now)*1000)
    cv2.imshow("orig", image)
    # rr = outputs[0]
    # print(rr.shape)
    cv2.imshow("orig2", prediction)
    cv2.waitKey(1)
