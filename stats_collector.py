# -*- coding: utf-8 -*-
from log_batch import LogBatch
from datetime import timedelta


"""Group log entries into batches of desired `interval` length [s]

Process log entries one by one. For each new entry decide if it fits to
already open batch, or current batch should be closed and the entry should
begin a new batch.
"""
class StatsCollector:

    interval = None
    current_batch = None
    current_batch_end_datetime = None

    @classmethod
    def append(cls, log):
        if not cls.current_batch or log.datetime >= cls.current_batch_end_datetime:
            cls.start_new_batch(log.datetime)
        cls.current_batch.append(log)

    @classmethod
    def initialize(cls, interval):
        cls.interval = interval
        LogBatch.print_headers()

    @classmethod
    def start_new_batch(cls, batch_start_datetime):
        cls.close()
        cls.current_batch_end_datetime = batch_start_datetime + timedelta(seconds=cls.interval)
        cls.current_batch = LogBatch(batch_start_datetime)

    @classmethod
    def close(cls):
        if cls.current_batch:
            cls.current_batch.close()