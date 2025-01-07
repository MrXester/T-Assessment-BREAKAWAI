#! ../../envTABAWAI/Scripts/python.exe

from auxiliary_modules.Custom_Logger import Logging_System
from auxiliary_modules.ExecuteSQL import SQL_executor
from auxiliary_modules.Exceptions import *
from auxiliary_modules.Config_File import Config
import pandas as pd
from datetime import datetime

CONFIG_PATH = "../config.cfg"
config = Config(CONFIG_PATH)
logger = Logging_System(config.get_log_file("log_file"),"logger")

in_files = config.input_files()
logger.info(f"Detected files for input: {in_files}")


sql_files = config.SQL_SCRIPTS
sql_exec = SQL_executor(sql_files,None)
logger.info(f"SQL scripts detected: {sql_files}")
logger.info(f"SQL commands: {sql_exec.commands}")


csvCont = config.get_csv_file("to_continent")
csvAlpha3 = config.get_csv_file("to_country")





def get_iso_to_continent_df():
	dfAlpha3 = pd.read_csv(csvAlpha3,encoding = "ISO-8859-1")[["iso3","country_common"]]
	dfAlpha3.columns = ["Iso3","Country"]
	dfCont = pd.read_csv(csvCont)
	df = dfCont.merge(dfAlpha3, on=["Country"], how='inner')[["Continent","Iso3"]]
	df.columns = ["Continent","Country"]
	return df



cont = get_iso_to_continent_df()
df = pd.read_csv(in_files[0])



def add_atributes(ref_data):
	df = ref_data.merge(cont, on=["Country"], how='inner')
	df["Start Timestamp"] = pd.to_datetime(df['Start Timestamp'], format="%d/%m/%Y %H:%M:%S")
	df["Complete Timestamp"] = pd.to_datetime(df['Complete Timestamp'], format="%d/%m/%Y %H:%M:%S")
	df["Quarter"] = 'Q' + df['Start Timestamp'].dt.quarter.astype(str)
	df["Week"] = df['Start Timestamp'].dt.isocalendar().week
	return df



df = add_atributes(df)

print(df.columns)
rows_with_nan = df[df.isnull().any(axis=1)]
print("NaN values:", rows_with_nan)



#rows in which the discount is higher than the invoice
rows = df[df['Discount'] > df['Invoice amount']]
print(rows)


duplicates = df[df.duplicated(subset=['Case ID',"Activity", "Resource", "Role", "Invoice amount", "Discount", "Country"], keep=False)]
print(duplicates)









#date_obj = datetime.strptime(date_str, "%d/%m/%Y %H:%M:%S")


#sql_exec = SQL_executor()

#configs = configparser.ConfigParser()
#log = Logging_System()
#sql_executor = SQL_executor()















