#
# This software is Copyright ©️ 2020 The University of Southern California. All Rights Reserved.
# Permission to use, copy, modify, and distribute this software and its documentation for educational, research and non-profit purposes, without fee, and without a written agreement is hereby granted, provided that the above copyright notice and subject to the full license file found in the root of this software deliverable. Permission to make commercial use of this software may be obtained by contacting:  USC Stevens Center for Innovation University of Southern California 1150 S. Olive Street, Suite 2300, Los Angeles, CA 90115, USA Email: accounting@stevens.usc.edu
#
# The full terms of this copyright and license should always be found in the root directory of this software deliverable as "license.txt" and if these terms are not found with this software, please contact the USC Stevens Center for the full license.
#
import pandas as pd
import os
import json
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from test_utils import fixture_path


# SETUP
def cluster(wineData_scaled, n_clusters):
    model = KMeans(n_clusters=n_clusters, n_init="auto", random_state=2023)
    model.fit(wineData_scaled)
    return model


# MODEL
def preprocess(wineDataFrame):
    # 1. drop "Wine" column which just assigns a number (1, 2, ...) to each wine
    # It is okay to modify wineDataFrame
    wineDataFrame.drop("Wine", axis=1, inplace=True)

    # 2. split into data and labels. It is okay to modify wineDataFrame.
    quality = wineDataFrame["quality"]
    wineDataFrame.drop("quality", axis=1, inplace=True)

    # 3. scale data but don't overwrite raw data
    # 4. return data and labels
    scaler = StandardScaler()
    scaler.fit(wineDataFrame)
    return (
        pd.DataFrame(scaler.transform(wineDataFrame), columns=wineDataFrame.columns),
        quality,
    )


wineData_raw = pd.read_csv(os.path.join(fixture_path("wine"), "wineQualityReds.csv"))
wineData_scaled, quality = preprocess(wineData_raw)
k = 6
model = cluster(wineData_scaled, k)

# VALIDATION
wineData_scaled["Cluster"] = pd.Series(model.predict(wineData_scaled))
wineData_scaled["quality"] = quality
quality_means = []
Ns = []
for i in range(k):
    cluster_df = wineData_scaled[wineData_scaled["Cluster"] == i]
    quality_means.append(cluster_df["quality"].mean())
    Ns.append(cluster_df.shape[0])
quality_df = pd.DataFrame({"quality": quality_means, "N": Ns})
quality_df.sort_values("quality", ascending=True, inplace=True)
print(quality_df)
result = "result"
