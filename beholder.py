# -*- coding: utf-8 -*-
from arguments import Arguments
from log import Log
from stats_collector import StatsCollector
from time import sleep


class Beholder:

    @classmethod
    def parse(cls, line):
        try:
            StatsCollector.append(Log(line))
        except Exception as e:
            # print('Exception while processing line:\n{}\n{}'.format(line, e))
            pass

    @classmethod
    def lines_generator(cls, file):
        while True:
            line = file.readline()
            if line:
                yield line
            else:
                if not Arguments.online_mode:
                    return
                sleep(Arguments.interval)

    @classmethod
    def process(cls, filename):
        try:
            file = open(filename, 'r')
            for line in cls.lines_generator(file):
                cls.parse(line.strip())
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    Arguments.parse()
    StatsCollector.initialize(Arguments.interval)
    Beholder.process(Arguments.filename)
