from collections import defaultdict
import string

class Database(object):

	def __init__(self):
		self.reset()

	def reset(self):
		self.values = {}
		self.values_index = defaultdict(dict)

	def set(self, name, value):
		if name in self.values:
			existing_value = self.values[name]

			if existing_value in self.values_index:
				del self.values_index[existing_value][name]

		self.values[name] = value

		self.values_index[value][name] = True
		
	def get(self, name):
		if not name in self.values:
			return 'NULL'

		return self.values[name]
		
	def unset(self, name):
		if name in self.values:

			if self.values[name] in self.values_index:
				del self.values_index[self.values[name]][name]

			del self.values[name]

		
	def equalto(self, value):
		if not value in self.values_index or not self.values_index[value]:
			return 'NONE'

		# iterkeys vs keys?
		return ' '.join(sorted(self.values_index[value].keys()))


class LineInput(object):

	def __init__(self, database):
		self.database = database
	
	def consume(self, line):

		if not line:
			return 'error', ''
		
		# python 3: command, *args = line.split()		
		
		line = line.split()
		
		command = string.lower(line[0])
		args = line[1:]

		if hasattr(self.database, command):
			method = getattr(self.database, command)
			
			try:
				ret = method(*args)

				return 'ok', ret
			except TypeError:
				# invalid command arguments
				return 'error', ''

		elif command == 'end':
			return 'end', ''

		# invalid command
		return 'error', ''

	
if __name__ == '__main__':

	db = Database()
	
	processor = LineInput(db)

	buffer = []
	
	while 1:
		try:
			input = raw_input()

			(status, ret) = processor.consume(input)

			if status == 'ok':
				if ret:
					buffer.append(ret)
			elif status == 'error':
				continue
			elif status == 'end':
				break

		except KeyboardInterrupt:
			break

	print "\n".join(buffer)

