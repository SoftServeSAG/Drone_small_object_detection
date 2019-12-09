# Tools

1. OpenVino_result.py - script to get bounding boxes and scores from OpenVino model and save this metrix to json file.

	Options:
	  -h, --help            Show this help message and exit.
	  -m MODEL, --model MODEL
		                Required. Path to an .xml file with a trained model.
	  -i INPUT, --input INPUT
		                Required. Path to video file or image. 'cam' for
		                capturing video stream from camera
	  -l CPU_EXTENSION, --cpu_extension CPU_EXTENSION
		                Optional. Required for CPU custom layers. Absolute
		                path to a shared library with the kernels
		                implementations.
	  -pp PLUGIN_DIR, --plugin_dir PLUGIN_DIR
		                Optional. Path to a plugin folder
	  -d DEVICE, --device DEVICE
		                Optional. Specify the target device to infer on; CPU,
		                GPU, FPGA, HDDL or MYRIAD is acceptable. The demo will
		                look for a suitable plugin for device specified. 
		                Default value is CPU
	  --labels LABELS       Optional. Path to labels mapping file
	  -pt PROB_THRESHOLD, --prob_threshold PROB_THRESHOLD
		                Optional. Probability threshold for detections
		                filtering
