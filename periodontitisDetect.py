import sys
import os
import sys
import random
import math
import numpy as np
import skimage.io
import matplotlib
import matplotlib.pyplot as plt
sys.path.append("/workspace/RoomDentist/periodontitisDetect")
from mrcnn import utils
import mrcnn.model as modellib
from mrcnn import visualize
from train_mask_rcnn import *

def detectionMaskFunction(imagePath, imageNum):
    weights = "/workspace/RoomDentist/mask_periodontitisDetect.h5"
    model,config = load_inference_model(1,weights)
    model.load_weights(weights, by_name=True)
    # Load a random image from the images folder
    image = skimage.io.imread(imagePath)
    class_names = ['plague'] * 100
    # Run detection
    results = model.detect([image], verbose=1)
    # Visualize results
    r = results[0]

    visualize.display_instances(image, r['rois'], r['masks'], r['class_ids'], class_names,imagePath, imageNum,r['scores'])

    return {'Cavity': 0, 'Gold': 0, 'Amalgam': 0, 'isCavity': "False"}