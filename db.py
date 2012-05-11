from collections import defaultdict
import string

class Database(object):

	def __init__(self):
		self._reset()
		self._reset_tx()

	def _reset(self):
		self.values = {}
		self.values_index = defaultdict(dict)

	def _reset_tx(self):
		self.tx_level = 0

		# holds the values of self.values as they existed *before* they were changed in the
		# current transaction (if they were changed at all)
		self.tx_values = defaultdict(dict)

	def set(self, name, value):
		if name in self.values:
			existing_value = self.values[name]

			self.tx_values[self.tx_level][name] = existing_value

			if existing_value in self.values_index:
				del self.values_index[existing_value][name]

		self.values[name] = value

		self.values_index[value][name] = True
		
	def get(self, name):
		if not name in self.values or not self.values[name]:
			return 'NULL'

		return self.values[name]
		
	def unset(self, name):
		if name in self.values:

			if self.values[name] in self.values_index:
				del self.values_index[self.values[name]][name]

			self.tx_values[self.tx_level][name] = self.values[name]

			del self.values[name]

	def equalto(self, value):
		if not value in self.values_index or not self.values_index[value]:
			return 'NONE'

		# iterkeys vs keys?
		return ' '.join(sorted(self.values_index[value].keys()))

	def begin(self):
		self.tx_level += 1

	def rollback(self):
		if self.tx_level == 0:
			return 'INVALID ROLLBACK'

		if self.tx_values[self.tx_level]:
			self.values.update(self.tx_values[self.tx_level])

		self.tx_level -= 1


	def commit(self):
		# as we're applying all changes to the canonical value dict, all we need to do to commit
		# is throw away all open transaction data
		self._reset_tx()


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

