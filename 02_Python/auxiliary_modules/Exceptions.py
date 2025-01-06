class Failed_Command_Exception(Exception):
	def __init__(self, cmd_name, message=None):
		header = f"Unable to execute Command [{cmd_name}]"
		if message is None:
			message = "Unknown Error"
		super().__init__(f"{header} :: {message}")


class Inexistent_Command_Exception(Failed_Command_Exception):
	def __init__(self, cmd_name):
		super().__init__(cmd_name,message="Command does not exist")


class DB_Command_Exception(Failed_Command_Exception):
	def __init__(self, cmd_name, exception):
		super().__init__(cmd_name,message=f"Connection with DataBase Failed [{exception}]")


class DB_Connection_Exception(Exception):
	def __init__(self, exception):
		super().__init__(f"DataBase Connection Failed [{exception}]")