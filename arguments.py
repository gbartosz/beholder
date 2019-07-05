import argparse

parser = argparse.ArgumentParser(description='Process log file in a live manner. Gather requests/sec, average response time and additional stats per returned http status code.')

#GENERAL
parser.add_argument('-i', '--interval',     help='interval (in seconds) of gathering stats', action='store', default=60.)
parser.add_argument('-f', '--filename',     help='path to observed log file', action='store')
parser.add_argument('-c', '--codes',        help='SEPARATOR separated list of http response codes to monitor. Regex expressions are supported.', action='store', default=None)
parser.add_argument('-m', '--methods',      help='SEPARATOR separated list of http methods to monitor. Regex expressions are supported.', action='store', default=None)
parser.add_argument('-e', '--endpoints',    help='SEPARATOR separated list of endpoints to monitor. Regex expressions are supported.', action='store', default=None)
parser.add_argument('-s', '--separator',    help='separator to use when splitting CODES and METHODS. Colon (;) by default', action='store', default=';')
parser.add_argument('-o', '--online_mode',  help='do not exit when entire file read. Set this option when processing a file that is being written by external source.', action='store_true')


# [$time_local] $remote_addr (#$connection_requests) "$request_method $request_truncated HTTP/1.1" request_time: $request_time status: $status bytes: $bytes_sent "$request" to: $upstream_addr upstream_response_time: $upstream_response_time';

class Arguments(object):
    interval = None
    codes = None
    filename = None
    methods = None
    endpoints = None
    separator = None
    online_mode = False
    

    @staticmethod
    def parse():
        args = parser.parse_args()

        Arguments.interval      = float(args.interval)
        Arguments.filename      = args.filename
        Arguments.separator     = args.separator
        Arguments.codes         = [code.strip() for code in args.codes.split(Arguments.separator)] if args.codes else []
        Arguments.methods       = [method.strip() for method in args.methods.split(Arguments.separator)] if args.methods else []
        Arguments.endpoints     = [endpoint.strip() for endpoint in args.endpoints.split(Arguments.separator)] if args.endpoints else []
        Arguments.online_mode   = args.online_mode
