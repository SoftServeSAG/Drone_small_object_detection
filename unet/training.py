import os
# os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"   # see issue #152
# os.environ["CUDA_VISIBLE_DEVICES"] = ""

import segmentation_models as sm
import tensorflow as tf
from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, TensorBoard
import dataGeneratorUnet


config = tf.ConfigProto()
config.gpu_options.allow_growth = True
sess = tf.Session(config=config)

model = sm.Unet('mobilenetv2', classes=1, activation='sigmoid', encoder_weights='imagenet', encoder_freeze=True)
# preprocess_input = sm.get_preprocessing('mobilenetv2')

model.compile(
    'Adam',
    loss=sm.losses.bce_jaccard_loss,
    # loss="binary_crossentropy", metrics=["accuracy"]
    metrics=[sm.metrics.iou_score, "accuracy"]
)

lr_reducer = ReduceLROnPlateau(factor=0.1,
                               cooldown=10,
                               patience=10, verbose=1,
                               min_lr=0.1e-5)
# model autosave callbacks
checkpoint = ModelCheckpoint("./weights/best/backup-{epoch:02d}-{val_accuracy:.2f}.hdf5", monitor='val_accuracy',
                             verbose=1, save_best_only=True, mode='max')
checkpoint_e = ModelCheckpoint("./weights/backup/backup-{epoch:02d}.hdf5", verbose=1, save_weights_only=True, period=1)
tensorboard = TensorBoard(log_dir='./logs/tenboard', histogram_freq=0,
                          write_graph=True, write_images=True, update_freq="batch")

callbacks = [checkpoint, checkpoint_e, lr_reducer, tensorboard]

train_generator = dataGeneratorUnet.DataGenerator(root_dir=r"./data/train", batch_size=3)
validation_generator = dataGeneratorUnet.DataGenerator(root_dir=r"./data/validation", batch_size=3)


model.fit_generator(generator=train_generator,
                    validation_data=validation_generator,
                    use_multiprocessing=True,
                    workers=12,
                    epochs=50,
                    callbacks=callbacks)

model.save_weights("./weights/final-weights.hdf5")

