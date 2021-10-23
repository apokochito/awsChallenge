import unittest

class MyFirstTest(unittest.TestCase):
	def test_upper(self):
		self.assertFalse('test'.isupper())
		self.assertTrue('TEST'.isupper())

if __name__ == '__main__':
	unittest.main()