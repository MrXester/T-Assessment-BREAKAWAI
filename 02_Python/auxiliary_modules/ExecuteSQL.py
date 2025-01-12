from .Exceptions import Inexistent_Command_Exception,DB_Command_Exception,DB_Connection_Exception
import re

class SQL_executor(object):
	#Class to execute code based on name in a given sql file and a given DataBase
	def __init__(self, sql_commands_files, db_connection):
		self.sql_commands = sql_commands_files
		self.conn = None
		self.cursor = None
		self.commands = {}
		self.conn = db_connection
		self._read_commands()
		
	def connect(self):
		#establish connection to db
		try:
			self.cursor = self.conn.cursor()
		except Exception as e:
			raise DB_Connection_Exception(e)




	def _read_commands(self):
		#Read SQL script file and register statement on a dictionary
		#Parses the SQL file registering commands with their respective names
		regx = re.compile(r"--BEGIN(.+?(?=--))--(.+?(?=--END))")
		for file_cmds in self.sql_commands:
			with open(file_cmds, 'r') as file:
				sql_scripts = file.read().replace("\n", " ")
				for cmd_name,statement in re.findall(regx, sql_scripts):
					self.commands[cmd_name.strip()] = statement.strip()
		pass


	def get_command(self,cmd_name):
		#get a certain command from the registered ones in the SQL script
		statement = self.commands.get(cmd_name,"")
		return statement


	def execute(self,cmd_name):
		#receives a command name and executes it in the DB connection previously set
		statement = self.get_command(cmd_name)
		if len(statement) <= 0:
			raise Inexistent_Command_Exception(cmd_name)
		else:
			try:
				self.cursor.execute(statement)
				self.conn.commit()

			except Exception as e:
				raise DB_Command_Exception(cmd_name,e)
		return 0
		


