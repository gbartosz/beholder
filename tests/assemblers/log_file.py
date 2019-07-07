from tests.assemblers.log import LogAssembler
from datetime import datetime, timedelta
from random import randint, random

HTTP_STATUSES = ['200', '201', '400', '404', '500', '502']
HTTP_METHODS = ['GET', 'OPTION', 'HEAD', 'PUT', 'PATCH', 'POST', 'DELETE']
ENDPOINTS = ['/product', '/product/id' '/user', '/user/id', '/items', '/items/parts/id']

class LogFileAssembler:

	def __init__(self):
		self.number_of_logs = 10
		self.log_start_date = datetime.now()
		self.log_end_date = self.log_start_date + timedelta(seconds=self.number_of_logs)
		self.update_duration()

	def update_duration(self):
		self.log_duration = self.log_end_date - self.log_start_date

	def random_address(self):
		return '.'.join([str(randint(0,255)) for _ in range(4)])

	def random_port(self):
		return ':{}'.format(randint(1,9999))

	def random_method(self):
		return HTTP_METHODS[randint(0,len(HTTP_METHODS)-1)]

	def random_endpoint(self):
		return ENDPOINTS[randint(0,len(ENDPOINTS)-1)]

	def random_status_code(self):
		return HTTP_STATUSES[randint(0,len(HTTP_STATUSES)-1)]

	def random_duration(self, max_dur=10):
		return max_dur*random()*random()

	def with_number_of_logs(self, value):
		self.number_of_logs = value
		return self

	def with_log_start_date(self, value):
		self.log_start_date = value
		self.update_duration()
		return self

	def with_log_end_date(self, value):
		self.log_end_date = value
		self.update_duration()
		return self

	def build(self):
		for i in range(self.number_of_logs):
			print(LogAssembler().with_datetime(self.log_start_date+i*self.log_duration/self.number_of_logs)
								.with_client_address(self.random_address())	
								.with_method(self.random_method())
								.with_endpoint(self.random_endpoint())
								.with_request_time(self.random_duration())
								.with_status_code(self.random_status_code())
								.with_upstream_address(self.random_address() + self.random_port())
								.with_upstream_response_time(factor_of_request_time=random())
								.with_byte_count(randint(10,10000))
								.with_request_number(randint(1,50))
								.build())

