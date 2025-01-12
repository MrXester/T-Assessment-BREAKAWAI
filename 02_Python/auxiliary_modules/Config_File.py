from configparser import ConfigParser
import os


class Config(ConfigParser):
	def __init__(self, pathToFile ,*args, **kwargs):
		super().__init__(*args, **kwargs)
		self.read(pathToFile)
		sql_path = self["PATH LOCATION"]["sql_path"]
		self._log_path = self["PATH LOCATION"]["log_path"]
		self.SQL_SCRIPTS = [os.path.join(sql_path,file_name) for file_name in os.listdir(sql_path) if file_name.endswith(".sql")]
		self._logs = {file_name[:-4]:os.path.join(self._log_path,file_name) for file_name in os.listdir(self._log_path) if file_name.endswith(".log")}



	def get_option_cast(self,option_name,castFunction):
		return castFunction(self["OPTIONS"][option_name])
		 

	def get_csv_file(self,constName):
		csv_path = self["PATH LOCATION"]["csv_path"]
		return os.path.join(csv_path,self["FILE LOCATION"][constName])

	def get_db_file(self):
		csv_path = self["PATH LOCATION"]["sql_path"]
		return os.path.join(csv_path,self["FILE LOCATION"]["db_file"])

	def get_log_file(self,base_name):
		if base_name in self._logs:
			file_name = self._logs[base_name]
		else:
			file_name = os.path.join(self._log_path,f"{base_name}.log")
			self._logs[base_name] = file_name
		return file_name
	
	def input_files(self):
		csv_path = self["PATH LOCATION"]["csv_path"]
		input_fact = self["FILE LOCATION"]["input_csv_files"]
		return (os.path.join(csv_path,file_name) for file_name in os.listdir(csv_path) if file_name.endswith(".csv") and file_name.startswith(input_fact))
	
	def output_files_factory(self,suffixes):
		csv_path = self["PATH LOCATION"]["csv_path"]
		out_fact = self["FILE LOCATION"]["output_csv_files"]
		
		for sufix in suffixes:
			complement = f"{sufix}"
			file_name = f"{out_fact}{complement}.csv"
			yield os.path.join(csv_path,file_name),sufix

