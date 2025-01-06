from Exceptions import Inexistent_Command_Exception,DB_Command_Exception,DB_Connection_Exception
import re

class SQL_executor(object):
	#Class to execute code based on name in a given sql file and a given DataBase
	def __init__(self, db_path, sql_commands_path, db_connection):
		self.db_path = db_path
		self.sql_commands_path = sql_commands_path
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
		regx = re.compile(r"-- BEGIN(.+?(?=--))(.+?(?=-- END))")
		with open(self.sql_commands_path, 'r') as file:
			sql_scripts = file.read().replace("\n", " ")
			for cmd_name,statement in re.findall(regx, sql_scripts):
				self.commands[cmd_name] = statement
		pass


	def get_command(self,cmd_name):
		statement = self.commands.get(cmd_name,"")
		return statement


	def execute(self,cmd_name):
		statement = self._get_command(cmd_name)
		if len(statement) <= 0:
			raise Inexistent_Command_Exception(cmd_name)
		else:
			try:
				cursor.execute(statement)
				conn.commit()

			except Exception as e:
				raise DB_Command_Exception(cmd_name)
		return 0
		



