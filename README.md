# mAP Evaluation Metric
The code takes ground truth boxes in the format of a dictionary of lists of boxes:  
###### {"filename1": [[xmin, ymin, xmax, ymax],...,[xmin, ymin, xmax, ymax]], "filename2": [...], ... }
  
  
Predicted boxes as a dictionary of a dictionary of boxes and scores like this:  

###### {'filename1': { 'boxes': [[xmin, ymin, xmax, ymax],...,[xmin, ymin, xmax, ymax]], 'scores': [score1,...,scoreN]}, 'filename2': { 'boxes': [[xmin, ymin, xmax, ymax],...,[xmin, ymin, xmax, ymax]], 'scores': [score1,...,scoreN]}, ... }
