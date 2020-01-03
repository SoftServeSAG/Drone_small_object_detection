# Tools

1. **OpenVino_result.py** - script to get bounding boxes and scores from OpenVino model and save this metrix to json file.

	Options:  
	  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -h, --help            Show this help message and exit.  
	  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-m MODEL, --model MODEL  
		                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Required. Path to an .xml file with a trained model.  
	 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -i INPUT, --input INPUT  
		                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Required. Path to video file or image. 'cam' for  
		               &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; capturing video stream from camera  
	 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -l CPU_EXTENSION, --cpu_extension CPU_EXTENSION  
		                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Optional. Required for CPU custom layers. Absolute  
		                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;path to a shared library with the kernels  
		              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  implementations.  
	 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -pp PLUGIN_DIR, --plugin_dir PLUGIN_DIR  
		              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  Optional. Path to a plugin folder  
	 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -d DEVICE, --device DEVICE  
		              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  Optional. Specify the target device to infer on; CPU,  
		              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  GPU, FPGA, HDDL or MYRIAD is acceptable. The demo will  
		              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  look for a suitable plugin for device specified.   
		              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  Default value is CPU  
	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  --labels LABELS       Optional. Path to labels mapping file  
	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  -pt PROB_THRESHOLD, --prob_threshold PROB_THRESHOLD  
		              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  Optional. Probability threshold for detections  
		              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  filtering 
			      
2. **augmentation_config.py** - augmentation configuration file for using with [albumentation](https://github.com/albumentations-team/albumentations)

Example of using: 

```python
aug = Compose(/* different augmentations */)
augmented = aug(image=image, mask=mask)
```
3. **augmentation_config.py** - Python script for dividing overall dataset into 2 parts (**TRAIN, VALIDATION**). 

INPUT: folder with `'MASKS', 'FRAMES', 'JSONS'` subfolders

OUTPUT: created subfolders `'train_frames', 'train_masks', 'train_json', 'val_frames', 'val_masks', 'val_json'`


4. **download_from_LabelBox.py** - script to get masks from LabelBox tool and create json anotation. Need two required argument:  
--folder - "Required. Path to folder where will save masks.";  
--input - "Required. Path to csv annotation file.";  

 Warning !!! Works for only one object class.
