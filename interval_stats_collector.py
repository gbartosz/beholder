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
        number_of_requests                  = len(self.logs)
        upstream_summary_response_time      = 0.0
        summary_response_time_per_code      = {}
        summary_response_time_per_method    = {}
        summary_response_time_per_endpoint  = {}
        number_of_requests_per_code         = {}
        number_of_requests_per_method       = {}
        number_of_requests_per_endpoint     = {}

        for code in Arguments.codes:
            summary_response_time_per_code[code] = 0.
            number_of_requests_per_code[code] = 0

        for method in Arguments.methods:
            summary_response_time_per_method[method] = 0.
            number_of_requests_per_method[method] = 0

        for endpoint in Arguments.endpoints:
            summary_response_time_per_endpoint[endpoint] = 0.
            number_of_requests_per_endpoint[endpoint] = 0            

        for log in self.logs:
            upstream_summary_response_time += log.request_time

            for code in Arguments.codes:
                if re.match(code, log.status_code):
                    summary_response_time_per_code[code]  += log.request_time
                    number_of_requests_per_code[code]     += 1

            for method in Arguments.methods:
                if re.match(method, log.method):
                    summary_response_time_per_method[method]  += log.request_time
                    number_of_requests_per_method[method]     += 1

            for endpoint in Arguments.endpoints:
                if re.match(endpoint, log.endpoint):
                    summary_response_time_per_endpoint[endpoint]  += log.request_time
                    number_of_requests_per_endpoint[endpoint]     += 1


        columns = [self.start_datetime,
                   number_of_requests,
                   upstream_summary_response_time/number_of_requests]

        for code in summary_response_time_per_code:
            columns.append(number_of_requests_per_code[code])
            columns.append(summary_response_time_per_code[code]/number_of_requests_per_code[code] if number_of_requests_per_code[code] else 0)

        for method in summary_response_time_per_method:
            columns.append(number_of_requests_per_method[method])
            columns.append(summary_response_time_per_method[method]/number_of_requests_per_method[method] if number_of_requests_per_method[method] else 0)

        for endpoint in summary_response_time_per_endpoint:
            columns.append(number_of_requests_per_endpoint[endpoint])
            columns.append(summary_response_time_per_endpoint[endpoint]/number_of_requests_per_endpoint[endpoint] if number_of_requests_per_endpoint[endpoint] else 0)

        print(';'.join(map(str,columns)))

    @staticmethod
    def print_headers():
        columns = ['datetime',
                   'number_of_requests',
                   'average_response_time']
        
        for code in Arguments.codes:
            columns.append('number_of_requests_with_response_{}'.format(code))
            columns.append('average_{}_response_time'.format(code))
        
        for method_or_endpoint in Arguments.methods + Arguments.endpoints:
            columns.append('number_of_{}_requests'.format(method_or_endpoint))
            columns.append('average_{}_response_time'.format(method_or_endpoint))

        print(';'.join(columns))
