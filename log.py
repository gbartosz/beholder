# -*- coding: utf-8 -*-
import re
from datetime import datetime

PATTERN = r'\[(\d{2}\/\S{3}\/\d{4}\:\d{2}:\d{2}:\d{2}\ \+\d{4})\]\ (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})[^\"]*\"(\S*)\s(\S*)\s\S*\srequest_time:\s(\S*)\sstatus:\s(\S*)\sbytes:\s\S*\s"[^"]*"\sto:\s(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,4}|\-)\supstream_response_time:\s(\S*)'

class Log:

    def __init__(self, line):
        matches = re.findall(PATTERN, line)[0]

        self.datetime               = datetime.strptime(matches[0], '%d/%b/%Y:%H:%M:%S %z')
        self.client_address         = matches[1]
        self.method                 = matches[2]
        self.endpoint               = matches[3]
        self.request_time           = float(matches[4])
        self.status_code            = matches[5]
        self.upstream_address       = matches[6]
        self.upstream_response_time = float(matches[7]) if matches[7]!='-' else 0.

    def __repr__(self):
        return (8*"{}\t").format(self.datetime,
                                 self.client_address,
                                 self.method, 
                                 self.request_time, 
                                 self.status_code, 
                                 self.upstream_address, 
                                 self.upstream_response_time, 
                                 self.endpoint)