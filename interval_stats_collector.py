# -*- coding: utf-8 -*-
from log import categories
from aggregator import Aggregator


class IntervalStatsCollector:

    def __init__(self, start_datetime):
        self.start_datetime = start_datetime
        self.logs = []

    def append(self, log):
        self.logs.append(log)

    def close(self):
        aggregators = [Aggregator()]

        for regex_pattern, log_attribute_name in categories():
            aggregators.append(Aggregator(regex_pattern, log_attribute_name))

        for log in self.logs:
            for aggregator in aggregators:
                aggregator.process(log)

        columns = [self.start_datetime]

        for aggregator in aggregators:
            columns.extend(aggregator.columns())
        
        print(';'.join(map(str, columns)))

    @staticmethod
    def print_headers():
        columns = ['datetime',
                   'req_cnt',
                   'avg_resp_time']

        for regex_pattern, log_attribute_name in categories():
            columns.append('req_cnt_{}_{}'.format(log_attribute_name, regex_pattern))
            columns.append('avg_resp_time_{}_{}'.format(log_attribute_name, regex_pattern))

        print(';'.join(columns))
