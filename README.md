# dntrc
Process web server log file and gather information about `number of requests` and `average response time` per category per specified time interval.

# categories
If you run this script with `-h` option you will get currently supported categories. Basic categories are:

`-c` (response status `CODES`)

`-m` (http `METHODS`)

`-e` (`ENDPOINTS` urls)

Beholder supports multiple categories as well as multiple values of a single category.

# Example commands
<code>python beholder.py -i 600 -f file.log -c 499 > output.csv</code>

creates output.csv file with column headers:

<code>datetime;number_of_requests;average_response_time;number_of_requests_with_response_499;average_499_response_time</code>

You can specify multiple codes:

<code>python beholder.py -i 600 -f file.log -c '499;502' > output.csv</code>

creates output.csv file with column headers:

<code>datetime;number_of_requests;average_response_time;number_of_requests_with_response_499;average_499_response_time;number_of_requests_with_response_502;average_502_response_time</code>

You can also use regular expressions in code definitions:

<code>python beholder.py -i 600 -f file.log -c '499;502;2..' > output.csv</code>

creates output.csv file with column headers:

<code>datetime;number_of_requests;average_response_time;number_of_requests_with_response_499;average_499_response_time;number_of_requests_with_response_502;average_502_response_time;number_of_requests_with_response_2..;average_2.._response_time</code>

where `2..` matches all success response codes.

Same rules apply to specifying http `METHODS` and `ENDPOINTS` urls, so:

<code>python beholder.py -i 600 -f file.log -c '499;502;5..' -m 'GET;P.{2,}' -e '/isn/api/' > output.csv</code>

creates output.csv file with column headers:

<code>datetime;number_of_requests;average_response_time;number_of_requests_with_response_499;average_499_response_time;number_of_requests_with_response_502;average_502_response_time;number_of_requests_with_response_5..;average_5.._response_time;number_of_GET_requests;average_GET_response_time;number_of_P.{2,}_requests;average_P.{2,}_response_time;number_of_/isn/api/_requests;average_/isn/api/_response_time</code>

# Regexp rules
If you provide 

<code>-m 'POST;P.{2,}'</code> 

columns `number_of_POST_requests` and `average_POST_response_time` will match only `POST` requests, while columns `number_of_P.{2,}_requests` and `average_P.{2,}_response_time` will match `POST`,`PUT` and `PATCH` requests. 

Specifying `POST` as an explicit method to monitor, does not exclude it from regex-matched method to monitor (`P.{2,}`).

Same rules apply to `METHODS` and `ENDPOINTS`.
