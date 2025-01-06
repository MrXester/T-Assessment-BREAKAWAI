# Technical Assessment for Breakawai
### (Breakawai) Data Scientist Trainee - Technical Assessment
⚠ Made with Python 3.10 and SQLite3 ⚠



## Set Objectives
- Create an ETL script to prepare a dataset for analysis:
  - Join the 3 Procure-to-Pay CSV files into one dataset, ensuring the validity and quality of the data; (🚩) <>
  - Add 2 new attributes to the dataset based on the Start Timestamp; (🚩) <>
  - Add an extra attribute of the World Continent based on the country given. (🚩) <>
  - Add a new dataset attribute to cluster the activities in phases, merging the dataset with the file "Phases_of_activities.csv" (🚩) <>

- Create a Machine Learning script for adding value based on the existing transformed dataset:
  - Create an extra column in the dataset that clusters the data based multiple "unseen" patterns; (🚩) <>
  - Explain the process and the decisions behind the machine learning techniques used to create this new column; (🚩) <>
  - Present some visualization of the graphical clusters; (🚩) <>

- Deadline <2025-01-15>

## Proposed Tasks
- Problem understanding:
  - Prepare Git |2025-01-06|
  - Define tasks |2025-01-06|
  - Understand Data |2025-01-06|
  - Prepare file hierarchy |2025-01-06|

- ETL pipeline:

- ML Engineering:

## Code Summary
- [Python](/02_Python) ⇒ Python Code folder with the ETL and ML files:
  - [ETL](/02_Python/script_1_ETL.py) → ETL pipeline designed for Main Objective 1;
  - [Models](/02_Python/script_2_ML.py) → ML models designed for Main Objective 2;
  - [Visualization]() → Data visualization and Model explanation;


- [Aux Modules](/02_Python/auxiliary_modules) ⇒ Python Code with auxiliary scripts and functions:

- [SQL](/03_SQL) ⇒ SQL queries folder:
  - [Queries]() → SQL queries used as auxiliary methods to the [ETL]() pipeline;

- [Data](/01_CSV) ⇒ Data folder with the required CSVs for execution;

- [Config](config.cfg) ⇒ Config file for global variables and adjustments to the script;

- [Requirements](requirements.txt) ⇒ File with python packages requirements on the running system - "pip install -r requirements.txt" [Stack Overflow](https://stackoverflow.com/questions/7225900/how-can-i-install-packages-using-pip-according-to-the-requirements-txt-file-from);


## Legend
|xxxx-xx-xx| ↦ To be addressed at
\<xxxx-xx-xx\> ↦ Ended at
(🚩) ↦ TODO
(✅) ↦ Done
(❌) ↦ To be Reviewed
