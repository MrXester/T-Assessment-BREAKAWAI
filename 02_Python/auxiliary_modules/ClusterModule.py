from sklearn.cluster import KMeans
from sklearn.tree import DecisionTreeClassifier, plot_tree
import matplotlib.pyplot as plt



class Clustering_Module(object):
	def __init__(self, n_clusters=3,max_depth=3, random_state=42):
		self.random_state = random_state
		self.kmeans = KMeans(n_clusters=n_clusters, random_state=self.random_state)
		self.DT = DecisionTreeClassifier(max_depth=max_depth, random_state=self.random_state)

	def fit_cluster(self,data):
		self.clusters = self.kmeans.fit_predict(data)
		return self.clusters.copy()

	def display_Decision_tree(self,data, feature_names,filename):
		self.DT.fit(data, self.clusters)

		plt.figure(figsize=(30, 15))
		plot_tree(
			self.DT,
			feature_names=feature_names,
			class_names=[str(c) for c in self.DT.classes_], 
			filled=True,
			fontsize=14
		)
		plt.title("Decision Tree Cluster Visualization")
		plt.savefig(filename)
		pass
		

