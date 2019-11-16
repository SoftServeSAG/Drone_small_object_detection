from albumentations import (
    GaussNoise,
    IAASharpen,
    RandomShadow,
    IAAEmboss,
    MedianBlur,
    Flip,
    RGBShift,
    HueSaturationValue,
    Compose,
    ElasticTransform,
    OpticalDistortion,
    ShiftScaleRotate,
    OneOf,
    CLAHE,
    RandomBrightnessContrast,
    RandomGamma,
    RandomCrop
)

# Define image size
original_height, original_width = 1280, 720

aug = Compose([
               ShiftScaleRotate(shift_limit=0.0, scale_limit=0.2,
                                rotate_limit=35, p=.4),
               OpticalDistortion(),
               ElasticTransform(),
               GaussNoise(),
               RandomShadow(),
               OneOf([

                   CLAHE(clip_limit=2),
                   IAASharpen(),
                   IAAEmboss(),
                   RandomBrightnessContrast(),
                   RandomGamma(),
                   MedianBlur()
               ], p=0.5),
               OneOf([
                   RGBShift(),
                   HueSaturationValue(),
               ], p=0.5),
               RandomCrop(p=1, height=original_height / 4, width=original_width / 4)])

# Input image/mask - Getting augmented results
augmented = aug(image=image, mask=mask)
