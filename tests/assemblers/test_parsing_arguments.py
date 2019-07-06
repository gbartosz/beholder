import unittest
import sys
from arguments import Arguments

class TestParsingArguments(unittest.TestCase):

    def test_flag_i_sets_arguments_interval(self):
        #given
        sys.argv = ['beholder.py', '-i', '500']
        #when
        Arguments.parse()
        #then
        self.assertEqual(Arguments.interval, 500)

    def test_default_interval_equals_60(self):
        #given
        sys.argv = ['beholder.py']
        #when
        Arguments.parse()
        #then
        self.assertEqual(Arguments.interval, 60)

    def test_flag_f_sets_filename(self):
        #given
        sys.argv = ['beholder.py', '-f', 'fname']
        #when
        Arguments.parse()
        #then
        self.assertEqual(Arguments.filename, 'fname')

    def test_flag_c_sets_single_code(self):
        #given
        sys.argv = ['beholder.py', '-c', '200']
        #when
        Arguments.parse()
        #then
        self.assertEqual(Arguments.codes, ['200'])

    def test_flag_c_sets_multiple_codes(self):
        #given
        sys.argv = ['beholder.py', '-c', '200;3..;50.;502']
        #when
        Arguments.parse()
        #then
        self.assertEqual(Arguments.codes, ['200','3..','50.','502'])

    def test_changing_separator_allows_for_colon_in_regexp(self):
        #given
        sys.argv = ['beholder.py', '-c', '2;0&&&3..;&&&50.&&&502', '-s', '&&&']
        #when
        Arguments.parse()
        #then
        self.assertEqual(Arguments.codes, ['2;0','3..;','50.','502'])

    def test_flag_m_sets_multiple_methods(self):
        #given
        sys.argv = ['beholder.py', '-m', 'PUT;POST;DELETE']
        #when
        Arguments.parse()
        #then
        self.assertEqual(Arguments.methods, ['PUT','POST','DELETE'])

    def test_flag_e_sets_multiple_endpoints(self):
        #given
        sys.argv = ['beholder.py', '-e', '/endp1/test1;/endp1/test2']
        #when
        Arguments.parse()
        #then
        self.assertEqual(Arguments.endpoints, ['/endp1/test1','/endp1/test2'])

    def test_flag_a_sets_multiple_addresses(self):
        #given
        sys.argv = ['beholder.py', '-a', '10.0.10.10;0.2.3.11']
        #when
        Arguments.parse()
        #then
        self.assertEqual(Arguments.client_addresses, ['10.0.10.10','0.2.3.11'])

    def test_flag_u_sets_multiple_upstream_addresses(self):
        #given
        sys.argv = ['beholder.py', '-u', '10.0.10.10:7721;0.2.3.11:9213']
        #when
        Arguments.parse()
        #then
        self.assertEqual(Arguments.upstream_addresses, ['10.0.10.10:7721','0.2.3.11:9213'])

    def test_flag_o_sets_online_mode(self):
        #given
        sys.argv = ['beholder.py', '-o']
        #when
        Arguments.parse()
        #then
        self.assertTrue(Arguments.online_mode)
