# -*- coding: utf-8 -*-
from arguments import Arguments
from log import Log
from stats_collector import StatsCollector
from time import sleep


def parse(line):
    try:
        StatsCollector.append(Log(line))
    except Exception as e:
        print(line)
        print(e)
        raise


def lines_generator(file):
    while True:
        line = file.readline()
        if line:
            yield line
        else:
            sleep(Arguments.interval)


def read_from_file_online(filename):
    try:
        file = open(filename, 'r')
        for line in lines_generator(file):
            parse(line.strip())
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    Arguments.parse()
    StatsCollector.initialize(Arguments.interval)
    read_from_file_online(Arguments.filename)