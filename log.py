# -*- coding: utf-8 -*-
import re
from datetime import datetime
from arguments import Arguments

"""Regular expression that matches single entry in processed log file"""
PATTERN = r'\[(.*)\]\s(\S*)\s\(#(\S*)\)\s"(\S*)\s(\S*)\s([^"]*)"\srequest_time:\s(\S*)\sstatus:\s(\S*)\sbytes:\s(\S*)\s"[^"]*"\sto:\s(\S*)\supstream_response_time:\s(\S*)'


"""Generator that yields tuples of log attribute and regex pattern looked for

Examples:
if `-m 'GET;D.*' is specified as an argument, this generator yields:
    ('GET', 'method')
    ('D.*', 'method')
if `-c '200;4..' -e '/sample/endpoint' -a 0.0.0.0:\d{4}` is specified, categories yields:
    ('200', 'status_code')
    ('4..', 'status_code')
    ('/sample/endpoint', 'endpoint')
    ('0.0.0.0:\d{4}', 'client_address')

This way you can access getattr(log_object, log_attribute_name) and check if it matches regular expression regex_pattern
"""
def categories():    
    #TODO: consider removing the dict if possible
    CATEGORIES = {
        "client_address" : Arguments.client_addresses,
        "method" : Arguments.methods,
        "endpoint" : Arguments.endpoints,
        "status_code" : Arguments.codes,
        "upstream_address" : Arguments.upstream_addresses,
        "byte_count" : Arguments.byte_count,
        "request_number": Arguments.request_number,
        "protocol_version": Arguments.protocol_version
    }
    for log_attribute_name, regex_patterns_list in CATEGORIES.items():
            for regex_pattern in regex_patterns_list:
                yield regex_pattern, log_attribute_name


"""Defines a structure looked for in each log entry

If you need to support any other log formats - this file is where you start.
If you need to extract more fields from log entry - you need to add more categories in arguments.py as well.
"""
class Log:

    def __init__(self, line):
        matches = re.findall(PATTERN, line)[0]

        self.datetime = datetime.strptime(matches[0], '%d/%b/%Y:%H:%M:%S %z')
        self.client_address = matches[1]
        self.request_number = matches[2]
        self.method = matches[3]
        self.endpoint = matches[4]
        self.protocol_version = matches[5]
        self.request_time = float(matches[6])
        self.status_code = matches[7]
        self.byte_count = matches[8]
        self.upstream_address = matches[9]
        self.upstream_response_time = float(matches[10]) if matches[10] != '-' else 0.

    #[02/Jul/2019:16:49:35 +0200] 83.210.40.132 (#1) "POST /mainapi/ HTTP/1.1" request_time: 1.396 status: 201 bytes: 959 "POST /mainapi/ID00611623 HTTP/1.1" to: 83.210.0.85:8000 upstream_response_time: 1.396'
    def __repr__(self):
        return """[{} +0000] {} (#{}) "{} {} {}" request_time: {:.3f} status: {} bytes: {} "{} {} HTTP/1.1" to: {} upstream_response_time: {:.3f}"""\
                .format(self.datetime.strftime('%d/%b/%Y:%H:%M:%S'),
                        self.client_address,
                        self.request_number,
                        self.method,
                        self.endpoint,
                        self.protocol_version,
                        self.request_time,
                        self.status_code,
                        self.byte_count,
                        self.method,
                        self.endpoint,
                        self.upstream_address,
                        self.upstream_response_time)
