import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from auxiliary_modules.PCADisplay import PCADisplay
from auxiliary_modules.ClusterModule import Clustering_Module
from auxiliary_modules.Config_File import Config
from auxiliary_modules.Custom_Logger import Logging_System
import matplotlib.pyplot as plt
import seaborn as sns

# Script kickstart
CONFIG_PATH = "../config.cfg"
CONFIG = Config(CONFIG_PATH)
LOGGER = Logging_System(CONFIG.get_log_file("log_file"),"ML_logger")
RANDOMSTT = CONFIG.get_option_cast("random_state",int)
in_file = CONFIG.get_csv_file("intermediary_csv_file")
components_to_select = CONFIG.get_option_cast("pca_components",int)
n_clusters = CONFIG.get_option_cast("clusters",int)
max_depth = CONFIG.get_option_cast("dtree_max_depth",int)


@LOGGER.wrap_log("Adding Calculated attributes to DataFrame","Attributes Added","Failed to Add Data",None)
def add_calculated_attributes(data):
	data["Start Timestamp"] = pd.to_datetime(data['Start Timestamp'], format="%Y-%m-%d %H:%M:%S")
	data["Complete Timestamp"] = pd.to_datetime(data['Complete Timestamp'], format="%Y-%m-%d %H:%M:%S")
	data["Time to Complete"] = ((data["Complete Timestamp"] - data["Start Timestamp"]).dt.total_seconds() // 60).astype(int)
	data['Discount Percentage'] = (data['Discount'] / data['Invoice amount']) * 100
	data["Days from start"] = (data["Start Timestamp"] - data["Start Timestamp"].min()).dt.days
	data['Phase'] = data['Phase'].str.replace("Phase ","").astype(int)
	data['Quarter'] = data['Quarter'].str.replace("Q","").astype(int)
	return data


@LOGGER.wrap_log("Processing Categorical Data","One Hot Encoded Categorical Data","Failed to Process Data",None)
def process_categorical_columns(data,columns_to_encode):
	encoder = OneHotEncoder(sparse_output=False)
	encoded_data = encoder.fit_transform(data[columns_to_encode])
	encoded_columns = encoder.get_feature_names_out(columns_to_encode)
	encoded_df = pd.DataFrame(encoded_data, columns=encoded_columns, index=data.index)
	data_encoded = pd.concat([data.drop(columns=columns_to_encode), encoded_df], axis=1)
	return data_encoded



@LOGGER.wrap_log("Normalizing Data","Data Normalized","Failed to Normalize Data",None)
def normalize_data(data):
	scaler = StandardScaler()
	normalized_data = scaler.fit_transform(data)
	return normalized_data



def export_correlation(data, fileName):
	df = data[['Invoice amount', 'Discount', 'Quarter', 'Week', 'Phase',
       'Time to Complete', 'Discount Percentage', 'Days from start',
       'Role_Financial Manager', 'Role_Purchasing Agent', 'Role_Requester',
       'Role_Requester Manager', 'Role_Supplier', 'Country_AUS', 'Country_JPN',
       'Country_NZL', 'Country_SGP', 'Continent_Asia', 'Continent_Oceania']]
	corr_matrix = df.corr()
	plt.figure(figsize=(10, 8))
	heatmap = sns.heatmap(
		corr_matrix,
		cbar=True
	)
	plt.title('Correlation Heatmap', fontsize=16)
	plt.savefig(fileName, dpi=300, bbox_inches='tight')
	plt.close()
	pass


@LOGGER.wrap_log("Running ML scripts for clustering","Script Successfull","Failed to Run Script",None)
def ML_pipeline(columns_to_encode,columns_to_use,in_file):
	df = pd.read_csv(in_file)
	data = df.copy()
	data = add_calculated_attributes(data)
	data = process_categorical_columns(data,columns_to_encode)
	export_correlation(data, CONFIG.get_image_file("Correlation_Matrix"))
	data = data[columns_to_use]
	data = normalize_data(data)
	
	PCA = PCADisplay(n_components=len(columns_to_use))
	pca_values = PCA.get_pca_values(data,components_to_select)
	PCA.get_components_variance(columns_to_use,fileName=CONFIG.csv_file_factory("out-PCA-variance"))
	
	elbow_file = CONFIG.get_image_file("elbow_plot")
	PCA.elbow_plot(elbow_file, components_to_select)

	clusterer = Clustering_Module(n_clusters=n_clusters,max_depth=max_depth, random_state=RANDOMSTT)
	clusters = clusterer.fit_cluster(pca_values)

	
	pca_display_file = CONFIG.get_image_file("PCA_plot")
	PCA.cluster_plot(components_to_select, clusters, pca_display_file)

	dtree_display_file = CONFIG.get_image_file("Decision_tree_plot")
	clusterer.display_Decision_tree(data, columns_to_use,dtree_display_file)

	df['Time and Value Cluster'] = clusters
	quarters = CONFIG.get_option_cast("quarters_to_output",parse_list)
	output_csv(df,quarters)



def output_csv(ref_data,quarters):
	for quarter in quarters:
		path = CONFIG.output_files_factory(quarter)
		ref_data[ref_data["Quarter"] == quarter].to_csv(path,index=False)
	pass

def parse_list(value):
	items = [item.strip() for item in value.strip("[]").split(",")]
	return items




if __name__ == '__main__':
	columns_to_encode = ['Role', 'Country', 'Continent']
	columns_to_use = [
		'Days from start', 'Invoice amount','Phase',
		'Time to Complete', 'Discount Percentage'
	]
	ML_pipeline(columns_to_encode,columns_to_use,in_file)

