import unittest
import sys
from arguments import Arguments

class TestIntegration(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_flag_i_sets_arguments_interval(self):
        #given
        sys.argv = ['beholder.py', '-i', '500']
        #when
        Arguments.parse()
        #then
        self.assertEqual(Arguments.interval, 500)
