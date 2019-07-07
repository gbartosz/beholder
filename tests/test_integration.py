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
    def test_should_correctly_sum_up_request_count(self):
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
    def test_should_correctly_calculate_average_response_time(self):
        #given
        #when
        self.run_beholder("-i 1 -f tests/log_10_lines_5s.log")
        #then
        self.assertAlmostEqual(float(self.output_cell(1, 2)), 1.05, places=2)
        self.assertAlmostEqual(float(self.output_cell(2, 2)), 4.47, places=2)
        self.assertAlmostEqual(float(self.output_cell(3, 2)), 3.27, places=2)
        self.assertAlmostEqual(float(self.output_cell(4, 2)), 0.20, places=2)
        self.assertAlmostEqual(float(self.output_cell(5, 2)), 2.01, places=2)

    # 2019-07-06 11:40:33+00:00;153;2.5590784313725496;0;0;1;2.027;22;1.6010454545454544;22;2.2419090909090915;50;2.74774;153;2.5590784313725496;22;2.2011818181818184;0;0;0;0
    # 2019-07-06 11:40:38+00:00;167;2.3678562874251505;0;0;0;0;29;1.9378620689655177;23;2.063347826086957;41;2.4855609756097565;167;2.3678562874251505;29;2.1981724137931034;0;0;0;0
    # 2019-07-06 11:40:43+00:00;166;2.352704819277108;0;0;0;0;19;1.138;29;2.666103448275862;55;2.4669636363636362;166;2.352704819277108;33;2.4484848484848487;0;0;0;0
    # 2019-07-06 11:40:48+00:00;167;2.3522335329341306;0;0;3;1.8503333333333334;27;2.0626296296296296;22;3.240727272727273;47;2.058978723404255;167;2.3522335329341306;27;1.832925925925926;0;0;0;0
    # 2019-07-06 11:40:53+00:00;167;2.482467065868263;0;0;2;0.708;17;2.210588235294118;28;1.9244285714285716;47;2.806446808510638;167;2.482467065868263;32;2.4767812499999993;0;0;0;0
    # 2019-07-06 11:40:58+00:00;166;2.8018674698795194;0;0;1;6.824;20;3.0552999999999995;25;2.9934000000000003;50;2.6084199999999993;166;2.8018674698795194;25;2.43816;0;0;0;0
    # 2019-07-06 11:41:03+00:00;14;1.7474285714285716;1;3.969;1;3.969;1;0.149;1;0.143;6;2.4746666666666663;14;1.7474285714285716;2;5.1165;0;0;1;6.76
    def test_should_correctly_sum_up_request_count_in_each_category(self):
        #given
        #when
        self.run_beholder("-i 5 -f 'tests/log_1k_lines_30s.log' -a '64.122.85.26;\d{1,3}.\d{1,3}.\d{1,3}.26' -m 'PUT;GET;P.{3,}' -e '/.*' -c '200;30.' -u '35.69.232.134:3048'")
        #then
        self.assertEqual(int(self.output_cell(1, 3)), 0)
        self.assertEqual(int(self.output_cell(2, 3)), 0)
        self.assertEqual(int(self.output_cell(3, 3)), 0)
        self.assertEqual(int(self.output_cell(4, 3)), 0)
        self.assertEqual(int(self.output_cell(5, 3)), 0)
        self.assertEqual(int(self.output_cell(6, 3)), 0)
        self.assertEqual(int(self.output_cell(7, 3)), 1)
    
        self.assertEqual(int(self.output_cell(1, 5)), 1)
        self.assertEqual(int(self.output_cell(2, 5)), 0)
        self.assertEqual(int(self.output_cell(3, 5)), 0)
        self.assertEqual(int(self.output_cell(4, 5)), 3)
        self.assertEqual(int(self.output_cell(5, 5)), 2)
        self.assertEqual(int(self.output_cell(6, 5)), 1)
        self.assertEqual(int(self.output_cell(7, 5)), 1)

        self.assertEqual(int(self.output_cell(1, 7)), 22)
        self.assertEqual(int(self.output_cell(2, 7)), 29)
        self.assertEqual(int(self.output_cell(3, 7)), 19)
        self.assertEqual(int(self.output_cell(4, 7)), 27)
        self.assertEqual(int(self.output_cell(5, 7)), 17)
        self.assertEqual(int(self.output_cell(6, 7)), 20)
        self.assertEqual(int(self.output_cell(7, 7)), 1)

        self.assertEqual(int(self.output_cell(1, 9)), 22)
        self.assertEqual(int(self.output_cell(2, 9)), 23)
        self.assertEqual(int(self.output_cell(3, 9)), 29)
        self.assertEqual(int(self.output_cell(4, 9)), 22)
        self.assertEqual(int(self.output_cell(5, 9)), 28)
        self.assertEqual(int(self.output_cell(6, 9)), 25)
        self.assertEqual(int(self.output_cell(7, 9)), 1)

        self.assertEqual(int(self.output_cell(1, 11)), 50)
        self.assertEqual(int(self.output_cell(2, 11)), 41)
        self.assertEqual(int(self.output_cell(3, 11)), 55)
        self.assertEqual(int(self.output_cell(4, 11)), 47)
        self.assertEqual(int(self.output_cell(5, 11)), 47)
        self.assertEqual(int(self.output_cell(6, 11)), 50)
        self.assertEqual(int(self.output_cell(7, 11)), 6)

        self.assertEqual(int(self.output_cell(1, 13)), 153)
        self.assertEqual(int(self.output_cell(2, 13)), 167)
        self.assertEqual(int(self.output_cell(3, 13)), 166)
        self.assertEqual(int(self.output_cell(4, 13)), 167)
        self.assertEqual(int(self.output_cell(5, 13)), 167)
        self.assertEqual(int(self.output_cell(6, 13)), 166)
        self.assertEqual(int(self.output_cell(7, 13)), 14)

        self.assertEqual(int(self.output_cell(1, 15)), 22)
        self.assertEqual(int(self.output_cell(2, 15)), 29)
        self.assertEqual(int(self.output_cell(3, 15)), 33)
        self.assertEqual(int(self.output_cell(4, 15)), 27)
        self.assertEqual(int(self.output_cell(5, 15)), 32)
        self.assertEqual(int(self.output_cell(6, 15)), 25)
        self.assertEqual(int(self.output_cell(7, 15)), 2)

        self.assertEqual(int(self.output_cell(1, 17)), 0)
        self.assertEqual(int(self.output_cell(2, 17)), 0)
        self.assertEqual(int(self.output_cell(3, 17)), 0)
        self.assertEqual(int(self.output_cell(4, 17)), 0)
        self.assertEqual(int(self.output_cell(5, 17)), 0)
        self.assertEqual(int(self.output_cell(6, 17)), 0)
        self.assertEqual(int(self.output_cell(7, 17)), 0)

        self.assertEqual(int(self.output_cell(1, 19)), 0)
        self.assertEqual(int(self.output_cell(2, 19)), 0)
        self.assertEqual(int(self.output_cell(3, 19)), 0)
        self.assertEqual(int(self.output_cell(4, 19)), 0)
        self.assertEqual(int(self.output_cell(5, 19)), 0)
        self.assertEqual(int(self.output_cell(6, 19)), 0)
        self.assertEqual(int(self.output_cell(7, 19)), 1)

    def test_should_correctly_calculate_average_response_time_in_each_category(self):
        #given
        #when
        self.run_beholder("-i 5 -f 'tests/log_1k_lines_30s.log' -a '64.122.85.26;\d{1,3}.\d{1,3}.\d{1,3}.26' -m 'PUT;GET;P.{3,}' -e '/.*' -c '200;30.' -u '35.69.232.134:3048'")
        #then
        self.assertAlmostEqual(float(self.output_cell(1, 3+1)), 0.0, places=2)
        self.assertAlmostEqual(float(self.output_cell(2, 3+1)), 0.0, places=2)
        self.assertAlmostEqual(float(self.output_cell(3, 3+1)), 0.0, places=2)
        self.assertAlmostEqual(float(self.output_cell(4, 3+1)), 0.0, places=2)
        self.assertAlmostEqual(float(self.output_cell(5, 3+1)), 0.0, places=2)
        self.assertAlmostEqual(float(self.output_cell(6, 3+1)), 0.0, places=2)
        self.assertAlmostEqual(float(self.output_cell(7, 3+1)), 3.97, places=2)
    
        self.assertAlmostEqual(float(self.output_cell(1, 5+1)), 2.03, places=2)
        self.assertAlmostEqual(float(self.output_cell(2, 5+1)), 0, places=2)
        self.assertAlmostEqual(float(self.output_cell(3, 5+1)), 0, places=2)
        self.assertAlmostEqual(float(self.output_cell(4, 5+1)), 1.85, places=2)
        self.assertAlmostEqual(float(self.output_cell(5, 5+1)), 0.71, places=2)
        self.assertAlmostEqual(float(self.output_cell(6, 5+1)), 6.82, places=2)
        self.assertAlmostEqual(float(self.output_cell(7, 5+1)), 3.97, places=2)

        self.assertAlmostEqual(float(self.output_cell(1, 7+1)), 1.601, places=2)
        self.assertAlmostEqual(float(self.output_cell(2, 7+1)), 1.937, places=2)
        self.assertAlmostEqual(float(self.output_cell(3, 7+1)), 1.138, places=2)
        self.assertAlmostEqual(float(self.output_cell(4, 7+1)), 2.062, places=2)
        self.assertAlmostEqual(float(self.output_cell(5, 7+1)), 2.210, places=2)
        self.assertAlmostEqual(float(self.output_cell(6, 7+1)), 3.055, places=2)
        self.assertAlmostEqual(float(self.output_cell(7, 7+1)), 0.149, places=2)

        self.assertAlmostEqual(float(self.output_cell(1, 9+1)), 2.241, places=2)
        self.assertAlmostEqual(float(self.output_cell(2, 9+1)), 2.063, places=2)
        self.assertAlmostEqual(float(self.output_cell(3, 9+1)), 2.666, places=2)
        self.assertAlmostEqual(float(self.output_cell(4, 9+1)), 3.240, places=2)
        self.assertAlmostEqual(float(self.output_cell(5, 9+1)), 1.924, places=2)
        self.assertAlmostEqual(float(self.output_cell(6, 9+1)), 2.993, places=2)
        self.assertAlmostEqual(float(self.output_cell(7, 9+1)), 0.143, places=2)

        self.assertAlmostEqual(float(self.output_cell(1, 11+1)), 2.747, places=2)
        self.assertAlmostEqual(float(self.output_cell(2, 11+1)), 2.485, places=2)
        self.assertAlmostEqual(float(self.output_cell(3, 11+1)), 2.466, places=2)
        self.assertAlmostEqual(float(self.output_cell(4, 11+1)), 2.058, places=2)
        self.assertAlmostEqual(float(self.output_cell(5, 11+1)), 2.806, places=2)
        self.assertAlmostEqual(float(self.output_cell(6, 11+1)), 2.608, places=2)
        self.assertAlmostEqual(float(self.output_cell(7, 11+1)), 2.474, places=2)

        self.assertAlmostEqual(float(self.output_cell(1, 13+1)), 2.559, places=2)
        self.assertAlmostEqual(float(self.output_cell(2, 13+1)), 2.367, places=2)
        self.assertAlmostEqual(float(self.output_cell(3, 13+1)), 2.352, places=2)
        self.assertAlmostEqual(float(self.output_cell(4, 13+1)), 2.352, places=2)
        self.assertAlmostEqual(float(self.output_cell(5, 13+1)), 2.482, places=2)
        self.assertAlmostEqual(float(self.output_cell(6, 13+1)), 2.801, places=2)
        self.assertAlmostEqual(float(self.output_cell(7, 13+1)), 1.747, places=2)

        self.assertAlmostEqual(float(self.output_cell(1, 15+1)), 2.201, places=2)
        self.assertAlmostEqual(float(self.output_cell(2, 15+1)), 2.198, places=2)
        self.assertAlmostEqual(float(self.output_cell(3, 15+1)), 2.448, places=2)
        self.assertAlmostEqual(float(self.output_cell(4, 15+1)), 1.832, places=2)
        self.assertAlmostEqual(float(self.output_cell(5, 15+1)), 2.476, places=2)
        self.assertAlmostEqual(float(self.output_cell(6, 15+1)), 2.438, places=2)
        self.assertAlmostEqual(float(self.output_cell(7, 15+1)), 5.116, places=2)

        self.assertAlmostEqual(float(self.output_cell(1, 17+1)), 0, places=2)
        self.assertAlmostEqual(float(self.output_cell(2, 17+1)), 0, places=2)
        self.assertAlmostEqual(float(self.output_cell(3, 17+1)), 0, places=2)
        self.assertAlmostEqual(float(self.output_cell(4, 17+1)), 0, places=2)
        self.assertAlmostEqual(float(self.output_cell(5, 17+1)), 0, places=2)
        self.assertAlmostEqual(float(self.output_cell(6, 17+1)), 0, places=2)
        self.assertAlmostEqual(float(self.output_cell(7, 17+1)), 0, places=2)

        self.assertAlmostEqual(float(self.output_cell(1, 19+1)), 0, places=2)
        self.assertAlmostEqual(float(self.output_cell(2, 19+1)), 0, places=2)
        self.assertAlmostEqual(float(self.output_cell(3, 19+1)), 0, places=2)
        self.assertAlmostEqual(float(self.output_cell(4, 19+1)), 0, places=2)
        self.assertAlmostEqual(float(self.output_cell(5, 19+1)), 0, places=2)
        self.assertAlmostEqual(float(self.output_cell(6, 19+1)), 0, places=2)
        self.assertAlmostEqual(float(self.output_cell(7, 19+1)), 6.76, places=2)
