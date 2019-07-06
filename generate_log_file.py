from tests.assemblers.log_file import LogFileAssembler
from datetime import datetime, timedelta
import sys

if __name__ == '__main__':
    LogFileAssembler().with_number_of_logs(int(sys.argv[1]))\
                      .with_log_start_date(datetime.now())\
                      .with_log_end_date(datetime.now()+timedelta(seconds=int(sys.argv[2])))\
                      .build()
