#! ../../envTABAWAI/Scripts/python.exe

from auxiliary_modules.Custom_Logger import Logging_System
from auxiliary_modules.ExecuteSQL import SQL_executor
from auxiliary_modules.Exceptions import *
from auxiliary_modules.Config_File import Config
import pandas as pd

CONFIG_PATH = "../config.cfg"
config = Config(CONFIG_PATH)
logger = Logging_System(config.get_log_file("log_file"),"logger")


#sql_exec = SQL_executor()

#configs = configparser.ConfigParser()
#log = Logging_System()
#sql_executor = SQL_executor()















