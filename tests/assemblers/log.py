from datetime import datetime
from log import Log

SAMPLE_LINE = '[02/Jul/2019:16:49:35 +0200] 83.210.40.132 (#1) "POST /mainapi/ HTTP/1.1" request_time: 1.396 status: 201 bytes: 959 "POST /mainapi/ID00611623 HTTP/1.1" to: 83.210.0.85:8000 upstream_response_time: 1.396'

class LogAssembler:

    def __init__(self):
        self.datetime = datetime.now()
        self.client_address = '0.0.0.0'
        self.method = 'GET'
        self.endpoint = '/test/endpoint'
        self.request_time = 1.0
        self.status_code = '200'
        self.upstream_address = '0.0.0.0:80'
        self.upstream_response_time = 1.0
        self.protocol_version = 'HTTP/1.1'
        self.byte_count = '2222'
        self.request_number = '1'

    def with_datetime(self, value):
        self.datetime = value
        return self
        
    def with_client_address(self, value):
        self.client_address = value
        return self
        
    def with_method(self, value):
        self.method = value
        return self
        
    def with_endpoint(self, value):
        self.endpoint = value
        return self
        
    def with_request_time(self, value):
        self.request_time = value
        return self
        
    def with_status_code(self, value):
        self.status_code = value
        return self
        
    def with_upstream_address(self, value):
        self.upstream_address = value
        return self
        
    def with_protocol_version(self, value):
        self.protocol_version = value
        return self
        
    def with_byte_count(self, value):
        self.byte_count = value
        return self
        
    def with_request_number(self, value):
        self.request_number = value
        return self
        
    def with_upstream_response_time(self, value=None, factor_of_request_time=None):
        if factor_of_request_time:
            self.upstream_response_time = factor_of_request_time*self.request_time
        elif value:
            self.upstream_response_time = value
        else:
            raise ValueError('LogAssembler.with_upstream_response_time should be called with one of `value` or `factor_of_request_time` argument.')
        return self
        
    def build(self):
        log = Log(SAMPLE_LINE)
        log.datetime = self.datetime
        log.client_address = self.client_address
        log.method = self.method
        log.endpoint = self.endpoint
        log.request_time = self.request_time
        log.status_code = self.status_code
        log.upstream_address = self.upstream_address
        log.upstream_response_time = self.upstream_response_time
        log.protocol_version = self.protocol_version
        log.byte_count = self.byte_count
        log.request_number = self.request_number
        return log