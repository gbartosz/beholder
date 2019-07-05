from interval_stats_collector import IntervalStatsCollector
from datetime import timedelta


class StatsCollector:

	interval = None
	interval_stats_collector = None
	current_interval_end_datetime = None


	@classmethod
	def append(cls, log):
		if not cls.interval_stats_collector or log.datetime > cls.current_interval_end_datetime:
			cls.start_new_interval(log.datetime)
		cls.interval_stats_collector.append(log)


	@classmethod
	def initialize(cls, interval):
		cls.interval = interval
		IntervalStatsCollector.print_headers()


	@classmethod
	def start_new_interval(cls, interval_start_datetime):
		if cls.interval_stats_collector:
			cls.interval_stats_collector.close()
		cls.current_interval_end_datetime = interval_start_datetime + timedelta(seconds=cls.interval)
		cls.interval_stats_collector = IntervalStatsCollector(interval_start_datetime)