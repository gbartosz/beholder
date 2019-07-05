# -*- coding: utf-8 -*-
import argparse

parser = argparse.ArgumentParser(
    description='Process log file in a live manner. Gather requests/sec, average response time and additional stats per returned http status code.')

# GENERAL
parser.add_argument('-i', '--interval', help='interval (in seconds) of gathering stats', action='store', default=60.)
parser.add_argument('-f', '--filename', help='path to observed log file', action='store')
parser.add_argument('-c', '--codes', help='SEPARATOR separated list of http response codes to monitor. Regex expressions are supported.', action='store', default=None)
parser.add_argument('-m', '--methods', help='SEPARATOR separated list of http methods to monitor. Regex expressions are supported.', action='store', default=None)
parser.add_argument('-e', '--endpoints', help='SEPARATOR separated list of endpoints to monitor. Regex expressions are supported.', action='store', default=None)
parser.add_argument('-s', '--separator', help='separator to use when splitting CODES and METHODS. Colon (;) by default', action='store', default=';')
parser.add_argument('-o', '--online_mode', help='do not exit when entire file read. Set this option when processing a file that is being written by external source.', action='store_true')


def argument_list(arg):
    return [a.strip() for a in arg.split(Arguments.separator)] if arg else []


class Arguments:
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

        Arguments.interval = float(args.interval)
        Arguments.filename = args.filename
        Arguments.separator = args.separator
        Arguments.codes = argument_list(args.codes)
        Arguments.methods = argument_list(args.methods)
        Arguments.endpoints = argument_list(args.endpoints)
        Arguments.online_mode = args.online_mode
