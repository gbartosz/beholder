# -*- coding: utf-8 -*-
import re
from datetime import datetime
from arguments import Arguments

PATTERN = r'\[(\d{2}\/\S{3}\/\d{4}\:\d{2}:\d{2}:\d{2}\ \+\d{4})\]\ (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})[^\"]*\"(\S*)\s(\S*)\s\S*\srequest_time' \
          r':\s(\S*)\sstatus:\s(\S*)\sbytes:\s\S*\s"[^"]*"\sto:\s(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,4}|\-)\supstream_response_time:\s(\S*)'


def categories():    
    CATEGORIES = {
        "client_address" : Arguments.client_addresses,
        "method" : Arguments.methods,
        "endpoint" : Arguments.endpoints,
        "status_code" : Arguments.codes,
        "upstream_address" : Arguments.upstream_addresses,
    }
    for log_attribute_name, regex_patterns_list in CATEGORIES.items():
            for regex_pattern in regex_patterns_list:
                yield regex_pattern, log_attribute_name


class Log:

    def __init__(self, line):
        matches = re.findall(PATTERN, line)[0]

        self.datetime = datetime.strptime(matches[0], '%d/%b/%Y:%H:%M:%S %z')
        self.client_address = matches[1]
        self.method = matches[2]
        self.endpoint = matches[3]
        self.request_time = float(matches[4])
        self.status_code = matches[5]
        self.upstream_address = matches[6]
        self.upstream_response_time = float(matches[7]) if matches[7] != '-' else 0.

    #[02/Jul/2019:16:49:35 +0200] 83.210.40.132 (#1) "POST /mainapi/ HTTP/1.1" request_time: 1.396 status: 201 bytes: 959 "POST /mainapi/ID00611623 HTTP/1.1" to: 83.210.0.85:8000 upstream_response_time: 1.396'
    def __repr__(self):
        return """[{} +0000] {} (#1) "{} {} HTTP/1.1" request_time: {:.3f} status: {} bytes: 112 "{} {} HTTP/1.1" to: {} upstream_response_time: {:.3f}"""\
                .format(self.datetime.strftime('%d/%b/%Y:%H:%M:%S'),
                        self.client_address,
                        self.method,
                        self.endpoint,
                        self.request_time,
                        self.status_code,
                        self.method,
                        self.endpoint,
                        self.upstream_address,
                        self.upstream_response_time)
