# mAP Evaluation Metric

## Evaluation  
The code takes ground truth boxes in the format of a dictionary of lists of boxes:  
###### {"filename1": [[xmin, ymin, xmax, ymax],...,[xmin, ymin, xmax, ymax]], "filename2": [...], ... }
  
  
Predicted boxes as a dictionary of a dictionary of boxes and scores like this:  
###### {'filename1': { 'boxes': [[xmin, ymin, xmax, ymax],...,[xmin, ymin, xmax, ymax]], 'scores': [score1,...,scoreN]}, 'filename2': { 'boxes': [[xmin, ymin, xmax, ymax],...,[xmin, ymin, xmax, ymax]], 'scores': [score1,...,scoreN]}, ... }  

To run calculate_mAP.py you mast add some arguments. Sample :  

python calculate_mAP.py "path to test annotation data file" "path to model output results file"  

For more information run python calculate_mAP.py -h


## Split to small, middle and large objects  
To split your main test dataset to small, middle and large objects, you can run splitObjects.py .  
To run splitObjects.py you must add some arguments. Sample :  

python splitObjects.py "small rate split number" "large rate split number" "path to test annotation data file" "path to model output results file" "path to train images"   

For more information run python splitObjects.py -h   

Script generate 6 json files which you can use in calculate_mAP.py script to calculate mAP metrix. 
