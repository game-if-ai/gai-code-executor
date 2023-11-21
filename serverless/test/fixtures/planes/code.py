#
# This software is Copyright ©️ 2020 The University of Southern California. All Rights Reserved.
# Permission to use, copy, modify, and distribute this software and its documentation for educational, research and non-profit purposes, without fee, and without a written agreement is hereby granted, provided that the above copyright notice and subject to the full license file found in the root of this software deliverable. Permission to make commercial use of this software may be obtained by contacting:  USC Stevens Center for Innovation University of Southern California 1150 S. Olive Street, Suite 2300, Los Angeles, CA 90115, USA Email: accounting@stevens.usc.edu
#
# The full terms of this copyright and license should always be found in the root directory of this software deliverable as "license.txt" and if these terms are not found with this software, please contact the USC Stevens Center for the full license.
#

### This cell is uneditable ###
import json
from test_utils import fixture_path
import os

# Build a network with
#  convolution layer 1 having "filters1" filters
#  convolution layer 2 having "filters2" filters
#  convolution layer 3 having "filters3" filters or None to remove
#  fully connected layer of neurons with "layer4" neurons
#  fully connected layer of neurons with "layer5" neurons
#
# PICK ONE
# setting_name = "large"
#         "filters1": 50
#         "filters2": 75
#         "filters3": 100
#         "layer4": 500
#         "layer5": 250
# setting_name = "medium"
#         "filters1": 25
#         "filters2": 50
#         "filters3": 75
#         "layer4": 250
#         "layer5": 100
# setting_name = "small"
#         "filters1": 25
#         "filters2": 25
#         "filters3": 25
#         "layer4": 125
#         "layer5": 50
# setting_name = "tiny"
#         "filters1": 25
#         "filters2": 25
#         "filters3": None
#         "layer4": 75
#         "layer5": 25

labels = ["plane", "car", "tank"]

# possible values: tiny, small, medium or large
setting_name = "tiny"
# possible values: 30 or 60
training_epochs = 30

### This cell is uneditable ###
if training_epochs != 30 and training_epochs != 60:
    raise Exception("training_epochs must be 30 or 60")
if setting_name not in ["tiny", "small", "medium", "large"]:
    raise Exception("invalid valid for settings_name")

prefix = os.path.join(
    fixture_path("planes"), "Epoch" + str(training_epochs) + "_" + setting_name + "_"
)
# LOAD ACCURACY DATA and PREDICTIONS
with open(prefix + "accuracy.json") as IN:
    plot_dict = json.load(IN)

with open(prefix + "predictions.json") as IN:
    predictions_dict = json.load(IN)

    y_pred_test = predictions_dict["y_pred_test"]
    y_proba = predictions_dict["y_proba"]


import random
import numpy as np

experiment = []
# 0: airplane, 1: automobile, 2: tank.
choices = [0, 1, 2]
cat0 = 0
cat1 = 100
cat2 = 200
for i in range(len(y_pred_test)):
    c = random.choice(choices)
    if not (choices):
        raise Exception("ERROR: generating test data")
    if c == 0:
        filename = "airplane_" + str(cat0) + ".png"
        y_true = 0
        pred = int(y_pred_test[cat0])
        prob = float(y_proba[cat0])
        cat0 += 1
        if cat0 >= 100:
            choices.remove(0)
    elif c == 1:
        filename = "automobile_" + str(cat1) + ".png"
        y_true = 1
        pred = int(y_pred_test[cat1])
        prob = float(y_proba[cat1])
        cat1 += 1
        if cat1 >= 200:
            choices.remove(1)
    else:
        filename = "tank_" + str(cat2) + ".png"
        y_true = 2
        pred = int(y_pred_test[cat2])
        prob = float(y_proba[cat2])
        cat2 += 1
        if cat2 >= 300:
            choices.remove(2)
    experiment.append(
        {
            "realLabel": labels[y_true],
            "classifierLabel": labels[pred],
            "confidence": prob,
        }
    )
output = np.array_split(experiment, 5)

result = "planes completed"
