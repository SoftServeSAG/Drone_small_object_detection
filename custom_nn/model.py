from keras import Model
from keras.layers import *


def model(input_shape):
    # Define the input_main placeholder as a tensor with shape input_shape. Think of this as your input_main image!
    nn_input = Input(input_shape)

    # Conv 1
    conv_1 = Conv2D(8, (7, 7), strides=(2, 2), padding="same")(nn_input)
    conv_1 = BatchNormalization()(conv_1)
    conv_1 = Activation('relu')(conv_1)

    conv_1 = Conv2D(8, (3, 3), padding="same")(conv_1)
    conv_1 = BatchNormalization()(conv_1)
    conv_1 = Activation('relu')(conv_1)

    conv_1 = MaxPooling2D((2, 2))(conv_1)

    # Conv 2
    conv_2 = Conv2D(16, (3, 3), name='conv2', padding="same")(conv_1)
    conv_2 = BatchNormalization()(conv_2)
    conv_2 = Activation('relu')(conv_2)

    conv_2 = Conv2D(16, (3, 3), padding="same")(conv_2)
    conv_2 = BatchNormalization()(conv_2)
    conv_2 = Activation('relu')(conv_2)

    conv_2 = MaxPooling2D((2, 2))(conv_2)

    upsc_conv2 = UpSampling2D(size=(2, 2))(conv_2)
    # Conv 3
    conv_3 = Conv2D(32, (3, 3), name="conv3", padding="same")(conv_2)
    conv_3 = BatchNormalization()(conv_3)
    conv_3 = Activation('relu')(conv_3)

    conv_3 = Conv2D(32, (3, 3), padding="same")(conv_3)
    conv_3 = BatchNormalization()(conv_3)
    conv_3 = Activation('relu')(conv_3)

    conv_3 = MaxPooling2D((2, 2))(conv_3)

    upsc_conv3 = UpSampling2D(size=(4, 4))(conv_3)

    concated = concatenate([conv_1, upsc_conv2, upsc_conv3])

    # Conv 4
    conv_4 = Conv2D(56, (3, 3), padding="same")(concated)
    conv_4 = BatchNormalization()(conv_4)
    conv_4 = Activation('relu')(conv_4)

    conv_4 = Conv2D(2, (3, 3), padding="same")(conv_4)
    conv_4 = BatchNormalization()(conv_4)
    conv_4 = Activation('relu')(conv_4)

    nn_output = Softmax()(conv_4)

    model = Model(inputs=nn_input, outputs=nn_output, name='myModel')

    return model
