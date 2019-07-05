# -*- coding: utf-8 -*-
import re
from arguments import Arguments


class IntervalStatsCollector:

    def __init__(self, start_datetime):
        self.start_datetime = start_datetime
        self.logs = []

    def append(self, log):
        self.logs.append(log)

    def close(self):
        number_of_requests = len(self.logs)
        upstream_summary_response_time = 0.0
        req_cnt_sum = {}
        avg_resp_time = {}

        for category, value_list in Arguments.categories().items():
            for value in value_list:
                req_cnt_sum[category+value] = 0
                avg_resp_time[category+value] = 0.

        for log in self.logs:
            upstream_summary_response_time += log.request_time

            for category, value_list in Arguments.categories().items():
                for value in value_list:
                    if re.match(value, getattr(log, category)):
                        req_cnt_sum[category+value] += 1
                        avg_resp_time[category+value] += log.request_time

        columns = [self.start_datetime,
                   number_of_requests,
                   upstream_summary_response_time / number_of_requests]

        for key, value in req_cnt_sum.items():
            columns.append(value)
            columns.append(avg_resp_time[key] / value if value else 0)

        print(';'.join(map(str, columns)))

    @staticmethod
    def print_headers():
        columns = ['datetime',
                   'req_cnt',
                   'avg_resp_time']

        for value_list in Arguments.categories().values():
            for value in value_list:
                columns.append('req_cnt_{}'.format(value))
                columns.append('avg_resp_time_{}'.format(value))

        print(';'.join(columns))
