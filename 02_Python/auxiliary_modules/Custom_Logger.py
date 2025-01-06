import logging

class Logging_System(object):
	def __init__(self, logging_path, logger_name):
		self.logging_path = logging_path
		logging.basicConfig(filename=self.logging_path, filemode="a",**{"format":'[%(asctime)s] %(levelname)s - %(message)s',"level":logging.INFO})
		self.logger = logging.getLogger(logger_name)


	def info(self, message):
		self.logger.info(message)
		pass

	def error(self, message):
		self.logger.error(message)
		pass
	
	
	def wrap_log(self, pre_text, post_text, deafaultValue):
		def inner_decorator(func):
			def wrapper(*args, **kwargs):
				result = deafaultValue
				self.info(pre_text)
				try:
					result = func(*args, **kwargs)
				except Exception as e:
					self.error(e)
				finally:
					self.info(post_text)
				return result
			return wrapper
		return inner_decorator


