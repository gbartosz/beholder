# -*- coding: utf-8 -*-
from log import categories
from aggregator import Aggregator


"""Aggregates a batch of log entries that fit into single interval

LogBatch creates a bunch of at least one aggregators. 
First aggregator is default and matches every log entry.
More aggregators are created depending on argument parameters.

When the batch is closed, it feeds logs into the aggregators, collects statistics 
from aggregators and prints them in a colon separated manner to create a csv output.

It also prints headers for .csv output
"""
class LogBatch:

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

        for aggregator in LogBatch.create_aggregators():
            columns.extend(aggregator.headers())
        
        print(';'.join(columns))
