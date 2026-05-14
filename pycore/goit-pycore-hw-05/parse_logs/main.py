from rich import print
from rich.table import Table
from helpers import load_logs, filter_logs_by_level, count_logs_by_level, display_log_counts

# parse logs
def parse_logs(path: str, level: str = None):

    # load logs from file to list
    parsed_lines = load_logs(path)
    # count logs by level
    counts = count_logs_by_level(parsed_lines)
    # display log counts in table
    display_log_counts(counts)

    if level:
        filtered_lines = filter_logs_by_level(parsed_lines, level)

        print(f"\nLogs level '{level.upper()}':\n")

        for log in filtered_lines:
            print(
                f"{log['date']} {log['time']} - {log['message']}"
            )

parse_logs('logs.txt', 'INFO')