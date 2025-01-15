from auxiliary_modules.Custom_Logger import Logging_System
from auxiliary_modules.ExecuteSQL import SQL_executor
from auxiliary_modules.Exceptions import *
from auxiliary_modules.Config_File import Config
import pandas as pd
import numpy as np
from datetime import datetime
from Levenshtein import distance as levenshtein_distance
import sqlite3
import json

# Script kickstart
CONFIG_PATH = "../config.cfg"
CONFIG = Config(CONFIG_PATH)
LOGGER = Logging_System(CONFIG.get_log_file("log_file"),"ETL_logger")
in_files = CONFIG.input_files()
LOGGER.info(f"Detected files for input: {[x for x in in_files]}")




# Read Data
def read_ISO():
	global CONFIG
	csv_ISO_codes = CONFIG.get_csv_file("iso_codes")
	df_iso = pd.read_csv(csv_ISO_codes,encoding ="ISO-8859-1")[["iso3","country_common"]]
	df_iso.columns = ["Iso3","Country"]
	return df_iso



def read_Continents():
	global CONFIG
	csv_continents = CONFIG.get_csv_file("continents")
	df_continent = pd.read_csv(csv_continents)
	df_continent.columns = ["Continent","Country"]
	return df_continent



def read_Phases():
	global CONFIG
	csv_activities = CONFIG.get_csv_file("activities")
	df_act = pd.read_csv(csv_activities, delimiter=";")
	return df_act



def read_inputs():
	global CONFIG
	input_files = CONFIG.input_files()
	input_csvs = []
	for input_csv_path in input_files:
		input_csvs.append(read_csv(input_csv_path))
	ref_data = pd.concat(input_csvs)
	ref_data = ref_data.reset_index(drop=True)
	return ref_data



def read_csv(input_csv_path):
	with open(input_csv_path, 'r') as file:
		content = file.readlines()
		columns = content.pop(0)[:-1].split(',')
		line_number = 1
		values = []
		for line in content:
			row = line[:-1].split(',')
			line_number += 1
			
			if len(row) > len(columns):
				merged_value = [row[-4],f"{row[-3]}.{row[-2]}",row[-1]]
				row = row[:-4] + merged_value

			if len(row) < len(columns):
				continue

			values.append(row)
		ref_data = pd.DataFrame(columns=columns,data=values)
	return ref_data



# ==================== Data Validation ====================
# Validate coherence values
def log_validation(func):
	validation_override = func.__name__[len("validate_"):]
	if validation_override is not None:
		validation_name = validation_override

	def wrapper(data,*args, **kwargs):
		@LOGGER.wrap_log(f"Validating {validation_name}...", f"{validation_name} Validated!", f"FAILED the {validation_name} Validation",np.ones(data.shape[0]).astype(bool))
		def inner_func(data,*args, **kwargs):
			return func(data,*args, **kwargs)
		
		validated_results = inner_func(data,*args, **kwargs)
		false_count = np.sum(~validated_results)
		LOGGER.info(f"Detected {false_count} Rows with invalid {validation_name}")
		if false_count > 0:
			LOGGER.info(f"Detected Lines:")
			for row in data[~validated_results].iterrows():
				LOGGER.info(f"\n{row}\n")
		return validated_results
	return wrapper


@log_validation
def validate_timestamp_order(ref_data):
	return ref_data["Start Timestamp"] <= ref_data['Complete Timestamp']

@log_validation
def validate_discount_value(ref_data):
	return ref_data["Discount"] < ref_data["Invoice amount"]

@log_validation
def validate_duplicates(ref_data):
	return ~ref_data.duplicated(subset=ref_data.columns, keep="first")

@log_validation
def validate_missing(ref_data):
	return ~ref_data.isnull().any(axis=1)

@log_validation
def validate_activity(ref_data,phases):
	return ref_data['Activity'].isin(phases['Activity'])


def iso_match_levenshtein(row_wrong_code,ISO_codes):
	if not row_wrong_code or pd.isna(row_wrong_code):
		return None, False
	closest_code = None
	closest_distance = float('inf')
	for code in ISO_codes['Iso3']:
		dist = levenshtein_distance(row_wrong_code, code)
		if dist < closest_distance:
			closest_distance = dist
			closest_code = code
	if closest_distance > 2:
		return None, True
	return closest_code,True


@log_validation
def validate_country_ISO(ref_data,ISO_data):
	return ref_data['Country'].isin(ISO_data['Iso3'])


@LOGGER.wrap_log("Trying to fit imputation Data","Data Imputed","Failed to imputate Data",None)
def process_iso_codes(ref_data, validation, ISO_data):
	for index,row in ref_data.loc[~validation, ['Country']].iterrows():
		match_code,has_match = iso_match_levenshtein(row['Country'],ISO_data)
		if has_match:
			before_imput = row['Country']
			ref_data.loc[int(index),'Country'] = match_code
			validation[index] = True
			LOGGER.info(f"Found a match for line {index} - Changing [{before_imput}]  to [{ref_data.loc[int(index),'Country']}]")
	
	return ref_data




def validate_semantics(ref_data,phases):
	return np.logical_and.reduce([validate_missing(ref_data),
	validate_timestamp_order(ref_data),
	validate_discount_value(ref_data),
	validate_activity(ref_data,phases),
	validate_duplicates(ref_data),
	])


