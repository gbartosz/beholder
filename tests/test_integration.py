import unittest
import sys
import subprocess
from arguments import Arguments
from beholder import Beholder
from stats_collector import StatsCollector
from io import StringIO

class TestIntegration(unittest.TestCase):

    def setUp(self):
        self.output = None
        self.parsed_output = None
        pass

    def tearDown(self):
        pass

    def run_beholder(self, command):
        self.output = subprocess.check_output('python beholder.py ' + command, shell=True).decode("utf-8")
        self.parse_output()

    def parse_output(self):
        if not self.parsed_output:
            self.parsed_output = []
            for row in self.output.split('\n'):
                self.parsed_output.append([])
                for col in row.split(';'):
                    self.parsed_output[-1].append(col)

        return self.parsed_output

    def output_cell(self, i, j):
        return self.parsed_output[i][j]

    def test_default_column_headers(self):
        #given
        #when
        self.run_beholder("-i 5 -f tests/log_1k_lines_30s.log")
        #then
        self.assertEqual(self.output_cell(0, 0), 'datetime')
        self.assertEqual(self.output_cell(0, 1), 'req_cnt')
        self.assertEqual(self.output_cell(0, 2), 'avg_resp_time')

    def test_complex_column_headers(self):
        #given
        #when
        self.run_beholder("-i 5 -f 'tests/log_1k_lines_30s.log' -a '64.122.85.26;\d{1,3}.\d{1,3}.\d{1,3}.26' -m 'PUT;GET;P.{3,}' -e '/.*' -c '200;30.' -u '35.69.232.134:3048'")
        #then
        self.assertEqual(self.output_cell(0, 0), 'datetime')
        self.assertEqual(self.output_cell(0, 1), 'req_cnt')
        self.assertEqual(self.output_cell(0, 2), 'avg_resp_time')

        self.assertEqual(self.output_cell(0, 3), 'req_cnt_client_address_64.122.85.26')
        self.assertEqual(self.output_cell(0, 4), 'avg_resp_time_client_address_64.122.85.26')

        self.assertEqual(self.output_cell(0, 5), 'req_cnt_client_address_\d{1,3}.\d{1,3}.\d{1,3}.26')
        self.assertEqual(self.output_cell(0, 6), 'avg_resp_time_client_address_\d{1,3}.\d{1,3}.\d{1,3}.26')

        self.assertEqual(self.output_cell(0, 7), 'req_cnt_method_PUT')
        self.assertEqual(self.output_cell(0, 8), 'avg_resp_time_method_PUT')

        self.assertEqual(self.output_cell(0, 9), 'req_cnt_method_GET')
        self.assertEqual(self.output_cell(0, 10), 'avg_resp_time_method_GET')

        self.assertEqual(self.output_cell(0, 11), 'req_cnt_method_P.{3,}')
        self.assertEqual(self.output_cell(0, 12), 'avg_resp_time_method_P.{3,}')

        self.assertEqual(self.output_cell(0, 13), 'req_cnt_endpoint_/.*')
        self.assertEqual(self.output_cell(0, 14), 'avg_resp_time_endpoint_/.*')

        self.assertEqual(self.output_cell(0, 15), 'req_cnt_status_code_200')
        self.assertEqual(self.output_cell(0, 16), 'avg_resp_time_status_code_200')

        self.assertEqual(self.output_cell(0, 17), 'req_cnt_status_code_30.')
        self.assertEqual(self.output_cell(0, 18), 'avg_resp_time_status_code_30.')

        self.assertEqual(self.output_cell(0, 19), 'req_cnt_upstream_address_35.69.232.134:3048')
        self.assertEqual(self.output_cell(0, 20), 'avg_resp_time_upstream_address_35.69.232.134:3048')

    def test_result_should_include_1k_rows(self):
        #given
        #when
        self.run_beholder("-i 5 -f tests/log_1k_lines_30s.log")
        #then
        self.assertEqual(sum(int(self.output_cell(i, 1)) for i in range(1, len(self.parsed_output)-1)), 1000)

    # datetime;req_cnt;avg_resp_time
    # 2019-07-06 11:40:33+00:00;153;2.5590784313725496
    # 2019-07-06 11:40:38+00:00;167;2.3678562874251505
    # 2019-07-06 11:40:43+00:00;166;2.352704819277108
    # 2019-07-06 11:40:48+00:00;167;2.3522335329341306
    # 2019-07-06 11:40:53+00:00;167;2.482467065868263
    # 2019-07-06 11:40:58+00:00;166;2.8018674698795194
    # 2019-07-06 11:41:03+00:00;14;1.7474285714285716    
    def test_result_should_correctly_sum_up_request_count(self):
        #given
        #when
        self.run_beholder("-i 5 -f tests/log_1k_lines_30s.log")
        #then
        self.assertEqual(int(self.output_cell(1, 1)), 153)
        self.assertEqual(int(self.output_cell(2, 1)), 167)
        self.assertEqual(int(self.output_cell(3, 1)), 166)
        self.assertEqual(int(self.output_cell(4, 1)), 167)
        self.assertEqual(int(self.output_cell(5, 1)), 167)
        self.assertEqual(int(self.output_cell(6, 1)), 166)
        self.assertEqual(int(self.output_cell(7, 1)), 14)

    # python beholder.py -i 1 -f tests/log_10_lines_5s.log 
    # datetime;req_cnt;avg_resp_time
    # 2019-07-06 13:27:21+00:00;2;1.0474999999999999
    # 2019-07-06 13:27:22+00:00;2;4.468500000000001
    # 2019-07-06 13:27:23+00:00;2;3.27
    # 2019-07-06 13:27:24+00:00;2;0.2025
    # 2019-07-06 13:27:25+00:00;2;2.0125
    def test_result_should_correctly_calculate_average_response_time(self):
        #given
        #when
        self.run_beholder("-i 1 -f tests/log_10_lines_5s.log")
        #then
        self.assertAlmostEqual(float(self.output_cell(1, 2)), 1.05, places=2)
        self.assertAlmostEqual(float(self.output_cell(2, 2)), 4.47, places=2)
        self.assertAlmostEqual(float(self.output_cell(3, 2)), 3.27, places=2)
        self.assertAlmostEqual(float(self.output_cell(4, 2)), 0.20, places=2)
        self.assertAlmostEqual(float(self.output_cell(5, 2)), 2.01, places=2)
