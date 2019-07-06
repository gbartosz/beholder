# -*- coding: utf-8 -*-
from log import categories
from aggregator import Aggregator


class IntervalStatsCollector:

    def __init__(self, start_datetime):
        self.start_datetime = start_datetime
        self.logs = []
        self.aggregators = self.create_aggregators()

    def append(self, log):
        self.logs.append(log)

    def close(self):
        for log in self.logs:
            for aggregator in self.aggregators:
                aggregator.process(log)

        columns = [self.start_datetime]

        for aggregator in self.aggregators:
            columns.extend(aggregator.columns())
        
        print(';'.join(map(str, columns)))

    @staticmethod
    def create_aggregators():
        aggregators = [Aggregator()]
        for regex_pattern, log_attribute_name in categories():
            aggregators.append(Aggregator(regex_pattern, log_attribute_name))
        return aggregators

    @staticmethod
    def print_headers():
        columns = ['datetime']

        for aggregator in IntervalStatsCollector.create_aggregators():
            columns.extend(aggregator.headers())
        
        print(';'.join(columns))
