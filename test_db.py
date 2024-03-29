
from db import Database, LineInput

import unittest

class DummyDatabase(object):
	def test(self, first):
		return first

class TestLineInput(unittest.TestCase):
	def setUp(self):
		self.input = LineInput(DummyDatabase())

	def test_input_ok(self):
		self.assertEqual(('ok', 'test'), self.input.consume('test test'))

	def test_input_no_method(self):
		self.assertEqual(('error', ''), self.input.consume('nothing command'))

	def test_input_bad_args(self):
		self.assertEqual(('error', ''), self.input.consume('test test test'))

class TestDatabase(unittest.TestCase):
	def setUp(self):
		self.db = Database()
		
	def test_get_and_set(self):
		self.db.set('a', 10)

		self.assertEqual(self.db.get('a'), 10)

	def test_get_null(self):
		self.assertEqual(self.db.get('nonexistant'), 'NULL')

	def test_unset(self):
		self.db.set('a', 10)

		self.db.unset('a')

		self.assertEqual(self.db.get('a'), 'NULL')

	def test_equalto(self):
		self.db.set('a', 10)
		self.db.set('c', 10)
		self.db.set('b', 10)

		self.assertEqual(self.db.equalto(10), 'a b c')

	def test_equalto_none(self):
		self.assertEqual(self.db.equalto(10), 'NONE')

	def test_equalto_unset(self):
		self.db.set('a', 10)
		self.db.set('c', 10)
		self.db.set('b', 10)

		self.db.unset('b')

		self.assertEqual(self.db.equalto(10), 'a c')

	def test_equalto_change(self):

		self.db.set('a', 10)
		self.db.set('a', 20)

		self.assertEqual(self.db.equalto(10), 'NONE')
		self.assertEqual(self.db.equalto(20), 'a')

	def test_program(self):
		"""SET a 10
		SET b 10
		EQUALTO 10
		EQUALTO 20
		UNSET a
		EQUALTO 10
		SET b 30
		EQUALTO 10"""

		self.db.set('a', 10)
		self.db.set('b', 10)

		self.assertEqual(self.db.equalto(10), 'a b')
		self.assertEqual(self.db.equalto(20), 'NONE')

		self.db.unset('a')

		self.assertEqual(self.db.equalto(10), 'b')

		self.db.set('b', 30)

		self.assertEqual(self.db.equalto(10), 'NONE')

	def test_tx_commit(self):
		self.db.set('a', 10)

		self.db.begin()

		self.assertEqual(self.db.get('a'), 10)

		self.db.set('a', 20)

		self.assertEqual(self.db.get('a'), 20)

		self.db.commit()

		self.assertEqual(self.db.get('a'), 20)

	def test_tx_full_commit(self):

		# test that commit commits *all* open transactions
		self.db.begin()
		self.db.set('a', 30)
		self.db.begin()
		self.db.set('a', 40)
		self.db.commit()
		self.assertEqual(self.db.get('a'), 40)
		self.assertEqual(self.db.rollback(), 'INVALID ROLLBACK')

	def test_tx_rollback(self):

		self.db.set('a', 10)

		self.db.begin()

		self.assertEqual(self.db.get('a'), 10)

		self.db.set('a', 20)

		self.assertEqual(self.db.get('a'), 20)

		self.db.rollback()

		self.assertEqual(self.db.get('a'), 10)

	def test_tx_invalid_rollback(self):
		self.assertEqual(self.db.rollback(), 'INVALID ROLLBACK')

	def test_tx_begin_rollback_commit(self):
		self.db.set('a', 50)
		self.db.begin()
		self.assertEqual(self.db.get('a'), 50)
		self.db.set('a', 60)
		self.db.begin()
		self.db.unset('a')
		self.assertEqual(self.db.get('a'), 'NULL')
		self.db.rollback()
		self.assertEqual(self.db.get('a'), 60)
		self.db.commit()
		self.assertEqual(self.db.get('a'), 60)
		
if __name__ == '__main__':
	unittest.main()
