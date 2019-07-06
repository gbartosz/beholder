# Beholder
Process web server log file and gather information about `number of requests` and `average response time` per category per specified time interval. It specifically targets nginx in a reverse-proxy setup with specific log format (see log.py), but can easily be customized to other log formats.

# Interval
Beholder accepts an `interval` as an input parameter. It groups log entries in batches of `interval` seconds length to count requests and average response times per batch.

# Categories
If you run this script with `-h` option you will get a list of currently supported categories. Basic categories are:

`-c` (response status `CODES`)

`-m` (http `METHODS`)

`-e` (`ENDPOINTS` urls)

`-u` (`UPSTREAM_ADDRESSES`)

`-a` (`CLIENT_ADDRESSES`)

Beholder supports multiple categories as well as multiple values per category.

# Example commands
<code>python beholder.py -i 600 -f file.log -c 499 > output.csv</code>

processes file.log, groups logs in batches of 600 seconds, calculates statistics per batch and creates output.csv file with column headers:

<code>datetime;req_cnt;avg_resp_time;req_cnt_status_code_499;avg_resp_time_status_code_499</code>

and a single row per 600s batch of log entries.

You can specify multiple codes:

<code>python beholder.py -i 600 -f file.log -c '499;502' > output.csv</code>

creates output.csv file with column headers:

<code>datetime;req_cnt;avg_resp_time;req_cnt_status_code_499;avg_resp_time_status_code_499;req_cnt_status_code_502;avg_resp_time_status_code_502</code>

You can also use regular expressions in code definitions:

<code>python beholder.py -i 600 -f file.log -c '499;502;2..' > output.csv</code>

creates output.csv file with column headers:

<code>datetime;req_cnt;avg_resp_time;req_cnt_status_code_499;avg_resp_time_status_code_499;req_cnt_status_code_502;avg_resp_time_status_code_502;req_cnt_status_code_2..;avg_resp_time_status_code_2..</code>

where `2..` matches all success response codes.

Same rules apply to specifying http `METHODS` and `ENDPOINTS` urls, so:

<code>python beholder.py -i 600 -f file.log -c '499;502;5..' -m 'GET;P.{2,}' -e '/isn/api/' > output.csv</code>

creates output.csv file with column headers:

<code>datetime;req_cnt;avg_resp_time;req_cnt_method_GET;avg_resp_time_method_GET;req_cnt_method_P.{2,};avg_resp_time_method_P.{2,};req_cnt_endpoint_/isn/api/;avg_resp_time_endpoint_/isn/api/;req_cnt_status_code_499;avg_resp_time_status_code_499;req_cnt_status_code_502;avg_resp_time_status_code_502;req_cnt_status_code_5..;avg_resp_time_status_code_5..</code>

# Regexp rules
If you provide 

<code>-m 'POST;P.{2,}'</code> 

columns `req_cnt_method_POST` and `avg_resp_time_method_POST` will match only `POST` requests, while columns `req_cnt_method_P.{2,}` and `avg_resp_time_method_P.{2,}` will match `POST`,`PUT` and `PATCH` requests. 

Specifying `POST` as an explicit method to monitor, does not exclude it from regex-matched method to monitor (`P.{2,}`).

Same rules apply to other categories.

# Online mode
By default `beholder` will process entire log file and exit. If you want to monitor your web-server in real-time enable `-o` option to read events appended to the log file.

# Separator
Default separator of multiple values per category is a colon (`;`). If you need to use colon in regular expression, a conflict occurs. To resolve this issue change default separator using `-s` option.

Output column separation disregards this setting and always uses a colon.