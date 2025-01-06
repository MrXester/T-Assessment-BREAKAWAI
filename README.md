# Technical Assessment for Breakawai
##(Breakawai) Data Scientist Trainee - Technical Assessment

### Set Objectives
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

### Proposed Tasks

- ETL pipeline:

- ML Engineering:

### Code Summary
[Python]() ⇒ Python Code folder with the ETL and ML files:
  - [ETL]() → ETL pipeline designed for Main Objective 1;
  - [Models]() → ETL pipeline designed for Main Objective 2;
  - [Visualization]() → Data visualization and Model explanation;

[SQL]() ⇒ SQL queries folder:
  - [Queries]() → SQL queries used as auxiliary methods to the [ETL]() pipeline;

[Data]() ⇒ Data folder with the required CSVs for execution;

[Config]() ⇒ Config file for global variables and adjustments to the script;
