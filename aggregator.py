# -*- coding: utf-8 -*-
import re


class Aggregator:

    def __init__(self, regex_pattern=None, log_attribute_name=None):
        self.regex_pattern = regex_pattern
        self.log_attribute_name = log_attribute_name
        self.request_count = 0
        self.response_time_sum = 0.

    def process(self, log):
        if self.is_default_aggregator or self.matches_log(log):
            self.request_count += 1
            self.response_time_sum += log.request_time

    def columns(self):
        return [self.request_count, self.average_response_time]

    def headers(self):
        default_headers = ['req_cnt', 'avg_resp_time']
        if not self.is_default_aggregator:
            return ['{}_{}_{}'.format(header, self.log_attribute_name, self.regex_pattern) for header in default_headers]
        return default_headers
    
    def matches_log(self, log):
        return re.match(self.regex_pattern, getattr(log, self.log_attribute_name))

    @property
    def is_default_aggregator(self):
        return not self.regex_pattern or not self.log_attribute_name

    @property
    def average_response_time(self):
        return self.response_time_sum / self.request_count if self.request_count else 0.