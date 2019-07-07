import unittest
import sys
from arguments import Arguments
from aggregator import Aggregator
from tests.assemblers.log_file import LogFileAssembler
from tests.assemblers.log import LogAssembler


class TestAggregator(unittest.TestCase):

    def test_default_aggregator_counts_every_log(self):
        #given
        logs = LogFileAssembler().build()
        aggregator = Aggregator()
        #when
        for log in logs:
            aggregator.process(log)
        #then
        self.assertEqual(len(logs), aggregator.request_count)

    def test_default_aggregator_averages_time_of_every_log(self):
        #given
        logs = LogFileAssembler().build()
        aggregator = Aggregator()
        #when
        for log in logs:
            aggregator.process(log)
        #then
        self.assertAlmostEqual(sum(l.request_time for l in logs)/len(logs), aggregator.average_response_time, places=5)

    def test_response_code_aggregator_counts_only_logs_of_matching_codes(self):
        #given
        logs = [
            LogAssembler().with_status_code('200').build(),
            LogAssembler().with_status_code('400').build(),
            LogAssembler().with_status_code('401').build(),
            LogAssembler().with_status_code('502').build(),
            LogAssembler().with_status_code('504').build(),
            LogAssembler().with_status_code('200').build()
        ]
        aggregator = Aggregator(regex_pattern=r'[2|5]..', log_attribute_name='status_code')
        #when
        for log in logs:
            aggregator.process(log)
        #then
        self.assertEqual(4, aggregator.request_count)

    def test_response_code_aggregator_averages_time_of_only_logs_of_matching_codes(self):
        #given
        logs = [
            LogAssembler().with_status_code('200').with_request_time(1.0).build(),
            LogAssembler().with_status_code('400').with_request_time(2.0).build(),
            LogAssembler().with_status_code('401').with_request_time(4.0).build(),
            LogAssembler().with_status_code('502').with_request_time(8.0).build(),
            LogAssembler().with_status_code('504').with_request_time(16.0).build(),
            LogAssembler().with_status_code('200').with_request_time(32.0).build()
        ]
        aggregator = Aggregator(regex_pattern=r'[2|5]..', log_attribute_name='status_code')
        #when
        for log in logs:
            aggregator.process(log)
        #then
        self.assertAlmostEqual(57/4, aggregator.average_response_time, places=5)
