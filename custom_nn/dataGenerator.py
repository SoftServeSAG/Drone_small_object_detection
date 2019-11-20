import os

import cv2
from keras.utils import Sequence
import numpy as np


class DataGenerator(Sequence):
    def __init__(self, root_dir=r'../data/val_test', image_folder='img/', mask_folder='mask/',
                 batch_size=1, image_size=(720, 1280), map_size = (180, 320), nb_y_features=2,
                 augmentation=None,
                 suffle=True):
        self.image_filenames = sorted(self.listdir_fullpath(os.path.join(root_dir, image_folder)))
        self.mask_names = sorted(self.listdir_fullpath(os.path.join(root_dir, mask_folder)))
        self.batch_size = batch_size
        self.augmentation = augmentation
        self.image_size = image_size
        self.map_size = map_size
        self.nb_y_features = nb_y_features
        self.shuffle = suffle

    def listdir_fullpath(self, d):
        return np.sort([os.path.join(d, f) for f in os.listdir(d)])

    def read_image_mask(self, file_img, file_mask):
        mask = np.empty((self.map_size[0], self.map_size[1], self.nb_y_features), dtype=np.float32)
        mask_component = cv2.extractChannel(cv2.imread(file_mask), 0)

        mask[..., 0] = cv2.normalize(mask_component, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
        mask[..., 1] = cv2.normalize(cv2.bitwise_not(mask_component), None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
        return cv2.imread(file_img), mask

    @staticmethod
    def shuffle_in_unison_scary(a, b):
        rng_state = np.random.get_state()
        np.random.shuffle(a)
        np.random.set_state(rng_state)
        np.random.shuffle(b)

    def on_epoch_end(self):
        self.shuffle_in_unison_scary(self.image_filenames, self.mask_names)

    def __len__(self):
        return int(np.floor(len(self.image_filenames) / self.batch_size))

    def __getitem__(self, index):
        data_index_min = int(index * self.batch_size)
        data_index_max = int(min((index + 1) * self.batch_size, len(self.image_filenames)))

        indexes = self.image_filenames[data_index_min:data_index_max]
        this_batch_size = len(indexes)  # The last batch can be smaller than the others

        X = np.empty((this_batch_size, self.image_size[0], self.image_size[1], 3), dtype=np.float32)
        y = np.empty((this_batch_size, self.map_size[0], self.map_size[1], self.nb_y_features), dtype=np.float32)

        for i, sample_index in enumerate(indexes):

            X_sample, y_sample = self.read_image_mask(self.image_filenames[index * self.batch_size + i],
                                                      self.mask_names[index * self.batch_size + i])

            # if augmentation is defined, we assume its a train set
            if self.augmentation is not None:

                # Augmentation code
                augmented = self.augmentation(self.image_size)(image=X_sample, mask=y_sample)
                image_augm = augmented['image']
                mask_augm = augmented['mask'].reshape(self.image_size, self.image_size, self.nb_y_features)
                # divide by 255 to normalize images from 0 to 1
                X[i, ...] = image_augm / 255
                y[i, ...] = mask_augm
            else:
                X[i, ...] = X_sample
                y[i, ...] = y_sample

        return X, y