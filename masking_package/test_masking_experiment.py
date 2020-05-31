'''A rudimentary testing function'''
from masking_functions import adjust_integer, create_trial_sequence, determine_masking_type


#class TestSum(unittest.TestCase):
#	def compute_integer_adjustment(self):
#		self.assertAlmostEqual(adjust_integer(-2.38), 2)
#
#
#if __name__ == '__main__':
#	unittest.main()
def test_function():
	a = []
	a.append(adjust_integer(-2.49)== 2)
	a.append(adjust_integer(10)== 10)
	a.append(determine_masking_type('s') == (True, True))
	a.append(determine_masking_type(1) == (False, False))
	a.append(determine_masking_type("Backw") == (False, True))
	a.append(determine_masking_type('F') == (True, False))
	a.append(len(create_trial_sequence(9, 1, True, True)) == 13)

	if False in a:
		print("Test failed!")
	else:
		print("7 of 7 tests succeeded. Test successful!")