# Centernet training pipeline

This is clone of original repo: https://github.com/xingyizhou/CenterNet

Original README: 
https://github.com/SoftServeSAG/Drone_small_object_detection/blob/centernet/models/CenterNet/README_original.md

# Short isntruction:
Put your annotations and images for training/validation in folder:
```
/data/coco/
```
IMPORTANT - preserve file namings

Run training:
```
python3 main.py ctdet --arch mobilenet  --batch_size 16 --gpus 0 --resume --num_epochs 2000
```

You can find training results and logs in directory:
```
/exp/ctdet/default
```
