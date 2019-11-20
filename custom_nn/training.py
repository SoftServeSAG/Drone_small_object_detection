import tensorflow as tf
from custom_nn.model import model
from custom_nn import dataGenerator
from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, TensorBoard

config = tf.ConfigProto()
config.gpu_options.allow_growth = True
sess = tf.Session(config=config)

train_generator = dataGenerator.DataGenerator(root_dir=r"./data/train", batch_size=16)
validation_generator = dataGenerator.DataGenerator(root_dir=r"./data/validation", batch_size=16)

myModel = model((720, 1280, 3))
myModel.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])


# reduces learning rate on plateau
lr_reducer = ReduceLROnPlateau(factor=0.1,
                               cooldown= 10,
                               patience=10,verbose =1,
                               min_lr=0.1e-5)
# model autosave callbacks
checkpoint = ModelCheckpoint("./weights/backup-{epoch:02d}-{val_accuracy:.2f}.hdf5", monitor='val_accuracy', verbose=1, save_best_only=True, mode='max')
checkpoint_e = ModelCheckpoint("./backup/backup-{epoch:02d}.hdf5", verbose=1, save_weights_only=True, period=1)

# stop learining as metric on validatopn stop increasing
# early_stopping = EarlyStopping(patience=10, verbose=1, mode = 'auto')

# tensorboard for monitoring logs
tensorboard = TensorBoard(log_dir='./logs/tenboard', histogram_freq=0,
                          write_graph=True, write_images=True, update_freq="batch")

callbacks = [checkpoint, checkpoint_e, lr_reducer, tensorboard]


myModel.load_weights("./weights/backup-03-0.98-best.hdf5")
myModel.fit_generator(generator=train_generator,
                      validation_data=validation_generator,
                      use_multiprocessing=True,
                      workers=12,
                      epochs=50,
                      callbacks=callbacks)


myModel.save_weights("./weighs/final-weights.hdf5")
