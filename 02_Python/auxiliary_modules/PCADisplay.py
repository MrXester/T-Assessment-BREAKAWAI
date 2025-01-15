from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import pandas as pd

class PCADisplay(PCA):
	def get_pca_values(self,data, components_to_select):
		self.transformed_values = self.fit_transform(data)
		return self.transformed_values.copy()[:,:components_to_select]


	def get_components_variance(self,columns_to_use, fileName=None):
		total_components = self.transformed_values.shape[1]
		self.df_comp = pd.DataFrame(
			self.components_,
			columns=columns_to_use,
			index=[f"Component {x}" for x in range(total_components)]
		)

		self.df_comp['Explained Variance'] = self.explained_variance_ratio_
		if fileName is not None:
			self.df_comp.to_csv(fileName)
		
		return self.df_comp.copy()


	def elbow_plot(self,fileName, components_to_select):
		total_components = self.transformed_values.shape[1]
		elbow_variance = self.df_comp["Explained Variance"].iloc[components_to_select - 1]
		plt.figure(figsize=(8, 6))
		plt.plot(range(total_components), self.df_comp["Explained Variance"], marker='o', linestyle='--')
		plt.axhline(y=elbow_variance, color='r', linestyle='--', label=f'Elbow Threshold = {elbow_variance:.2f}')
		plt.title("Elbow Plot for PCA")
		plt.xlabel("Number of Principal Components")
		plt.ylabel("Explained Variance")
		plt.grid(True)
		plt.savefig(fileName)
		pass



	def cluster_plot(self,components_to_select, clusters, fileName):
		explained_variance = self.explained_variance_ratio_
		fig, axes = plt.subplots(components_to_select, components_to_select, figsize=(15, 15))
		for i in range(components_to_select):
			for j in range(components_to_select):
				ax = axes[i, j]
				if i != j:
					ax.scatter(self.transformed_values[:, j], self.transformed_values[:, i], marker=".", c=clusters, cmap='viridis', alpha=0.7)
					ax.set_xlabel(f"Comp {j} ({explained_variance[j]:.2f})")
					ax.set_ylabel(f"Comp {i} ({explained_variance[i]:.2f})")

				ax.tick_params(axis='both', which='both', length=0)
		plt.tight_layout()
		plt.savefig(fileName)
		pass