# validate string formats
def validate_timestamp_format(column):
	return column.str.match(r"^\d{2}\/\d{2}\/\d{4} \d{2}:\d{2}:\d{2}")

def validate_float_format(column):
	return column.str.match(r"^[\d]+.[\d]+")

def validate_int_format(column):
	return column.str.match(r"^[\d]+")

@log_validation
def validate_formats(df):
	numbers =  validate_int_format(df["Case ID"]) &  validate_float_format(df["Invoice amount"]) & validate_float_format(df["Discount"])
	timestamps = validate_timestamp_format(df["Start Timestamp"]) & validate_timestamp_format(df["Complete Timestamp"])
	return numbers & timestamps




# ==================== Transform ====================
def strip_columns(ref_data):
	for column in ref_data.columns:
		if ref_data[column].dtype == "object":
			ref_data[column] = ref_data[column].str.strip()
	return ref_data

def add_timestamps_atributes(ref_data):
	ref_data["Quarter"] = 'Q' + ref_data['Start Timestamp'].dt.quarter.astype(str)
	ref_data["Week"] = ref_data['Start Timestamp'].dt.isocalendar().week
	return ref_data

def data_conversion(ref_data):
	ref_data["Start Timestamp"] = pd.to_datetime(ref_data['Start Timestamp'], format="%d/%m/%Y %H:%M:%S")
	ref_data["Complete Timestamp"] = pd.to_datetime(ref_data['Complete Timestamp'], format="%d/%m/%Y %H:%M:%S")	
	ref_data["Discount"] = ref_data["Discount"].astype(float)
	ref_data["Invoice amount"] = ref_data["Invoice amount"].astype(float)
	ref_data["Case ID"] = ref_data["Case ID"].astype(int)
	return ref_data




# To SQL
@LOGGER.wrap_log("Starting DB Connection","DB Connection successfull","Failed to connect to DB",None)
def create_SQL_manager():
	global CONFIG
	sql_files = CONFIG.SQL_SCRIPTS
	db_file = CONFIG.get_db_file()
	db_connection = sqlite3.connect(db_file)

	sql_exec = SQL_executor(sql_files,db_connection)
	LOGGER.info(f"SQL scripts detected: {sql_files}")
	LOGGER.info(f"SQL commands: {sql_exec.commands}")
	sql_exec.connect()
	return sql_exec,db_connection


@LOGGER.wrap_log("Kickstart SQL Structure","SQL Structure initialized","Failed to initialize SQL",None)
def SQL_kickstart(sql_manager,db_connection,ISO_data, continents_data, phases_data):
	sql_manager.execute("create iso table")
	sql_manager.execute("create continents table")
	sql_manager.execute("create phases table")
	sql_manager.execute("create main table")

	ISO_data.to_sql("ISOCodes", db_connection, if_exists="append", index=False)
	continents_data.to_sql("Continents", db_connection, if_exists="append", index=False)
	phases_data.to_sql("Phases", db_connection, if_exists="append", index=False)
	return


@LOGGER.wrap_log("Inputing Main Data into DB table","Input Sucessfull","Failed to Execute Input",None)
def data_to_SQL(db_connection,ref_data):
	ref_data.to_sql("ProcureToPay", db_connection, if_exists="append", index=False)
	return


@LOGGER.wrap_log("Joining Tables","Information retrieved","Failed to Execute Join",None)
def get_joint_table(sql_manager,db_connection):
	query = sql_manager.get_command("Join Info")
	df = pd.read_sql_query(query, db_connection)
	return df


def parse_bool(value):
	return value.strip().upper() == "TRUE"



@LOGGER.wrap_log("Running ETL","Task successfull","Failed to Execute Script",None)
def ETL_pipeline():
	iso = strip_columns(read_ISO())
	cont = strip_columns(read_Continents())
	phases = strip_columns(read_Phases())

	ref_data = read_inputs()
	ref_data = strip_columns(ref_data)
	ref_data = ref_data[validate_formats(ref_data)]
	ref_data = data_conversion(ref_data)
	ref_data = ref_data[validate_semantics(ref_data,phases)]
	ref_data = add_timestamps_atributes(ref_data)

	invalid_iso = validate_country_ISO(ref_data,iso)
	ref_data = process_iso_codes(ref_data, invalid_iso, iso)
	ref_data = ref_data[invalid_iso]

	ref_data = ref_data.reset_index(drop=True)

	SQL_MANAGER,DB_CONN = create_SQL_manager()
	start_db = CONFIG.get_option_cast("start_db_file",parse_bool)
	if start_db:
		SQL_kickstart(SQL_MANAGER,DB_CONN,iso, cont, phases)

	old_column_names = [name for name in ref_data.columns]
	ref_data.columns = [name.replace(" ","").upper() for name in ref_data.columns]
	data_to_SQL(DB_CONN,ref_data)
	ref_data = get_joint_table(SQL_MANAGER,DB_CONN)
	ref_data.columns = old_column_names + ["Continent","Phase"]
	ref_data['Phase'] = "Phase " + ref_data['Phase'].astype(str)
	ref_data.to_csv(CONFIG.get_csv_file("intermediary_csv_file"),index=False)
	pass




if __name__ == '__main__':
	ETL_pipeline()

