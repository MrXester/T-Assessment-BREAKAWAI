# Technical Assessment for Breakawai
### (Breakawai) Data Scientist Trainee - Technical Assessment
⚠ Made with Python 3.10 and SQLite3 ⚠


## Set Objectives
- Create an ETL script to prepare a dataset for analysis:
  - Join the 3 Procure-to-Pay CSV files into one dataset, ensuring the validity and quality of the data; (✅) \<2025-01-08\>
  - Add 2 new attributes to the dataset based on the Start Timestamp; (✅) \<2025-01-08\>
  - Add an extra attribute of the World Continent based on the country given. (✅) \<2025-01-09\>
  - Add a new dataset attribute to cluster the activities in phases, merging the dataset with the file "Phases_of_activities.csv" (✅) \<2025-01-09\>

- Create a Machine Learning script for adding value based on the existing transformed dataset:
  - Create an extra column in the dataset that clusters the data based multiple "unseen" patterns; (✅) \<2025-01-13\>
  - Explain the process and the decisions behind the machine learning techniques used to create this new column; (✅) \<2025-01-14\>
  - Present some visualization of the graphical clusters; (✅) \<2025-01-13\>

- Deadline \<2025-01-15\>

## Proposed Tasks
- Problem understanding:
  - Prepare Git (✅) \<2025-01-06\>
  - Define ETL tasks (✅) \<2025-01-08\>
  - Understand Data (✅) \<2025-01-07\>
  - Prepare ETL file hierarchy (✅) \<2025-01-06\>
  - Define ML tasks (✅) \<2025-01-10\>


- ETL pipeline:
  - Define an executor of commands in SQL (✅) \<2025-01-06\>
  - Define a Logger for the ETL process (✅) \<2025-01-06\>
  - Define a Config File Parser (✅) \<2025-01-07\>
  - Read CSVs (✅) \<2025-01-07\>
  
  - Add Atributes Quarter, Week, Continent (✅) \<2025-01-08\>
  - Validate Attributes, NAs, Duplicates, etc. (✅) \<2025-01-08\>
  
  - Clear CSV data (✅) \<2025-01-09\>
  - Define SQL Tables (✅) \<2025-01-09\>
  - Write SQL data (✅) \<2025-01-09\>
  - Merge Atributes and Cluster Phases (✅) \<2025-01-09\>


- ML Engineering:
  - Preprocess Data Types (✅) \<2025-01-10\>
  - Analyze Correlations (✅) \<2025-01-10\>
  - Reduce dimentionality and plot (✅) \<2025-01-10\>
  - Apply KMeans (❌) \<2025-01-10\>
  - Apply PCA (✅) \<2025-01-13\>
  - Apply KMeans (✅) \<2025-01-13\>
  - Analize Cluster (✅) \<2025-01-14\>
  - Explain Methods and Clusters (✅) \<2025-01-14\>

- Output:
  - Package Content (✅) \<2025-01-15\>

## Code Summary
- [Python](/02_Python) ⇒ Python Code folder with the ETL and ML files:

- [Aux Modules](/02_Python/auxiliary_modules) ⇒ Python Code with auxiliary scripts and functions

- [SQL](/03_SQL) ⇒ SQL queries and databases folder:

- [Data](/01_CSV) ⇒ Data folder with the required CSVs for execution and the output data;

- [Config](config.cfg) ⇒ Config file for global variables and adjustments to the script;

- [LOGS](/04_LOGS) ⇒ Logs produced by the script during execution;

- [LOGS](/05_IMAGES) ⇒ Output images produced by the script for cluster visualization;

- [Requirements](requirements.txt) ⇒ File with python packages requirements on the running system - "pip install -r requirements.txt" [Stack Overflow](https://stackoverflow.com/questions/7225900/how-can-i-install-packages-using-pip-according-to-the-requirements-txt-file-from);


## Results

- Main Output files will be on the CSV folder, folowing the name set at the config file +QN for quarter N;

- The scripts will also a DB file at the SQL folder;

- Images are resulting from the ML script, as well as an output csv with the Primary components variance;


## Legend
|xxxx-xx-xx| ↦ To be addressed at

\<xxxx-xx-xx\> ↦ Ended at

(🚩) ↦ TODO

(✅) ↦ Done

(❌) ↦ To be Reviewed




## Additional Resources

[Alpha3 to Country](https://www.kaggle.com/datasets/wbdill/country-codes-iso-3166) CSV by [Bdill](https://www.kaggle.com/wbdill) on Kaggle

[Country to Continent](https://www.kaggle.com/datasets/hserdaraltan/countries-by-continent) CSV by [Serdar Altan](https://www.kaggle.com/hserdaraltan) on kaggle
