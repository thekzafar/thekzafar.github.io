import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# read data
datafile = "air_data.csv"
data = pd.read_csv(datafile, encoding="ANSI")
print(data.shape)
print(data.head())
data.describe().transpose()

# the one columns about  LOAD_TIME
# only the type is: Standard time types that pandas can handle
# time in pandas---
time_gap = pd.to_datetime(data["LOAD_TIME"]) - pd.to_datetime(data["FFP_DATE"])
time_gap = time_gap / pd.Timedelta(days=30)
print(type(time_gap))
print(time_gap.head(5))

feature = data[["LAST_TO_END", "FLIGHT_COUNT", "SEG_KM_SUM", "avg_discount"]].copy()
# change the columns info
feature.columns = ["R", "F", "M", "C"]
feature["L"] = time_gap.values
print("*" * 70)
feature = feature[["L", "R", "F", "M", "C"]]
print(data.columns)
print(feature)

# find mean count etc
feature_summary = feature.describe(percentiles=[], include='all')
print(feature_summary)

# standardize
feature = (feature - feature.mean(axis=0)) / (feature.std(axis=0))
print(feature.head())


k = 5
x = feature[['L', 'R', 'F', 'M', 'C']]
kms = KMeans(n_clusters=k)
kms.fit(x)  # training model
print('Cluster centers:', kms.cluster_centers_)
print('Category:', kms.labels_)
r1 = pd.Series(kms.labels_)
r1 = r1.value_counts()
r2 = pd.DataFrame(kms.cluster_centers_)
r = pd.concat([r2, r1], axis=1)
r.columns = [u'number of clusters', u'R', u'F', u'M', u'C', u'L']
r.index.name = 'Clustering category'
r.index = ([u'Customer Group 1', u'Customer Group 2', u'Customer Group 3', u'Customer Group 4', u'Customer Group 5'])

# Plot chart
labels = r.columns
plot_data = kms.cluster_centers_
color = ['b', 'g', 'r', 'c', 'y']
angles = np.linspace(0, 2*np.pi, k, endpoint=False)
plot_data = np.concatenate((plot_data, plot_data[:, [0]]), axis=1)
angles = np.concatenate((angles, [angles[0]]))
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, polar=True)  # polar parameter
for i in range(len(plot_data)):
    ax.plot(angles, plot_data[i], 'bo-', color=color[i], label=r.index[i], linewidth=2)
    ax.set_thetagrids(angles * 180/np.pi, labels)
plt.legend(loc=1)
plt.show()
