#
# This software is Copyright ©️ 2020 The University of Southern California. All Rights Reserved.
# Permission to use, copy, modify, and distribute this software and its documentation for educational, research and non-profit purposes, without fee, and without a written agreement is hereby granted, provided that the above copyright notice and subject to the full license file found in the root of this software deliverable. Permission to make commercial use of this software may be obtained by contacting:  USC Stevens Center for Innovation University of Southern California 1150 S. Olive Street, Suite 2300, Los Angeles, CA 90115, USA Email: accounting@stevens.usc.edu
#
# The full terms of this copyright and license should always be found in the root directory of this software deliverable as "license.txt" and if these terms are not found with this software, please contact the USC Stevens Center for the full license.
#
### This cell is uneditable ###
import json, random
import numpy as np
from sklearn.model_selection import train_test_split
from test_utils import fixture_path
import os

# load fruit data:
fruit_traits = ["fruit", "color", "shape"]
fruits_file = open(os.path.join(fixture_path("fruitpicker"), "fruits.json"))
fruits = json.load(fruits_file)

# split into training and testing data
random.shuffle(fruits)
training_data, testing_data = train_test_split(fruits)

# split testing data into 5 simulation runs
inputs = []
for x in range(0, 5):
    run = []
    label = random.choice(fruit_traits)
    random.shuffle(testing_data)
    for fruit in testing_data:
        run.append({"label": label, "fruit": fruit})
    inputs.append(run)


# Your training code goes here:
def train():
    print("do something")


# Your classifier code goes here:
def classify(fruit, label):
    correctAnswer = random.randint(1, 10) < 5
    output = {
        "fruit": fruit,
        "label": label,
        "inputText": fruit["description"],
        "realLabel": fruit["traits"][label],
        "classifierLabel": fruit["traits"][label]
        if correctAnswer
        else fruits[random.randint(0, len(fruits) - 1)]["traits"][label],
        "confidence": random.uniform(0, 1),
    }
    return output


### This cell is uneditable ###

outputs = []
for run in inputs:
    output = []
    for fruit in run:
        output.append(classify(fruit.get("fruit"), fruit.get("label")))
    outputs.append(output)


result = "fruitpicker completes"
